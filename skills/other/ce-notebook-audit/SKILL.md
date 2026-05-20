---
name: ce-notebook-audit
description: >
  Audit notebooks for public-API correctness, policy compliance, and private-member
  usage violations.
---

# CE Notebook Audit

You are auditing notebooks in `notebooks/` for policy compliance and API
correctness. The key rules are defined in ADR-012 (gallery rendering: advisory
on mainline, blocking on release branches).

---

## Quick scan commands

```bash
# Scan for private-member usage in notebooks
make check-private-members

# Check agent instruction file consistency
make check-agent-instructions

# Run navigation tests (must pass before release)
pytest tests/docs/test_navigation.py -v
```

---

## Notebook policy matrix

| Rule | Severity | ADR |
|---|---|---|
| No `from calibrated_explanations.core.*` imports | **BLOCKING** | ADR-001 |
| No `_private` member access | **BLOCKING** | ADR-023 |
| Notebooks render without error (release branches) | **BLOCKING** | ADR-012 |
| Notebooks render without error (mainline) | Advisory | ADR-012 |
| Uses only public `CalibratedExplainer` / `WrapCalibratedExplainer` API | **BLOCKING** | ADR-001 |
| No hardcoded dataset paths outside `data/` | Non-blocking | — |
| Markdown cells have headings to aid navigation | Non-blocking | — |

---

## Scanning for private-member usage

```bash
# Dedicated scan script
python scripts/anti-pattern-analysis/scan_private_usage.py --check

# Direct grep across all notebooks
grep -r "\._[a-z]" notebooks/ --include="*.ipynb"
```

Allowed exceptions (implementation artefacts, not user APIs):
- None — all `_private` usage in notebooks is forbidden.

---

## Scanning for direct core imports

```bash
grep -r "from calibrated_explanations.core" notebooks/ --include="*.ipynb"
grep -r "import calibrated_explanations.core" notebooks/ --include="*.ipynb"
```

Any match is a blocking violation; fix by replacing with the public top-level
import:
```python
# BAD
from calibrated_explanations.core.calibrated_explainer import CalibratedExplainer

# GOOD
from calibrated_explanations import CalibratedExplainer
```

---

## Cell-level checks

For each notebook cell, verify:

1. **Imports**: only `from calibrated_explanations import ...` or
   `import calibrated_explanations as ce`.
2. **Method calls**: check against `QUICK_API.md` for valid public method names.
3. **Parameters**: `filter_top=n` not `n_top_features=n` on explanation calls.
4. **No `plt.show()` without a guard block**: notebooks should use
   `%matplotlib inline` and let plots render automatically.
5. **Data loading**: uses relative paths from workspace root or `data/` directory.

---

## Notebook execution audit

Run a notebook end-to-end and capture errors:
```bash
# Requires jupyter + nbconvert
jupyter nbconvert --to notebook --execute notebooks/core_demos/MyNotebook.ipynb \
    --output /tmp/test_run.ipynb \
    --ExecutePreprocessor.timeout=300
```

Check the exit code — non-zero means the notebook has a runtime error.

---

## Automated notebook audit (make target)

```bash
make notebook-lint       # syntax + import checks
make notebook-execute    # execute all core_demos notebooks
```

If these targets are unavailable run individual `nbconvert` commands.

---

## Known issues and resolution

| Issue | Resolution |
|---|---|
| `AttributeError: 'Explanation' has no attribute 'n_top_features'` | Replace with `filter_top=n` |
| `from calibrated_explanations.core import ...` | Replace with top-level import |
| `._conformal_calibrator` or any `._x` access | Remove; use public accessor if one exists |
| `pytest tests/docs/test_navigation.py` fails | Check that all notebooks listed in `docs/` are reachable and render |

---

## Audit report template

```
## Notebook Audit Report

Notebook: notebooks/core_demos/<name>.ipynb
Date: YYYY-MM-DD

### Blocking violations
- [ ] (none)

### Non-blocking issues
- [ ] (none)

### API usage notes
- (e.g., uses deprecated parameter X — schedule migration)

### Verdict
PASS / FAIL
Recommended action: (merge as-is | fix blocking violations before merge | advisory follow-up)
```

---

## Audit Checklist

- [ ] `make check-private-members` passes (exit code 0).
- [ ] `make check-agent-instructions` passes.
- [ ] `grep` for core imports returns no matches.
- [ ] Notebooks execute without error (`nbconvert --execute`).
- [ ] `pytest tests/docs/test_navigation.py` passes.
- [ ] All blocking violations resolved.
- [ ] Non-blocking issues logged for follow-up.
