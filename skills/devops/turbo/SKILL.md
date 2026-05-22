---
name: turbo
description: Fix and update Turborepo (Turbo) configuration and task setup. Use for turbo.json errors, schema updates (pipeline -> tasks), and package-level config issues like missing extends.
---

# Turbo Config Skill

## Core workflow

- Read the error output and identify whether it references root or package config.
- If a package-level `turbo.json` exists (inside a workspace package), ensure it includes `extends: ["//"]` to inherit the root configuration.
- Update deprecated keys: rename `pipeline` to `tasks` for Turbo 2+ configs.

## Tip/lesson (package-level config)

If Turbo reports `No "extends" key found` for a package-level `turbo.json`, add:

```
extends: ["//"]
```

This is required for package configurations to inherit the root config.
