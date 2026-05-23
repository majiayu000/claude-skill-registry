---
name: workflow-conductor
description: Workflow orchestration and automation engine
allowed-tools: [Bash, Read, Glob]
---

# Workflow Conductor Skill

## Overview

Workflow orchestration for complex automation. 90%+ context savings.

## Tools (Progressive Disclosure)

### Workflow Management

| Tool            | Description            | Confirmation |
| --------------- | ---------------------- | ------------ |
| list-workflows  | List defined workflows | No           |
| run-workflow    | Execute workflow       | Yes          |
| stop-workflow   | Stop running workflow  | Yes          |
| workflow-status | Check workflow status  | No           |

### Task Operations

| Tool        | Description         |
| ----------- | ------------------- |
| list-tasks  | List workflow tasks |
| task-output | Get task output     |
| retry-task  | Retry failed task   |

### Scheduling

| Tool            | Description       | Confirmation |
| --------------- | ----------------- | ------------ |
| schedule        | Schedule workflow | Yes          |
| list-schedules  | List schedules    | No           |
| cancel-schedule | Cancel schedule   | Yes          |

## Agent Integration

- **orchestrator** (primary): Workflow design
- **devops** (secondary): Automation pipelines
