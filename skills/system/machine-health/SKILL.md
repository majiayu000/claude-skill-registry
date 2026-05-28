---
name: machine-health
description: Monitor and optimize system resources (CPU, RAM, Disk). Includes cleaning routines.
trigger: high-load, system-lag, periodic-maintenance
scope: global
---

# Machine Health Skill

This skill provides tools to ensure the host machine remains stable and responsive during long autonomous runs.

## Capabilities:

1. **Memory Purge**: Clears stand-by memory and releases non-essential cache.
2. **CPU Stabilization**: Identifies rogue processes and optimizes task priority.
3. **Ghost Process Cleanup**: Kills orphaned agent subprocesses or leaked IDE instances.

## How to use:

If the agent detects high latency or "Out of Memory" warnings:

1. Invoke the `MachineHealthTool` (via MCP).
2. Command: `clean_resources`
3. Command: `status_check`

## Recommended Routine:

- Run `clean_resources` every 12 hours of continuous operation.
- Run `status_check` before starting a high-complexity task (e.g., massive refactoring).
