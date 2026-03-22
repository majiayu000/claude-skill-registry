---
name: ce-adr-consult
description: >
  Map a proposed change to governing ADRs and constraints before implementation; use
  for ADR applicability and conflict checks.
---

# CE ADR Consult

You are identifying which ADRs govern a proposed change and extracting their
binding constraints. ADR decisions take precedence over the release plan whenever
they conflict (execution-plan.instructions.md §3).

ADRs live in `docs/improvement/adrs/`. Superseded ADRs are prefixed with
`superseded ` and should not be consulted for new work.

---

## Quick lookup by change type

| Changing / implementing | Governing ADR(s) |
|---|---|
| Module / package boundaries | ADR-001 |
| Exception types or validation | ADR-002 |
| Caching (key design, eviction) | ADR-003 |
| Parallel execution / fallback | ADR-004 |
| Explanation payload schema / JSON | ADR-005 |
| Plugin registration / trust | ADR-006, ADR-033 |
| PlotSpec / visualization IR | ADR-007, ADR-016 |
| Explanation domain model | ADR-008 |
| Input preprocessing / mapping | ADR-009 |
| Evaluation vs core split | ADR-010 |
| Deprecation or migration | ADR-011 |
| Documentation build | ADR-012 |
| Interval calibrator plugin | ADR-013 |
| Plot plugin | ADR-014 |
| Explanation plugin | ADR-015, ADR-026 |
| PlotSpec schema versioning | ADR-016 |
| Legacy user API changes | ADR-020 |
| Calibrated intervals / semantics | ADR-021 |
| Matplotlib test coverage | ADR-023 |
| FAST feature filtering | ADR-027 |
| Logging and observability | ADR-028 |
| Reject/abstain strategy | ADR-029 |
| Test quality enforcement | ADR-030 |
| Serialization / save_state | ADR-031 |
| Guarded explanations | ADR-032 |
| Modality extension / packaging | ADR-033 |

---

## How to consult an ADR

1. Locate the file: `docs/improvement/adrs/ADR-<NNN>-<slug>.md`
2. Check `Status:` — skip if `Superseded`.
3. Read the **Decision** section to extract binding constraints.
4. Note the **Consequences** section for risk awareness.
5. Check the `docs/improvement/RELEASE_PLAN_v1.md` entry for the ADR to see
   which release milestone closes outstanding gaps.

```bash
# List all active (non-superseded) ADRs
Get-ChildItem docs/improvement/adrs/*.md | Where-Object Name -NotMatch '^superseded'
```

---

## Key invariants summary (most commonly hit)

### ADR-001 — Core / plugin boundary
- `core/` must never import from `plugins/`.
- New functionality → `plugins/`; delegation → via registry in `core/`.

### ADR-002 — Exceptions
- No bare `Exception` or `ValueError` in public-facing code.
- Use `calibrated_explanations.utils.exceptions.*`.

### ADR-006 — Plugin trust
- Third-party plugins: opt-in trust required (`trust_plugin()` / env var / pyproject).
- Built-ins: auto-trusted.

### ADR-011 — Deprecation
- Minimum 2 minor releases before removal.
- Legacy User API (ADR-020) exempt; follows "Major Only" lifecycle.

### ADR-013 — Interval plugin
- `predict_proba` must delegate to VennAbers/IntervalRegressor reference.
- `IntervalCalibratorContext` is read-only; plugin must not mutate it.

### ADR-021 — Interval semantics
- Invariant: `low ≤ predict ≤ high` must always hold.

### ADR-023 — Matplotlib exemption
- `viz/matplotlib_adapter.py` is excluded from coverage reporting.
- Tests run normally with `pytest --no-cov -m viz`.

### ADR-030 — Test quality
- Coverage gate: 90%+ (excluding ADR-023 exemption).
- Naming: `test_should_<behavior>_when_<condition>`.

### ADR-031 — Serialization
- All calibrators must implement `to_primitive()` / `from_primitive()`.
- `schema_version` mandatory; fail-fast on incompatible version.

### ADR-032 — Guarded explanations
- Use `explain_guarded_factual` / `explore_guarded_alternatives` for unknown distributions.

### ADR-033 — Modality extension
- Non-tabular modality code must NOT enter `core/`.
- `data_modalities` and `plugin_api_version` required in `plugin_meta`.

---

## Conflict resolution

When a release plan step and an ADR conflict:
1. The **ADR takes precedence**.
2. Document the conflict in the PR.
3. If the plan needs to supersede the ADR, a new ADR or ADR update is required first.

---

## Evaluation Checklist

- [ ] All governing ADRs identified for the proposed change.
- [ ] Status field checked (not `Superseded`).
- [ ] Decision section read; binding constraints listed.
- [ ] No ADR constraint violated by the proposed implementation.
- [ ] Release plan milestone for outstanding gaps noted and respected.
