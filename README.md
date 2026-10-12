# Celestia Workspace Grid

Hyprtasking-based 3 × 3 canvas on Mirai, packaged as a Caelestia Nexus plugin.

## Controls
- Three-finger touchpad pan navigates the 3 × 3 workspace grid.
- Four fingers open/close the workspace overview (configured in `hypr-user.lua`).
- Super+Tab opens the overview; Super+Shift+Tab covers all monitors.
- **Nexus → Plugins → WorkspaceGrid → switch** enables or disables the actual Hyprland Hyprtasking module; the state persists across sessions.

## Gesture safety
- No drag before 16 units net displacement (avoids first-frame jitter).
- Absolute pan from the gesture origin avoids boundary-clamping drift on loops and reversals.
- Release with under 40 units net displacement returns to the original workspace without switching.
- Build patch is preserved for Hyprland upgrades.

## Installation
The current Mirai installation has a separate local Hyprtasking overview compatibility patch. Do not delete it.
`bash install.sh` installs the gesture patch and the sync service. Rebuild Hyprtasking using `kagami-hyprtasking-build` after Hyprland updates. Plugin files live at `~/.local/share/caelestia/plugins/workspace-grid`. The native Caelestia plugin loader reads `manifest.json` from that directory.

`workspace-grid-watch.service` observes the canonical `~/.config/caelestia/plugins.json` toggle. It loads/unloads `libhyprtasking.so`, rather than merely hiding UI. It also reconciles after Hyprland restarts. You can run `scripts/workspace-grid-watch.py --once` to check the actual module state. If you install this plugin on another machine, the native Hyprland library and the existing Caelestia layout config must also be installed.

## Verification
`g++ -std=c++20 -Wall -Wextra -Werror tests/gesture_motion_test.cpp -o /tmp/workspace-grid-test && /tmp/workspace-grid-test`
