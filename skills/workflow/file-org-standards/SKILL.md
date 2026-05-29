---
name: file-org-standards
version: "1.0.0"
category: _internal
description: "File Organization Standards Skill"
---

# File Organization Standards Skill

> Version: 1.0.0
> Category: Standards
> Triggers: Creating files, organizing modules, folder structure

## Quick Reference

### Top-Level Structure (REQUIRED)
```
repository/
├── src/                 # Source code
├── tests/              # Test files
├── docs/               # Documentation
├── config/             # Configuration files
├── scripts/            # Utility scripts
├── data/               # Data files (raw, processed, results)
├── reports/            # Generated reports
└── .agent-os/          # Agent OS workflow files
```

### Module-Based Organization (src/)
```
src/
├── modules/            # Business/domain modules
│   ├── module_1/      # Domain-driven name
│   │   ├── __init__.py
│   │   ├── core.py
│   │   └── utils.py
│   └── shared/        # Shared utilities
└── __init__.py
```

## Naming Conventions

### Good Names (Domain-Driven)
✅ `marine_analysis/` - describes domain
✅ `data_processing/` - business purpose
✅ `api_gateway/` - technical purpose
✅ `authentication/` - feature domain

### Bad Names (Generic/Temporal)
❌ `python_files/` - too generic
❌ `utils/` - vague at top level
❌ `new_module/` - temporal
❌ `misc/` - meaningless
❌ `old/` or `temp/` - suggests temporary

## Folder Depth

**Maximum: 5 levels**
```
src/               # Level 1
└── modules/       # Level 2
    └── analysis/  # Level 3
        └── stress/ # Level 4
            └── components/ # Level 5 (MAX)
```

If you need deeper, re-evaluate module boundaries.

## When AI Organizes Files

**Triggers automatic organization after ~5 files accumulate:**

1. **AI recognizes pattern** → "I notice 5+ related files"
2. **AI proposes structure** → Shows folder layout
3. **Wait for approval** → "Should I proceed with this organization?"
4. **User confirms** → Only then execute reorganization
5. **AI updates imports** → All cross-references fixed

## Test Mirror Structure

Mirror src/ structure exactly:
```
tests/
├── unit/
│   └── modules/
│       └── module_name/
│           └── test_*.py
├── integration/
│   └── test_*_integration.py
└── fixtures/
    └── *.json
```

## Anti-Patterns to Avoid

```
❌ Overly generic
  src/stuff/, src/misc/, src/files/

❌ Technical instead of domain
  src/python_files/, src/yaml_configs/

❌ Temporal context
  src/old/, src/new/, src/v2/

❌ Too deep
  src/a/b/c/d/e/f/ (>5 levels)
```

## File Naming

| Type | Pattern | Example |
|------|---------|---------|
| Tests | `test_*.py` or `*_test.py` | `test_calculator.py` |
| Configs | `*.yaml` or `*.json` | `config.yaml` |
| Data | descriptive + extension | `raw_data.csv` |
| Reports | descriptive + `_report` | `analysis_report.html` |

## AI Decision Tree

When file count reaches threshold:
```
5+ files? → Yes → Same type? → Yes → AI proposes grouping
                ↓
           Logical pattern? → Yes → AI proposes organization
                ↓
         Different purposes? → Keep flat, use prefixes
```

## Full Reference

See: @docs/modules/standards/FILE_ORGANIZATION_STANDARDS.md

---

*Use this when organizing new modules, creating folder structures, or managing growing codebases.*
