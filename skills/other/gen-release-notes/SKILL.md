---
name: gen-release-notes
description: generate release notes for changes since a given tag
disable-model-invocation: true
---

# Release Notes Generator

Generate professional release notes following the Keep a Changelog standard.

**Input**: Previous tag (e.g., `v0.0.1`)

```
$ARGUMENTS
```

---

Use extended thinking to analyze the changes thoroughly before generating release notes.

## Gates

Do not invent tags, PR numbers, or links. Each row must pass before the work that depends on it.

| When | Pass condition (evidence) | On fail |
|------|---------------------------|---------|
| Before `git log` / `git diff` | `git tag -l "$PREV_TAG"` prints exactly one line matching `PREV_TAG` | Stop; report that the tag is missing—do not write changelog entries |
| Before categorizing | `git rev-parse "$PREV_TAG^{commit}"` exits 0 | Stop; fix `PREV_TAG` or repo checkout |
| If using `gh pr list` | Command exits 0 and JSON is valid | Fall back to commit subjects + merge-commit URLs only; do not fabricate PR numbers |
| After Step 5 footer edits | Step 6 footer-gate exits 0 (both `grep -q` checks pass against the staged `CHANGELOG.md`) | Re-run footer edits from Step 5, then re-run Step 6 until it exits 0 |

## Step 1: Gather Changes

Run these commands to collect information about changes since the provided tag:

```bash
# Store the previous tag
PREV_TAG="$ARGUMENTS"

# Gate: tag must exist (output must be non-empty and match PREV_TAG)
git tag -l "$PREV_TAG"
# If the line above prints nothing, STOP — do not continue below.

# Get the repo URL for PR links
git remote get-url origin

# List commits since last tag
git log ${PREV_TAG}..HEAD --pretty=format:"%h %s" --no-merges

# Get detailed diff stats
git diff ${PREV_TAG}..HEAD --stat

# List changed files by directory
git diff ${PREV_TAG}..HEAD --name-only | sort | uniq
```

Also gather PR information:

```bash
# Get merged PRs since the tag (requires gh CLI)
gh pr list --state merged --search "merged:>=$(git log -1 --format=%ci $PREV_TAG | cut -d' ' -f1)" --json number,title,author,labels
```

## Step 2: Analyze and Categorize

Categorize each change into exactly one of these groups (in this order):

| Category | Include | Exclude |
|----------|---------|---------|
| **Added** | New features, new public APIs, new CLI commands | Internal utilities not exposed to users |
| **Changed** | Modified behavior, performance improvements, updated dependencies with user impact | Refactors with no behavior change |
| **Deprecated** | Features marked for future removal | - |
| **Removed** | Deleted features, removed public APIs | Removed internal code |
| **Fixed** | Bug fixes, error handling improvements | Test-only fixes |
| **Security** | Vulnerability patches, security hardening | - |

**Exclude entirely:**
- CI/CD configuration changes (unless they affect users)
- Documentation-only changes (unless they reveal new features)
- Code style/formatting changes
- Test-only changes
- Internal refactors with no user-visible impact
- Merge commits

## Step 3: Determine Version Number

Based on the changes, suggest the next version following Semantic Versioning:
- **MAJOR** (X.0.0): Breaking changes to public API
- **MINOR** (x.Y.0): New features, backward-compatible
- **PATCH** (x.y.Z): Bug fixes only

Detect the tag format from existing tags (with or without `v` prefix).

## Step 4: Write Release Notes

Generate a `CHANGELOG.md` entry using this exact format:

```markdown
## [VERSION] - YYYY-MM-DD

### Added

- **scope:** Add new feature description ([#54](REPO_URL/pull/54))

### Changed

- **Breaking:** Rename `oldName()` to `newName()` for consistency ([#145](REPO_URL/pull/145))

  **Migration:** Replace all calls to `oldName()` with `newName()`.

### Deprecated

- **scope:** Deprecate `legacy_function()` in favor of `new_function()` ([#143](REPO_URL/pull/143))

### Removed

- **Breaking:** Remove deprecated `old_function()` ([#141](REPO_URL/pull/141))

### Fixed

- **scope:** Fix race condition when multiple workers access shared state ([#139](REPO_URL/pull/139))

### Security

- **deps:** Update vulnerable package to patched version ([#49](REPO_URL/pull/49))
```

### Writing Rules

**Format requirements:**
- Start every entry with an imperative verb: Add, Fix, Remove, Update, Improve, Rename, Deprecate, Patch
- Include scope prefix in bold when present: `**server:**`, `**cli:**`, `**api:**`
- One line per change (except breaking changes which get migration notes)
- Include PR/issue link at end of line
- Sort entries within each category by importance (most impactful first)
- Omit empty categories entirely

**Breaking changes:**
- Prefix with bold `**Breaking:**`
- List first within their category
- Add a `**Migration:**` block on the next line explaining exactly what users must change
- Include before/after code examples for API signature changes

**Tone:**
- Write for library consumers, not maintainers
- Focus on *what changed for users*, not *how it was implemented*
- Be specific—never write "various improvements" or "bug fixes"
- Each entry should be understandable without reading the PR

**Bad examples to avoid:**
```markdown
# BAD - Too vague
- Fixed bugs
- Performance improvements
- Updated dependencies

# BAD - Implementation-focused
- Refactored the internal state machine to use async/await

# BAD - Missing context
- Fixed #234
```

**Good examples to follow:**
```markdown
# GOOD - Specific and user-focused
- **server:** Fix timeout errors when processing files larger than 100MB ([#234](URL))
- **cli:** Add `--dry-run` flag to preview changes before execution ([#235](URL))
- **api:** Improve cold-start latency from 2.3s to 0.8s by lazy-loading plugins ([#236](URL))
```

## Step 5: Update CHANGELOG.md

1. If `CHANGELOG.md` exists:
   - Insert new version after the `## [Unreleased]` section (or at top if no Unreleased)

2. If `CHANGELOG.md` doesn't exist, create it with this header:
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

```

3. **Update the footer reference links at the bottom of the file.** This step is mandatory — CodeRabbit and other reviewers will flag the changelog as incomplete if these are missing. Two edits are required:

   a. **Advance `[Unreleased]`** so it compares against the new version instead of the previous one.
   b. **Insert a new `[NEW_VERSION]` line** right below `[Unreleased]`, comparing the previous tag to the new one.

   Example diff (releasing `3.2.0` after `3.1.0`):

   ```diff
   -[Unreleased]: https://github.com/OWNER/REPO/compare/v3.1.0...HEAD
   +[Unreleased]: https://github.com/OWNER/REPO/compare/v3.2.0...HEAD
   +[3.2.0]: https://github.com/OWNER/REPO/compare/v3.1.0...v3.2.0
    [3.1.0]: https://github.com/OWNER/REPO/compare/v3.0.0...v3.1.0
   ```

   After editing, run **Step 6** to verify both footer lines exist and are correct. Do not skip Step 6 — it is the hard gate that prevents the recurring "missing footer compare link" reviewer feedback.

## Step 6: Verify CHANGELOG footer compare links (HARD GATE)

This is the enforcement gate for footer compare links. It must run before `gen-release-notes` reports success and before any commit step in the release workflow. It is **not** advisory — both `grep -q` checks must exit 0 or the gate fails with a named missing line.

Run this block exactly:

```bash
# Read the staged CHANGELOG.md blob (index), not the working tree, so unstaged
# edits cannot make the gate pass when the commit would actually fail.
STAGED_CHANGELOG=$(git show :CHANGELOG.md)

# Extract NEW and PREV versions from the staged CHANGELOG.md.
# We only match numeric `## [X.Y.Z]` headings so `## [Unreleased]` is skipped.
NEW_VERSION=$(printf '%s\n' "$STAGED_CHANGELOG" | grep -m1 -E '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' | sed -E 's/^## \[([0-9]+\.[0-9]+\.[0-9]+)\].*/\1/')
PREV_VERSION=$(printf '%s\n' "$STAGED_CHANGELOG" | grep -m2 -E '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' | sed -n '2p' | sed -E 's/^## \[([0-9]+\.[0-9]+\.[0-9]+)\].*/\1/')

if [ -z "$NEW_VERSION" ] || [ -z "$PREV_VERSION" ]; then
  echo "GATE FAIL: could not extract NEW_VERSION ($NEW_VERSION) or PREV_VERSION ($PREV_VERSION) from staged CHANGELOG.md"
  exit 1
fi

# Infer optional tag prefix (`v` or empty) from the existing [Unreleased] footer.
# Step 3 explicitly allows tags with or without `v`; never hardcode `v` here.
# Fall back to `v` only when no [Unreleased] footer exists yet (first release).
TAG_PREFIX=$(printf '%s\n' "$STAGED_CHANGELOG" | sed -nE 's|^\[Unreleased\]: .*/compare/(v?)[0-9]+\.[0-9]+\.[0-9]+\.\.\.HEAD$|\1|p' | head -1)
if ! printf '%s\n' "$STAGED_CHANGELOG" | grep -qE '^\[Unreleased\]:'; then
  TAG_PREFIX="v"
fi

echo "Gating footer compare links: NEW=${TAG_PREFIX}${NEW_VERSION}, PREV=${TAG_PREFIX}${PREV_VERSION}"

# Escape dots so they match literally inside the regex.
NEW_RE=${NEW_VERSION//./\\.}
PREV_RE=${PREV_VERSION//./\\.}

# Check 1: the new [NEW_VERSION] footer line exists and points PREV->NEW.
printf '%s\n' "$STAGED_CHANGELOG" | grep -qE "^\[${NEW_RE}\]: .*compare/${TAG_PREFIX}${PREV_RE}\.\.\.${TAG_PREFIX}${NEW_RE}\$" \
  || { echo "GATE FAIL: missing footer line: [${NEW_VERSION}]: .../compare/${TAG_PREFIX}${PREV_VERSION}...${TAG_PREFIX}${NEW_VERSION}"; exit 1; }

# Check 2: the [Unreleased] footer line is advanced to compare from the new tag.
printf '%s\n' "$STAGED_CHANGELOG" | grep -qE "^\[Unreleased\]: .*compare/${TAG_PREFIX}${NEW_RE}\.\.\.HEAD\$" \
  || { echo "GATE FAIL: [Unreleased] is not advanced; expected: [Unreleased]: .../compare/${TAG_PREFIX}${NEW_VERSION}...HEAD"; exit 1; }

echo "Footer compare links verified: [${NEW_VERSION}] and [Unreleased] both present and correct."
```

**Pass condition (objective):** both `grep -q` invocations above exit 0 against the staged `CHANGELOG.md`. The block must print `Footer compare links verified: ...` and exit 0.

**On fail:** the gate names the missing or wrong line. Return to Step 5 and edit `CHANGELOG.md` to add or correct that line, then re-run this block. Do not proceed to Step 7 or report success until the block exits 0.

## Step 7: Output Summary

After updating the changelog, provide:
1. The suggested version number with rationale
2. Summary of categorized changes
3. Any breaking changes that need special attention
4. Confirmation that CHANGELOG.md was updated

## Conventional Commits Mapping

Map commit prefixes to changelog categories:

| Commit Prefix | Changelog Category |
|---------------|-------------------|
| `feat(scope):` | Added |
| `feat!(scope):` | Added (with Breaking prefix) |
| `fix(scope):` | Fixed |
| `perf(scope):` | Changed |
| `security(scope):` | Security |
| `docs:`, `chore:`, `ci:`, `test:`, `style:` | **Exclude** |
