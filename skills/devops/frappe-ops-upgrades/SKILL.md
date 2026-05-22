---
name: frappe-ops-upgrades
description: >
  Use when upgrading Frappe/ERPNext between major versions (v14 to v15, v15 to v16), troubleshooting failed migrations, or planning rollback.
  Prevents broken upgrades from skipped patches, incompatible customizations, and missing pre-upgrade checks.
  Covers version upgrade paths, bench update, migrate command, patch troubleshooting, rollback procedures, breaking changes per version.
  Keywords: upgrade, migration, v14, v15, v16, bench update, bench migrate, rollback, patches, breaking changes.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Version Upgrades

Complete guide for upgrading Frappe/ERPNext between major versions, handling failed migrations, and rolling back safely.

**Versions**: v14 → v15 → v16

---

## Quick Reference — Upgrade Commands

| Task | Command |
|------|---------|
| Full update | `bench update` |
| Update specific app | `bench update --pull --app erpnext` |
| Switch branch | `bench switch-to-branch version-15 frappe erpnext` |
| Run migrations only | `bench --site mysite migrate` |
| Check migration readiness | `bench --site mysite ready-for-migration` |
| Backup before upgrade | `bench --site mysite backup` |
| Restore from backup | `bench --site mysite restore /path/to/backup.sql.gz` |
| Re-run failed patch | Add `#YYYY-MM-DD` suffix in patches.txt |

---

## Decision Tree: Upgrade Strategy

```
Need to upgrade?
├── Single minor version bump (e.g., v15.10 → v15.20)?
│   └── YES → Run `bench update` directly
├── Major version jump (e.g., v14 → v15)?
│   ├── Have custom apps?
│   │   ├── YES → Test on staging FIRST, check breaking changes
│   │   └── NO → Follow standard upgrade path
│   └── Multiple major versions (v14 → v16)?
│       └── ALWAYS upgrade one version at a time: v14 → v15 → v16
└── Production environment?
    ├── YES → ALWAYS test on staging clone first
    └── NO → Proceed with standard upgrade
```

---

## Pre-Upgrade Checklist

**ALWAYS** complete these steps before ANY major version upgrade:

1. **Full backup** — `bench --site mysite backup --with-files`
2. **Test on staging** — Clone production to a staging bench and test there first
3. **Check breaking changes** — Review the breaking changes section below
4. **Audit custom apps** — Run custom apps against new version's API changes
5. **Check Python/Node versions** — v15 requires Node 18+; v16 requires Node 24+, Python 3.14+
6. **Disable scheduler** — `bench --site mysite scheduler disable`
7. **Check pending jobs** — `bench --site mysite ready-for-migration`
8. **Read release notes** — Check GitHub release notes for each version

---

## Standard Upgrade Process

### Step-by-Step

```bash
# 1. Backup all sites
bench backup-all-sites

# 2. Switch to target version branch
bench switch-to-branch version-15 frappe erpnext

# 3. Update (pulls code, installs deps, builds, migrates)
bench update

# 4. Verify
bench --site mysite migrate  # if not done by update
bench version                # confirm versions
```

### What `bench update` Executes (In Order)

1. Backup all sites
2. Pull latest code for all apps (`git pull`)
3. Install Python requirements (`pip install`)
4. Install Node requirements (`yarn install`)
5. Build static assets (`bench build`)
6. Run migrations on all sites (`bench migrate`)
7. Restart bench processes

---

## v14 → v15 Breaking Changes

### Environment Requirements

| Requirement | v14 | v15 |
|-------------|-----|-----|
| Node.js | v14+ | **v18+** |
| Python packaging | setup.py | **pyproject.toml** |

### Backend Breaking Changes

- **`db.set()` removed** — Use `doc.db_set()` instead
- **`db.sql()` parameters removed** — `as_utf8` and `formatted` no longer accepted
- **`db.set_value()` for Singles** — Use `frappe.db.set_single_value()` instead
- **`job_name` deprecated** — Use `job_id` parameter in `enqueue()`
- **`frappe.new_doc()` arguments** — `parent_doc`, `parentfield`, `as_dict` MUST be keyword args
- **`frappe.get_installed_apps()`** — No longer accepts `sort` or `frappe_last` args
- **Method override order reversed** — Last override now takes precedence
- **Timezone functions renamed** — `convert_utc_to_user_timezone` → `convert_utc_to_system_timezone`

### Frontend Breaking Changes

- **Vue 2 → Vue 3** — All Vue components MUST be migrated
- **Window globals removed** — `get_today` → `frappe.datetime.get_today`, `user` → `frappe.session.user`
- **`this` in Client Scripts** — Local scope access no longer supported
- **Image lazy loading** — Replace `website-image-lazy` class with native `loading="lazy"`

### Security Changes

- **Server Scripts disabled by default** — Enable: `bench set-config -g server_script_enabled 1`
- **"Desk User" role added** — Replaces "All" role for desk user permissions
- **`currentsite.txt` removed** — Use `bench use sitename` or `FRAPPE_SITE` env var

### Removed Features

- Event Streaming moved to separate app
- Cordova support removed
- `setup.py` removed (use `pyproject.toml`)
- `--make_copy` and `--restore` build flags removed (use `--hard-link`)

See [breaking-changes.md](references/breaking-changes.md) for the complete list.

---

## v15 → v16 Breaking Changes

### Environment Requirements

| Requirement | v15 | v16 |
|-------------|-----|-----|
| Node.js | v18+ | **v24+** |
| Python | 3.10+ | **3.14+** |

### Backend Breaking Changes

- **Default sort order changed** — `creation` instead of `modified` for all list queries
- **`has_permission` hooks** — MUST return explicit `True`; `None` no longer accepted
- **`frappe.get_doc(doctype, name, field=value)`** — No longer updates values
- **DB commits in document hooks** — No longer allowed to prevent data integrity issues
- **`frappe.sendmail(now=True)`** — No longer commits transactions implicitly
- **`db.get_value()` for Singles** — Now returns proper types instead of strings
- **State-changing methods require POST** — `/api/method/logout`, `/api/method/upload_file`, etc.

### Separated Modules (Install Separately)

- Energy Points → `frappe/eps`
- Newsletter → `frappe/newsletter`
- Backup Integrations → `frappe/offsite_backups`
- Blog → `frappe/blog`

### Frontend Breaking Changes

- Report/Dashboard/Page JS evaluated as IIFEs (no global scope pollution)
- Awesome Bar redesigned, moved to sidebar (`Cmd+K`)
- List view right sidebar removed
- `/apps` endpoint deprecated; `/app` reroutes to `/desk`

### Configuration Changes

- Site config cached for up to one minute (changes not immediate)
- Country field requires valid ISO 3166 ALPHA-2 code
- `bench version` output format changed to "plain" (use `-f legacy` for old format)
- `override_doctype` hook classes MUST inherit from the overridden class

See [breaking-changes.md](references/breaking-changes.md) for the complete list.

---

## Patch System

### How Patches Work

Patches are one-off data migration scripts that run during `bench migrate`. They are defined in each app's `patches.txt` file.

### patches.txt Format [v14+]

```ini
[pre_model_sync]
# Runs BEFORE schema sync — use for data prep
myapp.patches.v15_0.prepare_data_for_migration

[post_model_sync]
# Runs AFTER schema sync — use for data that needs new schema
myapp.patches.v15_0.migrate_data_to_new_fields
```

### Patch Execution Rules

- Patches run in the order defined in `patches.txt`
- Each patch runs exactly ONCE — tracked in the `__patches` table
- To re-run a patch, append a date comment: `myapp.patches.v15_0.fix #2025-03-20`
- One-off statements: `execute:frappe.delete_doc('Page', 'old_page', ignore_missing=True)`

### Writing a Patch

```python
# myapp/patches/v15_0/migrate_field_data.py
import frappe

def execute():
    # ALWAYS reload if you need the NEW schema
    frappe.reload_doc("module_name", "doctype", "doctype_name")

    # Perform data migration
    frappe.db.sql("""
        UPDATE `tabSales Invoice`
        SET new_field = old_field
        WHERE old_field IS NOT NULL
    """)
```

### Debugging Stuck Patches

```bash
# Check which patches have run
bench --site mysite console
>>> frappe.db.sql("SELECT * FROM __patches WHERE patch LIKE '%stuck_patch%'")

# Remove a patch record to force re-run
>>> frappe.db.sql("DELETE FROM __patches WHERE patch = 'myapp.patches.v15_0.broken_patch'")
>>> frappe.db.commit()

# Then re-run migrate
bench --site mysite migrate
```

---

## Rollback Procedure

### Immediate Rollback (Within Hours)

```bash
# 1. Stop all processes
bench stop

# 2. Restore database from pre-upgrade backup
bench --site mysite restore /path/to/pre-upgrade-backup.sql.gz \
  --with-public-files /path/to/files.tar \
  --with-private-files /path/to/private-files.tar

# 3. Switch back to previous version branch
bench switch-to-branch version-14 frappe erpnext

# 4. Install old dependencies
bench setup requirements

# 5. Build old assets
bench build

# 6. Start bench
bench start  # or: sudo bench restart (production)
```

### Critical Rules for Rollback

- **ALWAYS** keep pre-upgrade backups for at least 7 days
- **NEVER** run `bench migrate` after restoring to old branch — schema is already correct
- **ALWAYS** restore files alongside database — file references may break otherwise
- **NEVER** attempt rollback after users have created new data on the upgraded version

---

## Frappe Packages — Moving Customizations Between Sites

Frappe Packages (v14+) are lightweight UI-built applications — bundles of Custom Module Defs distributed as `.tar.gz` tarballs. For Custom Fields, Property Setters, and DocPerms on standard DocTypes, use **Fixtures** instead.

### Quick Reference — Package vs Fixtures vs App

| Mechanism | Use When | CLI Command |
|-----------|----------|-------------|
| **Package** | UI-built DocTypes, Scripts, Web Pages | UI only (Package Import/Release) |
| **Fixtures** | Custom Fields, Property Setters, DocPerms | `bench --site mysite export-fixtures` |
| **Frappe App** | Full development workflow, CI/CD, tests | `bench get-app`, `bench install-app` |

### Package Workflow (UI-Based)

1. Create a **Package** document → assign Custom Module Defs to it
2. Create a **Package Release** → exports to `[bench]/sites/[site]/packages/` as `[package]-[version].tar.gz`
3. On target site, create **Package Import** → attach tarball, check **Activate**
4. System migrates data like an app migration; use **Force** to overwrite existing files

### Fixtures Workflow (CLI-Based)

```python
# hooks.py — define what to export
fixtures = [
    "Custom Field",
    "Property Setter",
    {"dt": "Client Script", "filters": [["module", "=", "My Module"]]}
]
```

```bash
# Export fixtures to JSON in your app
bench --site mysite export-fixtures --app myapp

# Fixtures auto-sync on: bench --site mysite migrate
```

**NEVER** use Packages to modify standard/core DocTypes — use a Frappe App with Fixtures.

See [frappe-packages.md](references/frappe-packages.md) for the complete reference including decision trees, limitations, and best practices.

---

## Custom App Compatibility Checks

Before upgrading, audit each custom app:

1. **Check deprecated APIs** — Search for removed functions listed in breaking changes
2. **Check `setup.py`** — Must migrate to `pyproject.toml` for v15+
3. **Check Vue components** — Must be Vue 3 compatible for v15+
4. **Check `patches.txt`** — Ensure patches use `[pre_model_sync]`/`[post_model_sync]` sections [v14+]
5. **Check hooks.py** — Verify no removed hooks are used
6. **Run tests** — `bench --site test_site run-tests --app myapp`

---

## Decision Tree: In-Place vs Fresh Install

```
Choosing upgrade strategy:
├── Small site (< 10 GB database)?
│   └── In-place upgrade is usually fine
├── Large site (> 50 GB database)?
│   ├── Many custom apps? → Fresh install + data migration
│   └── Standard apps only? → In-place with extended downtime window
├── Skipping multiple versions (v13 → v15)?
│   └── ALWAYS fresh install — sequential upgrades are too risky
└── Critical production with zero-downtime requirement?
    └── Fresh install on parallel server + DNS switch
```

---

## Version Differences Summary

| Feature | v14 | v15 | v16 |
|---------|:---:|:---:|:---:|
| Python packaging | setup.py | pyproject.toml | pyproject.toml |
| Vue version | Vue 2 | **Vue 3** | Vue 3 |
| Node.js minimum | v14 | **v18** | **v24** |
| Python minimum | 3.8 | 3.10 | **3.14** |
| Server Scripts | Enabled | **Disabled default** | Disabled default |
| Default sort | modified | modified | **creation** |
| patches.txt sections | Yes | Yes | Yes |
| Workspace sidebar | No | No | **Yes** |
| Separated modules | — | Event Streaming | Blog, Newsletter, EPS |

---

## Reference Files

| File | Contents |
|------|----------|
| [examples.md](references/examples.md) | Complete upgrade workflow examples |
| [anti-patterns.md](references/anti-patterns.md) | Common upgrade mistakes and fixes |
| [breaking-changes.md](references/breaking-changes.md) | Detailed breaking changes per version |
| [frappe-packages.md](references/frappe-packages.md) | Packages, fixtures, and moving customizations between sites |
