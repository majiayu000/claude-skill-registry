---
name: minion-patch
description: >
  Use when a mechanical code change needs review before applying.
  Delegates grunt work to local LLMs — saves cloud tokens. Generates patch for review.
  Use for changes that might need adjustment. Files must be <500 lines.
allowed-tools: Bash, Read, Glob, Grep
---

# Minion Patch

Generate a patch for manual review.

## When to Invoke

- Changes need careful review before applying
- User wants to see diff before commit
- Complex changes that might need adjustment

## Command

```bash
source .venv/bin/activate && python scripts/minions.py --json patch "<task>" --target <file> --read <file>
```

## Examples

```bash
# Generate patch
python scripts/minions.py --json patch "Add TODO comment at top" --target src/foo.py --read src/foo.py

# Multiple targets
python scripts/minions.py --json patch "Add header" --target src/a.py --target src/b.py --read src/a.py --read src/b.py
```

## Output

```json
{
  "task": "Add TODO comment",
  "patch_path": "sessions/20260112-123456.patch",
  "summary": "Added comment to foo.py"
}
```

## Applying Patches

```bash
# Review
cat sessions/*.patch

# Dry-run
patch -p1 --dry-run < sessions/*.patch

# Apply
patch -p1 < sessions/*.patch
```

## Limits

- Files <500 lines (32K context)
- Mechanical changes only
- Always pass --read with target file
