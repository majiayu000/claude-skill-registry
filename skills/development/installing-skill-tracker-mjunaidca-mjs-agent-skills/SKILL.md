---
name: installing-skill-tracker
description: |
  Installs Claude Code hooks for automatic skill usage measurement.
  Use when setting up skill tracking infrastructure in a new project.
  NOT when hooks are already installed (run verify.py to check).
---

## Quick Start

```bash
python .claude/skills/installing-skill-tracker/scripts/setup.py
python .claude/skills/installing-skill-tracker/scripts/verify.py
```

## Instructions

1. **Run setup** to install tracking hooks:
   ```bash
   python .claude/skills/installing-skill-tracker/scripts/setup.py
   ```

2. **Verify installation**:
   ```bash
   python .claude/skills/installing-skill-tracker/scripts/verify.py
   ```

3. **View usage analysis** (after some skill usage):
   ```bash
   python .claude/hooks/analyze-skills.py
   ```

## If Verification Fails

1. **Check jq is installed**:
   ```bash
   jq --version || echo "Install jq: brew install jq"
   ```

2. **Check hook scripts exist**:
   ```bash
   ls -la .claude/hooks/track-*.sh
   ```

3. **Check settings.json**:
   ```bash
   cat .claude/settings.json | jq .hooks
   ```

4. **Re-run setup** if components missing:
   ```bash
   python .claude/skills/installing-skill-tracker/scripts/setup.py
   ```

**Stop and report** if verification still fails after re-running setup.
