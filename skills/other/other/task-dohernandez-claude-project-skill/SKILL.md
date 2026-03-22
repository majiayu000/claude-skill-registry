---
name: task
description: "Structured implementation process for features, chores, refactors, and docs. Use when implementing non-bugfix work."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
hooks:
  Stop:
    - type: command
      command: "task claude:validate-skill -- --skill task"
---

# Task

## Purpose

Structured implementation methodology for non-bugfix work (features, chores, refactors, docs). Ensures work is properly scoped, planned, implemented following project patterns, and verified before completion.

## Quick Reference

- **Phases**: Scope -> Plan -> Implement -> Verify
- **Key Rule**: Understand before building
- **Output**: Working implementation with changes reviewed

## Task Phases

```
+-----------------------------------------------------------------------------+
|                           TASK WORKFLOW                                      |
+-----------------------------------------------------------------------------+
|   1. SCOPE   ->   2. PLAN   ->   3. IMPLEMENT   ->   4. VERIFY             |
+-----------------------------------------------------------------------------+
```

## Phase T1: Scope

**Goal:** Understand what needs to be done and define boundaries.

**Procedure:**
1. Read the ticket/request description carefully
2. Identify the core requirement (what must be delivered)
3. Identify out-of-scope items (what NOT to do)
4. Clarify any ambiguities with user
5. Document the scope

**Output:** Clear understanding of deliverables

```markdown
## Scope
- **Goal:** Add retry logic to the E2E runner script
- **Deliverables:**
  - Configurable retry count in run-e2e.sh
  - Proper exit code propagation
- **Out of scope:**
  - Changes to the GitHub Actions workflow triggers
  - Dashboard or reporting changes
```

**Key Rule:** Don't start planning until scope is clear. Ask questions early.

## Phase T2: Plan

**Goal:** Design the approach before writing code.

**Procedure:**
1. Explore the relevant parts of the codebase
2. Identify files to create/modify
3. Consider how changes interact with existing scripts and workflows
4. Document the plan
5. Get user approval on plan before implementing

**Output:** Implementation plan with files and approach

```markdown
## Plan
- **Area:** E2E runner orchestration
- **Files to modify:**
  - scripts/run-e2e.sh (add retry loop)
  - .github/workflows/run-e2e.yml (pass retry count input)
- **Approach:** Wrap test execution in retry loop with configurable count
```

**Key Rule:** Get user approval on plan before implementing.

## Phase T3: Implement

**Goal:** Write code following project patterns.

**Procedure:**
1. Follow existing code patterns and conventions in the project
2. Work in small increments
3. Keep changes minimal and focused on the scope
4. Use proper shell scripting practices (set -euo pipefail, quoting, etc.)
5. Follow YAML best practices for workflow files

**Guidelines:**
- Match existing code style and patterns
- Don't over-engineer
- Keep shell scripts defensive (error handling, input validation)
- Use consistent naming with existing files

**Output:** Working code changes

**Key Rule:** Minimal changes only. Don't refactor unrelated code.

## Phase T4: Verify

**Goal:** Ensure implementation is complete and correct.

**Procedure:**
1. Review the diff of all changes against the original scope
2. Run shellcheck on modified shell scripts (if available)
3. Validate YAML syntax on modified workflow files
4. Check for common issues: unquoted variables, missing error handling, hardcoded values
5. Verify no unintended side effects in related files

**Output:** Changes reviewed, no obvious errors, ready for commit

```bash
# Verification checks (as applicable)
shellcheck scripts/run-e2e.sh       # Lint shell scripts
yamllint .github/workflows/*.yml    # Validate YAML syntax
git diff --stat                     # Review scope of changes
```

**Key Rule:** Don't skip the review step. Always check the diff against the original scope.

## Flow Diagram

```
+-------------------+
| Request received  |
+---------+---------+
          |
          v
+-------------------+     +-------------------+
| T1: SCOPE         |---->| Unclear?          |
| Understand req    |     | Ask user          |
+---------+---------+     +-------------------+
          | Clear
          v
+-------------------+     +-------------------+
| T2: PLAN          |---->| Need approval     |
| Design approach   |     | Show plan         |
+---------+---------+     +-------------------+
          | Approved
          v
+-------------------+     +-------------------+
| T3: IMPLEMENT     |---->| Issues?           |
| Write code        |     | Iterate           |
|                   |<----|                   |
+---------+---------+     +-------------------+
          | Complete
          v
+-------------------+     +-------------------+
| T4: VERIFY        |---->| Problems found?   |
| Review changes    |     | Fix and re-check  |
|                   |<----|                   |
+---------+---------+     +-------------------+
          | All clear
          v
+-------------------+
| Ready for         |
| commit            |
+-------------------+
```

## Task Context

Track progress in workflow context:

```json
{
  "type": "feat",
  "task": {
    "phase": "implement",
    "scopeConfirmed": true,
    "planApproved": true,
    "filesModified": ["scripts/run-e2e.sh"]
  }
}
```

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Start coding immediately | Scope and plan first |
| Plan in isolation | Get user approval on plan |
| Change unrelated code | Minimal changes only |
| Skip reviewing the diff | Always review changes against scope |
| Ignore lint/syntax errors | Fix all errors before commit |

## Automation

See `skill.yaml` for patterns and procedures.
See `sharp-edges.yaml` for common implementation pitfalls.
