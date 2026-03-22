---
name: ce-release-finalize
description: >
  Execute the PyPI release checklist for calibrated-explanations: version bumps,
  changelog, build, validation, tagging, RTD publication, and PyPI upload.
---

# CE Release Finalize

You are finalizing a release of calibrated-explanations for publication on PyPI.
This skill follows the canonical release guide step by step.

Load `references/pypi_release_guide.md` for the full release procedure.

## Use this skill when

- All release tasks for the target version are closed.
- The user asks to "release", "publish", or "ship" a version.
- Preparing the final version bump, changelog, and build artifacts.

## Pre-flight checks

Before starting the release process:

1. Confirm all tasks in `docs/improvement/vX.Y.Z_plan.md` are completed.
2. Confirm CI is green on `main`: `make ci-local-new`.
3. Confirm the user has PyPI credentials configured.

## Release workflow

### Step 1: Version files update

Update version strings in all required files. The version format rules:
- PEP 440 version (no `v` prefix): `pyproject.toml`, `docs/conf.py` release,
  `METADATA.json`
- Display version (with `v` prefix): `__init__.py`, `CITATION.cff`,
  `docs/citing.md`
- Short version: `docs/conf.py` version field (e.g., `"0.11"`)

Files to update:
- `pyproject.toml` -> `[project].version = "X.Y.Z"`
- `src/calibrated_explanations/__init__.py` -> `__version__ = "vX.Y.Z"`
- `CITATION.cff` -> `version: vX.Y.Z` and `date-released: 'YYYY-MM-DD'`
- `docs/conf.py` -> `release = "X.Y.Z"` and `version = "X.Y"`
- `docs/citing.md` -> BibTeX `version = {vX.Y.Z}` and month/year
- `METADATA.json` -> `"version": "X.Y.Z"`

### Step 2: Changelog

Update `CHANGELOG.md`:
- Create new version section under `[Unreleased]`
- Move relevant bullets from `[Unreleased]` into the new section
- Update compare links

### Step 3: Version consistency check

Verify all version strings are aligned across all files listed above.

### Step 4: Build and validate

```bash
rm -rf dist/ build/ *.egg-info/
python -m build
python -m twine check dist/*
```

### Step 5: Smoke test (recommended)

Test the wheel locally in a clean venv before publishing.

### Step 6: Commit and tag

```bash
git add .
git commit -m 'calibrated-explanations vX.Y.Z'
git tag vX.Y.Z
git push
git push --tags
```

### Step 7: RTD publication

- Confirm tag is on remote
- Trigger RTD build for the tag
- Activate the tag version and set as stable
- Spot-check rendered docs

### Step 8: PyPI upload

```bash
python -m twine upload --repository pypi dist/*
```

### Step 9: Post-release verification

- Check PyPI project page renders correctly
- Test installation in a clean venv

### Step 10: Post-release dev bump (required finalization)

Immediately after publishing `X.Y.Z`, bump to next development version:

- `pyproject.toml` -> `[project].version = "X.Y.(Z+1)-dev"`
- `src/calibrated_explanations/__init__.py` -> `__version__ = "vX.Y.(Z+1)-dev"`

Commit this as a separate post-release commit (recommended message:
`start vX.Y.(Z+1)-dev`) so `main` never remains on the released version.

## Constraints

- Never upload to PyPI without user confirmation (immutable action).
- Never push tags without user confirmation.
- Always run `twine check` before upload.
- Follow the canonical release guide in `references/pypi_release_guide.md`.
