---
name: release
description: Prepare and execute a release to pub.dev. Bumps versions, validates changelogs, checks pub.dev status, and guides through the tiered publishing process.
argument-hint: "<version>"
disable-model-invocation: true
allowed-tools: Bash, Read, Grep, Glob, WebFetch
---

# Release to pub.dev

Prepare and execute a dart_node release. This is a multi-step process that publishes packages in tiers due to interdependencies.

## Arguments

`$ARGUMENTS` = version to release (e.g., `0.12.0-beta`, `1.0.0`)

If no version provided, show current versions and prompt for the target version.

## Step 1: Pre-flight checks

### 1.1 Verify clean state

```bash
git status
git branch --show-current
```

- Must be on `main` branch (or create a release branch)
- Working directory should be clean

### 1.2 Check current versions

```bash
grep -h "^version:" packages/*/pubspec.yaml | head -20
```

### 1.3 Validate all packages have configs

```bash
dart run tools/prepare_publish.dart 2>&1 || true
```

This shows any packages missing from `tools/lib/packages.dart`.

## Step 2: Switch dependencies to pub.dev versions

**CRITICAL**: Before publishing, all internal dependencies must point to pub.dev versions, NOT local paths!

Use `tools/switch_deps.dart` to switch:

```bash
# Switch from local paths to pub.dev versioned dependencies
dart run tools/switch_deps.dart release
```

This converts:
```yaml
# FROM (local development):
dart_node_core:
  path: ../dart_node_core

# TO (release):
dart_node_core: ^0.11.0-beta
```

To switch back to local for development:

```bash
dart run tools/switch_deps.dart local
```

**Note**: The CI workflow handles this automatically on the release branch.

## Step 3: Validate changelogs

Every publishable package must have a `## $ARGUMENTS` entry in its CHANGELOG.md.

**Publishable packages** (must have changelog entries):

| Tier | Package |
|------|---------|
| 1 | dart_logging |
| 1 | dart_node_core |
| 2 | reflux |
| 2 | dart_node_express |
| 2 | dart_node_ws |
| 2 | dart_node_better_sqlite3 |
| 2 | dart_node_mcp |
| 3 | dart_node_react |
| 3 | dart_node_react_native |

Check each changelog:

```bash
VERSION="$ARGUMENTS"
for pkg in dart_logging dart_node_core reflux dart_node_express dart_node_ws dart_node_better_sqlite3 dart_node_mcp dart_node_react dart_node_react_native; do
  if grep -q "^## $VERSION" "packages/$pkg/CHANGELOG.md" 2>/dev/null; then
    echo "✅ $pkg"
  else
    echo "❌ $pkg - missing ## $VERSION entry"
  fi
done
```

If any are missing, **stop and update the changelogs** before proceeding.

## Step 4: Validate READMEs

Each package should have a README.md. Quick sanity check:

```bash
for pkg in dart_logging dart_node_core reflux dart_node_express dart_node_ws dart_node_better_sqlite3 dart_node_mcp dart_node_react dart_node_react_native; do
  if [[ -f "packages/$pkg/README.md" ]]; then
    LINES=$(wc -l < "packages/$pkg/README.md")
    echo "✅ $pkg - $LINES lines"
  else
    echo "❌ $pkg - missing README.md"
  fi
done
```

## Step 5: Check pub.dev status

Verify which versions are currently published:

```bash
for pkg in dart_logging dart_node_core reflux dart_node_express dart_node_ws dart_node_better_sqlite3 dart_node_mcp dart_node_react dart_node_react_native; do
  LATEST=$(curl -s "https://pub.dev/api/packages/$pkg" | grep -o '"version":"[^"]*"' | head -1 | cut -d'"' -f4)
  echo "$pkg: $LATEST"
done
```

## Step 6: Run tests

Before releasing, ensure all tests pass:

```bash
./tools/test.sh
```

Or run specific tiers:

```bash
./tools/test.sh --tier 1
./tools/test.sh --tier 2
./tools/test.sh --tier 3
```

## Step 7: Bump versions (dry run)

Preview what changes the prepare script will make:

```bash
dart run tools/prepare_publish.dart $ARGUMENTS
```

This updates:
- `version:` in all pubspec.yaml files
- Interdependencies to use `^$ARGUMENTS` (pub.dev versions)
- Removes `publish_to: none`

**Do NOT commit these changes yet** - they are made on a release branch by CI.

## Step 8: Create release tag

The release is triggered by pushing a tag:

```bash
git tag "Release/$ARGUMENTS"
git push origin "Release/$ARGUMENTS"
```

This triggers the **publish-tier1** workflow which:
1. Creates a `release/$ARGUMENTS` branch
2. Runs `prepare_publish.dart`
3. Creates a PR to main
4. Publishes dart_logging and dart_node_core

## Step 9: Tier 2 publishing

After tier 1 succeeds and packages are live on pub.dev (wait ~5 minutes for indexing):

```bash
git tag "Release-Tier2/$ARGUMENTS"
git push origin "Release-Tier2/$ARGUMENTS"
```

Publishes: reflux, dart_node_express, dart_node_ws, dart_node_better_sqlite3, dart_node_mcp

## Step 10: Tier 3 publishing

After tier 2 succeeds:

```bash
git tag "Release-Tier3/$ARGUMENTS"
git push origin "Release-Tier3/$ARGUMENTS"
```

Publishes: dart_node_react, dart_node_react_native

After tier 3 completes, it switches dependencies back to local and pushes to the release branch.

## Step 11: Merge the release PR

After all tiers complete successfully:

1. Go to the PR created by tier 1
2. Verify all packages are published on pub.dev
3. Merge the PR to main

## Verification

After release, verify all packages are available:

```bash
VERSION="$ARGUMENTS"
for pkg in dart_logging dart_node_core reflux dart_node_express dart_node_ws dart_node_better_sqlite3 dart_node_mcp dart_node_react dart_node_react_native; do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "https://pub.dev/api/packages/$pkg/versions/$VERSION")
  if [[ "$HTTP_CODE" == "200" ]]; then
    echo "✅ $pkg@$VERSION published"
  else
    echo "❌ $pkg@$VERSION not found (HTTP $HTTP_CODE)"
  fi
done
```

## Troubleshooting

### Package already published
If a package version already exists, the publish script skips it. This is safe.

### Dependency resolution fails
Tier 2/3 packages depend on tier 1. Wait for tier 1 to be fully indexed on pub.dev before starting tier 2.

### Changelog validation fails
Add the missing `## X.Y.Z` header to the package's CHANGELOG.md with release notes.

## Checklist summary

- [ ] On main branch, clean working directory
- [ ] **No local path dependencies** (all point to pub.dev versions)
- [ ] All changelogs have `## $ARGUMENTS` entries
- [ ] All READMEs are present and up-to-date
- [ ] All tests pass
- [ ] `Release/$ARGUMENTS` tag pushed (triggers tier 1)
- [ ] Tier 1 complete, packages live on pub.dev
- [ ] `Release-Tier2/$ARGUMENTS` tag pushed
- [ ] Tier 2 complete, packages live on pub.dev
- [ ] `Release-Tier3/$ARGUMENTS` tag pushed
- [ ] Tier 3 complete, packages live on pub.dev
- [ ] Release PR merged to main
