---
name: refactor-break-compat
description: Refactors by removing backward-compatibility layers, legacy code, and migration debt. Use when modernizing APIs, removing compat shims, killing feature flags, or rewriting a subsystem cleanly.
---

# Breaking Refactors — Scorched Earth

Backward compatibility is the tax the present pays to the past. This skill stops paying. Every compat shim, every legacy adapter, every "v1 still supported" branch is debt that compounds against the reader. Tear it all out. Break everything. Rebuild the system as if the old shape never existed.

There is no migration plan. There is no deprecation window. There is the old shape, and there is the right shape, and the only acceptable end state is the right shape with zero residue of the old.

## Doctrine

1. **Break first, apologize never.** Do not ask whether a thing can be broken. Assume it must be. The default verdict is demolition.
2. **One shape, no adapters.** The new design owns the entire surface. Never write new-to-old bridges, fallbacks, or translation layers — they resurrect the corpse you came to bury.
3. **Total migration or nothing.** A half-migrated codebase is the only true failure state. If you touch a subsystem, every caller leaves on the new API before you stop.
4. **Callers are not sacred.** "Unknown external consumers" is not a reason to preserve — it is a reason to rewrite their contract and let them adapt. You change the interface; the world changes with it.
5. **Delete, never disable.** Flags, gates, version checks, `if legacy:` — collapse to the winning branch and erase the fork entirely. Version control is the only museum.
6. **Old tests are old assumptions.** Tests that assert the legacy behavior encode the contract you are abolishing. Rewrite them to the new behavior or delete them. Do not let them veto the refactor.

## Demolition Targets — Find and Destroy

Hunt these down with `ast-grep` / `rg` and rip out every hit:

- `@deprecated` / `#[deprecated]` / `warnings.warn` — kill the marker and the thing it marks.
- Version-gated paths (`if version >= X`, `#[cfg(feature = "legacy")]`, capability checks) — collapse to the new branch.
- Adapter / shim / bridge / wrapper / compat layers — delete wholesale, rewrite callers against the real interface.
- Dual serialization formats (v1/v2 JSON, protobuf legacy fields, `oneof` fallbacks) — keep one format, drop the reader/writer for the rest.
- Feature flags and config toggles that select old vs new — delete the flag, hardwire the winner.
- Re-export / forwarding / alias modules that keep old import paths alive — delete them; fix every importer.
- Default-value fallbacks that exist only to tolerate old callers — remove the tolerance, make the new contract mandatory.
- Backward-compat tests, golden files, and fixtures pinning legacy output — rewrite to the new shape.
- Changelog promises, doc sections, and error strings naming the old API — purge.

## Execution Strategy

1. **Map the blast radius — to demolish it, not to spare it.** List every file, module, and caller of the old shape with `ast-grep` / `rg`. This is the demolition manifest, not a veto list.
2. **Tear out the old path.** Delete the compat layer, adapter, legacy branch, and every flag that fed it. No commenting out — delete.
3. **Rewrite every caller to the new contract.** Migrate all references from step 1. Typecheck/compile after each batch; let the compiler enumerate what you missed.
4. **Rewrite the tests to the new truth.** Update assertions to the new behavior; delete tests whose entire purpose was the old behavior. Add tests for the new contract where coverage is now thin.
5. **Exterminate ghosts.** Grep for string references, config keys, env vars, doc links, error messages, and import paths naming the old API. Zero survivors.
6. **Strip dead weight.** Remove imports, packages, dependencies, types, and dead files that only the old path needed.
7. **Verify the residue is zero.** A search for every old symbol, flag, and format name returns nothing. If it returns anything, you are not done.

## Anti-patterns — the urge to hedge

- **Asking permission to break.** The skill's premise is that breaking is correct. Map, then demolish.
- **New-to-old adapters.** Any code that lets an old caller keep calling the old way re-entrenches the thing you deleted. Forbidden.
- **Partial migration.** Half on new, half on old. The single worst outcome — worse than never starting.
- **Commenting out instead of deleting.** Invisible debt that grep cannot find. Delete.
- **Compat-of-compat.** Wrapping a shim in a shim. Two corpses, one coffin. Delete both.
- **Keeping a flag "for safety."** A flag that always resolves one way is a fork pretending to be a choice. Collapse it.
- **Letting legacy tests block the rewrite.** A red old-behavior test is not a regression — it is the contract dying on schedule. Rewrite it.

## Validation Gates

| Gate | Condition |
|------|-----------|
| Blast radius mapped | Every caller of the old shape enumerated as a demolition manifest |
| Old path deleted | Compat layers, adapters, flags, and legacy branches removed — not disabled |
| All callers migrated | Every reference now targets the new contract; project compiles/typechecks |
| Tests on new contract | Legacy-behavior tests rewritten or deleted; new behavior covered |
| Zero residue | `ast-grep` / `rg` for old API names, flags, formats, and import paths returns zero hits |
| No dead weight | No unused imports, packages, types, or files left by the old path |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Clean demolition — old shape erased, every caller on the new contract, tests green on new behavior, zero residue |
| 1 | Residue remains — old references survive in code, tests, docs, or config |
| 2 | Build/tests broken — migration incomplete, callers or assertions not yet on the new shape |
| 3 | Migration stalled mid-flight — codebase is half old, half new (the forbidden state); finish or revert, never ship |
