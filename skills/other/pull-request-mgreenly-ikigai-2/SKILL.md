---
name: pull-request
description: Creating pull requests with concise descriptions
---

# Pull Request

## Creating PRs

**This is a jj repository.** Use `gh pr create --repo` to create PRs without needing a git repository.

No test plan section - CI runs the full quality suite automatically.

## Template

```markdown
<concise description of what changed and why>

🤖 Generated with Ralph harness
```

## Command

```bash
gh pr create \
  --repo mgreenly/ikigai \
  --base main \
  --head <bookmark-name> \
  --title "<title>" \
  --body "$(cat <<'EOF'
<description>

🤖 Generated with Ralph harness
EOF
)"
```

**Parameters:**
- `--repo`: Repository in owner/repo format (required for jj repos)
- `--base`: Target branch (usually `main`)
- `--head`: Source bookmark name (e.g., `rel-09-rc5`)
- `--title`: PR title (imperative mood, concise)
- `--body`: PR description

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

🤖 Generated with Ralph harness
```

**Feature addition:**
```
Add JSON export for metrics data

Enables users to export their usage metrics in JSON format
for integration with external tools.

🤖 Generated with Ralph harness
```

**Bug fix:**
```
Fix null pointer dereference in config parser

The parser didn't handle missing optional fields correctly
when the config file used the legacy format.

🤖 Generated with Ralph harness
```
