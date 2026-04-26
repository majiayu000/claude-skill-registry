---
name: ln-013-config-syncer
description: "Use when installing or verifying this marketplace in Claude and Codex, aligning selected plugins, MCP settings, and Codex execution defaults."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`) are relative to skills repo root. Locate this SKILL.md directory and go up one level for repo root.

# Marketplace and Config Aligner

**Type:** L3 Worker
**Category:** 0XX Shared

Installs or verifies this repository's marketplace and selected plugins for Claude Code and Codex CLI without making either agent the source of truth for the other. `agile-workflow` is the default development plugin; optional plugins are installed only when explicitly requested or selected. MCP and Codex policy settings are aligned non-destructively after marketplace health is known.

## MANDATORY READ

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md`, `shared/references/environment_worker_runtime_contract.md`, and `shared/references/worker_runtime_contract.md`
**MANDATORY READ:** Load `shared/references/agent_skill_roots_contract.md`

---

## Input / Output

| Direction | Content |
|-----------|---------|
| **Input** | OS info, `disabled` flags per agent, `targets` (`claude` / `codex` / `both` / `all`), `plugins` (`agile-workflow` default, explicit list, or `all`), `dry_run` flag, optional `auto_install_providers` flag, optional `runId`, optional `summaryArtifactPath` |
| **Output** | Structured summary envelope with `payload.status` = `completed` / `skipped` / `error`, plus per-target alignment outcomes in `changes` / `detail` |

If `summaryArtifactPath` is provided, write the same summary JSON there. If not provided, return the summary inline and remain fully standalone. If `runId` is not provided, generate a standalone `run_id` before emitting the summary envelope.

`dry_run=true` is detection-only: do not register marketplaces, install plugins, edit MCP/Codex config, write `.bak` files, or auto-install providers. Return planned actions and drift details in the summary.

## Runtime

Runtime family: `environment-worker-runtime`

Phase profile:
1. `PHASE_0_CONFIG`
2. `PHASE_1_DISCOVER_STATE`
3. `PHASE_2_VERIFY_MARKETPLACE_INSTALLS`
4. `PHASE_3_ALIGN_MCP_SETTINGS`
5. `PHASE_4_ALIGN_CODEX_POLICY`
5a. `PHASE_4A_MCP_PROVIDER_CHECK`
6. `PHASE_5_WRITE_SUMMARY`
7. `PHASE_6_SELF_CHECK`

Runtime rules:
- emit `summary_kind=env-marketplace-align`
- standalone runs generate their own `run_id` and write the default worker-family artifact path
- managed runs require both `runId` and `summaryArtifactPath` and must write the summary to the exact provided path
- always write the validated summary artifact before terminal outcome

## Output Contract

Always build a structured `env-marketplace-align` summary envelope per:
- `shared/references/coordinator_summary_contract.md`
- `shared/references/environment_worker_runtime_contract.md`

Payload fields:
- `targets`
- `plugin_alignment`
- `marketplace_health`
- `mcp_alignment`
- `mcp_providers`
- `codex_execution_defaults`
- `status`

---

## Config Paths by OS

| Agent | Windows | macOS / Linux |
|-------|---------|---------------|
| **Claude** (primary) | `%USERPROFILE%\.claude.json` | `~/.claude.json` |
| **Claude** (fallback) | `%USERPROFILE%\.claude\settings.json` | `~/.claude/settings.json` |
| **Codex** | `%USERPROFILE%\.codex\config.toml` | `~/.codex/config.toml` |

---

## Workflow

```text
Discover State -> Verify Marketplace Installs -> Align MCP -> Align Codex Policy -> Verify & Report
```

### Phase 1: Discover State

1. Read Claude settings:
   - `~/.claude.json` (primary) + `~/.claude/settings.json` (fallback)
   - extract `mcpServers`, enabled marketplaces/plugins, and hook state
2. Read Codex config:
   - `~/.codex/config.toml`
   - extract `[mcp_servers.*]`, `[marketplaces.*]`, top-level `approval_policy`, and top-level `sandbox_mode`
3. Inspect repo marketplace surfaces:
   - Claude: `.claude-plugin/marketplace.json`
   - Codex: `.agents/plugins/marketplace.json`
   - Codex plugin manifests: `plugins/*/.codex-plugin/plugin.json`
4. Resolve plugin selection:
   - always include `agile-workflow`
   - if `plugins=all`, include every plugin listed by the marketplace
   - if an explicit list is provided, install `agile-workflow` plus the requested plugins
   - if interactive and optional plugins are not specified, ask which optional plugins to install
   - if non-interactive and optional plugins are not specified, install or verify only `agile-workflow`
5. Display current state table with enabled targets, selected plugins, marketplace health, duplicate-risk findings, and Codex execution-default drift.

### Phase 2: Verify Marketplace Installs

For each target where `disabled` is not `true`:

| Target | Expected install model | Verification |
|--------|------------------------|--------------|
| Claude | Native Claude marketplace | Marketplace is registered through Claude plugin settings and selected plugins resolve from `.claude-plugin/marketplace.json` |
| Codex | Native Codex marketplace | Marketplace is registered through Codex plugin settings and selected plugins resolve from `.agents/plugins/marketplace.json` / `plugins/*/.codex-plugin/plugin.json` |

Install policy:
- Claude marketplace: `/plugin marketplace add levnikolaevich/claude-code-skills`
- Claude plugin: `/plugin install {plugin}@levnikolaevich-skills-marketplace`
- Codex marketplace: `codex plugin marketplace add levnikolaevich/claude-code-skills`
- Codex plugin selection: verify selected plugins exist in `.agents/plugins/marketplace.json` and `plugins/{plugin}/.codex-plugin/plugin.json`; if the installed Codex version exposes plugin-level selection only through an interactive native flow, report that exact step instead of fabricating a non-existent CLI command

Rules:
- If `dry_run=true`, do not run marketplace add/install commands; report the exact commands that would run.
- Do not symlink or junction Claude plugin roots into Codex discovery roots.
- Do not expose both the Claude bridge surface and Codex native surface to the same Codex runtime at once; duplicate skill names are an alignment failure.
- Do not delete user plugin roots. If duplicate active roots are detected, report the exact paths and ask for explicit cleanup approval.
- Do not install optional plugins silently.
- Run `node skills-catalog/shared/scripts/marketplace/sync-codex-adapters.mjs validate` when the repo root is available. Report failure as marketplace drift.

### Phase 3: Align MCP Settings

MCP settings are aligned by server name. No target is the universal source of truth.

Merge strategy:
1. Build a union of Claude `mcpServers` and Codex `[mcp_servers.*]`.
2. For matching names, preserve target-only fields and update only fields that are semantically equivalent.
3. For missing servers, add them to the requested target after format conversion.
4. Create `.bak` before modifying any config file.
5. Preserve target-only servers and unrelated config sections.
6. If `dry_run=true`, report the merge plan only; do not create `.bak` files or edit config.

Field mapping:

| Semantic field | Claude JSON | Codex TOML |
|---|---|---|
| command | `command` | `command` |
| args | `args` | `args` |
| env | `env` | `[mcp_servers.{name}.env]` |
| HTTP URL | `type: "http"` + `url` | `url` |
| headers | `headers` | `http_headers` |

Codex-only fields to preserve:
`bearer_token_env_var`, `enabled_tools`, `disabled_tools`, `startup_timeout_sec`, `tool_timeout_sec`, `enabled`, `required`

**Windows implementation note:** Config format conversions with regex or backslash escaping MUST use a temporary `.mjs` script file, not inline `node -e` or bash heredocs.

### Phase 4: Align Hooks and Codex Policy

**Claude hooks:**
- Claude hook/style sync remains Claude-only.
- Do not project Claude hooks into Codex.

**Codex execution defaults:**

Managed Codex defaults for low-friction setup:

```toml
approval_policy = "never"
sandbox_mode = "danger-full-access"
```

Decision logic:

| Condition | Action |
|-----------|--------|
| Codex target `disabled: true` | SKIP, report `disabled` |
| defaults already present | SKIP, report `already aligned` |
| one or both keys missing/drifted | Patch only top-level managed keys, preserve unrelated keys/tables, create `.bak` first |

Rules:
- Manage only top-level `approval_policy` and top-level `sandbox_mode`.
- Do not rewrite `[windows].sandbox`; it is a different Windows-specific knob.
- Preserve unrelated Codex config sections such as `model`, `projects`, `notice`, `[marketplaces.*]`, and `[mcp_servers.*]`.

### Phase 4a: MCP Provider Check

**MANDATORY READ:** Load `references/mcp_provider_requirements.md`.

Runs once per project invocation after MCP alignment. Goal: ensure every MCP server referenced in any aligned config has its language-analyzer providers available for the languages the project actually uses.

1. **Enumerate MCP servers.** Union of MCP servers across Claude and Codex configs. Deduplicate by name.
2. **Detect project languages.** Probe in order, cheapest first: `pyproject.toml`, `package.json`, `tsconfig.json`, `Cargo.toml`, `go.mod`, `*.csproj`. Use `mcp__hex-line__inspect_path` to probe; do not shell out.
3. **Look up provider requirements.** Read `references/mcp_provider_requirements.md`. For `hex-graph`, delegate to `mcp__hex-graph__install_graph_providers`.
4. **Run provider check.** Call `mcp__hex-graph__install_graph_providers({ mode: "check", path: <project_root> })`. Do NOT auto-install unless `auto_install_providers=true`.
5. **Record result.** Write into `environment_state.json` under `mcp_providers`.

### Phase 5: Verify & Report

Verify:
- Claude marketplace registration resolves the expected source
- Codex marketplace registration resolves the expected source
- Codex native adapters validate against the Claude marketplace
- No duplicate active Codex skill surfaces point to this repo
- Codex `approval_policy = "never"`
- Codex `sandbox_mode = "danger-full-access"`
- MCP targets were merged without deleting target-only settings

```text
Marketplace and Config Alignment:
| Action         | Target | Status                                              |
|----------------|--------|-----------------------------------------------------|
| Marketplace    | Claude | registered; agile-workflow installed               |
| Marketplace    | Codex  | registered; native adapters validated              |
| MCP align      | Claude | 4 servers aligned (0 deleted)                       |
| MCP align      | Codex  | 4 servers aligned (1 new)                           |
| Execution mode | Codex  | approval_policy=never; sandbox_mode=danger-full-access |
| Hooks          | Codex  | skipped (not supported)                             |
```

---

## Critical Rules

1. **Independent installs.** Claude and Codex install skills through their own native marketplace flows.
2. **No agent is the source of truth for another agent's skill installs.**
3. **Default plugin set.** `agile-workflow` is installed or verified by default because it contains the development workflow.
4. **Optional plugins are explicit.** Install non-default plugins only when requested, selected, or `plugins=all`.
5. **No project command copying.** Do not copy `.claude/commands` into Codex; project-local commands are host-specific unless represented as marketplace skills/plugins.
6. **Non-destructive merge.** Target-only servers and settings are preserved.
7. **No duplicate active surfaces.** One runtime must not see the same skill names from both bridge and native adapter roots.
8. **No data loss.** Real directories at target paths -> warn and skip, never delete blindly.
9. **Backup before write.** Create `.bak` before modifying any config file.
10. **Dry run is read-only.** `dry_run=true` reports planned commands and config changes without mutating user or repo-tracked state.
11. **Respect `disabled` flags.** Skip all operations for disabled agents.
12. **Idempotent.** Safe to run multiple times. Already-aligned state is skipped.
13. **Claude and Codex only.** Do not add unrelated agent branches.

## Anti-Patterns

| DON'T | DO |
|-------|-----|
| Treat Claude as Codex source of truth | Install each agent independently |
| Symlink `.codex/skills` to `.claude/plugins` | Use Codex native marketplace registration |
| Expose both bridge and native Codex surfaces at once | Keep exactly one active Codex install surface |
| Install every marketplace plugin by default | Install `agile-workflow` by default and require explicit selection for the rest |
| Copy project-local `.claude/commands` to Codex | Represent reusable behavior as marketplace skills/plugins |
| Overwrite target config from scratch | Read -> deep-merge -> backup -> edit |
| Delete plugin/cache directories automatically | Report exact cleanup steps and require explicit approval |

---

## Definition of Done

- [ ] Claude and Codex target configs discovered
- [ ] Marketplace registrations verified or installed per target
- [ ] `agile-workflow` verified or installed for enabled targets
- [ ] Optional plugins installed only when explicitly requested or selected
- [ ] `dry_run=true` performed no marketplace, plugin, config, backup, or provider mutations
- [ ] Skill install surfaces verified without duplicate active roots
- [ ] Codex native adapters validated
- [ ] MCP settings aligned without deleting target-only settings
- [ ] Codex execution defaults aligned or explicitly reported as drift
- [ ] Hooks handled only for supported targets
- [ ] MCP provider check completed or explicitly skipped
- [ ] Structured summary returned
- [ ] Summary artifact written to the managed or standalone runtime path

---

**Version:** 2.0.0
**Last Updated:** 2026-04-14
