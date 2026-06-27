import unittest
from pathlib import Path
import sys
import tempfile


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from statusline_kit.cli import format_claude_status, main, upsert_tui_status_line


class ClaudeStatusTests(unittest.TestCase):
    def test_formats_available_fields(self):
        status = format_claude_status(
            {
                "model": {"display_name": "Claude Sonnet"},
                "workspace": {"current_dir": "/tmp/statusline-kit"},
                "usage": {"input_tokens": 12450, "output_tokens": 830},
                "cost": {"total_cost_usd": 0.0214},
            }
        )

        self.assertIn("CC Claude Sonnet", status)
        self.assertIn("statusline-kit", status)
        self.assertIn("in 12k out 830", status)
        self.assertIn("$0.0214", status)

    def test_tolerates_missing_json_fields(self):
        self.assertTrue(format_claude_status({}).startswith("CC Claude"))


class CodexConfigTests(unittest.TestCase):
    def test_adds_tui_section_when_missing(self):
        result = upsert_tui_status_line('model = "gpt-5-codex"\n')

        self.assertIn("[tui]", result)
        self.assertIn('"model-with-reasoning"', result)
        self.assertIn("status_line_use_colors = true", result)

    def test_replaces_status_line_and_preserves_other_tui_keys(self):
        original = """model = "gpt-5-codex"

[tui]
theme = "dark"
status_line = [
  "old",
]
status_line_use_colors = false

[tui.model_availability_nux]
gpt-5-codex = "seen"
"""
        result = upsert_tui_status_line(original)

        self.assertIn('theme = "dark"', result)
        self.assertIn('"model-with-reasoning"', result)
        self.assertNotIn('"old"', result)
        self.assertIn("[tui.model_availability_nux]", result)
        self.assertIn('gpt-5-codex = "seen"', result)


class CliDispatchTests(unittest.TestCase):
    def test_install_claude_dispatch_uses_status_command_arg(self):
        with tempfile.TemporaryDirectory() as tempdir:
            settings = Path(tempdir) / "settings.json"

            code = main(
                [
                    "install-claude",
                    "--settings",
                    str(settings),
                    "--command",
                    "custom-statusline claude",
                ]
            )

            self.assertEqual(0, code)
            self.assertIn("custom-statusline claude", settings.read_text())


if __name__ == "__main__":
    unittest.main()
