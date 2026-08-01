---
name: dependency-updater
description: Smart dependency update checker with changelog summaries and breaking
  change detection.
---

---
name: dependency-updater
description: Analyze and update Python dependencies in pyproject.toml, checking for compatibility and security vulnerabilities. Use when: updating dependencies, checking security issues, dependency analysis, version pinning, pip-audit, outdated packages.
---

# Dependency Updater

Manage Python dependencies systematically.

## Analysis Commands

```bash
# List installed packages
pip list

# Check for outdated
pip list --outdated

# Security check
pip-audit

# Dependency tree
pipdeptree
```

## Update Priority

1. **Critical Security Fixes** - Update immediately
2. **Bug Fixes** - Next patch release
3. **New Features** - Evaluate need
4. **Major Versions** - Plan migration

## Version Pinning

```toml
[project]
dependencies = [
    # Core: Pin to minor version
    "PySide6>=6.6.0,<6.7.0",

    # Infrastructure: Pin to patch
    "asyncpg>=0.29.0,<0.30.0",

    # Utilities: Allow minor updates
    "loguru>=0.7.2",
]
```

## Core Framework

- `PySide6` - Qt GUI framework
- `NodeGraphQt` - Node graph visualization
- `Playwright` - Browser automation
- `qasync` - Qt + asyncio bridge

## Update Workflow

1. Research updates (changelogs, breaking changes)
2. Update `pyproject.toml`
3. Test in clean environment
4. Run full test suite
5. Update CHANGELOG.md

## Special Cases

### Playwright Updates
```bash
playwright install chromium
pytest tests/nodes/browser/ -v
```

### Database Drivers
```bash
pytest tests/infrastructure/resources/test_database_manager.py -v
```
