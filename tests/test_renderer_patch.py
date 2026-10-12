import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class RendererPatchTests(unittest.TestCase):
    def test_context_guards(self):
        patch=(ROOT/'patches/hyprtasking-caelestia-overview.patch').read_text()
        self.assertIn('hyprtasking_rendering_workspace_tile',patch)
        self.assertIn('name == "caelestia-drawers"',patch)
        self.assertIn('name == "caelestia-area-picker"',patch)
        self.assertIn('data.blur = false',patch)
        self.assertIn('renderWorkspace',patch)

    def test_quickshell_tiles_remain_visible(self):
        # Regression: explicitly skipping "quickshell" made the shell vanish.
        source=(ROOT/'src/layer_visibility.hpp').read_text()
        self.assertIn('name == "caelestia-drawers"', source)
        self.assertIn('name == "caelestia-area-picker"', source)
        self.assertNotIn('name == "quickshell"', source)
        self.assertIn("hyprtasking_skip_tile_layer", (ROOT/'patches/hyprtasking-caelestia-overview.patch').read_text())

    def test_rebuild_carries_patches(self):
        s=(ROOT/'scripts/kagami-hyprtasking-build').read_text()
        self.assertIn('src/render.cpp',s)
        self.assertIn('gesture_patch',s)
        self.assertIn('applied workspace-grid gesture patch',s)

if __name__=='__main__':
    unittest.main()
