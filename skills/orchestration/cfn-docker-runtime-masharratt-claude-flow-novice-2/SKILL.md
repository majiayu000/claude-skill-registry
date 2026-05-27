---
name: cfn-docker-runtime
description: "Docker container orchestration for CFN Loop - spawning, coordination, logging, wave execution. Use when running CFN Loop agents in Docker containers, executing waves of parallel agents, coordinating containerized agents via Redis, or managing Docker-based agent lifecycle."
version: 1.0.0
tags: [mega-skill, docker, containers, orchestration]
status: production
---

# Docker Runtime Skill (Mega-Skill)

**Version:** 1.0.0
**Purpose:** Docker container orchestration for CFN Loop
**Status:** Production
**Consolidates:** cfn-docker-agent-spawning, cfn-docker-coordination, cfn-docker-logging, cfn-docker-loop-orchestration, cfn-docker-skill-mcp-selection, cfn-docker-wave-execution

---

## Overview

This mega-skill provides complete Docker container management for CFN Loop:
- **Spawning** - Container-based agent deployment
- **Coordination** - Redis-based container coordination
- **Logging** - Container log collection and storage
- **Orchestration** - Docker-mode loop execution
- **MCP** - Skill-based MCP container selection
- **Waves** - Wave-based parallel execution

---

## Directory Structure

```
docker-runtime/
├── SKILL.md
├── lib/
│   ├── spawning/         # From cfn-docker-agent-spawning
│   ├── coordination/     # From cfn-docker-coordination
│   ├── logging/          # From cfn-docker-logging
│   ├── orchestration/    # From cfn-docker-loop-orchestration
│   ├── mcp/              # From cfn-docker-skill-mcp-selection
│   └── waves/            # From cfn-docker-wave-execution
└── cli/
    ├── spawn-container.sh
    ├── coordinate.sh
    └── execute-wave.sh
```

---

## Quick Start

### Spawn Container Agent
```bash
./.claude/skills/docker-runtime/lib/spawning/spawn-agent.sh \
  --agent-type backend-developer \
  --task-id task-123
```

### Execute Wave
```bash
./.claude/skills/docker-runtime/lib/waves/execute-wave.sh \
  --wave-id wave-1 \
  --agents "backend-developer,tester"
```

---

## Migration Paths

| Old Path | New Path |
|----------|----------|
| cfn-docker-agent-spawning/ | docker-runtime/lib/spawning/ |
| cfn-docker-coordination/ | docker-runtime/lib/coordination/ |
| cfn-docker-logging/ | docker-runtime/lib/logging/ |
| cfn-docker-loop-orchestration/ | docker-runtime/lib/orchestration/ |
| cfn-docker-skill-mcp-selection/ | docker-runtime/lib/mcp/ |
| cfn-docker-wave-execution/ | docker-runtime/lib/waves/ |

---

## Version History

### 1.0.0 (2025-12-02)
- Consolidated 6 Docker skills into mega-skill
