---
name: multi-ai
description: Use when configuring ARC_PROVIDER_MODE or routing verification work to external AI providers (Codex, Gemini). Claude-only is always the safe fallback.
invocation: agent
---

# Multi AI

Lightweight provider routing for Arc. Controls when and how external AI providers (Codex, optionally Gemini) participate alongside Claude in the workflow. No command may fail solely because optional providers are unavailable — Claude-only is always the safe fallback.

## Invocation Contract

Inputs:
- `ARC_PROVIDER_MODE`
- `ARC_MULTI_AI`
- Provider availability/auth state

Outputs:
- Effective provider mode
- Explicit downgrade notice when fallback is applied

## Provider Modes

Set via `.arc/config.json` (preferred) or environment variables (override):

- **`claude-only`** (default) — All work stays with Claude. No external calls.
- **`codex-assist`** — Codex produces draft findings; Claude validates and publishes.
- **`codex-primary`** — Codex performs primary analysis; Claude runs final adjudication.

Resolution order: `ARC_PROVIDER_MODE` env var > `.arc/config.json` `provider_mode` field > default (`claude-only`).

The `multi_ai: true` flag (in config) or `ARC_MULTI_AI=true` (env) must be set to enable any non-Claude mode. If provider mode is set to a non-Claude mode but `multi_ai` is false or unset, emit an explicit downgrade notice and continue in Claude-only mode.

## Provider Detection

Detection runs in this order before any external call:

1. Check `ARC_MULTI_AI=true` (env) or `multi_ai: true` (`.arc/config.json`) — if false/unset, use Claude-only.
2. Detect `codex` CLI availability — is the binary on PATH?
3. Detect Codex authentication — `OPENAI_API_KEY` or active Codex auth session.
4. Detect optional Gemini — only if the current command explicitly supports it.

If any required check fails, downgrade to Claude-only and continue. Log the downgrade reason.

## Agent Routing Matrix

### Claude-Only Agents (Never Routed Externally)

- `plan-creator-default`
- `openspec-default`
- `beads-default`
- `bead-worker`
- `fix-finding`
- Team lead orchestration

Reason: these agents mutate project artifacts and must remain deterministic. External provider variability could corrupt plan/spec/bead state.

### Codex-Eligible Agents

- `verify-typescript`
- `verify-performance`
- `verify-architecture`
- `verify-security`
- `verify-requirements`

In **codex-assist** mode:
1. Codex produces draft findings.
2. Claude validates and normalizes findings against Arc's verification schema.
3. Claude publishes the final result.

In **codex-primary** mode:
1. Codex performs primary analysis with full context.
2. Claude runs a final adjudication gate before reporting results.

## External Call Rules

- All external provider calls must be explicit and logged in output.
- Recommended Codex invocation pattern:
  `codex exec --model ${ARC_CODEX_MODEL:-gpt-5.3-codex} "<prompt>"`
- On provider failure or timeout, fallback to Claude-only and continue.
- Never silently swallow provider errors — log them and note the fallback.

## Gemini Integration

Gemini support is optional and command-specific. When available:
- Use for design review and frontend analysis (large context window advantage).
- Detection follows the same pattern: check availability, check auth, fallback if missing.
- Gemini is never required for any core Arc workflow.

## Related Skills

- `router` determines the tier; provider routing applies within any tier.
- `debate` may route debate participants to different providers in multi-AI mode.
- Verification agents are the primary consumers of external provider routing.
