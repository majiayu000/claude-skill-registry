---
description: Configures Claude Code permissions for safe agent autonomy. Creates settings.json with allow/deny rules and a path-restriction hook.
disable-model-invocation: true
---

# Optimus Permissions

Configure safe permission rules and a path-restriction hook so Claude Code agents can work autonomously inside the project without constant permission prompts, while blocking destructive operations outside the project.

## Security Model

| Operation | Inside Project | Outside Project |
|-----------|---------------|-----------------|
| Read/Search | Allow | Allow |
| Write/Edit | Allow | Ask user |
| Write/Edit precious unversioned file | **Ask user** | Ask user |
| Delete (rm/rmdir) | Allow | **BLOCKED** |
| Delete precious unversioned file | **BLOCKED** | **BLOCKED** |
| Git on feature branch | Allow | — |
| Git on protected branch | **BLOCKED** | — |

## Step 1: Detect Existing Configuration

1. Check if `.claude/settings.json` exists. If so, read its full content — it will be preserved during merge.
2. Check if `.claude/hooks/restrict-paths.sh` (or `restrict-paths.*`) already exists. Note whether this is a fresh install or an update — report this to the user in Step 5.
3. Check if `.mcp.json` exists at the project root. If so, extract all MCP server names (top-level keys) for Step 4.

Print a brief detection summary to the user: what exists, what will be created/updated.

## Step 2: Create Directory Structure

```bash
mkdir -p .claude/hooks
```

## Step 3: Install Path-Restriction Hook

Copy the hook template to the project (overwrites any existing version):
- Source: `$CLAUDE_PLUGIN_ROOT/skills/permissions/templates/hooks/restrict-paths.sh`
- Destination: `.claude/hooks/restrict-paths.sh`

Copy the file contents exactly — do not modify the template.

## Step 4: Create or Update settings.json

Use the template from `$CLAUDE_PLUGIN_ROOT/skills/permissions/templates/settings.json` as the base configuration.

### If `.claude/settings.json` does NOT exist

Create it from the template. If `.mcp.json` was found in Step 1, add `mcp__<server-name>` entries to the `permissions.allow` list for each server.

### If `.claude/settings.json` already exists

**Merge** the template into the existing file:

1. **permissions.allow** — add any entries from the template that are not already present. If `.mcp.json` was found, also add `mcp__<server-name>` entries. Never remove existing entries.
2. **permissions.deny** — add any entries from the template that are not already present. Then check for **extra git deny patterns**: collect all deny entries containing the word `git` (as a command, not as part of words like `github`) from both the existing settings and the template. If the existing settings have git deny entries not present in the template, list them and use `AskUserQuestion` — header "Git patterns", question "Your settings have extra git deny patterns that may block feature-branch workflow (commit/push) needed by /optimus:tdd: [list patterns]. Replace with the template's set?":
   - **Replace with template set (Recommended)** — "Remove extra git deny patterns, keep the template's. Branch protection is still enforced by the hook."
   - **Keep all** — "Preserve existing patterns. Skills that need git commit/push may not work."

   If **Replace**: remove all existing git deny entries, add the template's git deny set. Non-git deny entries are untouched. If **Keep all**: no changes.
3. **hooks.PreToolUse** — add the hook entry from the template. If a PreToolUse array already exists, append to it (avoid duplicates if an entry already references `restrict-paths.sh`).
4. **Preserve everything else** — existing `hooks.PostToolUse`, custom sections, and any other configuration must remain untouched.

### Merge principles

- Never remove existing allow/deny entries or hooks — except git deny patterns, which are reconciled with the user when existing patterns go beyond the template (see step 2 above)
- Never overwrite the file — read, merge, write
- The result must be valid JSON

## Step 5: Verify and Report

Run through this checklist. Fix any issues before reporting.

1. `.claude/hooks/restrict-paths.sh` exists and contains the hook logic
2. `.claude/settings.json` exists and contains:
   - `permissions.allow` with at least the 13 tool entries from the template
   - `permissions.deny` with at least the 30 deny patterns from the template
   - `hooks.PreToolUse` with an entry referencing `restrict-paths.sh`
3. If the file had existing PostToolUse hooks or other content, verify it is preserved

**Report to the user:**
- Files created or updated
- Number of tools in the allow list, number of deny patterns
- If MCP servers were detected, list them
- Brief security model reminder: writes outside project will prompt, deletes outside project are blocked, reads are unrestricted
- Trust model reminder: commands not on the deny list will execute without prompts inside the project (database operations, file deletions, network requests, etc.). See the skill's README for the full trust model
- Git branch protection is active — git operations (commit, push, rebase, reset, merge) are allowed on feature branches but blocked on protected branches (master, main, develop, dev, development, staging, stage, prod, production, release). Customize the `PROTECTED_BRANCHES` array in `.claude/hooks/restrict-paths.sh`
- Precious file protection is always active — the hook automatically protects well-known sensitive files (`.env`, `*.key`, `*.pem`, `*.sqlite`, etc.) that are not tracked by git

4. Scan for precious unversioned files in the project:
   ```bash
   find . -maxdepth 4 \( -name ".env" -o -name ".env.*" -o -name "local.settings.json" -o -name "credentials.*" -o -name "secrets.*" -o -name "docker-compose.override.yml" -o -name "appsettings.*.json" -o -name "*keyfile*.json" -o -name "newrelic.config" -o -name "*.key" -o -name "*.pem" -o -name "*.pfx" -o -name "*.p12" -o -name "*.cert" -o -name "*.crt" -o -name "*.jks" -o -name "*.sqlite" -o -name "*.sqlite3" -o -name "*.db" -o -name "*.db-shm" -o -name "*.db-wal" -o -name "*.db-journal" -o -name "*.mdf" -o -name "*.ldf" -o -name "*.ndf" -o -name "*.bak" -o -name "*.dump" -o -name "*.sql.gz" -o -name "*.suo" -o -name "*.user" \) -not -path "./.git/*" -not -path "*/node_modules/*" -not -path "*/obj/*" -not -path "*/bin/*" 2>/dev/null
   ```
   - If any are found and not git-tracked, report them as protected files
   - If the scan discovers unversioned files that look sensitive but do not match built-in patterns (e.g., custom config files like `config.local.yaml`), ask the user if they want to add custom patterns to the `is_precious()` function in `.claude/hooks/restrict-paths.sh`. **Note:** custom edits to this file will be replaced if the user re-runs `/optimus:permissions`. For persistent customizations, edit the template in the plugin source instead.

Recommend the next step based on project state:
- If `.claude/CLAUDE.md` does not exist → `/optimus:init` to set up coding guidelines and project structure
- If already initialized → `/optimus:unit-test` to establish test coverage, or `/optimus:tdd` to start developing with test-driven workflow

Tell the user: **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.
