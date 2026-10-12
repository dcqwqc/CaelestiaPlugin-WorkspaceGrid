#include "../src/layer_visibility.hpp"
#include <cassert>

int main() {
    // The regression: generic "quickshell" is the real bar and must survive.
    assert(!hyprtasking_skip_tile_layer("quickshell"));
    assert(!hyprtasking_skip_tile_layer("caelestia-background"));
    assert(!hyprtasking_skip_tile_layer("loom-agent-cursors"));
    assert(!hyprtasking_skip_tile_layer("yoga-osk-toolbar"));
    assert(!hyprtasking_skip_tile_layer("yoga-osk-handle"));
    assert(!hyprtasking_skip_tile_layer("mpvpaper"));
    assert(!hyprtasking_skip_tile_layer("caelestia-border-exclusion"));

    // Blur/compositor overlays are not per-workspace UI.
    assert(hyprtasking_skip_tile_layer("caelestia-drawers"));
    assert(hyprtasking_skip_tile_layer("caelestia-area-picker"));
    return 0;
}
