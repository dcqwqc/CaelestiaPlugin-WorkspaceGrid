"""Hyprtasking must not compete with reserved three-finger window gestures."""
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "integrate-hypr-user.py"


class ThreeFingerReservation(unittest.TestCase):
    def run_installer(self, content):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / ".config" / "caelestia" / "hypr-user.lua"
            config.parent.mkdir(parents=True)
            config.write_text(content)
            env = {**os.environ, "HOME": directory}
            command = [sys.executable, str(SCRIPT), "--gesture-only"]
            first = subprocess.run(command, env=env, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            text = config.read_text()
            second = subprocess.run(command, env=env, capture_output=True, text=True)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(text, config.read_text())
            self.assertEqual(len(list(config.parent.glob("hypr-user.lua.bak-gesture-priority-*"))), 1)
            return text

    def test_three_finger_stops_grid_without_disabling_four_finger_osk(self):
        text = self.run_installer('''hl.config({plugin = {hyprtasking = {
            gestures = { open_fingers = 0 }
        }}})
        -- leave Hyprgrass untouched
        hl.plugin.hyprgrass.bind({pattern = {kind="longpress",fingers=3}})
        ''')
        self.assertIn("move_fingers = 0", text)
        self.assertIn("open_fingers = 0", text)
        self.assertIn("hyprgrass.bind", text)

    def test_existing_move_setting_is_replaced(self):
        text = self.run_installer('''hl.config({plugin = {hyprtasking = {
            gestures = { open_fingers = 0, move_fingers = 3, }
        }}})''')
        self.assertIn("move_fingers = 0", text)
        self.assertNotIn("move_fingers = 3", text)
        self.assertNotIn(",,", text)

    def test_refuses_multiple_hyprtasking_blocks(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / ".config" / "caelestia" / "hypr-user.lua"
            config.parent.mkdir(parents=True)
            contents = 'hyprtasking = { gestures = { open_fingers = 0 } }\n' * 2
            config.write_text(contents)
            process = subprocess.run(
                [sys.executable, str(SCRIPT), "--gesture-only"],
                env={**os.environ, "HOME": directory}, capture_output=True, text=True)
            self.assertNotEqual(process.returncode, 0)
            self.assertEqual(config.read_text(), contents)


if __name__ == "__main__":
    unittest.main()
