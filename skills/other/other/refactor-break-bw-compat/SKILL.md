---
name: refactor-break-bw-compat
description: "Refactor by removing backward compatibility and legacy layers. Use when modernizing APIs, cleaning up migration debt, removing compat shims, or eliminating stale feature flags."
---

# Breaking Refactors — Freedom Through Structure

Compatibility layers are coupling debt with interest. Every compat shim is a decision deferred, not a decision avoided. Break cleanly, break once, break with evidence.

## Principles

1. **No half-measures.** A partial migration is worse than no migration — it doubles the surface area and confuses every reader.
2. **One migration direction.** Old-to-new only. Never add new-to-old adapters; that entrenches the old path.
3. **Blast radius awareness.** Map every consumer before removing anything. Surprise breakage is a planning failure, not a courage signal.
4. **Dead code is a lie.** "Just in case" code is not dead — it actively misleads readers about what the system does.
5. **Compat shims are temporary.** If a shim has no removal date, it is permanent. If it is permanent, it is architecture. Decide which.

## Reconnaissance Checklist

Before breaking anything, find and catalog:

- `@deprecated` / `#[deprecated]` / `warnings.warn` markers — especially ones without removal versions
- Version-gated code paths (`if version >= X`, feature flags, `#[cfg(feature = "legacy")]`)
- Adapter / shim / bridge / wrapper layers that translate between old and new interfaces
- Dual serialization formats (v1/v2 JSON schemas, protobuf `oneof` with legacy fields)
- Tests that exist solely to validate backward-compatible behavior
- Configuration keys that toggle between old and new behavior
- Re-export / forwarding modules that alias old paths to new locations
- Changelog entries promising deprecation timelines

## Decision: Break or Not?

| Signal | Break | Do NOT Break |
|--------|-------|--------------|
| Zero external consumers | Yes | — |
| Single internal consumer, you own it | Yes | — |
| Well-tested, high coverage | Yes | — |
| Clear new path exists | Yes | — |
| External/public API with unknown consumers | — | Not without migration plan |
| No tests covering the boundary | — | Write tests first, then break |
| Multiple consumers, unclear ownership | — | Map consumers first |
| Compat layer under active use by migration-in-progress | — | Finish migration first |

## Execution Strategy

1. **Map blast radius.** List every file, module, and external consumer that references the old API. Use `ast-grep`, `rg`, or equivalent — not guesswork.
2. **Snapshot current behavior.** Ensure tests cover the old path. If coverage is missing, add characterization tests before removal.
3. **Remove the old path.** Delete the compat layer, adapter, or legacy code. Do not comment it out.
4. **Update all call sites.** Migrate every reference found in step 1 to the new API. Compile/typecheck after each batch.
5. **Delete orphaned tests.** Tests that validated the old path are now dead weight. Remove them.
6. **Search for ghosts.** Grep for string references, config keys, environment variables, documentation links, and error messages that mention the old API.
7. **Verify no dead imports/deps.** Check for unused imports, packages, or dependencies that only the old path required.

## Anti-patterns

- **"Just in case" paths** — keeping old code "in case someone needs it." That is what version control is for.
- **Partial migration** — half the codebase on new API, half on old. Worse than either alone.
- **Commenting out instead of deleting** — commented code is invisible debt that greps cannot find.
- **Compat-of-compat** — wrapping a compat layer in another compat layer. Two wrongs do not make an abstraction.
- **Deprecated without removal date** — a deprecation warning without a deadline is a suggestion, not a plan.
- **Stale feature flags** — flags that are always on (or always off) in every environment. Delete the flag, keep the winning path.

## Validation Gates

| Gate | Condition |
|------|-----------|
| Blast radius mapped | Every consumer of old API identified and listed |
| Tests green pre-removal | Existing tests pass before any deletion begins |
| Zero references post-removal | `ast-grep` / `rg` for old API names returns zero hits |
| No dead imports/deps | No unused imports, packages, or type declarations remain |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Clean break — old API fully removed, all consumers migrated, tests pass |
| 1 | Partial — old references remain in code, docs, or config |
| 2 | Tests broken — removal caused test failures not yet resolved |
| 3 | External consumers found — need migration plan before proceeding |
