---
name: pr-operations
description: Pull request lifecycle procedures including create, CI check, merge, and review.
---

# PR Operations Skill

Pull request lifecycle procedures including create, CI check, merge, and review.

## When Used

| Agent    | Phase       |
| -------- | ----------- |
| pr-agent | All actions |

## CLI Tools

All operations use GitHub CLI (`gh`):

```bash
# Verify gh CLI is authenticated
gh auth status

# If not authenticated, run:
gh auth login
```

### gh CLI Command Reference

| Operation            | Command                                                       |
| -------------------- | ------------------------------------------------------------- |
| List PRs             | `gh pr list`                                                  |
| View PR              | `gh pr view <number>`                                         |
| Create PR            | `gh pr create --title "..." --body "..."`                     |
| Merge PR             | `gh pr merge <number> --squash --delete-branch`               |
| Review PR            | `gh pr review <number> --approve/--comment/--request-changes` |
| Check CI             | `gh pr checks <number>`                                       |
| PR Diff              | `gh pr diff <number>`                                         |
| Close PR             | `gh pr close <number>`                                        |
| View PR comments     | `gh api repos/{owner}/{repo}/pulls/<number>/comments`         |
| View review comments | `gh api repos/{owner}/{repo}/pulls/<number>/reviews`          |
| View issue comments  | `gh pr view <number> --comments`                              |

**Note:** For `{owner}/{repo}`, use: `gh repo view --json owner,name -q '"\(.owner.login)/\(.name)"'`

### Viewing PR Comments

```bash
# View conversation/issue-style comments on PR
gh pr view <number> --comments

# View inline code review comments (requires API)
gh api repos/{owner}/{repo}/pulls/<number>/comments

# View reviews with their comments
gh api repos/{owner}/{repo}/pulls/<number>/reviews

# Get owner/repo from current directory
gh repo view --json owner,name -q '"\(.owner.login)/\(.name)"'
```

**For Linear issue linking:** Include `Fixes LIN-123` in PR body to auto-link.

**Note:** The github MCP server has been replaced with `gh` CLI. All GitHub operations use Bash tool with gh commands.

## Procedures

### 1. Create PR

Create a pull request from current branch:

**Pre-requisites:**

```bash
# Ensure branch is pushed
git push -u origin <branch>

# Verify all checks pass locally
pnpm lint && pnpm typecheck && pnpm test:run
```

**Create PR:**

```bash
gh pr create --title "<type>: <description>" --body "$(cat <<'EOF'
## Summary

- <bullet point 1>
- <bullet point 2>

## Test Plan

- [ ] Unit tests pass
- [ ] Type checks pass
- [ ] Manual testing completed

🤖 Generated with Claude Code
EOF
)"
```

**With Linear issue linking:**

```bash
gh pr create --title "<type>: <description>" --body "$(cat <<'EOF'
## Summary

- <bullet points>

Fixes LIN-123

## Test Plan

- [ ] Tests pass

🤖 Generated with Claude Code
EOF
)"
```

---

### 2. Create Draft PR

Create a work-in-progress PR:

```bash
gh pr create --draft --title "WIP: <description>" --body "$(cat <<'EOF'
## Summary

Work in progress - not ready for review.

## TODO

- [ ] Item 1
- [ ] Item 2

🤖 Generated with Claude Code
EOF
)"
```

---

### 3. Check CI Status

Monitor CI/CD pipeline:

```bash
# Get PR number
gh pr view --json number -q .number

# Check status
gh pr checks <number>
```

**Poll until complete:**

```bash
# Wait for checks to complete
gh pr checks <number> --watch
```

**Interpret results:**

| Status  | Meaning                   | Action         |
| ------- | ------------------------- | -------------- |
| pass    | All checks passed         | Ready to merge |
| fail    | One or more checks failed | Fix and push   |
| pending | Checks still running      | Wait           |

---

### 4. Merge PR

Merge after CI passes:

**Squash merge (default, recommended):**

```bash
gh pr merge <number> --squash --delete-branch
```

**Merge commit:**

```bash
gh pr merge <number> --merge --delete-branch
```

**Rebase merge:**

```bash
gh pr merge <number> --rebase --delete-branch
```

**Post-merge cleanup:**

```bash
git checkout main
git pull origin main
```

---

### 5. Review PR

Analyze a PR for review:

**Get PR info:**

```bash
gh pr view <number>
gh pr diff <number>
gh pr view <number> --json files,additions,deletions
```

**Review checklist:**

1. **Code quality**
   - Functions < 30 lines
   - No deep nesting
   - Clear naming

2. **Security**
   - No hardcoded secrets
   - Input validation
   - No console.log

3. **Testing**
   - Tests for new code
   - Tests pass
   - Coverage adequate

4. **Patterns**
   - Follows project conventions
   - Uses established patterns
   - No unnecessary abstraction

**Submit review:**

```bash
# Approve
gh pr review <number> --approve --body "LGTM"

# Request changes
gh pr review <number> --request-changes --body "Please address:
- Issue 1
- Issue 2"

# Comment only
gh pr review <number> --comment --body "Suggestions:
- Consider X"
```

---

### 6. Update PR

Add commits to an existing PR:

```bash
# Make changes
git add <files>
git commit -m "fix: address review feedback"
git push
```

**Force push after rebase:**

```bash
git rebase origin/main
git push --force-with-lease
```

---

### 7. Close PR

Close without merging:

```bash
gh pr close <number>
```

**With deletion of branch:**

```bash
gh pr close <number> --delete-branch
```

## Error Handling

| Error          | How to Handle                             |
| -------------- | ----------------------------------------- |
| CI failing     | Check logs: `gh pr checks <n> --web`      |
| Merge conflict | Rebase and resolve: `git rebase main`     |
| Not pushed     | Push first: `git push -u origin <branch>` |
| No permission  | Request access or ask maintainer          |
| Draft PR       | Mark ready: `gh pr ready <number>`        |

## Output

### PR Created

```markdown
## PR Created

**URL:** https://github.com/owner/repo/pull/123

**Title:** feat: add prompt manager CRUD

**Status:** Ready for review

**Next Steps:**

1. Wait for CI to pass
2. Request review if needed
3. Address feedback
4. Merge when approved
```

### PR Merged

```markdown
## PR Merged

**PR:** #123 - feat: add prompt manager CRUD

**Merge Type:** Squash

**Branch Deleted:** Yes

**Local Cleanup:**

- Switched to main
- Pulled latest changes
```

### PR Review

```markdown
## PR Review: #123

**Verdict:** APPROVE / REQUEST_CHANGES / COMMENT

**Summary:**

- <finding 1>
- <finding 2>

**Issues Found:**

1. [CRITICAL] <issue>
2. [SUGGESTION] <suggestion>

**Recommendation:** <action>
```
