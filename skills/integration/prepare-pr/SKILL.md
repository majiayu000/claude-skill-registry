---
name: prepare-pr
description: Generate PR title and description from multiple commits (Korean and English). Use when preparing a pull request with multiple commits that need consolidated description.
allowed-tools: Bash(git:*), Write
argument-hint: [BASE-BRANCH (default: auto-detect)]
disable-model-invocation: true
---

# Pull Request Content Generator

Generates PR title and description by analyzing all commits in the current branch compared to the base branch. **Creates both Korean and English versions for easy copying.**

## Repository State Analysis

- Git status: !`git status --porcelain`
- Current branch: !`git branch --show-current`
- Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main"`
- Remote branches: !`git branch -r --list 'origin/main' 'origin/master' 2>/dev/null`
- Commits since divergence: !`git log --oneline origin/HEAD..HEAD 2>/dev/null || git log --oneline origin/main..HEAD 2>/dev/null || git log --oneline origin/master..HEAD 2>/dev/null || echo "Unable to detect base branch"`
- Changed files summary: !`git diff --stat origin/HEAD..HEAD 2>/dev/null || git diff --stat origin/main..HEAD 2>/dev/null || git diff --stat origin/master..HEAD 2>/dev/null`

## What This Command Does

1. Detects the base branch (main/master) automatically or uses provided argument
2. Collects all commits from base to current HEAD
3. Analyzes commit messages and changed files
4. Generates a consolidated PR title (Conventional Commits style)
5. Generates PR description with summary, changes, and related issues
6. **Saves to pr_content.md file for easy copying**

## When to Use This Command

| Scenario                | Recommendation                                               |
| ----------------------- | ------------------------------------------------------------ |
| Single commit PR        | Use commit message directly (GitHub does this automatically) |
| **Multiple commits PR** | **Use this command** to consolidate changes                  |
| Large feature branch    | Use this command to summarize all work                       |

## PR Title Format (Conventional Commits)

```
<type>[(optional scope)]: <description>
```

### Type Selection for PRs

Analyze all commits and select the dominant type:

| Pattern                   | PR Type                           |
| ------------------------- | --------------------------------- |
| Mostly `feat` commits     | `feat`                            |
| Mostly `fix` commits      | `fix`                             |
| Mixed `feat` and `fix`    | `feat` (features take precedence) |
| Only `docs` commits       | `docs`                            |
| Only `chore`/`ci` commits | `chore`                           |
| `refactor` focused        | `refactor`                        |

**Priority**: `feat` > `fix` > `refactor` > `perf` > `docs` > `chore`

### Title Writing Guidelines

- **50 characters or less** (GitHub truncates longer titles)
- Focus on **user-facing value**, not implementation details
- Use imperative mood: "add feature" not "added feature"

## PR Body Format

### Summary Section

1-3 sentences describing the overall change and its purpose.

### Changes Section

- Bullet points of key changes
- Group by category if many changes
- Focus on **what** changed, not **how**

### Related Issues Section

- Extract issue numbers from branch name and commits
- Use `fix #N` format (consistent with commit.md)

## Output Template

```markdown
## PR Title (Korean)

{type}: {한글 제목}

## PR Title (English)

{type}: {English title}

---

## PR Body (Korean)

### 요약

{변경사항 요약 1-3문장}

### 주요 변경사항

- {변경사항 1}
- {변경사항 2}
- {변경사항 3}

### 관련 이슈

fix #{issue_number}

### 테스트 계획

{테스트 방법 - 필요시만}

---

## PR Body (English)

### Summary

{1-3 sentence summary of changes}

### Changes

- {Change 1}
- {Change 2}
- {Change 3}

### Related Issues

fix #{issue_number}

### Test Plan

{How to test - if needed}
```

## Important Notes

- This command ONLY generates PR content - it never creates actual PRs
- **pr_content.md file contains both versions** - choose the one you prefer
- For single-commit PRs, consider using the commit message directly
- If branch name contains issue number, it will be auto-detected
- Copy content from generated file and paste into GitHub PR form
- Use `gh pr create` with the generated content for CLI workflow

## Execution Instructions

1. **Determine base branch**: Use argument if provided, otherwise detect from origin/HEAD
2. **Collect commit information**: Run git log and git diff commands
3. **Analyze commits**: Count types, identify primary type, extract scope
4. **Extract issue numbers**: From branch name and commit messages
5. **Generate PR title**: Summarize in ≤50 chars
6. **Generate PR body**: Summary, changes, issues, test plan
7. **Create both versions**: Korean first, English second
8. **Write to file**: Save to `pr_content.md`
