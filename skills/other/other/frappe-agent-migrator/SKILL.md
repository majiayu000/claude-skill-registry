---
name: frappe-agent-migrator
description: >
  Use when migrating a Frappe app between major versions, detecting breaking API changes, or resolving post-migration errors.
  Prevents failed migrations from undetected deprecated APIs, removed methods, and changed function signatures.
  Covers breaking change detection v14-v15-v16, deprecated API mapping, migration checklist, common migration errors, automatic fix suggestions.
  Keywords: migration, version upgrade, breaking changes, deprecated API, v14, v15, v16, migrate, compatibility.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Version Migration Assistant

Systematically plans and executes Frappe/ERPNext version migrations by analyzing breaking changes, scanning custom code for compatibility issues, and generating migration plans.

**Purpose**: Prevent failed migrations by detecting every breaking change BEFORE upgrading.

## When to Use This Agent

```
MIGRATION TRIGGER
|
+-- Planning a version upgrade
|   "We need to go from v14 to v15"
|   --> USE THIS AGENT
|
+-- Post-upgrade errors
|   "Everything broke after bench update"
|   --> USE THIS AGENT (Step 2-5 for diagnosis)
|
+-- Checking custom app compatibility
|   "Will our custom app work on v16?"
|   --> USE THIS AGENT (Step 3 for code scan)
|
+-- Already mid-migration with issues
|   "bench migrate fails with errors"
|   --> USE THIS AGENT + frappe-agent-debugger
```

## Migration Workflow

```
STEP 1: IDENTIFY MIGRATION PATH
  Source version → Target version (NEVER skip major versions)

STEP 2: CHECK BREAKING CHANGES
  Apply breaking changes database for each version jump

STEP 3: SCAN CUSTOM CODE
  Grep for deprecated patterns in all custom apps

STEP 4: GENERATE MIGRATION PLAN
  Backup → Staging → Test → Production sequence

STEP 5: GENERATE PATCH LIST
  Specific code changes needed per custom app
```

See [references/workflow.md](references/workflow.md) for detailed steps.

## Step 1: Migration Path Rules

NEVER skip major versions. ALWAYS migrate sequentially:

| Source | Target | Path |
|--------|--------|------|
| v14 | v15 | v14 → v15 |
| v14 | v16 | v14 → v15 → v16 |
| v15 | v16 | v15 → v16 |

### Version Identification
```bash
# Check current versions
bench version
# Output shows: frappe X.Y.Z, erpnext X.Y.Z

# Check available versions
cd apps/frappe && git tag | grep "^v1[456]" | tail -5
```

## Step 2: Breaking Changes Summary

### v14 → v15 Breaking Changes

| Category | Change | Impact | Detection Pattern |
|----------|--------|--------|-------------------|
| Scheduler | Tick interval 240s → 60s | Jobs may run more frequently | Review `scheduler_events` |
| Background Jobs | `job_id` deduplication added | Duplicate jobs now prevented | Check `frappe.enqueue()` calls |
| Web Views | Workspace replaces Module Def pages | Custom module pages break | Grep for `Module Def` references |
| Print Format | HTML to PDF engine changes | Print layout differences | Test all print formats |
| Database | MariaDB 10.6+ required | Server prerequisite | Check `mysql --version` |
| Python | Python 3.10+ required | Syntax/library compatibility | Check `python3 --version` |
| API | `frappe.client.get_list` signature change | Custom API calls may fail | Grep for `frappe.client.get_list` |
| Permissions | Stricter permission checks on API | Guest access may break | Check `allow_guest=True` usage |
| Assets | New frontend build system | Custom JS bundles may break | Test `bench build` |
| Hooks | `boot_session` hook changes | Custom boot data may fail | Grep for `boot_session` |
| Naming | Some naming series changes | Document names may differ | Review `autoname` settings |
| Report | Report Builder changes | Custom reports may need updates | Test all Script Reports |

### v15 → v16 Breaking Changes

| Category | Change | Impact | Detection Pattern |
|----------|--------|--------|-------------------|
| DocType Extension | `extend_doctype_class` replaces `doc_events` override | Controller overrides need refactoring | Grep for `doc_events` with method override |
| Type Annotations | Type hints now best practice | Code style change | Not breaking, but recommended |
| Chrome PDF | New PDF engine (Chrome-based) | Print format rendering changes | Test all print formats |
| Data Masking | New privacy feature | PII fields need configuration | Review sensitive fields |
| UUID Naming | New `uuid` naming rule | Naming logic changes | Check `autoname` settings |
| Python | Python 3.11+ required | Library compatibility | Check `python3 --version` |
| Node.js | Node 18+ required | Build system prerequisite | Check `node --version` |
| Redis | Redis 7+ required | Cache/queue compatibility | Check `redis-server --version` |
| Deprecated APIs | Several APIs removed | Code using removed APIs fails | See breaking-changes.md |
| Workflow | Workflow engine updates | Custom workflow states may need review | Test all workflows |
| Portal | Portal page rendering changes | Custom portal pages may break | Test all portal pages |
| Background Jobs | RQ version upgrade | Job serialization changes | Test background jobs |

See [references/breaking-changes.md](references/breaking-changes.md) for complete details.

## Step 3: Deprecated Pattern Detection

ALWAYS scan custom app code for these patterns:

### v14 → v15 Deprecated Patterns

```bash
# Run these grep commands in apps/{your_app}/ directory:

# 1. Old-style module page references
grep -rn "Module Def" --include="*.py" --include="*.json"

# 2. Old scheduler API
grep -rn "frappe.utils.scheduler" --include="*.py"

# 3. Deprecated client API
grep -rn "frappe.set_route\|cur_page\|page_container" --include="*.js"

# 4. Old-style print format
grep -rn "frappe.get_print\|standard_format" --include="*.py"

# 5. Deprecated database methods
grep -rn "frappe.db.sql_list\|frappe.db.sql_ddl" --include="*.py"
```

### v15 → v16 Deprecated Patterns

```bash
# Run these grep commands in apps/{your_app}/ directory:

# 1. doc_events that should use extend_doctype_class
grep -rn "doc_events" hooks.py

# 2. Old-style controller override
grep -rn "override_doctype_class" --include="*.py"

# 3. Deprecated frappe.utils methods
grep -rn "frappe.utils.now_datetime\b" --include="*.py"

# 4. Old print format API
grep -rn "frappe.utils.pdf\|get_pdf" --include="*.py"

# 5. Removed API calls
grep -rn "frappe.get_hooks\b.*boot_session" --include="*.py"

# 6. Missing type annotations (warning, not error)
grep -rn "def .*whitelist" --include="*.py"
```

## Step 4: Migration Plan Template

ALWAYS generate a migration plan in this format:

```markdown
## Migration Plan: v{source} → v{target}

### Prerequisites
- [ ] Python version: {required}
- [ ] Node.js version: {required}
- [ ] MariaDB version: {required}
- [ ] Redis version: {required}
- [ ] Disk space: minimum 2x current DB size

### Phase 1: Preparation (Day 1)
1. Full backup: `bench --site {site} backup --with-files`
2. Document current state: `bench version > pre-migration-versions.txt`
3. List all custom apps: `bench --site {site} list-apps`
4. Run deprecated pattern scan (Step 3)
5. Fix all detected issues in custom apps

### Phase 2: Staging (Day 2-3)
1. Clone production to staging environment
2. Restore backup on staging: `bench --site staging restore {backup}`
3. Switch branch: `bench switch-to-branch version-{target} frappe erpnext`
4. Run migration: `bench --site staging migrate`
5. Run full test suite on staging

### Phase 3: Testing (Day 4-5)
- [ ] All DocTypes load correctly
- [ ] All print formats render correctly
- [ ] All workflows transition correctly
- [ ] All scheduled jobs execute correctly
- [ ] All custom reports generate correctly
- [ ] All API endpoints respond correctly
- [ ] All user permissions work correctly
- [ ] Performance is acceptable (page load < 3s)

### Phase 4: Production (Day 6)
1. Schedule maintenance window
2. Enable maintenance mode: `bench --site {site} set-maintenance-mode on`
3. Final backup: `bench --site {site} backup --with-files`
4. Switch branch: `bench switch-to-branch version-{target} frappe erpnext`
5. Run migration: `bench --site {site} migrate`
6. Run `bench build --production`
7. Restart: `bench restart` (or `sudo supervisorctl restart all`)
8. Disable maintenance mode: `bench --site {site} set-maintenance-mode off`
9. Verify (Phase 3 checklist again)

### Rollback Plan
1. Stop all services: `sudo supervisorctl stop all`
2. Restore backup: `bench --site {site} restore {backup_path}`
3. Switch back: `bench switch-to-branch version-{source} frappe erpnext`
4. Run migration: `bench --site {site} migrate`
5. Rebuild: `bench build --production`
6. Restart: `sudo supervisorctl restart all`
```

## Step 5: Custom App Patch List

For each deprecated pattern found in Step 3, generate a specific fix:

| File | Line | Current Code | Required Change | Breaking? |
|------|------|-------------|-----------------|-----------|
| `{file}` | `{line}` | `{old_pattern}` | `{new_pattern}` | Yes/No |

### Common Patches (v14 → v15)

| Pattern | Replace With |
|---------|-------------|
| `frappe.db.sql_list(...)` | `frappe.db.get_all(..., pluck="name")` |
| `Module Def` page references | Workspace configuration |
| `cur_page` JS references | `frappe.router` API |
| Old scheduler tick assumptions | Review timing for 60s interval |

### Common Patches (v15 → v16)

| Pattern | Replace With |
|---------|-------------|
| `doc_events` controller override | `extend_doctype_class` in hooks.py |
| Missing `super()` in overrides | Add `super().method()` call |
| `frappe.utils.pdf.get_pdf()` | Updated PDF API |
| No type annotations | Add type hints to public methods |

## Agent Output Format

ALWAYS produce migration output in this format:

```markdown
## Migration Assessment

### Version Path
{source} → {target} (via {intermediate versions if any})

### Prerequisites Status
| Requirement | Current | Required | Status |
|-------------|---------|----------|--------|
| Python | {ver} | {ver} | OK/FAIL |
| Node.js | {ver} | {ver} | OK/FAIL |
| MariaDB | {ver} | {ver} | OK/FAIL |

### Breaking Changes Found: {count}
[List from Step 2]

### Custom Code Issues Found: {count}
[Table from Step 3 scan]

### Migration Plan
[From Step 4]

### Patch List
[From Step 5]

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|

### Estimated Timeline
Preparation: {days} | Staging: {days} | Testing: {days} | Production: {hours}

### Referenced Skills
- `frappe-ops-upgrades`: Version upgrade procedures
- `frappe-ops-backup`: Backup and restore
- `frappe-agent-debugger`: For post-migration error diagnosis
```

See [references/checklists.md](references/checklists.md) for complete migration checklists.
See [references/breaking-changes.md](references/breaking-changes.md) for full breaking changes database.
