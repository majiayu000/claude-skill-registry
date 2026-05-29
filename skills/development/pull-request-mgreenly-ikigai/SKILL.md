---
name: pull-request
description: Creating pull requests with concise descriptions
---

# Pull Request

## Creating PRs

**This is a jj repository.** The `gh pr create` command requires a git repository and will fail. Use `gh api` instead to create PRs via the GitHub API.

No test plan section - CI runs the full quality suite automatically.

## Template

```markdown
<concise description of what changed and why>

---
🤖 Generated with [Claude Code](https://claude.ai/code)
```

## Command

```bash
gh api repos/mgreenly/ikigai/pulls \
  --method POST \
  --field title="<title>" \
  --field head="<branch-name>" \
  --field base="main" \
  --field body="$(cat <<'EOF'
<description>

---
🤖 Generated with [Claude Code](https://claude.ai/code)
EOF
)"
```

**Parameters:**
- `title`: PR title (imperative mood, concise)
- `head`: Source branch name (e.g., `rel-08-a`)
- `base`: Target branch (usually `main`)
- `body`: PR description

## Guidelines

- **Title:** Imperative mood, concise (e.g., "Add user authentication", "Fix memory leak in parser")
- **Description:** One line or short paragraph explaining what and why
- **No headers:** They add noise for typical PRs
- **No test plan:** Implicit - CI runs quality checks
- **Footer:** Attribution preserved

## Examples

**Simple change:**
```
Remove dead code: ik_content_block_thinking

---
🤖 Generated with [Claude Code](https://claude.ai/code)
```

**Feature addition:**
```
Add JSON export for metrics data

Enables users to export their usage metrics in JSON format
for integration with external tools.

---
🤖 Generated with [Claude Code](https://claude.ai/code)
```

**Bug fix:**
```
Fix null pointer dereference in config parser

The parser didn't handle missing optional fields correctly
when the config file used the legacy format.

---
🤖 Generated with [Claude Code](https://claude.ai/code)
```
