#!/usr/bin/env python3
"""Keep the Hyprtasking Hyprland module in sync with Caelestia's Plugins switch."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time

PLUGIN_ID = "dcqwqc/workspacegrid"
HOME = Path.home()
CONFIG = HOME / ".config/caelestia/plugins.json"
MARKER = HOME / ".config/caelestia/workspace-grid.enabled"
LIBRARY = HOME / ".local/lib/hyprland/libhyprtasking.so"


def wanted(config=CONFIG):
    try:
        return PLUGIN_ID in json.loads(config.read_text()).get("enabled", [])
    except (OSError, ValueError, TypeError):
        # If config is briefly being replaced, don't change the running plugin.
        return None


def hypr_env():
    env = os.environ.copy()
    if env.get("HYPRLAND_INSTANCE_SIGNATURE"):
        return env
    try:
        raw = subprocess.check_output(["hyprctl", "-j", "instances"], timeout=5, text=True)
        processes = json.loads(raw)
        instances = [x for x in processes if isinstance(x, dict) and x.get("instance")]
        if not instances:
            return None
        # Prefer the user's most recently started compositor.
        env["HYPRLAND_INSTANCE_SIGNATURE"] = max(instances, key=lambda x: x.get("time", 0))["instance"]
        return env
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def is_loaded(env):
    try:
        p = subprocess.run(["hyprctl", "plugin", "list"], capture_output=True,
                           text=True, env=env, timeout=5, check=True)
        return "Plugin Hyprtasking by " in p.stdout
    except (OSError, subprocess.SubprocessError):
        return None


def reconcile(verbose=False):
    desired = wanted()
    env = hypr_env()
    if desired is None or env is None:
        if verbose:
            print("not ready: config/Hyprland unavailable")
        return False
    MARKER.parent.mkdir(parents=True, exist_ok=True)
    value = "1\n" if desired else "0\n"
    if not MARKER.exists() or MARKER.read_text() != value:
        MARKER.write_text(value)
    loaded = is_loaded(env)
    if loaded is None:
        if verbose:
            print("not ready: unable to inspect loaded modules")
        return False
    if desired == loaded:
        if verbose:
            print(f"Workspace Grid: {'enabled and loaded' if loaded else 'disabled and unloaded'}")
        return True
    if desired and not LIBRARY.is_file():
        if verbose:
            print("unable to load: compiled Hyprtasking library missing")
        return False
    command = ["hyprctl", "plugin", "load" if desired else "unload", str(LIBRARY)]
    try:
        result = subprocess.run(command, capture_output=True, text=True, env=env, timeout=10)
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"Workspace Grid: {exc}", flush=True)
        return False
    actual = is_loaded(env)
    if result.returncode != 0 or actual != desired:
        print(f"Workspace Grid: {result.stderr.strip() or result.stdout.strip()}; loaded={actual}", flush=True)
        return False
    print(f"Workspace Grid: {'loaded' if desired else 'unloaded'}", flush=True)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Apply desired state once and exit")
    args = parser.parse_args()
    if args.once:
        raise SystemExit(0 if reconcile(verbose=True) else 1)
    last_config = object()
    last_instance = None
    last_check = 0
    while True:
        try:
            st = CONFIG.stat()
            state = (st.st_mtime_ns, st.st_size)
        except OSError:
            state = None
        env = hypr_env()
        instance = env.get("HYPRLAND_INSTANCE_SIGNATURE") if env else None
        now = time.monotonic()
        if state != last_config or instance != last_instance or now - last_check > 20:
            reconcile()
            last_check = now
            last_config = state
            last_instance = instance
        time.sleep(1.5)


if __name__ == "__main__":
    main()
