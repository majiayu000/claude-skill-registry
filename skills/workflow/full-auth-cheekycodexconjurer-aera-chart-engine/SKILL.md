---
name: full_auth
description: When explicitly authorized, execute end-to-end with a phased plan in one run until Definition of Done is met.
metadata:
  short-description: Full authorization execution mode
---

## Authorization
Use this skill only when the user explicitly grants permission to edit files and
complete the task end-to-end without asking “should I continue?”.

## Execution Mode
PHASED PLAN, ALL PHASES IN ONE RUN
- Produce a phased implementation plan first (Phase 1/2/3…).
- Immediately execute all phases in sequence in the same run, until Definition
  of Done is met.
- Only pause if blocked by missing info or if a command fails and cannot be
  resolved autonomously.

## Blocking Rule
If blocked, ask exactly one concise question that would unblock the work.
Otherwise, keep going.

## Definition of Done (generic)
- Safety validation passes (respect `.agentignore`).
- Use the best available repo verification:
  - Prefer `.agent-docs/memory/COMMANDS.json` and `MANIFEST.yaml`.
  - If missing, run capability/command detection and record confidence.
  - Run tests, lint, and build as applicable.
- If `QUALITY_GATES.md` exists, follow it as the source of truth.
- Provide a final summary and list all modified/created files.

## Output Requirements
1) Investigation notes (what matters in the repo).
2) Phased plan (Phase 1/2/3… with files and behaviors).
3) Implementation (commit-style narrative by phase).
4) Files changed + verification results (commands run and outcomes).

## Guardrails
- Always respect `.agentignore` forbidden zones.
- Enforce Trust Layer TDD for behavior changes.
- Keep an Action Ledger entry for meaningful work.
