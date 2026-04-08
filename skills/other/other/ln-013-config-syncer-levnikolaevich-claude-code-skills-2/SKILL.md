---
name: ln-013-config-syncer
description: "Syncs skills, MCP settings, and hooks from Claude Code to Gemini CLI and Codex CLI via symlinks and config conversion. Use when agent configs need alignment."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`) are relative to skills repo root. Locate this SKILL.md directory and go up one level for repo root.

# Config Syncer

**Type:** L3 Worker
**Category:** 0XX Shared

Synchronizes skills (via symlinks) and MCP/hook settings from Claude Code (source of truth) to Gemini CLI and Codex CLI. Converts formats: JSON for Gemini, TOML for Codex.

---

## Input / Output

| Direction | Content |
|-----------|---------|
| **Input** | OS info, `disabled` flags per agent, `targets` (gemini/codex/both), `dry_run` flag, optional `runId`, optional `summaryArtifactPath` |
| **Output** | Structured summary envelope with `payload.status` = `completed` / `skipped` / `error`, plus per-target sync outcomes in `changes` / `detail` |

If `summaryArtifactPath` is provided, write the same summary JSON there. If not provided, return the summary inline and remain fully standalone. If `runId` is not provided, generate a standalone `run_id` before emitting the summary envelope.

---

## Config Paths by OS

| Agent | Windows | macOS / Linux |
|-------|---------|---------------|
| **Claude** (primary) | `%USERPROFILE%\.claude.json` | `~/.claude.json` |
| **Claude** (fallback) | `%USERPROFILE%\.claude\settings.json` | `~/.claude/settings.json` |
| **Gemini** | `%USERPROFILE%\.gemini\settings.json` | `~/.gemini/settings.json` |
| **Codex** | `%USERPROFILE%\.codex\config.toml` | `~/.codex/config.toml` |

---

## Workflow

```
Discover State  -->  Sync Skills  -->  Sync MCP  -->  Sync Hooks  -->  Report
```

### Phase 1: Discover State

1. Read Claude settings (source of truth):
   - `~/.claude.json` (primary) + `~/.claude/settings.json` (fallback)
   - Merge: primary overrides fallback by server name
2. Read target configs (if exist):
   - Gemini: `~/.gemini/settings.json` → extract `mcpServers`
   - Codex: `~/.codex/config.toml` → extract `[mcp_servers.*]`
3. Check existing symlinks: `~/.gemini/skills`, `~/.codex/skills`
4. Display current state table

### Phase 2: Sync Skills (symlinks/junctions)

For each target where `disabled` is not `true`:

| OS | Command |
|----|---------|
| Windows | `node -e "require('fs').symlinkSync('{source}', '{target}', 'junction')"` |
| macOS/Linux | `ln -s "{source}" "{target}"` |

Decision logic:

| Condition | Action |
|-----------|--------|
| `disabled: true` for this agent | SKIP, report "disabled" |
| Link exists, points correctly | SKIP, report "already linked" |
| Link exists, points wrong | WARN, ask user before replacing |
| Real directory exists (not link) | WARN, skip (avoid data loss) |
| No link exists | Create link |
| Link exists, target does not exist (stale) | WARN "stale junction: {path} → {dead_target}". Remove stale link, recreate with correct target |

**Stale junction detection:** Use `lstatSync()` (succeeds on dangling links) + `statSync()` (throws if target missing). Do NOT rely on `existsSync()` alone — it returns `false` for dangling junctions on Windows, but the filesystem entry still exists and will cause `EEXIST` on create.

### Phase 3: Sync MCP Settings
IF agent `disabled: true` → SKIP for that target.

**3a: Claude to Gemini (JSON to JSON)**

| Claude Field | Gemini Field | Notes |
|---|---|---|
| `type: "http"` + `url` | `url` | HTTP (Gemini auto-detects streamable/SSE) |
| `command` + `args` | `command` + `args` | stdio (same format) |
| `env` | `env` | Same format |
| `headers` | `headers` | Same format |

Gemini-only fields (preserve during merge, not mapped from Claude):
`timeout`, `trust`, `includeTools`, `excludeTools`

**3b: Claude to Codex (JSON to TOML)**

| Claude JSON | Codex TOML | Notes |
|---|---|---|
| `command` | `command` | Same |
| `args` | `args` | JSON array to TOML array |
| `env` | `[mcp_servers.{name}.env]` | Nested table |
| `type: "http"` + `url` | `url` | Codex auto-detects by `url` presence |
| `headers` | `http_headers` | **Different key name** |

Codex-only fields (preserve during merge, not mapped from Claude):
`bearer_token_env_var`, `enabled_tools`, `disabled_tools`, `startup_timeout_sec`, `tool_timeout_sec`, `enabled`, `required`

**Merge strategy (both targets):** Claude servers override target by key name. Target-only servers preserved. Backup `.bak` before writing.

**Windows implementation note:** Config format conversions with regex or backslash escaping (especially JSON→TOML for Codex) MUST use a temporary `.mjs` script file, not inline `node -e` or bash heredocs. Git Bash/MSYS2 mangles backslashes in both forms. Pattern: write temp file → `node "$TEMP/sync.mjs"` → delete after.

### Phase 4: Sync Hooks

**4a: Claude to Gemini (event name + tool name mapping)**

| Claude Event | Gemini Event | Notes |
|---|---|---|
| `PreToolUse` | `BeforeTool` | Same concept, different name |
| `PostToolUse` | `AfterTool` | Same concept, different name |
| `Stop` | `AfterAgent` | Agent completion |
| `SessionStart` | `SessionStart` | Same name |

Tool name mapping in hook matchers:

| Claude Tool Name | Gemini Tool Name |
|---|---|
| `Read` | `read_file` |
| `Edit` | `edit_file` |
| `Write` | `write_file` |
| `Grep` | `search_files` |

Hook scripts must support both tool name formats (same mapping as matchers above).

**4b: Claude to Codex**

Codex does NOT support hooks. SKIP hook sync for Codex. Report "hooks not supported by Codex CLI".

### Phase 4c: Gemini MCP Policy

Gemini CLI policy engine blocks MCP tool calls by default (error: "Tool execution denied by policy") even with `--yolo`. Fix: ensure `~/.gemini/policies/allow-mcp.toml` exists.

| Condition | Action |
|-----------|--------|
| File exists with `mcpName` allow rule | SKIP |
| File missing or no allow rule | Create `~/.gemini/policies/allow-mcp.toml` |

File content:

```toml
[[rule]]
mcpName = "*"
decision = "allow"
priority = 200
```

### Phase 5: Report

```
Config Sync:
| Action         | Target | Status                         |
|----------------|--------|--------------------------------|
| Skills symlink | Gemini | created -> ~/.claude/plugins   |
| Skills symlink | Codex  | already linked                 |
| MCP sync       | Gemini | 4 servers synced (2 new)       |
| MCP sync       | Codex  | 4 servers synced (1 new)       |
| Hooks sync     | Gemini | 3 events synced                |
| Hooks sync     | Codex  | skipped (not supported)        |
| MCP policy     | Gemini | allow-mcp.toml created         |
```

---

## Critical Rules

1. **Claude = source of truth.** Never write TO Claude settings. Read-only source
2. **Non-destructive merge.** Target-only servers and settings preserved. Only Claude servers added/updated
3. **No data loss.** Real directories (not symlinks) at target path → warn and skip, never delete
4. **Backup before write.** Create `.bak` copy before modifying any config file
5. **Respect `disabled` flags.** Skip all operations for disabled agents
6. **Idempotent.** Safe to run multiple times. Already-synced state is skipped
7. **Non-destructive config writes.** Always read → deep-merge → edit. Never overwrite target config files from scratch. Preserve all keys not mapped from Claude.

## Anti-Patterns

| DON'T | DO |
|-------|-----|
| Write TO Claude settings from targets | Claude is read-only source |
| Delete target-only MCP servers during sync | Preserve target-only servers |
| Create symlinks inside symlinks (circular) | Check link target before creating |
| Modify config files without backup | Always create `.bak` first |
| Try to sync hooks to Codex | Report "not supported", skip |
| Use `cmd /c mklink /J` from Git Bash | Use `fs.symlinkSync(source, target, 'junction')` via Node.js — works from any shell |
| Auto-replace mispointed symlinks | Ask user before replacing |
| Overwrite entire config file with only known fields | Read existing → deep-merge only owned fields → edit back |

---

## Definition of Done

- [ ] Claude settings read successfully (both config locations)
- [ ] Skills symlinks created/verified for each non-disabled target
- [ ] MCP settings synced with correct format conversion (JSON for Gemini, TOML for Codex)
- [ ] Hook events and tool names mapped for Gemini
- [ ] Codex hooks skipped with report
- [ ] Gemini MCP policy file verified/created
- [ ] Backup files created before any config modification
- [ ] Final report table displayed

---

**Version:** 1.1.0
**Last Updated:** 2026-04-05
