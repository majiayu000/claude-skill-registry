---
name: commit-prepare
description: "Prepare git commit messages following conventional commits. Activates on: commit, prepare commit, commit this, commit message, ready to commit, stage and commit"
---

# Commit Preparation Skill

Automatically prepare commit messages following conventional commits standard.

## Activation

This skill activates on keywords:
- "commit", "prepare commit", "commit this"
- "commit message", "write commit"
- "stage and commit", "commit changes"
- "what should I commit", "ready to commit"

## Workflow

When activated, follow these steps:

### 1. Gather Context

Run these commands to understand what's being committed:

```bash
# See all changes
git status

# Staged changes (what will be committed)
git diff --cached --stat
git diff --cached

# Unstaged changes (won't be committed yet)
git diff --stat
```

### 2. Analyze Changes

Determine:
- **Type**: feat, fix, docs, refactor, test, chore, perf, ci
- **Scope**: Which component/module is affected (optional)
- **Breaking**: Are there breaking changes?
- **What**: What was changed
- **Why**: Why was it changed (if not obvious)

### 3. Generate Commit Message

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type Reference

| Type | When to Use | Example |
|------|-------------|---------|
| `feat` | New feature | `feat: add user authentication` |
| `fix` | Bug fix | `fix: resolve null pointer in parser` |
| `docs` | Documentation only | `docs: update API reference` |
| `refactor` | Code restructuring | `refactor: extract validation logic` |
| `test` | Adding/fixing tests | `test: add unit tests for auth` |
| `perf` | Performance improvement | `perf: optimize database queries` |
| `chore` | Maintenance, deps | `chore: update dependencies` |
| `ci` | CI/CD changes | `ci: add caching to workflow` |
| `style` | Formatting only | `style: fix indentation` |

#### Rules

- **Subject**: Imperative mood ("add" not "added"), no period, max 50 chars
- **Body**: Wrap at 72 chars, explain what and why (not how)
- **Footer**: Breaking changes, issue references

### 4. Handle Staging

If there are unstaged changes, ask:
- "Stage all changes?" (`git add .`)
- "Stage specific files?" (list them)
- "Review changes first?" (show diff)

### 5. Execute Commit

After user confirms the message:

```bash
git add <files>
git commit -m "<message>"
```

**Important**: Always use HEREDOC for multi-line commits:

```bash
git commit -m "$(cat <<'EOF'
feat: add user authentication

Implement OAuth2 flow with Google and GitHub providers.
Includes session management with secure cookies.

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### 6. Post-Commit

After successful commit:
- Show `git log -1` to confirm
- Suggest `git push` if ready
- Mention if more changes remain unstaged

## Example Interactions

### Simple Commit

**User**: "commit these changes"

**Claude**:
```bash
git status
git diff --cached
```

Looking at your staged changes:
- Modified `src/auth/oauth.py` - added token refresh logic
- Modified `tests/test_auth.py` - added refresh tests

**Suggested commit**:
```
feat(auth): add OAuth token refresh

Implement automatic token refresh when access token expires.
Includes retry logic with exponential backoff.
```

Shall I commit with this message?

---

### Breaking Change

**User**: "ready to commit"

**Claude**: I see you've changed the API response format. This is a breaking change.

**Suggested commit**:
```
feat(api)!: change response envelope format

BREAKING CHANGE: API responses now use { data, meta, errors }
envelope instead of flat response. Clients must update parsing.

Migration: Update response handlers to access .data property.
```

This marks it as a breaking change with `!`. Proceed?

---

### Multiple Logical Changes

**User**: "commit this"

**Claude**: I see changes to multiple unrelated areas:
1. Bug fix in `parser.py`
2. New feature in `export.py`
3. Updated docs

Recommend splitting into separate commits:
1. `fix(parser): handle empty input gracefully`
2. `feat(export): add CSV export option`
3. `docs: update export documentation`

Want me to help stage and commit each separately?

## Attribution

Always include Claude attribution for AI-assisted commits:

```
🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Safety Rules

- **Never** use `git commit --amend` on pushed commits
- **Never** skip hooks with `--no-verify` unless explicitly asked
- **Always** show the commit message before executing
- **Check** for secrets/credentials in staged files
- **Warn** about large binary files
