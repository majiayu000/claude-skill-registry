---
name: ln-012-mcp-configurator
description: "Installs MCP server npm packages and registers them in Claude Code. Use when MCP servers need setup or reconfiguration."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`) are relative to skills repo root. Locate this SKILL.md directory and go up one level for repo root.

# MCP Configurator

**Type:** L3 Worker
**Category:** 0XX Shared

Configures MCP servers in Claude Code: audits current state, registers missing servers via `claude mcp add`, analyzes token budget impact.

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
| hex-line | stdio | local `mcp/hex-line-mcp/server.mjs` OR `npx -y @levnikolaevich/hex-line-mcp` | Yes | No |
| hex-ssh | stdio | local `mcp/hex-ssh-mcp/server.mjs` OR `npx -y @levnikolaevich/hex-ssh-mcp` | No | No |
| hex-graph | stdio | local `mcp/hex-graph-mcp/server.mjs` | No | No |
| context7 | HTTP | `https://mcp.context7.com/mcp` | Yes | Optional |
| Ref | HTTP | `https://api.ref.tools/mcp` | Yes | Yes (prompt user) |
| linear | HTTP | `https://mcp.linear.app/mcp` | Ask user | No (OAuth) |

**hex-line/hex-ssh/hex-graph source selection:** Prefer local path if skills repo is cloned and `mcp/` directory exists. Otherwise use `npx -y {pkg}` (not available for hex-graph yet).

---

## Workflow

```
Audit  -->  Configure  -->  Register  -->  Budget Analysis  -->  Report
```

### Phase 1: Audit Current MCP State

1. Read Claude configs (two locations, merge):
   - `~/.claude.json` (primary, app state)
   - `~/.claude/settings.json` (fallback, user settings)
   - Merge: primary overrides fallback by server name
2. Build table of configured vs missing servers (compare against registry)
3. Check for deprecated servers and flag for removal:

| Deprecated Server | Action |
|-------------------|--------|
| hashline-edit | Remove if found |
| pencil | Remove if found |
| lighthouse | Remove if found |
| playwright | Remove if found |
| browsermcp | Remove if found |

### Phase 2: Configure Missing Servers

For each server in registry not yet configured:

1. IF already configured AND `claude mcp list` shows connected → SKIP
2. IF `dry_run: true` → show planned `claude mcp add` command, do not execute
3. IF **linear** → ask user: "Do you use Linear for task management?" → no → SKIP

### Phase 3: Register via `claude mcp add`

Registration commands by server and source:

| Server | Command |
|--------|---------|
| hex-line (local) | `claude mcp add -s user hex-line -- node {repo}/mcp/hex-line-mcp/server.mjs` |
| hex-line (npm) | `claude mcp add -s user hex-line -- npx -y @levnikolaevich/hex-line-mcp` |
| hex-ssh (local) | `claude mcp add -s user hex-ssh -- node {repo}/mcp/hex-ssh-mcp/server.mjs` |
| hex-ssh (npm) | `claude mcp add -s user hex-ssh -- npx -y @levnikolaevich/hex-ssh-mcp` |
| hex-graph (local) | `claude mcp add -s user hex-graph -- node {repo}/mcp/hex-graph-mcp/server.mjs` |
| context7 | `claude mcp add -s user --transport http context7 https://mcp.context7.com/mcp` |
| Ref | `claude mcp add -s user --transport http Ref https://api.ref.tools/mcp` |
| linear | `claude mcp add -s user --transport http linear-server https://mcp.linear.app/mcp` |

**Post-registration verification:** After each `claude mcp add`, run `claude mcp list` and confirm the server shows connected status. If not connected, report as failed with the error detail.

**Error handling:**

| Error | Response |
|-------|----------|
| `claude` CLI not found | FAIL, report "Claude CLI not in PATH" |
| Server already exists | SKIP, report "already configured" |
| Connection failed after add | WARN, report detail from `claude mcp list` |
| API key missing (Ref) | Prompt user for key, skip if declined |

### Phase 4: Budget Analysis

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

### Phase 5: Report

```
MCP Configuration:
| Server    | Transport | Status        | Detail                  |
|-----------|-----------|---------------|-------------------------|
| hex-line  | stdio     | configured    | local server.mjs        |
| hex-ssh   | stdio     | added         | local server.mjs        |
| context7  | HTTP      | configured    | mcp.context7.com        |
| Ref       | HTTP      | configured    | api.ref.tools (key set) |
| linear    | HTTP      | skipped       | user declined           |

Budget: 4 servers ~ 20K tokens (10.0% of context) — OK
```

---

### Phase 6: Token Efficiency Benchmark

After hex-line is configured, run benchmark on user's repo:

```bash
node mcp/hex-line-mcp/benchmark.mjs
```

Display results to user — demonstrates value of the MCP setup just completed.

Key metrics shown:
- Outline vs full read savings (expect 57-93% on medium-XL files)
- Compact diff savings (expect 32-38% on edits)
- Hash overhead (expect ~0% — negligible)
- Break-even point (typically ~30 lines)

If benchmark shows >50% savings on outline+read → recommend adding hex-line hook for automatic reminders.

---

## Critical Rules

1. **Claude configs are read-only.** Use `claude mcp add` CLI to register servers. Never write directly to Claude JSON files
2. **Verify after add.** Always run `claude mcp list` after registration to confirm connection
3. **Ask before optional servers.** Linear requires explicit user consent
4. **Prefer local source.** For hex-line/hex-ssh, use local `server.mjs` when available
5. **Remove deprecated servers.** Clean up servers no longer in the registry
6. **Idempotent.** Safe to run multiple times. Already-configured servers are skipped

## Anti-Patterns

| DON'T | DO |
|-------|-----|
| Write directly to `~/.claude.json` | Use `claude mcp add` CLI |
| Skip verification after add | Always check `claude mcp list` |
| Auto-add optional servers | Ask user for Linear and other optional servers |
| Ignore budget impact | Always calculate and report token budget |
| Leave deprecated servers | Remove hashline-edit, pencil, etc. |

---

## Definition of Done

- [ ] Current MCP state audited (both Claude config locations)
- [ ] Deprecated servers flagged for removal
- [ ] Missing required servers registered via `claude mcp add`
- [ ] Each registered server verified via `claude mcp list`
- [ ] Token budget calculated and warnings shown if applicable
- [ ] Final status table displayed with all servers
- [ ] Token efficiency benchmark run and results shown to user

---

**Version:** 1.0.0
**Last Updated:** 2026-03-20
