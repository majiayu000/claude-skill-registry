---
name: node-deps
description: This skill should be used when the user asks to "update dependencies", "update npm packages", "run taze", "upgrade node packages", "check for outdated packages", "update package.json", or mentions dependency updates, npm/pnpm/yarn package upgrades, or taze CLI usage.
---

# Node Dependencies Update Skill

Update Node.js dependencies using taze CLI with smart prompting: auto-apply MINOR/PATCH updates, prompt for MAJOR updates individually, skip fixed-version packages.

## Prerequisites

Before starting, verify taze is installed by running:

```bash
~/.claude/skills/node-deps/scripts/run-taze.sh
```

If exit code is 1, stop and inform the user that taze must be installed:

- Global install: `npm install -g taze`
- One-time: `nlx taze`

## Update Workflow

### Step 1: Determine Scope

Ask the user if this is a monorepo project. Use the `-r` flag for recursive scanning of workspaces.

### Step 2: Scan for Updates

Run the taze script to discover all available updates:

```bash
# Single package
~/.claude/skills/node-deps/scripts/run-taze.sh

# Monorepo (recursive)
~/.claude/skills/node-deps/scripts/run-taze.sh -r
```

### Step 3: Parse and Categorize Updates

From the taze output, categorize each package update:

| Category  | Version Change                              | Action        |
| --------- | ------------------------------------------- | ------------- |
| **Fixed** | No `^` or `~` prefix (e.g., `"1.0.0"`)      | Skip entirely |
| **PATCH** | `x.y.z` → `x.y.Z` (e.g., `1.0.0` → `1.0.1`) | Auto-apply    |
| **MINOR** | `x.y.z` → `x.Y.0` (e.g., `1.0.0` → `1.1.0`) | Auto-apply    |
| **MAJOR** | `x.y.z` → `X.0.0` (e.g., `1.0.0` → `2.0.0`) | Prompt user   |

**Identifying fixed versions:** In package.json, fixed versions have no range prefix:

- Fixed: `"lodash": "4.17.21"` → skip
- Ranged: `"lodash": "^4.17.21"` → process

### Step 4: Apply MINOR/PATCH Updates

Apply all non-major updates automatically without prompting:

```bash
# Single package
taze minor --write

# Monorepo
taze minor --write -r
```

Report the packages that were updated.

### Step 5: Prompt for MAJOR Updates

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

### Step 6: Apply Approved MAJOR Updates

After collecting user approvals, apply the approved major updates:

```bash
# Apply specific packages
taze major --write --include <pkg1>,<pkg2>,<pkg3>

# With monorepo
taze major --write -r --include <pkg1>,<pkg2>,<pkg3>
```

### Step 7: Install Dependencies

After all updates are applied, remind the user to run their package manager's install command:

```bash
npm install
# or
pnpm install
# or
yarn install
```

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

| Script                     | Purpose                                              |
| -------------------------- | ---------------------------------------------------- |
| `./scripts/run-taze.sh`    | Run taze in non-interactive mode, check installation |
| `./scripts/run-taze.sh -r` | Same with recursive monorepo scanning                |

## Important Notes

- Fixed-version dependencies (no `^` or `~`) indicate intentional pinning—never modify these
- MAJOR updates may contain breaking changes—always prompt the user
- MINOR/PATCH updates are backward-compatible by semver convention—safe to auto-apply
- The `--include` flag accepts comma-separated package names or regex patterns
