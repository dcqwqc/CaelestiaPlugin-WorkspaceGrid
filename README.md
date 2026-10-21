# Celestia Workspace Grid

Hyprtasking-based 3 × 3 canvas on Mirai, packaged as a Caelestia Nexus plugin.

## Controls
- Three-finger hold + drag is reserved for moving a window (Hyprgrass on touchscreen); three-finger downward swipe closes a window.
- Hyprtasking no longer intercepts three-finger swipes for workspace navigation. Open the grid with Super+Tab and navigate using its on-screen controls or pointer input.
- Four-finger swipes in any direction (touchpad or touchscreen) toggle the Yoga touch keyboard via the Gestures plugin; these swipes do not open/close the grid.
- Super+Tab opens the overview; Super+Shift+Tab covers all monitors.
- **Nexus → Plugins → WorkspaceGrid → switch** enables or disables the actual Hyprland Hyprtasking module; the state persists across sessions.

## Rendering safety
- Normal QuickShell bars, controls, background and Loom layers remain visible in every workspace preview. The drawer layer is retained because it contains actual top/side controls. Only the full-screen area-picker is excluded; preview blur remains disabled.
- Live workspace previews do not re-sample desktop-size blur buffers; normal desktop blur is unaffected.
- This also avoids costly duplicate background-blur processing while panning.

## Gesture safety
- The installer sets `plugin.hyprtasking.gestures.open_fingers = 0` and `move_fingers = 0` in `hypr-user.lua`, so the grid cannot compete for either four-finger keyboard swipes or three-finger window dragging. Super+Tab still opens the grid, but three-finger navigation is disabled to avoid stealing a window drag.
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
The renderer patch is packaged together with the pre-existing Caelestia overview compatibility patch and is installed by `install.sh`. Existing Hyprland plugin binaries are backed up before hot-replacing them; the new module successfully loaded in the running Mirai compositor. A later successful Wayland screenshot verified that the QuickShell panels now appear in the 3×3 grid; physical three-finger fluidity still requires user acceptance testing.

## 2026-10-12 panel visibility regression
A too-broad filter excluded the generic `quickshell` namespace and hid the actual desktop bars when opening the grid. The renderer now tests an explicit minimal exclusion policy. Regression tests verify that generic QuickShell, background, Loom and keyboard layers render in all tiles, while the area-picker overlay is filtered; drawers and their contents are rendered without preview blur.

## 2026-10-13 visual verification
The full-screen caelestia-drawers layer also contains the actual QuickShell bars and sidebar. We now retain it while suppressing its expensive blur in scaled previews. A fresh Wayland screenshot of the 3×3 grid on Mirai confirmed top and side QuickShell controls on every workspace tile.

## Three-finger input arbitration (2026-10-21)

Hyprtasking 0.56-compatible builds default `gestures:move_fingers` to **3**
independently of `gestures:open_fingers`. Disabling only `open_fingers`
left three-finger workspace navigation active during Hyprgrass long-press
window drags. This led to workspace-grid navigation taking over the drag.

The installer now persists both values as zero. Setting zero is safe here:
physical libinput swipe events have positive finger counts, so the plugin
does not enter its navigation branch. Workspace overview itself, including
Super+Tab and pointer controls, remains enabled. The gesture-only mode
(`python3 scripts/integrate-hypr-user.py --gesture-only`) performs a
backup-protected, idempotent adjustment without touching unrelated startup
guards. The active value can be checked using
`hyprctl getoption plugin:hyprtasking:gestures:move_fingers`.
