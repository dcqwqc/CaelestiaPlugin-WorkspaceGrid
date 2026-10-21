#!/usr/bin/env python3
"""Make built-in Hyprtasking autoload respect the real Workspace Grid switch."""
from pathlib import Path
import shutil
import re
import sys
from datetime import datetime

path = Path.home() / ".config/caelestia/hypr-user.lua"
text = path.read_text()
# Reserve *every* four-finger swipe on touchpad and touchscreen for the
# Celestia Gestures on-screen keyboard toggle. The grid remains available
# through SUPER+TAB, with three fingers navigating while it is open.
# Hyprtasking treats a zero-finger match as unreachable, disabling only its
# own open/close swipe without disabling the grid or three-finger navigation.
old_fingers = "open_fingers = 4,"
new_fingers = "open_fingers = 0, -- Four-finger swipes belong to the OSK"
if old_fingers in text:
    backup = path.with_name(path.name + ".bak-osk-swipe-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    shutil.copy2(path, backup)
    text = text.replace(old_fingers, new_fingers, 1)
    path.write_text(text)
    print(f"Reserved four-finger swipes for OSK; backup: {backup}")
# The four-finger opening gesture is not Hyprtasking's only listener:
# "move_fingers" defaults to 3 even when "open_fingers" is 0.
# Reserve three fingers for Hyprgrass window hold/drag and close; the overview
# remains available via SUPER+TAB and its pointer UI. Zero cannot match a
# physical libinput swipe, so no compositor plugin rebuild is required.
match = re.search(r'(hyprtasking\s*=\s*\{[\s\S]*?gestures\s*=\s*\{)([^{}]*)(\})', text)
if not match or len(re.findall(r'hyprtasking\s*=\s*\{', text)) != 1:
    raise SystemExit("Refusing ambiguous Hyprtasking gesture configuration")
body = match.group(2)
if not re.search(r'\bopen_fingers\s*=\s*0\b', body):
    raise SystemExit("Expected Hyprtasking four-finger OSK reservation")
if re.search(r'\bmove_fingers\s*=\s*0\b', body):
    print("Hyprtasking three-finger navigation already disabled")
else:
    if re.search(r'\bmove_fingers\s*=', body):
        new_body = re.sub(r'\bmove_fingers\s*=\s*\d+', 'move_fingers = 0', body, count=1)
    else:
        trimmed = body.rstrip()
        new_body = trimmed + ('' if trimmed.endswith(',') else ',') + ' move_fingers = 0 '
    backup = path.with_name(path.name + ".bak-gesture-priority-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    shutil.copy2(path, backup)
    text = text[:match.start(2)] + new_body + text[match.end(2):]
    path.write_text(text)
    print(f"Reserved three fingers for window control; backup: {backup}")
# Existing installations may have independently managed Hyprland startup
# callbacks. --gesture-only changes exactly the competing gesture setting.
if "--gesture-only" in sys.argv:
    sys.exit(0)

if "workspace_grid_autoload" in text:
    print("Workspace Grid startup guard already installed")
    sys.exit(0)
old = """hl.plugin.load(hyprtasking)
hl.on("hyprland.start", function()
    hl.exec_cmd("hyprctl plugin list | grep -q hyprtasking || hyprctl plugin load " .. hyprtasking)
end)"""
new = """-- Obey the WorkspaceGrid toggle even before the QuickShell sync service starts.
-- The service updates this marker whenever the native Plugins switch changes.
local workspace_grid_marker = io.open((os.getenv("HOME") or "/home/qwqc")
    .. "/.config/caelestia/workspace-grid.enabled", "r")
local workspace_grid_autoload = true
if workspace_grid_marker then
    workspace_grid_autoload = workspace_grid_marker:read("*l") ~= "0"
    workspace_grid_marker:close()
end
if workspace_grid_autoload then
    hl.plugin.load(hyprtasking)
    hl.on("hyprland.start", function()
        hl.exec_cmd("hyprctl plugin list | grep -q hyprtasking || hyprctl plugin load " .. hyprtasking)
    end)
end"""
if text.count(old) != 1:
    raise SystemExit("Cannot install startup guard safely: unexpected Hyprtasking config")
backup=path.with_name(path.name + ".bak-workspace-grid-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
shutil.copy2(path, backup)
path.write_text(text.replace(old,new))
print(f"Installed persistent startup guard; backup: {backup}")
