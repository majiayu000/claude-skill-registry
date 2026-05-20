---
name: promote-wayfinder-script
description: Promote a session scratch run script into the local Wayfinder library so it persists across sessions.
metadata:
  tags: wayfinder, runs, promotion, cleanup
---

## When to use

Use this skill when a one-off script created during an interactive session is worth keeping for future reuse.

## How to use

This repo creates a per-session scratch directory (see `$WAYFINDER_SCRATCH_DIR`) and a persistent local library (see `$WAYFINDER_LIBRARY_DIR`).

Keep (promote) a script when it worked as intended and you expect it to be useful again in later sessions — the goal is to speed up future runs by reusing a known-good script instead of regenerating/re-reviewing new ad-hoc code.

Promote a script into the library:

```bash
poetry run python scripts/promote_wayfinder_script.py "$WAYFINDER_SCRATCH_DIR/my_script.py" my_script
```

Notes:
- By default, scripts are organized under `$WAYFINDER_LIBRARY_DIR/<protocol>/...` when the tool can infer a protocol from the filename/content (otherwise it uses `misc/`).
- You can force the folder with `--protocol`, e.g.:

  ```bash
  poetry run python scripts/promote_wayfinder_script.py "$WAYFINDER_SCRATCH_DIR/my_script.py" my_script --protocol hyperliquid
  ```
- The destination is `$WAYFINDER_LIBRARY_DIR/<protocol>/<name>.py`.
- The promoted copy gets a short header block (source + timestamp + optional description).
- A simple index is maintained at `$WAYFINDER_LIBRARY_DIR/index.json`.
