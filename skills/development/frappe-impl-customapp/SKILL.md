---
name: frappe-impl-customapp
description: >
  Use when building a custom Frappe app from scratch. Covers bench new-app
  walkthrough, app structure decisions, adding DocTypes, hooks, patches,
  fixtures management, development workflow (bench migrate, build,
  clear-cache), testing, packaging, installing on another site, version
  management, and app dependencies for v14/v15/v16. Keywords: create custom
  app, new frappe app, bench new-app, app structure, module creation,
  doctype creation, fixtures, patches, deployment, packaging.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Custom App - Implementation

Workflow for building a custom Frappe app from scratch. For exact syntax, see `frappe-syntax-customapp`.

**Version**: v14/v15/v16 compatible

---

## Main Decision: Do You Need a Custom App?

```
WHAT CHANGES DO YOU NEED?
|
+-- Add fields to existing DocType?
|   +-- NO APP NEEDED: Custom Field + Property Setter
|
+-- Simple automation/validation (<50 lines)?
|   +-- NO APP NEEDED: Server Script or Client Script
|
+-- Complex business logic, new DocTypes, or Python code?
|   +-- YES: Create custom app
|
+-- Integration with external system (needs imports)?
|   +-- YES: Custom app REQUIRED (Server Scripts block imports)
|
+-- Custom reports with complex queries?
|   +-- Script Report (no app) vs Query Report (app optional)
```

**Rule**: ALWAYS start with the simplest solution. Server Scripts + Custom Fields solve 70% of needs without a custom app.

---

## Step 1: Create App Structure

```bash
cd ~/frappe-bench
bench new-app my_app
# Prompts: Title, Description, Publisher, Email, License
```

ALWAYS verify immediately:
```python
# my_app/my_app/__init__.py MUST have:
__version__ = "0.0.1"
```

---

## Step 2: Configure pyproject.toml (v15+)

```toml
[build-system]
requires = ["flit_core >=3.4,<4"]
build-backend = "flit_core.buildapi"

[project]
name = "my_app"
authors = [{ name = "Your Company", email = "dev@example.com" }]
description = "Your app description"
requires-python = ">=3.10"
readme = "README.md"
dynamic = ["version"]
dependencies = [
    "requests>=2.28.0"   # Only PyPI packages here
]

[tool.bench.frappe-dependencies]
frappe = ">=15.0.0,<16.0.0"
# erpnext = ">=15.0.0,<16.0.0"  # Only if needed
```

**Rule**: NEVER put frappe or erpnext in `[project].dependencies` -- they are NOT on PyPI.

---

## Step 3: Configure hooks.py

```python
app_name = "my_app"
app_title = "My App"
app_publisher = "Your Company"
app_description = "Description"
app_email = "dev@example.com"
app_license = "MIT"

required_apps = ["frappe"]  # Or ["frappe", "erpnext"]

fixtures = []  # Configured later
```

**Rule**: ALWAYS declare `required_apps` with all dependencies.

---

## Step 4: Define Modules

```text
# my_app/my_app/modules.txt
My App
```

| App Size | Module Strategy |
|----------|----------------|
| 1-5 DocTypes | ONE module with app name |
| 6-15 DocTypes | 2-4 modules by functional area |
| 15+ DocTypes | Modules by business domain |

**Rule**: Each DocType belongs to EXACTLY one module. Module name in `modules.txt` maps to directory: `My Custom App` --> `my_custom_app/`.

### Adding a Module
```bash
mkdir -p my_app/my_app/new_module/doctype
touch my_app/my_app/new_module/__init__.py
# Add "New Module" to modules.txt
bench --site mysite migrate
```

---

## Step 5: Install and Create DocTypes

```bash
# Install app on site
bench --site mysite install-app my_app

# Create DocType (via UI recommended, or CLI)
bench --site mysite new-doctype "My Document" --module "My App"
```

This creates:
```
my_app/my_app/doctype/my_document/
+-- my_document.json    # DocType definition
+-- my_document.py      # Controller
+-- my_document.js      # Client script
+-- test_my_document.py # Tests
```

---

## Step 6: Add Hooks

### doc_events (v14/v15/v16)
```python
doc_events = {
    "Sales Invoice": {
        "validate": "my_app.events.sales_invoice.validate",
        "on_submit": "my_app.events.sales_invoice.on_submit"
    }
}
```

### extend_doctype_class (v16 ONLY -- preferred)
```python
extend_doctype_class = {
    "Sales Invoice": "my_app.overrides.sales_invoice.CustomSalesInvoice"
}
```

**Rule**: ALWAYS call `super().method()` when overriding lifecycle methods in v16.

### Scheduler Events
```python
scheduler_events = {
    "daily": ["my_app.tasks.daily_cleanup"],
    "cron": {"0 9 * * 1-5": ["my_app.tasks.morning_report"]}
}
```

See `frappe-impl-hooks` and `frappe-impl-scheduler` for complete patterns.

---

## Step 7: Add Patches

### Create Patch File
```bash
mkdir -p my_app/my_app/patches/v1_0
touch my_app/my_app/patches/__init__.py
touch my_app/my_app/patches/v1_0/__init__.py
```

```python
# my_app/my_app/patches/v1_0/populate_defaults.py
import frappe

def execute():
    if not frappe.db.has_column("My DocType", "target_field"):
        return  # Skip if not applicable

    batch_size = 1000
    offset = 0
    while True:
        records = frappe.get_all("My DocType",
            limit_page_length=batch_size, limit_start=offset)
        if not records:
            break
        for r in records:
            frappe.db.set_value("My DocType", r.name,
                "target_field", "default", update_modified=False)
        frappe.db.commit()
        offset += batch_size
```

### Register in patches.txt
```ini
[pre_model_sync]
# Patches that run BEFORE schema changes (backup data from deleted fields)

[post_model_sync]
# Patches that run AFTER schema changes (populate new fields)
my_app.patches.v1_0.populate_defaults
```

**Rules**:
- ALWAYS check if patch is needed (guard clause)
- ALWAYS batch process 1000+ records
- ALWAYS commit after each batch
- NEVER run untested patches on production

---

## Step 8: Fixtures Management

### Configure in hooks.py
```python
fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "My App"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "My App"]]},
    {"dt": "Role", "filters": [["name", "in", ["My App User", "My App Manager"]]]},
    {"dt": "Workflow", "filters": [["document_type", "=", "My DocType"]]},
    "My Category",  # All records of your own config DocType
]
```

### Export and Verify
```bash
bench --site mysite export-fixtures --app my_app
ls my_app/my_app/fixtures/
# custom_field.json, property_setter.json, etc.
```

**Rules**:
- ALWAYS filter fixtures to YOUR app's customizations
- NEVER include transactional data (invoices, orders)
- NEVER export without filters for shared DocTypes (Custom Field, Workflow)
- Fixtures auto-import during `bench migrate`

---

## Step 9: Development Workflow

### Essential Commands
```bash
# After schema changes (DocType fields, hooks.py, patches)
bench --site mysite migrate

# After JS/CSS changes
bench build --app my_app

# After Python changes (controllers, events)
bench --site mysite clear-cache

# Full restart (production)
bench restart

# Watch mode (development)
bench watch  # Auto-rebuilds on file changes
```

### Development Cycle
```
1. Edit code/DocType
2. bench --site mysite migrate (if schema changed)
3. bench build --app my_app (if JS/CSS changed)
4. bench --site mysite clear-cache (if Python changed)
5. Test in browser
6. Repeat
```

---

## Step 10: Testing the App

```bash
# Run all tests
bench --site mysite run-tests --app my_app

# Run specific test
bench --site mysite run-tests --module my_app.my_module.doctype.my_doctype.test_my_doctype

# Run with verbose output
bench --site mysite run-tests --app my_app -v
```

See `frappe-testing-unit` for writing test cases.

---

## Step 11: Packaging for Distribution

### Via Git (standard method)
```bash
cd apps/my_app
git init && git add . && git commit -m "Initial commit"
git remote add origin https://github.com/org/my_app.git
git push -u origin main
```

### Install on Another Site
```bash
# On target bench
bench get-app https://github.com/org/my_app.git
bench --site target-site install-app my_app
bench --site target-site migrate
```

### Version Management
```python
# my_app/my_app/__init__.py
__version__ = "1.0.0"  # Semantic versioning: MAJOR.MINOR.PATCH
```

| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| Breaking changes | MAJOR | 1.x -> 2.0.0 |
| New features | MINOR | 1.1.x -> 1.2.0 |
| Bug fixes | PATCH | 1.2.0 -> 1.2.1 |

---

## Step 12: App Dependencies

### Frappe/ERPNext Dependencies
```python
# hooks.py
required_apps = ["frappe", "erpnext"]  # Install order matters
```

```toml
# pyproject.toml
[tool.bench.frappe-dependencies]
frappe = ">=15.0.0,<16.0.0"
erpnext = ">=15.0.0,<16.0.0"
```

### Python Package Dependencies
```toml
[project]
dependencies = ["requests>=2.28.0", "pandas>=1.5.0"]
```

**Rule**: NEVER create circular dependencies between apps.

---

## Version-Specific Considerations

| Aspect | v14 | v15 | v16 |
|--------|-----|-----|-----|
| Build config | setup.py | pyproject.toml | pyproject.toml |
| DocType extension | doc_events | doc_events | `extend_doctype_class` preferred |
| Python minimum | 3.10 | 3.10 | 3.11 |
| Patch format | INI sections | INI sections | INI sections |

### v16 Breaking Changes to Know
- `extend_doctype_class` hook: Cleaner extension via mixins
- Data masking: Field-level privacy configuration
- UUID naming: New naming rule option
- Chrome PDF: wkhtmltopdf deprecated

---

## Critical Rules Summary

### ALWAYS
1. Start with `bench new-app` - NEVER create structure manually
2. Define `__version__` in `__init__.py`
3. Use `dynamic = ["version"]` in pyproject.toml
4. Test patches on database copy before production
5. Filter fixtures to your app's customizations only
6. Version your patches (v1_0, v2_0 directories)
7. Test installation on a fresh site

### NEVER
1. Put frappe/erpnext in `[project].dependencies`
2. Include transactional data in fixtures
3. Hardcode site-specific values (use settings DocTypes)
4. Skip `frappe.db.commit()` in large patches
5. Delete fields without backup patch
6. Modify core ERPNext files directly

---

## Reference Files

| File | Contents |
|------|----------|
| [workflows.md](references/workflows.md) | 8 step-by-step implementation guides |
| [decision-tree.md](references/decision-tree.md) | Complete decision flowcharts |
| [examples.md](references/examples.md) | 5 complete working app examples |
| [anti-patterns.md](references/anti-patterns.md) | Common mistakes to avoid |

## See Also

- `frappe-syntax-customapp` - Exact syntax reference
- `frappe-syntax-hooks` - Hooks configuration syntax
- `frappe-impl-hooks` - Hook implementation patterns
- `frappe-core-database` - Database operations for patches
- `frappe-impl-scheduler` - Scheduled task implementation
- `frappe-ops-bench` - Bench commands reference
- `frappe-ops-app-lifecycle` - App versioning and release management
- `frappe-testing-unit` - Writing tests for your app
- `frappe-testing-cicd` - CI/CD pipeline for app testing
