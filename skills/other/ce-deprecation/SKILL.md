---
name: ce-deprecation
description: >
  Implement ADR-011 deprecation and removal workflows with correct warnings,
  migration notes, and release timeline handling.
---

# CE Deprecation & Mitigation

You are deprecating a public symbol, parameter, module path, or serialized output,
or removing a previously deprecated symbol. Follow ADR-011 strictly.
The mitigation guide (`docs/migration/deprecations.md`) is the single source of
truth for all deprecated and removed features.

Load `references/deprecation_patterns.md` for full code patterns and test templates.

---

## ⚠ Mandatory: Update the Status Table

Every deprecation introduced or removed **MUST** update `docs/migration/deprecations.md`:

- **New deprecation**: Add a row to the **Active Deprecations** table (set Removal ETA to at least 2 minor versions ahead).
- **Removal**: Move the row from Active to the **Removed Deprecations (History)** table and fill in the actual version removed.
- This is not optional — the table is the authoritative inventory of all library deprecations.

---

## The Mitigation Guide (`docs/migration/deprecations.md`)

1. **Check if existing**: Every symbol marked with `.. deprecated::` MUST be listed in the Active Deprecations table.
2. **Add if missing**: If you find a deprecation in code that isn't in the guide, add it immediately.
3. **Removal Status**: Check the "Removal ETA" column to determine if a symbol is eligible for removal.

---

## Removing Deprecated Symbols

Before removing a symbol, verify it meets the ADR-011 "Two Minor Release" rule:
- A symbol deprecated in `v0.10.x` is only eligible for removal in `v0.12.x` or later.

**Steps for removal**:

1. Delete the implementation, deprecated parameters, or module shims.
2. Update `docs/migration/deprecations.md`: move the row from **Active Deprecations** to **Removed Deprecations (History)** and fill in the actual removal version.
3. Confirm no remaining call sites exist in `src/` via `grep -r "<symbol>" src/`.
4. Remove associated deprecation tests.
5. Update `docs/improvement/RELEASE_PLAN_v1.md` status table.

---

## Historical Research (Missing Versions)

If a symbol's docstring contains `.. deprecated::` but lacks a version:
1. Search commit history: `git log -S ".. deprecated::"` or `git blame <file>`.
2. Find the earliest version/tag containing that change.
3. Update code + guide with the found version.

---

## Timeline (ADR-011)

```
v0.X.0  — introduce new API; add deprecation warning for old API
v0.X+1  — still warning (minimum: 2 minor releases before removal)
v0.X+2  — remove old API (earliest)
```

---

## Docstring annotation

Always add a `.. deprecated::` directive to the Numpy docstring:
```
.. deprecated:: <version>
    <one-line reason and migration pointer>.
```

---

## Migration guide entry

Add an entry to `docs/migration/deprecations.md`:

```markdown
| Deprecated symbol | Replacement | Introduced | Removal ETA | Notes |
|---|---|---:|---:|---|
| `old_param` | `top_features` | v0.11.0 | v0.13.0 | Uses `deprecate()` in `explain_factual`. |
```

Also update the status table in `docs/improvement/RELEASE_PLAN_v1.md`.

---

## CI strict mode

Users can opt into treating deprecation warnings as errors:
```bash
CE_DEPRECATIONS=error pytest
```

---

## Out of Scope

- Legacy User API (ADR-020) — governed by "Major Release Only" lifecycle, not ADR-011.
- Plugin removal — plugins follow their own version lifecycle but still use `deprecate()`.

## Evaluation Checklist

- [ ] `deprecate()` called with descriptive message naming old and new symbol.
- [ ] `once_key` is unique and follows the `<module>.<symbol>_deprecation` pattern.
- [ ] `.. deprecated:: <version>` added to docstring.
- [ ] If version is unknown, research commit history to find deprecation origin.
- [ ] Removal version is at least 2 minor releases after the deprecation release.
- [ ] Row added to the **Active Deprecations** table in `docs/migration/deprecations.md` (or moved to **Removed Deprecations (History)** on removal, with actual version filled in).
- [ ] `RELEASE_PLAN_v1.md` status table updated.
- [ ] Test uses `pytest.deprecated_call()` to assert the warning fires.
