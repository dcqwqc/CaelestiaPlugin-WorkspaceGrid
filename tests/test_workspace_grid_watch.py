import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

FILE = Path(__file__).resolve().parents[1] / "scripts/workspace-grid-watch.py"
spec = importlib.util.spec_from_file_location("workspace_grid_watch", FILE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class WatchTests(unittest.TestCase):
    def test_enabled(self):
        with tempfile.TemporaryDirectory() as temp:
            f = Path(temp) / "plugins.json"
            f.write_text(json.dumps({"enabled": ["dcqwqc/workspacegrid"]}))
            self.assertTrue(module.wanted(f))
            f.write_text(json.dumps({"enabled": ["dcqwqc/loom"]}))
            self.assertFalse(module.wanted(f))
            f.write_text("{")
            self.assertIsNone(module.wanted(f))

if __name__ == "__main__":
    unittest.main()
