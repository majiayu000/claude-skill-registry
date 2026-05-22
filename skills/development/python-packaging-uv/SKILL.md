---
name: python-packaging-uv
description: Use when building or publishing Python packages with uv, including dist artifacts and pre-publish checks.
---

# Python Packaging with uv

## Overview

Use uv build and publish commands to produce wheels/sdists and ship to PyPI. Core principle: build, verify, then publish.

## Quick Reference

| Task | Command |
| --- | --- |
| Build wheel+sdist | `uv build` |
| Build wheel only | `uv build --no-sources` |
| Publish to PyPI | `uv publish --token $PYPI_TOKEN` |
| Publish to Test PyPI | `uv publish --publish-url https://test.pypi.org/legacy/ --token $TEST_PYPI_TOKEN` |

## Workflow

1. Build artifacts in `dist/`.
2. Test install from wheel.
3. Publish to Test PyPI, validate, then publish to PyPI.

## Example

```bash
uv build --no-sources
uv pip install dist/my_package-1.0.0-py3-none-any.whl
uv publish --publish-url https://test.pypi.org/legacy/ --token $TEST_PYPI_TOKEN
```

## Common Mistakes

- Publishing before verifying wheel contents.
- Skipping Test PyPI for first release.

## Red Flags

- Packaging guidance that ignores uv build/publish.

## References

- `references/packaging.md` - Build and publish details
