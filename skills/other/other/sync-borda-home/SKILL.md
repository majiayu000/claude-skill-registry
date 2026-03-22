---
name: sync
description: Drift-detect and sync git-tracked .claude/ and .codex/ config from project to home. Default shows what would change; "apply" performs the sync.
argument-hint: '[apply]'
allowed-tools: Read, Bash
---

<objective>

Sync git-tracked files from project `.claude/` and `.codex/` to their home equivalents (`~/.claude/` and `~/.codex/`). Uses `rsync` driven by `git ls-files` as the file manifest — only git-tracked files are ever synced; runtime state, secrets, and temp files are excluded automatically.

Project always wins: files in home that have no counterpart in the project are left untouched. No deletion, ever.

</objective>

<inputs>

- **$ARGUMENTS**: optional
  - Omitted → dry-run: show what would change, no files written
  - `apply` → apply sync: rsync files and report outcome

</inputs>

<constants>

- PROJECT root: `$(git rev-parse --show-toplevel)`
- HOME_EXPANDED: `$(eval echo ~)`
- File manifest: `git ls-files .claude/` and `git ls-files .codex/` — git-tracked only; gitignored paths (state/, logs/, settings.local.json, auth.json) excluded automatically
- settings.json transform: replace `node .claude/hooks/` with `node $HOME/.claude/hooks/` (portable — avoids hardcoded usernames). Covers all hook entries — statusLine, task-log, and future additions.
- Never synced: `settings.local.json`, `.codex/auth.json` — not git-tracked, excluded automatically
- No `context: fork` — sync reads files from both project and home then writes decisions; forking would give the skill an isolated context with no access to the home directory state it needs to compare against

</constants>

<workflow>

## Step 1: Resolve paths

```bash
PROJECT="$(git rev-parse --show-toplevel)"
HOME_EXPANDED="$(eval echo ~)"
HOME_CLAUDE="$HOME_EXPANDED/.claude"
HOME_CODEX="$HOME_EXPANDED/.codex"
```

## Step 2: Dry-run — show what would change

Each bash block must be self-contained (redeclare variables at the top). Do not rely on variables from a previous tool call.

**`.claude/` files** (excluding `settings.json`):

```bash
PROJECT="$(git rev-parse --show-toplevel)"
HOME_EXPANDED="$(eval echo ~)"
HOME_CLAUDE="$HOME_EXPANDED/.claude"
cd "$PROJECT" && git ls-files .claude/ \
  | grep -vE 'settings\.json$|settings\.local\.json$' \
  | sed 's|^\.claude/||' \
  | rsync -av --dry-run --files-from=- "$PROJECT/.claude/" "$HOME_CLAUDE/"
```

rsync prints only files that would change; identical files are silently skipped.

**`settings.json`** — transform then compare (self-contained):

```bash
PROJECT="$(git rev-parse --show-toplevel)"
HOME_EXPANDED="$(eval echo ~)"
HOME_CLAUDE="$HOME_EXPANDED/.claude"
SETTINGS_TMP="$(mktemp /tmp/settings_sync_XXXXXX.json)"
sed 's|node \.claude/hooks/|node $HOME/.claude/hooks/|g' \
  "$PROJECT/.claude/settings.json" > "$SETTINGS_TMP"
CHANGED=$(rsync --checksum --itemize-changes --dry-run \
  "$SETTINGS_TMP" "$HOME_CLAUDE/settings.json" 2>&1)
if [ -z "$CHANGED" ]; then
  echo "✓ IDENTICAL settings.json"
else
  echo "DIFFERS — semantic summary:"
  # Permissions added (in project, not in home)
  comm -23 \
    <(jq -r '.permissions.allow[]' "$SETTINGS_TMP" | sort) \
    <(jq -r '.permissions.allow[]' "$HOME_CLAUDE/settings.json" | sort) \
    | sed 's/^/  + /'
  # Permissions removed (in home, not in project)
  comm -13 \
    <(jq -r '.permissions.allow[]' "$SETTINGS_TMP" | sort) \
    <(jq -r '.permissions.allow[]' "$HOME_CLAUDE/settings.json" | sort) \
    | sed 's/^/  - /'
  # Hook matcher changes
  diff \
    <(jq -r '.hooks // {} | to_entries[] | "\(.key): \(.value[].matcher // "")"' "$SETTINGS_TMP" 2>/dev/null | sort) \
    <(jq -r '.hooks // {} | to_entries[] | "\(.key): \(.value[].matcher // "")"' "$HOME_CLAUDE/settings.json" 2>/dev/null | sort) \
    | grep '^[<>]' | sed 's/^< /  project: /' | sed 's/^> /  home:    /'
fi
rm -f "$SETTINGS_TMP"
```

**`.codex/` files**:

```bash
PROJECT="$(git rev-parse --show-toplevel)"
HOME_EXPANDED="$(eval echo ~)"
HOME_CODEX="$HOME_EXPANDED/.codex"
cd "$PROJECT" && git ls-files .codex/ \
  | sed 's|^\.codex/||' \
  | rsync -av --dry-run --files-from=- "$PROJECT/.codex/" "$HOME_CODEX/"
```

If `$ARGUMENTS` is empty: print the combined dry-run output and offer `/sync apply`. Stop here.

**Bash fallback**: if the Bash tool is denied or unavailable, fall back to using the Read tool to compare files manually. For each git-tracked file in `.claude/`, read both the project copy and the home copy (`~/.claude/<path>`), compare their contents, and report `✓ IDENTICAL` or `⚠ DIFFERS` for each. For `settings.json`, apply the `node .claude/hooks/` → absolute path substitution mentally before comparing. Note that without Bash, rsync cannot transfer files — report only what would change and ask the user to run `/sync apply` in a context where Bash is available.

## Step 3: Apply (only when $ARGUMENTS == "apply")

Each bash block must be self-contained (redeclare variables at the top).

**`.claude/` files** (excluding `settings.json`):

```bash
PROJECT="$(git rev-parse --show-toplevel)"
HOME_EXPANDED="$(eval echo ~)"
HOME_CLAUDE="$HOME_EXPANDED/.claude"
cd "$PROJECT" && git ls-files .claude/ \
  | grep -vE 'settings\.json$|settings\.local\.json$' \
  | sed 's|^\.claude/||' \
  | rsync -av --files-from=- "$PROJECT/.claude/" "$HOME_CLAUDE/"
```

**`settings.json`** — transform and apply (self-contained, content-based comparison):

```bash
PROJECT="$(git rev-parse --show-toplevel)"
HOME_EXPANDED="$(eval echo ~)"
HOME_CLAUDE="$HOME_EXPANDED/.claude"
SETTINGS_TMP="$(mktemp /tmp/settings_sync_XXXXXX.json)"
sed 's|node \.claude/hooks/|node $HOME/.claude/hooks/|g' \
  "$PROJECT/.claude/settings.json" > "$SETTINGS_TMP"
CHANGED=$(rsync --checksum --itemize-changes \
  "$SETTINGS_TMP" "$HOME_CLAUDE/settings.json" 2>&1)
rm -f "$SETTINGS_TMP"
if [ -n "$CHANGED" ]; then
  echo "merged   settings.json"
else
  echo "✓ unchanged settings.json"
fi
```

`rsync --checksum` compares file content (not mtime), so it transfers only when content actually differs.

**`.codex/` files**:

```bash
PROJECT="$(git rev-parse --show-toplevel)"
HOME_EXPANDED="$(eval echo ~)"
HOME_CODEX="$HOME_EXPANDED/.codex"
cd "$PROJECT" && git ls-files .codex/ \
  | sed 's|^\.codex/||' \
  | rsync -av --files-from=- "$PROJECT/.codex/" "$HOME_CODEX/"
```

## Step 4: Verify and report outcome (apply mode only)

```bash
PROJECT="$(git rev-parse --show-toplevel)"
HOME_EXPANDED="$(eval echo ~)"
# JSON validity
jq empty "$HOME_EXPANDED/.claude/settings.json" && echo "settings.json: valid"

# Counts
echo ".claude files: $(cd "$PROJECT" && git ls-files .claude/ | wc -l | tr -d ' ')"
echo ".codex files:  $(cd "$PROJECT" && git ls-files .codex/  | wc -l | tr -d ' ')"
```

```
## Sync Outcome — <date>

| Target          | Result             |
|-----------------|--------------------|
| .claude/ files  | N transferred      |
| settings.json   | merged / unchanged |
| .codex/ files   | N transferred      |
| JSON validity   | valid              |
```

</workflow>

<notes>

- File manifest from `git ls-files` — adding a new agent, skill, hook, or codex agent to git automatically includes it in future syncs; no skill edits needed
- `settings.local.json` and `.codex/auth.json` are never synced — gitignored, excluded automatically
- All `node .claude/hooks/` paths in settings.json are rewritten to `node $HOME/.claude/hooks/` — avoids hardcoded usernames; `$HOME` is expanded by the shell when hooks fire
- Project owns what it tracks; home-only files are never touched or deleted
- rsync skips identical files — only changed files are transferred, making repeated runs cheap
- Run `/sync` (dry-run) first, then `/sync apply` once the report looks correct
- Follow-up: after `/sync apply`, run `/audit` to confirm the propagated config is structurally sound

</notes>
