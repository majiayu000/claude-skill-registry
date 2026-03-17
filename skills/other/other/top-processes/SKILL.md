---
name: top-processes
description: Get the top memory or CPU consuming processes on the system. Use this when asked about which processes are using the most resources, memory leaks, or process monitoring.
allowed-tools: Bash
---

# Top Processes by Resource Usage

Run this skill when the user asks about:
- Which processes are consuming the most memory
- Top CPU or memory users
- Process resource consumption
- Memory leaks or high resource usage
- Application performance issues

## Run using:

```bash
# Ensure venv is activated
source venv/bin/activate
python scripts/get_top_processes.py
```

## Parameters

You can optionally specify the number of processes to return:
```bash
source venv/bin/activate
python scripts/get_top_processes.py --limit 20
```

Default limit is 10 processes.

## Output

Returns JSON array with:
- Process name
- Process ID (PID)
- Memory usage (MB)
- Parent process ID
- Process path
- Command line arguments

Sorted by memory usage (highest first).

## Dependencies

Requires the MCP osquery server. Install with:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Environment

No environment variables required.
