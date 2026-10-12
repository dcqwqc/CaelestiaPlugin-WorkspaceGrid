# Celestia Workspace Grid

Hyprtasking-based 3 × 3 canvas on Mirai, packaged as a Caelestia Nexus plugin.

## Controls
- Three-finger touchpad pan navigates the 3 × 3 workspace grid.
- Four fingers open/close the workspace overview (configured in `hypr-user.lua`).
- Super+Tab opens the overview; Super+Shift+Tab covers all monitors.
- **Nexus → Plugins → WorkspaceGrid → switch** enables or disables the actual Hyprland Hyprtasking module; the state persists across sessions.

## Rendering safety
- Normal QuickShell bars, controls, background and Loom layers remain visible in every workspace preview. Only the full-screen drawers/area-picker effect surfaces are excluded (to avoid blurred ghost rectangles).
- Live workspace previews do not re-sample desktop-size blur buffers; normal desktop blur is unaffected.
- This also avoids costly duplicate background-blur processing while panning.

## Gesture safety
- No drag before 16 units net displacement (avoids first-frame jitter).
- Absolute pan from the gesture origin avoids boundary-clamping drift on loops and reversals.
- Release with under 40 units net displacement returns to the original workspace without switching.
- Build patch is preserved for Hyprland upgrades.

## Installation
The current Mirai installation has a separate local Hyprtasking overview compatibility patch. Do not delete it.
`bash install.sh` installs the gesture patch and the sync service. Rebuild Hyprtasking using `kagami-hyprtasking-build` after Hyprland updates. Plugin files live at `~/.local/share/caelestia/plugins/workspace-grid`. The native Caelestia plugin loader reads `manifest.json` from that directory.

`workspace-grid-watch.service` observes the canonical `~/.config/caelestia/plugins.json` toggle. It loads/unloads `libhyprtasking.so`, rather than merely hiding UI. It also reconciles after Hyprland restarts. The installer adds an idempotent startup guard to `~/.config/caelestia/hypr-user.lua`, preventing the compositor from auto-loading a disabled grid before the switch service starts. The old config is backed up. You can run `scripts/workspace-grid-watch.py --once` to check the actual module state. If you install this plugin on another machine, the native Hyprland library and the existing Caelestia layout config must also be installed.

## Verification
`g++ -std=c++20 -Wall -Wextra -Werror tests/gesture_motion_test.cpp -o /tmp/workspace-grid-test && /tmp/workspace-grid-test`

## Mirai verification (2026-10-12)

- Standalone C++ gesture tests passed. Python toggle parser test passed.
- Patched native module compiled against the installed Hyprland, loaded successfully.
- A clean upstream checkout accepted both persistent patches; standalone test passed again.
- Native config OFF unloaded Hyprtasking; ON loaded it again; systemd watcher stayed active.
- Actual human three-finger touchpad circular-motion acceptance still requires a physical gesture test.

## 2026-10-12 visual-artifact remediation
The renderer patch is packaged together with the pre-existing Caelestia overview compatibility patch and is installed by `install.sh`. Existing Hyprland plugin binaries are backed up before hot-replacing them; the new module successfully loaded in the running Mirai compositor. Automated screenshot capture via remote compositor screencopy was unavailable, so physical three-finger fluidity and the elimination of all graphical artifacts still need human acceptance testing.

## 2026-10-12 panel visibility regression
A too-broad filter excluded the generic `quickshell` namespace and hid the actual desktop bars when opening the grid. The renderer now tests an explicit minimal exclusion policy. Regression tests verify that generic QuickShell, background, Loom and keyboard layers render in all tiles, while global drawers/area-picker blur overlays are filtered.
