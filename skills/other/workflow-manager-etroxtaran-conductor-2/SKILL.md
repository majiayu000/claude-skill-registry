---
name: workflow-manager
description: Coordinate the multi-agent workflow across planning, validation, implementation, and verification.
version: 1.1.0
tags: [workflow, orchestration, governance]
owner: orchestration
status: active
---

# Workflow Manager Skill

Multi-agent workflow orchestration for coordinating Claude, Cursor, and Gemini agents.

## Overview

This skill enables Claude Code to act as the lead orchestrator in a multi-agent development workflow. Claude coordinates with Cursor (code quality, security) and Gemini (architecture, scalability) to implement features with robust validation and verification.

## Usage

```
/workflow-manager
```

## Prerequisites

- SurrealDB configured for workflow state persistence.

## Capabilities

### Core Orchestration
- Initialize and manage 5-phase workflows
- Track workflow state with persistence and resumability
- Coordinate parallel agent execution
- Handle context versioning and drift detection

### Approval Management
- Evaluate agent feedback using configurable policies
- Support multiple approval strategies: ALL_MUST_APPROVE, NO_BLOCKERS, WEIGHTED_SCORE, MAJORITY
- Track iteration counts for plan-validate cycles

### Conflict Resolution
- Detect conflicts between agent feedback
- Resolve using weighted expertise areas
- Support escalation to human decision when needed

## Workflow Phases

| Phase | Name | Lead Agent | Parallel Agents |
|-------|------|------------|-----------------|
| 1 | Planning | Claude | - |
| 2 | Validation | Claude | Cursor, Gemini |
| 3 | Implementation | Claude | - |
| 4 | Verification | Claude | Cursor, Gemini |
| 5 | Completion | Claude | - |

## File Structure

```
project/
├── AGENTS.md           # Workflow rules (source of truth)
├── PRODUCT.md          # Feature specification
├── CLAUDE.md           # Claude-specific context
├── GEMINI.md           # Gemini context
├── .cursor/rules       # Cursor rules
├── scripts/
│   ├── call-cursor.sh  # Cursor CLI wrapper
│   └── call-gemini.sh  # Gemini CLI wrapper
└── (SurrealDB)          # workflow_state, phase_outputs, logs
```

## Agent Expertise Areas

### Cursor (Code Quality Focus)
- **Security**: 0.8 weight - SQL injection, XSS, OWASP vulnerabilities
- **Code Quality**: 0.7 weight - Style, best practices, maintainability
- **Testing**: 0.7 weight - Test coverage, test quality

### Gemini (Architecture Focus)
- **Architecture**: 0.7 weight - Design patterns, modularity
- **Scalability**: 0.8 weight - Performance at scale, bottlenecks
- **Patterns**: 0.6 weight - Design patterns, anti-patterns

## Approval Policies

### Phase 2 (Validation) - NO_BLOCKERS
- Approve if no high-severity blocking issues
- Minimum combined score: 6.0
- Single agent can approve if other unavailable

### Phase 4 (Verification) - ALL_MUST_APPROVE
- Both Cursor and Gemini must approve
- Minimum score: 7.0
- No blocking issues allowed
- Uses CONSERVATIVE conflict resolution

## Context Versioning

The workflow tracks checksums of context files:
- `AGENTS.md` - Workflow rules
- `PRODUCT.md` - Feature spec
- `.cursor/rules` - Cursor rules
- `GEMINI.md` - Gemini context
- `CLAUDE.md` - Claude context

Drift detection warns when files change mid-workflow.

## Commands

| Command | Description |
|---------|-------------|
| `/orchestrate` | Start or resume workflow |
| `/phase-status` | Show workflow status |
| `/validate-plan` | Run Phase 2 validation |
| `/verify-code` | Run Phase 4 verification |
| `/resolve-conflict` | Resolve agent disagreements |

## Usage Example

```
User: Implement the feature in PRODUCT.md

Claude: I'll start the multi-agent workflow.
[Reads AGENTS.md, PRODUCT.md]
[Creates plan.json in Phase 1]
[Runs /validate-plan - Cursor and Gemini review in parallel]
[Implements with TDD in Phase 3]
[Runs /verify-code - Both agents must approve]
[Completes Phase 5 with documentation]
```

## Integration

### With Python Orchestrator

```python
from orchestrator import Orchestrator

orch = Orchestrator("/path/to/project")
orch.run()  # Runs all 5 phases
```

### With Bash Scripts

```bash
# Initialize project
bash scripts/init-multi-agent.sh /path/to/project

# Call agents directly
bash scripts/call-cursor.sh prompt.md output.json
bash scripts/call-gemini.sh prompt.md output.json
```

## State Management

The workflow state is persisted in SurrealDB (`workflow_state` table):

```json
{
  "project_name": "my-project",
  "current_phase": 3,
  "iteration_count": 1,
  "phases": {
    "planning": {"status": "completed"},
    "validation": {"status": "completed"},
    "implementation": {"status": "in_progress"}
  },
  "context": {
    "files": {"agents": {"checksum": "abc123..."}}
  }
}
```

## Error Handling

- Phases can retry up to 3 times (configurable)
- Blockers are recorded and reported
- Failed phases can be resumed after fixing issues
- Context drift is detected and logged

## Best Practices

1. **Read AGENTS.md first** - Contains complete workflow rules
2. **Follow TDD in Phase 3** - Write tests before implementation
3. **Address all blocking issues** - Required for approval
4. **Don't skip phases** - Each phase builds on previous
5. **Check drift regularly** - Use `/phase-status` to monitor

## Outputs

- Updated workflow records in SurrealDB (`workflow_state`, `phase_outputs`, `logs`).

## Related Skills

- `/orchestrate` - Run the full workflow
- `/phase-status` - Detailed phase status
