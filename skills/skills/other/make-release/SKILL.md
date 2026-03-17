---
name: make-release
description: Use when ready to publish a new version. Triggers on "release", "publish", "ship it", or version bump requests. Runs quality checks, bumps version, tags, and creates GitHub release.
---

# Release

Release workflow for publishing a new version to PyPI via GitHub Actions.

## When to Use

- After feature work is complete and committed
- When asked to release, publish, or ship a new version
- When bumping to a new version number

## Prerequisites

Before releasing:
- All work committed (clean working tree)
- On `main` branch
- `/code-review` passed
- `/commit-work` completed (CHANGELOG updated)

## Workflow

```
┌─────────────────────────┐
│ 1. Ask for version      │
│    Patch/Minor/Major?   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ 2. Verify clean state   │
│    git status           │
└───────────┬─────────────┘
            │
            ▼
      ┌───────────┐
      │ Clean?    │───No──→ STOP. Commit or stash first.
      └─────┬─────┘
            │Yes
            ▼
┌─────────────────────────┐
│ 3. Run quality checks   │
│    ruff → pytest        │
└───────────┬─────────────┘
            │
            ▼
      ┌───────────┐
      │ All pass? │───No──→ STOP. Fix issues first.
      └─────┬─────┘
            │Yes
            ▼
┌─────────────────────────┐
│ 4. Bump version         │
│    __init__.py +        │
│    pyproject.toml       │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ 5. Update CHANGELOG     │
│    [Unreleased] → [X.Y.Z]
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ 6. Commit + Tag + Push  │
│    (triggers workflow)  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ 7. Verify release       │
│    PyPI + GitHub release│
└─────────────────────────┘
```

## Step 1: Ask for Version Number

**Before doing anything else**, ask the user which version number to release:

Use `AskUserQuestion` with options:
- **Patch** (X.Y.Z+1): Bug fixes only
- **Minor** (X.Y+1.0): New features, backward compatible
- **Major** (X+1.0.0): Breaking changes

Or let them specify a custom version.

## Step 2: Verify Clean State

```bash
scripts/verify_release_state.sh
```

**Requirements:**
- Working tree must be clean (no uncommitted changes)
- Must be on `main` branch

If not clean: Run `/commit` first or stash changes.

## Step 3: Run Quality Checks

```bash
scripts/run_release_checks.sh
```

**All must pass.** No exceptions - releases with failing tests are forbidden.

## Step 4: Bump Version

Update version in **both** files:

```bash
uv run python scripts/bump_version.py X.Y.Z
```

**Important:** Both files must have the same version number.

**Version format:** Follow [SemVer](https://semver.org/)
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

## Step 5: Update CHANGELOG

In `CHANGELOG.md`, convert the Unreleased section to a versioned release:

**Before:**
```markdown
## [Unreleased]

### Added
- New feature
```

**After:**
```markdown
## [Unreleased]

## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature
```

Keep an empty `[Unreleased]` section at the top for future changes.

Use the deterministic script to promote the changelog:

```bash
uv run python scripts/promote_changelog.py X.Y.Z
```

## Step 6: Commit, Tag, and Push

```bash
git add agr/__init__.py pyproject.toml CHANGELOG.md
git commit -m "$(cat <<'EOF'
Release vX.Y.Z

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
scripts/tag_and_push.sh X.Y.Z
```

**Order matters:** Push commit first, then tag. This ensures the commit exists on remote before the tag references it.

**Important:** The tag push triggers the publish workflow which:
1. Runs quality checks
2. Builds and publishes to PyPI
3. Extracts release notes from CHANGELOG.md
4. Creates GitHub release

## Step 7: Verify Release

### Watch the Workflow

The tag push triggers `.github/workflows/publish.yml` which:
1. **Quality checks**: Runs ruff + pytest
2. **Build**: Creates wheel and sdist
3. **Publish**: Uploads to PyPI via trusted publishing (OIDC)
4. **Release**: Creates GitHub release from CHANGELOG.md

```bash
# Watch the workflow run to completion
gh run watch --workflow=publish.yml
```

### Verify Everything Succeeded

```bash
# Verify GitHub release was created
gh release view vX.Y.Z

# Verify PyPI publication (may take a few minutes)
pip index versions agr
```

### If Workflow Fails

| Failure Point | Result | Action |
|---------------|--------|--------|
| Quality checks | No PyPI, no release | Delete tag (`git push --delete origin vX.Y.Z && git tag -d vX.Y.Z`), fix issue, re-release |
| PyPI publish | No release created | Fix PyPI config, delete tag (`git push --delete origin vX.Y.Z && git tag -d vX.Y.Z`), re-release |
| Release creation | PyPI has package, no release | Create release manually (see below) |

**Manual release creation** (if only the release step failed):
```bash
VERSION="X.Y.Z"
gh release create "v$VERSION" --title "v$VERSION" --notes-file <(
  echo "## What's New in v$VERSION"
  echo ""
  awk -v ver="$VERSION" '/^## \[/ { if (found) exit; if ($0 ~ "\\[" ver "\\]") found=1; next } found { print }' CHANGELOG.md
  echo ""
  echo "---"
  echo ""
  echo "**Full changelog**: https://github.com/kasperjunge/agent-resources/blob/main/CHANGELOG.md"
)

## Red Flags - STOP

- Uncommitted changes → Commit first
- Tests failing → Fix before release
- Not on main branch → Switch to main
- CHANGELOG not updated → Update it
- Skipping quality checks → Never skip

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Releasing with dirty working tree | Commit or stash first |
| Skipping tests "we tested earlier" | Run tests immediately before release |
| Forgetting to push the tag | Push tag separately after commit |
| Not watching the workflow | Use `gh run watch` to verify full pipeline |
| CHANGELOG not updated for version | Add version section before tagging |
| Only updating `__init__.py` version | Update both `__init__.py` and `pyproject.toml` |

## No Exceptions

- "We already tested it" → Run tests again now
- "It's just a patch" → Full quality checks required
- "Nobody reads release notes" → CHANGELOG is documentation. Use it.
- "We're in a hurry" → Rushed releases cause incidents
