---
name: log-agent
description: Record agent run logs into .tmp/logs/. Use this to maintain an audit trail of agent actions and errors.
---

# Log Agent

## Overview

This skill provides a standardized way to log agent activities to the filesystem. It creates JSON-formatted log entries in `.tmp/logs/` (or a specified directory).

## Usage

### Log Script

**Syntax:**

```bash
python3 .agent/skills/log-agent/scripts/log_run.py <agent_name> <message> [--log_dir <dir>]
```

**Example:**

```bash
python3 .agent/skills/log-agent/scripts/log_run.py ParserAgent "Started parsing resume.pdf"
```

**Log Format:**

```json
{"timestamp": "2023-10-27T10:00:00", "agent": "ParserAgent", "message": "Started parsing resume.pdf"}
```
