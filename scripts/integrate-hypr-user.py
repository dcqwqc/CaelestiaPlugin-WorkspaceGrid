#!/usr/bin/env python3
"""Make built-in Hyprtasking autoload respect the real Workspace Grid switch."""
from pathlib import Path
import shutil
import sys
from datetime import datetime

path = Path.home() / ".config/caelestia/hypr-user.lua"
text = path.read_text()
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
