---
name: mounted
description: Report which CCB providers are mounted (session exists AND daemon is online). Outputs JSON.
metadata:
  short-description: Show mounted CCB providers as JSON
---

# Mounted Providers

Reports which CCB providers are considered "mounted" for the current project.

## Definition

`mounted = has_session && daemon_on`

## Execution

```bash
ccb-mounted
```
