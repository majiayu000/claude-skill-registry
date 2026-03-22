---
name: ce-onboard
description: >
  Read-only session primer for CE-first invariants, key files, and skill routing at
  session start.
---

# CE Onboard

This is your session primer. Read it in full before touching any CE code.
Nothing here requires running code or calling tools — just read and confirm
you understand the invariants.

---

## 1. Project identity

`calibrated_explanations` is a scikit-learn-compatible Python XAI library.
It extracts calibrated factual rules, alternative rules, and prediction
intervals from any model.

- **Current version**: v0.10.4
- **Target milestone**: v0.11.0 (see `docs/improvement/RELEASE_PLAN_v1.md`)
- **Core entry points**: `CalibratedExplainer`, `WrapCalibratedExplainer`
- **Public install**: `pip install calibrated-explanations`

---

## 2. The CE-First invariants (memorise these)

1. **Always use `WrapCalibratedExplainer`** — never subclass or bypass it.
2. **Fit → Calibrate → Explain** — that is the only valid lifecycle order.
3. **Never access `_private` members** — if you need it, there is a public
   accessor or the feature does not exist yet.
4. **Lazy imports** — do not add eager top-level imports for heavy libraries
   (`matplotlib`, `pandas`, `catboost`…) in `__init__.py`.
5. **Plugin-first** — new functionality belongs in `plugins/`, not `core/`.
6. **ADR wins** — if a plan and an ADR conflict, the ADR takes precedence.
7. **Fallback visibility** — every fallback emits `_LOGGER.info()` AND
   `warnings.warn(..., UserWarning)`. No silent fallbacks ever.
8. **Numpy docstrings** — all public functions and classes use numpy-style.
9. **Coverage gate** — `pytest --cov=... --cov-fail-under=90` must pass.
10. **Test naming** — `test_should_<behavior>_when_<condition>`.

---

## 3. Key files to read on first touch

| File | What it tells you |
|---|---|
| `CONTRIBUTOR_INSTRUCTIONS.md` | Canonical CE-First rules (authoritative) |
| `docs/improvement/RELEASE_PLAN_v1.md` | Current milestone + outstanding gates |
| `docs/improvement/adrs/` | All architectural decisions (ADRs 001–033) |
| `QUICK_API.md` | Public API surface cheat-sheet |
| `src/calibrated_explanations/ce_agent_utils.py` | CE-First runtime helpers |
| `tests/README.md` | Test structure and coverage requirements |

---

## 4. Skill catalogue (when to use which skill)

| Intent | Skill |
|---|---|
| Author a new ADR | `ce-adr-author` |
| Look up which ADRs apply | `ce-adr-consult` |
| Analyze ADR compliance gaps | `ce-adr-gap-analyzer` |
| Generate alternative explanations | `ce-alternatives-explore` |
| Get calibrated predictions (without explanations) | `ce-calibrated-predict` |
| Explanations for binary and multiclass tasks | `ce-classification` |
| Identify quality risks and anti-patterns | `ce-code-quality-auditor` |
| Code review a PR | `ce-code-review` |
| Validate/preprocess input data | `ce-data-preparation` |
| Identify unreachable or non-contributing code | `ce-deadcode-hunter` |
| Deprecate a function or param | `ce-deprecation` |
| Review proposals for risks and blind spots | `ce-devils-advocate` |
| Write or fix a docstring | `ce-docstring-author` |
| Post-generation API interaction | `ce-explain-interact` |
| Generate factual explanations | `ce-factual-explain` |
| Implement a fallback | `ce-fallback-impl` |
| Verify fallback coverage in tests | `ce-fallback-test` |
| Compare CE with SHAP or LIME | `ce-integration-compare` |
| Manage logging and audit context (ADR-028) | `ce-logging-observability` |
| Extend to a new data modality | `ce-modality-extension` |
| Use conditional/Mondrian calibration for fairness | `ce-mondrian-conditional` |
| Audit notebooks for API compliance | `ce-notebook-audit` |
| Prime a new CE session | `ce-onboard` |
| Manage and validate payloads (ADR-005) | `ce-payload-governance` |
| Build a CE pipeline from scratch | `ce-pipeline-builder` |
| Review visualization code | `ce-plot-review` |
| Author a new PlotSpec | `ce-plotspec-author` |
| Audit an existing plugin | `ce-plugin-audit` |
| Tune CE performance (caching/parallelism) | `ce-performance-tuning` |
| Scaffold a new plugin | `ce-plugin-scaffold` |
| Generate regression prediction intervals | `ce-regression-intervals` |
| Map CE to regulatory compliance obligations | `ce-regulatory-compliance` |
| Configure reject/defer policies | `ce-reject-policy` |
| Select next release task | `ce-release-check` |
| Finalize a PyPI release | `ce-release-finalize` |
| Plan an upcoming release version | `ce-release-planner` |
| Implement and verify a release task | `ce-release-task` |
| Audit RTD documentation quality | `ce-rtd-auditor` |
| Author or revise RTD pages | `ce-rtd-writer` |
| Implement serialization | `ce-serializer-impl` |
| Audit serialization coverage | `ce-serialization-audit` |
| Audit skills against Claude authoring guidance | `ce-skill-audit` |
| Create/refactor skills and templates | `ce-skill-creator` |
| Sync skill registries after skill changes | `ce-skill-registry-sync` |
| Audit existing tests | `ce-test-audit` |
| Write new tests | `ce-test-author` |
| Design tests to close coverage gaps | `ce-test-creator` |
| Remove redundant or low-value tests | `ce-test-pruning-expert` |
| Coordinate the Test Quality Method | `ce-test-quality-method` |

---

## 5. Module layout (ADR-001 boundary)

```
src/calibrated_explanations/
├── core/           # CalibratedExplainer, WrapCalibratedExplainer — do NOT modify unless necessary
├── plugins/        # All extensible functionality — registry, calibrators, plotters, explanations
├── calibration/    # Venn-Abers and conformal calibration logic
├── viz/            # PlotSpec IR + matplotlib adapter (ADR-007, ADR-016, ADR-023)
├── utils/          # Shared helpers, deprecation, logging
└── ce_agent_utils.py  # CE-first pipeline helpers for agents
```

**Rule**: Code in `core/` must not import from `plugins/`. Plugins import from `core/`, never the reverse.

---

## 6. Check your environment

Before coding, verify the install:
```bash
python -c "import calibrated_explanations; print(calibrated_explanations.__version__)"
python -m pytest -q --co -q   # list tests without running
make local-checks-pr           # fast gates (lint + type + quick tests)
```

---

## 7. Frequent agent mistakes (recorded in `.github/copilot-feedback-log.md`)

- Using `n_top_features=n` → correct param is `filter_top=n` on explain calls.
- Importing from `calibrated_explanations.core.*` directly → use top-level import.
- Adding a new fallback without `warnings.warn(UserWarning)` → always warn.
- Writing tests without `test_should_<behavior>_when_<condition>` naming.
- Adding eager `import matplotlib` at module top level → always import lazily.

---

## 8. Proceed

Once you have read sections 1–7, you are ready.
Select the appropriate skill from section 4 and begin.
