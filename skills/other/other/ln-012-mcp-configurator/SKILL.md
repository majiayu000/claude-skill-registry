---
name: ln-012-mcp-configurator
description: "Installs MCP servers, registers them in Claude Code, and grants user-level permissions. Use when MCP servers need setup or reconfiguration."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`) are relative to skills repo root. Locate this SKILL.md directory and go up one level for repo root.

# MCP Configurator

**Type:** L3 Worker
**Category:** 0XX Shared

Configures MCP servers in Claude Code: audits state, registers servers, installs hooks and output style, migrates allowed-tools, updates instruction files, grants permissions, analyzes token budget.

---

## Input / Output

| Direction | Content |
|-----------|---------|
| **Input** | OS info, existing MCP state (optional, from scan), `dry_run` flag |
| **Output** | Per-server status (`configured` / `added` / `skipped` / `failed`), budget analysis |

---

## Server Registry

Two transport types: **stdio** (local process) and **HTTP** (cloud endpoint).

| Server | Transport | Source | Required | API Key |
|--------|-----------|--------|----------|---------|
| hex-line | stdio | `npm i -g @levnikolaevich/hex-line-mcp` → `hex-line-mcp` | Yes | No |
| hex-ssh | stdio | `npm i -g @levnikolaevich/hex-ssh-mcp` → `hex-ssh-mcp` | No | No |
| hex-graph | stdio | `npm i -g @levnikolaevich/hex-graph-mcp` → `hex-graph-mcp` | No | No |
| context7 | HTTP | `https://mcp.context7.com/mcp` | Yes | Optional |
| Ref | HTTP | `https://api.ref.tools/mcp` | Yes | Yes (prompt user) |
| linear | HTTP | `https://mcp.linear.app/mcp` | Ask user | No (OAuth) |

**hex-line/hex-ssh/hex-graph source selection:** Prefer global install (`npm i -g`). Hooks require stable absolute path — `npx` cache is ephemeral and rejected by `setup_hooks`. Use local `node {repo}/mcp/*/server.mjs` only for active MCP development.

---

## Workflow

Audit  -->  Update  -->  Configure  -->  Register  -->  Permissions  -->  Budget  -->  Report

### Phase 1: Audit Current MCP State

1. Run `claude mcp list` — canonical source of truth for configured servers
   - Parse output: server name, transport type, connection status
   - Fallback if `claude` CLI unavailable: read `~/.claude.json` + `~/.claude/settings.json`, merge by server name
2. Build table of configured vs missing servers (compare against registry)
3. Check for deprecated servers and flag for removal:

| Deprecated Server | Action |
|-------------------|--------|
| hashline-edit | Remove if found |
| pencil | Remove if found |
| lighthouse | Remove if found |
| playwright | Remove if found |
| browsermcp | Remove if found |

### Phase 2: Update Outdated npm Packages

For each hex MCP package (`@levnikolaevich/hex-line-mcp`, `hex-ssh-mcp`, `hex-graph-mcp`):

1. Check if globally installed: `npm ls -g @levnikolaevich/hex-line-mcp --json 2>/dev/null`
2. If installed, check for updates: `npm outdated -g @levnikolaevich/hex-line-mcp`
3. If outdated → run `npm i -g @levnikolaevich/hex-line-mcp@latest`
4. Report: `"hex-line: 1.1.0 → 1.1.2 (updated)"` or `"hex-line: 1.1.2 (current)"`

```bash
# Check and update all hex MCP packages:
for pkg in @levnikolaevich/hex-line-mcp @levnikolaevich/hex-ssh-mcp @levnikolaevich/hex-graph-mcp; do
  current=$(npm ls -g "$pkg" --json 2>/dev/null | node -e "try{console.log(JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')).dependencies['${pkg}'].version)}catch{console.log('')}")
  if [ -n "$current" ]; then
    latest=$(npm view "$pkg" version 2>/dev/null)
    if [ "$current" != "$latest" ]; then
      npm i -g "${pkg}@latest"
      echo "$pkg: $current → $latest (updated)"
    else
      echo "$pkg: $current (current)"
    fi
  fi
done
```

**Skip conditions:**
- Package not installed globally → skip (Phase 3 handles fresh installs)
- `dry_run: true` → show planned update, do not execute
- Dev mode servers (local `node {repo}/mcp/*/server.mjs`) → skip npm update

### Phase 3: Configure Missing Servers

For each server in registry not yet configured:

1. IF already configured AND `claude mcp list` shows connected → SKIP
2. IF `dry_run: true` → show planned `claude mcp add` command, do not execute
3. IF **linear** → ask user: "Do you use Linear for task management?" → no → SKIP

### Phase 4: Register via `claude mcp add`

Registration commands by server and source:

| Server | Command |
|--------|---------|
| hex-line (global) | `npm i -g @levnikolaevich/hex-line-mcp` then `claude mcp add -s user hex-line -- hex-line-mcp` |
| hex-ssh (global) | `npm i -g @levnikolaevich/hex-ssh-mcp` then `claude mcp add -s user hex-ssh -- hex-ssh-mcp` |
| hex-graph (global) | `npm i -g @levnikolaevich/hex-graph-mcp` then `claude mcp add -s user hex-graph -- hex-graph-mcp` |
| hex-line (dev) | `claude mcp add -s user hex-line -- node {repo}/mcp/hex-line-mcp/server.mjs` |
| hex-ssh (dev) | `claude mcp add -s user hex-ssh -- node {repo}/mcp/hex-ssh-mcp/server.mjs` |
| hex-graph (dev) | `claude mcp add -s user hex-graph -- node {repo}/mcp/hex-graph-mcp/server.mjs` |
| context7 | `claude mcp add -s user --transport http context7 https://mcp.context7.com/mcp` |
| Ref | `claude mcp add -s user --transport http Ref https://api.ref.tools/mcp` |
| linear | `claude mcp add -s user --transport http linear-server https://mcp.linear.app/mcp` |

**Post-registration verification:** After ALL servers are registered, run `claude mcp list` once. For each hex MCP (hex-line, hex-ssh, hex-graph): verify status is `Connected`. If any shows disconnected or missing — retry `claude mcp add`, then re-check. Report failures explicitly.

**Error handling:**

| Error | Response |
|-------|----------|
| `claude` CLI not found | FAIL, report "Claude CLI not in PATH" |
| Server already exists | SKIP, report "already configured" |
| Connection failed after add | WARN, report detail from `claude mcp list` |
| API key missing (Ref) | Prompt user for key, skip if declined |

### Phase 4b: Install Hooks and Output Style [CRITICAL]

MUST call `mcp__hex-line__setup_hooks(agent="claude")` immediately after hex-line registration. This configures:

**Hooks** (in `~/.claude/settings.json`):
1. `PreToolUse` hook — redirects built-in Read/Edit/Write/Grep to hex-line equivalents
2. `PostToolUse` hook — compresses verbose tool output (RTK filter)
3. `SessionStart` hook — injects MCP Tool Preferences reminder
4. Sets `disableAllHooks: false`

**Output Style:**
5. Copies `output-style.md` to `~/.claude/output-styles/hex-line.md`
6. Sets `outputStyle: "hex-line"` if no style is active (preserves existing style)

**Verification:** After setup_hooks returns, confirm hooks array is non-empty in its response. If empty or error — STOP and report failure. Without hooks, hex-line pipeline does not work.

### Phase 4c: Graph Indexing

After hex-graph registration + connected status:
1. `mcp__hex-graph__index_project({ path: "{project_path}" })` — build initial code knowledge graph
2. `mcp__hex-graph__watch_project({ path: "{project_path}" })` — enable live incremental updates on file changes

Skip if hex-graph not registered or not connected.

### Phase 4d: Migrate Project allowed-tools [CRITICAL]

After hex-line is configured, MUST scan project commands and skills to replace built-in tools with hex-line equivalents in `allowed-tools` frontmatter. Failure to do this leaves commands using slow built-in tools despite hex-line being available.

**Tool mapping:**

| Built-in | Hex equivalent |
|----------|---------------|
| `Read` | `mcp__hex-line__read_file` |
| `Edit` | `mcp__hex-line__edit_file` |
| `Write` | `mcp__hex-line__write_file` |
| `Grep` | `mcp__hex-line__grep_search` |

**Steps:**

1. Glob `.claude/commands/*.md` + `.claude/skills/*/SKILL.md` in current project
2. For each file: parse YAML frontmatter, extract `allowed-tools`
3. For each mapping entry:
   a. If built-in present AND hex equivalent absent → add hex equivalent, remove built-in (except `Read` and `Bash`)
   b. If built-in present AND hex equivalent already present → remove built-in (except `Read` and `Bash`)
   c. Preserve ALL existing `mcp__*` tools not in the replacement table (e.g., `mcp__hex-ssh__remote-ssh`)
4. Write back updated frontmatter (preserve quoting style)
5. Report:

```
allowed-tools Migration:
| File                        | Tools Added                    | Status           |
|-----------------------------|--------------------------------|------------------|
| commands/deploy.md          | read_file, edit_file           | migrated         |
| commands/run-tests.md       | —                              | already migrated |
| commands/review.md          | —                              | no allowed-tools |
```

**Skip conditions:**

| Condition | Action |
|-----------|--------|
| No `.claude/` directory | Skip entire phase |
| File has no `allowed-tools` | Skip file, report "no allowed-tools" |
| All hex equivalents present, no stale built-ins, all `mcp__*` preserved | Skip file, report "already migrated" |
| `dry_run: true` | Show planned changes, don't write |

**Strategy:** REPLACE built-in tools with hex-line equivalents. Keep `Bash` and `Read` (always needed). Preserve all existing `mcp__*` tools (hex-ssh, linear, etc.) that are NOT being replaced.

### Phase 4e: Update Instruction Files [CRITICAL]

After hex-line is configured with hooks, ensure instruction files have MCP Tool Preferences section. Without this section, agents default to built-in tools in every session — negating the entire hex-line setup.

**MANDATORY READ:** Load `mcp/hex-line-mcp/output-style.md` → use its `# MCP Tool Preferences` section as template. MUST include the full table (Read, Edit, Write, Grep + directory_tree row).

**Steps (MUST execute all):**

1. For each file: CLAUDE.md, GEMINI.md, AGENTS.md (if exists in project):
2. Search for `## MCP Tool Preferences` or `### MCP Tool Preferences`
3. If MISSING → MUST insert section before `## Navigation` (or at end of conventions/rules block)
4. If PRESENT but OUTDATED → MUST update table rows to match template
5. For GEMINI.md: MUST adapt tool names (`Read` → `read_file`, `Edit` → `edit_file`, `Grep` → `search_files`)

**Skip conditions:**

| Condition | Action |
|-----------|--------|
| File doesn't exist | Skip (don't create instruction files) |
| Section already matches template | Skip, report "up to date" |

### Phase 5: Grant Permissions

For each **configured** MCP server, add `mcp__{name}` to `~/.claude/settings.json` → `permissions.allow[]`.

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
3. Missing → append
4. Write back (2-space indent JSON)
5. Report: `"Granted N permissions (M already present)"`

**Idempotent:** existing entries skipped.

### Phase 6: Budget Analysis

| Metric | Formula | Threshold |
|--------|---------|-----------|
| Server count | count of `mcpServers` keys | recommended 5 or fewer |
| Estimated tokens | count x 5000 | recommended 25,000 or fewer |
| Context percentage | tokens / 200,000 x 100 | recommended 12.5% or less |

Budget warnings:

| Server Count | Level | Message |
|--------------|-------|---------|
| 1-5 | OK | "Budget within limits" |
| 6-8 | WARN | "Consider disabling unused MCP servers to reduce context overhead" |
| >8 | WARN | "Significant context impact — review which servers are actively used" |

### Phase 7: Report

```
MCP Configuration:
| Server    | Transport | Status        | Permission | Detail                  |
|-----------|-----------|---------------|------------|-------------------------|
| hex-line  | stdio     | configured    | granted    | global npm (hex-line-mcp) |
| hex-ssh   | stdio     | added         | granted    | global npm (hex-ssh-mcp)  |
| context7  | HTTP      | configured    | granted    | mcp.context7.com        |
| Ref       | HTTP      | configured    | granted    | api.ref.tools (key set) |
| linear    | HTTP      | skipped       | skipped    | user declined           |

Budget: 4 servers ~ 20K tokens (10.0% of context) — OK
```

---

### Phase 8: Token Efficiency Benchmark

After hex-line is configured, run benchmark on user's repo:

```bash
node "$(npm root -g)/@levnikolaevich/hex-line-mcp/benchmark.mjs"
```

Display results to user — demonstrates value of the MCP setup just completed.

Key metrics shown:
- Outline vs full read savings (expect 57-93% on medium-XL files)
- Compact diff savings (expect 32-38% on edits)
- Hash overhead (expect ~0% — negligible)
- Break-even point (typically ~30 lines)

Report savings summary to user.

---

## Critical Rules

1. **Write only via sanctioned paths.** Register servers via `claude mcp add`. Write to `~/.claude/settings.json` ONLY for hooks (via `setup_hooks`), permissions (`permissions.allow[]`), and `outputStyle`
2. **Verify after add.** Always run `claude mcp list` after registration to confirm connection
3. **Ask before optional servers.** Linear requires explicit user consent
4. **Prefer global install.** Use `npm i -g` for hex-line/hex-ssh/hex-graph — hooks need stable paths. Local only for active MCP development
5. **Remove deprecated servers.** Clean up servers no longer in the registry
6. **Grant permissions.** After registration, add `mcp__{server}` to user `~/.claude/settings.json`

## Anti-Patterns

| DON'T | DO |
|-------|-----|
| Write arbitrary fields to `~/.claude.json` | Use `claude mcp add` for servers, `setup_hooks` for hooks |
| Skip verification after add | Always check `claude mcp list` |
| Auto-add optional servers | Ask user for Linear and other optional servers |
| Ignore budget impact | Always calculate and report token budget |
| Leave deprecated servers | Remove hashline-edit, pencil, etc. |

---

## Definition of Done

- [ ] Current MCP state audited via `claude mcp list`
- [ ] Outdated hex-* npm packages updated (or skipped if current)
- [ ] Missing required servers registered via `claude mcp add`
- [ ] Each registered server verified via `claude mcp list`
- [ ] Hooks installed in settings.json (PreToolUse, PostToolUse, SessionStart) and `disableAllHooks: false`
- [ ] Output style installed (`outputStyle: "hex-line"` or existing style preserved)
- [ ] Token budget calculated and warnings shown if applicable
- [ ] Final status table displayed with all servers
- [ ] Permissions granted for all configured servers in user settings
- [ ] Project allowed-tools migrated: built-ins replaced with hex-line, existing `mcp__*` preserved
- [ ] MCP Tool Preferences section present in all existing instruction files
- [ ] Token efficiency benchmark run and results shown

---

**Version:** 1.1.0
**Last Updated:** 2026-03-20
