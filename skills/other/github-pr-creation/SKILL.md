---
name: github-pr-creation
description: Creates GitHub Pull Requests with automated validation and task tracking. Use when user wants to create PR, open pull request, submit for review, or check if ready for PR. Analyzes commits, validates task completion, generates Conventional Commits title and description, suggests labels. NOTE - for merging existing PRs, use github-pr-merge instead.
---

# GitHub PR creation

Creates Pull Requests with task validation, test execution, and Conventional Commits formatting.

## Current state

!`git rev-parse --abbrev-ref HEAD 2>/dev/null`
!`git log @{u}..HEAD --oneline 2>/dev/null || echo "(no upstream tracking)"`

## Core workflow

### 1. Confirm target branch

**ALWAYS ask user before proceeding:**

```
Creating PR from [current-branch] to [target-branch]. Correct?
```

| Branch flow | Typical target |
|-------------|---------------|
| feature/* | develop |
| fix/* | develop |
| hotfix/* | main/master |
| develop | main/master |

### 2. Search for task documentation

Look for task/spec files that describe what this PR should accomplish. Common locations by tool:

| Tool/Convention | Path |
|-----------------|------|
| Spec2Ship (s2s) | `.s2s/plans/*.md` (look for active plan matching branch name or commits) |
| AWS Kiro | `.kiro/specs/*/tasks.md` |
| Cursor | `.cursor/rules/*.md`, `.cursorrules` |
| Trae | `.trae/rules/*.md` |
| GitHub Issues | `gh issue list --assignee @me --state open` |
| Generic | `docs/specs/`, `specs/`, `tasks.md`, `TODO.md` |

Extract task IDs, titles, descriptions, and requirements references when found.

### 3. Analyze commits

For each commit on this branch, identify type, scope, task references, and breaking changes. Map commits to documented tasks when task files exist.

### 4. Verify task completion

If task documentation exists:

1. Identify main task from branch name (e.g., `feature/task-2-*` -> Task 2)
2. Find all sub-tasks (e.g., Task 2.1, 2.2, 2.3)
3. Check which sub-tasks are referenced in commits
4. Report missing sub-tasks

**If tasks incomplete**, STOP and show status:
```
Task 2 INCOMPLETE: 1/3 sub-tasks missing
- Task 2.1: done
- Task 2.2: done
- Task 2.3: MISSING
```

Ask user whether to complete missing tasks or proceed anyway.

### 5. Run tests

Run the project test suite. Tests **MUST** pass before creating PR.

### 6. Determine PR type and generate title

| Branch flow | Title prefix |
|-------------|-------------|
| feature/* -> develop | `feat(scope):` |
| fix/* -> develop | `fix(scope):` |
| hotfix/* -> main | `hotfix(scope):` |
| develop -> main | `release:` |
| refactor/* -> develop | `refactor(scope):` |
| chore/* -> develop | `chore(scope):` |
| ci/* -> develop | `ci(scope):` |
| docs/* -> develop | `docs(scope):` |

**Title format**: `<type>(<scope>): <description>`
- Type: dominant commit type from analysis (feat > fix > refactor > ci > chore)
- Scope: most common scope from commits (kebab-case)
- Description: imperative, lowercase, no period, max 50 chars

**Breaking changes**: if any commit contains `BREAKING CHANGE:` or `!` after type:
- Add `breaking` label if it exists in the project
- Include a `## Breaking changes` section in the PR body

### 7. Generate PR body

Use the appropriate template from `references/pr_templates.md` based on PR type and populate with gathered data.

### 8. Suggest labels

**ALWAYS check available labels first:**

```bash
gh label list
```

Match commit types to available project labels. The project may use different names than standard (e.g., "feature" instead of "enhancement").

| Commit type | Common label names |
|-------------|-------------------|
| feat | feature, enhancement |
| fix | bug, bugfix |
| refactor | refactoring, tech-debt |
| docs | documentation |
| ci | ci/cd, infrastructure |
| security | security |
| hotfix | urgent, priority:high |

**If no matching label exists**: suggest creating one. The user may have removed default labels, so offering to add relevant ones is appropriate.

### 9. Determine milestone

Check for open milestones:

```bash
gh api repos/$(gh repo view --json nameWithOwner -q '.nameWithOwner')/milestones \
  --jq '.[] | select(.state == "open") | "\(.number): \(.title)"'
```

- If one active milestone exists: assign the PR to it (all work in progress belongs to the next release)
- If multiple milestones exist: ask the user which one applies
- If no milestones exist: skip (do not create one automatically)

### 10. Create PR

**ALWAYS show title, body, labels, and milestone for user approval first.**

```bash
gh pr create \
  --title "[title]" \
  --body "$(cat <<'EOF'
[body content]
EOF
)" \
  --base [base_branch] \
  --label "[label1]" --label "[label2]" \
  --milestone "[milestone-title]" \
  --reviewer "[username]"          # if teammates are known
```

Use `--draft` if the PR is not ready for merge review yet (work in progress,
awaiting CI, or created only to trigger AI bot review on the branch).

## Important rules

- **ALWAYS** confirm target branch with user
- **ALWAYS** run tests before creating PR
- **ALWAYS** show PR content for approval before creating
- **ALWAYS** check available labels with `gh label list` before suggesting
- **ALWAYS** use HEREDOC for body to preserve formatting
- **ALWAYS** add `--label` for each label separately (not comma-separated in one string)
- **ALWAYS** check for open milestones and assign if one is active
- **NEVER** create PR without user confirmation
- **NEVER** modify repository files (read-only analysis)
- **NEVER** create a milestone automatically - only assign existing ones
- Use `--draft` for PRs not ready for merge review
- Use `--reviewer` when teammates are known from team config or CODEOWNERS

## References

- `references/pr_templates.md` - PR body templates for all types (feature, release, bugfix, hotfix, refactoring, docs, CI/CD)
