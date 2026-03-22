---
name: coding-agent
description: Incremental development agent with TDD workflow. Use when implementing features one at a time, following test-driven development, making commits, or resuming development work.
version: 1.0.0
category: autonomous-coding
layer: core-workflow
---

# Coding Agent

Incremental development agent that implements features using test-driven development (TDD) in subsequent sessions after initialization.

## Quick Start

### Start a Coding Session
```python
from scripts.coding_agent import CodingAgent

agent = CodingAgent(project_dir)
context = await agent.start_session()
print(f"Session {context.iteration} started")
```

### Implement Next Feature
```python
feature = await agent.select_next_feature()
result = await agent.implement_feature(feature)

if result.success:
    await agent.mark_feature_complete(feature)
    await agent.commit_work(f"Implement: {feature.description}")
```

## Session Protocol

```
┌─────────────────────────────────────────────────────────────┐
│                   CODING SESSION PROTOCOL                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. RESTORE CONTEXT                                         │
│     ├─ Read claude-progress.txt (quick state)              │
│     ├─ Read feature_list.json (work remaining)             │
│     └─ Get git log (recent commits)                        │
│                                                              │
│  2. ENVIRONMENT CHECK                                       │
│     ├─ Run init.sh if needed                               │
│     ├─ Verify server running                               │
│     └─ Run smoke tests                                     │
│                                                              │
│  3. SELECT FEATURE                                          │
│     ├─ Get highest-priority incomplete feature             │
│     ├─ Read feature steps                                  │
│     └─ Plan implementation                                 │
│                                                              │
│  4. IMPLEMENT WITH TDD                                      │
│     ├─ Write failing test                                  │
│     ├─ Verify test fails                                   │
│     ├─ Implement code                                      │
│     ├─ Verify test passes                                  │
│     └─ Verify E2E (if applicable)                         │
│                                                              │
│  5. MARK COMPLETE                                           │
│     ├─ Update feature_list.json (passes: true)            │
│     └─ IMPORTANT: Features only go false → true            │
│                                                              │
│  6. COMMIT WORK                                             │
│     ├─ git add relevant files                              │
│     ├─ Descriptive commit message                          │
│     └─ Reference feature ID                                │
│                                                              │
│  7. UPDATE PROGRESS                                         │
│     ├─ Append to claude-progress.txt                       │
│     └─ List accomplishments and blockers                   │
│                                                              │
│  8. END SESSION                                             │
│     ├─ Leave code in mergeable state                       │
│     └─ Auto-continue or shutdown                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## TDD Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                     TDD CYCLE                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│    ┌──────────┐                                             │
│    │  1. RED  │  Write failing test                        │
│    └────┬─────┘                                             │
│         │ Test fails ✓                                      │
│         ▼                                                   │
│    ┌──────────┐                                             │
│    │ 2. GREEN │  Write minimal code to pass                │
│    └────┬─────┘                                             │
│         │ Test passes ✓                                     │
│         ▼                                                   │
│    ┌──────────┐                                             │
│    │3.REFACTOR│  Clean up without breaking tests           │
│    └────┬─────┘                                             │
│         │ All tests pass ✓                                  │
│         ▼                                                   │
│    ┌──────────┐                                             │
│    │ 4. E2E   │  Verify in browser (if needed)             │
│    └────┬─────┘                                             │
│         │ Feature works ✓                                   │
│         ▼                                                   │
│      COMMIT                                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Key Rules

1. **ONE FEATURE PER SESSION**: Focus prevents context exhaustion
2. **TEST FIRST**: Always write test before implementation
3. **VERIFY BEFORE MARKING**: Feature must actually pass
4. **DESCRIPTIVE COMMITS**: Reference feature ID and explain changes
5. **MERGEABLE STATE**: Code should always be in working state

## Commit Message Format

```
<type>: <description>

<body - what and why>

Feature: <feature-id>
```

Example:
```
feat: implement user signup with email validation

- Added SignupForm component with validation
- Created /api/auth/signup endpoint
- Added email verification check
- Tests: 8 passing

Feature: auth-001
```

## Integration Points

- **autonomous-session-manager**: Detects CONTINUE session
- **context-state-tracker**: Provides and updates state
- **security-sandbox**: Validates commands
- **progress-tracker**: Tracks completion metrics

## References

- `references/CODING-WORKFLOW.md` - Detailed workflow
- `references/TDD-PATTERNS.md` - TDD best practices
- `references/COMMIT-CONVENTIONS.md` - Commit guidelines

## Scripts

- `scripts/coding_agent.py` - Main CodingAgent class
- `scripts/feature_selector.py` - Feature prioritization
- `scripts/implementation_workflow.py` - TDD implementation
- `scripts/commit_workflow.py` - Git commit workflow
