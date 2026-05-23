---
name: cfn-agent-selector
description: Agent selection based on task classification with fallback support
version: 1.0.0
tags: [agent-selection, task-classification, fallback]
status: production
---

# Agent Selector Submodule

**Parent Skill:** cfn-agent-lifecycle
**Purpose:** Select appropriate agents based on task classification with fallback support

## Components

- `select-agents.sh` - Basic agent selection
- `select-agents-with-fallback.sh` - Selection with fallback strategy
- `task-classifier.sh` - Task classification for agent mapping
- `agent-mappings.json` - Task-to-agent mapping configuration

## Usage

```bash
# Basic selection
./.claude/skills/cfn-agent-lifecycle/lib/selection/select-agents.sh --task "implement feature"

# With fallback
./.claude/skills/cfn-agent-lifecycle/lib/selection/select-agents-with-fallback.sh --task "implement feature"
```
