---
name: pre-mortem
description: Imagine failure first to surface guardrails and feature mitigations.
license: MIT
command: /ctx:pre-mortem
---

# `/collaboration:pre-mortem`

Use when planning initiatives where early risk surfacing saves rework.

## Inputs
- Initiative and horizon (30/90/180 days)
- Success definition
- Known risks/compliance constraints

## Steps
1. Define success state and horizon (default 90 days).
2. List top failure modes across tech, UX, org, market, compliance.
3. For each, propose mitigations/guardrails with Effort (S/M/L) and Owner.
4. Pull 2–3 mitigations that double as feature ideas.
5. Create Tasks for guardrails or pass to `/ctx:plan`.

## Output Template
```
### Success State (horizon)
### Failure Modes
### Mitigations & Guardrails (effort, owner)
### Feature Candidates from Mitigations
### Immediate Tasks
```

## Pairings
- Run after `/collaboration:concept-forge` to sanity-check top concepts.
- Feed guardrails into `/dev:code-review` or security skills as needed.
