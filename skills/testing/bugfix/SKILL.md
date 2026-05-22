---
name: bugfix
description: 'Investigates and fixes bugs systematically with root cause analysis. Use when asked to debug, troubleshoot, fix a bug, investigate an issue, or find why something is broken. Creates reproduction tests and verifies fixes.'
---

**User request**: $ARGUMENTS

Investigate and fix bugs with systematic root cause analysis. Orchestrates the complete debugging workflow from understanding the problem to verifying the fix.

> **Prerequisite**: Run in a git repository with a testable codebase.

## Workflow

**Loop**: Prerequisites → Gather context → Investigate/Fix → Verify → Report

This skill guides you through:
0. **Prerequisite Check** - Verify git repo, gather project context
1. **Bug Context Gathering** - Understand the bug through targeted questions (if not provided)
2. **Investigation** - Launch bug-fixer agent for deep analysis and fix implementation
3. **Verification Summary** - Report results and next steps

## Workflow

### Initial Setup (TodoWrite immediately)

**Create todo list** - phases to complete.

**Starter todos**:
```
- [ ] Prerequisite check; done when git status verified + project context gathered
- [ ] Bug context gathering (if needed); done when bug summary constructed
- [ ] Investigation and fix; done when bug-fixer agent completes
- [ ] Verification summary; done when results reported
```

### Phase 0: Prerequisite Check

**Mark "Prerequisite check" todo `in_progress`.**

**CRITICAL**: Before anything else, verify the environment:

1. **Check for git repository**: Run `git rev-parse --is-inside-work-tree`
2. **If NOT a git repo**: Warn the user:

```
"Warning: This doesn't appear to be a git repository. The bugfix workflow works best in a git repo where changes can be tracked and reverted if needed. Proceed anyway?"
```

Use AskUserQuestion:
```
header: "Not a Git Repository"
question: "This directory isn't a git repository. The bugfix workflow works best with git for tracking changes. How would you like to proceed?"
options:
  - "Continue anyway - I'll manage changes manually"
  - "Stop - I'll initialize git first"
```

3. **If git repo**: Check for uncommitted changes that might interfere:
   - Run `git status --porcelain`
   - If there are changes, note them but don't block (bugs often need fixing in dirty trees)

4. **Gather project context**:
   - Look for test configuration files (jest.config.*, pytest.ini, vitest.config.*, etc.)
   - Identify the test command if possible (check package.json scripts, pyproject.toml, etc.)
   - Note the project language/framework for context

**Mark "Prerequisite check" todo `completed`.**

### Phase 1: Bug Context Gathering

**Mark "Bug context gathering" todo `in_progress`.**

**If the user provided detailed bug information** (error message, reproduction steps, or clear description), skip directly to Phase 2.

**If bug information is vague or missing**, use AskUserQuestion to gather essential context:

**Question 1: Bug Type**

```
header: "Bug Type"
question: "What type of bug are you experiencing?"
options:
  - "Error/Exception - code crashes or throws an error"
  - "Wrong behavior - code runs but does the wrong thing"
  - "Performance - code is slow or uses too many resources"
  - "UI/Visual - display issues or broken UI"
  - "Data issue - incorrect data, missing data, or data corruption"
  - "Integration - problem with external service or API"
```

**Question 2: Reproduction Information**

```
header: "Reproduction"
question: "Can you reproduce this bug?"
options:
  - "Yes, consistently - it happens every time"
  - "Yes, sometimes - it happens intermittently"
  - "Not sure - I've only seen it once or twice"
  - "No - it only happened in production/another environment"
```

**Question 3: Error Details** (if type is Error/Exception)

```
header: "Error Details"
question: "Do you have an error message or stack trace?"
options:
  - "Yes - I'll paste it below"
  - "No - no error message available"
  - "Partial - I have some error info"
freeText: true
placeholder: "Paste the error message or stack trace here..."
```

**Question 4: Location Hints**

```
header: "Location"
question: "Do you know where in the codebase the bug might be?"
options:
  - "Yes - I know the specific file(s)"
  - "Somewhat - I know the general area"
  - "No idea - I need help finding it"
freeText: true
placeholder: "If you know the location, describe it here (file names, function names, etc.)..."
```

**Question 5: Recent Changes** (helpful for tracking root cause)

```
header: "Recent Changes"
question: "Did this bug appear after recent changes?"
options:
  - "Yes - it worked before, broke recently"
  - "Unknown - not sure when it started"
  - "No - it's been like this for a while"
  - "New feature - this is new code that doesn't work"
```

**Construct Bug Summary**:
After gathering context, summarize:
- Bug type and symptoms
- Reproduction status
- Error details (if any)
- Location hints (if any)
- Recent change context

**Mark "Bug context gathering" todo `completed`.**

### Phase 2: Investigation and Fix

**Mark "Investigation and fix" todo `in_progress`.**

Launch the bug-fixer agent to perform the actual investigation and fix work.

**Launch Bug-Fixer Agent:**

```
Use the bug-fixer agent to investigate and fix the bug.

Bug Summary:
[Constructed from Phase 1 or user's original input]

Context:
- Project type: [detected language/framework]
- Test command: [if discovered]
- Working tree status: [clean/dirty]
- Recent changes: [if provided]

The agent should:
1. Deep investigation - explore codebase, form hypotheses
2. Root cause analysis - trace through code paths
3. Create reproduction test - prove understanding of the bug
4. Implement fix - targeted fix addressing root cause
5. Verify fix - ensure test passes, no regressions
```

The bug-fixer agent will:
1. Investigate the codebase thoroughly
2. Form and test hypotheses about root cause
3. Create a test that reproduces the bug
4. Implement a fix
5. Verify the fix works

**IMPORTANT**: Let the agent work autonomously. Do not interrupt unless it asks for input or gets stuck.

**Mark "Investigation and fix" todo `completed`.**

### Phase 3: Verification Summary

**Mark "Verification summary" todo `in_progress`.**

After the bug-fixer agent completes, summarize the results:

**If fix was successful:**
```
Bug Fix Summary:
- Root cause: [what was wrong]
- Fix applied: [what was changed]
- Test added: [test file and name]
- Verification: [test results]

Recommended next steps:
1. Review the changes: `git diff`
2. Run full test suite to check for regressions
3. Commit when satisfied: `git add -A && git commit -m "fix: [description]"`
```

**If fix was not successful:**
```
Investigation Summary:
- What was tried: [approaches]
- What was learned: [findings]
- Blockers: [what prevented the fix]

Recommended next steps:
- [Specific suggestions based on findings]
```

**Mark "Verification summary" todo `completed`. Mark all todos complete.**

## Key Principles

| Principle | Rule |
|-----------|------|
| **Track progress** | Use TodoWrite to track phases; mark progress immediately; visible state at all times |
| **Systematic** | Form hypotheses before changes; test methodically; document findings |
| **Test-driven** | Create reproduction test BEFORE fixing; test proves fix works; prevents regression |
| **Root cause** | Fix underlying cause, not symptoms; consider why bug wasn't caught; look for patterns |
| **Minimal changes** | Smallest fix for root cause; avoid refactoring while bug fixing; keep focused |
| **Reduce cognitive load** | AskUserQuestion for clarification; reasonable defaults; don't repeat questions |

## Edge Cases

### Cannot Reproduce
If the bug cannot be reproduced:
1. Document reproduction attempts
2. Look for environmental differences
3. Check logs for clues
4. Consider adding diagnostic logging

### Multiple Bugs
If investigation reveals multiple related bugs:
1. Focus on fixing one at a time
2. Document the others for follow-up
3. Consider if there's a common root cause

### Fix Breaks Other Things
If the fix causes test failures:
1. Analyze if the tests are testing the wrong behavior
2. Update tests if they were asserting buggy behavior
3. Find an alternative fix if tests are correct
