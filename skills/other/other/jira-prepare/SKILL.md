---
name: jira:prepare
description: Prepare a Jira task with enrichment and subtask creation. Use when the user wants to "prepare task", "enrich issue", "create subtasks", or "prepare for development".
version: 4.0.0
---

# Jira Task Preparation

Prepare a Jira task with technical enrichment, subtask creation, and work breakdown structure.

## Usage

```
/jira:prepare <issue-key>
```

## Features

- Analyzes issue requirements
- Creates technical subtasks
- Enriches description with implementation notes
- Identifies dependencies
- Estimates effort

## Related Commands

- `/jira:work` - Start working on the prepared issue
- `/jira:triage` - Triage and analyze issues
