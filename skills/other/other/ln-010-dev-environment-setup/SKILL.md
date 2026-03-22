---
name: ln-010-dev-environment-setup
description: "Scans, installs, and configures dev environment: CLI agents, MCP servers, config sync, hooks. Use after setup or when agents/MCP need alignment."
disable-model-invocation: true
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/{path}`.

# Dev Environment Setup

**Type:** L2 Domain Coordinator
**Category:** 0XX Shared

Single-pass coordinator that scans, installs, and configures the full agent development environment: CLI agents, MCP servers, config sync across agents, hooks, and best practices audit. Delegates to 4 specialized workers.

## When to Use This Skill

- First-time project setup (no `docs/environment_state.json`)
- After installing/removing CLI agents (Codex, Gemini)
- After adding/removing MCP servers in Claude Code
- When hooks need reconfiguration or verification
- Periodic alignment check across all agents

## Input Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| targets | No | both | `gemini`, `codex`, or `both` |
| dry_run | No | false | Show planned actions without executing |

## Workflow

```
OS Detect → Full Scan → Delegate Workers → Best Practices Audit → Write State + Report
```

### Phase 0: OS & Environment Detection

| Check | Command | Result |
|-------|---------|--------|
| OS | `uname` or platform | win32 / darwin / linux |
| Home | `$HOME` or `$USERPROFILE` | Config root |
| Node | `node --version` | Required for hooks/MCP |
| npm | `npm --version` | Required for agent install |

**Config paths by OS:**

| Agent | Windows | macOS / Linux |
|-------|---------|---------------|
| **Claude** (primary) | `%USERPROFILE%\.claude.json` | `~/.claude.json` |
| **Claude** (fallback) | `%USERPROFILE%\.claude\settings.json` | `~/.claude/settings.json` |
| **Gemini** | `%USERPROFILE%\.gemini\settings.json` | `~/.gemini/settings.json` |
| **Codex** | `%USERPROFILE%\.codex\config.toml` | `~/.codex/config.toml` |

**Load disabled flags:** Read `docs/environment_state.json` if exists. Extract `agents.{name}.disabled` for each agent.

### Phase 1: Full Scan

Run all sub-checks before any modifications. Display scan table after.

**1a: Probe CLI Agents**
- `node shared/agents/agent_runner.mjs --health-check` — probes all registered agents
- Parse output: per-agent `available`, `version`
- If agent_runner.mjs not found: set both `available: false`

**1b: Discover MCP Servers**
- Run `claude mcp list` — canonical source of truth for configured servers
- Parse output: server name, transport type (stdio/HTTP), connection status
- Fallback if `claude` CLI unavailable: read `~/.claude.json` + `~/.claude/settings.json`, merge by server name

**1c: MCP Token Budget**
- Formula: `server_count * 5000` tokens
- Context percentage: `estimated_tokens / 200000 * 100`
- Threshold: <=5 servers OK, 6-8 WARN, >8 WARN critical

**1d: Hook Health**

**MANDATORY READ:** Load `shared/references/hook_health_check.md`

- Validate hooks from both locations: `hooks/hooks.json` (plugin) and `.claude/settings.local.json` (project)
- Check JSON syntax, script existence, dependencies

**1e: CLAUDE.md Health**
- Exists in project root
- Line count (<100 recommended)
- No timestamps (breaks prompt cache)
- Has compact instructions section

**1f: Target Agent Configs**
- Per target (Gemini/Codex): config exists, MCP servers count, symlinks state

**Display scan table:**
```
Environment Scan:
| Area          | Status | Detail                        |
|---------------|--------|-------------------------------|
| Codex CLI     | ok     | 0.1.2503                      |
| Gemini CLI    | ok     | 2025.6.15                     |
| MCP servers   | ok     | 5 servers, 25K tokens (12.5%) |
| Hooks         | ok     | 3 events, 3/3 scripts found   |
| CLAUDE.md     | ok     | 85 lines, compact, no TS      |
| Gemini config | drift  | 3/5 servers synced            |
| Codex config  | ok     | 5/5 servers synced            |
```

### Phase 2: Delegate to Workers (sequential, same context)

> **MANDATORY:** All 4 workers MUST be invoked via Skill tool sequentially in this context. DO NOT skip any worker. DO NOT execute worker tasks inline — each worker MUST be invoked via Skill tool.
> Pass scan results as delegation context. If agent `disabled: true`, pass flag so workers skip operations for that agent.

| Step | Worker | Responsibility | Args |
|------|--------|---------------|------|
| 2a | ln-011-agent-installer | Install/update Codex CLI, Gemini CLI, Claude Code | `{OS} {disabled_flags} {dry_run}` |
| 2b | ln-012-mcp-configurator | Configure MCP servers, hooks, output style, permissions, instruction files, token budget | `{OS} {mcp_state} {dry_run}` |
| 2c | ln-013-config-syncer | Sync Claude settings to Gemini/Codex via symlinks & format conversion | `{OS} {disabled_flags} {targets} {dry_run}` |
| 2d | ln-014-agent-instructions-auditor | Audit CLAUDE.md, AGENTS.md, GEMINI.md for quality and consistency | `{instruction_file_list} {dry_run}` |

**Invocation (each step):**
```
Skill(skill: "{worker}", args: "{args}")
```

### Phase 3: Best Practices Audit

Aggregate checks from workers + coordinator's own checks into one table.

| # | Check | Pass | Fail | Source |
|---|-------|------|------|--------|
| 1 | MCP servers <=5 | <=25K tokens | WARN budget exceeded | ln-012 |
| 2 | CLAUDE.md exists | Found | SUGGEST creating | coordinator |
| 3 | CLAUDE.md compact | <100 lines | INFO consider compacting | coordinator |
| 4 | No timestamps in CLAUDE.md | Clean | WARN prompt cache breakage | coordinator |
| 5 | Hooks configured and enabled | All hooks active | WARN missing hooks | coordinator |
| 6 | Project MCP gate | `enableAllProjectMcpServers: false` | WARN security risk | ln-012 |
| 7 | Codex shell isolation | Env inheritance restricted | SUGGEST hardening | coordinator |
| 8 | Gemini auto-compression | `chatCompression` set | SUGGEST enabling | coordinator |
| 9 | Verification tools | test/lint in package.json | INFO missing tooling | coordinator |

### Phase 4: Write State + Report

1. **Read existing** `docs/environment_state.json` (preserve `disabled` flags)
2. **Build new state** validated against `references/environment_state_schema.json`:
   - `scanned_at`: ISO 8601 timestamp
   - `agents`: probe results merged with preserved `disabled`
   - `claude_md`: exists, line_count, has_timestamps, has_compact_instructions
   - `config_sync`: per-target synced status
   - `best_practices`: score and findings
   - **NOT persisted** (scan-time only): MCP servers, MCP budget, hooks — shown in scan table but not written to file (native CC settings are source of truth)
3. **Ensure** `docs/` directory exists
4. **Ensure gitignore:** If inside a git repo (`git rev-parse --git-dir`), check `.gitignore` for `docs/environment_state.json`. If not covered → append:
   ```
   # Machine-specific environment state (generated by ln-010)
   docs/environment_state.json
   ```
5. **Write** `docs/environment_state.json` (2-space indent)
6. **Summary report:**

```
Dev Environment Setup Complete:
| Area          | Result   | Actions Taken               |
|---------------|----------|-----------------------------|
| CLI agents    | ok       | Gemini updated to 2025.6.15 |
| MCP servers   | ok       | 5 configured, budget OK     |
| Config sync   | ok       | Gemini: 2 new, Codex: skip  |
| Hooks         | ok       | output-filter added         |
| Best practices| 9/10     | 1 WARN (see above)          |

State: docs/environment_state.json
```

---

## Worker Invocation (MANDATORY)

| Phase | Worker | Context |
|-------|--------|--------|
| 2a | ln-011-agent-installer | Shared (Skill tool) — install/update CLI agents |
| 2b | ln-012-mcp-configurator | Shared (Skill tool) — MCP servers, permissions, output style |
| 2c | ln-013-config-syncer | Shared (Skill tool) — sync settings to Gemini/Codex |
| 2d | ln-014-agent-instructions-auditor | Shared (Skill tool) — audit instruction files |

**All workers:** Invoke via Skill tool sequentially — workers see coordinator context.

**TodoWrite format (mandatory):**
```
- OS & environment detection (pending)
- Full scan (pending)
- Invoke ln-011-agent-installer (pending)
- Invoke ln-012-mcp-configurator (pending)
- Invoke ln-013-config-syncer (pending)
- Invoke ln-014-agent-instructions-auditor (pending)
- Best practices audit (pending)
- Write state + report (pending)
```


## Critical Rules

| # | Rule | Detail |
|---|------|--------|
| 1 | Claude = source of truth | Read Claude configs as source. Writes ONLY via `claude mcp add`, `setup_hooks()`, and permissions in `settings.json` |
| 2 | Skip disabled agents | If `disabled: true` in environment_state.json, skip ALL operations for that agent |
| 3 | Preserve disabled field | Never overwrite user's `disabled` flags. Detection updates, preference stays |
| 4 | Scan before fix | Always display current state (Phase 1) before any modifications (Phase 2) |
| 5 | Idempotent | Safe to run multiple times. Already-correct state is skipped |
| 6 | Fail gracefully | One worker failure does not block others. Report per-area status independently |

## Anti-Patterns

| DON'T | DO |
|-------|-----|
| Skip Phase 1 scan | Always scan first, then delegate |
| Write arbitrary Claude settings | Only write via `claude mcp add`, `setup_hooks()`, and `permissions.allow[]` |
| Delete disabled flags on rescan | Merge: overwrite detection fields, preserve disabled |
| Block on single worker failure | Continue with remaining workers, report failure |
| Run workers without scan context | Pass Phase 1 results as delegation input |
| Execute worker tasks inline | Invoke workers via Skill tool, never do their work directly |
| Mark worker steps done without Skill invocation | Each worker MUST be invoked via Skill tool |


## Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `execution-orchestrator`. Analyze this session per protocol §7. Output per protocol format.
---

## Definition of Done

- [ ] OS and environment detected (Phase 0)
- [ ] Full scan completed with table displayed (Phase 1)
- [ ] All 4 workers invoked with scan context (Phase 2)
- [ ] Best practices audit table shown with 9 checks (Phase 3)
- [ ] `docs/environment_state.json` written (Phase 4)
- [ ] `docs/environment_state.json` covered in `.gitignore` (or skipped if not a git repo)
- [ ] Existing `disabled` flags preserved across rescan
- [ ] Summary report displayed to user

---
**Version:** 1.0.0
**Last Updated:** 2026-03-20
