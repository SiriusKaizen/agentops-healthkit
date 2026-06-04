import json
import tempfile
import unittest
from pathlib import Path

import agentops_healthkit


class AgentOpsHealthkitTests(unittest.TestCase):
    def test_python_command_is_detected(self):
        result = agentops_healthkit.check_command("python3")
        self.assertEqual(result.kind, "command")
        self.assertEqual(result.target, "python3")
        self.assertTrue(result.ok)

    def test_profile_loader_reads_json_object(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            profile_path = Path(tmpdir) / "profile.json"
            profile_path.write_text(json.dumps({"commands": ["python3"], "ports": []}), encoding="utf-8")
            profile = agentops_healthkit.load_profile(str(profile_path))
        self.assertEqual(profile["commands"], ["python3"])
        self.assertEqual(profile["ports"], [])

    def test_doctor_can_run_without_port_checks(self):
        exit_code = agentops_healthkit.main(["doctor", "--command", "python3", "--no-default-ports"])
        self.assertEqual(exit_code, 0)

    def test_only_failures_does_not_change_exit_code(self):
        exit_code = agentops_healthkit.main(
            ["doctor", "--command", "definitely-not-a-real-command", "--no-default-ports", "--only-failures"]
        )
        self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
