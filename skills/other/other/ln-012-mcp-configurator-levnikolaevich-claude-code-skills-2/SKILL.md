---
name: ln-012-mcp-configurator
description: "Installs MCP packages, registers servers in Claude Code, configures hooks, permissions, and migrations. Use when MCP needs setup or reconfiguration."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`) are relative to skills repo root. Locate this SKILL.md directory and go up one level for repo root.

# MCP Configurator

**Type:** L3 Worker
**Category:** 0XX Shared

Configures MCP servers in Claude Code: installs npm packages, registers servers, installs hooks and output style, migrates allowed-tools, updates instruction files, grants permissions.

---

## Input / Output

| Direction | Content |
|-----------|---------|
| **Input** | OS info, `dry_run` flag, optional `runId`, optional `summaryArtifactPath` |
| **Output** | Structured summary envelope with per-server status (`configured` / `added` / `updated` / `skipped` / `failed`) |

If `summaryArtifactPath` is provided, write the same summary JSON there. If not provided, return the summary inline and remain fully standalone.

---

## Server Registry

Two transport types: **stdio** (local process) and **HTTP** (cloud endpoint).

| Server | Transport | Install | Required | API Key |
|--------|-----------|---------|----------|---------|
| hex-line | stdio | `npx -y @levnikolaevich/hex-line-mcp` | Yes | No |
| hex-ssh | stdio | `npx -y @levnikolaevich/hex-ssh-mcp` | No | No |
| hex-graph | stdio | `npx -y @levnikolaevich/hex-graph-mcp` | No | No |
| context7 | HTTP | `https://mcp.context7.com/mcp` | Yes | Optional |
| Ref | HTTP | `https://api.ref.tools/mcp` | Yes | Yes (prompt user) |
| linear | HTTP | `https://mcp.linear.app/mcp` | Ask user | No (OAuth) |


---

## Workflow

```
Check Status & Version → Register & Configure → Hooks → Permissions → Migrate → Report
```

### Phase 1: Check Status & Version

Smart install: check MCP status AND package drift. npx -y caches aggressively — a connected server may still be backed by an older cached package.

**Step 1a: Check MCP server status**

Run `claude mcp list` -> parse each hex server:

| Server | Status | Action |
|--------|--------|--------|
| Registered + Connected | Working | Check version (Step 1b) |
| Registered + Disconnected | Broken | Re-register (Phase 2) |
| Not registered | Missing | Register in Phase 2 |

**Step 1b: Version check for connected hex-* servers**

For each connected hex server, run in parallel:
```bash
npm view @levnikolaevich/${PKG} version 2>/dev/null
```

Then compare npm latest against the running local version:
1. **npx cache probe:** `npm config get cache` -> scan `{cacheRoot}/_npx/**/node_modules/@levnikolaevich/${PKG}/package.json` -> pick newest by semver/mtime

Use the npx cache version. If probe returns nothing, report `running=unknown` and treat the server as refresh-recommended rather than claiming it is current.

Note: hex packages run via `npx -y`, NOT global install. Never probe global npm paths.

| npm latest | cached local version | Action |
|------------|---------|--------|
| Same | Same | SKIP |
| Newer | Older | Mark "needs update" -> Phase 2 re-registers |
| Unknown | Any | WARN, proceed |

**Skip conditions:**

| Condition | Action |
|-----------|---------|
| `disabled: true` | SKIP |
| `dry_run: true` | Show planned commands |
| Connected + cached local version matches npm latest | SKIP, report version |

### Phase 2: Register & Configure

One pass: use Phase 1 state (do NOT re-run `claude mcp list`) -> remove deprecated -> register/update -> verify.

1. **Reuse Phase 1 state** — server map from Step 1a already has registration + connection status
   - Fallback (standalone only): read `~/.claude.json` + `~/.claude/settings.json`
2. Remove deprecated servers:

| Deprecated Server | Action |
|-------------------|--------|
| hashline-edit | Remove if found |
| pencil | Remove if found |
| lighthouse | Remove if found |
| playwright | Remove if found |
| browsermcp | Remove if found |

3. Register missing OR update outdated servers:
   - IF already configured AND connected AND cached local version matches -> SKIP
   - IF connected but outdated -> remove + re-add (forces npx to fetch latest)
   - IF `dry_run: true` -> show planned command
   - IF **linear** -> ask user: "Do you use Linear?" -> no -> SKIP

Registration commands (OS-dependent prefix):

| OS | Prefix | Why |
|----|--------|-----|
| Windows (bash/MSYS2) | `MSYS_NO_PATHCONV=1 claude mcp add ... -- cmd /c npx` | MSYS2/Git Bash converts `/c` -> `C:/` in args. `MSYS_NO_PATHCONV=1` prevents this |
| Windows (PowerShell/cmd) | `cmd /c npx` | No path conversion issue in native shells |
| macOS / Linux | `npx` | Direct execution |

| Server | Command (Windows bash — always prefix with `MSYS_NO_PATHCONV=1`) |
|--------|----------|
| hex-line | `MSYS_NO_PATHCONV=1 claude mcp add -s user hex-line -- cmd /c npx -y @levnikolaevich/hex-line-mcp` |
| hex-ssh | `MSYS_NO_PATHCONV=1 claude mcp add -s user hex-ssh -- cmd /c npx -y @levnikolaevich/hex-ssh-mcp` |
| hex-graph | `MSYS_NO_PATHCONV=1 claude mcp add -s user hex-graph -- cmd /c npx -y @levnikolaevich/hex-graph-mcp` |
| context7 | `claude mcp add -s user --transport http context7 https://mcp.context7.com/mcp` |
| Ref | `claude mcp add -s user --transport http Ref https://api.ref.tools/mcp` |
| linear | `claude mcp add -s user --transport http linear-server https://mcp.linear.app/mcp` |

4. Verify: `claude mcp list` -> check all registered show `Connected`. This is the only second `claude mcp list` call (post-mutation verify). Retry + report failures.

**Windows MSYS2 path validation (MANDATORY on win32):**
After registration, read `~/.claude.json` -> verify each hex server's `args[0]` is `"/c"` not `"C:/"`.
If corrupted: fix via `mcp__hex-line__edit_file` (set_line the arg to `"/c"`).


**Error handling:**

| Error | Response |
|-------|----------|
| `claude` CLI not found | FAIL, report "Claude CLI not in PATH" |
| Server already exists | SKIP, report "already configured" |
| Connection failed after add | WARN, report detail from `claude mcp list` |
| API key missing (Ref) | Prompt user for key, skip if declined |

### Phase 3: Hooks & Output Style [CRITICAL]

MUST call `mcp__hex-line__setup_hooks(agent="all")` AFTER all Phase 2 registrations complete (not just hex-line). This ensures the latest hook.mjs and output-style.md from the updated package are installed.

**Hooks** (in `~/.claude/settings.json`):
1. `PreToolUse` hook — redirects built-in Read/Edit/Write/Grep to hex-line equivalents
2. `PostToolUse` hook — compresses verbose tool output (RTK filter)
3. `SessionStart` hook — injects MCP Tool Preferences reminder
4. Sets `disableAllHooks: false`

**Output Style:**
5. Copies `output-style.md` to `~/.claude/output-styles/hex-line.md`
6. Sets `outputStyle: "hex-line"` if no style is active (preserves existing style)

**Verification:** Response must contain `Hooks configured for`. If `SKIPPED`, `UNKNOWN_AGENT`, `Error`, or `failed` — STOP.

**Note:** `setup_hooks(agent="all")` also syncs MCP server entries and hook paths for Gemini. Codex is reported as "not supported" (expected). After this call, ln-013 should verify Gemini state rather than blindly overwriting.

**Note:** `setup_hooks(agent="all")` is idempotent. Calling it again during later verification is safe and keeps hooks current.

### Phase 4: Graph Indexing

After hex-graph registration + connected status:
1. `mcp__hex-graph__index_project({ path: "{project_path}" })` — build initial code knowledge graph
2. `mcp__hex-graph__watch_project({ path: "{project_path}" })` — enable live incremental updates

Skip if hex-graph not registered or not connected.

### Phase 5: Migrate allowed-tools [CRITICAL]

Scan project commands/skills to replace built-in tools with hex-line equivalents in `allowed-tools` frontmatter.

**Tool mapping:**

| Built-in | Hex equivalent |
|----------|----------------|
| `Read` | `mcp__hex-line__read_file` |
| `Edit` | `mcp__hex-line__edit_file` |
| `Write` | `mcp__hex-line__write_file` |
| `Grep` | `mcp__hex-line__grep_search` |

**Steps:**

1. Glob `.claude/commands/*.md` + `.claude/skills/*/SKILL.md` in current project
2. For each file: parse YAML frontmatter, extract `allowed-tools`
3. For each mapping entry:
   a. If built-in present AND hex equivalent absent -> add hex equivalent, remove built-in (except `Read` and `Bash`)
   b. If built-in present AND hex equivalent already present -> remove built-in (except `Read` and `Bash`)
   c. Preserve ALL existing `mcp__*` tools not in the replacement table
4. Write back updated frontmatter (preserve quoting style)


**Skip conditions:**

| Condition | Action |
|-----------|--------|
| No `.claude/` directory | Skip entire phase |
| File has no `allowed-tools` | Skip file |
| All hex equivalents present | Skip file, report "already migrated" |
| `dry_run: true` | Show planned changes |

### Phase 6: Update Instruction Files [CRITICAL]

Ensure instruction files have MCP Tool Preferences section.

**MANDATORY READ:** Load `mcp/hex-line-mcp/output-style.md` -> use its `# MCP Tool Preferences` section as template.

**Steps:**

1. For each file: CLAUDE.md, GEMINI.md, AGENTS.md (if exists in project)
2. Search for `## MCP Tool Preferences` or `### MCP Tool Preferences`
3. If MISSING -> insert before `## Navigation` (or at end of conventions/rules block)
4. If PRESENT but OUTDATED -> update table rows to match template
5. For GEMINI.md: adapt tool names (`Read` -> `read_file`, `Edit` -> `edit_file`, `Grep` -> `search_files`)

**Skip conditions:**

| Condition | Action |
|-----------|--------|
| File doesn't exist | Skip |
| Section already matches template | Skip, report "up to date" |

### Phase 7: Grant Permissions

For each **configured** MCP server, add `mcp__{name}` to `~/.claude/settings.json` -> `permissions.allow[]`.

| Server | Permission entry |
|---|---|
| hex-line | `mcp__hex-line` |
| hex-ssh | `mcp__hex-ssh` |
| hex-graph | `mcp__hex-graph` |
| context7 | `mcp__context7` |
| Ref | `mcp__Ref` |
| linear | `mcp__linear-server` |

1. Read `~/.claude/settings.json` (create if missing: `{"permissions":{"allow":[]}}`)
2. For each configured server: check if `mcp__{name}` already in `allow[]`
3. Missing -> append
4. Write back (2-space indent JSON)

**Idempotent:** existing entries skipped.

### Phase 8: Report

**Status table:**

```
MCP Configuration:
| Server    | Transport | Version | Status        | Permission | Detail                  |
|-----------|-----------|---------|---------------|------------|-------------------------|
| hex-line  | stdio     | 1.5.0   | configured    | granted    | global npm (hex-line-mcp) |
| hex-ssh   | stdio     | 1.2.0   | updated       | granted    | was 1.1.6, now 1.2.0     |
| context7  | HTTP      | —       | configured    | granted    | mcp.context7.com        |
| Ref       | HTTP      | —       | configured    | granted    | api.ref.tools (key set) |
| linear    | HTTP      | —       | skipped       | skipped    | user declined           |
```

---

## Critical Rules

1. **Write only via sanctioned paths.** Register servers via `claude mcp add`. Write to `~/.claude/settings.json` ONLY for hooks (via `setup_hooks`), permissions (`permissions.allow[]`), and `outputStyle`
2. **Verify after add.** Always run `claude mcp list` after registration to confirm connection
3. **Ask before optional servers.** Linear requires explicit user consent
4. **npx -y for all hex MCP.** Never `npm i -g` — npx provides process isolation and avoids EBUSY on Windows. On Windows, wrap with `cmd /c npx` (see Phase 2 OS prefix table)
5. **Remove deprecated servers.** Clean up servers no longer in the registry
6. **Grant permissions.** After registration, add `mcp__{server}` to user settings
7. **Minimize `claude mcp list` calls.** Phase 1 runs it once (discovery). Phase 2 reuses that data. Only Phase 2 Step 4 runs it again (post-mutation verify). Max 2 calls total
8. **Always check npm drift.** Connected != up to date. Compare npm latest against the newest locally cached npx package version before skipping
9. **MSYS2 path safety.** On Windows with Git Bash/MSYS2, always prefix `claude mcp add` with `MSYS_NO_PATHCONV=1`. After registration, verify `args[0]` in `.claude.json` is `"/c"` not `"C:/"`. Fix inline if corrupted.

## Anti-Patterns

| DON'T | DO |
|-------|-----|
| Write arbitrary fields to `~/.claude.json` | Use `claude mcp add` for servers, `setup_hooks` for hooks |
| Skip verification after add | Always check `claude mcp list` after mutations |
| Auto-add optional servers | Ask user for Linear and other optional servers |
| Leave deprecated servers | Remove hashline-edit, pencil, etc. |
| Calculate token budget | Not this worker's responsibility |
| Run `claude mcp list` in every phase | Run once in Phase 1, reuse in Phase 2, verify once after mutations |
| Assume connected = up to date | Check `npm view` version vs newest cached npx package version |
| Call `setup_hooks` before all packages re-registered | Call `setup_hooks(agent="all")` AFTER all Phase 2 registrations complete |
| Run `claude mcp add` without MSYS_NO_PATHCONV on Windows bash | Always `MSYS_NO_PATHCONV=1 claude mcp add ...` or verify+fix args after |

---

## Definition of Done

- [ ] MCP packages installed and versions verified against npm registry (Phase 1)
- [ ] Missing servers registered and verified connected (Phase 2)
- [ ] Outdated servers re-registered with latest version (Phase 2)
- [ ] Hooks installed (PreToolUse, PostToolUse, SessionStart) and `disableAllHooks: false` (Phase 3)
- [ ] Output style installed (Phase 3)
- [ ] Permissions granted for all configured servers (Phase 7)
- [ ] Project allowed-tools migrated (Phase 5)
- [ ] MCP Tool Preferences in all instruction files (Phase 6)
- [ ] Status table with version column displayed (Phase 8)

---

**Version:** 1.4.1
**Last Updated:** 2026-03-25
