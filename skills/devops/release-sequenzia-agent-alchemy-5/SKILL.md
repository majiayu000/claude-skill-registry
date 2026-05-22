---
name: release
description: Prepare and execute a Python package release with verification steps. Use for releasing Python packages with uv and ruff.
dependencies: []
---

# Python Release Manager

Execute a complete pre-release workflow for Python packages using `uv` and `ruff`. This command automates version calculation, changelog updates, and tag creation.

## Arguments

Accept the following inputs:
- **version-override** (optional) — A specific version string (e.g., `1.0.0`). If not provided, the version is calculated from changelog entries.

## Workflow

Execute these 9 steps in order. **Fail fast**: Stop immediately if any verification step fails.

---

### Step 1: Pre-flight Checks

Run these checks and stop if any fail:

```bash
# Check current branch
git branch --show-current
```
- **Must be on `main` branch**. If not, stop and report: "Release must be run from the main branch. Currently on: {branch}"

```bash
# Check for uncommitted changes
git status --porcelain
```
- **Must have clean working directory**. If output is not empty, stop and report: "Working directory has uncommitted changes. Please commit or stash them first."

```bash
# Pull latest changes
git pull origin main
```
- Report any merge conflicts and stop if they occur.

---

### Step 2: Run Tests

Execute the test suite:

```bash
uv run pytest
```

- If tests fail, stop and report the failure output
- If tests pass, report: "All tests passed"

---

### Step 3: Run Linting

Execute linting checks:

```bash
uv run ruff check
```

```bash
uv run ruff format --check
```

- If either command fails, stop and report the issues
- If both pass, report: "Linting and formatting checks passed"

---

### Step 4: Verify Build

Build the package:

```bash
uv build
```

- If build fails, stop and report the error
- If build succeeds, report: "Package builds successfully"

---

### Step 5: Changelog Update Check

All verification checks have passed. Before calculating the version, offer to run the changelog-manager skill to ensure the `[Unreleased]` section is up-to-date.

Prompt the user to choose:
- "Yes, update changelog first (Recommended)" - Recommended option
- "No, continue with existing changelog"

**If user selects "Yes":**

Delegate to the **changelog-manager** skill:
- Prompt: "Analyze commits since the last release and update the CHANGELOG.md [Unreleased] section"
- Wait for the task to complete before proceeding

**If user selects "No":**

Continue to Step 6 (Calculate Version) without running the changelog-manager skill.

---

### Step 6: Calculate Version

#### 6.1 Read CHANGELOG.md

Read `CHANGELOG.md` and parse its structure. Look for:
- The `## [Unreleased]` section and its subsections
- The most recent versioned section (e.g., `## [0.1.0]`) to get the current version

#### 6.2 Analyze Change Types

Count entries under `[Unreleased]` by subsection:
- `### Added` - New features
- `### Changed` - Changes to existing functionality
- `### Deprecated` - Features marked for removal
- `### Removed` - Removed features (breaking change)
- `### Fixed` - Bug fixes
- `### Security` - Security fixes

#### 6.3 Calculate Suggested Version

Apply semantic versioning rules to the current version (MAJOR.MINOR.PATCH):

| Condition | Bump Type | Example |
|-----------|-----------|---------|
| `### Removed` present AND current >= 1.0.0 | MAJOR | 1.2.3 → 2.0.0 |
| `### Removed` present AND current < 1.0.0 | MINOR | 0.2.3 → 0.3.0 |
| `### Added` or `### Changed` present | MINOR | 0.1.0 → 0.2.0 |
| Only `### Fixed`, `### Security`, or `### Deprecated` | PATCH | 0.1.0 → 0.1.1 |

#### 6.4 Handle Edge Cases

- **No unreleased changes**: Warn user "No entries found under [Unreleased]. Are you sure you want to release?"
- **Missing CHANGELOG.md**: Stop and report "CHANGELOG.md not found. Please create one following Keep a Changelog format."
- **Version override provided**: Use the provided version instead of calculating

#### 6.5 User Confirmation

Prompt the user to choose:

```
Based on changelog analysis:
- Found: {count} Added, {count} Changed, {count} Fixed, {count} Removed entries
- Current version: {current}
- Suggested version: {suggested} ({bump_type} bump)

Confirm version or provide override:
```

- "Confirm {suggested}"
- "Enter different version"

---

### Step 7: Update CHANGELOG.md

#### 7.1 Get Repository URL

Read `pyproject.toml` and extract the repository URL from `[project.urls]`:
- Check keys: `Repository`, `repository`, `Source`, `source`, `Homepage`, `homepage`
- Extract the GitHub/GitLab URL

If no repository URL found, warn but continue (comparison links will be omitted).

#### 7.2 Update Changelog Content

Transform the changelog:

**Before:**
```markdown
## [Unreleased]

### Added
- New feature X

## [0.1.0] - 2024-01-15

### Added
- Initial release

[Unreleased]: https://github.com/user/repo/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/user/repo/releases/tag/v0.1.0
```

**After (releasing 0.2.0):**
```markdown
## [Unreleased]

## [0.2.0] - {today's date YYYY-MM-DD}

### Added
- New feature X

## [0.1.0] - 2024-01-15

### Added
- Initial release

[Unreleased]: https://github.com/user/repo/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/user/repo/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/user/repo/releases/tag/v0.1.0
```

#### 7.3 Write Updated CHANGELOG.md

Modify CHANGELOG.md with the transformed content.

---

### Step 8: Commit Changelog

Stage and commit the changelog update:

```bash
git add CHANGELOG.md
```

```bash
git commit -m "docs: update changelog for v{version}"
```

```bash
git push origin main
```

Report: "Changelog committed and pushed"

---

### Step 9: Create and Push Tag

Create an annotated tag and push it:

```bash
git tag -a v{version} -m "Release v{version}"
```

```bash
git push origin v{version}
```

#### Final Report

Report success with details:
```
Release v{version} completed successfully!

- Changelog updated: CHANGELOG.md
- Tag created: v{version}
- Tag URL: {repository_url}/releases/tag/v{version}

Next steps:
- GitHub/GitLab will create a release from the tag
- Publish to PyPI if configured in CI
```

---

## Error Recovery

If any step fails after Step 6 (version confirmation):
- Report which step failed and the error
- Provide commands to manually complete or rollback:
  - `git checkout CHANGELOG.md` - Revert changelog changes
  - `git tag -d v{version}` - Delete local tag if created
  - `git push origin :refs/tags/v{version}` - Delete remote tag if pushed

## Integration Notes

**What this component does:** Automates the Python package release workflow including pre-flight checks, testing, linting, version calculation, changelog updates, and git tagging.

**Capabilities needed:**
- Shell command execution (git, uv, ruff)
- File reading and editing (CHANGELOG.md, pyproject.toml)
- User interaction (version confirmation, changelog update prompt)

**Adaptation guidance:**
- Step 5 delegates to the **changelog-manager** skill for changelog updates -- this is a soft dependency (the release can proceed without it)
- The workflow is Python-specific (uses `uv` and `ruff`); adapt package manager and linter commands for other ecosystems
- Git operations assume a standard GitHub/GitLab workflow with tags and remote pushes
