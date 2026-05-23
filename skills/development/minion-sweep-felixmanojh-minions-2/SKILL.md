---
name: minion-sweep
description: >
  PROACTIVELY USE when user asks to add docstrings/types across multiple files or a directory.
  Delegates bulk grunt work to local LLMs — saves cloud tokens. Two phases: discover, then apply.
  Use instead of manually editing many files. Files must be <500 lines each.
allowed-tools: Bash, Read, Glob
---

# Minion Sweep

Codebase-wide maintenance scan.

## When to Invoke

- User requests "add docstrings to all files"
- Periodic codebase cleanup
- Tech debt reduction

## Commands

```bash
# Discover what needs work
source .venv/bin/activate && python scripts/minions.py --json sweep <dir> --task <task>

# Apply fixes
source .venv/bin/activate && python scripts/minions.py --json sweep <dir> --task <task> --apply
```

## Tasks

| Task | What it checks |
|------|----------------|
| `all` | Everything (default) |
| `docstrings` | Missing function/class/module docstrings |
| `types` | Missing type hints |
| `headers` | Missing module-level docstrings only |

## Examples

```bash
# Discover
python scripts/minions.py --json sweep src/ --task docstrings

# Apply
python scripts/minions.py --json sweep src/ --task docstrings --apply

# With backups
python scripts/minions.py --json sweep src/ --task all --apply --backup
```

## Output (Discover)

```json
{
  "candidates": [
    {"file": "src/foo.py", "lines": 120, "missing": ["3 functions without docstrings"]}
  ],
  "total_candidates": 1,
  "skipped": []
}
```

## Claude Integration

1. Run discover first to show scope
2. Confirm with user: "Found 12 files. Apply?"
3. Run with --apply on approval
4. Report summary
