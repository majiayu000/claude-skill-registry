---
name: n8n-workflow
description: n8n workflow automation and integration platform
allowed-tools: [Bash, Read, WebFetch]
---

# n8n Workflow Skill

## Overview

n8n workflow automation platform integration. 90%+ context savings.

## Requirements

- n8n instance URL
- N8N_API_KEY environment variable

## Tools (Progressive Disclosure)

### Workflows

| Tool           | Description          | Confirmation |
| -------------- | -------------------- | ------------ |
| list-workflows | List all workflows   | No           |
| get-workflow   | Get workflow details | No           |
| activate       | Activate workflow    | Yes          |
| deactivate     | Deactivate workflow  | Yes          |
| execute        | Execute workflow     | Yes          |

### Executions

| Tool            | Description            |
| --------------- | ---------------------- |
| list-executions | List recent executions |
| get-execution   | Get execution details  |
| retry-execution | Retry failed execution |

### Credentials

| Tool             | Description           |
| ---------------- | --------------------- |
| list-credentials | List credential types |

## Agent Integration

- **llm-architect** (primary): AI workflow design
- **orchestrator** (secondary): Integration patterns
- **developer** (secondary): Custom nodes

## Security

⚠️ Never expose N8N_API_KEY
