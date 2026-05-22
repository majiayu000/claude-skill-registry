---
name: publish-pypi
description: Publish a new release to PyPI. Use when releasing, publishing to PyPI, or making a release.
---

# Publish to PyPI

## Steps

1. **Ensure version is bumped** — verify or use bump-version skill

2. **Run full checks** — use complete-checkpoint skill, but include LLM tests (`uv run pytest -v`)

3. **Commit** version bump if not already committed

4. **Build and publish**:
   ```bash
   uv build
   uv run uv-publish
   ```

5. **Tag and push**:
   ```bash
   git tag vX.Y.Z
   git push && git push --tags
   ```

## Notes

- `uv run uv-publish` reads credentials from `~/.pypirc`
- For TestPyPI: `uv run uv-publish --repository testpypi`
