#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$HOME/.local/share/kagami/patches" "$HOME/.local/bin" "$HOME/.config/systemd/user"
cp "$ROOT/patches/hyprtasking-caelestia-overview.patch" "$HOME/.local/share/kagami/patches/hyprtasking-caelestia-overview.patch"
cp "$ROOT/patches/hyprtasking-gesture.patch" "$HOME/.local/share/kagami/patches/hyprtasking-caelestia-gesture.patch"
install -m 0755 "$ROOT/scripts/kagami-hyprtasking-build" "$HOME/.local/bin/kagami-hyprtasking-build"
python3 "$ROOT/scripts/integrate-hypr-user.py"
cp "$ROOT/systemd/workspace-grid-watch.service" "$HOME/.config/systemd/user/"
systemctl --user daemon-reload
systemctl --user enable --now workspace-grid-watch.service
echo 'Workspace Grid installed. Turn it on/off in Celestia Nexus > Plugins.'
