---
name: system-headroom
description: >
  Check system resources: CPU, memory, disk.
  Warns when thresholds exceeded.
triggers:
  - check system resources
  - disk space
  - memory usage
  - am i running low
  - system status
  - check headroom
  - how much disk
  - how much memory
---

# System Headroom

Quick system resource check with configurable thresholds.

## Commands

```bash
# Check all resources with default thresholds
./scripts/check.sh

# Custom thresholds
./scripts/check.sh --disk 90 --mem 95
```

## Output

Shows:

- CPU load (uptime output)
- Disk usage per mount (df -h)
- Memory usage percentage
- Warnings if thresholds exceeded

## Exit Codes

- `0`: All resources within thresholds
- `1`: One or more warnings triggered

## Environment Variables

| Variable         | Default | Description                    |
| ---------------- | ------- | ------------------------------ |
| `DISK_THRESHOLD` | 85      | Warn if disk usage exceeds %   |
| `MEM_THRESHOLD`  | 90      | Warn if memory usage exceeds % |
