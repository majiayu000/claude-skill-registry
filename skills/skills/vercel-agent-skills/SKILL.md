---
name: vercel-agent-skills
description: Vercel AI SDK agent skill management
allowed-tools: [Bash, Read, Glob, Write]
---

# Vercel Agent Skills Skill

## Overview

Manage Vercel AI SDK agent skills. 90%+ context savings.

## Tools (Progressive Disclosure)

### Skills

| Tool         | Description       | Confirmation |
| ------------ | ----------------- | ------------ |
| list-skills  | List agent skills | No           |
| create-skill | Create new skill  | Yes          |
| update-skill | Update skill      | Yes          |
| delete-skill | Delete skill      | Yes          |

### Tools

| Tool        | Description       |
| ----------- | ----------------- |
| list-tools  | List skill tools  |
| add-tool    | Add tool to skill |
| remove-tool | Remove tool       |

### Testing

| Tool       | Description           |
| ---------- | --------------------- |
| test-skill | Test skill execution  |
| validate   | Validate skill schema |
| simulate   | Simulate agent call   |

## Agent Integration

- **llm-architect** (primary): Agent design
- **developer** (secondary): Skill implementation
