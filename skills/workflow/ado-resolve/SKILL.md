---
name: ado-resolve
description: Use when committing, pushing, creating PR, and resolving Azure DevOps ticket in one workflow. Also use when creating a new ADO ticket. Triggers on "resolve ticket", "close ticket", "create ticket", "commit and PR", or ticket number mentions with resolution intent.
model: sonnet
---

# Resolve DevOps Ticket

Commit, push, create PR, create or update Azure DevOps ticket with PR link + test notes, resolve.

> **Read `~/.claude/skills/_ado-shared.md`** for auth, env vars, fetch/update ticket, write-payload, and Windows/MSYS2 patterns.

## Workflow

1. `git status` + `git diff` + `git log --oneline -5`
2. Commit with descriptive message + Co-Authored-By (skip if nothing to commit)
3. **Detect fork remote**: find remote pointing to `Vvanlaar/` (fallback: ask user)
4. **Detect upstream remote**: find remote pointing to `bluebillywig/` for `--repo` in PR creation
5. Push to fork remote
6. Create PR via `gh pr create` with `--repo bluebillywig/<repo> --head Vvanlaar:<branch>`
7. **Read existing test notes** from ticket before updating
8. Update ticket via ADO REST API (see shared for auth + write-payload pattern)
   - `System.State`: "Resolved"
   - `Microsoft.VSTS.Common.Resolution`: PR link (HTML)
   - `BB.Testnotes`: preserve existing + append new (HTML)

## Required Info

| Info | Source |
|------|--------|
| Ticket ID | User provides or from branch name (e.g. `17885-feature`) |
| Fork remote | Detect via `git remote -v \| grep -i vvanlaar` |
| Upstream remote | Detect via `git remote -v \| grep bluebillywig/` |
| Base branch | Usually `master` (NOT `main` — check with `git remote show <upstream>`) |
| Test notes | Derive from PR description or ask |

## Remote Detection

```bash
# Fork (for push)
git remote -v | grep -i 'vvanlaar/' | grep fetch | head -1 | awk '{print $1}'
# Upstream (for PR --repo)
git remote -v | grep 'bluebillywig/' | grep fetch | head -1 | awk '{print $1}'
```

If either not found, list remotes and ask user.

## Commit Format

```bash
git commit -m "$(cat <<'EOF'
<imperative summary>

Co-Authored-By: Claude <model> <noreply@anthropic.com>
EOF
)"
```

Note: `--no-verify` only when pre-commit hooks fail on pre-existing staged files unrelated to current changes. Otherwise omit it.

## PR Format

```bash
gh pr create --repo bluebillywig/<repo-name> --head Vvanlaar:<branch> --base master \
  --title "<title> #<ticketnr>" --body "$(cat <<'EOF'
## Summary
- <bullet points>

## Test plan
- <test steps>

Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**IMPORTANT**: Base branch is usually `master`, NOT `main`. Check tracking branch if unsure.

## CRITICAL: Ticket Number in PR Title

**Always** include ` #<ticketnr>` at end of PR title — e.g. `Show metadata toggle #18014`.

## ADO Ticket Update Payload

```json
[
  {"op":"replace","path":"/fields/System.State","value":"Resolved"},
  {"op":"replace","path":"/fields/Microsoft.VSTS.Common.Resolution","value":"<a href=\"PR_URL\">REPO #PR_N - PR title</a>"},
  {"op":"replace","path":"/fields/BB.Testnotes","value":"<existing HTML><ul><li>new step</li></ul>"}
]
```

Use write-payload pattern from shared (node + cygpath + curl PATCH).

### Create new ticket (POST instead of PATCH)

```bash
source ~/.env && B64=$(printf ':%s' "$ADO_PAT" | base64 -w0)
WINPATH=$(cygpath -w "$LOCALAPPDATA/Temp/ado-payload.json")
curl -s -H "Authorization: Basic $B64" -X POST -H "Content-Type: application/json-patch+json" \
  'https://dev.azure.com/bluebillywig/BBNew/_apis/wit/workitems/$Task?api-version=7.0' \
  -d @"$WINPATH"
```

New ticket payload uses `"op":"add"` for all fields. Always set `System.AreaPath` to `BBNew\Core`.

Resolution link text format: `REPO #PR_N - PR title` (uppercase repo name) — e.g. `OVP6 #6178 - Show metadata toggle`.

### Test notes format
- **Preserve existing** test notes (fetch ticket first, read `BB.Testnotes`)
- Append new steps after existing content
- Use `<ul><li>...</li></ul>` HTML format

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `--base main` | Default branch is `master` for bb repos |
| Push to wrong remote | Default to `vvanlaar`, verify with `git remote get-url` first |
| Missing test notes | Always include test steps |
| Overwriting existing test notes | Fetch ticket first, preserve existing `BB.Testnotes` |
| Wrong sprint path | Fetch current sprint dynamically (see shared), don't hardcode |
| `"op":"replace"` on create | New tickets need `"op":"add"` |
