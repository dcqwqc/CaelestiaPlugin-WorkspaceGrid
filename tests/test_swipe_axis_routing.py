import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class AxisRoutingPatchTests(unittest.TestCase):
    def test_install_reserves_four_fingers_for_keyboard(self):
        script = (ROOT / "scripts/integrate-hypr-user.py").read_text()
        self.assertIn('new_fingers = "open_fingers = 0,', script)
        self.assertIn('text.replace(old_fingers, new_fingers, 1)', script)

    def test_grid_requires_vertical_direction_lock(self):
        text = (ROOT/'patches/hyprtasking-gesture.patch').read_text()
        self.assertIn("swipe_open_axis = HTSwipeMotion::lock_axis", text)
        self.assertIn("swipe_open_axis != 'v'", text)
        self.assertIn("swipe_total_x += e.delta.x", text)
        self.assertIn("swipe_open_axis = 0;", text)
        self.assertIn("assert(HTSwipeMotion::lock_axis(40, 11, 28, 1.65) == 'h')", text)

if __name__ == '__main__':
    unittest.main()
