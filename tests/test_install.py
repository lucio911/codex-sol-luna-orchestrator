"""Unit tests for local safe install and configuration behavior."""
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from install import install, desired_config, get_destinations, modify_toml, validate_model_id
from doctor import diagnose
from validate import validate


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_install_and_idempotency(self):
        first = install(scope="project", project_root=self.root)
        self.assertTrue(any("Install skill" in item for item in first))
        skill, agent, cfg = get_destinations("project", self.root)
        self.assertTrue((skill / "SKILL.md").is_file())
        self.assertEqual(tomllib.loads(agent.read_text())["model"], "gpt-6-luna")
        self.assertFalse(cfg.exists())
        self.assertEqual(install(scope="project", project_root=self.root), ["Already installed; no changes needed."])

    def test_dry_run_leaves_no_files(self):
        install(scope="project", project_root=self.root, dry_run=True, configure_defaults=True, planner_model="gpt-6.1-sol")
        self.assertFalse((self.root / ".agents").exists())
        self.assertFalse((self.root / ".codex").exists())

    def test_collision_refuses_without_force(self):
        skill, agent, cfg = get_destinations("project", self.root)
        agent.parent.mkdir(parents=True)
        agent.write_text("custom agent", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            install(scope="project", project_root=self.root)
        self.assertEqual(agent.read_text(), "custom agent")
        self.assertFalse(skill.exists())  # preflight avoids partial install

    def test_force_creates_backup(self):
        install(scope="project", project_root=self.root)
        skill, agent, cfg = get_destinations("project", self.root)
        agent.write_text("custom content", encoding="utf-8")
        install(scope="project", project_root=self.root, force=True)
        backups = list(agent.parent.glob("luna_executor.toml.bak-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "custom content")

    def test_merge_existing_config_preserves_section(self):
        skill, agent, cfg = get_destinations("project", self.root)
        cfg.parent.mkdir(parents=True)
        original = '# keep this\ncustom = "value"\n[agents]\ndefault_subagent_model = "something"\n[mcp_servers.local]\nurl = "http://localhost:3000"\n'
        cfg.write_text(original)
        install(scope="project", project_root=self.root, configure_defaults=True, planner_model="gpt-6.1-sol")
        parsed = tomllib.loads(cfg.read_text())
        self.assertEqual(parsed["custom"], "value")
        self.assertEqual(parsed["model"], "gpt-6.1-sol")
        self.assertEqual(parsed["agents"]["default_subagent_model"], "something")
        self.assertTrue(parsed["agents"]["enabled"])
        self.assertEqual(parsed["mcp_servers"]["local"]["url"], "http://localhost:3000")
        self.assertEqual(len(list(cfg.parent.glob("config.toml.bak-*"))), 1)
        self.assertIn("# keep this", cfg.read_text())

    def test_merge_no_agents_table(self):
        result = desired_config('[mcp_servers.foo]\nurl = "test"\n', planner_model="gpt-6.1-sol")
        parsed = tomllib.loads(result)
        self.assertTrue(parsed["agents"]["enabled"])
        self.assertEqual(parsed["model"], "gpt-6.1-sol")
        self.assertEqual(parsed["mcp_servers"]["foo"]["url"], "test")

    def test_invalid_config_does_not_change_files(self):
        skill, agent, cfg = get_destinations("project", self.root)
        cfg.parent.mkdir(parents=True)
        cfg.write_text("[invalid\n")
        with self.assertRaises(ValueError):
            install(scope="project", project_root=self.root, configure_defaults=True)
        self.assertFalse(skill.exists())

    def test_custom_executor_model(self):
        install(scope="project", project_root=self.root, executor_model="gpt-6-luna-custom")
        _, agent, _ = get_destinations("project", self.root)
        self.assertEqual(tomllib.loads(agent.read_text())["model"], "gpt-6-luna-custom")
        with self.assertRaises(ValueError):
            validate_model_id('invalid"\\model')

    def test_doctor_cannot_prove_routing(self):
        install(scope="project", project_root=self.root, configure_defaults=True)
        status = diagnose("project", self.root)
        self.assertTrue(status["skill_exists"])
        self.assertEqual(status["agent_model"], "gpt-6-luna")
        self.assertFalse(status["live_routing_verified"])

    def test_no_unexpected_config_modification(self):
        _, _, cfg = get_destinations("project", self.root)
        cfg.parent.mkdir(parents=True)
        cfg.write_text('model = "gpt-5"\n')
        install(scope="project", project_root=self.root)
        self.assertEqual(cfg.read_text(), 'model = "gpt-5"\n')

    def test_independent_efforts(self):
        install(scope="project", project_root=self.root, configure_defaults=True,
                planner_model="gpt-6.1-sol", planner_effort="max", executor_effort="high")
        _, agent, cfg = get_destinations("project", self.root)
        self.assertEqual(tomllib.loads(cfg.read_text())["model_reasoning_effort"], "max")
        self.assertEqual(tomllib.loads(agent.read_text())["model_reasoning_effort"], "high")
        status = diagnose("project", self.root)
        self.assertEqual(status["primary_reasoning_effort"], "max")
        self.assertEqual(status["agent_reasoning_effort"], "high")

    def test_executor_max_with_backup(self):
        install(scope="project", project_root=self.root)
        _, agent, _ = get_destinations("project", self.root)
        with self.assertRaises(FileExistsError):
            install(scope="project", project_root=self.root, executor_effort="max")
        install(scope="project", project_root=self.root, executor_effort="max", force=True)
        self.assertEqual(tomllib.loads(agent.read_text())["model_reasoning_effort"], "max")
        backups = list(agent.parent.glob("luna_executor.toml.bak-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(tomllib.loads(backups[0].read_text())["model_reasoning_effort"], "high")

    def test_primary_only_effort(self):
        _, _, cfg = get_destinations("project", self.root)
        cfg.parent.mkdir(parents=True)
        cfg.write_text('model = "gpt-6.1-sol"\n')
        install(scope="project", project_root=self.root, configure_defaults=True, planner_effort="max")
        self.assertEqual(tomllib.loads(cfg.read_text())["model_reasoning_effort"], "max")
        self.assertEqual(tomllib.loads(cfg.read_text())["model"], "gpt-6.1-sol")

    def test_primary_effort_requires_opt_in(self):
        with self.assertRaises(ValueError):
            install(scope="project", project_root=self.root, planner_effort="max")
        self.assertFalse((self.root / ".codex").exists())

    def test_reject_invalid_effort(self):
        with self.assertRaises(ValueError):
            install(scope="project", project_root=self.root, executor_effort="ultra")
        self.assertFalse((self.root / ".agents").exists())

    def test_validator(self):
        self.assertEqual(validate(), [])


if __name__ == "__main__":
    unittest.main()
