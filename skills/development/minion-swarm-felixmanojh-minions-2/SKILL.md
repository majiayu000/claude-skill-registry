---
name: minion-swarm
description: >
  PROACTIVELY USE when same mechanical change is needed on multiple files (add headers, comments, etc.).
  Delegates parallel grunt work to local LLMs — saves cloud tokens. Runs in parallel for speed.
  Use instead of repetitive manual edits. Files must be <500 lines each.
allowed-tools: Bash, Read, Glob, Grep
---

# Minion Swarm

Parallel patches on multiple files.

## When to Invoke

- Same change needed on many files
- Adding headers/comments across codebase
- Batch mechanical operations

## Command

```bash
source .venv/bin/activate && python scripts/minions.py --json swarm "<task>" <files...>
```

## Examples

```bash
# Add header to multiple files
python scripts/minions.py --json swarm "Add # Minions header" src/a.py src/b.py src/c.py

# With more workers
python scripts/minions.py --json swarm "Add docstring" *.py --workers 5
```

## Output

```json
{
  "completed": [{"target": "src/a.py", "result": "success"}],
  "failed": [],
  "stats": {"completed": 3, "failed": 0, "total": 3}
}
```

## Limits

- Each file <500 lines
- Mechanical changes only
- Default 3 parallel workers
