---
name: add-dependency
description: Add a dependency to a Lean project's lakefile. Use when adding requires, dependencies, or imports to a project.
---

# Add Dependency

Add dependencies to a Lean project with tier validation.

## Quick Start

1. Identify the project and dependency
2. Check tier ordering (can't depend on higher tiers)
3. Find the dependency's current version tag
4. Update lakefile.lean with require statement
5. Run `lake update` and `lake build`

## Dependency Tiers

Projects should only depend on projects in the same or lower tiers.

| Tier | Projects |
|------|----------|
| 0 | crucible, staple, cellar, assimptor, raster |
| 1 | herald, trellis, collimator, protolean, scribe, chronicle, terminus, fugue, linalg, chronos, measures, rune, tincture, wisp, chisel, ledger, quarry, convergent, reactive, tabular, entity, totem, conduit, tracer, smalltalk |
| 2 | citadel, legate, oracle, parlance, arbor, blockfall, twenty48, minefield, solitaire, stencil |
| 3 | loom, afferent, canopy, ask, lighthouse, enchiridion, docgen |
| 4 | todo-app, homebase-app, chroma, vane, worldmap, grove, cairn, afferent-demos |

## Require Statement Format

```lean
require <name> from git "https://github.com/nathanial/<repo>" @ "v0.0.X"
```

## Finding Current Version

```bash
cd <category>/<dependency>
git describe --tags --abbrev=0
```

Or check GitHub releases.

## Common Dependencies

| Dependency | Use Case | Require Statement |
|------------|----------|-------------------|
| crucible | Testing | `require crucible from git "https://github.com/nathanial/crucible" @ "v0.0.1"` |
| collimator | Optics/lenses | `require collimator from git "https://github.com/nathanial/collimator" @ "v0.0.1"` |
| terminus | TUI apps | `require terminus from git "https://github.com/nathanial/terminus" @ "v0.0.1"` |
| wisp | HTTP client | `require wisp from git "https://github.com/nathanial/wisp" @ "v0.0.1"` |
| chronos | Time/dates | `require chronos from git "https://github.com/nathanial/chronos-lean" @ "v0.0.1"` |

## External Dependencies

```lean
-- Mathlib (for collimator)
require mathlib from git "https://github.com/leanprover-community/mathlib4" @ "v4.X.0"

-- Batteries (for ledger)
require batteries from git "https://github.com/leanprover-community/batteries" @ "v4.X.0"

-- Plausible (for property testing)
require plausible from git "https://github.com/leanprover-community/plausible" @ "v4.X.0"
```

## After Adding

```bash
lake update   # Fetch new dependency
lake build    # Verify it builds
lake test     # Ensure tests still pass
```

## Tier Violation Warning

If adding a dependency from a higher tier, warn the user:

> ⚠️ Warning: Adding `<dep>` (Tier X) to `<project>` (Tier Y) violates tier ordering.
> This creates a circular dependency risk. Consider:
> - Moving `<project>` to a higher tier
> - Finding an alternative in a lower tier
> - Extracting shared code to a new lower-tier project
