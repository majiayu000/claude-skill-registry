---
name: orchestrate
description: 'Out-of-session orchestration instrument lane: route, preflight, verify before human atm/am procedure. Triggers: "orchestrate out-of-session", "route + preflight + verify a run", "orchestration preflight".'
practices:
- team-topologies
- hexagonal-architecture
hexagonal_role: supporting
consumes:
- automation-shape-routing
produces:
- result.json
context_rel:
- kind: customer-of
  with: using-atm
skill_api_version: 1
user-invocable: true
context:
  window: isolated
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
metadata:
  tier: orchestration
  dependencies:
  - automation-shape-routing
output_contract: schemas/orchestration-instrument.v1.schema.json
---

# Orchestrate — Out-of-Session Instrument Lane

When work escalates **outside** the in-session loop, start with deterministic
instruments — not a parallel spawn manual.

## Procedure

1. **Route** — `ao orchestrate route --json` (or `--writers N --models opus,codex,agy`)
2. **Preflight** — `ao orchestrate preflight --profile <name> --json`
3. **Spawn** — follow the profile in `docs/contracts/orchestration-profiles.yaml` using raw `atm` (human procedure; see `using-atm` / `dual-pane-atm`)
4. **Verify** — `ao orchestrate verify --session <name> --profile <name> --json`

Profiles contract is SOT; skills are drift-gated procedure, not CLI replacements.

## Commands

| Command | Role |
|---------|------|
| `ao orchestrate route` | Posture → profile recommendation |
| `ao orchestrate preflight` | Admission gate before spawn |
| `ao orchestrate verify` | Post-spawn windshield |
| `ao orchestrate tools` | Tool matrix probe |
| `ao orchestrate status` | Active ATM sessions |
| `ao orchestrate shape` | Stamp execution-packet shape |
| `ao orchestrate select` | Backend ladder (existing) |

## Non-goals

- Does not replace `atm spawn` in Phase 1 (earn-it wrappers deferred)
- Does not mandate orchestrate via hook on day one

## References

- Acceptance: `references/orchestrate.feature`
- Contract: `docs/contracts/orchestration-profiles.yaml`
- Playbook: `skills/dual-pane-atm/`
- Substrate: `skills/using-atm/`
