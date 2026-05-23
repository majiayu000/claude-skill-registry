---
name: pr-review
description: Review and merge a PR with quality gates. Verifies AC coverage and spec alignment before merge. Used in subagent context.
---

# PR Review Skill

Review a PR linked to a kspec task, verify quality gates, and merge. This skill runs in **subagent context** (spawned by ralph) and focuses on getting the PR merged with proper quality verification.

## Usage

```
/pr-review @task-ref
```

**Task reference is required.** This skill needs to know which task's PR to review.

## Quick Start

```bash
# Validate inputs first
kspec task get @task-ref           # Verify task exists
gh pr list --search "Task: @task-ref"  # Find linked PR

# Start the workflow
kspec workflow start @pr-review-loop
```

## Validation (Before Starting)

### 1. Task Reference Required

If no task ref provided, error immediately:

```
Error: Task reference required.
Usage: /pr-review @task-ref
```

### 2. PR Must Exist

Find the PR linked to this task:

```bash
# Check task for vcs_refs
kspec task get @task-ref --json | jq '.vcs_refs'

# Or search PR body/commits for task reference
gh pr list --search "Task: @task-ref" --json number,url,title
```

If no PR found:

```
Error: No PR found for task @task-ref.
Create a PR first with /pr, then run /pr-review @task-ref.
```

## Quality Gates

This skill emphasizes **two key quality gates** beyond just "tests pass":

### 1. AC Coverage

Every acceptance criterion in the linked spec MUST have test coverage:

```typescript
// AC: @spec-ref ac-1
it('should validate task ref is provided', () => { ... });

// AC: @spec-ref ac-2
it('should error when no PR exists', () => { ... });
```

**Check for gaps:**
- Read spec ACs from `kspec task get @task-ref`
- Search test files for `// AC: @spec-ref ac-N` annotations
- Flag any ACs without test coverage

### 2. Spec Alignment

Implementation must match spec intent, not just pass tests:

- Read the spec description and ACs
- Read the implementation code
- Verify behavior matches spec (not just syntactically correct)
- Check for undocumented behavior or spec deviations

**This is NOT just "do tests pass"** - it's verifying the implementation actually does what the spec says.

## Workflow

This skill delegates all behavior to `@pr-review-loop` workflow:

```bash
kspec workflow start @pr-review-loop
```

The workflow handles:
1. Run local review (`/local-review`)
2. Verify AC coverage (all spec ACs have tests)
3. Verify spec alignment (implementation matches spec)
4. Fix issues if found
5. Wait for CI to pass
6. Merge with quality gates

### CRITICAL: CI Re-verification

**After ANY push, you MUST re-verify CI from the beginning.** Prior CI checks are invalidated by new commits. Never merge without fresh CI verification on the current HEAD.

If you push fixes during review:
1. Wait for CI to complete on the new commits
2. Verify CI status shows current HEAD (not stale)
3. Only then proceed to merge

## Subagent Context

This skill runs in **ACP subagent context**:
- Spawned by ralph for PR review
- Runs sequentially (ralph waits for completion)
- No human interaction expected
- Auto-resolves decisions based on quality gate outcomes

## Exit Conditions

- **PR merged** - Success, quality gates passed
- **Quality gates failed** - AC gaps or spec misalignment that couldn't be auto-fixed
- **CI failed** - Tests don't pass after fixes
- **PR not found** - Validation failed, no PR for task

## Example

```
/pr-review @task-reflect-loop-skill

[Validates task exists]
[Finds PR #234 linked to task]
[Starts @pr-review-loop workflow]
[Runs local review - checks AC coverage]
[Verifies spec alignment]
[Waits for CI]
[Merges PR]

PR #234 merged successfully.
Task @task-reflect-loop-skill ready for completion.
```

## Task Completion

**CRITICAL: You MUST complete the task after merging the PR.**

The `@pr-review-loop` workflow includes task completion as the final step (ac-7). After the PR is merged:

```bash
kspec task complete @task-ref --reason "Merged in PR #N. <summary>"
```

Include in the reason:
- PR number
- Summary of what was implemented
- Any notable changes or deviations
- AC coverage confirmation

Do NOT exit after merge without completing the task.
