---
name: execution-types-contract
description: Keep execution engine changes aligned with stable public types (execution.py + types.py lockstep).
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-01T04:33:04.956Z"
  updated_at: "2026-02-01T04:33:04.956Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Purpose
When extending execution behavior, keep the public contract stable and import-safe.

# When To Use
- You change execution orchestration in `src/vibe_piper/execution.py`.
- You also add/adjust public result/config types in `src/vibe_piper/types.py`.

# Procedure
- Decide what is "public API" vs. internal implementation.
- Put public dataclasses/enums/protocols in `src/vibe_piper/types.py`.
- Keep `src/vibe_piper/execution.py` focused on orchestration and flow.
- Enforce a one-way dependency:
  - `src/vibe_piper/execution.py` may import from `vibe_piper.types`.
  - Avoid `src/vibe_piper/types.py` importing from `vibe_piper.execution`.
- If you need type-only references that would create a cycle, use `typing.TYPE_CHECKING` and forward references.
- Prefer narrow, explicit types (dataclasses/enums) over loose dicts for cross-module boundaries.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
