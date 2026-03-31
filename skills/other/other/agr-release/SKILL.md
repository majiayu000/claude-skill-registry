---
name: agr-release
description: >
  Release process for the agr package. Handles version bumping (major/minor/patch/beta),
  changelog updates, pre-release quality checks, git tagging, and monitoring the GitHub Actions
  publish pipeline. Use this skill whenever the user wants to cut a release, bump the version,
  publish to PyPI, or asks about the release process — even if they just say "let's ship it"
  or "time for a new version".
---

# agr Release Process

This skill walks through the full release process for the `agr` package. The release is
tag-driven: pushing a `vX.Y.Z` tag triggers the GitHub Actions pipeline that runs quality
checks, builds the package, publishes to PyPI, and creates a GitHub Release.

Your job is to prepare everything so that when the tag is pushed, the pipeline succeeds
on the first try.

## Before you start

Verify the preconditions. If any fail, stop and tell the user.

1. **Clean working tree** — `git status` should show no uncommitted changes
2. **On the `main` branch** — releases should only come from main
3. **Up to date with remote** — `git pull` to make sure you're not behind

Ask the user what kind of release this is:
- **patch** (0.7.10 → 0.7.11) — bug fixes, small changes
- **minor** (0.7.10 → 0.8.0) — new features, backwards-compatible
- **major** (0.7.10 → 1.0.0) — breaking changes
- **beta** (0.7.11b1) — pre-release for testing

If the user already said what type they want, don't ask again.

## Step 1: Figure out what changed

Before touching any files, understand what's being released.

```bash
# See all commits since the last release tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline
```

Also check the `[Unreleased]` section in `CHANGELOG.md` — it may already have entries. Cross-reference with the git log to make sure nothing is missing. If there are commits that aren't reflected in the changelog, add them.

Group changes into the standard Keep a Changelog categories:
- **Added** — new features
- **Changed** — changes to existing functionality
- **Fixed** — bug fixes
- **Removed** — removed features
- **Docs** — documentation-only changes

## Step 2: Run quality checks

Run all three locally before proceeding. These are the same checks the CI pipeline runs,
so catching failures here saves a round-trip.

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest -m "not e2e and not network and not slow"
uv run ty check
```

If anything fails, fix it before continuing. The release commit should pass CI cleanly.

## Step 3: Check if docs need updating

Not every release needs doc changes — use judgement. Docs updates are warranted when:
- A CLI command was added, removed, or its flags changed
- A new module or public API was added
- Behavior that users rely on changed in a way they'd notice

The docs to consider:
- `README.md` — the primary entry point, should reflect current capabilities
- `docs/docs/reference.md` — CLI command reference
- `docs/docs/index.md` — landing page / getting started
- Other files in `docs/docs/` as relevant (sdk.md, configuration.md, etc.)
- Skills in `skills/` — if any exist and are affected by the changes

If nothing user-facing changed (internal refactors, test improvements, dependency bumps),
skip this step and move on.

## Step 4: Bump the version

The version lives in two places — both must be updated:

1. `pyproject.toml` line 7: `version = "X.Y.Z"`
2. `agr/__init__.py` line 3: `__version__ = "X.Y.Z"`

Calculate the new version based on the current version and the release type the user chose.

For beta releases, append `b1` (or increment the beta number if one already exists):
- `0.7.10` → `0.7.11b1` (first beta of next patch)
- `0.7.11b1` → `0.7.11b2` (next beta)
- `0.7.11b2` → `0.7.11` (promote beta to stable)

## Step 5: Update the changelog

In `CHANGELOG.md`:

1. Replace `## [Unreleased]` with `## [X.Y.Z] - YYYY-MM-DD` (today's date)
2. Make sure all changes from Step 1 are included under the right categories
3. Add a new empty `## [Unreleased]` section at the top
4. Review the entries — they should be concise but descriptive enough that a user
   scanning the changelog understands what changed without reading the code

The changelog format matters because the GitHub Actions pipeline extracts the version's
section to use as release notes. Malformed entries = bad release notes.

## Step 6: Commit, tag, and push

```bash
# Stage the changed files
git add pyproject.toml agr/__init__.py CHANGELOG.md
# Plus any docs files you updated

# Commit
git commit -m "release: vX.Y.Z"

# Tag
git tag vX.Y.Z

# Push commit and tag
git push origin main
git push origin vX.Y.Z
```

**Wait for the user to confirm before pushing.** Show them a summary of what will be pushed:
- The version being released
- The changelog entry
- Which files were modified
- The tag that will be created

## Step 7: Monitor the pipeline

After pushing the tag, monitor the GitHub Actions pipeline:

```bash
# Watch the workflow run
gh run list --workflow=publish.yml --limit=1
gh run watch $(gh run list --workflow=publish.yml --limit=1 --json databaseId -q '.[0].databaseId')
```

The pipeline has four stages:
1. **Quality Checks** — ruff + pytest
2. **Build Package** — `uv build` + verify
3. **Publish to PyPI** — trusted publishing via OIDC
4. **Create GitHub Release** — extracts notes from CHANGELOG.md

If any stage fails, read the logs and help the user fix it:

```bash
gh run view <run-id> --log-failed
```

Common failure modes:
- Quality checks fail → something slipped past local checks, fix and re-tag
- PyPI publish fails → usually a version conflict (version already exists on PyPI)
- Release notes extraction fails → changelog format issue

## Step 8: Verify the release

Once the pipeline succeeds, confirm:

```bash
# Check PyPI (may take a minute to propagate)
pip index versions agr

# Check the GitHub release exists
gh release view vX.Y.Z
```

Tell the user the release is live and share the links:
- PyPI: https://pypi.org/project/agr/X.Y.Z/
- GitHub Release: the URL from `gh release view`

## If something goes wrong after pushing

If the pipeline fails and you need to retry:

1. Fix the issue
2. Delete the tag locally and remotely: `git tag -d vX.Y.Z && git push origin :refs/tags/vX.Y.Z`
3. Amend the release commit if needed, or create a new fix commit
4. Re-tag and re-push

This is destructive — confirm with the user before deleting tags.
