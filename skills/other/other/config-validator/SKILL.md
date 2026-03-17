---
name: config-validator
description: Validate wavecapsdr.yaml configuration files for syntax errors, schema violations, and logical inconsistencies. Use when editing config, troubleshooting startup failures, or verifying recipe/preset definitions before deployment.
---

# Config Validator for WaveCap-SDR

This skill validates `backend/config/wavecapsdr.yaml` for errors and provides helpful suggestions.

## When to Use This Skill

Use this skill when:
- Server fails to start with config errors
- Editing wavecapsdr.yaml manually
- Adding new presets or recipes
- Migrating config between environments
- Troubleshooting "invalid config" errors

## Usage

Validate the default config:

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/config-validator/validate_config.py
```

Validate a specific config file:

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/config-validator/validate_config.py \
  --config /path/to/wavecapsdr.yaml
```

## Common Validation Errors

### YAML Syntax Errors
- Missing colons
- Incorrect indentation (use spaces, not tabs)
- Unquoted special characters

### Schema Violations
- Missing required fields (server.port, device.driver)
- Invalid types (string for integer field)
- Out-of-range values (negative sample rate)

### Logical Errors
- Center frequency outside device range
- Sample rate not supported by device
- Channel offset beyond sample rate
- Duplicate recipe/preset names

## Files in This Skill

- `SKILL.md`: This file
- `validate_config.py`: Config validation script
