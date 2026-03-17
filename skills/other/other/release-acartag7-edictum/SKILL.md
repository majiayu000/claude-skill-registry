---
name: release
description: Bump version, tag, push, create GitHub Release, and verify PyPI publish.
user-invocable: true
allowed-tools: Read, Edit, Bash, Grep, Glob, AskUserQuestion
---

# Release

Automates the full release process for edictum (Python).

## Arguments

- `version` (optional): The semver version to release, e.g. `/release 0.1.0`

## Step 1: Pre-flight checks

Run all checks in sequence. Abort immediately on any failure.

1. **Tests:**
   ```
   Bash: pytest tests/ -v
   ```
   Abort if tests fail.

2. **Lint:**
   ```
   Bash: ruff check src/ tests/
   ```
   Abort if lint fails.

3. **Build (dry run):**
   ```
   Bash: python -m build --sdist --wheel
   ```
   Abort if build fails.

4. **Clean working tree:**
   ```
   Bash: git status --porcelain
   ```
   Abort if output is non-empty (dirty tree).

5. **Read current version:**
   ```
   Read: pyproject.toml
   ```
   Extract the `version` field from `[project]` section.

## Step 2: Determine new version

- If a version argument was provided (e.g. `/release 0.1.0`), use it.
- If no argument, ask the user:
  ```
  AskUserQuestion: "What version should this release be? Current version is {current_version}."
  ```
- Validate the version:
  - Must be valid semver (MAJOR.MINOR.PATCH)
  - Must be strictly greater than the current version
  - Abort with a clear message if validation fails

## Step 3: Bump version

1. **Edit `pyproject.toml`:**
   ```
   Edit: pyproject.toml
   old_string: version = "{current_version}"
   new_string: version = "{new_version}"
   ```

2. **Audit all version references in the repo:**
   ```
   Grep: pattern="{current_version}" (search tracked files only, exclude CHANGELOG.md)
   ```
   For each match, determine if it is a **"current version" reference** or a **historical reference**:
   - **Current version references** — strings like `Current version: **v0.5.3**`, `version 0.5.3`, `(v0.5.3)` in docs/README/CLAUDE.md that describe the *current* state of the library. **Update these** to `{new_version}`.
   - **Historical references** — changelog entries, "What's Shipped" bullet points, test docstrings noting when a fix was introduced (e.g., `Regression tests for ... (v0.5.2)`), git commit messages. **Leave these unchanged.**

   Use `Edit` to update each current-version reference. Common locations to check:
   - `README.md` — install/version badges, "Current version" line
   - `CLAUDE.md` — "Current version" line in header (but NOT the "What's Shipped" history)
   - `docs/index.md` — homepage version mention
   - `docs/roadmap.md` — version references in prose
   - Any other `.md` or `.py` file that mentions the old version as current

   If unsure whether a reference is current or historical, **leave it unchanged** and flag it to the user.

3. **Commit the change:**
   ```
   Bash: git add -A && git commit -m "chore: bump version to {version}"
   ```
   - Do NOT include `Co-Authored-By` in the commit message.

## Step 4: Tag and push

```
Bash: git tag v{version}
Bash: git push origin main && git push origin v{version}
```

## Step 5: Create GitHub Release

```
Bash: gh release create v{version} --generate-notes
```

This auto-generates release notes from commits since the previous tag.

## Step 6: Wait and verify

1. **Find the publish workflow run:**
   ```
   Bash: gh run list --workflow=publish.yml --limit=1 --json databaseId,status --jq '.[0]'
   ```

2. **Watch it:**
   ```
   Bash: gh run watch {run_id}
   ```

3. **Report result:**
   - If the run succeeds, confirm to the user: "v{version} published to PyPI successfully."
   - If the run fails, show the logs:
     ```
     Bash: gh run view {run_id} --log-failed
     ```
     And report the failure to the user.

## Post-release

After successful publish:
1. Verify on PyPI: `pip index versions edictum`
2. Test install: `pip install edictum=={version}`

## Important Notes

- Always run pre-flight checks before anything else — never skip them.
- Never amend a previous commit; always create a new one.
- The publish workflow (`publish.yml`) is triggered by the GitHub Release `published` event.
- Clean up build artifacts after dry run: `rm -rf dist/ *.egg-info`
