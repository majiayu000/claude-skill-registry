---
name: context-restore
description: "Use when you need to fully restore working context from a previous session - loads STATUS.json, reads key files, rebuilds mental model of current work state. Do NOT use for quick questions or when starting fresh unrelated work - the full context restoration adds overhead that isn't needed for standalone tasks."
---

# Context Restore

## Overview

Fully restore working context when resuming after a break. Goes beyond STATUS.json to rebuild complete understanding.

**Core principle:** Don't just know what to do - understand why and how.

**Trigger:** After session-resume for Fresh Start sessions, or manual deep restore

## The Restore Process

### Step 1: Load STATUS.json

Read and parse the status file:

- Project name and current branch
- In-progress tasks
- Focus area and next action
- Key decisions made

### Step 2: Review Git State

```bash
# See what's changed
git status

# Review recent commits for context
git log --oneline -10

# See uncommitted changes
git diff --stat
```

### Step 3: Read Key Files

Based on focus area, read relevant files:

**If working on feature:**

- Main feature file(s)
- Related test files
- Recently modified files (git diff --name-only)

**If debugging:**

- Error-related files
- Test files that failed
- Log files if available

**If refactoring:**

- Files being refactored
- Files that import/use them
- Test coverage for affected areas

### Step 4: Check Project State

```bash
# Run tests to verify state
npm test

# Check for lint errors
npm run lint

# Verify build passes
npm run build
```

### Step 5: Rebuild Mental Model

Construct understanding:

```markdown
## Current Context

### What We're Building

[Feature description from STATUS.json focus area]

### Where We Are

- Branch: [branch name]
- Last commit: [commit message]
- Uncommitted: [files and their purpose]

### Key Files

- `path/to/main.ts` - [what it does, current state]
- `path/to/test.ts` - [test coverage status]

### Decisions Made

- [Decision 1 from keyDecisions]
- [Decision 2]

### What's Next

1. [nextAction from STATUS.json]
2. [Logical following step]

### Potential Issues

- [Any warnings from tests/lint]
- [Any blockers noted]
```

### Step 6: Offer Continuation

Present restored context and options:

```
Context fully restored. Here's where we are:

[Mental model summary]

Ready to continue. Options:
1. Proceed with: [next action]
2. Review specific file first
3. Run full test suite
4. See detailed task breakdown

What would you like to do?
```

## Deep Restore Checklist

For complex projects or long breaks:

- [ ] STATUS.json loaded and parsed
- [ ] Git branch and status verified
- [ ] Recent commits reviewed
- [ ] Key files read and understood
- [ ] Tests run and status known
- [ ] Build verified
- [ ] Services checked
- [ ] Mental model constructed
- [ ] Next action clear

## Example Restore

```
🔍 Full Context Restore

Loading STATUS.json...
✓ Project: my-app
✓ Branch: feature/user-auth
✓ Focus: Authentication system

Reviewing git state...
✓ Last commit: a7f3c2e - feat: add login form
✓ 2 uncommitted files:
  - src/auth/reset.ts (new)
  - src/auth/reset.test.ts (new)

Reading key files...
✓ src/auth/login.ts - Login form complete
✓ src/auth/reset.ts - Password reset in progress (50%)
✓ Tests: 45 passing, 0 failing

Mental Model:
- Building password reset flow
- Login and validation complete
- Reset flow needs: email template, token generation
- Using nodemailer (decided last session)

Next action: Add forgot password email template

Ready to continue?
```

## When to Use

**Use context-restore when:**

- Fresh Start session (> 4 hours gap)
- Complex feature with many files
- Returning after distraction
- Unclear on previous state
- Need to verify decisions made

**Skip context-restore when:**

- Continuation session (< 30 min)
- Simple, single-file work
- Just committed everything
- Clear on what to do next

## Integration

**Pairs with:**

- **session-resume** - Triggers context-restore for Fresh Start
- **session-capture** - Creates the STATUS.json being restored

**Calls:**

- Read tool to examine key files
- Bash for git commands and tests
- TodoWrite to restore task state
