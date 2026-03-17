---
name: cube-iml
user_invocable: true
description: |
  Check and repair PyCharm/IntelliJ module configuration (.iml file).
  Triggered by "/cube-iml" or when user reports PyCharm doesn't recognize src/tests folders.
---

# Cube IML Skill

Check and repair the PyCharm/IntelliJ module configuration file.

## Trigger

Use when:
- User runs `/cube-iml` or asks about PyCharm/IntelliJ configuration
- User reports "module not configured" or import resolution issues
- User says PyCharm doesn't recognize src or tests folders

## Action

Run the reconstruct script:

```bash
python dev-tools/reconstruct_iml.py
```

The script will:
- Auto-detect the Python interpreter from existing config
- Find all venv/cache folders to exclude
- Create backup if .iml already exists
- Generate a proper .iml with src as source and tests as test source

## Options

```bash
# Preview without writing (dry run)
python dev-tools/reconstruct_iml.py --dry-run

# Specify interpreter manually
python dev-tools/reconstruct_iml.py --interpreter "Python 3.14 (cubesolve)"
```

## After Running

Tell user: "If PyCharm doesn't pick up changes immediately, try **File → Invalidate Caches and Restart**."
