---
name: uv-lockfile-hygiene
description: Triage unexpected uv.lock changes and generated src/*.egg-info diffs in uv-driven Python repos.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-30T04:44:58.018Z"
  updated_at: "2026-01-30T04:44:58.018Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Purpose
Keep dependency diffs clean and intentional in uv-driven repos.

# When To Use
- `git diff` shows `uv.lock` changes you did not expect.
- `git diff` also shows `src/*.egg-info/**` changes after `uv pip install -e .` / `uv run ...`.

# Procedure
- Identify why `uv.lock` changed:
  - Check whether `pyproject.toml` dependency constraints changed.
  - Re-run the intended install step (usually `uv sync --dev`) and confirm the lock diff is stable.
- Decide what to commit:
  - Commit `uv.lock` only when the dependency change is intentional (new/updated dependency, resolver behavior change, platform marker update).
  - Treat `src/*.egg-info/` as generated metadata; do not commit by default.
- If `src/*.egg-info/` is untracked noise:
  - Prefer ignoring it via `.gitignore` (`src/*.egg-info/`) rather than committing.
- If `src/*.egg-info/` is already tracked:
  - Only commit it when doing explicit packaging/version metadata work; otherwise keep it out of feature commits.

# Notes
- `uv.lock` is the dependency source of truth; `src/*.egg-info/` is typically a local artifact of editable installs.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
