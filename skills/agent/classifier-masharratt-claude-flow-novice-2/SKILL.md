---
name: task-classifier
description: Analyzes task descriptions and classifies them into categories for agent selection
version: 1.0.0
tags: [classification, agent-selection, automation]
---

# Task Classifier Skill

Analyzes task descriptions using keyword matching to suggest appropriate agent specializations.

## Usage

```bash
./.claude/skills/task-classifier/classify-task.sh "Task description"
```

## Classification Categories

| Category | Keywords | Use Case |
|----------|----------|----------|
| **frontend** | ui, ux, react, component, css, styling, layout, responsive, interface | UI/UX development |
| **backend** | api, endpoint, server, database, rest, graphql, service, authentication | Server-side development |
| **devops** | docker, kubernetes, ci/cd, deployment, infrastructure, container, pipeline | Infrastructure work |
| **testing** | test, qa, validation, coverage, integration, unit, e2e | Quality assurance |
| **security** | security, auth, encryption, vulnerability, audit, penetration | Security work |
| **data** | database, sql, migration, schema, data, model, entity | Data modeling |
| **performance** | performance, optimization, speed, cache, memory, cpu | Performance tuning |
| **general** | (default) | General development |

## Output Format

Comma-separated list of classifications:

```bash
$ classify-task.sh "Create a React dashboard with API integration"
frontend,backend,testing
```

## Integration with Agent Selector

This skill is typically used with `cfn-agent-selector` to determine which agents to spawn:

```bash
CLASSIFICATION=$(classify-task.sh "$TASK_DESCRIPTION")
AGENTS=$(select-agents.sh --classification "$CLASSIFICATION" --mode standard)
```

## Examples

```bash
# Frontend task
$ classify-task.sh "Build responsive navigation component"
frontend

# Full-stack task
$ classify-task.sh "Create REST API with React admin panel"
frontend,backend

# DevOps task
$ classify-task.sh "Setup CI/CD pipeline with Docker"
devops

# Security audit
$ classify-task.sh "Perform security audit and fix vulnerabilities"
security
```

## Implementation Details

- Uses `grep -E` for case-insensitive pattern matching
- Returns multiple classifications if multiple keywords match
- Falls back to "general" if no specific keywords detected
- Stateless execution (no persistent state)
- Exit code 0 on success, 1 on error

## Used By

- `cfn-v3-coordinator` - For automatic agent selection
- `cfn-agent-selector` - As input for agent mapping
- CFN Loop orchestration - For task-specific agent spawning
