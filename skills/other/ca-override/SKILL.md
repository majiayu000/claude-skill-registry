---
name: ca-override
description: Sanctioned, logged bypass of a gate or hard rule — one audit line, then proceed.
argument-hint: "<reason>"
---

# /ca-override — logged bypass

The sanctioned escape hatch. Bypass is permitted only with an audit log entry. Overrides are always
logged, always visible, never silent. Single identity, single confirm.

## Flow

1. Validate `$ARGUMENTS` — the reason names the gate being bypassed and a justification. Reject a
   vague reason ("just skip it") and ask for a specific one.
2. Detect the operator identity from `git config user.email` only. If it is unset, ask the user once
   to state their identity for the log. (No platform ladder, no second confirmation.)
3. Append one line to `<project-root>/.codearbiter/overrides.log`:

   ```
   [ISO-8601 timestamp] | BY: <email> | GATE: <gate bypassed> | REASON: <reason>
   ```

   The log is append-only — never edited or deleted, committed as a permanent audit artifact.
4. Proceed with the overridden action. Note in the response that the override is logged.

## Security ceiling — heavier path for security-critical stops

A routine gate (lint, a style rule, a non-security review finding) takes the single-confirm path above.
But a **security-critical stop is NOT bypassable by a single confirm.** The following require the
heavier path below, never the one-line flow:

- a security **CRITICAL** finding;
- the crypto/secret commit gate (hook **H-09b / H-10b** — staged crypto/TLS or secret without a gate pass);
- an **irreversible** operation (data loss, a destructive migration, anything unrollbackable).

Heavier path (all required, in order):
1. **Surface the specific finding verbatim** — name the exact primitive/secret/operation and the
   concrete risk. A generic "security override" is rejected.
2. **Explicit per-finding acknowledgement** — the user must acknowledge *that specific finding* in
   their own words (a bare "yes"/"go ahead"/"I trust you" is declined — this mirrors `decision-variance`).
   Detect identity from `git config user.email`; if unset, ask once.
3. **Heavier log entry** — append a line tagged `SECURITY-OVERRIDE` that records the specific finding,
   not just the gate name:

   ```
   [ISO-8601] | BY: <email> | SECURITY-OVERRIDE | FINDING: <specific finding> | REASON: <reason>
   ```
4. **Only then** record the bypass. For the crypto/secret commit gate, that means running
   `python3 "<plugin-root>/hooks/security-pass.py" || python "<plugin-root>/hooks/security-pass.py"`,
   which writes `<project-root>/.codearbiter/.markers/security-gate-passed` bound to the
   sensitive lines it approves, so hook H-09b/H-10b allows the commit — recorded **only** after
   steps 1–3, never to skip the gate proper.

Under `/ca-sprint`, a security-critical override is a hard-gate STOP: it surfaces to the user and is
**never** auto-decided, even in autonomous mode (`SPRINT.md` hard gates).

## Hard gate

MUST write the log line before proceeding — it is not optional. MUST capture an operator identity —
"codeArbiter" or "automated" are not valid. MUST include a justification. The override is scoped to
the immediate action only; it creates no standing exception. MUST NOT edit or delete an existing
`overrides.log` entry. MUST route a security-critical / crypto-secret / irreversible stop through the
**Security ceiling** path — never the single-confirm flow — and MUST NOT auto-decide such an override
under `/ca-sprint`.

## When NOT to use

- Routine work that passes all gates — never needed.
- Reconciling two conflicting sources → `/ca-conflict`.
