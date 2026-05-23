---
name: sdlc
description: SDLC workflow automation that implements features using TDD skill, runs test-runner skill, and prepares commit commands for user review. Use when user provides a spec/plan for a new feature. Workflow: (1) invokes test-driven-development skill with spec, (2) invokes test-runner skill, (3) prepares git commands for user to execute manually.
---

# SDLC - Software Development Lifecycle Automation

## Overview

This skill automates the software development lifecycle workflow for implementing features:

**Workflow:** TDD Skill → Test-Runner Skill → Identify Files → Prepare Commit Commands

1. Invoke **test-driven-development skill** with the spec/plan
2. Invoke **test-runner skill** (handles lint, type checking, and all tests)
3. Identify all modified files related to the user's request
4. Prepare commit commands using `/commit` (saves to `tmp/git-commands.txt` for user to copy/paste)

**⚠️ NOTE:** This skill does NOT execute git commits or pushes. It prepares the commands for user review and manual execution.

## When This Skill Is Invoked

**Immediately execute the SDLC workflow. DO NOT ask questions first.**

**Execute these steps NOW:**

1. Invoke the **test-driven-development skill** with the spec/plan
2. Invoke the **test-runner skill**
3. Identify all modified files related to the user's request
4. Prepare commit commands with `/commit` (user executes manually)

**DO NOT:**
- ❌ Ask "Would you like me to run the workflow?"
- ❌ Wait for user confirmation before starting
- ❌ Run `just` commands directly (let test-runner skill handle them)
- ❌ Execute git commit or push commands directly

**JUST RUN IT. The user invoked this skill to complete the SDLC workflow.**

## Workflow

### Step 0: DRY Check - Can We Reuse Existing Patterns?

**BEFORE implementing, run semantic search to find similar implementations:**

```bash
docker exec arsenal-semantic-search-cli code-search find "<what the spec does>"
```

**Ask yourself:**
1. Does similar functionality already exist?
2. Could we **modify the spec slightly** to reuse existing infrastructure?
3. Would extending existing code be simpler than building new?

**If reuse is possible, STOP and propose spec modifications to the user:**
```
⚠️ SPEC SIMPLIFICATION OPPORTUNITY

I found existing infrastructure that does something similar:
- [existing pattern/file]

Instead of implementing the spec as-is, we could:
- Option A: Extend [existing thing] with minor changes
- Option B: Adjust the spec to use [existing pattern]

This would reduce complexity by [benefit].

Should I adjust the approach?
```

**Example:** If spec says "create new DSL for cron conditions" but you find `group_message_intervention_conditions_dsl` already handles similar logic, propose reusing/extending that instead.

**Only proceed to Step 1 after confirming no reuse opportunity exists.**

### Step 1: Invoke TDD Skill

Invoke the **test-driven-development skill** with the spec/plan:

```
Use the test-driven-development skill to implement '/path/to/spec.md'
```

Or with inline spec:

```
Use the test-driven-development skill to implement: [description]
```

The TDD skill handles all implementation details (tests first, watch fail, minimal code to pass, refactor).

### Step 2: Invoke Test-Runner Skill

Invoke the **test-runner skill**.

The test-runner skill handles:
- Lint and auto-fix (ruff)
- Type checking (mypy)
- Running all appropriate tests
- Ensuring code quality before commit

**Critical:** Do NOT proceed to prepare commits if test-runner reports failures.

### Step 3: Identify Modified Files

After test-runner completes successfully:
- Run `git status` to see all modified files
- Identify which files are related to the user's request
- Include both:
  - Files modified by TDD skill (production code and test files)
  - Files that were auto-fixed by the linter

### Step 4: Prepare Commit Commands

Run `/commit` with all modified files related to the user's request:

```
/commit api/src/services/user.py api/tests/unit/test_user.py
```

The `/commit` command:
1. Analyzes the changes
2. Creates appropriate conventional commit message(s)
3. **Saves git commands to `tmp/git-commands.txt`** as one-liners (does NOT execute them)
4. Tells user to run `cat tmp/git-commands.txt` to copy/paste

### Step 5: User Executes Manually

After the workflow completes, inform the user:

```
✅ SDLC workflow complete!

Git commands saved to: tmp/git-commands.txt

To commit and push:
1. View commands: cat tmp/git-commands.txt
2. Copy/paste each line to execute
3. Push: git push origin <branch-name>
```

## Usage Examples

### Example 1: Implement from spec file

```
Use the SDLC skill to implement spec/2024-12-15-user-auth/01-authentication.md
```

Runs: TDD skill → test-runner skill → prepare commit commands

### Example 2: Implement from inline description

```
Use the SDLC skill to add user authentication to the API
```

Runs: TDD skill → test-runner skill → prepare commit commands

## Notes

- **TDD First**: Always invokes test-driven-development skill first
- **Quality Gates**: Always invokes test-runner skill before preparing commits
- **Delegates to Skills**: Does NOT run `just` commands directly — lets skills handle details
- **Smart Commits**: Only includes files related to the user's request
- **Non-Executing**: Git commands are saved to `tmp/git-commands.txt` for user to copy/paste
- **No Questions**: Executes immediately when invoked (don't ask for confirmation)
- **No Broken Code**: Never prepares commits if test-runner reports failures
