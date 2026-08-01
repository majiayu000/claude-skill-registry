---
name: secret-handling
description: The secret-source gate. Routed to when changed code reads, writes, or passes a secret — API key, token, password, connection string, signing key, certificate, or any value that grants access. Validates that every secret comes from the approved store and never lands in source, log, test fixture, error response, image, or LLM prompt. The auth-crypto-reviewer agent is dispatched as the reviewer.
---

# secret-handling

The secret-source gate. Routed to when changed code reads, writes, generates, stores, or passes a secret. If a value's secret status is uncertain, treat it as a secret.

## Pre-flight

Read these, or STOP and surface the gap — never guess the policy:

- `<project-root>/.codearbiter/security-controls.md` — the approved secret store, the access method (IAM role, workload identity, service-account token — never long-lived static keys), and any required reference format. If this file is unreadable, BLOCK; do not infer the store.

## Phase 1 — Identify · gate: BLOCK

Scan the changed code for secret-bearing names: `password`, `secret`, `token`, `key`, `credential`, `api_key`, `apikey`, `private`, `cert`, `passphrase`. For each match, record its source (where the value originates) and every sink (where it flows). No candidate may remain unclassified.

Gate: every candidate secret is listed with its source and sinks.

## Phase 2 — Source · gate: BLOCK

Each secret MUST originate from the approved store in `security-controls.md`, accessed via the approved method. The following sources BLOCK unconditionally:

- Hardcoded string literal.
- `process.env` or `.env` for a secret value — these are for non-sensitive config only (ports, log levels). `.env` files MUST be gitignored and secrets-scanned on every PR.
- A database column holding the raw value (a stored *reference* is allowed — see Phase 3).
- Any store endpoint not named in `security-controls.md`.

**Stakes:** a hardcoded or unapproved-source secret ships to every clone, every CI log, and the
history; rotation is the only fix once it lands. State that when you block, not just "unapproved
source." A genuine catch the user then rotates earns **exactly one** warm sentence at the close (per
the orchestrator register), never on a clean pass.

Gate: every secret is sourced from the approved store via the approved access method.

## Phase 3 — Sinks and persistence · gate: BLOCK

Trace each secret to all sinks. These are prohibited regardless of project, with no log-redaction excuse:

- Any logger call, at any level.
- Client-facing error messages or HTTP response bodies.
- Telemetry, metrics, tracing, span attributes.
- Any LLM prompt or agent context — treat the provider as out-of-boundary; verify shape with length, prefix, or hash, never the value.
- Serialized state, session storage, or JWT payload.
- A database column, except the store *reference* (path, ID, ARN) in the format `security-controls.md` requires. A migration adding a reference column without a format check constraint BLOCKs.

Secrets MUST NOT outlive the request that uses them — no module-level variable, no instance field, no cross-request cache holding a secret value.

Dispatch the `auth-crypto-reviewer` agent (`${CLAUDE_PLUGIN_ROOT}/agents/auth-crypto-reviewer.md`) to confirm these findings against `security-controls.md`.

Gate: no secret reaches a prohibited sink and no secret persists beyond its request.

**On pass — record the gate:** follow `${CLAUDE_PLUGIN_ROOT}/includes/security-gate-record.md` (the shared record mechanism). For this gate the relevant commit hook is **H-10b** (secrets). On any BLOCK, do NOT record the pass.

**Out-of-scope finding:** do not act on it and do not author an ADR (ADRs are user-attributed, via `/adr` only). Mark it inline with `[NEEDS-TRIAGE]`; never silently drop it.

## Hard rules

- MUST read `security-controls.md` for the approved store before Phase 2 — BLOCK if it cannot be read.
- MUST NOT source a secret from a hardcoded literal, `process.env`, a `.env` file, or any unapproved store.
- MUST NOT let a secret reach a logger, error response, telemetry, LLM prompt, serialized state, or session/JWT payload.
- MUST NOT store a secret value in the database — store the approved-store reference only, with a format check constraint.
- MUST NOT let a secret persist beyond the request boundary.
- MUST record the `security-gate-passed` marker (via `hooks/security-pass.py`) ONLY when the gate genuinely passes — the marker is what unblocks the commit (hook H-10b), so a premature or unconditional recording defeats the gate.
