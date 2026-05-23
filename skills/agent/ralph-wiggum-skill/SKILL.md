---
name: ralph-wiggum
category: workflow
version: 1.0.0
description: Autonomous task completion loop with PRD tracking and LLM memory
author: Matt Pocock / Jeffrey Huntley (adapted for NodeJS Starter V1)
priority: 2
auto-load: false
triggers:
  - ralph
  - autonomous
  - loop
  - prd
  - overnight
requires:
  - verification/verification-first.skill.md
  - workflow/feature-development.skill.md
---

# Ralph Wiggum Technique

## Overview

The Ralph Wiggum technique is a simple but powerful pattern for autonomous AI-driven development:

1. **PRD (prd.json)**: JSON file with user stories, each having a `passes` boolean
2. **Progress file (progress.txt)**: LLM memory between iterations
3. **Loop**: Run Claude Code repeatedly until all tasks pass

Named after Ralph Wiggum from The Simpsons - simple but effective.

> "Me fail English? That's unpossible!" - Ralph Wiggum

## Why It Works

### The Problem with AI Coding

- LLMs lose context between sessions
- No persistent memory of what worked/failed
- Tendency to declare victory without verification
- Complex orchestration systems add overhead

### The Solution

1. **Structured task list (JSON)**: Machine-readable, hard for LLM to corrupt
2. **Progress file**: Persistent memory across iterations
3. **Verification gate**: MUST pass all checks before marking complete
4. **Git commits**: Checkpoint after each success
5. **Simple loop**: No complex orchestration needed

## Components

### 1. PRD File (plans/prd.json)

```json
{
  "project": "My Project",
  "version": "1.0.0",
  "user_stories": [
    {
      "id": "US-001",
      "epic": "Authentication",
      "title": "User can sign up with email",
      "description": "As a user, I want to sign up so I can access the app",
      "priority": "critical",
      "acceptance_criteria": [
        "Email validation works",
        "Password strength checked",
        "Confirmation email sent"
      ],
      "verification": {
        "type_check": true,
        "lint": true,
        "unit_tests": true,
        "e2e_tests": true,
        "build": true
      },
      "passes": false,
      "last_attempt": null,
      "attempt_count": 0,
      "depends_on": []
    }
  ],
  "metadata": {
    "total_stories": 1,
    "passing_stories": 0
  }
}
```

### Key Fields

| Field | Purpose |
|-------|---------|
| `passes` | Boolean gate - only true after verification |
| `priority` | Execution order: critical > high > medium > low |
| `depends_on` | Task IDs that must pass first |
| `acceptance_criteria` | Specific requirements to implement |
| `attempt_count` | Tracks failed attempts (for debugging) |

### 2. Progress File (plans/progress.txt)

Append-only file with session entries:

```markdown
# Ralph Wiggum Progress Log
# Project: my-project
# Created: 2026-01-07T10:00:00Z

---

## Session 1: 2026-01-07T10:30:00Z
**Task**: US-001 - User can sign up with email
**Status**: IN_PROGRESS

### Work Done
- Created SignUpForm component at apps/web/src/components/auth/SignUpForm.tsx
- Added zod schema for email validation

### Issues Encountered
- useAuth hook missing return type annotation

### Learnings
- Always add explicit return types to custom hooks
- Email regex pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/

### Next Steps
1. Fix useAuth hook return type
2. Add unit tests for SignUpForm
3. Run full verification

---

## Session 2: 2026-01-07T11:00:00Z
**Task**: US-001 - User can sign up with email
**Status**: COMPLETED

### Work Done
- Fixed useAuth return type
- Added comprehensive unit tests
- All verification passed

### Learnings
- Vitest mocking pattern for Supabase auth

### Next Steps
- Move to US-002
```

### 3. Verification Pipeline

ALL must pass before marking `passes: true`:

```bash
pnpm turbo run type-check  # TypeScript compilation
pnpm turbo run lint        # ESLint + Ruff linting
pnpm turbo run test        # Unit tests (Vitest/Pytest)
pnpm turbo run build       # Production build
pnpm --filter=web test:e2e # Playwright E2E tests
```

## Workflow Diagram

```
┌─────────────────────────────────────────┐
│           Start Iteration N             │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  All tasks passed?                      │
│  ├─ Yes → Exit (Project Complete!)      │
│  └─ No  → Continue                      │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Find highest priority unpassed task    │
│  (respecting depends_on constraints)    │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Load context:                          │
│  - Read prd.json for task details       │
│  - Read progress.txt for learnings      │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Work on task:                          │
│  - Implement per acceptance criteria    │
│  - Add/update tests                     │
│  - Follow project conventions           │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Run verification pipeline              │
│  type-check → lint → test → build → e2e │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
┌───────────────┐   ┌───────────────┐
│  All PASS     │   │  Any FAIL     │
└───────┬───────┘   └───────┬───────┘
        │                   │
        ▼                   ▼
┌───────────────┐   ┌───────────────┐
│ Set passes:   │   │ Increment     │
│ true in PRD   │   │ attempt_count │
│               │   │               │
│ Git commit    │   │ Record issues │
└───────┬───────┘   └───────┬───────┘
        │                   │
        └─────────┬─────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Append session to progress.txt         │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Continue to Iteration N+1              │
└─────────────────────────────────────────┘
```

## Invocation

### Initialize (First Time)

```bash
# Unix/Mac/WSL
./scripts/ralph.sh --init

# Windows PowerShell
.\scripts\ralph.ps1 -Init

# Creates:
# - plans/prd.json (template)
# - plans/progress.txt (empty)
# - plans/ralph-prompt.md (iteration prompt)
```

### Run the Loop

```bash
# Unix/Mac/WSL
./scripts/ralph.sh 50  # Max 50 iterations

# Windows PowerShell
.\scripts\ralph.ps1 -MaxIterations 50

# Claude Code command
/ralph run 50
```

## Best Practices

### 1. Small, Focused Tasks

Keep user stories to 1-2 hour scope:

```json
// Good
{ "title": "Add email validation to sign-up form" }

// Too big
{ "title": "Implement entire authentication system" }
```

### 2. Specific Acceptance Criteria

Vague criteria lead to incomplete implementations:

```json
// Good
{
  "acceptance_criteria": [
    "Email format validated with regex",
    "Error message shown for invalid email",
    "Submit button disabled until valid"
  ]
}

// Too vague
{
  "acceptance_criteria": [
    "Form works properly"
  ]
}
```

### 3. Use Dependencies

Order tasks logically:

```json
{
  "id": "US-002",
  "title": "User can log in",
  "depends_on": ["US-001"]  // Sign-up must work first
}
```

### 4. Read Progress Before Working

Check what was learned in previous iterations:

```markdown
### Learnings
- Vitest mocking pattern for Supabase: vi.mock('@supabase/ssr')
- Always await signUp() before checking error state
```

### 5. Commit After Each Success

Creates checkpoints for recovery:

```bash
git log --oneline
# feat(US-003): User can reset password
# feat(US-002): User can log in
# feat(US-001): User can sign up with email
```

### 6. Escalate Repeated Failures

If `attempt_count >= 3`:
- Stop working on task
- Record blocker in progress.txt
- Move to next available task
- Flag for human review

## Integration with Existing Systems

### Long-Running Agents

Ralph follows the same patterns as `apps/backend/src/agents/long_running/`:

| Ralph | Long-Running |
|-------|--------------|
| `progress.txt` | `ProgressFile` class |
| `prd.json` | `FeatureManager` |
| Session entries | `SessionProgress` |

### Orchestrator Delegation

The orchestrator can hand off to Ralph for autonomous completion:

```python
async def handle_large_feature(feature_description: str):
    # Create PRD from feature description
    prd = generate_prd(feature_description)
    save_prd("plans/prd.json", prd)

    # Delegate to Ralph
    return await delegate_to_agent("ralph-wiggum", {
        "prd_path": "plans/prd.json",
        "max_iterations": 50
    })
```

### Verification Agent

Uses the same verification-first principles:
- No self-attestation
- Run actual commands
- All checks must pass

## Example Session Output

```
============================================
  Ralph Wiggum Technique
  Autonomous Task Completion Loop
============================================

>>> Checking prerequisites...
Claude CLI found
PRD file found
All prerequisites OK

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Iteration 1: US-001
  User can sign up with email
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

>>> Invoking Claude Code...
[Claude implements sign-up form]

>>> Running verification pipeline...
  Running type check...
  Type check: PASS
  Running lint...
  Lint: PASS
  Running tests...
  Tests: PASS
  Running build...
  Build: PASS
  Running E2E tests...
  E2E: PASS

Verification passed! Marking US-001 as complete.
[Auto-commit: feat(US-001): User can sign up with email]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Iteration 2: US-002
  User can log in with email
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...

============================================
  Summary
============================================
  Iterations: 5
  Tasks Completed: 5
  Progress: 5/5 tasks complete
  Duration: 00:45:23

All tasks complete! Project finished in 5 iterations.
```

## Australian Context

All implementations follow Australian defaults:
- en-AU spelling (colour, organisation, behaviour)
- DD/MM/YYYY date format
- AUD currency formatting where applicable
- Privacy Act 1988 compliance considerations for user data

## References

- [Original Ralph Article](https://ghuntley.com/ralph/) by Jeffrey Huntley
- [Matt Pocock Video](https://www.youtube.com/watch?v=_IK18goX4X8)
- [Anthropic Engineering Blog](https://www.anthropic.com/engineering)
