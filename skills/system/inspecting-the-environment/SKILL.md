---
name: inspecting-the-environment
description: Fast environment briefing for agents and subagents. Use at session start to learn OS/shell, container/WSL/VM status, git repo + upstream + dirty state, Python venv status/locations, markdown folders to read, and availability of common tools (uv, mcpc, rg/grep/jq/git/python/node/npm/pnpm, etc.).
---
# Environment Inspection

## Overview
Collect a quick, machine-readable snapshot of the current workspace so agents know operating constraints, dev tooling, and where to look first for context.

## Quick Start
Generate JSON (default):
```text
python scripts/inspect_environment.py
```
Readable text:
```text
python scripts/inspect_environment.py --format text
```

Key fields:
- `os`: system, release, version, machine
- `shell`: detected shell/command host
- `environment`: container hint, WSL flag, VM hint (via systemd-detect-virt when available)
- `git`: repo presence, root, branch, upstream, dirty state
- `python`: interpreter path/version, active venv/conda, whether running inside a venv
- `virtualenv_dirs`: nearby `.venv`/`venv`/`env` folders
- `markdown_dirs`: directories (depth-limited) containing `.md` files worth skimming
- `tools`: availability of common CLIs (uv, mcpc, rg/grep/jq/git/python/node/npm/pnpm, etc.)

## Options
- `--root PATH` to inspect a different directory (default: cwd).
- `--format json|text` for programmatic vs quick-read output (default: json).
- `--md-limit N` / `--md-depth N` to cap markdown directory discovery (defaults: 40 dirs, depth 5; skips .git/node_modules/.venv/venv/.tox/dist/build/.cache).
- `--extra-tool NAME` (repeatable) to probe additional binaries.

## Notes and Heuristics
- Container detection uses marker files and `/proc/1/cgroup`; WSL is reported separately.
- VM detection is opportunistic via `systemd-detect-virt`; missing tools yield `null`.
- Git checks are no-op outside a repo and never modify state.
- Traversal is pruned to avoid heavy dirs; adjust limits if you need more coverage.
