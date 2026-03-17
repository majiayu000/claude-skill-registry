---
argument-hint: '[package ...]'
disable-model-invocation: false
name: bump-deps
user-invocable: true
description: This skill should be used when the user asks to "update dependencies", "update npm packages", "bump dependencies", "upgrade node packages", "check for outdated packages", "update package.json", or mentions dependency updates, npm/pnpm/yarn/bun package upgrades, or taze CLI usage.
---

# Bump Dependencies Skill

Update Node.js dependencies using taze CLI with smart prompting: auto-apply MINOR/PATCH updates, prompt for MAJOR updates individually, skip fixed-version packages.

When package names are provided as arguments (e.g. `/bump-deps react typescript`), scope all taze commands to only those packages using `--include`.

## Prerequisites

Before starting, verify taze is installed by running:

```bash
scripts/run-taze.sh
```

If exit code is 1, stop and inform the user that taze must be installed:

- Global install: `npm install -g taze`
- One-time: `npx taze`

## Update Workflow

### Step 1: Scan for Updates

Run the taze script to discover available updates. The script auto-detects monorepo projects (`workspaces` in package.json or `pnpm-workspace.yaml`) and enables recursive mode automatically.

```bash
scripts/run-taze.sh
```

### Step 2: Parse and Categorize Updates

From the taze output, categorize each package update:

| Category  | Version Change                              | Action        |
| --------- | ------------------------------------------- | ------------- |
| **Fixed** | No `^` or `~` prefix (e.g., `"1.0.0"`)      | Skip entirely |
| **PATCH** | `x.y.z` → `x.y.Z` (e.g., `1.0.0` → `1.0.1`) | Auto-apply    |
| **MINOR** | `x.y.z` → `x.Y.0` (e.g., `1.0.0` → `1.1.0`) | Auto-apply    |
| **MAJOR** | `x.y.z` → `X.0.0` (e.g., `1.0.0` → `2.0.0`) | Prompt user   |

If package arguments were provided, filter to only those packages.

**Identifying fixed versions:** In package.json, fixed versions have no range prefix:

- Fixed: `"lodash": "4.17.21"` → skip
- Ranged: `"lodash": "^4.17.21"` → process

### Step 3: Apply MINOR/PATCH Updates

Apply all non-major updates automatically without prompting:

```bash
# All packages
taze minor --write

# Specific packages only (when args provided)
taze minor --write --include react,typescript
```

The script auto-detects monorepo mode, but when running taze directly, detect it yourself: check for `workspaces` in package.json or `pnpm-workspace.yaml` and add `-r` if present.

Report the packages that were updated.

### Step 4: Prompt for MAJOR Updates

**Auto-skip packages:** Never prompt for these packages—auto-apply their major updates:

- `lucide-react` (icon library with frequent major bumps, backward-compatible in practice)

For each remaining package with a major update available, use `AskUserQuestion` to ask the user individually:

```
Package: <package-name>
Current: <current-version>
Available: <new-version>

Update to major version?
```

**Question format:**

- header: Package name (max 12 chars, truncate if needed)
- options: "Yes, update" / "No, skip"
- multiSelect: false

Collect all approved major updates.

### Step 5: Apply Approved MAJOR Updates

After collecting user approvals, apply the approved major updates:

```bash
taze major --write --include <pkg1>,<pkg2>,<pkg3>
```

Add `-r` if monorepo was detected.

### Step 6: Update Bun Catalogs

After applying all updates, check the **root** `package.json` for Bun workspace catalogs. Bun monorepos can centralize dependency versions using `catalog` and `catalogs` fields inside the `workspaces` object:

```json
{
  "workspaces": {
    "packages": ["packages/*"],
    "catalog": {
      "react": "^19.0.0"
    },
    "catalogs": {
      "testing": {
        "jest": "^30.0.0"
      }
    }
  }
}
```

Workspace packages reference these with `"react": "catalog:"` (default catalog) or `"jest": "catalog:testing"` (named catalog).

**Skip this step** if neither `workspaces.catalog` nor `workspaces.catalogs` exists in the root `package.json`.

For each package that was updated in Steps 3/5:

1. Check if it appears in `workspaces.catalog` — if so, update the version there
2. Check each named catalog in `workspaces.catalogs` — if the package appears, update the version there

Preserve the existing range prefix (`^`, `~`, or none) from the catalog entry. For example, if the catalog has `"react": "^19.0.0"` and taze bumped react to `19.1.0`, update the catalog to `"react": "^19.1.0"`.

Use `Edit` to apply the version changes directly to the root `package.json`.

### Step 7: Install Dependencies

After all updates are applied, run `ni` to install dependencies. It auto-detects the package manager.

## Taze Output Interpretation

Taze displays updates grouped by type. Example output:

```
@types/node  ^20.0.0  →  ^22.0.0   (major)
typescript   ^5.3.0   →  ^5.4.0    (minor)
eslint       ^8.56.0  →  ^8.57.0   (patch)
```

The rightmost column indicates update type (major/minor/patch).

Packages shown with `--include-locked` that have no `^` or `~` are fixed versions—skip these entirely.

## Script Reference

| Script                | Purpose                                              |
| --------------------- | ---------------------------------------------------- |
| `scripts/run-taze.sh` | Run taze in non-interactive mode, check installation |

## Important Notes

- Fixed-version dependencies (no `^` or `~`) indicate intentional pinning—never modify these
- MAJOR updates may contain breaking changes—always prompt the user
- MINOR/PATCH updates are backward-compatible by semver convention—safe to auto-apply
- The `--include` flag accepts comma-separated package names or regex patterns
- Monorepo detection is automatic—no flag needed
- Bun catalogs (`workspaces.catalog` / `workspaces.catalogs`) are the source of truth for workspace packages using the `catalog:` protocol—always update catalog entries alongside regular deps
