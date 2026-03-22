---
name: bugfix
description: Execute a complete bugfix workflow for wouterwisse.com using Opus subagents. Investigates root cause, implements fix, and verifies no regressions.
allowed-tools: Task, TodoWrite, TaskOutput
---

# Bugfix Skill - Orchestrator

**Orchestrator ONLY spawns Opus subagents and collects summaries. ALL work is delegated.**

## Critical Rules

1. **NEVER read files** - subagents read files
2. **NEVER run commands** - subagents run commands
3. **NEVER create commits** - subagents create commits
4. Orchestrator only: spawns agents, tracks todos, reports summaries
5. **Always use Opus model** for ALL Task agents (`model: "opus"`)

---

## Phase 0: Setup Subagent

Spawn a single subagent to understand the bug and set up branches:

```
Task(general-purpose, model: opus):

Parse bug report and set up fix branch.

---

## Tasks

1. **Parse Bug Report**:
   - Extract bug summary and symptoms
   - Identify affected areas (pages, components, scripts)
   - Note reproduction steps (if provided)
   - Determine severity and impact

2. **Validate Bug Report**:
   - Is it actionable? (clear symptoms, reproducible)
   - What areas might be affected?
   - Are there related error messages?

3. **Create Fix Branch**:
   ```bash
   git checkout main && git pull && git checkout -b fix/<name>
   ```

---

## Output Format

```yaml
---
BUG_VALID: true | false
QUESTIONS_IF_INVALID: []
BUG_REPORT:
  title: "[bug summary]"
  symptoms: "[description of what's wrong]"
  reproduction_steps: [list, if known]
  severity: high | medium | low
AFFECTED_AREAS:
  - pages: [list of routes]
  - components: [list of components]
  - scripts: [scripts affected]
  - other: [any other affected areas]
BRANCH_NAME: fix/<name>
---
```
```

**If BUG_VALID: false** → Ask user for clarification before proceeding.

---

## Phase 1: Investigation Subagents (Parallel)

Spawn parallel investigation subagents to find root cause:

```
Task(Explore, model: opus, run_in_background: true):
Investigate bug in affected pages and components.

Find:
- Code paths that could cause the reported symptoms
- Recent changes to affected files (git log)
- Similar patterns that might have the same issue

Output the likely root cause locations and evidence.

---

Task(Explore, model: opus, run_in_background: true):
Search for error patterns and edge cases.

Find:
- Error handling in affected areas
- Edge cases that might not be covered
- State management issues
- Async/timing issues

Output findings relevant to the bug.

---

Task(Explore, model: opus, run_in_background: true):
Check for related issues in similar code.

Find:
- Other code using the same patterns
- Whether the bug might exist elsewhere
- Test coverage for affected areas

Output findings and potential regression points.
```

Wait for all investigation subagents with TaskOutput. Synthesize findings for root cause analysis.

---

## Phase 2: Root Cause Analysis Subagent

Spawn analysis subagent with investigation results:

```
Task(general-purpose, model: opus):

Analyze investigation findings and create fix plan.

---

## Context

BUG_REPORT: [from Phase 0]
INVESTIGATION_FINDINGS: [synthesis from Phase 1]
AFFECTED_AREAS: [list]

---

## Requirements

1. Determine the root cause with evidence
2. Write fix plan to: .claude/plans/<name>.fix.md
3. Include:
   - Root cause explanation
   - Fix approach
   - Files to modify
   - Regression risks
   - Verification steps

---

## Output Format

```yaml
---
ROOT_CAUSE: "[clear explanation of what causes the bug]"
PLAN_FILE: .claude/plans/<name>.fix.md
FIX_STEPS:
  - id: fix-1
    content: "[what to fix]"
    files: [list of files]
    regression_risk: low | medium | high
VERIFICATION_STEPS:
  - "[how to verify the fix works]"
---
```
```

---

## Phase 3: Review Subagent

Spawn review subagent to validate fix plan:

```
Task(general-purpose, model: opus):

Review fix plan for completeness and correctness.

---

## Tasks

1. Read: .claude/plans/<name>.fix.md

2. Validate:
   - Root cause is correctly identified
   - Fix addresses the root cause (not just symptoms)
   - All affected files are included
   - Regression risks are identified
   - Verification steps are complete

3. If issues found: FIX THEM directly in the plan file

---

## Output Format

```yaml
---
REVIEW_RESULT: APPROVED | NEEDS_REVISION
CHANGES_MADE: [list of changes, if any]
---
```
```

---

## Phase 4: Implementation Subagents

Execute fix steps by invoking `/task` skill. For simple fixes (1-2 steps), run sequentially. For larger fixes, analyze dependencies for wave-based execution.

For EACH fix step, spawn subagent that invokes `/task`:

```
Task(general-purpose, model: opus):

Execute fix step by invoking /task skill.

---

## Step Details

STEP_ID: [from plan]
CONTENT: [fix description from plan]
ROOT_CAUSE: [context about what we're fixing]

---

## Workflow

1. **Invoke the /task skill**:
   ```
   Skill(task)
   ```

   Pass these details to /task:
   - TASK: [CONTENT from step details]
   - Context: This is a bugfix for [ROOT_CAUSE]
   - Note: /task will handle quality checks and commit

2. **After /task completes**, return the result.

---

## Output Format

```yaml
---
STEP_ID: [id]
STATUS: SUCCESS | FAILURE
COMMIT: [short hash from /task]
FILES_CHANGED: [list from /task]
BUILD: PASSED | FAILED
LINT: PASSED | FAILED
ERRORS: [if FAILURE]
---
```
```

---

## Phase 5: Verification Subagents (Parallel)

Spawn parallel verification subagents:

```
Task(general-purpose, model: opus, run_in_background: true):

Verify the bug is fixed.

---

## Verification Tasks

1. Check that the original bug symptoms are resolved
2. Run through reproduction steps (if applicable)
3. Verify the fix addresses root cause

---

## Output Format

```yaml
---
BUG_FIXED: true | false
VERIFICATION_EVIDENCE: "[how we know it's fixed]"
---
```

---

Task(general-purpose, model: opus, run_in_background: true):

Check for regressions and code quality.

---

## Checks

1. TypeScript strict compliance:
   npx tsc --noEmit

2. Lint compliance:
   npm run lint

3. Build passes:
   npm run build

4. No forbidden patterns:
   grep -rn 'console.log\|TODO\|FIXME' --include='*.ts' --include='*.tsx' src/

---

## Output Format

```yaml
---
STATUS: PASSED | FAILED
BUILD: PASSED | FAILED
LINT: PASSED | FAILED
REGRESSIONS_FOUND: [list if any]
---
```
```

**Both must pass before proceeding.**

---

## Phase 6: Completion Subagent

Spawn completion subagent:

```
Task(general-purpose, model: opus):

Finalize bugfix implementation.

---

## Context

BRANCH_NAME: [from Phase 0]
PLAN_FILE: .claude/plans/<name>.fix.md
BUG_TITLE: [from Phase 0]
ROOT_CAUSE: [from Phase 2]

---

## Tasks

1. **Final validation**:
   - Build passes
   - No uncommitted changes
   - Bug is verified fixed

2. **Push fix branch**:
   ```bash
   git push -u origin [branch]
   ```

3. **Create PR**:
   ```bash
   gh pr create --base main --title "fix: [title]" --body "## Summary
   Fixes: [bug description]

   ## Root Cause
   [root cause explanation]

   ## Changes
   [bullets describing the fix]

   ## Test Plan
   - [ ] Build passes
   - [ ] TypeScript strict mode passes
   - [ ] Lint passes
   - [ ] Bug no longer reproduces
   - [ ] No regressions observed"
   ```

4. **DELETE plan file** (MANDATORY):
   ```bash
   rm -f .claude/plans/<name>.fix.md
   ```

---

## Output Format

```yaml
---
STATUS: COMPLETE
PR_URL: [url]
PLAN_DELETED: true
---
```
```

---

## Phase 7: Report to User

Summarize all results:

```markdown
## Bugfix Complete

**Bug**: [title]

### Root Cause
[brief explanation]

### Fix Applied
- Files changed: [list]
- Commits: X

### Verification
- Bug fixed: YES
- Build: PASSED
- TypeScript: PASSED
- Lint: PASSED
- Regressions: None found

### PR Created
[url]

### Next Steps
1. Review the PR
2. Run `/fix-pr` to address review comments
3. Merge when ready
```

---

## Progress Tracking

Use TodoWrite throughout:

```yaml
todos:
  - content: "Parse bug and setup branch"
    status: completed
  - content: "Investigate root cause"
    status: completed
  - content: "Create fix plan"
    status: completed
  - content: "Review fix plan"
    status: completed
  - content: "Implement fix"
    status: in_progress
  - content: "Verify fix and check regressions"
    status: pending
  - content: "Create PR"
    status: pending
```

---

## Key Principles

1. **Orchestrator is minimal** - only spawns and collects
2. **Root cause first** - understand before fixing
3. **Fix the cause, not symptoms** - avoid band-aid solutions
4. **Verify thoroughly** - confirm fix works, no regressions
5. **Each step uses /task** - consistent implementation workflow
6. **Clean completion** - plan files deleted, PRs created
