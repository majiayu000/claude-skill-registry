---
name: ln-011-agent-installer
description: "Installs or updates Codex CLI and Claude Code. Use when CLI agents need installation or update."
license: MIT
model: claude-sonnet-4-6
---

> **Paths:** File paths (`references/`) are relative to this skill directory.

# Agent Installer

**Type:** L3 Worker
**Category:** 0XX Shared

Installs or updates the two supported CLI agents: Codex CLI and Claude Code. Single pass per agent: install then immediately verify.

**MANDATORY READ:** Load `references/coordinator_summary_contract.md`, `references/environment_worker_runtime_contract.md`, and `references/worker_runtime_contract.md`

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
3. `PHASE_2_POST_CODEX_SANITY_CHECK`
4. `PHASE_3_WRITE_SUMMARY`
5. `PHASE_4_SELF_CHECK`

Runtime rules:
- emit `summary_kind=env-agent-install`
- standalone runs generate their own `run_id` and write the default worker-family artifact path
- managed runs require both `runId` and `summaryArtifactPath` and must write the summary to the exact provided path
- always write the validated summary artifact before terminal outcome

## Output Contract

Always build a structured `env-agent-install` summary envelope per:
- `references/coordinator_summary_contract.md`
- `references/environment_worker_runtime_contract.md`

Payload fields:
- `targets`
- `agents_processed`
- `agents_skipped`
- `versions`
- `codex_drift_detected`
- `status`

---

## Agent Registry

| Agent | Install Command | Health Check | Interactive |
|-------|----------------|--------------|-------------|
| Codex | `npm i -g @openai/codex` | `codex --version` | `codex` or `codex "prompt"` |
| Claude | `npm i -g @anthropic-ai/claude-code` or `claude update` | `claude --version` | `claude` or `claude "prompt"` |

Automation uses:
- Codex: `codex exec ...`
- Claude: `claude -p ...`

Note: `codex` / `codex "prompt"` are interactive TTY entrypoints. Non-interactive validation and review automation must use `codex exec ...`, because Codex rejects direct interactive mode when stdin is not a terminal.

---

## Workflow

```text
For each enabled agent: Install or Update -> Verify -> Record
```

### Phase 1: Install & Verify

For each agent in registry, apply first matching rule:

| Condition | Action | Report |
|-----------|--------|--------|
| `disabled: true` | SKIP | `disabled by user` |
| `dry_run: true` | Show planned command | `dry run` |
| Codex | `npm install -g @openai/codex` then `codex --version` | version or error |
| Claude installed | `claude update` then `claude --version` | version or error |
| Claude missing | `npm install -g @anthropic-ai/claude-code` then `claude --version` | version or error |

**Single pass:** install and verify happen atomically per agent. No separate scan phase; the install result is the state.

**Error handling:**

| Error | Detection | Response |
|-------|-----------|----------|
| npm not in PATH | `npm --version` fails | FAIL gracefully, report `npm not found in PATH` |
| Permission denied | stderr contains `EACCES` | FAIL, suggest `npm install -g --prefix ~/.local {pkg}` |
| Network error | stderr contains `ETIMEDOUT` or `ENETUNREACH` | FAIL, report `network error` |
| Unknown error | Any other non-zero exit | FAIL, include stderr |

**Output table:**

```text
Agent Installation:
| Agent  | Action    | Version  | Status |
|--------|-----------|----------|--------|
| Codex  | installed | 0.124.0  | ok     |
| Claude | updated   | 2.1.119  | ok     |
```

### Phase 2: Post-Install Codex Sanity Check

After successful Codex install/update:

1. Check `~/.codex/config.toml` top-level `approval_policy` and `sandbox_mode`.
2. Check configured Codex marketplaces for duplicate active paths to this repo.
3. If drift is found, report a WARN and defer remediation to `ln-013-config-syncer`.

This installer does not install marketplace plugins, rewrite Codex marketplace layout, or manage Codex execution defaults. It only reports drift so install success is not mistaken for a healthy two-agent environment.

---

## Critical Rules

1. **Never modify `disabled` flags.** Respect them, never change them.
2. **Fail gracefully.** One agent failure does not block the other.
3. **Global install only.** CLI tools must be in PATH.
4. **Report all changes.** Include config observations in the final summary table.
5. **Idempotent.** Safe to run multiple times.
6. **Claude and Codex only.** Do not add unrelated agent branches.
7. **Codex marketplace/plugin and execution-default remediation belongs to ln-013.** This skill may detect drift, but must not rewrite marketplace/cache layout or Codex top-level permission defaults itself.

## Anti-Patterns

| DON'T | DO |
|-------|-----|
| Separate check/install/verify phases | Single pass: install then verify |
| Retry failed installs automatically | One attempt, report failure |
| Use `sudo npm install` | Suggest `--prefix` for permission issues |
| Install agents marked `disabled` | Skip with clear report |
| Configure MCP settings or marketplace plugins here | Route environment alignment to `ln-013-config-syncer` |

---

## Definition of Done

- [ ] Codex and Claude processed in single pass (install + verify)
- [ ] Disabled agents skipped with report
- [ ] Version verified immediately after each install
- [ ] Codex marketplace/plugin and execution-default sanity checked or explicitly reported for ln-013 follow-up
- [ ] Status table displayed
- [ ] Structured summary returned
- [ ] Summary artifact written to the managed or standalone runtime path

---

**Version:** 1.1.0
**Last Updated:** 2026-03-23
