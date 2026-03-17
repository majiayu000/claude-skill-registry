---
argument-hint: '[version] [--beta] [--dry-run]'
disable-model-invocation: false
name: bump-release
user-invocable: true
description: This skill should be used when the user asks to "bump release", "cut a release", "tag a release", "bump version", "create a new release", or mentions release versioning, changelog updates, or version tagging workflows.
---

# Bump Release

Support for both regular and beta releases.

## Parameters

- `version`: Optional explicit version to use (e.g., `2.0.0`). When provided, skips automatic version inference
- `--beta`: Create a beta release with `-beta.X` suffix
- `--dry-run`: Preview the release without making any changes (no file modifications, commits, or tags)

## Steps

0. **Locate the package** - The user may be in a monorepo where the package to release lives in a subdirectory. Look for `package.json` in the current working directory first; if not found, ask which package to release. All file paths (`CHANGELOG.md`, `package.json`, `justfile`) are relative to the package directory.
1. Update the `CHANGELOG.md` file with all changes since the last version release (**skip this step for beta releases**).
2. Bump the version in `package.json`:
   - **Regular release**: Follow semantic versioning (e.g., 1.2.3)
   - **Beta release**: Add `-beta.X` suffix (e.g., 1.2.3-beta.1)
3. **Format files** - If a `justfile` exists in the repository, run `just full-write` to ensure `CHANGELOG.md` and `package.json` are properly formatted
4. Commit the changes with a message like "docs: release <version>"
5. Create a new git tag by running `git tag -a v<version> -m "<version>"`

**Note**: When `--dry-run` flag is provided, display what would be done without making any actual changes to files, creating commits, or tags.

## Tasks

## Process

1. **Check for arguments** - Determine if `version` was provided, if this is a beta release (`--beta`), and/or dry-run (`--dry-run`)
2. **Check for clean working tree** - Run `git status --porcelain` to verify there are no uncommitted changes unrelated to this release. If there are, run the `commit` skill to commit them before proceeding
3. **Write Changelog** - Examine diffs between the current branch and the previous tag to write Changelog. Then find
   relevant PRs by looking at the commit history and add them to each changelog (when available). If `package.json` contains
   a `files` field, only include changes within those specified files/directories. If no `files` field exists, include all
   changes except test changes, CI/CD workflows, and development tooling
4. **Follow format** - Consult `references/common-changelog.md` for the Common Changelog specification
5. **Check version** - Get current version from `package.json`
6. **Bump version** - If `version` argument provided, use it directly. Otherwise, if unchanged since last release, increment per Semantic Versioning rules:
   - **For regular releases**:
     - **PATCH** (x.x.X) - Bug fixes, documentation updates
     - **MINOR** (x.X.x) - New features, backward-compatible changes
     - **MAJOR** (X.x.x) - Breaking changes
   - **For beta releases** (`--beta` flag):
     - If current version has no beta suffix: Add `-beta.1` to the version
     - If current version already has beta suffix: Increment beta number (e.g., `-beta.1` → `-beta.2`)
     - If moving from beta to release: Remove beta suffix and use the base version

## Beta Release Logic

When `--beta` flag is provided in the $ARGUMENTS

1. **Check for explicit version** - If `version` provided:
   - If version already has beta suffix → use as-is
   - If version has no beta suffix → append `-beta.1`
2. **Otherwise, parse current version** from `package.json` and **determine beta version**:
   - If current version is `1.2.3`: Create `1.2.4-beta.1` (increment patch + beta.1)
   - If current version is `1.2.3-beta.1`: Create `1.2.3-beta.2` (increment beta number)
   - If current version is `1.2.3-beta.5`: Create `1.2.3-beta.6` (increment beta number)
3. **Skip CHANGELOG.md update** - Beta releases don't update the changelog
4. **Commit and tag** with beta version (e.g., `v1.2.4-beta.1`)

## Output

For regular releases only, generate changelog entries in `CHANGELOG.md` following the format and writing guidelines in `references/common-changelog.md`. Use the `Changed`, `Added`, `Removed`, `Fixed` categories (in that order). Every entry must begin with a present-tense verb in imperative mood.

## Inclusion Criteria

For regular releases only (changelog generation is skipped for beta releases):

- **Files field constraint** - If `package.json` contains a `files` field, only include changes to files/directories specified in that array. All other codebase changes should be excluded from the CHANGELOG
- **Production changes only** - When no `files` field exists, exclude test changes, CI/CD workflows, and development tooling
- **Reference pull requests** - Link to PRs when available for context
- **Net changes only** - Examine diffs between the current branch and the previous tag to identify changes
- **Only dependencies and peerDependencies changes** - Exclude changes to devDependencies

## Examples

### Regular Release

```bash
# Create a regular patch/minor/major release
/bump-release

# Preview what a regular release would do
/bump-release --dry-run
```

### Beta Release

```bash
# Create a beta release with -beta.X suffix
/bump-release --beta

# Preview what a beta release would do
/bump-release --beta --dry-run
```

### Explicit Version

```bash
# Specify exact version
/bump-release 2.0.0

# Specify exact beta version
/bump-release 2.0.0-beta.1

# Combine with flags
/bump-release 2.0.0 --dry-run
```

## Version Examples

| Current Version | Release Type   | New Version     |
| --------------- | -------------- | --------------- |
| `1.2.3`         | Regular        | `1.2.4` (patch) |
| `1.2.3`         | Beta           | `1.2.4-beta.1`  |
| `1.2.3-beta.1`  | Beta           | `1.2.3-beta.2`  |
| `1.2.3-beta.5`  | Regular        | `1.2.3`         |
| `1.2.3`         | `2.0.0`        | `2.0.0`         |
| `1.2.3`         | `2.0.0` + Beta | `2.0.0-beta.1`  |

## Resources

- `references/common-changelog.md` — Common Changelog format and writing guidelines
