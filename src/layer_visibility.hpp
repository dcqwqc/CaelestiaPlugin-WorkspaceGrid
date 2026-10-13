#pragma once

#include <string_view>

// Only global full-screen effect surfaces are omitted from workspace tiles.
// Ordinary QuickShell panels, wallpaper, keyboard handles and Loom controls
// remain visible on each desktop preview.
inline bool hyprtasking_skip_tile_layer(std::string_view name) {
    return name == "caelestia-area-picker";
}
