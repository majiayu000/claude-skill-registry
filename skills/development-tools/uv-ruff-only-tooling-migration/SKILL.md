---
name: uv-ruff-only-tooling-migration
description: Migrate a Python repo from Poetry/Black to UV + Ruff-only (CI, pre-commit, pyproject, docs).
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-29T05:46:15.157Z"
  updated_at: "2026-01-29T05:46:15.157Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# When To Use
- Repo has `uv.lock` (or wants UV).
- User wants no Poetry and/or no Black.

# Steps
- Remove Poetry artifacts
  - Delete `poetry.lock`.
  - Remove Poetry commands/docs references.
- Make `pyproject.toml` UV-native
  - Ensure PEP 621 `[project]` is source of truth.
  - Prefer `[dependency-groups]` for `dev`/`docs` tool deps.
  - Add missing runtime deps surfaced by imports/tests.
  - Run `uv lock` to regenerate `uv.lock`.
- Pre-commit
  - Remove Black hook.
  - Add `ruff-format` and `ruff` hooks.
  - Ensure hooks run via the repo’s standard workflow.
- CI
  - Replace Black check with `uv run ruff format --check`.
  - Lint with `uv run ruff check`.
  - Use `uv sync --dev` and `uv pip install -e .`.
  - If needed, temporarily run a stable smoke suite while fixing failing tests.
- Docs/agent guidance
  - Update `AGENTS.md`, `README.md`, and contrib/dev docs to reference UV + Ruff only.

# Verify
- `uv sync --dev`
- `uv pip install -e .`
- `uv run ruff format --check src tests`
- `uv run ruff check src tests`
- `uv run pytest` (or smoke suite if full is broken)
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
