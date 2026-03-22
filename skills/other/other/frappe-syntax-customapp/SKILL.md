---
name: frappe-syntax-customapp
description: >
  Use when building Frappe custom apps from scratch. Covers app structure,
  pyproject.toml configuration, module creation, patches, and fixtures
  for v14/v15/v16. Prevents common mistakes with app scaffolding and
  module organization. Keywords: custom app, bench new-app, pyproject.toml,
  patches, fixtures, modules, app structure.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Custom App Syntax

Deterministic syntax reference for building Frappe custom apps — scaffolding, configuration, modules, patches, and fixtures.

## Decision Tree

```
What do you need?
├─ Brand new app from scratch → bench new-app
├─ Extend existing ERPNext behavior → bench new-app + required_apps = ["frappe", "erpnext"]
├─ Install existing app from Git → bench get-app <url>
└─ Add functionality to an installed app
   ├─ New data model → Add module to modules.txt + create DocType
   ├─ New fields on existing DocType → Fixtures (Custom Field)
   ├─ Modify field properties → Fixtures (Property Setter)
   └─ Data migration → Patch in patches.txt

New app vs extend existing?
├─ Independent functionality → New app
├─ Tightly coupled to one app → New app with required_apps dependency
└─ Small customization (fields, properties) → Extend via fixtures in existing custom app
```

## Creating an App

```bash
# Create new app (interactive prompts for title, description, publisher, etc.)
bench new-app my_custom_app

# Install on site
bench --site mysite install-app my_custom_app

# Get existing app from Git
bench get-app https://github.com/org/my_custom_app

# Build frontend assets
bench build --app my_custom_app

# Run migrations (patches + fixtures + schema sync)
bench --site mysite migrate
```

## App Directory Structure

### [v15+] pyproject.toml (Primary)

```
apps/my_custom_app/
├── pyproject.toml                     # Build configuration (flit)
├── README.md
├── my_custom_app/                     # Inner Python package
│   ├── __init__.py                    # MUST contain __version__
│   ├── hooks.py                       # Frappe integration hooks
│   ├── modules.txt                    # Module registration
│   ├── patches.txt                    # Migration scripts
│   ├── patches/                       # Patch files
│   │   └── __init__.py
│   ├── my_custom_app/                 # Default module (same name as app)
│   │   ├── __init__.py
│   │   └── doctype/
│   ├── public/                        # Static assets → /assets/my_custom_app/
│   │   ├── css/
│   │   └── js/
│   ├── templates/                     # Jinja templates
│   │   └── includes/
│   └── www/                           # Portal pages (URL = directory path)
└── .git/
```

### [v14] setup.py (Legacy)

```
apps/my_custom_app/
├── setup.py                           # Build configuration (setuptools)
├── MANIFEST.in
├── requirements.txt                   # Python dependencies
├── dev-requirements.txt               # Dev dependencies (developer_mode only)
├── package.json                       # Node dependencies
├── my_custom_app/
│   ├── __init__.py
│   ├── hooks.py
│   ├── modules.txt
│   ├── patches.txt
│   └── [same inner structure as v15]
└── .git/
```

## Critical Files

### __init__.py (REQUIRED)

```python
# my_custom_app/__init__.py
__version__ = "0.0.1"
```

**CRITICAL**: Without `__version__`, the flit build FAILS and the app CANNOT be installed.

### pyproject.toml [v15+]

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
dependencies = []            # Python packages ONLY — NEVER Frappe/ERPNext

[tool.bench.frappe-dependencies]
frappe = ">=15.0.0,<16.0.0"
erpnext = ">=15.0.0,<16.0.0"  # Only if app extends ERPNext
```

**CRITICAL rules for pyproject.toml**:
- `name` MUST match the inner directory name exactly
- `dynamic = ["version"]` is REQUIRED — flit reads `__version__` from `__init__.py`
- NEVER put `frappe` or `erpnext` in `[project] dependencies` (they are not on PyPI)
- ALWAYS put Frappe app dependencies in `[tool.bench.frappe-dependencies]`

### setup.py [v14] (Legacy)

```python
from setuptools import setup, find_packages

setup(
    name="my_custom_app",
    version="0.0.1",
    description="Description of your app",
    author="Your Company",
    author_email="dev@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[],
)
```

### hooks.py (Minimal Skeleton)

```python
app_name = "my_custom_app"
app_title = "My Custom App"
app_publisher = "Your Company"
app_description = "Description"
app_email = "dev@example.com"
app_license = "MIT"

required_apps = ["frappe"]  # Or ["frappe", "erpnext"] if extending ERPNext

fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "My Custom App"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "My Custom App"]]},
]
```

## Modules

### modules.txt

```
My Custom App
Integrations
Settings
Reports
```

**Rules**:
- One module name per line — NEVER leave empty lines or trailing spaces
- Module name uses spaces; directory name uses underscores (`My Custom App` → `my_custom_app/`)
- Every DocType MUST belong to a registered module
- ALWAYS include `__init__.py` in every module directory

### Module Directory Structure

```
my_custom_app/
├── my_custom_app/       # "My Custom App" module
│   ├── __init__.py
│   └── doctype/
├── integrations/        # "Integrations" module
│   ├── __init__.py
│   └── doctype/
├── settings/            # "Settings" module
│   ├── __init__.py
│   └── doctype/
└── reports/             # "Reports" module
    ├── __init__.py
    └── report/
```

### DocType Directory (within a module)

```
doctype/my_doctype/
├── __init__.py              # Empty (REQUIRED)
├── my_doctype.json          # DocType definition (generated by UI)
├── my_doctype.py            # Python controller
├── my_doctype.js            # Client script
├── test_my_doctype.py       # Unit tests
└── my_doctype_dashboard.py  # Dashboard config
```

## Patches (Migration Scripts)

### patches.txt with INI Sections

```ini
[pre_model_sync]
# Runs BEFORE schema sync — old fields still available
myapp.patches.v1_0.backup_old_data

[post_model_sync]
# Runs AFTER schema sync — new fields available
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
            limit_start=offset,
        )
        if not records:
            break

        for record in records:
            frappe.db.set_value(
                "MyDocType", record.name,
                "new_field", "default_value",
                update_modified=False,
            )

        frappe.db.commit()
        offset += batch_size
```

### Pre vs Post Model Sync

| Situation | Section | Reason |
|-----------|---------|--------|
| Migrate data from old field | `[pre_model_sync]` | Old field still exists |
| Rename field + preserve data | `[pre_model_sync]` | Old name still available |
| Populate new required fields | `[post_model_sync]` | New field already exists |
| General data cleanup | `[post_model_sync]` | No schema dependency |

### Re-running a Patch

```
# Patches run ONCE. To re-run, make the line unique with a comment:
myapp.patches.v1_0.my_patch #2024-01-15
```

### bench migrate Workflow

1. `before_migrate` hooks execute
2. `[pre_model_sync]` patches execute
3. Database schema sync (DocType JSON → tables)
4. `[post_model_sync]` patches execute
5. Fixtures sync
6. `after_migrate` hooks execute

## Fixtures

### hooks.py Configuration

```python
fixtures = [
    "Category",                                              # All records
    {"dt": "Custom Field", "filters": [["module", "=", "My Custom App"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "My Custom App"]]},
    {"dt": "Role", "filters": [["name", "like", "MyApp%"]]},
]
```

### Exporting and Importing

```bash
# Export fixtures to JSON files
bench --site mysite export-fixtures --app my_custom_app

# Import happens automatically during bench migrate or install-app
```

### Fixtures vs Patches

| What | Fixtures | Patches |
|------|:--------:|:-------:|
| Custom Fields | YES | NO |
| Property Setters | YES | NO |
| Roles, Workflows | YES | NO |
| Data transformation | NO | YES |
| One-time migration | NO | YES |
| Seed configuration data | YES | NO |

### Fixture Ordering

ALWAYS order fixtures so dependencies come first:

```python
fixtures = [
    "Workflow State",   # FIRST — Workflow depends on states
    "Workflow",         # SECOND
]
```

## Version Differences

| Aspect | v14 | v15+ | v16+ |
|--------|-----|------|------|
| Build config | setup.py | pyproject.toml | pyproject.toml |
| Build backend | setuptools | flit_core | flit_core |
| Dependencies file | requirements.txt | pyproject.toml | pyproject.toml |
| Python minimum | >=3.10 | >=3.10 | >=3.14 |
| INI patches | YES | YES | YES |

### Migration v14 to v15

1. Create `pyproject.toml` with flit_core build-system
2. Move dependencies from `requirements.txt` to `[project] dependencies`
3. Verify `__version__` in `__init__.py`
4. Optionally remove: `setup.py`, `MANIFEST.in`, `requirements.txt`
5. Test with `bench get-app` and `bench install-app`

## Critical Rules

### ALWAYS

1. Define `__version__` in `__init__.py` — flit build fails without it
2. Add `dynamic = ["version"]` in pyproject.toml
3. Register EVERY module in `modules.txt`
4. Include `__init__.py` in EVERY Python directory
5. Put Frappe dependencies in `[tool.bench.frappe-dependencies]`, NEVER in `[project] dependencies`
6. Use batch processing and error handling in patches
7. Set `module` field on Custom Fields and Property Setters for correct fixture export
8. Order fixtures by dependency (states before workflows)

### NEVER

1. Put `frappe` or `erpnext` in pip dependencies (not on PyPI — install fails)
2. Create patches without try/except and logging
3. Include user data or transactional data (Sales Invoice, User) in fixtures
4. Hardcode site-specific values in patches
5. Process large datasets without batching and periodic `frappe.db.commit()`
6. Use spaces in directory names (spaces in `modules.txt` only)
7. Change module names after DocTypes have been created in production

## Reference Files

| File | Contents |
|------|----------|
| [structure.md](references/structure.md) | Complete directory structure for v14 and v15 |
| [pyproject-toml.md](references/pyproject-toml.md) | Full pyproject.toml and setup.py configuration |
| [modules.md](references/modules.md) | Module organization, naming, workspaces |
| [patches.md](references/patches.md) | Patch syntax, pre/post model sync, batch processing |
| [fixtures.md](references/fixtures.md) | Fixture configuration, filters, common DocTypes |
| [examples.md](references/examples.md) | Complete minimal and ERPNext extension app examples |
| [anti-patterns.md](references/anti-patterns.md) | Top 10 mistakes and corrections |

## See Also

- `frappe-syntax-hooks` — Full hooks.py reference
- `frappe-syntax-controllers` — DocType controller methods
- `frappe-impl-customapp` — Implementation patterns and workflows
