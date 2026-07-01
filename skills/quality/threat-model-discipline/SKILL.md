---
name: threat-model-discipline
description: Use when starting an engagement, before exploitation, or whenever the attack surface changes — build/validate the threat model and detect drift (new unreviewed surface) before advancing
scripts:
  - scripts/threatmodel_lint.py
---

# Threat-Model Discipline

## Overview

**You cannot test what you have not modeled.** A threat model names the assets, entry points, trust
boundaries, relevant ATT&CK techniques, and existing mitigations — so coverage is deliberate, not
accidental. On a long engagement the surface drifts (a new endpoint, a new dependency); **un-reviewed
drift is where bugs hide.** This skill keeps the model complete and re-checks it for drift.

## When to Activate

- At engagement start (after recon-osint), before weaponize/exploit.
- Whenever recon is re-run or the target changes — to catch new attack surface.
- At `/engage.gate` — the gate refuses to advance on un-acknowledged drift.

## The model (JSON, materialized from recon)

`threat-model.json` (see `templates/threat-model/`): five required lists —
`assets`, `entry_points`, `trust_boundaries`, `attck` (technique ids), `mitigations`.

```bash
# 1. Lint - every required field present, no placeholders, valid ATT&CK ids
python skills/threat-model-discipline/scripts/threatmodel_lint.py lint .engage/recon/threat-model.json

# 2. Drift - diff a re-run against the reviewed baseline; NEW entry points/assets/boundaries are
#    unreviewed surface and BLOCK the gate until re-reviewed or acknowledged
python skills/threat-model-discipline/scripts/threatmodel_lint.py drift \
    .engage/recon/threat-model.baseline.json .engage/recon/threat-model.json
```

Or use `/engage.threatmodel` (materialize | lint | drift).

## Red Flags — STOP

- "We'll model it as we go" — unmodeled surface = untested surface. Model first.
- "Recon changed but the threat model didn't" — re-run drift; new surface must be re-reviewed.
- A threat model full of `TBD`/`[fill in]` — that is not a model; the lint fails it.
- A new `entry_point` appeared and you proceeded anyway — that is the exact gap attackers use.

## Rationalizations

| Excuse | Reality |
|--------|---------|
| "The model is obvious, skip it" | Obvious to you ≠ documented. Coverage you can't diff is coverage you can't trust. |
| "Drift is just noise" | A new entry point is new attack surface. Acknowledge it explicitly or re-review. |
| "ATT&CK mapping is busywork" | It turns 'we tested stuff' into 'we covered these techniques' — the report's backbone. |

Pairs with `scope-discipline` (what you may touch) and `finding-discipline` (what counts as proven).
