---
name: to-greenfield
description: 'Greenfield recovery for a degraded codebase: diagnose its field state, route the fix. Use when the user says "to greenfield" or "greenfield this", asks to rescue a codebase, or names a field — darkfield (undocumented, no tests), redfield (broken, failing), brownfield (legacy but working), bluefield (half-migrated, two coexisting paths).'
metadata:
  short-description: 'Field-state diagnosis, routed recovery to greenfield'
---

# To greenfield

Greenfield is the exit state, not the starting point: a codebase a newcomer could extend without archaeology. Every degraded codebase sits in one of four fields, and each field has exactly one route out. The lattice is fixed: **darkfield**, **redfield**, and **bluefield** each resolve into **brownfield**; brownfield resolves into **greenfield**. Diagnose first, route second, converge on the shared exit criteria.

## Diagnose the field

| Field | Observable signals | Route |
|---|---|---|
| **redfield** | Verifier fails; active regressions; red CI; broken build | Redfield → green |
| **darkfield** | No tests, no docs; structure unclear; fog of war — nobody can say what a change would break | Darkfield → light |
| **bluefield** | Two coexisting implementations of one concern: old/new dirs, migration flags, `v2` suffixes, TODO-migrate markers | Bluefield → one path |
| **brownfield** | Green and working, but compat shims, legacy patterns, dead weight | Brownfield → greenfield |

Signals mix; precedence settles it: **red trumps all** (a broken bluefield is redfield until green), then darkfield, then bluefield, then brownfield. Large repos get a per-subsystem field map — different subsystems may sit in different fields and take different routes.

**Completion criterion:** every subsystem in scope is assigned exactly one field with cited evidence (paths, verifier output). None left uncolored.

## Routes

Each route is a sequence of existing skills, invoked by name. This skill owns the routing and the exit tests; the invoked skills own their own doctrine.

### Darkfield → light

Map before touching — never refactor in fog.

1. Invoke `odin:explore` to map structure, symbols, and dependencies.
2. Invoke `odin:tests-adversarial` to pin current behavior with characterization tests around every subsystem you will later touch.
3. Invoke `odin:init` to write the newcomer doc capturing what the mapping found.

**Exit:** re-run Diagnose; the subsystem now reads as brownfield (or redfield, if mapping exposed breakage — route there next).

### Redfield → green

Stabilize only — no refactors while red.

1. Invoke `odin:fix` on each failure; take the smallest change that reaches green.
2. Quarantine flaky tests with a tracking note rather than deleting them.

**Exit:** verifier green twice consecutively; re-run Diagnose and take the next route.

### Bluefield → one path

Finish the migration, kill the old path — never add a third path.

1. Invoke `odin:deprecate-and-migrate` to move every remaining caller onto the new path.
2. Invoke `odin:refactor-break-compat` to delete the old path and its shims outright.

**Exit:** one implementation per concern; the old path is deleted, not deprecated-in-place. Re-run Diagnose.

### Brownfield → greenfield

Characterize, then attack.

1. Invoke `odin:tests-adversarial` to pin behavior where coverage is thin.
2. Invoke `odin:refactor-break-compat` for the offensive refactor: replace structures, remove shims.
3. Invoke `odin:cleanup-codebase` to sweep dead code, duplication, and ceremony.

**Exit:** the greenfield criteria below.

## Greenfield exit criteria

All five, checked with evidence:

1. Verifier green.
2. Every touched subsystem has behavior-pinning tests.
3. Exactly one path per concern — no shims, no dual implementations, no dead code.
4. A newcomer doc exists and matches reality.
5. Re-running Diagnose assigns **no** color to any subsystem in scope.

**Completion criterion:** all five confirmed with evidence, or the remaining field states reported with their next route.
