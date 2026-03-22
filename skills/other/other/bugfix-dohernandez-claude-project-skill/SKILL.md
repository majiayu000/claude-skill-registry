---
name: bugfix
description: "Structured debugging process for bug fixes: reproduce, plan, fix, verify. Use when fixing bugs."
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
      command: "task claude:validate-skill -- --skill bugfix"
---

# Bugfix

## Purpose

Structured debugging methodology for fixing bugs. Ensures bugs are properly understood before fixing, root-caused with evidence, and fixed with minimal changes.

## Quick Reference

- **Phases**: Reproduce -> Plan -> Fix -> Verify
- **Key Rule**: Understand before changing
- **Output**: Minimal fix with verified resolution

## Bug Fix Phases

```
+---------------------------------------------------------------------------------+
|                              BUG FIX WORKFLOW                                   |
+---------------------------------------------------------------------------------+
|  1. REPRODUCE  ->  2. PLAN  ->  3. FIX  ->  4. VERIFY                          |
+---------------------------------------------------------------------------------+
```

## Phase B1: Reproduce the Bug

**Goal:** Confirm the bug exists and understand how to trigger it.

**Procedure:**
1. Read the bug description and any error logs/screenshots
2. Identify the reproduction steps from the report
3. Execute reproduction steps (run the script, trigger the workflow, check logs)
4. Document the observed behavior vs expected behavior
5. If cannot reproduce: ask user for more context, check environment differences

**Output:** Bug reproduction confirmed with clear steps

```markdown
## Bug Reproduction
- **Steps to reproduce:**
  1. Trigger dispatch with profile=32-validators
  2. Observe run-e2e.sh exits at webdriver step
- **Expected:** WebDriver cluster starts successfully
- **Actual:** Script exits with error "docker compose file not found"
- **Environment:** Self-hosted runner, Docker 24.x
```

**Key Rule:** Cannot proceed without reproduction. If you can't trigger the bug, you can't verify the fix.

## Phase B2: Plan (Root Cause + Fix)

**Goal:** Understand WHY the bug occurs and design the fix approach.

**Procedure:**
1. Trace the code path from reproduction steps
2. Read relevant source files (scripts, workflow YAML)
3. Form hypothesis about the cause
4. **If root cause is unclear:**
   - Add temporary debug output (echo/printf in shell scripts)
   - Run with debug output and analyze
   - **Do NOT change implementation logic yet**
5. Once root cause is identified, design the minimal fix approach
6. **Get user approval on the fix plan**

**Debug Output Pattern:**
```bash
# Temporary debug output to identify root cause
echo "[DEBUG] PROFILE=$PROFILE" >&2
echo "[DEBUG] COMPOSE_FILE=$COMPOSE_FILE" >&2
echo "[DEBUG] pwd=$(pwd)" >&2
```

**Output:** Root cause identified + fix plan approved

```markdown
## Root Cause & Fix Plan
- **Location:** `scripts/run-e2e.sh:87`
- **Cause:** COMPOSE_FILE path uses relative path that breaks when working directory changes
- **Why it happens:** cd into cloned repo changes pwd but COMPOSE_FILE was set before cd
- **Fix:** Use absolute path for COMPOSE_FILE or set it after cd
- **Edge cases:** Both single and cluster WebDriver paths need fixing
```

**Key Rule:** Get user approval before proceeding. Never guess-and-fix.

## Phase B3: Fix

**Goal:** Implement the minimal fix that resolves the root cause.

**Procedure:**
1. Make the **minimal change** to fix the root cause
2. Remove any temporary debug output added in Phase B2
3. Do not refactor, clean up, or "improve" surrounding code

**Output:** Fix applied, debug output removed

```bash
# Before (bug)
COMPOSE_FILE="docker/webdriver/docker-compose.yml"
cd "$CLONE_DIR"
docker compose -f "$COMPOSE_FILE" up -d

# After (fix)
cd "$CLONE_DIR"
COMPOSE_FILE="$(pwd)/docker/webdriver/docker-compose.yml"
docker compose -f "$COMPOSE_FILE" up -d
```

**Key Rule:** Minimal fix only. Do not refactor, clean up, or "improve" surrounding code. That's a separate task.

## Phase B4: Verify

**Goal:** Ensure the fix resolves the bug and doesn't break anything else.

**Procedure:**
1. Re-run the reproduction steps to confirm the bug is fixed
2. Review the diff to ensure changes are minimal and correct
3. Run shellcheck on modified shell scripts (if available)
4. Validate YAML syntax on modified workflow files (if available)
5. Check related code paths for similar issues (the same bug pattern may exist elsewhere)
6. Verify no unintended side effects in related files

**Output:** Fix verified, no regressions

```bash
# Verification checks (as applicable)
shellcheck scripts/run-e2e.sh       # Lint shell scripts
yamllint .github/workflows/*.yml    # Validate YAML syntax
git diff --stat                     # Review scope of changes
```

## Flow Diagram

```
+-------------------+
| Bug reported      |
+---------+---------+
          |
          v
+-------------------+     +-------------------+
| B1: REPRODUCE     |---->| Cannot reproduce? |
|                   |     | Ask for context   |
+---------+---------+     +-------------------+
          | Confirmed
          v
+-------------------+     +-------------------+
| B2: PLAN          |---->| Unclear cause?    |
| Root cause +      |     | Add debug output  |
| fix approach      |<----| Re-analyze        |
+---------+---------+     +-------------------+
          | User approved
          v
+-------------------+     +-------------------+
| B3: FIX           |---->| Doesn't resolve?  |
| Minimal change    |     | Re-analyze fix    |
|                   |<----|                   |
+---------+---------+     +-------------------+
          | Fixed
          v
+-------------------+     +-------------------+
| B4: VERIFY        |---->| Issues found?     |
| Review + check    |     | Check side        |
|                   |<----| effects           |
+---------+---------+     +-------------------+
          | All clear
          v
+-------------------+
| Ready for         |
| commit            |
+-------------------+
```

## Bug Fix Context

When working on a bug fix, track progress:

```json
{
  "type": "fix",
  "bugfix": {
    "phase": "plan",
    "reproductionConfirmed": true,
    "rootCause": "Relative path breaks after cd into clone directory",
    "rootCauseLocation": "scripts/run-e2e.sh:87",
    "planApproved": true
  }
}
```

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Jump straight to fixing | Reproduce first, plan the fix |
| Change code to debug | Add debug output, analyze, then change |
| Fix without approval | Get user approval on fix plan |
| Fix + refactor together | Minimal fix only, refactor separately |
| Skip verifying the fix | Always confirm the fix resolves the bug |
| Guess the root cause | Trace code path, add debug output if unclear |

## Automation

See `skill.yaml` for patterns and procedures.
See `sharp-edges.yaml` for common debugging pitfalls.
