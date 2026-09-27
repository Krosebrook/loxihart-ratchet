"""Behavioral contract tests; reviewer/approval records here are synthetic fixtures."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/loxihart-ratchet/skills/ratchet/scripts/checkpoint.py"
spec = importlib.util.spec_from_file_location("checkpoint", SCRIPT)
ledger = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ledger)


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / ".gitignore").write_text(".ratchet/\nignored.txt\n", encoding="utf-8")
        (self.root / "app.py").write_text("value = 1\n", encoding="utf-8")
        self.plan = {"title": "Preserve a value", "reference": "Existing public constant",
                     "acceptance": ["value remains 1"], "ui": False, "ui_skip_reason": "No interface",
                     "implementer_session": "implementation-session", "max_attempts": 3}
        self.planfile = self.root / ".ratchet" / "input.json"
        self.planfile.parent.mkdir()
        ledger.write(self.planfile, self.plan)
        self.folder = self.root / ".ratchet/checkpoints/cp-01"
        self.run_command("init", plan=str(self.planfile))
        self.revision = self.run_command("snapshot")["revision"]

    def run_command(self, command, **kwargs):
        return ledger.execute(SimpleNamespace(project=str(self.root), checkpoint="cp-01", command=command, **kwargs))

    def record(self, gate, **kwargs):
        artifact = self.folder / "evidence" / (gate + ".txt")
        artifact.write_text("Synthetic test fixture: " + gate, encoding="utf-8")
        report = {"gate": gate, "revision": self.revision, "verdict": "pass",
                  "actor": "fixture", "session": gate + "-session", "summary": "Synthetic verdict for ledger tests",
                  "findings": [], "artifacts": ["evidence/" + artifact.name]}
        if gate == "approval":
            report["authority"] = "human"
        report.update(kwargs)
        path = self.folder / "evidence/input.json"
        ledger.write(path, report)
        return self.run_command("record", report=str(path))

    def pass_all(self):
        for gate in ledger.gates(ledger.read(self.folder / "plan.json")):
            self.record(gate)

    def test_complete_logic_checkpoint_can_close_without_ui(self):
        self.pass_all()
        self.assertTrue(self.run_command("check")["ready"])
        self.assertTrue(self.run_command("close")["closed"])
        with self.assertRaisesRegex(ValueError, "closed"):
            self.run_command("snapshot")

    def test_cannot_skip_gate_order_or_close_early(self):
        with self.assertRaisesRegex(ValueError, "earlier gate"):
            self.record("review-a")
        with self.assertRaisesRegex(ValueError, "missing"):
            self.run_command("close")

    def test_new_untracked_file_invalidates_all_reviews(self):
        self.pass_all()
        (self.root / "new.py").write_text("value = 2\n", encoding="utf-8")
        self.assertFalse(self.run_command("check")["ready"])
        with self.assertRaisesRegex(ValueError, "changed"):
            self.record("behavior")

    def test_tracked_deletion_changes_revision(self):
        subprocess.run(["git", "-C", str(self.root), "add", "app.py"], check=True)
        self.revision = self.run_command("snapshot")["revision"]
        self.pass_all()
        (self.root / "app.py").unlink()
        self.assertFalse(self.run_command("check")["ready"])

    def test_plan_change_invalidates_approval(self):
        self.pass_all()
        plan = ledger.read(self.folder / "plan.json")
        plan["acceptance"].append("Another behavior")
        ledger.write(self.folder / "plan.json", plan)
        self.assertFalse(self.run_command("check")["ready"])

    def test_artifact_edit_invalidates_gate(self):
        self.pass_all()
        (self.folder / "evidence/behavior.txt").write_text("Changed after review", encoding="utf-8")
        self.assertFalse(self.run_command("check")["ready"])

    def test_archived_report_edit_invalidates_gate(self):
        self.pass_all()
        state = ledger.read(self.folder / "state.json")
        report = self.folder / state["gates"]["review-a"]["report"]
        report.write_text("{}", encoding="utf-8")
        self.assertFalse(self.run_command("check")["ready"])

    def test_replacing_earlier_gate_clears_later_approvals(self):
        self.pass_all()
        self.record("behavior", verdict="fail", findings=["Observed regression"])
        state = ledger.read(self.folder / "state.json")
        self.assertEqual(set(state["gates"]), {"behavior"})
        self.assertFalse(self.run_command("check")["ready"])
        self.assertGreater(len(state["history"]), 4)

    def test_rejects_self_review_and_duplicate_sessions(self):
        self.record("behavior")
        with self.assertRaisesRegex(ValueError, "Self-review"):
            self.record("review-a", session="implementation-session")
        self.record("review-a")
        with self.assertRaisesRegex(ValueError, "distinct"):
            self.record("review-b", session="review-a-session")

    def test_ui_checkpoint_requires_actual_ui_gate(self):
        plan = ledger.read(self.folder / "plan.json")
        plan["ui"] = True
        ledger.write(self.folder / "plan.json", plan)
        self.revision = self.run_command("snapshot")["revision"]
        self.record("behavior")
        with self.assertRaisesRegex(ValueError, "ui"):
            self.record("review-a")
        self.record("ui", verdict="blocked", findings=["No screenshots"])
        self.assertFalse(self.run_command("check")["ready"])

    def test_retry_budget_is_bounded(self):
        self.run_command("snapshot")
        self.run_command("snapshot")
        with self.assertRaisesRegex(ValueError, "budget exhausted"):
            self.run_command("snapshot")

    def test_complete_ui_checkpoint_closes_with_all_five_records(self):
        plan = ledger.read(self.folder / "plan.json")
        plan["ui"] = True
        ledger.write(self.folder / "plan.json", plan)
        self.revision = self.run_command("snapshot")["revision"]
        self.pass_all()
        self.assertTrue(self.run_command("close")["closed"])

    def test_code_fix_requires_new_snapshot_and_new_verdicts(self):
        self.pass_all()
        (self.root / "app.py").write_text("value = 2\n", encoding="utf-8")
        self.revision = self.run_command("snapshot")["revision"]
        self.assertFalse(self.run_command("check")["ready"])
        self.pass_all()
        self.assertTrue(self.run_command("close")["closed"])

    def test_report_must_reference_current_revision(self):
        with self.assertRaisesRegex(ValueError, "current snapshot"):
            self.record("behavior", revision="stale")

    def test_missing_or_outside_evidence_is_rejected(self):
        for paths in (["evidence/missing.txt"], ["../../../../app.py"], []):
            with self.subTest(paths=paths), self.assertRaises(ValueError):
                self.record("behavior", artifacts=paths)

    def test_passing_report_cannot_hide_unresolved_findings(self):
        with self.assertRaisesRegex(ValueError, "Resolve findings"):
            self.record("behavior", findings=["Data loss"])

    def test_approval_requires_declared_authority(self):
        for gate in ("behavior", "review-a", "review-b"):
            self.record(gate)
        with self.assertRaisesRegex(ValueError, "Approval needs"):
            self.record("approval", authority="tests-passed")
        self.record("approval", authority="explicit-delegation")
        self.assertTrue(self.run_command("check")["ready"])

    def test_evidence_writes_and_ignored_data_do_not_change_revision(self):
        self.pass_all()
        (self.root / "ignored.txt").write_text("documented excluded input", encoding="utf-8")
        (self.folder / "evidence/extra.txt").write_text("extra observation", encoding="utf-8")
        self.assertTrue(self.run_command("check")["ready"])

    def test_init_refuses_overwrite_and_invalid_plan(self):
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.run_command("init", plan=str(self.planfile))
        self.plan["ui_skip_reason"] = ""
        with self.assertRaisesRegex(ValueError, "ui_skip_reason"):
            ledger.validate_plan(self.plan)

    def test_cli_exit_codes(self):
        base = [sys.executable, str(SCRIPT), "--project", str(self.root), "--checkpoint", "cp-01"]
        self.assertEqual(subprocess.run(base + ["check"], capture_output=True).returncode, 1)
        self.assertEqual(subprocess.run(base + ["status"], capture_output=True).returncode, 0)
        self.assertEqual(subprocess.run(base + ["close"], capture_output=True).returncode, 2)
        self.pass_all()
        self.assertEqual(subprocess.run(base + ["check"], capture_output=True).returncode, 0)


if __name__ == "__main__":
    unittest.main()
