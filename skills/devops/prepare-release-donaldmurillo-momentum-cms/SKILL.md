---
name: prepare-release
description: Prepare a patch/minor/major version release for all Momentum CMS packages. Bumps versions, verifies builds/tests, adds new packages to Nx release config, and commits. Triggers include "prepare release", "bump version", "release patch", or "/prepare-release".
argument-hint: <patch|minor|major>
allowed-tools: Bash(npx *), Bash(npm *), Bash(grep *), Bash(find *), Bash(ls *), Bash(git *), Read, Glob, Grep, Edit, Write
---

# Prepare Release Skill

Prepare a new version release for all `@momentumcms/*` packages in the monorepo.

## Inputs

- **bump type**: `patch` (default), `minor`, or `major` from the argument
- If no argument provided, default to `patch`

## Step 1: Determine Current Version

Find the current version from any lib's `package.json`:

```bash
grep '"version"' libs/core/package.json
```

All packages share the same version (lockstep versioning).

## Step 2: Calculate New Version

Given current version `X.Y.Z`:

- `patch` -> `X.Y.(Z+1)`
- `minor` -> `X.(Y+1).0`
- `major` -> `(X+1).0.0`

## Step 3: Verify New Packages Are in Nx Release Config

Read `nx.json` and check the `release.projects` array. Every library in `libs/` and `libs/plugins/` that has a `package.json` with `@momentumcms/` name MUST be in this array.

To find all publishable packages:

```bash
grep -r '"@momentumcms/' libs/*/package.json libs/plugins/*/package.json apps/create-momentum-app/package.json | grep '"name"'
```

Compare against `release.projects` in `nx.json`. If any are missing:

1. Add them to the `release.projects` array in `nx.json`
2. Verify the package's `project.json` has an `nx-release-publish` target:
   ```json
   "nx-release-publish": {
       "options": {
           "packageRoot": "dist/{projectRoot}",
           "access": "public"
       }
   }
   ```

## Step 4: Bump All Versions

Replace the old version with the new version in ALL publishable `package.json` files. This includes:

- The `"version"` field
- Any `"@momentumcms/*"` dependency references

```bash
find libs apps/create-momentum-app -name "package.json" -not -path "*/node_modules/*" -exec grep -l "OLD_VERSION" {} \; | while read f; do
  sed -i '' "s/OLD_VERSION/NEW_VERSION/g" "$f"
done
```

Verify no old version references remain:

```bash
grep -r "OLD_VERSION" libs/*/package.json libs/plugins/*/package.json apps/create-momentum-app/package.json
```

## Step 5: Run Full Test Suite

Run the full test suite to verify nothing is broken:

```bash
npm run test:all -- --skip cli-scaffold
```

The CLI scaffold test is slow and unrelated to library code; skip it unless the release includes CLI template changes.

Check results:

- **Unit Tests**: Must pass (0 failures)
- **Angular E2E**: Must pass
- **Analog E2E**: Must pass (flaky tests that retry and pass are OK)
- **Migration Tests**: Must pass

## Step 6: Build All Packages

```bash
npx nx run-many -t build
```

All packages must build successfully.

## Step 7: Verify Dist Versions

Spot-check that dist output has the correct version:

```bash
grep '"version"' dist/libs/core/package.json dist/libs/plugins/redirects/package.json
```

## Step 8: Commit

Stage and commit with a conventional commit message:

```
chore(release): bump version to X.Y.Z

Bump all @momentumcms/* packages from OLD to NEW.
[Include any notable additions like new packages]
```

## Step 9: Summary

Print a summary:

- Old version -> New version
- Number of packages bumped
- Any new packages added to release config
- Test results
- Reminder: `npx nx release publish` to publish to npm (do NOT run this automatically)

## Important Notes

- **Never run `npx nx release publish`** without explicit user confirmation
- All packages use lockstep versioning (same version number)
- The root `package.json` version (`0.0.0`) is intentionally static and should NOT be bumped
- `conventionalCommits: true` in nx.json means Nx Release can auto-determine version bumps from commit messages, but this skill does manual bumps for explicit control
- Always verify the `nx-release-publish` target exists in new packages' `project.json` before releasing
