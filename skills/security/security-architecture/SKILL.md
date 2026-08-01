---
name: security-architecture
description: Optional, opt-in STRIDE threat pass for a sensitive feature — invoked deliberately via /threat-model, never forced on ordinary changes. Walks the change's attack surface and security boundaries (governed by ${CLAUDE_PROJECT_DIR}/.codearbiter/security-controls.md), surfaces threats and unmitigated gaps, and MAY dispatch security-reviewer or auth-crypto-reviewer. Not a routine gate; it can hard-STOP only on a genuinely critical unmitigated threat it surfaces.
---

# security-architecture

Optional, lightweight threat-modeling pass over a design before it is built. Routed to only when the user deliberately invokes `/threat-model <scope>` for a sensitive feature — never forced on an ordinary change. Reviews architectural intent before code exists; for code already written, dispatch `security-reviewer` instead.

## Pre-flight

- Read `${CLAUDE_PROJECT_DIR}/.codearbiter/security-controls.md` — approved primitives, declared security boundaries and their permitted crossings, what is and is not allowed. If it cannot be read, STOP and surface the gap; do not guess the boundary model.
- Establish the scope from the user's `/threat-model` argument: the feature, component, or design under review.

## Phase 1 — Attack surface · gate: BLOCK

Map what the change exposes. Name, for the scope:

- New or changed entry points — routes, endpoints, message consumers, CLI surfaces.
- New egress — outbound calls, external dependencies, new data sinks.
- Security boundaries crossed, as declared in `security-controls.md` (trust transitions, privilege changes, data leaving a controlled zone).
- The data handled and its sensitivity.

A boundary crossing not described in `security-controls.md` is a finding, not a silent pass. A finding outside this scope gets one line with an inline `[NEEDS-TRIAGE]` marker.

Gate: the attack surface and every boundary crossing in scope are enumerated.

## Phase 2 — STRIDE pass · gate: STOP

Walk the surface from Phase 1 through STRIDE. For each relevant category, name the concrete threat and the control expected to mitigate it:

- **Spoofing** — identity/authentication of the actor at the boundary.
- **Tampering** — integrity of data in transit and at rest.
- **Repudiation** — whether actions are attributable.
- **Information disclosure** — exposure of sensitive data, including in logs and errors.
- **Denial of service** — exhaustion or availability impact.
- **Elevation of privilege** — privilege gained across the boundary.

Mark each threat's mitigation `PRESENT`, `PLANNED`, or `GAP`. Skip a category only with a one-line reason it does not apply.

If the threat depends on auth, crypto, key handling, or secrets, MAY dispatch `${CLAUDE_PLUGIN_ROOT}/agents/auth-crypto-reviewer.md`. For broader boundary or surface concerns, MAY dispatch `${CLAUDE_PLUGIN_ROOT}/agents/security-reviewer.md`. Both govern by `security-controls.md`.

Gate: STOP only on a genuinely critical unmitigated threat — a `GAP` that is exploitable now with high impact. Lesser gaps are surfaced as constraints, not stops.

## Phase 3 — Report · gate: BLOCK

Produce a terse report:

- **Surface** — entry points, egress, boundaries crossed.
- **Threats** — the STRIDE findings; lead with `GAP`s, then `PLANNED`, summarize `PRESENT` in one line.
- **Verdict** — `PROCEED` (no open gap), `PROCEED-WITH-CONSTRAINTS` (gaps listed with owner), or `STOP` (a critical unmitigated threat is present; name it).

A decision-worthy gap is escalated to the user or to `${CLAUDE_PROJECT_DIR}/.codearbiter/decisions/` via `/adr` — never authored as an ADR by this skill.

Gate: report delivered with a stated verdict; every STOP-level threat from Phase 2 is reflected in it.

## Hard rules

- MUST NOT force this pass on an ordinary change. It is invoked deliberately for sensitive features only.
- MUST NOT guess the boundary model — read `security-controls.md` or STOP.
- MUST NOT silently pass an undeclared boundary crossing — surface it.
- MUST NOT STOP on anything short of a critical, exploitable, unmitigated threat; lesser gaps are constraints.
- MUST NOT author an ADR — escalate decision-worthy gaps to the user or `/adr`.
