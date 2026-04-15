---
name: ln-011-agent-installer
description: "Installs or updates Codex CLI, Gemini CLI, Claude Code, and detects Google Antigravity IDE. Use when CLI agents need installation or update."
license: MIT
model: claude-sonnet-4-6
---

> **Paths:** File paths (`shared/`, `references/`) are relative to skills repo root. Locate this SKILL.md directory and go up one level for repo root.

# Agent Installer

**Type:** L3 Worker
**Category:** 0XX Shared

Installs or updates CLI agents via npm and Claude CLI. Single pass per agent: install then immediately verify.

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md`, `shared/references/environment_worker_runtime_contract.md`, and `shared/references/worker_runtime_contract.md`

---

## Input / Output

| Direction | Content |
|-----------|----------|
| **Input** | OS info, `disabled` flags per agent, `dry_run` flag, optional `runId`, optional `summaryArtifactPath` |
| **Output** | Structured summary envelope with `payload.status` = `completed` / `skipped` / `error`, plus per-agent install outcomes in `changes` / `detail` |

If `summaryArtifactPath` is provided, write the same summary JSON there. If not provided, return the summary inline and remain fully standalone. If `runId` is not provided, generate a standalone `run_id` before emitting the summary envelope.

## Runtime

Runtime family: `environment-worker-runtime`

Phase profile:
1. `PHASE_0_CONFIG`
2. `PHASE_1_INSTALL_VERIFY`
3. `PHASE_2_POST_GEMINI_CONFIG`
4. `PHASE_3_POST_CODEX_SANITY_CHECK`
5. `PHASE_4_WRITE_SUMMARY`
6. `PHASE_5_SELF_CHECK`

Runtime rules:
- emit `summary_kind=env-agent-install`
- standalone runs generate their own `run_id` and write the default worker-family artifact path
- managed runs require both `runId` and `summaryArtifactPath` and must write the summary to the exact provided path
- always write the validated summary artifact before terminal outcome

## Output Contract

Always build a structured `env-agent-install` summary envelope per:
- `shared/references/coordinator_summary_contract.md`
- `shared/references/environment_worker_runtime_contract.md`

Payload fields:
- `targets`
- `agents_processed`
- `agents_skipped`
- `versions`
- `gemini_settings_updated`
- `codex_drift_detected`
- `status`

---

## Agent Registry

| Agent | Install Command | Health Check |
|-------|----------------|---------------|
| Codex | `npm i -g @openai/codex` | `codex --version` |
| Gemini | `npm i -g @google/gemini-cli` | `gemini --version` |
| Claude | `claude update` | `claude --version` |
| Antigravity | _manual install via IDE_ (no CLI) | detect `~/.gemini/antigravity/` directory presence |

---

## Workflow

```
For each agent: Install → Verify → Record
```

### Phase 1: Install & Verify

For each agent in registry, apply first matching rule:

| Condition | Action | Report |
|-----------|--------|--------|
| `disabled: true` | SKIP | "disabled by user" |
| `dry_run: true` | Show planned command | "dry run" |
| npm agent | `npm install -g {pkg}` then `{cmd} --version` | version or error |
| Claude | `claude update` then `claude --version` | version or error |

**Single pass:** install and verify happen atomically per agent. No separate scan phase — the install result IS the state.

**Error handling:**

| Error | Detection | Response |
|-------|-----------|----------|
| npm not in PATH | `npm --version` fails | FAIL gracefully, report "npm not found in PATH" |
| Permission denied | stderr contains "EACCES" | FAIL, suggest `npm install -g --prefix ~/.local {pkg}` |
| Network error | stderr contains "ETIMEDOUT" or "ENETUNREACH" | FAIL, report "network error" |
| Unknown error | Any other non-zero exit | FAIL, include stderr |

**Output table:**

```
Agent Installation:
| Agent  | Action    | Version  | Status |
|--------|-----------|----------|--------|
| Codex  | installed | 0.1.2503 | ok     |
| Gemini | skipped   | -        | disabled by user |
| Claude | updated   | 1.0.30   | ok     |
```

### Phase 2: Post-Install Gemini Configuration

After successful Gemini install/update, merge into `~/.gemini/settings.json`:

1. Read existing file (or `{}` if missing)
2. Deep-merge: set `security.enableConseca` to `false` (preserve all other keys — MCP servers, model, trust, etc.)
3. Write back (2-space indent JSON)
4. **Model** — do NOT pass `-m` flag when invoking Gemini CLI. Auto mode routes to best available model (gemini-3.1-pro / gemini-3-flash).

### Phase 2b: Post-Install Codex Mapping Sanity Check

After successful Codex install/update:

1. Check `~/.codex/skills` for discovery-visible cache (especially `~/.codex/skills/cache/**`)
2. Check `~/.codex/skills/known_marketplaces.json` install locations for foreign paths such as `~/.claude/plugins/...`
3. Check `~/.codex/config.toml` top-level `approval_policy` and `sandbox_mode`
4. If drift is found, report a WARN and defer remediation to `ln-013-config-syncer`

This installer does not relocate Codex cache, rewrite skill mapping, or manage Codex execution defaults. It only reports drift so install success is not mistaken for a healthy Codex environment.

---

## Critical Rules

1. **Never modify `disabled` flags.** Respect them, never change them
2. **Fail gracefully.** One agent failure does not block others
3. **Global install only.** Always `npm install -g` (CLI tools must be in PATH)
4. **Report all changes.** Include config modifications in the final summary table
5. **Idempotent.** Safe to run multiple times
6. **Non-destructive config writes.** Always read → deep-merge → edit. Never overwrite `~/.gemini/settings.json` from scratch — it contains MCP servers, hooks, and user preferences managed by other skills.
7. **Codex mapping and execution-default remediation belongs to ln-013.** This skill may detect Codex skill-root drift or `approval_policy` / `sandbox_mode` drift, but it must not rewrite marketplace/cache layout or Codex top-level permission defaults itself.

## Anti-Patterns

| DON'T | DO |
|-------|-----|
| Separate check/install/verify phases | Single pass: install then verify |
| Retry failed installs automatically | One attempt, report failure |
| Use `sudo npm install` | Suggest `--prefix` for permission issues |
| Install agents marked `disabled` | Skip with clear report |
| Overwrite entire config file with only known fields | Read existing → deep-merge only owned fields → edit back |

---

## Definition of Done

- [ ] All agents processed in single pass (install + verify)
- [ ] Disabled agents skipped with report
- [ ] Version verified immediately after each install
- [ ] Codex mapping and execution-default sanity checked or explicitly reported for ln-013 follow-up
- [ ] Status table displayed
- [ ] Structured summary returned
- [ ] Summary artifact written to the managed or standalone runtime path

---

**Version:** 1.1.0
**Last Updated:** 2026-03-23
