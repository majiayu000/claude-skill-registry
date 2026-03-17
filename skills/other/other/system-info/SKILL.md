---
name: system-info
description: 获取系统信息，包括CPU、内存、磁盘、网络和进程详情。
metadata:
  short-description: 系统信息
source:
  repository: https://github.com/giampaolo/psutil
  license: BSD-3-Clause
---

# System Info Tool

## Description
Get detailed system information including CPU, memory, disk usage, network stats, and running processes.

## Trigger
- `/sysinfo` command
- User needs system information
- User wants to check resources

## Usage

```bash
# Full system overview
python scripts/system_info.py

# CPU information
python scripts/system_info.py --cpu

# Memory usage
python scripts/system_info.py --memory

# Disk usage
python scripts/system_info.py --disk

# Running processes
python scripts/system_info.py --processes --top 10
```

## Tags
`system`, `cpu`, `memory`, `disk`, `monitor`

## Compatibility
- Codex: ✅
- Claude Code: ✅
