#!/usr/bin/env python3
"""Local checkpoint evidence ledger. Python 3.10+, Git; no network or LLM calls."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone
from uuid import uuid4


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False).encode()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE)


def fingerprint(root, plan):
    """Hash tracked + nonignored untracked files, including deletions and modes."""
    require(Path(os.fsdecode(git(root, "rev-parse", "--show-toplevel")).strip()).resolve() == root,
            "--project must be the Git repository root")
    names = set(git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard").split(b"\0"))
    entries = []
    for name in sorted(names):
        if not name or name.startswith(b".ratchet/"):
            continue
        path = root / os.fsdecode(name)
        if path.is_symlink():
            payload, kind = os.fsencode(os.readlink(path)), "link"
        elif path.is_file():
            payload, kind = path.read_bytes(), "executable" if path.stat().st_mode & 0o111 else "file"
        elif path.is_dir():
            raise ValueError("Submodules are not fingerprinted; use a separate checkpoint in " + str(path))
        else:
            payload, kind = b"", "deleted"
        entries.append([os.fsdecode(name), kind, digest(payload)])
    return digest(encoded({"files": entries, "plan": plan}))


def validate_plan(plan):
    require(isinstance(plan, dict), "Plan must be a JSON object")
    for field in ("title", "reference", "implementer_session"):
        require(nonempty(plan.get(field)), "Plan requires " + field)
    require(isinstance(plan.get("acceptance"), list) and plan["acceptance"]
            and all(nonempty(x) for x in plan["acceptance"]), "Plan requires observable acceptance criteria")
    require(type(plan.get("ui")) is bool, "Plan.ui must be true or false")
    if not plan["ui"]:
        require(nonempty(plan.get("ui_skip_reason")), "Logic-only plan requires ui_skip_reason")
    require(type(plan.get("max_attempts")) is int and 1 <= plan["max_attempts"] <= 20,
            "max_attempts must be 1..20")


def gates(plan):
    return ["behavior"] + (["ui"] if plan["ui"] else []) + ["review-a", "review-b", "approval"]


def evidence_file(folder, relative):
    require(nonempty(relative), "Artifact path must be a nonempty string")
    path = (folder / relative).resolve()
    require(path.is_relative_to((folder / "evidence").resolve()) and path.is_file(),
            "Artifacts must be existing files inside this checkpoint's evidence/ directory")
    require(path.stat().st_size > 0, "Empty artifacts cannot substantiate a verdict")
    return path


def record_valid(folder, record, revision):
    if record.get("revision") != revision or record.get("verdict") != "pass":
        return False
    try:
        if digest((folder / record["report"]).read_bytes()) != record["report_sha256"]:
            return False
        return all(digest(evidence_file(folder, name).read_bytes()) == sha
                   for name, sha in record["artifacts"].items())
    except (OSError, ValueError, KeyError):
        return False


def check(root, folder, plan, state):
    current = fingerprint(root, plan)
    errors = []
    if state.get("revision") != current:
        errors.append("Code or plan changed (or no snapshot); snapshot again and rerun all gates")
    for gate in gates(plan):
        if not record_valid(folder, state["gates"].get(gate, {}), current):
            errors.append(gate + ": missing, failed, or stale evidence")
    return errors


def execute(args):
    root = Path(args.project).expanduser().resolve()
    require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.checkpoint), "Invalid checkpoint identifier")
    folder = root / ".ratchet" / "checkpoints" / args.checkpoint
    require(folder.resolve().is_relative_to(root), "Checkpoint path escapes the project")
    if args.command == "init":
        plan = read(Path(args.plan))
        validate_plan(plan)
        fingerprint(root, plan)
        require(not folder.exists(), "Checkpoint already exists")
        folder.mkdir(parents=True)
        (folder / "evidence").mkdir()
        (folder / "reports").mkdir()
        write(folder / "plan.json", plan)
        write(folder / "state.json", {"schema": 1, "attempts": 0, "revision": None,
                                      "closed": False, "gates": {}, "history": []})
        return {"checkpoint": str(folder), "next": "Implement, then snapshot before collecting evidence"}
    plan, state = read(folder / "plan.json"), read(folder / "state.json")
    validate_plan(plan)
    require(state.get("schema") == 1, "Unsupported ledger schema")
    if args.command in ("check", "status"):
        errors = check(root, folder, plan, state)
        return {"ready": not errors, "closed": state["closed"], "revision": state["revision"],
                "attempts": state["attempts"], "errors": errors}
    require(not state["closed"], "Checkpoint closed; create a new checkpoint for follow-up changes")
    if args.command == "snapshot":
        require(state["attempts"] < plan["max_attempts"], "Retry budget exhausted; request a scoped budget change")
        state["attempts"] += 1
        state["revision"] = fingerprint(root, plan)
        state["gates"] = {}
        state["history"].append({"event": "snapshot", "revision": state["revision"]})
    elif args.command == "record":
        current = fingerprint(root, plan)
        require(state["revision"] == current, "Code or plan changed; snapshot and rerun gates")
        report = read(Path(args.report))
        require(isinstance(report, dict), "Report must be a JSON object")
        gate = report.get("gate")
        require(gate in gates(plan), "Gate is unknown or inapplicable")
        require(report.get("revision") == current, "Report must name the current snapshot revision")
        for prior in gates(plan)[:gates(plan).index(gate)]:
            require(record_valid(folder, state["gates"].get(prior, {}), current),
                    "Pass earlier gate first: " + prior)
        require(report.get("verdict") in ("pass", "fail", "blocked"), "Invalid verdict")
        for field in ("actor", "session", "summary"):
            require(nonempty(report.get(field)), "Report requires " + field)
        require(isinstance(report.get("findings"), list), "Report requires findings array")
        require(report["verdict"] != "pass" or not report["findings"],
                "Resolve findings before passing; keep accepted tradeoffs in summary")
        if gate.startswith("review-"):
            require(report["session"] != plan["implementer_session"], "Self-review is not independent")
            other = state["gates"].get("review-a", {})
            if gate == "review-b":
                require(report["session"] != other.get("session"), "Reviewers must use distinct sessions")
        if gate == "approval":
            require(report.get("authority") in ("human", "explicit-delegation"),
                    "Approval needs a human decision or explicit prior delegation")
        require(isinstance(report.get("artifacts"), list) and report["artifacts"], "Evidence artifacts required")
        artifacts = {p: digest(evidence_file(folder, p).read_bytes()) for p in report["artifacts"]}
        target = "reports/" + gate + "-" + uuid4().hex + ".json"
        write(folder / target, report)
        entry = {"revision": current, "verdict": report["verdict"], "session": report["session"],
                 "report": target, "report_sha256": digest((folder / target).read_bytes()), "artifacts": artifacts}
        for downstream in gates(plan)[gates(plan).index(gate):]:
            state["gates"].pop(downstream, None)
        state["gates"][gate] = entry
        state["history"].append({"event": "record", "gate": gate, **entry})
    elif args.command == "close":
        errors = check(root, folder, plan, state)
        require(not errors, "; ".join(errors))
        state["closed"] = True
        state["history"].append({"event": "close", "revision": state["revision"]})
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    write(folder / "state.json", state)
    return {"revision": state["revision"], "attempts": state["attempts"], "closed": state["closed"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=".", help="Git repository root")
    parser.add_argument("--checkpoint", required=True, help="Unique lowercase checkpoint slug")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init").add_argument("--plan", required=True)
    for name in ("snapshot", "status", "check", "close"):
        commands.add_parser(name)
    commands.add_parser("record").add_argument("--report", required=True)
    args = parser.parse_args()
    try:
        result = execute(args)
        print(json.dumps(result, indent=2))
        return 1 if args.command == "check" and not result["ready"] else 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print("ratchet: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
