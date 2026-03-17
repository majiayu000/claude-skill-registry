---
name: erpnext-impl-customapp
description: "Implementation workflows for building Frappe/ERPNext custom apps. Covers app structure, module creation, doctype design, fixtures, patches, and deployment. V14/V15/V16 compatible. Triggers: create custom app, new frappe app, bench new-app, app structure, module creation, doctype creation, fixtures, patches."
---

# ERPNext Custom App - Implementation

This skill helps you determine HOW to build and structure Frappe/ERPNext custom apps. For exact syntax, see `erpnext-syntax-customapp`.

**Version**: v14/v15/v16 compatible (differences noted)

---

## Main Decision: What Are You Building?

```
┌─────────────────────────────────────────────────────────────────────────┐
│ WHAT DO YOU WANT TO CREATE?                                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ► Completely new Frappe/ERPNext app?                                    │
│   └─► See: NEW APP WORKFLOW                                             │
│                                                                         │
│ ► Extend existing ERPNext functionality?                                │
│   └─► See: EXTENSION DECISION                                           │
│                                                                         │
│ ► Migrate data between fields/DocTypes?                                 │
│   └─► See: PATCH vs FIXTURE DECISION                                    │
│                                                                         │
│ ► Export configuration for deployment?                                  │
│   └─► See: FIXTURE WORKFLOW                                             │
│                                                                         │
│ ► Update existing app to newer Frappe version?                          │
│   └─► See: VERSION UPGRADE WORKFLOW                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Decision 1: Do You Need a Custom App?

```
┌─────────────────────────────────────────────────────────────────────────┐
│ DO YOU ACTUALLY NEED A CUSTOM APP?                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ What changes do you need?                                               │
│                                                                         │
│ ► Add fields to existing DocType?                                       │
│   └─► NO APP NEEDED: Use Custom Field + Property Setter                 │
│       (Can be exported as fixtures from ANY app)                        │
│                                                                         │
│ ► Simple automation/validation?                                         │
│   └─► NO APP NEEDED: Server Script or Client Script                     │
│       (Stored in database, no deployment needed)                        │
│                                                                         │
│ ► Complex business logic, new DocTypes, or Python code?                 │
│   └─► YES, CREATE APP: You need controllers, models, and deployment     │
│                                                                         │
│ ► Integration with external system?                                     │
│   └─► USUALLY YES: APIs need whitelisted methods, scheduled sync        │
│                                                                         │
│ ► Custom reports with complex queries?                                  │
│   └─► DEPENDS: Script Report (no app) vs Query Report (app optional)    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Rule**: Start with the SIMPLEST solution. Server Scripts + Custom Fields solve 70% of customization needs without a custom app.

---

## Decision 2: Extension Strategy

```
┌─────────────────────────────────────────────────────────────────────────┐
│ HOW TO EXTEND ERPNext?                                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ► Add fields to existing DocType (e.g., Sales Invoice)?                 │
│   └─► Custom Field (via UI or fixtures)                                 │
│   └─► Property Setter for behavior changes                              │
│                                                                         │
│ ► Modify DocType behavior/logic?                                        │
│   ├─► v16: Use `extend_doctype_class` hook (PREFERRED)                  │
│   └─► v14/v15: Use `doc_events` hooks in hooks.py                       │
│                                                                         │
│ ► Override Jinja template?                                              │
│   └─► Copy template to your app's templates/ folder                     │
│   └─► Register via `jinja.override_template` in hooks.py                │
│                                                                         │
│ ► Add new DocType related to existing?                                  │
│   └─► Create in your app's module                                       │
│   └─► Link via Link field or Dynamic Link                               │
│                                                                         │
│ ► Add new workspace/menu items?                                         │
│   └─► Create Workspace DocType in your app                              │
│   └─► Or use `standard_portal_menu_items` hook                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

> **See**: `references/decision-tree.md` for detailed extension patterns.

---

## Decision 3: Patch vs Fixture

```
┌─────────────────────────────────────────────────────────────────────────┐
│ SHOULD THIS BE A PATCH OR A FIXTURE?                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ Is it CONFIGURATION that should be the same everywhere?                 │
│ (Custom Fields, Roles, Workflows, Property Setters)                     │
│   └─► USE FIXTURE                                                       │
│                                                                         │
│ Is it a ONE-TIME data transformation?                                   │
│ (Migrate old field values, cleanup bad data, populate defaults)         │
│   └─► USE PATCH                                                         │
│                                                                         │
│ Does it need to run BEFORE schema changes?                              │
│ (Backup data from field that will be deleted)                           │
│   └─► USE PATCH with [pre_model_sync]                                   │
│                                                                         │
│ Does it need to run AFTER schema changes?                               │
│ (Populate newly added field with calculated values)                     │
│   └─► USE PATCH with [post_model_sync]                                  │
│                                                                         │
│ Is it master data / lookup tables?                                      │
│ (Categories, Status options, Configuration records)                     │
│   └─► USE FIXTURE for initial, PATCH for updates                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

> **See**: `references/decision-tree.md` for patch timing flowchart.

---

## Decision 4: Module Organization

```
┌─────────────────────────────────────────────────────────────────────────┐
│ HOW MANY MODULES DO YOU NEED?                                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ Small app (1-5 DocTypes, single purpose)?                               │
│   └─► ONE MODULE with app name                                          │
│       Example: my_app/my_app/ (module "My App")                         │
│                                                                         │
│ Medium app (6-15 DocTypes, multiple areas)?                             │
│   └─► 2-4 MODULES by functional area                                    │
│       Example: core/, settings/, integrations/                          │
│                                                                         │
│ Large app (15+ DocTypes, complex domain)?                               │
│   └─► MODULES by business domain                                        │
│       Example: inventory/, sales/, purchasing/, settings/               │
│                                                                         │
│ Multi-tenant or vertical solution?                                      │
│   └─► Consider MULTIPLE APPS instead                                    │
│       Base app + vertical-specific apps                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Rule**: Each DocType belongs to EXACTLY one module. Choose module = where would a user look for this DocType?

---

## Quick Implementation Workflows

### New App Workflow

```
1. Create app structure    → bench new-app my_app
2. Configure pyproject     → Edit pyproject.toml (v15+) or setup.py (v14)
3. Define modules          → Edit modules.txt
4. Create DocTypes         → bench --site mysite new-doctype MyDocType
5. Write controllers       → my_app/doctype/my_doctype/my_doctype.py
6. Configure hooks         → hooks.py for integration
7. Export fixtures         → bench --site mysite export-fixtures
8. Test installation       → bench --site testsite install-app my_app
```

> **See**: `references/workflows.md` for detailed steps.

### Patch Workflow

```
1. Plan the migration      → What data moves where?
2. Choose timing           → [pre_model_sync] or [post_model_sync]
3. Write patch file        → myapp/patches/v1_0/description.py
4. Add to patches.txt      → Under correct section
5. Test locally            → bench --site testsite migrate
6. Handle errors           → Add rollback logic if needed
7. Test on copy of prod    → ALWAYS before production
```

> **See**: `references/workflows.md` for patch patterns.

### Fixture Workflow

```
1. Configure hooks.py      → Define fixtures list with filters
2. Make changes via UI     → Custom Fields, Property Setters, etc.
3. Export fixtures         → bench --site mysite export-fixtures --app my_app
4. Verify JSON files       → Check my_app/fixtures/*.json
5. Commit to version control
6. Test import             → bench --site newsite migrate
```

> **See**: `references/workflows.md` for fixture strategies.

---

## Version-Specific Considerations

| Aspect | v14 | v15 | v16 |
|--------|-----|-----|-----|
| Build config | setup.py | pyproject.toml | pyproject.toml |
| DocType extension | doc_events | doc_events | `extend_doctype_class` preferred |
| Python minimum | 3.10 | 3.10 | 3.11 |
| INI patches | ✅ | ✅ | ✅ |
| Fixtures format | JSON | JSON | JSON |

### v16 Breaking Changes

- **`extend_doctype_class`** hook: Cleaner DocType extension pattern
- **Data masking**: Field-level privacy configuration available
- **UUID naming**: New naming rule option for DocTypes
- **Chrome PDF**: wkhtmltopdf deprecated for PDF generation

---

## Critical Implementation Rules

### ✅ ALWAYS

1. **Start with `bench new-app`** - Never create structure manually
2. **Define `__version__` in `__init__.py`** - Build will fail without it
3. **Test patches on database copy** - Never run untested patches on production
4. **Use batch processing** - Any patch touching 1000+ records needs batching
5. **Filter fixtures** - Never export all records of a DocType
6. **Version your patches** - Use v1_0, v2_0 directories for organization

### ❌ NEVER

1. **Put frappe/erpnext in pyproject dependencies** - They're not on PyPI
2. **Include transactional data in fixtures** - Only configuration!
3. **Hardcode site-specific values** - Use hooks or settings DocTypes
4. **Skip `frappe.db.commit()` in large patches** - Memory will explode
5. **Delete fields without backup patch** - Data loss is irreversible
6. **Modify core ERPNext files** - Always use hooks or override patterns

---

## Reference Files

| File | Contents |
|------|----------|
| `references/decision-tree.md` | Complete decision flowcharts |
| `references/workflows.md` | Step-by-step implementation guides |
| `references/examples.md` | Complete working examples |
| `references/anti-patterns.md` | Common mistakes to avoid |

---

## See Also

- `erpnext-syntax-customapp` - Exact syntax reference
- `erpnext-syntax-hooks` - Hooks configuration
- `erpnext-impl-hooks` - Hook implementation patterns
- `erpnext-database` - Database operations for patches
