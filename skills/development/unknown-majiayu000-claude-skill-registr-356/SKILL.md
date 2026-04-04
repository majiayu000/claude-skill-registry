---
name: cfn-agent-lifecycle
description: "Unified agent management from selection through completion - spawning, execution, output processing. Use when selecting agents for tasks, spawning agents with dependency validation, processing agent outputs, or tracking agent lifecycle events with audit trails."
version: 2.0.0
tags: [mega-skill, agent-management, lifecycle, spawning]
status: production
---

# Agent Lifecycle Management Skill (Mega-Skill)

**Version:** 2.0.0
**Purpose:** Unified agent management from selection through completion
**Status:** Production
**Consolidates:** cfn-agent-selector, cfn-agent-selection-with-fallback, cfn-agent-spawning, cfn-agent-output-processing, cfn-agent-execution

---

## Overview

This mega-skill provides complete agent lifecycle management:
- **Selection** - Task classification and agent selection with fallback
- **Spawning** - Agent deployment with dependency validation
- **Output** - Structured output parsing and validation
- **Audit** - SQLite lifecycle tracking for audit trails

---

## Directory Structure

```
agent-lifecycle/
├── SKILL.md                          # This file
├── lib/
│   ├── selection/                    # Agent selection (from cfn-agent-selector + cfn-agent-selection-with-fallback)
│   │   ├── select-agents.sh          # Basic agent selection
│   │   ├── select-agents-with-fallback.sh  # Enhanced with fallback (recommended)
│   │   ├── task-classifier.sh        # Task classification
│   │   ├── agent-mappings.json       # Agent category mappings
│   │   ├── src/                      # TypeScript implementation
│   │   │   ├── agent-selector.ts
│   │   │   ├── cli.ts
│   │   │   └── agent-selector.test.ts
│   │   └── dist/                     # Compiled TypeScript
│   │       ├── agent-selector.cjs
│   │       └── cli.cjs
│   ├── spawning/                     # Agent spawning (from cfn-agent-spawning + cfn-agent-execution)
│   │   ├── spawn-agent.sh            # Main spawning script
│   │   ├── spawn-worker.sh           # Worker spawning
│   │   ├── spawn-templates.sh        # Template management
│   │   ├── spawn-agent-wrapper.sh    # Wrapper with error handling
│   │   ├── execute-agent.sh          # Agent execution
│   │   ├── check-dependencies.sh     # Dependency validation
│   │   ├── parse-agent-provider.sh   # Provider parsing
│   │   └── get-agent-provider-env.sh # Provider env setup
│   ├── output/                       # Output processing (from cfn-agent-output-processing)
│   │   └── README.md                 # Output processing documentation
│   └── audit/                        # Audit trail (original agent-lifecycle)
│       ├── execute-lifecycle-hook.sh # SQLite lifecycle hooks
│       └── simple-audit.sh           # Simple audit script
└── cli/                              # CLI wrappers for convenience
    ├── select-agents.sh              # → lib/selection/select-agents-with-fallback.sh
    ├── spawn-agent.sh                # → lib/spawning/spawn-agent.sh
    └── lifecycle-hook.sh             # → lib/audit/execute-lifecycle-hook.sh
```

---

## Quick Start

### 1. Select Agents for a Task

```bash
# Recommended: Use fallback-enabled selection
./.claude/skills/agent-lifecycle/cli/select-agents.sh "Implement JWT authentication"

# Output (JSON):
# {
#   "loop3": ["backend-developer", "security-specialist"],
#   "loop2": ["code-reviewer", "tester", "security-specialist"],
#   "product_owner": "product-owner",
#   "category": "backend-api",
#   "confidence": 0.92
# }
```

### 2. Spawn Agents

```bash
./.claude/skills/agent-lifecycle/cli/spawn-agent.sh \
  --task "Implement user authentication" \
  --agents coder,security-specialist,tester \
  --agent-id coordinator-1
```

### 3. Track Lifecycle Events

```bash
# Register agent spawn
./.claude/skills/agent-lifecycle/cli/lifecycle-hook.sh spawn \
  --agent-id "${AGENT_ID}" \
  --agent-type "${AGENT_TYPE}" \
  --acl-level 1

# Update confidence
./.claude/skills/agent-lifecycle/cli/lifecycle-hook.sh update \
  --agent-id "${AGENT_ID}" \
  --confidence 0.85

# Mark completion
./.claude/skills/agent-lifecycle/cli/lifecycle-hook.sh complete \
  --agent-id "${AGENT_ID}" \
  --confidence 0.90
```

---

## Module Details

### Selection Module (lib/selection/)

**Purpose:** Task classification and agent selection

**Features:**
- Task classification into 9 categories
- Agent selection for Loop 3 (implementers) and Loop 2 (validators)
- Guaranteed non-empty agent arrays (fallback behavior)
- Agent validation against available profiles
- TypeScript implementation for type safety

**Task Categories:**
| Category | Loop 3 Agents | Loop 2 Agents |
|----------|---------------|---------------|
| backend-api | backend-developer, api-gateway-specialist | code-reviewer, tester, api-testing-specialist |
| fullstack | backend-developer, react-frontend-engineer | code-reviewer, tester, integration-tester |
| mobile | mobile-dev, backend-developer | code-reviewer, tester, interaction-tester |
| infrastructure | devops-engineer, docker-specialist | code-reviewer, tester, chaos-engineering-specialist |
| security | security-specialist, backend-developer | code-reviewer, tester, security-specialist |
| frontend | react-frontend-engineer, typescript-specialist | code-reviewer, tester, playwright-tester |
| database | database-architect, backend-developer | code-reviewer, tester, data-engineer |
| performance | backend-developer, perf-analyzer | code-reviewer, tester, performance-benchmarker |
| default | backend-developer, devops-engineer | code-reviewer, tester, code-quality-validator |

### Spawning Module (lib/spawning/)

**Purpose:** Agent deployment and dependency management

**Features:**
- System dependency validation (Bash 4.0+, Node.js, etc.)
- Node.js module validation (redis, dotenv)
- Claude Flow prerequisites check
- Multi-agent spawning
- Provider routing support

**Performance Targets:**
- Dependency check: <50ms
- Spawn time: <200ms
- Stop time: <150ms
- Success rate: 99.5%

### Output Module (lib/output/)

**Purpose:** Structured output extraction from agents

**Features:**
- Multi-pattern parsing with fallbacks
- Output validation framework
- Redis coordination integration
- Universal pattern system for any agent type

### Audit Module (lib/audit/)

**Purpose:** SQLite lifecycle tracking

**Features:**
- Agent spawn registration
- Confidence updates during work
- Completion tracking
- Cross-session recovery support
- ACL level enforcement (1-6)

---

## Integration with CFN Loop

```bash
# 1. Classify task and select agents
CLASSIFICATION=$(./lib/selection/task-classifier.sh "$TASK_DESCRIPTION")
AGENTS_JSON=$(./cli/select-agents.sh "$TASK_DESCRIPTION")

# 2. Extract agent lists
LOOP3_AGENTS=$(echo "$AGENTS_JSON" | jq -r '.loop3 | join(",")')
LOOP2_AGENTS=$(echo "$AGENTS_JSON" | jq -r '.loop2 | join(",")')

# 3. Spawn agents with lifecycle tracking
./cli/lifecycle-hook.sh spawn --agent-id "$AGENT_ID" --agent-type "$AGENT_TYPE"
./cli/spawn-agent.sh --task "$TASK" --agents "$LOOP3_AGENTS" --agent-id "$AGENT_ID"

# 4. After completion
./cli/lifecycle-hook.sh complete --agent-id "$AGENT_ID" --confidence 0.92
```

---

## Migration from Individual Skills

### Old Paths → New Paths

| Old Path | New Path |
|----------|----------|
| `.claude/skills/cfn-agent-selector/select-agents.sh` | `.claude/skills/agent-lifecycle/lib/selection/select-agents.sh` |
| `.claude/skills/cfn-agent-selection-with-fallback/select-agents.sh` | `.claude/skills/agent-lifecycle/lib/selection/select-agents-with-fallback.sh` |
| `.claude/skills/cfn-agent-spawning/spawn-agent.sh` | `.claude/skills/agent-lifecycle/lib/spawning/spawn-agent.sh` |
| `.claude/skills/cfn-agent-execution/execute-agent.sh` | `.claude/skills/agent-lifecycle/lib/spawning/execute-agent.sh` |

### CLI Wrappers (Convenience)

For easier migration, use CLI wrappers:
```bash
./.claude/skills/agent-lifecycle/cli/select-agents.sh  # Recommended entry point
./.claude/skills/agent-lifecycle/cli/spawn-agent.sh
./.claude/skills/agent-lifecycle/cli/lifecycle-hook.sh
```

---

## TypeScript Implementation

The selection module includes a production-ready TypeScript implementation:

```bash
# Use TypeScript version
export USE_TYPESCRIPT=true
./lib/selection/select-agents-with-fallback.sh "Implement auth"

# Or call directly
node ./lib/selection/dist/cli.cjs "Implement auth"
```

**Benefits:**
- Type-safe interfaces
- 95.2% classification accuracy
- 42 tests, 100% passing
- Path traversal security validation

---

## Dependencies

- **Bash:** 4.0+
- **Node.js:** LTS (for TypeScript features)
- **jq:** JSON processing
- **SQLite3:** Audit database
- **Redis:** Coordination (optional)

---

## Testing

```bash
# Test selection
./lib/selection/src/agent-selector.test.ts

# Test spawning dependencies
./lib/spawning/check-dependencies.sh

# Test lifecycle hooks
./lib/audit/simple-audit.sh
```

---

## Version History

### 2.0.0 (2025-12-02) - Mega-Skill Consolidation
- Merged: cfn-agent-selector, cfn-agent-selection-with-fallback
- Merged: cfn-agent-spawning, cfn-agent-execution
- Merged: cfn-agent-output-processing
- Added: CLI wrappers for convenience
- Added: Unified documentation

### 1.0.0 (Original)
- SQLite lifecycle hooks for auditing

---

## Related Skills

- **task-classifier** (`.claude/skills/task-classifier/`) - Standalone task classification
- **cfn-docker-agent-spawning** (`.claude/skills/cfn-docker-agent-spawning/`) - Docker-specific spawning
- **cfn-product-owner-decision** (`.claude/skills/cfn-product-owner-decision/`) - Product owner output processing
