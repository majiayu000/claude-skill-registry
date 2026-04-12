---
name: ln-013-config-syncer
description: "Use when syncing skills, MCP settings, defaults, and hooks from Claude Code to Gemini CLI and Codex CLI with symlink support for Gemini and install-based sync for Codex."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`) are relative to skills repo root. Locate this SKILL.md directory and go up one level for repo root.

# Config Syncer

**Type:** L3 Worker
**Category:** 0XX Shared

Synchronizes skills and MCP/hook settings from Claude Code (source of truth) to Gemini CLI and Codex CLI. Gemini skills are shared via symlink/junction. Codex skills are mapped as active installs under `~/.codex/skills`, with cache kept outside the Codex discovery root. Converts formats: JSON for Gemini, TOML for Codex.

Shared MCP servers still come from Claude. Codex top-level execution defaults are a managed local policy owned by this skill because Claude has no equivalent `approval_policy` / `sandbox_mode` fields.

## MANDATORY READ

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md`, `shared/references/environment_worker_runtime_contract.md`, and `shared/references/worker_runtime_contract.md`
**MANDATORY READ:** Load `shared/references/agent_skill_roots_contract.md`

---

## Input / Output

| Direction | Content |
|-----------|---------|
| **Input** | OS info, `disabled` flags per agent, `targets` (`gemini` / `codex` / `both`), `dry_run` flag, optional `runId`, optional `summaryArtifactPath` |
| **Output** | Structured summary envelope with `payload.status` = `completed` / `skipped` / `error`, plus per-target sync outcomes in `changes` / `detail` |

If `summaryArtifactPath` is provided, write the same summary JSON there. If not provided, return the summary inline and remain fully standalone. If `runId` is not provided, generate a standalone `run_id` before emitting the summary envelope.

## Runtime

Runtime family: `environment-worker-runtime`

Phase profile:
1. `PHASE_0_CONFIG`
2. `PHASE_1_DISCOVER_STATE`
3. `PHASE_2_SYNC_SKILLS_MAPPING`
4. `PHASE_3_SYNC_MCP_SETTINGS`
5. `PHASE_4_SYNC_HOOKS_AND_POLICY`
6. `PHASE_5_WRITE_SUMMARY`
7. `PHASE_6_SELF_CHECK`

Runtime rules:
- emit `summary_kind=env-config-sync`
- standalone runs generate their own `run_id` and write the default worker-family artifact path
- managed runs require both `runId` and `summaryArtifactPath` and must write the summary to the exact provided path
- always write the validated summary artifact before terminal outcome

## Output Contract

Always build a structured `env-config-sync` summary envelope per:
- `shared/references/coordinator_summary_contract.md`
- `shared/references/environment_worker_runtime_contract.md`

Payload fields:
- `targets`
- `skills_mapping`
- `mcp_sync`
- `hook_sync`
- `gemini_policy`
- `codex_execution_defaults`
- `status`

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

```text
Discover State  -->  Sync Skills / Mapping  -->  Sync MCP  -->  Sync Hooks / Policy  -->  Verify & Report
```

### Phase 1: Discover State

1. Read Claude settings (source of truth):
   - `~/.claude.json` (primary) + `~/.claude/settings.json` (fallback)
   - Merge: primary overrides fallback by server name
2. Read target configs (if they exist):
   - Gemini: `~/.gemini/settings.json` → extract `mcpServers`
   - Codex: `~/.codex/config.toml` → extract `[mcp_servers.*]`, top-level `approval_policy`, and top-level `sandbox_mode`
3. Inspect skill roots:
   - Gemini skill link: `~/.gemini/skills`
   - Codex discovery root: `~/.codex/skills`
   - Codex active marketplaces: `~/.codex/skills/marketplaces/*`
   - Codex illegal cache path: `~/.codex/skills/cache/**`
   - Codex cache root candidates outside discovery: `~/.codex/skill-cache/*`
   - Codex marketplace metadata: `~/.codex/skills/known_marketplaces.json`
4. Detect duplicate skill directory names under the Codex discovery root
5. Display current state table with active roots, cache roots, duplicate-risk findings, and Codex execution-default drift

### Phase 2: Sync Skills / Mapping

For each target where `disabled` is not `true`:

**2a: Gemini skill link**

| OS | Command |
|----|---------|
| Windows | `node -e "require('fs').symlinkSync('{source}', '{target}', 'junction')"` |
| macOS/Linux | `ln -s "{source}" "{target}"` |

Gemini decision logic:

| Condition | Action |
|-----------|--------|
| `disabled: true` for this agent | SKIP, report `disabled` |
| Link exists, points correctly | SKIP, report `already linked` |
| Link exists, points wrong | WARN, ask user before replacing |
| Real directory exists (not link) | WARN, skip (avoid data loss) |
| No link exists | Create link |
| Link exists, target does not exist (stale) | WARN `stale junction: {path} -> {dead_target}`. Remove stale link, recreate with correct target |

**Stale junction detection:** Use `lstatSync()` (succeeds on dangling links) + `statSync()` (throws if target missing). Do NOT rely on `existsSync()` alone.

**2b: Codex active install mapping**

**Target structure:**

```text
~/.codex/skills/                                    <- real directory (NOT a junction)
  marketplaces/
      {marketplace-A}/                              <- junction -> ~/.claude/plugins/marketplaces/{marketplace-A}
      {marketplace-B}/                              <- junction -> ~/.claude/plugins/marketplaces/{marketplace-B}
  known_marketplaces.json                           <- installLocation -> ~/.codex/skills/marketplaces/{marketplace}
```

Per-marketplace junctions preserve auto-update: when Claude updates a marketplace, Codex sees changes automatically through the junction. Cache and other non-skill directories are excluded from the Codex discovery root.

Codex decision logic:

| Condition | Action |
|-----------|--------|
| `disabled: true` for this agent | SKIP, report `disabled` |
| `~/.codex/skills` is a junction/symlink to `~/.claude/plugins` (whole-root) | Replace with real directory + per-marketplace junctions (see steps below) |
| `~/.codex/skills/cache/**` exists | Relocate cache outside the discovery root (or report the planned move on `dry_run`) |
| `known_marketplaces.json` points to `~/.claude/plugins/...` or another foreign root | Rewrite `installLocation` to the active Codex marketplace path (`~/.codex/skills/marketplaces/{marketplace}`) |
| Active marketplace exists under `~/.codex/skills/marketplaces/{marketplace}` as junction and duplicate scan is clean | SKIP, report `already mapped` |
| Active marketplace missing but an approved source exists | Create junction `~/.codex/skills/marketplaces/{marketplace}` -> `~/.claude/plugins/marketplaces/{marketplace}` |
| Duplicate skill names remain under `~/.codex/skills` after relocation / repair | FAIL sync health, report discovery violation |

**Whole-root junction detection:** Use `fs.lstatSync('~/.codex/skills').isSymbolicLink()`. If true and `fs.readlinkSync()` points to `~/.claude/plugins`, this is a whole-root junction that must be replaced.

**Steps for whole-root junction replacement (Windows):**

1. Backup `known_marketplaces.json` content (read before removing junction)
2. Remove junction: `execSync('rmdir "<path>"', { shell: 'cmd.exe' })` -- safe for junctions, does not delete target
3. Create real directory: `fs.mkdirSync('<path>', { recursive: true })`
4. Create `<path>/marketplaces/`
5. For each enabled marketplace in `~/.claude/settings.json` -> `enabledPlugins`:
   - Create junction: `fs.symlinkSync('<claude_marketplace_path>', '<codex_marketplace_path>', 'junction')`
6. Write `known_marketplaces.json` with `installLocation` pointing to the Codex-local marketplace path
7. Verify: no `cache/`, junctions resolve, duplicate scan clean

**Steps for whole-root junction replacement (macOS/Linux):**

1. Backup `known_marketplaces.json` content
2. Remove symlink: `rm ~/.codex/skills` (not `rm -rf` -- symlink only)
3. Create real directory: `mkdir -p ~/.codex/skills/marketplaces`
4. For each enabled marketplace: `ln -s ~/.claude/plugins/marketplaces/{mp} ~/.codex/skills/marketplaces/{mp}`
5. Write `known_marketplaces.json` with Codex-local `installLocation`

**Implementation note:** On Windows, use a temporary `.mjs` script file for the junction replacement sequence, not inline `node -e` or bash heredocs, because Windows path escaping is fragile in shells.

Rules for Codex mapping:
- Never symlink or junction `~/.codex/skills` itself to the Claude plugin tree.
- Never expose cache snapshots under the Codex discovery root.
- `known_marketplaces.json` is part of the Codex mapping contract and must agree with the active marketplace path.
- A marketplace-level junction is the preferred mapping strategy. A whole-root mirror of `.claude/plugins` is not acceptable.
- Per-marketplace junctions auto-update when Claude updates marketplaces -- no manual re-sync needed.

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
| `headers` | `http_headers` | Different key name |

Codex-only fields (preserve during merge, not mapped from Claude):
`bearer_token_env_var`, `enabled_tools`, `disabled_tools`, `startup_timeout_sec`, `tool_timeout_sec`, `enabled`, `required`

**Merge strategy (both targets):** Claude servers override target by key name. Target-only servers are preserved. Backup `.bak` before writing.

**Windows implementation note:** Config format conversions with regex or backslash escaping (especially JSON → TOML for Codex) MUST use a temporary `.mjs` script file, not inline `node -e` or bash heredocs.

### Phase 4: Sync Hooks / Policy

**4a: Claude to Gemini (event name + tool name mapping)**

| Claude Event | Gemini Event | Notes |
|---|---|---|
| `PreToolUse` | `BeforeTool` | Same concept, different name |
| `PostToolUse` | `AfterTool` | Same concept, different name |
| `Stop` | `AfterAgent` | Agent completion |
| `SessionStart` | `SessionStart` | Same name |

Tool name mapping in hook matchers:

| Claude Tool Name | Gemini Tool Name(s) |
|---|---|
| `Read` | `read_file` |
| `Edit` | `replace` (legacy alias: `edit`) |
| `Write` | `write_file` |
| `Grep` | `search_file_content` |
| `Glob` | `glob` |

Hook scripts must support both tool name formats. Prefer current Gemini snake_case names in generated config, but tolerate legacy aliases where encountered during migration.

**4b: Codex execution defaults**

Managed Codex defaults for this environment setup flow:

```toml
approval_policy = "never"
sandbox_mode = "danger-full-access"
```

Decision logic:

| Condition | Action |
|-----------|--------|
| Codex target `disabled: true` | SKIP, report `disabled` |
| `approval_policy = "never"` and `sandbox_mode = "danger-full-access"` already present | SKIP, report `already aligned` |
| One or both keys are missing or drifted | Patch only the top-level managed keys, preserve all unrelated top-level keys/tables, create `.bak` first |

Rules for Codex execution defaults:
- Manage only top-level `approval_policy` and top-level `sandbox_mode`.
- Do not rewrite `[windows].sandbox` when aligning Codex full-access defaults. It is a different Windows-specific knob.
- Preserve unrelated Codex config sections such as `model`, `projects`, `notice`, and `[mcp_servers.*]`.

**4c: Claude to Codex**

Codex does NOT support hooks. SKIP hook sync for Codex. Report `hooks not supported by Codex CLI`.

**4d: Gemini MCP Policy**

Gemini CLI policy engine blocks MCP tool calls by default (error: `Tool execution denied by policy`) even with `--yolo`. Fix: ensure `~/.gemini/policies/allow-mcp.toml` exists.

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

### Phase 5: Verify & Report

Verify:
- Gemini skill link points to the expected active source
- Codex discovery root contains no `cache/**`
- Codex `known_marketplaces.json` points to the active Codex marketplace path
- Duplicate skill scan under `~/.codex/skills` is clean
- Codex `approval_policy` = `never`
- Codex `sandbox_mode` = `danger-full-access`
- MCP targets were merged without deleting target-only settings

```text
Config Sync:
| Action         | Target | Status                                              |
|----------------|--------|-----------------------------------------------------|
| Skills symlink | Gemini | created -> ~/.claude/plugins                        |
| Skills mapping | Codex  | cache relocated; active install verified            |
| MCP sync       | Gemini | 4 servers synced (2 new)                            |
| MCP sync       | Codex  | 4 servers synced (1 new)                            |
| Execution mode | Codex  | approval_policy=never; sandbox_mode=danger-full-access |
| Hooks sync     | Gemini | 3 events synced                                     |
| Hooks sync     | Codex  | skipped (not supported)                             |
| MCP policy     | Gemini | allow-mcp.toml created                              |
| Discovery root | Codex  | clean (0 duplicate skill names)                     |
```

---

## Critical Rules

1. **Claude = source of truth.** Never write TO Claude settings. Read-only source
2. **Non-destructive merge.** Target-only servers and settings preserved. Only Claude servers added/updated
3. **Gemini and Codex do not share the same skill mapping model.** Gemini may use a symlink/junction; Codex must use active installs plus cache outside the discovery root
4. **Codex cache must stay outside `~/.codex/skills`.** `~/.codex/skills/cache/**` is always drift
5. **No data loss.** Real directories at target paths -> warn and skip, never delete blindly
6. **Backup before write.** Create `.bak` copy before modifying any config file
7. **Respect `disabled` flags.** Skip all operations for disabled agents
8. **Idempotent.** Safe to run multiple times. Already-synced state is skipped
9. **Non-destructive config writes.** Always read -> deep-merge -> edit. Never overwrite target config files from scratch. Preserve all keys not mapped from Claude
10. **Codex execution defaults are managed policy.** Keep `approval_policy=never` and `sandbox_mode=danger-full-access` unless the user explicitly requests a different Codex default
11. **Do not confuse top-level `sandbox_mode` with `[windows].sandbox`.** Full-access startup is controlled by the top-level key

## Anti-Patterns

| DON'T | DO |
|-------|-----|
| Write TO Claude settings from targets | Claude is read-only source |
| Delete target-only MCP servers during sync | Preserve target-only servers |
| Create symlinks inside symlinks (circular) | Check link target before creating |
| Modify config files without backup | Always create `.bak` first |
| Try to sync hooks to Codex | Report `not supported`, skip |
| Map `~/.codex/skills` to `~/.claude/plugins` | Repair only the Codex active marketplace surface |
| Treat `~/.codex/skills/cache/**` as harmless | Relocate it outside the discovery root and re-scan |
| Count every cache snapshot as a real Codex skill | Scan only the active Codex discovery root after remediation |
| Treat `[windows].sandbox` as the Codex full-access default | Manage top-level `sandbox_mode` instead |
| Rewrite `~/.codex/config.toml` from scratch to fix permission drift | Patch only `approval_policy` / `sandbox_mode` and preserve the rest |
| Auto-replace mispointed links without warning | Ask user before replacing |
| Overwrite entire config file with only known fields | Read existing -> deep-merge only owned fields -> edit back |

---

## Definition of Done

- [ ] Claude settings read successfully (both config locations)
- [ ] Gemini skill link created/verified for each non-disabled target
- [ ] Codex active install mapping repaired or verified, with cache outside `~/.codex/skills`
- [ ] MCP settings synced with correct format conversion (JSON for Gemini, TOML for Codex)
- [ ] Codex execution defaults aligned to `approval_policy=never` and `sandbox_mode=danger-full-access`
- [ ] Hook events and tool names mapped for Gemini
- [ ] Codex hooks skipped with report
- [ ] Gemini MCP policy file verified/created
- [ ] Codex duplicate-skill scan is clean or explicitly reported as drift
- [ ] Backup files created before any config modification
- [ ] Final report table displayed
- [ ] Structured summary returned
- [ ] Summary artifact written to the managed or standalone runtime path

---

**Version:** 1.1.0
**Last Updated:** 2026-04-05
