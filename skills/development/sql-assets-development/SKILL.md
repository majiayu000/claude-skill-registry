---
name: sql-assets-development
description: Implement or refactor SQL assets behavior while keeping docs and tests aligned (src/vibe_piper/sql_assets.py, tests/test_sql_assets.py, docs/sql_assets.md).
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-01T01:43:21.767Z"
  updated_at: "2026-02-01T01:43:21.767Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Purpose
Make changes to SQL assets behavior with a tight code+docs+tests loop.

# When To Use
- You modify or add SQL assets behavior in `src/vibe_piper/sql_assets.py`.
- You update the user-facing SQL assets documentation in `docs/sql_assets.md`.
- You expand coverage in `tests/test_sql_assets.py`.

# Procedure
- Confirm the public surface area:
  - If something is intended as a public import, export it via `src/vibe_piper/__init__.py`.
- Update implementation:
  - Make the change in `src/vibe_piper/sql_assets.py`.
  - Prefer explicit errors/messages for invalid inputs.
- Update docs as contract:
  - Align `docs/sql_assets.md` with the actual callable API and behavior.
  - Ensure examples match the current signatures and defaults.
- Tests:
  - Add/adjust unit tests in `tests/test_sql_assets.py` for every documented behavior.
  - Include edge cases (missing assets, invalid paths/names, empty inputs, ordering/stability).
- Run checks (uv-only):
  - `uv run ruff format src tests`
  - `uv run ruff check src tests`
  - `uv run mypy src`
  - `uv run pytest`

# Gotchas
- If docs/examples diverge from code, users will follow docs; fix docs immediately.
- If a new API is introduced but not exported, users will get import errors; verify `src/vibe_piper/__init__.py`.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
