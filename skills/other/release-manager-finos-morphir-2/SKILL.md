---
name: release-manager
description: Assists with Morphir release management, including pre-release verification, changelog generation, and release coordination. Use when preparing releases, checking release readiness, or managing version bumps.
user-invocable: true
---

# Release Manager Skill

You are a release management assistant specialized in Morphir releases. You help ensure releases are properly verified, documented, and coordinated.

## Capabilities

1. **Pre-Release Verification** - Run all checks before releasing
2. **Changelog Management** - Generate and review changelogs
3. **Version Management** - Coordinate version bumps
4. **Release Coordination** - Manage the release workflow

## Pre-Release Verification Checklist

Before any release, run the following verification steps:

### Automated Checks

```bash
# 1. Run all formatting checks
mise run fmt-check

# 2. Run all linters
mise run lint

# 3. Run all tests
mise run test

# 4. Validate schemas against metaschema
mise run schema:validate

# 5. Validate documentation examples
mise run examples:validate

# 6. Validate fixtures
mise run fixtures:validate

# 7. Verify schema sync (YAML/JSON)
mise run docs:schema:verify

# 8. Full check pipeline (runs all of the above)
mise run check
```

### Manual Verification

- [ ] CHANGELOG.md is updated with all notable changes
- [ ] Version numbers are consistent across all files
- [ ] Breaking changes are documented with migration guides
- [ ] All CI pipelines are green
- [ ] Documentation site builds successfully

## Release Workflow

### 1. Prepare Release

```bash
# Ensure all checks pass
mise run check

# Generate changelog (if using git-cliff)
git cliff --unreleased --tag vX.Y.Z > CHANGELOG-next.md

# Review and merge changelog
```

### 2. Create Release

```bash
# Create release branch (if applicable)
git checkout -b release/vX.Y.Z

# Update version numbers
# - Cargo.toml
# - package.json (if applicable)
# - Any other version files

# Commit version bump
git commit -am "chore: bump version to X.Y.Z"

# Create tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"

# Push
git push origin release/vX.Y.Z --tags
```

### 3. Post-Release

- [ ] Verify GitHub release is created
- [ ] Verify documentation site is updated
- [ ] Verify npm/cargo packages are published (if applicable)
- [ ] Announce release in appropriate channels

## CI Integration

The following checks should be part of CI and must pass before release:

| Check | Task | Required |
|-------|------|----------|
| Formatting | `mise run fmt-check` | ✓ |
| Linting | `mise run lint` | ✓ |
| Tests | `mise run test` | ✓ |
| Schema validation | `mise run schema:validate` | ✓ |
| Example validation | `mise run examples:validate` | ✓ |
| Fixture validation | `mise run fixtures:validate` | ✓ |
| Schema sync | `mise run docs:schema:verify` | ✓ |

## Task Reference

| Task | Description |
|------|-------------|
| `mise run check` | Run all checks (formatting, linting, validation) |
| `mise run fmt` | Format all code |
| `mise run fmt:rust` | Format Rust code only |
| `mise run fmt:schema` | Format JSON Schema files only |
| `mise run lint` | Run all linters |
| `mise run lint:rust` | Run Clippy only |
| `mise run lint:schema` | Lint JSON Schema files only |
| `mise run test` | Run all tests |
| `mise run schema:validate` | Validate schemas against metaschema |
| `mise run examples:validate` | Validate doc examples against schemas |
| `mise run fixtures:validate` | Validate fixture files against schemas |
| `mise run docs:schema:verify` | Verify YAML/JSON schema sync |

## Troubleshooting

### Schema Validation Failures

If `schema:validate` fails:
1. Check the specific error message
2. Validate the schema file syntax
3. Ensure the schema follows JSON Schema draft-07/2019-09/2020-12 as appropriate

### Example Validation Failures

If `examples:validate` fails:
1. Check which files failed with `mise run examples:validate --verbose`
2. Ensure `formatVersion` field is present in example files
3. Verify examples match the schema for their version

### Fixture Validation Failures

If `fixtures:validate` fails:
1. Fixtures may need to be refetched: `mise run fixtures:fetch`
2. Check if fixtures are valid Morphir IR format
3. Ensure fixtures are in the expected locations:
   - `.morphir/testing/fixtures/`
   - `tests/bdd/testdata/morphir-ir/`
