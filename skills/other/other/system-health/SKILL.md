---
name: system-health
description: Query system health metrics including CPU, memory, disk usage, and running processes. Use this when the user asks about system status, performance monitoring, or resource utilization.
allowed-tools: Bash
---

# System Health Check

Run this skill when the user asks about:
- System status or health
- Resource utilization
- Performance monitoring
- Memory or CPU usage
- Running processes and their consumption

## Run using:

```bash
# Ensure venv is activated
source venv/bin/activate
python scripts/check_system_health.py
```

## Output

Returns JSON with:
- System information (OS, hostname, uptime)
- Memory usage
- CPU information
- Top processes by memory consumption
- Disk usage
- Network interfaces

## Dependencies

Requires the MCP osquery server to be available. Install dependencies with:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Environment

No environment variables required for basic usage.
