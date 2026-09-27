import importlib.util
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("installer", ROOT / "scripts/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        output = redirect_stdout(StringIO())
        output.__enter__()
        self.addCleanup(output.__exit__, None, None, None)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()

    def test_every_host_receives_complete_skill_and_script(self):
        for agent, location in installer.TARGETS.items():
            with self.subTest(agent=agent):
                project = self.root / agent
                project.mkdir()
                self.assertEqual(installer.install(project, [agent]), 6)
                self.assertTrue((project / location / "ratchet/scripts/checkpoint.py").is_file())
                self.assertEqual(len(list((project / location).glob("*/SKILL.md"))), 6)

    def test_dry_run_writes_nothing(self):
        self.assertEqual(installer.install(self.root, ["codex"], True), 6)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_repeat_install_is_noop(self):
        installer.install(self.root, ["claude"])
        self.assertEqual(installer.install(self.root, ["claude"]), 0)

    def test_shared_destinations_are_deduplicated(self):
        self.assertEqual(installer.install(self.root, ["codex", "antigravity", "kimi"]), 6)

    def test_collision_preflight_prevents_partial_install(self):
        path = self.root / ".agents/skills/ratchet-memory"
        path.mkdir(parents=True)
        (path / "SKILL.md").write_text("User's customized skill", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "differs"):
            installer.install(self.root, ["codex", "claude"])
        self.assertFalse((self.root / ".agents/skills/ratchet").exists())
        self.assertFalse((self.root / ".claude").exists())
        self.assertEqual((path / "SKILL.md").read_text(encoding="utf-8"), "User's customized skill")

    def test_preserves_existing_agent_config(self):
        (self.root / "AGENTS.md").write_text("Project instructions", encoding="utf-8")
        installer.install(self.root, ["codex"])
        self.assertEqual((self.root / "AGENTS.md").read_text(encoding="utf-8"), "Project instructions")


if __name__ == "__main__":
    unittest.main()
