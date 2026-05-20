---
name: frappe-agent-validator
description: >
  Use when reviewing or validating Frappe/ERPNext code against best
  practices and common pitfalls. Checks generated code before deployment,
  validates against all 60 frappe-* skills, catches v16 patterns
  (extend_doctype_class, type annotations), validates ops patterns (bench
  commands, deployment), and generates correction reports. Keywords: review
  code, check script, validate deployment, find bugs, code quality.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Code Validator Agent

Validates Frappe/ERPNext code against the complete 60-skill knowledge base, catching errors BEFORE deployment.

**Purpose**: Catch errors before deployment, not after

## When to Use This Agent

```
CODE VALIDATION TRIGGERS
|
+-- Code has been generated and needs review
|   "Check this Server Script before I save it"
|   --> USE THIS AGENT
|
+-- Code is causing errors
|   "Why isn't this working?"
|   --> USE THIS AGENT
|
+-- Pre-deployment validation
|   "Is this production-ready?"
|   --> USE THIS AGENT
|
+-- Code review for best practices
|   "Can this be improved?"
|   --> USE THIS AGENT
|
+-- Ops/deployment validation
|   "Is my bench setup correct?"
|   --> USE THIS AGENT
```

## Validation Workflow

```
STEP 1: IDENTIFY CODE TYPE
  Client Script | Server Script | Controller | hooks.py |
  Jinja | Whitelisted | Bench/Ops | DocType JSON

STEP 2: RUN TYPE-SPECIFIC CHECKS
  Apply checklist for identified code type

STEP 3: CHECK UNIVERSAL RULES
  Error handling | Security | Performance | User feedback

STEP 4: VERIFY VERSION COMPATIBILITY
  v14/v15/v16 features | Deprecated patterns

STEP 5: VALIDATE AGAINST SKILL CATALOG
  Cross-reference with relevant frappe-* skills

STEP 6: GENERATE VALIDATION REPORT
  Critical errors | Warnings | Suggestions | Corrected code
```

See [references/workflow.md](references/workflow.md) for detailed steps.

## Critical Checks by Code Type

### Server Script Checks

| Check | Severity | Pattern | Fix |
|-------|----------|---------|-----|
| Import statements | FATAL | `import X` or `from X import Y` | Use `frappe.utils.X()` directly |
| Wrong doc variable | FATAL | `self.field` or `document.field` | Use `doc.field` |
| Wrong event for purpose | ERROR | Validation code in on_update | Move to validate event |
| try/except blocks | WARNING | `try: ... except:` | Use `frappe.throw()` for validation |
| No null checks | WARNING | `doc.field.lower()` | Add `if doc.field:` guard |

### Client Script Checks

| Check | Severity | Pattern | Fix |
|-------|----------|---------|-----|
| Server-side API calls | FATAL | `frappe.db.get_value()` | Use `frappe.call()` |
| Missing async handling | FATAL | `let x = frappe.call()` | Use callback or async/await |
| No refresh after set_value | ERROR | `frm.set_value()` alone | Add `frm.refresh_field()` |
| Using cur_frm | WARNING | `cur_frm.doc.field` | Use `frm` parameter |
| No form state check | WARNING | Missing `__islocal`/`docstatus` | Add state guards |

### Controller Checks

| Check | Severity | Pattern | Fix |
|-------|----------|---------|-----|
| self.* in on_update | FATAL | `self.field = X` in on_update | Use `self.db_set()` |
| Circular save | FATAL | `self.save()` in lifecycle hook | Remove self.save() |
| Missing super() | ERROR | Override without super() | Add `super().method()` |
| v16 extend_doctype_class | ERROR | Missing super() in mixin | ALWAYS call super() first |
| No type annotations | SUGGESTION | Missing type hints (v16) | Add type annotations |

### hooks.py Checks

| Check | Severity | Pattern | Fix |
|-------|----------|---------|-----|
| Invalid Python syntax | FATAL | Syntax errors | Fix dict/list structure |
| Wrong event names | FATAL | Typo in event name | Use correct event names |
| Invalid function paths | FATAL | Wrong dotted path | Verify path exists |
| v16-only hooks on v14/v15 | ERROR | `extend_doctype_class` | Use `doc_events` instead |
| Missing required_apps | WARNING | No dependency declaration | Add all dependencies |

### Ops/Bench Checks

| Check | Severity | Pattern | Fix |
|-------|----------|---------|-----|
| No migrate after hooks | FATAL | hooks.py changed, no migrate | Run `bench migrate` |
| Wrong bench command syntax | ERROR | Incorrect CLI args | Check `frappe-ops-bench` |
| Missing backup before upgrade | ERROR | Upgrade without backup | ALWAYS backup first |
| Production without supervisor | WARNING | No process manager | Use supervisor/systemd |
| No SSL in production | WARNING | HTTP-only deployment | Configure SSL/TLS |

### DocType JSON Checks

| Check | Severity | Pattern | Fix |
|-------|----------|---------|-----|
| Missing mandatory fields | ERROR | No primary identifier | Add name or autoname |
| Duplicate fieldnames | FATAL | Same fieldname twice | Use unique fieldnames |
| Wrong fieldtype for data | WARNING | Text for short values | Use Data/Small Text |
| No permissions defined | WARNING | Empty permission list | Add role permissions |

## v16 Specific Validations

### extend_doctype_class Pattern
```python
# VALIDATE: Mixin class MUST call super()
class CustomSalesInvoice(SalesInvoice):
    def validate(self):
        super().validate()       # REQUIRED - never skip
        self.custom_validation()

    def on_submit(self):
        super().on_submit()      # REQUIRED - never skip
        self.custom_on_submit()
```

### Type Annotations (v16 best practice)
```python
# v16 recommended pattern
def get_customer_balance(customer: str) -> float:
    ...

# Validate: type hints on public API methods
@frappe.whitelist()
def process_order(order_name: str, action: str = "approve") -> dict:
    ...
```

### Data Masking (v16)
```python
# Validate: sensitive fields should use data masking
# Check if PII fields have mask_with configured in DocType JSON
```

## Universal Validation Rules

### Security Checks (ALL code types)

| Check | Severity | Description |
|-------|----------|-------------|
| SQL Injection | CRITICAL | Raw user input in SQL |
| Permission bypass | CRITICAL | Missing permission checks |
| XSS vulnerability | HIGH | Unescaped user input in HTML |
| Sensitive data exposure | HIGH | Logging passwords/tokens |
| Hardcoded credentials | CRITICAL | API keys in source code |

### Performance Checks (ALL code types)

| Check | Severity | Description |
|-------|----------|-------------|
| Query in loop | HIGH | `frappe.db.*` inside for loop |
| Unbounded query | MEDIUM | SELECT without LIMIT |
| Unnecessary get_doc | LOW | get_doc when get_value suffices |
| Missing index | MEDIUM | Filter on non-indexed field |
| No batch commit | HIGH | Commit per record in bulk ops |

### Error Handling Checks (ALL code types)

| Check | Severity | Description |
|-------|----------|-------------|
| Silent failures | HIGH | `except: pass` without logging |
| Missing user feedback | MEDIUM | Errors not shown to user |
| Generic error messages | LOW | "An error occurred" |
| No rollback on failure | HIGH | Partial data on error |

## Validation Report Format

ALWAYS generate reports in this format:

```markdown
## Code Validation Report

### Code Type: [type]
### Target: [DocType / App / File]
### Event/Trigger: [if applicable]

### CRITICAL ERRORS (Must Fix)
| # | Line | Issue | Fix |
|---|------|-------|-----|

### WARNINGS (Should Fix)
| # | Line | Issue | Recommendation |
|---|------|-------|----------------|

### SUGGESTIONS (Nice to Have)
| # | Line | Suggestion |
|---|------|------------|

### Corrected Code
[If critical errors found, provide corrected version]

### Version Compatibility
| Version | Status | Notes |
|---------|--------|-------|
| v14 | [status] | |
| v15 | [status] | |
| v16 | [status] | |

### Referenced Skills
- frappe-skill-name: [what was validated against]
```

## Validation Depth Levels

| Level | Checks | Use When |
|-------|--------|----------|
| Quick | Fatal errors only | Initial scan |
| Standard | + Warnings + Security | Pre-deployment (DEFAULT) |
| Deep | + Suggestions + Performance + Ops | Production review |

## Skill Catalog Cross-Reference

This validator validates against ALL 60 frappe-* skills:

### Syntax Validation (11 skills)
`frappe-syntax-clientscripts`, `frappe-syntax-serverscripts`, `frappe-syntax-controllers`, `frappe-syntax-hooks`, `frappe-syntax-hooks-events`, `frappe-syntax-whitelisted`, `frappe-syntax-jinja`, `frappe-syntax-scheduler`, `frappe-syntax-customapp`, `frappe-syntax-doctypes`, `frappe-syntax-reports`

### Implementation Validation (12 skills)
`frappe-impl-clientscripts`, `frappe-impl-serverscripts`, `frappe-impl-controllers`, `frappe-impl-hooks`, `frappe-impl-whitelisted`, `frappe-impl-jinja`, `frappe-impl-scheduler`, `frappe-impl-customapp`, `frappe-impl-reports`, `frappe-impl-workflow`, `frappe-impl-website`, `frappe-impl-ui-components`, `frappe-impl-integrations`

### Error Pattern Validation (7 skills)
`frappe-errors-clientscripts`, `frappe-errors-serverscripts`, `frappe-errors-controllers`, `frappe-errors-hooks`, `frappe-errors-api`, `frappe-errors-permissions`, `frappe-errors-database`

### Core Pattern Validation (7 skills)
`frappe-core-database`, `frappe-core-permissions`, `frappe-core-api`, `frappe-core-workflow`, `frappe-core-notifications`, `frappe-core-files`, `frappe-core-cache`

### Ops Validation (8 skills)
`frappe-ops-bench`, `frappe-ops-deployment`, `frappe-ops-backup`, `frappe-ops-performance`, `frappe-ops-upgrades`, `frappe-ops-cloud`, `frappe-ops-app-lifecycle`, `frappe-ops-frontend-build`

### Testing Validation (2 skills)
`frappe-testing-unit`, `frappe-testing-cicd`

## Quick Validation Commands

### Server Script: 5-point check
1. Any `import` statements? --> FATAL
2. Any `self.` references? --> FATAL (use `doc.`)
3. Any `try/except`? --> WARNING (usually wrong)
4. Uses `frappe.throw()` for validation? --> GOOD
5. Uses `doc.field` for access? --> GOOD

### Client Script: 5-point check
1. Any `frappe.db.*` calls? --> FATAL
2. Any `frappe.get_doc()` calls? --> FATAL
3. `frappe.call()` without callback? --> FATAL
4. Uses `frm.doc.field` for access? --> GOOD
5. Uses `frm.refresh_field()` after changes? --> GOOD

### Controller: 5-point check
1. Modifying `self.*` in `on_update`? --> FATAL
2. Missing `super().method()` calls? --> ERROR
3. `self.save()` in lifecycle hook? --> FATAL
4. Imports at top of file? --> GOOD
5. Error handling for external calls? --> GOOD

### hooks.py: 5-point check
1. Valid Python syntax? --> Check
2. Function paths exist? --> Check
3. v16-only hooks marked? --> Check
4. required_apps complete? --> Check
5. Fixture filters present? --> Check

### Bench/Ops: 5-point check
1. `bench migrate` after changes? --> REQUIRED
2. Backup before destructive ops? --> REQUIRED
3. Scheduler enabled? --> Check
4. Workers running? --> Check
5. SSL configured (production)? --> Check

See [references/checklists.md](references/checklists.md) for complete checklists.
See [references/examples.md](references/examples.md) for validation examples.
