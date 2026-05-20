---
name: aim-pause-updates
description: "Toggle auto_update_enabled kill switch for automatic memory updates"
trigger: "/aim-pause-updates"
---

```python
"""Pause/resume automatic memory updates: /aim-pause-updates

Toggle the auto_update_enabled kill switch. When paused:
- GitHub sync still runs (data still ingested)
- Freshness scans still run (staleness still detected)
- BUT: no auto-corrections, no auto-re-captures

Usage:
    /aim-pause-updates          # Toggle current state
    /aim-pause-updates on       # Enable updates
    /aim-pause-updates off      # Disable updates
"""

from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

_install_dir = os.path.expanduser("~/.ai-memory")
sys.path.insert(0, os.path.join(_install_dir, "src"))

from memory.metrics_push import push_skill_metrics_async


def _find_env_file():
    """Locate the .env file (project-local or install dir)."""
    # Check project-local .env first
    local_env = Path.cwd() / ".env"
    if local_env.exists():
        return local_env
    # Check AI_MEMORY_INSTALL_DIR
    install_dir = os.environ.get("AI_MEMORY_INSTALL_DIR", "")
    if install_dir:
        install_env = Path(install_dir) / "docker" / ".env"
        if install_env.exists():
            return install_env
    # Fallback to ~/.ai-memory/docker/.env
    home_env = Path.home() / ".ai-memory" / "docker" / ".env"
    if home_env.exists():
        return home_env
    return None


def _read_env_value(env_file, key):
    """Read a value from .env file."""
    if not env_file or not env_file.exists():
        return None
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith(f"{key}="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def _write_env_value(env_file, key, value):
    """Update a value in .env file (preserves other lines)."""
    if not env_file or not env_file.exists():
        return False
    lines = env_file.read_text(encoding="utf-8").splitlines()
    found = False
    for i, line in enumerate(lines):
        if line.strip().startswith(f"{key}="):
            lines[i] = f"{key}={value}"
            found = True
            break
    if not found:
        lines.append(f"{key}={value}")
    env_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def _log_toggle(env_file, old_value, new_value):
    """Write toggle event to JSONL audit log."""
    log_path = Path.cwd() / ".audit" / "logs" / "kill-switch-log.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "field": "AUTO_UPDATE_ENABLED",
        "old_value": old_value,
        "new_value": new_value,
        "env_file": str(env_file),
    }
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    start_time = time.perf_counter()

    # Parse optional explicit on/off
    explicit = None
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ("on", "true", "enable", "1"):
            explicit = True
        elif arg in ("off", "false", "disable", "0"):
            explicit = False
        else:
            print(f"Error: Unknown argument '{sys.argv[1]}'. Use 'on' or 'off'.")
            sys.exit(1)

    env_file = _find_env_file()
    if not env_file:
        print("Error: Cannot locate .env file. Ensure AI Memory is installed.")
        sys.exit(1)

    current = _read_env_value(env_file, "AUTO_UPDATE_ENABLED")
    current_bool = current.lower() in ("true", "1", "yes") if current else True

    if explicit is not None:
        new_bool = explicit
    else:
        new_bool = not current_bool  # Toggle

    new_value = "true" if new_bool else "false"
    old_value = "true" if current_bool else "false"

    _write_env_value(env_file, "AUTO_UPDATE_ENABLED", new_value)
    _log_toggle(env_file, old_value, new_value)

    if new_bool:
        print("## Auto-Updates: ENABLED")
        print("")
        print("Automatic memory updates are **active**.")
        print("- Freshness corrections will be applied")
        print("- Auto-recapture will run on stale memories")
    else:
        print("## Auto-Updates: PAUSED")
        print("")
        print("Automatic memory updates are **paused**.")
        print("- GitHub sync still runs (data ingestion continues)")
        print("- Freshness scans still run (staleness detected)")
        print("- Auto-corrections are **disabled** until re-enabled")
        print("")
        print("Run `/aim-pause-updates on` to re-enable.")

    push_skill_metrics_async("pause-updates", "success", time.perf_counter() - start_time)

    # Skill tracing (PLAN-014 G-06)
    try:
        from memory.trace_buffer import emit_trace_event
        emit_trace_event(
            event_type="skill_execution",
            data={
                "input": f"Skill: aim-pause-updates"[:10000],
                "output": f"Result: completed"[:10000],
                "metadata": {"skill_name": "aim-pause-updates"},
            },
            session_id=os.environ.get("CLAUDE_SESSION_ID", "unknown"),
            tags=["skill"],
        )
    except Exception:
        pass  # Tracing failures never break skill execution


if __name__ == "__main__":
    main()
```
