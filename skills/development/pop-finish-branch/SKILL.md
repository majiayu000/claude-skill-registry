---
name: finishing-a-development-branch
description: "Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup. Presents exactly 4 options: merge locally, create PR, keep as-is, or discard. Do NOT use when tests are failing or work is incomplete - fix issues first before finishing the branch."
inputs:
  - from: pop-executing-plans
    field: tasks_completed
    required: false
  - from: pop-code-review
    field: merge_ready
    required: false
outputs:
  - field: completion_type
    type: string
  - field: pr_url
    type: string
  - field: issue_closed
    type: boolean
next_skills:
  - pop-session-capture
  - pop-using-git-worktrees
workflow:
  id: finish-branch
  name: Branch Completion Workflow
  version: 1
  description: Structured branch completion with verification
  steps:
    - id: verify_tests
      description: Run test suite to verify code works
      type: agent
      agent: test-writer-fixer
      next: test_result
    - id: test_result
      description: Evaluate test results
      type: user_decision
      question: "Test results?"
      header: "Tests"
      options:
        - id: passing
          label: "All passing"
          description: "Tests pass, ready to proceed"
          next: determine_base
        - id: failing
          label: "Some failing"
          description: "Tests fail, need to fix"
          next: fix_tests
        - id: no_tests
          label: "No tests"
          description: "No tests exist for this code"
          next: add_tests_decision
      next_map:
        passing: determine_base
        failing: fix_tests
        no_tests: add_tests_decision
    - id: fix_tests
      description: Fix failing tests
      type: skill
      skill: pop-test-driven-development
      next: verify_tests
    - id: add_tests_decision
      description: Decide on adding tests
      type: user_decision
      question: "Add tests before finishing?"
      header: "Tests"
      options:
        - id: yes
          label: "Add tests"
          description: "Write tests for this code first"
          next: fix_tests
        - id: no
          label: "Skip tests"
          description: "Proceed without tests (not recommended)"
          next: determine_base
      next_map:
        yes: fix_tests
        no: determine_base
    - id: determine_base
      description: Determine base branch
      type: agent
      agent: code-explorer
      next: completion_choice
    - id: completion_choice
      description: Choose how to complete the branch
      type: user_decision
      question: "Implementation complete. What would you like to do?"
      header: "Complete"
      options:
        - id: merge
          label: "Merge locally"
          description: "Merge back to base branch and clean up"
          next: merge_locally
        - id: pr
          label: "Create PR"
          description: "Push and create a Pull Request for review"
          next: create_pr
        - id: keep
          label: "Keep as-is"
          description: "Keep the branch, I'll handle it later"
          next: keep_branch
        - id: discard
          label: "Discard"
          description: "Delete this work permanently"
          next: confirm_discard
      next_map:
        merge: merge_locally
        pr: create_pr
        keep: keep_branch
        discard: confirm_discard
    - id: merge_locally
      description: Merge to base branch
      type: agent
      agent: code-architect
      next: post_merge_tests
    - id: post_merge_tests
      description: Verify tests after merge
      type: agent
      agent: test-writer-fixer
      next: cleanup_branch
    - id: create_pr
      description: Push branch and create PR
      type: agent
      agent: code-architect
      next: issue_close_decision
    - id: keep_branch
      description: Keep branch as-is
      type: terminal
    - id: confirm_discard
      description: Confirm discarding work
      type: user_decision
      question: "This will permanently delete the branch and all commits. Are you sure?"
      header: "Confirm"
      options:
        - id: yes
          label: "Yes, discard"
          description: "Permanently delete this work"
          next: discard_branch
        - id: no
          label: "Cancel"
          description: "Keep the branch"
          next: completion_choice
      next_map:
        yes: discard_branch
        no: completion_choice
    - id: discard_branch
      description: Delete branch and cleanup
      type: agent
      agent: code-architect
      next: cleanup_worktree
    - id: cleanup_branch
      description: Delete merged branch
      type: agent
      agent: code-architect
      next: issue_close_decision
    - id: cleanup_worktree
      description: Remove worktree if exists
      type: skill
      skill: pop-using-git-worktrees
      next: complete
    - id: issue_close_decision
      description: Close related issue?
      type: user_decision
      question: "Close the related GitHub issue?"
      header: "Issue"
      options:
        - id: yes
          label: "Yes, close it"
          description: "Mark issue as completed"
          next: close_issue
        - id: no
          label: "No, keep open"
          description: "Issue needs more work"
          next: next_action
      next_map:
        yes: close_issue
        no: next_action
    - id: close_issue
      description: Close GitHub issue
      type: agent
      agent: code-architect
      next: check_epic
    - id: check_epic
      description: Check if part of epic
      type: agent
      agent: code-explorer
      next: next_action
    - id: next_action
      description: Choose next action
      type: user_decision
      question: "What would you like to do next?"
      header: "Next Action"
      options:
        - id: another_issue
          label: "Another issue"
          description: "Work on another GitHub issue"
          next: fetch_issues
        - id: run_checks
          label: "Run checks"
          description: "Run full test suite"
          next: run_checks
        - id: exit
          label: "Exit"
          description: "Save state and exit"
          next: save_and_exit
      next_map:
        another_issue: fetch_issues
        run_checks: run_checks
        exit: save_and_exit
    - id: fetch_issues
      description: Fetch prioritized open issues
      type: agent
      agent: code-explorer
      next: complete
    - id: run_checks
      description: Run full test and lint suite
      type: agent
      agent: test-writer-fixer
      next: next_action
    - id: save_and_exit
      description: Save session state
      type: skill
      skill: pop-session-capture
      next: complete
    - id: complete
      description: Branch completion workflow done
      type: terminal
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

## The Process

### Step 1: Verify Tests

Before presenting options, run project test suite:

```bash
npm test / cargo test / pytest / go test ./...
```

**If tests fail:** Show failures and stop. Cannot proceed until tests pass.

**If tests pass:** Continue to Step 2.

### Step 2: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

### Step 3: Present Options

**ALWAYS use AskUserQuestion** - never present plain text numbered options:

```
Use AskUserQuestion tool with:
- question: "Implementation complete. What would you like to do?"
- header: "Complete"
- options:
  - label: "Merge locally"
    description: "Merge back to <base-branch> and clean up"
  - label: "Create PR"
    description: "Push and create a Pull Request for review"
  - label: "Keep as-is"
    description: "Keep the branch, I'll handle it later"
  - label: "Discard"
    description: "Delete this work permanently"
- multiSelect: false
```

### Step 4: Execute Choice

See `examples/merge-workflow.md` for detailed implementation of each option.

| Option            | Actions                                                                 |
| ----------------- | ----------------------------------------------------------------------- |
| **Merge locally** | Switch to base → Pull → Merge → Test → Delete branch → Cleanup worktree |
| **Create PR**     | Push branch → Create PR with gh → Cleanup worktree                      |
| **Keep as-is**    | Report preservation → Keep worktree                                     |
| **Discard**       | Confirm → Delete branch (force) → Cleanup worktree                      |

**Worktree cleanup** (Options 1, 2, 4 only):

```bash
git worktree list | grep $(git branch --show-current)
git worktree remove <worktree-path>  # if found
```

### Step 5: Issue Close & Continue

**Only when invoked via `/popkit:dev work #N`** - skip for standalone use.

#### 5a: Close Prompt

After merge (Option 1) or PR (Option 2):

```
Use AskUserQuestion tool with:
- question: "Work on issue #N complete. Close the issue?"
- header: "Close Issue"
- options:
  - label: "Yes, close it"
    description: "Mark issue as completed"
  - label: "No, keep open"
    description: "Issue needs more work or follow-up"
```

If "Yes": `gh issue close <number> --comment "Completed via /popkit:dev work #<number>"`

#### 5b: Epic Parent Check

Check for parent epic reference in issue body:

```bash
gh issue view <number> --json body --jq '.body' | grep -oE '(Part of|Parent:?) #[0-9]+'
```

If all children closed → Prompt to close epic.

#### 5c: Context-Aware Next Actions

See `examples/next-action-example.md` for detailed flow.

Generate dynamic options by fetching prioritized issues, sorting by priority/phase, and presenting top 3 + "session capture and exit".

## Quick Reference

| Option        | Merge | Push | Keep Worktree | Cleanup Branch | Close Prompt |
| ------------- | ----- | ---- | ------------- | -------------- | ------------ |
| Merge locally | ✓     | -    | -             | ✓              | ✓ (if issue) |
| Create PR     | -     | ✓    | ✓             | -              | ✓ (if issue) |
| Keep as-is    | -     | -    | ✓             | -              | -            |
| Discard       | -     | -    | -             | ✓ (force)      | -            |

## Red Flags

**Never:**

- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request

**Always:**

- Verify tests before offering options
- Present exactly 4 options via AskUserQuestion
- Get typed "discard" confirmation for Option 4
- Clean up worktree for Options 1 & 4 only

## Integration

**Called by:**

- **subagent-driven-development** (Step 7) - After all tasks complete
- **executing-plans** (Step 5) - After all batches complete

**Pairs with:**

- **using-git-worktrees** - Cleans up worktree created by that skill

<details>
<summary>Common Mistakes (Click to expand)</summary>

**Skipping test verification**

- Problem: Merge broken code, create failing PR
- Fix: Always verify tests before offering options

**Open-ended questions**

- Problem: "What should I do next?" → ambiguous
- Fix: Present exactly 4 structured options

**Automatic worktree cleanup**

- Problem: Remove worktree when might need it (Option 2, 3)
- Fix: Only cleanup for Options 1 and 4

**No confirmation for discard**

- Problem: Accidentally delete work
- Fix: Require typed "discard" confirmation

</details>
