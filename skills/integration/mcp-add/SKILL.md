---
name: mcp-add
description: Install an MCP server template from dotforge into a project or global Claude Code config with a single command.
---

# MCP Add

Install a dotforge MCP server template into the current project's or global Claude Code configuration.

## Input parsing

From `$ARGUMENTS` (format: `mcp add <server> [--global]`):
- Extract `<server>`: the word after `mcp add` — one of `github`, `postgres`, `supabase`, `redis`, `slack`
- Detect `--global` flag: if present, target `~/.claude/settings.json`; otherwise target `.claude/settings.json`

## Step 0: Validate

1. Verify the server template exists: `$DOTFORGE_DIR/mcp/<server>/`
   - If directory not found:
     ```
     ✗ Unknown server '{{server}}'.
     Available: github, postgres, supabase, redis, slack
     Usage: /forge mcp add <server> [--global]
     ```
     Stop.

2. Determine target settings path:
   - `--global` → `~/.claude/settings.json`
   - default → `.claude/settings.json`
   - If target doesn't exist and not `--global`: warn "No settings.json found. Run `/forge bootstrap` first, or use `--global` to install globally." Stop.
   - If target doesn't exist and `--global`: create `~/.claude/settings.json` with `{"permissions": {"allow": [], "deny": []}, "mcpServers": {}}`.

## Step 1: Load template files

Read all three template files:
- `$DOTFORGE_DIR/mcp/<server>/config.json`
- `$DOTFORGE_DIR/mcp/<server>/permissions.json`
- `$DOTFORGE_DIR/mcp/<server>/rules.md`

From `config.json`:
- **Server key**: the non-metadata top-level key (e.g., `"github"`, `"postgres"`)
- **Server config block**: the value of that key (the object with `type`, `command`, `args`, `env`)
- **Install note**: the `_install` string — contains required env vars and instructions
- Ignore all keys starting with `_` (metadata)

From `permissions.json`:
- **allow**: the `allow` array value (or `[]` if absent)
- **deny**: the `deny` array value (or `[]` if absent)
- Ignore all keys starting with `_`

## Step 2: Check for existing configuration

Read the target `settings.json`.

Check if the server is already configured:
- Present if `mcpServers.<server>` key exists in settings, OR
- Present if any of the server's allow entries appear in `permissions.allow`

If already configured:
```
⚠  {{server}} MCP is already configured in {{target}}.

   Options:
   [u] Update — replace mcpServers.{{server}}, add missing permissions (does not remove existing ones)
   [q] Quit — make no changes

What would you like to do? [u/Q]
```
- `u` → continue with update flow (Step 3)
- `Q` or anything else → stop

## Step 3: Show preview

```
══════════════════════════════════════════
  MCP Add: {{SERVER}} → {{target path}}
══════════════════════════════════════════

mcpServers.{{server}}:
{{pretty-print the server config block, replacing env var values like "${GITHUB_TOKEN}"
with the literal placeholder strings — do not expand env vars}}

New permissions:
  allow (+{{N}} new): {{list entries not already in target settings}}
  deny  (+{{N}} new): {{list entries not already in target settings}}
  (Existing permissions are not modified)

Rules:
  $DOTFORGE_DIR/mcp/{{server}}/rules.md
  → {{rules destination}}

Required environment variables:
  {{_install text from config.json}}

Proceed? [Y/n]
```

If all permissions are already present, show "Permissions: no changes (already configured)".
If no new denies to add, omit that line.

## Step 4: Apply changes

Only proceed if user confirms (Y, y, Enter, or "yes").

### 4a. Merge mcpServers

Read target `settings.json` as JSON.
Set `settings["mcpServers"]["{{server}}"]` = the server config block.
If `mcpServers` key doesn't exist in settings, create it.

### 4b. Merge permissions

**Allow list:**
- For each entry in template `allow[]`: add to `settings.permissions.allow` only if not already present
- Never remove or reorder existing entries

**Deny list:**
- For each entry in template `deny[]`: add to `settings.permissions.deny` only if not already present
- Never remove or reorder existing entries

If `settings.permissions` doesn't exist, create it with `{"allow": [], "deny": []}`.

### 4c. Write settings.json

Write the modified settings.json with 2-space indentation. Preserve all other existing keys
(hooks, autoMemoryEnabled, env, etc.) exactly as they were.

### 4d. Copy rules.md

Determine rules destination:
- Project mode: `.claude/rules/mcp-{{server}}.md`
- Global mode: `~/.claude/rules/mcp-{{server}}.md`

Copy `$DOTFORGE_DIR/mcp/{{server}}/rules.md` to the destination.
If the file already exists: overwrite — it's a managed template file. Any project-specific
customizations should live in a separate rule file, not in `mcp-{{server}}.md`.

Create the destination directory if it doesn't exist.

## Step 5: Confirm result

```
✓ {{SERVER}} MCP configured

  Updated files:
    {{target settings.json}} — mcpServers.{{server}} added
    {{rules destination}} — behavior rules copied
    {{"+N permissions" if any were added, else "permissions: no changes"}}

  Next step:
    {{_install text from config.json}}
    Restart Claude Code to activate the MCP server.
```

If global install:
  Add: "Installed globally — active in all projects."

If project-only install:
  Add: "Installed in the current project. For global use: /forge mcp add {{server}} --global"
