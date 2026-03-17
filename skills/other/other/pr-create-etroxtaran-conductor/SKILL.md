---
name: pr-create
description: Create GitHub pull requests with comprehensive descriptions and proper review setup
version: 1.1.0
tags: [git, github, pr, collaboration]
owner: orchestration
status: active
---

# PR Create Skill

## Overview

Create consistent, review-ready pull requests with required metadata and checks.

## Usage

```
/pr-create
```

## Identity
**Role**: Pull Request Author
**Objective**: Create well-structured GitHub pull requests that facilitate efficient code review and merge.

## Prerequisites Check

Before creating a PR, verify:
1. All changes are committed (no uncommitted changes)
2. **Remote uses SSH** (never HTTPS)
3. Branch is pushed to remote
4. Branch is up-to-date with base branch
5. CI checks pass locally (if applicable)

```bash
# Run these checks
git status
git fetch origin
git log origin/main..HEAD --oneline

# CRITICAL: Verify SSH remote (not HTTPS)
git remote -v
# Must show: git@github.com:owner/repo.git
# NOT: https://github.com/owner/repo.git

# If HTTPS detected, convert to SSH:
git remote set-url origin git@github.com:OWNER/REPO.git
```

## PR Structure

### Title Format
```
<type>(<scope>): <short description>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

Examples:
- `feat(auth): add OAuth2 login support`
- `fix(api): handle null response from payment gateway`
- `refactor(db): migrate to connection pooling`

### Description Template

```markdown
## Summary
<!-- 1-3 bullet points describing WHAT changed -->
- Added OAuth2 authentication flow
- Integrated with Google and GitHub providers
- Updated user model to store provider info

## Motivation
<!-- WHY this change is needed -->
Enables social login to reduce friction in user onboarding.
Addresses user feedback requesting Google login (Issue #234).

## Changes
<!-- Technical details of HOW -->
- Added `src/auth/oauth.ts` - OAuth2 client wrapper
- Modified `src/models/user.ts` - Added `provider` field
- Updated `src/routes/auth.ts` - New `/auth/oauth/*` endpoints

## Testing
<!-- How this was tested -->
- [ ] Unit tests added for OAuth client
- [ ] Integration tests for OAuth flow
- [ ] Manual testing with Google and GitHub

## Screenshots
<!-- If UI changes, add before/after screenshots -->

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or migration guide provided)

## Related Issues
Closes #234
Related to #189
```

## Best Practices

### PR Size Guidelines
- **Optimal**: 200-400 lines changed
- **Maximum**: 500 lines (split larger changes)
- **Exception**: Generated files, migrations, large refactors (document in description)

### Review Optimization
1. **Self-review first**: Review your own PR before requesting others
2. **Add context**: Use PR comments to explain non-obvious decisions
3. **Highlight risks**: Call out areas needing careful review
4. **Link related**: Reference issues, docs, design decisions

### Draft PRs
Use draft PRs for:
- Work in progress needing early feedback
- Experimental approaches for discussion
- Breaking changes requiring team alignment

```bash
gh pr create --draft --title "WIP: new feature" --body "..."
```

## Workflow

### Step 1: Analyze Changes
```bash
# See what will be in the PR
git log origin/main..HEAD --oneline
git diff origin/main --stat
```

### Step 2: Generate PR Content
1. Identify the type and scope from commits
2. Write summary from commit messages
3. Add motivation (why) and technical details (how)
4. List testing done
5. Add relevant labels

### Step 3: Create PR
```bash
gh pr create \
  --title "<type>(<scope>): <description>" \
  --body "$(cat <<'EOF'
## Summary
...

## Test plan
...

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)" \
  --reviewer "@team/backend" \
  --label "enhancement"
```

### Step 4: Post-Creation
1. Link related issues
2. Add to project board if applicable
3. Request specific reviewers for specialized areas
4. Set milestone if release-bound

## CODEOWNERS Integration

If the repo has `.github/CODEOWNERS`:
- Reviewers are auto-assigned based on paths changed
- Ensure all required reviewers are notified
- Check if approval from code owners is required

## Error Handling

| Error | Solution |
|-------|----------|
| "Branch has no commits ahead" | Ensure you're on feature branch with changes |
| "Remote branch doesn't exist" | Push branch first: `git push -u origin HEAD` |
| "Base branch out of date" | Rebase: `git rebase origin/main` |
| "Merge conflicts" | Resolve conflicts before creating PR |
| "Required status check failing" | Fix CI issues before requesting review |

## Anti-Patterns

**DO NOT**:
- Create PRs without descriptions
- Include unrelated changes (scope creep)
- Force push after review started (unless requested)
- Merge without required approvals
- Leave PR stale for more than 3 days

## Outputs

- A created pull request with standardized title and description.

## Related Skills

- `/git-committer-atomic` - Prepare atomic commits
- `/git-commit-conventional` - Standardize commit messages
