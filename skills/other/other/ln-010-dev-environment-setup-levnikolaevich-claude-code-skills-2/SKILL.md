---
name: ln-010-dev-environment-setup
description: "Installs agents, configures MCP servers, syncs configs, creates and audits instructions. Use after setup or when agents/MCP need alignment."
disable-model-invocation: true
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Dev Environment Setup

**Type:** L2 Domain Coordinator
**Category:** 0XX Shared

Assess-Dispatch-Verify coordinator. Probes entire environment once, builds dispatch plan, invokes only workers that have work to do, then verifies everything. **Runs all phases in one uninterrupted pass.**

## When to Use This Skill

- First-time project setup (no `.hex-skills/environment_state.json`)
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
Detect → Assess → Dispatch → Verify & Report
```

### Phase 0: Environment Detection

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

**Load disabled flags:** Read `.hex-skills/environment_state.json` if exists. Extract `agents.{name}.disabled` for each agent.

### Phase 1: ASSESS (all probes, one pass, read-only)

Single pass that collects the full environment state. No mutations — read-only probes.

**1a: CLI Agent Probes**

For each non-disabled agent, run `{agent} --version`:

| Agent | Command | Captures |
|-------|---------|----------|
| Codex | `codex --version` | available, version |
| Gemini | `gemini --version` | available, version |
| Claude | `claude --version` | available, version |

Skip disabled agents. Record "not found" for missing agents.

**1b: MCP Server Probes**

One `claude mcp list` call. Parse into map per server: `registered`, `connected`.

For each registered hex package:
1. `npm view @levnikolaevich/{pkg} version` — registry latest
2. npx cache scan: find `{cacheRoot}/_npx/**/node_modules/@levnikolaevich/{pkg}/package.json` — cached version
3. Compare: registry > cached → `outdated: true`. Cache miss → `outdated: unknown` (treat as needs-refresh).

Note: hex packages run via `npx -y`, NOT global install. Never use `npm outdated -g`.

Detect deprecated servers (from ln-012 deprecated list in its SKILL.md).

**1c: Hooks & Permissions Probe**

Read `~/.claude/settings.json` (or `settings.local.json`):
- Hooks present? (PreToolUse, PostToolUse, SessionStart)
- `disableAllHooks` flag?
- `permissions.allow[]` — which `mcp__*` entries present?

**MANDATORY READ:** Load `shared/references/hook_health_check.md` — run script existence + dependency checks.

**1d: Config Sync Probe**

For each non-disabled target agent:
- Check symlink status (`~/.gemini/skills`, `~/.codex/skills`)
- Read target config — compare MCP servers against Claude source
- Check hook mappings (Gemini only)

**1e: Instruction Files Probe**

Check existence of: `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` in project root.

For each existing file: line count, estimated tokens, has timestamps, has compact instructions, has MCP Tool Preferences table.

**1f: Output Style Probe**

- Check `~/.claude/output-styles/hex-line.md` exists
- Read `~/.claude/settings.json` -> `outputStyle` field
- If installed file exists: compare `Last Updated:` line vs source in hex-line-mcp package

| Condition | Status |
|-----------|---------|
| File exists + outputStyle = "hex-line" + current | OK |
| File exists + outputStyle differs | INFO -- user has custom style |
| File missing + hex-line MCP registered | WARN -- output style not installed |
| File outdated (source newer) | WARN -- output style outdated |

**Assessment Summary Table:**

```
Environment Assessment:
| Area               | Status | Detail                              |
|--------------------|--------|-------------------------------------|
| CLI Agents         | 2/3 ok | codex: not found                    |
| MCP Servers        | 5 conn | hex-line outdated (1.3.5 → 1.3.6)  |
| Hooks              | ok     | 3/3 configured                      |
| Permissions        | 4/5    | mcp__hex-ssh missing                |
| Config Sync        | gemini | codex: symlink missing              |
| Instruction Files  | 1/3    | AGENTS.md, GEMINI.md missing        |
| Output Style       | ok     | hex-line active, current            |
```

### Phase 2: DISPATCH (selective invocation)

**2a: Decision Matrix**

| Worker | SKIP when | RUN when |
|--------|-----------|----------|
| ln-011 | All agents: (available) OR (disabled) | Any agent: not available AND not disabled |
| ln-012 | All servers connected + not outdated AND permissions complete AND no deprecated AND output style OK | Any: missing/disconnected/outdated server, permissions missing, deprecated found, output style missing/outdated |
| ln-013 | All targets: (disabled) OR (linked + synced) | Any non-disabled target: not linked OR servers not synced |
| ln-014 | All instruction files exist AND quality OK (no timestamps, has compact, has MCP prefs) | Any file missing OR quality issues |

**2b: Dispatch Plan**

Display the plan before invoking:

```
Dispatch Plan:
| Worker | Action | Reason                           |
|--------|--------|----------------------------------|
| ln-011 | RUN    | codex not installed               |
| ln-012 | SKIP   | all servers connected, permissions ok |
| ln-013 | RUN    | codex symlink missing             |
| ln-014 | RUN    | AGENTS.md, GEMINI.md missing      |
```

**2c: Fast Path** — if ALL workers SKIP → go directly to Phase 3 with message: "All green — no workers needed."

**2d: Invoke** (sequential, no stops between invocations):

```
For each worker where action == RUN:
  Skill(skill: "{worker}", args: "{OS} {disabled_flags} {dry_run}")
```

Workers check their own zone and fix what's needed. ln-010 does NOT tell them what to do — only decides whether to call them.

### Phase 3: VERIFY & REPORT

Full verification after workers complete. This is the **acceptance check** — confirms everything is correct.

**3a: Verify CLI Agents**
- `codex --version`, `gemini --version`, `claude --version` for each non-disabled agent
- Record: available, version
- Compare Phase 3a versions against Phase 1a versions
- If any version changed during the session: INFO "Agent {name} updated from {v1} to {v2} during setup"

**3b: Verify MCP Servers**
- `claude mcp list` → verify all registered servers `Connected`
- Token budget: `server_count * 5000` tokens (% of 200K context)

| Server Count | Level | Message |
|--------------|-------|---------|
| 1-5 | OK | "Budget within limits" |
| 6-8 | WARN | "Consider disabling unused MCP servers" |
| >8 | WARN | "Significant context impact" |

**3c: Verify & Refresh Hooks**

**Step 1:** Always call `mcp__hex-line__setup_hooks(agent="all")` (idempotent).
This ensures hook.mjs and output-style.md are always current, even when ln-012 is skipped.
Verify response contains `Hooks configured for`. If error → report FAIL, continue.

**Step 2:** **MANDATORY READ:** Load `shared/references/hook_health_check.md`

- Validate hooks from `hooks/hooks.json` (plugin) and `.claude/settings.local.json` (project)
- Check JSON syntax, script existence, dependencies

**3d: Verify Instruction Files**
- Exists in project root
- Line count (<100 recommended)
- No timestamps (breaks prompt cache)
- Has compact instructions section

**3e: Best Practices Audit**

| # | Check | Pass | Fail | Auto-fix |
|---|-------|------|------|----------|
| 1 | MCP servers <=5 | <=25K tokens | WARN budget exceeded | — (user decides) |
| 2 | CLAUDE.md exists | Found | Created by ln-014 | — |
| 3 | CLAUDE.md compact | <100 lines | INFO consider compacting | — (user decides) |
| 4 | No timestamps | Clean | FIX: remove lines matching `\d{4}-\d{2}-\d{2}.\d{2}:\d{2}` and standalone `Last Updated: {date}` | auto |
| 5 | Hooks configured | All hooks active | Fixed by Phase 3c | setup_hooks already called |
| 6 | Project MCP gate | `enableAllProjectMcpServers: false` | FIX: set to false in settings.json | auto |
| 7 | Codex shell isolation | Env restricted | SUGGEST | — (user decides) |
| 8 | Gemini auto-compression | `chatCompression` set | SUGGEST | — (user decides) |
| 9 | Verification tools | test/lint found | INFO | — |
| 10 | Output style installed | hex-line active | Fixed by Phase 3c | setup_hooks already called |

**Auto-fix policy:** Checks marked "FIX" are applied automatically (unless `dry_run: true`). Checks marked "Fixed by Phase 3c" are resolved by the setup_hooks call. Remaining WARN/INFO/SUGGEST require user action.

**3f: Write State**

1. **Read existing** `.hex-skills/environment_state.json` (preserve `disabled` flags)
2. **Build new state** validated against `references/environment_state_schema.json`:
   - `scanned_at`: ISO 8601 timestamp
   - `agents`: probe results merged with preserved `disabled`, plus config sync data per agent
   - `claude_md`: exists, line_count, has_timestamps, has_compact_instructions
   - `best_practices`: score and findings
   - `last_assessment`: dispatch plan outcome (workers_run, workers_skipped)
   - `hooks`: object with `mode` field (`"blocking"` or `"advisory"`, default `"blocking"`). Read by hook.mjs at runtime
   - **NOT persisted** (verify-time only): MCP servers, MCP budget — shown in report but not written to file (native CC settings are source of truth)
3. **Migrate legacy paths** (idempotent — skips if already migrated):
   ```
   mkdir -p .hex-skills

   FOR each {old, new} IN:
     .agent-review/              -> .hex-skills/agent-review/
     .codegraph/                 -> .hex-skills/codegraph/
     .pipeline/                  -> .hex-skills/pipeline/
     .worktrees/                 -> .hex-skills/worktrees/
     .optimization/              -> .hex-skills/optimization/
     docs/environment_state.json -> .hex-skills/environment_state.json
   IF old exists AND new does NOT exist: mv old new

   # .codegraph/ migration note: hex-graph-mcp >= 0.4.0 already writes to .hex-skills/codegraph/.
   # Old .codegraph/ may be locked by a running MCP process from an older version.
   # IF mv fails (EBUSY/locked): skip, WARN "restart Claude Code first, then re-run ln-010".
   # After restart the new hex-graph process writes to .hex-skills/codegraph/ and old .codegraph/ is stale.

   Clean .gitignore (line-by-line, surgical removal):
     Remove ONLY lines that EXACTLY match these legacy patterns:
       /.codegraph
       /.agent-review
       /.pipeline
       /.worktrees
       /.optimization
       docs/environment_state.json
     Method: grep -v with exact match, or mcp__hex-line__edit_file with set_line per line.
     NEVER use replace_between on .gitignore -- risk of deleting adjacent unrelated entries.
     After removal: verify no unrelated lines were affected (read file, compare line count).
   ```
4. **Ensure gitignore:** If `.hex-skills/` not in `.gitignore` -> append:
   ```
   # Skill-generated working artifacts (machine-specific)
   .hex-skills/
   ```
5. **Ensure `.hex-skills/.gitignore`** exists (content: `*` + `!.gitignore`)
6. **Write** `.hex-skills/environment_state.json` (2-space indent)

**3g: Summary Report**

```
Dev Environment Setup Complete:
| Area              | Result   | Detail                        |
|-------------------|----------|-------------------------------|
| CLI agents        | ok       | codex installed v0.1.2503     |
| MCP servers       | ok       | 5 configured, budget OK       |
| Config sync       | ok       | codex: symlink + 5 servers    |
| Hooks             | ok       | 3/3 active                    |
| Instructions      | ok       | AGENTS.md, GEMINI.md created  |
| Best practices    | 9/9      | All green                     |

Dispatch: 3 workers run (ln-011, ln-013, ln-014), 1 skipped (ln-012)
State: .hex-skills/environment_state.json
```

**If ANY problems found** → list them explicitly after the table with suggested fix per issue.

---

## Worker Invocation (MANDATORY)

| Phase | Worker | Context |
|-------|--------|--------|
| 2d | ln-011-agent-installer | Shared (Skill tool) — install/update CLI agents |
| 2d | ln-012-mcp-configurator | Shared (Skill tool) — MCP packages, servers, hooks, permissions |
| 2d | ln-013-config-syncer | Shared (Skill tool) — sync settings to Gemini/Codex |
| 2d | ln-014-agent-instructions-manager | Shared (Skill tool) — create missing + audit instruction files |

**All workers:** Invoke via Skill tool. **Do NOT stop or pause between invocations — execute the entire pipeline from Phase 0 to Phase 3 in a single uninterrupted pass.**

**TodoWrite format (mandatory):**
```
- Detect environment (pending)
- Assess: probe all areas (pending)
- Dispatch: build plan + invoke workers (pending)
- Verify & report (pending)
```

## Critical Rules

| # | Rule | Detail |
|---|------|--------|
| 1 | Claude = source of truth | Read Claude configs as source. Writes ONLY via `claude mcp add`, `setup_hooks()`, and permissions in `settings.json` |
| 2 | Skip disabled agents | If `disabled: true` in environment_state.json, skip ALL operations for that agent |
| 3 | Preserve disabled field | Never overwrite user's `disabled` flags. Detection updates, preference stays |
| 4 | Idempotent | Safe to run multiple times. Already-correct state is skipped |
| 5 | Fail gracefully | One worker failure does not block others. Report per-area status independently |
| 6 | Assess before dispatch | All probes run in Phase 1 BEFORE any worker invocation. Workers are called only when assessment shows work to do |
| 7 | Verify after dispatch | Phase 3 runs full verification AFTER workers — this is the acceptance check |
| 8 | Single-pass, no stops | Execute ALL phases (0→3) in one uninterrupted run. Never pause between workers, never ask for confirmation mid-flow |

## Anti-Patterns

| DON'T | DO |
|-------|-----|
| Invoke all workers regardless of state | Assess first, skip workers with nothing to do |
| Duplicate probes across phases | Assess once in Phase 1, verify once in Phase 3 |
| Block on single worker failure | Continue with remaining workers, report failure |
| Execute worker tasks inline | Invoke workers via Skill tool |
| Mark worker steps done without Skill invocation | Each worker MUST be invoked via Skill tool |
| Stop or pause between workers | Execute all phases in one continuous pass |
| Tell workers what to do | Workers check own zone and fix — ln-010 only decides whether to call them |

## Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `execution-orchestrator`. Analyze this session per protocol §7. Output per protocol format.
---

## Definition of Done

- [ ] OS and environment detected (Phase 0)
- [ ] Full assessment completed — all areas probed (Phase 1)
- [ ] Dispatch plan built and displayed (Phase 2)
- [ ] Only needed workers invoked (Phase 2d)
- [ ] Full verification pass completed (Phase 3)
- [ ] Best practices audit table shown with 10 checks (Phase 3e)
- [ ] `.hex-skills/environment_state.json` written with dispatch plan outcome (Phase 3f)
- [ ] `.hex-skills/environment_state.json` covered in `.gitignore`
- [ ] Existing `disabled` flags preserved across rescan
- [ ] Summary report displayed with dispatch outcome and problems listed if any (Phase 3g)

---

**Version:** 2.2.0
**Last Updated:** 2026-03-25
