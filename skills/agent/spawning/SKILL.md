---
name: cfn-agent-spawning
description: Agent process spawning with provider configuration and execution
version: 1.0.0
tags: [agent-spawning, process-management, execution]
status: production
---

# Agent Spawning Submodule

**Parent Skill:** cfn-agent-lifecycle
**Purpose:** Spawn agent processes with proper environment and provider configuration

## Components

- `spawn-agent.sh` - Primary agent spawning script
- `spawn-worker.sh` - Worker process spawning
- `spawn-agent-wrapper.sh` - Wrapper for standardized spawning
- `spawn-templates.sh` - Template-based spawning
- `execute-agent.sh` - Agent execution handler
- `get-agent-provider-env.sh` - Provider environment configuration
- `parse-agent-provider.sh` - Provider parsing utilities
- `check-dependencies.sh` - Dependency validation

## Usage

```bash
# Spawn an agent
./.claude/skills/cfn-agent-lifecycle/lib/spawning/spawn-agent.sh \
  --agent-type backend-dev \
  --task-id "task-123" \
  --provider kimi

# Execute agent directly
./.claude/skills/cfn-agent-lifecycle/lib/spawning/execute-agent.sh \
  --agent-id "agent-123" \
  --task "implement feature"
```
