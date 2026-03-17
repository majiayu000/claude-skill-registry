---
name: commit-helper
description: Generate clear, conventional commit messages from git diffs. Use when creating commits, reviewing staged changes, or writing commit messages.
allowed-tools: Bash, Read, Grep
---

# Commit Helper

**Version**: 1.0.0
**Purpose**: Generate Conventional Commits compliant messages

---

## Triggers

| Trigger | Examples |
|---------|----------|
| Commit | "commit this", "コミットして", "commit changes" |
| Message | "write commit message", "コミットメッセージ作成" |
| Stage | "what should I commit?", "変更内容は？" |

---

## Conventional Commits Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(auth): add OAuth login` |
| `fix` | Bug fix | `fix(api): handle null response` |
| `docs` | Documentation | `docs: update README` |
| `style` | Formatting | `style: fix indentation` |
| `refactor` | Code restructure | `refactor(utils): extract helper` |
| `perf` | Performance | `perf(query): add index` |
| `test` | Tests | `test(auth): add unit tests` |
| `chore` | Maintenance | `chore: update deps` |
| `ci` | CI/CD | `ci: add GitHub Action` |

---

## Workflow

### Step 1: Analyze Changes

```bash
# View staged changes
git diff --cached --stat
git diff --cached
```

### Step 2: Determine Type

- Adding new functionality? → `feat`
- Fixing a bug? → `fix`
- Updating docs? → `docs`
- Refactoring without behavior change? → `refactor`

### Step 3: Write Subject

```
✅ GOOD: feat(api): add user authentication endpoint
❌ BAD: updated stuff
❌ BAD: feat: Add User Authentication Endpoint (no caps after colon)
```

**Rules:**
- Imperative mood ("add" not "added")
- No period at end
- Max 50 characters
- Lowercase after colon

### Step 4: Write Body (optional)

```
feat(auth): add OAuth2.0 authentication

Implement OAuth2.0 flow with Google and GitHub providers.
This replaces the legacy session-based auth system.

- Add OAuth callback handlers
- Store refresh tokens securely
- Add logout functionality
```

### Step 5: Add Footer (optional)

```
BREAKING CHANGE: auth tokens now expire after 24h

Closes #123
Co-authored-by: Name <email>
```

---

## Examples

### Simple Fix

```bash
git commit -m "fix(parser): handle empty input gracefully"
```

### Feature with Body

```bash
git commit -m "$(cat <<'EOF'
feat(dashboard): add real-time metrics

- WebSocket connection for live updates
- Auto-refresh every 5 seconds
- Graceful fallback to polling

Closes #456
EOF
)"
```

### Breaking Change

```bash
git commit -m "$(cat <<'EOF'
feat(api)!: change response format to JSON:API

BREAKING CHANGE: API responses now follow JSON:API spec.
See migration guide: docs/migration-v2.md

Closes #789
EOF
)"
```

---

## Auto-Generated Footer

All commits include:

```
🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```
