---
name: new-export-version
description: Create a new game export schema version, migration module, and related tests.
---

# New Export Version

Cut a new game export format version. This creates a standalone schema, migration module, and updates all references.

## Background

Each export version has its own schema file (`schemas/game-export-vN.schema.json`). Migrations live in `schemas/migrations/` as modules with `up(data)` and `down(data)` functions. The shared runner at `scripts/migrate_exports.py` handles file I/O, chaining, and CLI.

Key files:

- `schemas/game-export-v*.schema.json` — per-version JSON Schemas
- `schemas/migrations/` — migration modules and registry (`__init__.py`)
- `scripts/migrate_exports.py` — unified migration runner
- `scripts/export_game.py` — export producer (sets version, computes new fields)
- `puppeteer/tests/test_migrate_exports.py` — roundtrip and runner tests
- `puppeteer/tests/test_export_schema.py` — schema validation tests

## Step 1: Determine what's changing

Ask the user what fields are being added, removed, or modified. Determine:

- The current version number N (check the `"version"` line in `scripts/export_game.py`)
- What new fields to add and their JSON Schema types
- Whether the `up()` migration needs external data or is purely derived from existing fields
- Whether the `down()` migration is lossless (can we reconstruct N from N+1?)

Before deciding on a version bump for a semantics-only fix, check whether the
latest typed loaders (`load_game_export`, `load_built_game_export`) are used
directly against committed exports in tests or scripts. If they only accept the
newest version, a code-only version bump can break local consumers until the
repo's game exports are migrated too. In that case, consider whether an
in-place backfill on the existing version is the safer path.

## Step 2: Create the new schema file

Copy `schemas/game-export-vN.schema.json` to `schemas/game-export-v{N+1}.schema.json`:

- Change `"const": N` to `"const": N+1` in the `version` property
- Update `$id`, `title`, `description` to reference v{N+1}
- Add new fields to `properties`
- Add new `$defs` if needed

## Step 3: Create the migration module

Create `schemas/migrations/vN_to_v{N+1}.py`:

```python
"""Migration: vN -> v{N+1} (description of what changes)."""

SOURCE_VERSION = N
TARGET_VERSION = N + 1

def up(data: dict) -> dict:
    """Migrate from vN to v{N+1}."""
    assert data["version"] == N, f"Expected vN, got v{data['version']}"
    # Add new fields here
    data["version"] = N + 1
    return data

def down(data: dict) -> dict:
    """Migrate from v{N+1} to vN."""
    assert data["version"] == N + 1, f"Expected v{N+1}, got v{data['version']}"
    # Remove new fields here
    data["version"] = N
    return data
```

The migration must satisfy: `down(up(game)) == game` for all exported games.

## Step 4: Register the migration

Add the new module to `schemas/migrations/__init__.py`:

```python
from schemas.migrations import ..., vN_to_v{N+1}

MIGRATIONS = [
    ...,
    vN_to_v{N+1},
]
```

## Step 5: Update `scripts/export_game.py`

1. Change `"version": N` to `"version": N+1` in `build_export()`
2. Add computation for new fields in `build_export()`
3. Update `_validate_export()`: change `version == N` to `version == N+1`
4. Update the comment referencing the schema filename

## Step 6: Update schema references

These files reference the schema filename and need updating:

- `Makefile` (`regen-schema-types` and `verify-schema-types` targets) → `game-export-v{N+1}.schema.json`
- `.claude/hooks/enforce-agents-rules.py` — no change needed (uses glob pattern)
- `doc/export-schema.md` — update prose reference if it mentions a specific version

## Step 7: Regenerate TypeScript types

```bash
make regen-schema-types
```

Verify the generated types look correct in `website/src/types/game-export.d.ts`.

## Step 8: Add tests

In `puppeteer/tests/test_export_schema.py`, add:

- `test_v{N+1}_schema_is_valid` — validates the new schema structure
- `test_v{N+1}_schema_accepts_v{N+1}` — minimal valid export passes
- `test_v{N+1}_schema_rejects_vN` — old version is rejected

In `puppeteer/tests/test_migrate_exports.py`, add a new test class:

- `test_vN_to_v{N+1}_up_adds_fields` — verify up() adds the right fields
- `test_v{N+1}_to_vN_down_removes_fields` — verify down() strips them
- `test_round_trip_preserves_vN_structure` — `down(up(game)) == game`

## Step 9: Run checks

```bash
make check
```

All lint, typecheck, and tests must pass before proceeding.

## Step 10: Create the PR (code only — no data migration)

Do NOT migrate existing games in this PR. Game migrations touch hundreds of JSON files and GitHub cannot render large diffs. Instead:

1. Create the PR with only the code changes (schema, migration module, export_game.py, tests, docs, TypeScript types).
2. In the PR description, note that a follow-up data-only PR will migrate existing games.

## Step 11: Update documentation

- `schemas/migrations/README.md` — update the "Current state" section

## Step 12: Follow-up PR — migrate existing games

After the code PR merges, create a second data-only PR:

```bash
# Preview first
uv run python scripts/migrate_exports.py --to {N+1} --dry-run

# Then migrate for real
uv run python scripts/migrate_exports.py --to {N+1}

# Verify checks still pass with migrated data
make check
```

Commit and PR the migrated game files separately. This keeps the code review clean and avoids GitHub choking on large diffs.
