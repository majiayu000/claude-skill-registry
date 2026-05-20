---
name: codebase-quality:post-push
description: Fetch GitHub feedback after git push OR PR creation. These are TWO SEPARATE use cases with different feedback sources. Use the Python script with appropriate flags.
version: 3.0.0
title: "Codebase Quality:Post Push"
status: active
---

# Post-Push Review Sub-Skill

Part of the [codebase-quality](../SKILL.md) skill family.

## Purpose

Fetch GitHub feedback for **two distinct scenarios**:

| Scenario | Trigger | Feedback Source | Script Flag |
|----------|---------|-----------------|-------------|
| **Push** | `git push` | Check run annotations, commit comments | `--commit <sha>` |
| **PR Creation** | `gh pr create` | PR bot comments, reviews | `--pr <num>` |

**These are SEPARATE use cases - do not conflate them.**

## The Python Script

All feedback fetching uses the CLI tool:
```
.claude/skills/codebase-quality/post-push/fetch-github-feedback.py
```

## Scenario 1: After `git push`

**What happens**: Post-Push Code Review workflow runs, produces check run annotations.

**What to check**: Push-level feedback ONLY.

```python
# MANDATORY after git push
Task(
    subagent_type="general-purpose",
    model="haiku",
    run_in_background=True,
    description="Poll GitHub for push feedback",
    prompt="""
    Monitor GitHub for push-level feedback after a git push.

    CONTEXT:
    - Commit SHA: {commit_sha}
    - Branch: {branch}
    - Project path: {project_path}

    TASK: Poll for workflow completion, then fetch PUSH-LEVEL feedback only.

    ## Step 1: Poll for workflow completion (max 10 min, every 30s)
    ```bash
    gh run list --commit {commit_sha} --json status,conclusion,name
    ```
    Wait until status != "in_progress" and status != "queued"

    ## Step 2: Run the feedback script for PUSH-LEVEL ONLY
    ```bash
    cd {project_path}
    python .claude/skills/codebase-quality/post-push/fetch-github-feedback.py --commit {commit_sha}
    ```

    ## Step 3: Report the script output to the user

    IMPORTANT: Do NOT check PR comments - this is a push event, not a PR event.
    """
)
```

**User notification:**
```
🔄 Background agent monitoring push feedback.
   Commit: {sha}
   Checking: Workflow runs, check run annotations, commit comments
```

## Scenario 2: After `gh pr create`

**What happens**: Claude Code workflow runs on PR creation, produces PR comments.

**What to check**: PR-level feedback ONLY.

```python
# MANDATORY after gh pr create
Task(
    subagent_type="general-purpose",
    model="haiku",
    run_in_background=True,
    description="Poll GitHub for PR feedback",
    prompt="""
    Monitor GitHub for PR-level feedback after PR creation.

    CONTEXT:
    - PR Number: {pr_number}
    - Project path: {project_path}

    TASK: Poll for PR workflow completion, then fetch PR-LEVEL feedback only.

    ## Step 1: Poll for PR checks to complete (max 10 min, every 30s)
    ```bash
    gh pr checks {pr_number} --json name,status,conclusion
    ```
    Wait until all checks complete.

    ## Step 2: Run the feedback script for PR-LEVEL ONLY
    ```bash
    cd {project_path}
    python .claude/skills/codebase-quality/post-push/fetch-github-feedback.py --pr {pr_number}
    ```

    ## Step 3: Report the script output to the user

    IMPORTANT: Focus on PR bot comments - this is a PR creation event.
    """
)
```

**User notification:**
```
🔄 Background agent monitoring PR feedback.
   PR: #{number}
   Checking: Bot comments, review comments
```

## Quick Reference

### Script Usage

```bash
# After git push - check PUSH-LEVEL feedback
python fetch-github-feedback.py --commit abc123def

# After gh pr create - check PR-LEVEL feedback
python fetch-github-feedback.py --pr 137

# Auto-detect (NOT recommended - be explicit!)
python fetch-github-feedback.py --auto

# JSON output for parsing
python fetch-github-feedback.py --commit abc123 --json

# Quiet mode (only output if findings)
python fetch-github-feedback.py --commit abc123 --quiet
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success, no critical/high issues |
| 1 | High severity issues found |
| 2 | Critical severity issues found |

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    git push succeeds                         │
├─────────────────────────────────────────────────────────────┤
│ 1. Launch background agent                                   │
│ 2. Agent polls: gh run list --commit <sha>                  │
│ 3. Agent runs: fetch-github-feedback.py --commit <sha>      │
│ 4. Agent reports: Check run annotations, commit comments    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  gh pr create succeeds                       │
├─────────────────────────────────────────────────────────────┤
│ 1. Launch background agent                                   │
│ 2. Agent polls: gh pr checks <num>                          │
│ 3. Agent runs: fetch-github-feedback.py --pr <num>          │
│ 4. Agent reports: PR bot comments, review comments          │
└─────────────────────────────────────────────────────────────┘
```

## What Each Flag Checks

### `--commit <sha>` (Push-Level)

| Source | Command Used | What It Contains |
|--------|--------------|------------------|
| Workflow runs | `gh run list --commit` | Pass/fail status |
| Check run annotations | `gh api commits/<sha>/check-runs` | `::warning`, `::error` from workflows |
| Commit comments | `gh api commits/<sha>/comments` | Direct comments on commit |

### `--pr <num>` (PR-Level)

| Source | Command Used | What It Contains |
|--------|--------------|------------------|
| PR comments | `gh pr view --json comments` | Bot-generated analysis |
| PR reviews | `gh pr view --json reviews` | Review decisions |

## Severity Levels

| Level | Examples |
|-------|----------|
| CRITICAL | Workflow failed, check run conclusion="failure" |
| HIGH | Annotation level="failure", changes requested |
| MEDIUM | Annotation level="warning" |
| LOW | Annotation level="notice", all passing |

## Common Mistakes to Avoid

❌ **Wrong**: After `git push`, checking PR comments
```python
# WRONG - git push doesn't trigger PR workflows!
fetch-github-feedback.py --pr 137
```

✅ **Correct**: After `git push`, check push-level feedback
```python
# CORRECT - push triggers push workflows
fetch-github-feedback.py --commit abc123
```

❌ **Wrong**: After `gh pr create`, checking commit annotations
```python
# WRONG - PR creation triggers PR workflows, not push workflows!
fetch-github-feedback.py --commit abc123
```

✅ **Correct**: After `gh pr create`, check PR-level feedback
```python
# CORRECT - PR creation triggers PR workflows
fetch-github-feedback.py --pr 137
```

## Integration with CLAUDE.md

The CLAUDE.md protocol specifies:

**After `git push`:**
```python
Skill("codebase-quality", args="post-push --commit")
```

**After `gh pr create`:**
```python
Skill("codebase-quality", args="post-push --pr")
```

---

**Skill Version**: 3.0.0
**Last Updated**: 2025-12-23
**Parent Skill**: [codebase-quality](../SKILL.md)
