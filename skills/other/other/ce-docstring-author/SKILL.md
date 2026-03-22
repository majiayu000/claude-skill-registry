---
name: ce-docstring-author
description: >
  Write or repair NumPy-style docstrings for public CE APIs following STD-002 and
  contributor documentation rules.
---

# CE Docstring Author

You are writing or fixing Numpy-style docstrings for CE source code.
Numpy style is mandatory for all public symbols in `src/calibrated_explanations/`.

Load `references/docstring_patterns.md` for full templates and CE-specific patterns.

---

## Section presence rules

| Section | When required |
|---|---|
| One-line summary | Always |
| `Parameters` | When there are >= 1 parameters |
| `Returns` | When the function returns a non-None value |
| `Raises` | When the function raises documented exceptions |
| `Notes` | Optional — use for non-obvious behaviour |
| `References` | Optional — when citing papers or ADRs |
| `Examples` | Strongly encouraged for public API; required for CE-First entry points |

Canonical order: `Parameters` -> `Returns` -> `Raises` -> `Notes` -> `References` -> `Examples`.

---

## Type annotation format (in docstrings)

```
param : np.ndarray of shape (n_samples, n_features)
param : int or None, optional
param : {'regular', 'triangular', 'ensured'}, optional
param : list of str
param : Mapping[str, Any]
param : CalibratedExplanations
param : float, optional. Default 0.5.
```

---

## Deprecation in docstrings

When a parameter is deprecated, add a `.. deprecated::` directive in its entry:
```
param : int, optional
    .. deprecated:: 0.11.0
        Use ``new_param`` instead. Will be removed in v0.13.0.
```

---

## Running docstring coverage

```bash
python scripts/quality/check_docstring_coverage.py src/
```

The coverage gate is tracked in `docstring_coverage.txt`. Public members with
missing docstrings appear as failures in CI.

---

## Evaluation Checklist

- [ ] Summary is one line, imperative mood, no trailing period.
- [ ] `Parameters` section present for all non-trivial inputs.
- [ ] Types match the function signature (or are more specific when `Any` is used).
- [ ] `Returns` section describes the return value and its shape/keys.
- [ ] `Raises` documents all exceptions the caller must handle.
- [ ] `Examples` section present for CE-First entry points.
- [ ] Deprecated parameters annotated with `.. deprecated:: <version>`.
- [ ] Section order matches the canonical order above.
