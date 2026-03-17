---
name: ln-004-agent-config-sync
description: "Sync skills (symlinks) and MCP settings from Claude to Gemini CLI and Codex CLI"
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Agent Sync (Standalone Utility)

**Type:** Standalone Utility
**Category:** 0XX Shared

Synchronizes skills and MCP server configurations from Claude Code (source of truth) to Gemini CLI and Codex CLI. Creates symlinks for skills, copies/converts MCP settings.

---

## When to Use This Skill

- After adding/removing MCP servers in Claude Code settings
- After installing new plugins in Claude Code
- First-time setup of Gemini CLI or Codex CLI alongside Claude Code
- Periodic sync to keep all agents aligned

---

## Input Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| targets | No | both | `gemini`, `codex`, or `both` |
| mode | No | full | `skills` (symlinks only), `mcp` (MCP only), or `full` (both) |
| dry_run | No | false | Show planned actions without executing |

---

## Workflow

```
Detect OS → Discover Configs → Sync Skills → Sync MCP → Report
```

### Phase 0: OS Detection

| Check | Result | Impact |
|-------|--------|--------|
| `uname` or platform | win32 / darwin / linux | Junction vs symlink |
| Home directory | `$HOME` or `$USERPROFILE` | Config paths |

**Paths by OS:**

| Agent | Windows | macOS / Linux |
|-------|---------|---------------|
| **Claude** | `%USERPROFILE%\.claude.json` (primary) | `~/.claude.json` (primary) |
| **Claude** | `%USERPROFILE%\.claude\settings.json` (fallback) | `~/.claude/settings.json` (fallback) |
| **Gemini** | `%USERPROFILE%\.gemini\settings.json` | `~/.gemini/settings.json` |
| **Codex** | `%USERPROFILE%\.codex\config.toml` | `~/.codex/config.toml` |

### Phase 1: Discover Current State

1. **Read Claude settings (check both sources, merge):**
   - Parse `~/.claude.json` → extract `mcpServers` block (primary source, app state file)
   - Parse `~/.claude/settings.json` → extract `mcpServers` block (fallback, user settings file)
   - Merge: primary overrides fallback by server name
   - If no `mcpServers` in either → WARN "No MCP servers configured in Claude", skip MCP sync

2. **Read target configs (if exist):**
   - Gemini: Parse `~/.gemini/settings.json` → extract existing `mcpServers`
   - Codex: Parse `~/.codex/config.toml` → extract existing `[mcp_servers.*]`

3. **Detect installed plugins:**
   - Glob `~/.claude/plugins/*/plugin.json` → list plugin directories
   - Also check if skills repo itself is a plugin source

4. **Check existing symlinks:**
   - `~/.gemini/skills` → exists? points where?
   - `~/.codex/skills` → exists? points where?

5. **Show current state:**
   ```
   Current State:
   | Agent | Skills | MCP Servers | Config Exists |
   |-------|--------|-------------|---------------|
   | Claude (source) | 5 plugins | 4 servers | yes |
   | Gemini | no link | 2 servers | yes |
   | Codex | → ~/.claude/plugins | 4 servers | yes |
   ```

### Phase 2: Sync Skills (symlinks/junctions)

FOR EACH target IN (gemini, codex) WHERE target in targets:

1. **Determine link path:**
   - Gemini: `~/.gemini/skills`
   - Codex: `~/.codex/skills`

2. **Check if already linked correctly:**
   - IF link exists AND points to correct source → SKIP (already synced)
   - IF link exists AND points to wrong source → WARN, ask user before replacing
   - IF regular directory (not link) exists → WARN "Target is a real directory, not a link. Skip to avoid data loss."

3. **Determine source:**
   - IF single plugin: link directly to plugin dir
   - IF multiple plugins: ask user which plugin to share

4. **Create link:**

   | OS | Command |
   |----|---------|
   | Windows | `cmd /c mklink /J "{target_path}" "{source_path}"` |
   | macOS / Linux | `ln -s "{source_path}" "{target_path}"` |

5. **Verify:** Check link exists and resolves correctly

### Phase 3: Sync MCP Settings

**Source:** `~/.claude.json` (primary) + `~/.claude/settings.json` (fallback) → merged `mcpServers`

#### 3a: Claude → Gemini (JSON → JSON)

1. Read Claude `mcpServers` as JSON object
2. Read Gemini `settings.json` (or create `{}` if missing)
3. **Merge strategy:** Claude servers override Gemini servers by key name. Gemini-only servers preserved.
4. Write updated `settings.json`

**Conversion:** Transport type mapping required:

   | Claude field | Gemini field | Notes |
   |---|---|---|
   | `type: "http"` + `url` | `httpUrl` | Streamable HTTP |
   | `type: "sse"` + `url` | `url` | SSE transport |
   | `command` + `args` | `command` + `args` + `cwd` | stdio (same format) |
   | `env` | `env` | Same format (`$VAR_NAME` syntax in Gemini) |
   | `headers` | `headers` | Same format (JSON object, for `url`/`httpUrl`) |

   **Gemini-only fields (not mapped from Claude):**
   - `timeout` — request timeout in ms (default: 10min)
   - `trust` — bypass tool confirmations
   - `includeTools` / `excludeTools` — tool whitelist/blacklist

#### 3b: Claude → Codex (JSON → TOML)

1. Read Claude `mcpServers` as JSON object
2. Read Codex `config.toml` (or create empty if missing)
3. **Convert each server:**

   | Claude JSON field | Codex TOML field | Notes |
   |-------------------|------------------|-------|
   | `command` | `command` | Same |
   | `args` | `args` | JSON array → TOML array |
   | `env` | `[mcp_servers.{name}.env]` | Nested table |
   | `type: "http"` + `url` | `url` | Streamable HTTP (Codex auto-detects by `url` presence) |
   | `type: "sse"` + `url` | `url` | SSE → Streamable HTTP (same `url` field) |
   | `headers` | `http_headers` | **Different key name!** Static header values |

   **Example conversion:**
   ```json
   "context7": {
     "command": "npx",
     "args": ["-y", "@upstash/context7-mcp"]
   }
   ```
   ```toml
   [mcp_servers.context7]
   command = "npx"
   args = ["-y", "@upstash/context7-mcp"]
   ```

4. **Merge strategy:** Claude servers override. Codex-only servers preserved.
5. Write updated `config.toml`

**Codex-only fields (preserve as-is, no Claude equivalent):**
- `bearer_token_env_var` — Codex bearer token auth
- `enabled_tools` / `disabled_tools` — Codex tool filtering
- `startup_timeout_sec` / `tool_timeout_sec` — Codex timeouts
- `enabled` / `required` — Codex server lifecycle
- `env_vars` / `env_http_headers` — Codex env-based headers

### Phase 4: Report

```
Sync Complete:
| Action | Target | Status |
|--------|--------|--------|
| Skills symlink | Gemini | Created → ~/.claude/plugins/... |
| Skills symlink | Codex | Already linked |
| MCP sync | Gemini | 4 servers synced (2 new, 2 updated) |
| MCP sync | Codex | 4 servers synced (1 new, 3 updated) |
```

---

## Critical Rules

1. **Claude = source of truth.** Never write TO Claude settings. Read-only source.
2. **Non-destructive merge.** Target-only servers/settings preserved. Only Claude servers added/updated.
3. **No data loss.** If target is a real directory (not symlink) — warn and skip, never delete.
4. **Backup before write.** Before modifying any config file, create `.bak` copy.
5. **Dry run first.** If `dry_run=true`, show all planned actions without executing.
6. **Ask on conflict.** If symlink points to different source — ask user, don't auto-replace.

## Anti-Patterns

- Writing TO Claude settings from Gemini/Codex (reverse sync)
- Deleting target-only MCP servers during sync
- Creating symlinks inside symlinks (circular)
- Modifying config files without backup

---

## Definition of Done

| # | Criterion |
|---|-----------|
| 1 | Claude settings read successfully |
| 2 | Skills symlinks created/verified for each target |
| 3 | MCP settings synced with format conversion (JSON→TOML for Codex) |
| 4 | Backup files created before any config modification |
| 5 | Report shown with all actions and warnings |

---

**Version:** 1.1.0
**Last Updated:** 2026-03-09
