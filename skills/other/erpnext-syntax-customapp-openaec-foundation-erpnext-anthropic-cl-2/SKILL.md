---
name: erpnext-syntax-customapp
version: 1.0.0
description: "Deterministic syntax for building Frappe custom apps including app structure, pyproject.toml, modules, patches and fixtures"
author: OpenAEC Foundation
tags: [erpnext, frappe, custom-app, pyproject, patches, fixtures, modules]
languages: [en]
frappe_versions: [v14, v15, v16]
---

# ERPNext Custom App Syntax Skill

> Complete syntax for building Frappe custom apps in v14/v15, including build configuration, module organization, patches and fixtures.

---

## When to Use This Skill

USE this skill when you:
- Create a new Frappe/ERPNext custom app
- Configure pyproject.toml or setup.py
- Organize modules within an app
- Write database migration patches
- Configure fixtures for data export/import
- Manage app dependencies

DO NOT USE for:
- DocType controllers (use erpnext-syntax-controllers)
- Client Scripts (use erpnext-syntax-clientscripts)
- Server Scripts (use erpnext-syntax-serverscripts)
- Hooks configuration (use erpnext-syntax-hooks)

---

## App Structure Overview

### v15 (pyproject.toml - Primary)

```
apps/my_custom_app/
├── pyproject.toml                     # Build configuration
├── README.md
├── my_custom_app/                     # Main package
│   ├── __init__.py                    # MUST contain __version__!
│   ├── hooks.py                       # Frappe integration
│   ├── modules.txt                    # Module registration
│   ├── patches.txt                    # Migration scripts
│   ├── patches/                       # Patch files
│   ├── my_custom_app/                 # Default module
│   │   └── doctype/
│   ├── public/                        # Client assets
│   └── templates/                     # Jinja templates
└── .git/
```

> **See**: `references/structure.md` for complete directory structure.

---

## Critical Files

### __init__.py (REQUIRED)

```python
# my_custom_app/__init__.py
__version__ = "0.0.1"
```

**CRITICAL**: Without `__version__` the flit build fails!

### pyproject.toml (v15)

```toml
[build-system]
requires = ["flit_core >=3.4,<4"]
build-backend = "flit_core.buildapi"

[project]
name = "my_custom_app"
authors = [
    { name = "Your Company", email = "dev@example.com" }
]
description = "Description of your app"
requires-python = ">=3.10"
readme = "README.md"
dynamic = ["version"]
dependencies = []

[tool.bench.frappe-dependencies]
frappe = ">=15.0.0,<16.0.0"
erpnext = ">=15.0.0,<16.0.0"
```

> **See**: `references/pyproject-toml.md` for all configuration options.

---

## Modules

### modules.txt

```
My Custom App
Integrations
Settings
Reports
```

**Rules:**
- One module per line
- Spaces in name → underscores in directory
- Every DocType MUST belong to a module

### Module Directory

```
my_custom_app/
├── my_custom_app/       # "My Custom App" module
│   ├── __init__.py      # REQUIRED
│   └── doctype/
├── integrations/        # "Integrations" module
│   ├── __init__.py      # REQUIRED
│   └── doctype/
└── settings/            # "Settings" module
    ├── __init__.py      # REQUIRED
    └── doctype/
```

> **See**: `references/modules.md` for module organization.

---

## Patches (Migration Scripts)

### patches.txt with INI Sections

```ini
[pre_model_sync]
# Before schema sync - old fields still available
myapp.patches.v1_0.backup_old_data

[post_model_sync]
# After schema sync - new fields available
myapp.patches.v1_0.populate_new_fields
myapp.patches.v1_0.cleanup_data
```

### Patch Implementation

```python
# myapp/patches/v1_0/populate_new_fields.py
import frappe

def execute():
    """Populate new fields with default values."""
    
    batch_size = 1000
    offset = 0
    
    while True:
        records = frappe.get_all(
            "MyDocType",
            filters={"new_field": ["is", "not set"]},
            fields=["name"],
            limit_page_length=batch_size,
            limit_start=offset
        )
        
        if not records:
            break
        
        for record in records:
            frappe.db.set_value(
                "MyDocType",
                record.name,
                "new_field",
                "default_value",
                update_modified=False
            )
        
        frappe.db.commit()
        offset += batch_size
```

### When Pre vs Post Model Sync?

| Situation | Section |
|-----------|---------|
| Migrate data from old field | `[pre_model_sync]` |
| Populate new fields | `[post_model_sync]` |
| Data cleanup | `[post_model_sync]` |

> **See**: `references/patches.md` for complete patch documentation.

---

## Fixtures

### hooks.py Configuration

```python
fixtures = [
    # All records
    "Category",
    
    # With filter
    {
        "dt": "Custom Field",
        "filters": [["module", "=", "My Custom App"]]
    },
    
    # Multiple filters
    {
        "dt": "Property Setter",
        "filters": [
            ["module", "=", "My Custom App"],
            ["doc_type", "in", ["Sales Invoice", "Sales Order"]]
        ]
    }
]
```

### Exporting

```bash
bench --site mysite export-fixtures --app my_custom_app
```

### Common Fixture DocTypes

| DocType | Usage |
|---------|-------|
| `Custom Field` | Custom fields on existing DocTypes |
| `Property Setter` | Modify field properties |
| `Role` | Custom roles |
| `Workflow` | Workflow definitions |

> **See**: `references/fixtures.md` for fixture configuration.

---

## Minimal hooks.py

```python
app_name = "my_custom_app"
app_title = "My Custom App"
app_publisher = "Your Company"
app_description = "Description"
app_email = "dev@example.com"
app_license = "MIT"

required_apps = ["frappe"]  # Or ["frappe", "erpnext"]

fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "My Custom App"]]}
]
```

---

## Creating and Installing App

```bash
# Create new app
bench new-app my_custom_app

# Install on site
bench --site mysite install-app my_custom_app

# Migrate (patches + fixtures)
bench --site mysite migrate

# Build assets
bench build --app my_custom_app
```

---

## Version Differences

| Aspect | v14 | v15 |
|--------|-----|-----|
| Build config | setup.py | pyproject.toml |
| Dependencies | requirements.txt | In pyproject.toml |
| Build backend | setuptools | flit_core |
| Python minimum | >=3.10 | >=3.10 |
| INI patches | ✅ | ✅ |

---

## Critical Rules

### ✅ ALWAYS

1. Define `__version__` in `__init__.py`
2. Add `dynamic = ["version"]` in pyproject.toml
3. Register modules in `modules.txt`
4. Include `__init__.py` in EVERY directory
5. Put Frappe dependencies in `[tool.bench.frappe-dependencies]`
6. Add error handling in patches
7. Use batch processing for large datasets

### ❌ NEVER

1. Put Frappe/ERPNext in project dependencies (not on PyPI)
2. Create patches without error handling
3. Include user/transactional data in fixtures
4. Hardcode site-specific values
5. Process large datasets without batching

---

## Fixtures vs Patches

| What | Fixtures | Patches |
|------|:--------:|:-------:|
| Custom Fields | ✅ | ❌ |
| Property Setters | ✅ | ❌ |
| Roles/Workflows | ✅ | ❌ |
| Data transformation | ❌ | ✅ |
| Data cleanup | ❌ | ✅ |
| One-time migration | ❌ | ✅ |

---

## Reference Files

| File | Contents |
|------|----------|
| `references/structure.md` | Complete directory structure |
| `references/pyproject-toml.md` | Build configuration options |
| `references/modules.md` | Module organization |
| `references/patches.md` | Migration scripts |
| `references/fixtures.md` | Data export/import |
| `references/examples.md` | Complete app examples |
| `references/anti-patterns.md` | Mistakes to avoid |

---

## See Also

- `erpnext-syntax-hooks` - For hooks.py configuration
- `erpnext-syntax-controllers` - For DocType controllers
- `erpnext-impl-customapp` - For implementation patterns
