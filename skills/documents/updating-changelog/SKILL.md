---
name: updating-changelog
description: Updates changelog documentation for contract developers and node operators by analyzing branch changes relative to 'next'. Use when preparing a PR, updating migration notes, documenting breaking changes, or when asked to update changelog/release notes.
---

# Updating Changelog

## Steps

### 1. Determine Target Files

Read `.release-please-manifest.json` to get the version (e.g., `{"." : "4.0.0"}` → edit `v4.md`).

**Target files:**

- Aztec contract developers: `docs/docs-developers/docs/resources/migration_notes.md`
- Node operators and Ethereum contract developers: `docs/docs-network/reference/changelog/v{major}.md`

### 2. Analyze Branch Changes

Run `git diff next...HEAD --stat` for overview, then `git diff next...HEAD` for details.

**Categorize changes:**

- Breaking changes (API modifications, removals, renames)
- New features (APIs, CLI flags, configuration)
- Deprecations
- Configuration changes (CLI flags, environment variables)

### 3. Generate Draft Entries

Present draft entries for review BEFORE editing files. Match the formatting conventions by reading existing entries in each file.

### 4. Edit Documentation

After approval, add entries to the appropriate files.

## Migration Notes Format

**File:** `docs/docs-developers/docs/resources/migration_notes.md`

Add entries under `## TBD` section:

````markdown
### [Component] Brief description

Explanation of what changed.

**Migration:**

```diff
- old code
+ new code
```
````

**Impact**: Effect on existing code.

**Component tags:** `[Aztec.nr]`, `[Aztec.js]`, `[PXE]`, `[Aztec Node]`, `[AVM]`, `[L1 Contracts]`, `[CLI]`

## Node Operator Changelog Format

**File:** `docs/docs-network/reference/changelog/v{major}.md`

**Breaking changes:**
````markdown
### Feature Name

**v{previous}:**
```bash
--old-flag <value>                    ($OLD_ENV_VAR)
```

**v{current}:**
```bash
--new-flag <value>                    ($NEW_ENV_VAR)
```

**Migration**: How to migrate.
````

**New features:**
````markdown
### Feature Name

```bash
--new-flag <value>                    ($ENV_VAR)
```

Description of the feature.
````

**Changed defaults:** Use table format with Flag, Environment Variable, Previous, New columns.
