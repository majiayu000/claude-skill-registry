---
name: pdm-migration-specialist
description: Migrate pyproject.toml from pre-PDM 2.0 syntax to modern PEP-compliant format. Focuses on dev-dependencies to dependency-groups conversion and PEP 621 project metadata. Integrates with Context7 for latest PDM documentation.
---

# PDM Migration Specialist

Focused skill for migrating pyproject.toml files from pre-PDM 2.0 legacy syntax to modern PEP-compliant format.

## When to Use

Activate when the user:
- Needs to migrate from `[tool.pdm.dev-dependencies]` to `[dependency-groups]`
- Wants to update legacy pyproject.toml to PEP 621 standards
- Asks about old vs new PDM syntax
- Needs to understand modern dependency specification
- Mentions PDM migration, legacy format, or pre-2.0 syntax
- Encounters deprecated PDM configuration patterns

## Core Capabilities

- **Dev Dependencies Migration**: Convert `[tool.pdm.dev-dependencies]` → `[dependency-groups]`
- **PEP 621 Compliance**: Migrate to standardized `[project]` table
- **Dependency Specification**: Modern PEP 440/508 formats
- **Build Backend Updates**: Migrate to `pdm-backend`
- **Local Dependencies**: Convert to `file:///${PROJECT_ROOT}/` syntax
- **Context7 Integration**: Fetch latest PDM migration docs

## Quick Migration Patterns

### Development Dependencies (Most Common)

**Old (Pre-2.0)**:
```toml
[tool.pdm.dev-dependencies]
test = ["pytest>=6.0", "pytest-cov"]
lint = ["flake8", "black"]
```

**New (PEP 735)**:
```toml
[dependency-groups]
test = ["pytest>=6.0", "pytest-cov"]
lint = ["flake8", "black"]
```

### Project Metadata

**Old (Legacy)**:
```toml
[tool.pdm]
name = "myproject"
version = "1.0.0"
```

**New (PEP 621)**:
```toml
[project]
name = "myproject"
version = "1.0.0"
dependencies = ["requests>=2.28.0"]
requires-python = ">=3.11"
```

### Build Backend

**Old**:
```toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
```

**New**:
```toml
[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"
```

## Key Differences

| Aspect | Pre-2.0 | Modern (2.0+) |
|--------|---------|---------------|
| Dev Dependencies | `[tool.pdm.dev-dependencies]` | `[dependency-groups]` |
| Project Metadata | `[tool.pdm]` or non-standard | `[project]` (PEP 621) |
| Optional Deps | Various formats | `[project.optional-dependencies]` |
| Local Paths | Relative paths | `file:///${PROJECT_ROOT}/` |
| Build Backend | setuptools/flit | `pdm-backend` preferred |

## CLI Changes

**Adding Dev Dependencies**:
```bash
# Old approach (still works but deprecated)
pdm add --dev pytest

# New approach (PEP 735)
pdm add -dG test pytest
```

## Reference Documentation

- **Detailed Migration Guide**: See `reference.md` in this directory
- **Real Migration Examples**: See `examples.md` in this directory
- **Context7 Library ID**: `/pdm-project/pdm`
- **Relevant PEPs**: PEP 621 (project metadata), PEP 735 (dependency groups)
