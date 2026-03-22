---
name: create-release
description: Create a release for CodeCompress following Gitflow conventions, Semantic Versioning, and .NET version management. Handles version bumps in Directory.Build.props, CHANGELOG generation, and PR creation.
argument-hint: [major|minor|patch|hotfix|rc]
---

# Create Release — CodeCompress

You are a release manager for the CodeCompress project. Guide the user through a consistent, repeatable release process following Gitflow conventions and Semantic Versioning with .NET-specific version management.

## Step 1: Determine Release Type

Parse `$ARGUMENTS` to determine the release type. If not provided or unclear, use `AskUserQuestion` to ask:

| Argument | Release Type | Description |
|----------|-------------|-------------|
| `major` | Major Release | Breaking changes or major rewrites |
| `minor` | Minor Release | New features (backwards compatible) |
| `patch` | Patch Release | Bug fixes and minor improvements |
| `hotfix` | Hotfix | Urgent production fix (branches from main) |
| `rc` or `prerelease` | Release Candidate | Pre-release for testing |

Use `AskUserQuestion` with these options if `$ARGUMENTS` doesn't match any of the above:
- "Minor release (new features, backwards compatible)"
- "Patch release (bug fixes)"
- "Major release (breaking changes)"
- "Hotfix (urgent production fix)"
- "Release candidate (pre-release for testing)"

## Step 2: Read Current State

### 2a. Clean working tree check

Run `git status --porcelain`. If the output is non-empty, **stop immediately** and tell the user to commit or stash changes first.

### 2b. Detect main branch (production target)

Run `git branch -a` and look for `main` or `master` (local or remote). Priority:
1. `main` (preferred)
2. `master` (fallback)
3. If neither found, use `AskUserQuestion` to ask which branch is the production branch.

Store this as `{main_branch}`.

### 2c. Detect develop branch (integration branch)

Check if a `develop` branch exists (local or remote):
- **If develop exists** → Gitflow model. Standard releases branch from `develop`, hotfixes from `{main_branch}`, back-merge required after release.
- **If no develop** → Trunk-based model. All releases branch from `{main_branch}`, no back-merge needed.

Store the branching model as `{flow}` (either "gitflow" or "trunk").

### 2d. Detect current version from git tags

```bash
git tag --list --sort=-v:refname 'v*'
```

Parse tags as semantic versions. Take the **highest stable version** (ignore pre-release suffixes like `-rc.1`, `-preview.1` unless there are no stable tags).

If no `v*` tags exist, also try tags without the `v` prefix. If still no tags found, this is the **first release** — set current version to `v0.0.0`.

For RC/pre-release types, also check for existing RC tags on the target version to determine the next RC number:
```bash
git tag --list 'v{version}-rc.*' --sort=-v:refname
```

### 2e. Cross-check Directory.Build.props

Read the `<VersionPrefix>` from `Directory.Build.props` and verify it matches the latest git tag. If they differ, warn the user — someone may have forgotten to bump it or a tag is missing.

### 2f. Current branch and recent commits

```bash
git branch --show-current
git log --oneline {last_tag}..HEAD
```

If no tags exist, use `git log --oneline -30`.

### 2g. Display current state

```
============================================
  Current State
============================================
  Latest Version:   {version} (from git tag)
  Build.props:      {version_from_props}
  Current Branch:   {branch}
  Working Tree:     clean
  Branching Model:  {Gitflow (develop → main) | Trunk-based (main)}
  Main Branch:      {main_branch}
  Commits Since:    {N} commits since {version}
============================================
```

## Step 3: Calculate New Version

Based on the release type and current version:

- **Major**: `1.2.3` → `2.0.0`
- **Minor**: `1.2.3` → `1.3.0`
- **Patch**: `1.2.3` → `1.2.4`
- **Hotfix**: Same as patch, but branches from `{main_branch}`
- **RC**: `1.3.0` → `1.3.0-rc.1` (or increment existing RC number, e.g., `1.3.0-rc.2`)

**Edge cases:**
- **First release** (current = `v0.0.0`): Suggest `v0.1.0` for minor, `v1.0.0` for major, `v0.0.1` for patch. Use `AskUserQuestion` to confirm: "No existing version tags found. This appears to be the first release."
- **Pre-release to stable**: If the latest tag is a pre-release (e.g., `v0.3.0-rc.1`) and the user requests a standard release, ask whether to promote to stable (`v0.3.0`) or bump from the last stable version.

Use `AskUserQuestion` to confirm the version plan:

```
============================================
  Version Plan
============================================
  Current:       {old_version}
  New:           {new_version}
  Release Type:  {type}
  Branch Name:   {release/vX.Y.Z or hotfix/vX.Y.Z}
  Branch From:   {develop or main_branch}
  PR Target:     {main_branch}
============================================
```

Provide options: "Looks good, proceed" or "Let me specify a different version".

## Step 4: Create Release Branch

**Before creating, check for conflicts:**
- Run `git branch -a --list '*release/v{new_version}*' '*hotfix/v{new_version}*'` — if a matching branch exists, use `AskUserQuestion` to ask: use existing, delete and recreate, or abort.
- Run `git tag --list 'v{new_version}'` — if the tag already exists, **abort** with a clear message.

**Create the branch:**

For **Gitflow** standard releases (major/minor/patch):
```bash
git checkout develop
git pull origin develop
git checkout -b release/v{new_version}
```

For **hotfixes** (any branching model):
```bash
git checkout {main_branch}
git pull origin {main_branch}
git checkout -b hotfix/v{new_version}
```

For **trunk-based** standard releases:
```bash
git checkout {main_branch}
git pull origin {main_branch}
git checkout -b release/v{new_version}
```

For **release candidates**, use the same logic as the underlying release type but name the branch `release/v{new_version}-rc.{N}`.

## Step 5: Version Bump — Directory.Build.props (Mandatory)

This project uses `<VersionPrefix>` in `Directory.Build.props` as the single source of truth for the .NET assembly version. The MCP server reads this at runtime via `AssemblyInformationalVersionAttribute` to report its version to clients.

### 5a. Update Directory.Build.props

Update the `<VersionPrefix>` value to the new version (without the `v` prefix):

```xml
<VersionPrefix>{new_version_without_v}</VersionPrefix>
```

For RC/pre-release versions, also add or update `<VersionSuffix>`:
```xml
<VersionPrefix>{base_version}</VersionPrefix>
<VersionSuffix>rc.{N}</VersionSuffix>
```

### 5b. Build verification

Run a build to verify the version change compiles cleanly:

```bash
dotnet build CodeCompress.slnx
```

Must produce **zero warnings and zero errors**. If it fails, fix before proceeding.

### 5c. Commit version bump

```bash
git add Directory.Build.props
git commit -m "chore: bump version to v{new_version}"
```

## Step 6: Generate Changelog Entry

### 6a. Gather commits

```bash
git log --format="%H %s" {last_tag}..HEAD
```

If this is the first release (no previous tag), gather all commits:
```bash
git log --format="%H %s"
```

### 6b. Categorize commits

Analyze each commit message and categorize using your judgment. Use these heuristics as **guidance**, not rigid rules:

| Category | Typical signals |
|----------|----------------|
| **Added** | New features, new files, new capabilities, "add", "implement", "introduce", "create" |
| **Changed** | Updates to existing functionality, "update", "refactor", "improve", "enhance", "overhaul", "modify" |
| **Fixed** | Bug fixes, corrections, "fix", "bug", "patch", "correct", "resolve" |
| **Removed** | Removed features or code, "remove", "delete", "drop", "deprecate" |

**Important rules:**
- **Use your judgment.** A commit saying "Add tests for the fix" is **Added** (tests), not Fixed. Read the intent.
- **Filter out merge commits.** Skip messages starting with "Merge pull request" or "Merge branch".
- **Clean up messages.** Rewrite raw commit messages into user-facing changelog entries. Remove PR numbers from the text but keep them as references at the end (e.g., `(#42)`).
- **Group related commits.** If multiple commits relate to the same feature/fix, combine them into a single entry.
- **Skip internal/meta commits.** Version bumps, CI changes, and other non-user-facing changes can be omitted or grouped under Changed.

### 6c. Format as Keep a Changelog

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- Description of new feature (#PR)

### Changed
- Description of change (#PR)

### Fixed
- Description of fix (#PR)

### Removed
- Description of removal (#PR)
```

Only include categories that have entries. Use today's date.

### 6d. User review

Present the draft changelog to the user via `AskUserQuestion`: "Here is the generated changelog entry for v{new_version}. Would you like to edit, add, or remove any entries?"

Options: "Looks good, proceed" / "I'd like to make changes" (if they want changes, ask what to modify)

### 6e. Write CHANGELOG.md

- **If `CHANGELOG.md` exists:** Prepend the new entry after the header section. If there's an `## [Unreleased]` section, replace it with the new version entry (move unreleased items into the versioned section).
- **If `CHANGELOG.md` does not exist:** Use `AskUserQuestion` to ask whether to create one.

### 6f. Commit

```bash
git add CHANGELOG.md
git commit -m "docs: update CHANGELOG for v{new_version}"
```

## Step 7: Push Release Branch

```bash
git push -u origin {branch_name}
```

## Step 8: Create Pull Request

Create a PR targeting `{main_branch}`:

**For standard releases:**
```bash
gh pr create --base {main_branch} --title "Release v{new_version}" --body "$(cat <<'EOF'
## Release v{new_version}

{changelog_entry_content}

---
**Release type:** {type}
**Previous version:** v{old_version}
EOF
)"
```

**For hotfixes:**
```bash
gh pr create --base {main_branch} --title "Hotfix v{new_version}" --body "$(cat <<'EOF'
## Hotfix v{new_version}

{changelog_entry_content}

---
**Release type:** hotfix
**Previous version:** v{old_version}
EOF
)"
```

Display:
```
============================================
  Pull Request Created
============================================
  PR:       {pr_url}
  Base:     {main_branch}
  Branch:   {branch_name}
  Version:  v{new_version}
============================================
```

## Step 9: Post-Merge Steps

Provide the remaining steps as instructions, then offer to execute them.

**For Gitflow:**
```
============================================
  After PR is Merged — Run These Steps
============================================

  1. Pull merged main:
     git checkout {main_branch} && git pull origin {main_branch}

  2. Create annotated tag:
     git tag -a v{new_version} -m "Release v{new_version}"

  3. Push tag (triggers CI/CD GitHub Release):
     git push origin v{new_version}

  4. Back-merge to develop:
     git checkout develop && git merge {main_branch} && git push origin develop

  5. Clean up release branch:
     git branch -d {branch_name}
     git push origin --delete {branch_name}
============================================
```

**For trunk-based** — same steps but **skip step 4** (no develop branch to back-merge into).

Use `AskUserQuestion` to ask:
- "Would you like me to execute the post-merge steps now, or save these instructions for later?"
- Options: "Execute now (PR must be merged)" / "Save for later"

**If executing now:**
1. Check if the PR is merged: `gh pr view {pr_number} --json state`
2. If not merged, tell the user to merge the PR first and re-run
3. If merged, execute steps 1-5 above (resolve merge conflicts if needed — take main's version for `Directory.Build.props` and `CHANGELOG.md`)
4. **Update GitHub Release notes** — CI/CD creates the release but with minimal auto-generated notes. Replace them with the full changelog content:
   ```bash
   gh release edit v{new_version} --notes "{full_release_notes_with_changelog}" --repo MCrank/code-compress
   ```
   The release notes should include: a "What's New" header, the changelog entries rewritten for a release audience (grouped by theme, not just raw commit messages), and install instructions at the bottom.
5. Execute step 5 (clean up release branch)

## Step 10: Exit Summary

```
============================================
  Release Complete: v{new_version}
============================================
  PR:              {pr_url}
  Tag:             v{new_version} {created | pending}
  GitHub Release:  CI/CD will create on tag push
  CHANGELOG:       {updated | created}
  Build.props:     {new_version} ✓
  Branching Model: {Gitflow | Trunk-based}
============================================
```

## Behavioral Rules

1. **Git tags are the source of truth for versions.** `Directory.Build.props` must match the tag — this is enforced in Step 2e.
2. **Directory.Build.props is mandatory.** Unlike the generic release command, this project always has `<VersionPrefix>` and it must be updated. Never skip this step.
3. **Build verification is mandatory.** Always run `dotnet build CodeCompress.slnx` after version bump to catch any issues.
4. **Auto-detect the branching model.** Never assume Gitflow or trunk-based — always detect from actual branches.
5. **Clean working tree is mandatory.** Abort immediately if there are uncommitted changes.
6. **Confirm before destructive actions.** Always ask before force-pushing, deleting branches, or overwriting tags.
7. **Follow Semantic Versioning strictly.** Major for breaking changes, minor for new features, patch for bug fixes.
8. **Generate meaningful changelogs.** Analyze commit intent — do not just echo raw commit messages.
9. **CI/CD creates GitHub Releases.** Do NOT manually create GitHub releases — the pipeline handles this when a tag is pushed.
10. **Strip the `v` prefix for Directory.Build.props.** Git tags use `vX.Y.Z` but the props file uses `X.Y.Z`.
