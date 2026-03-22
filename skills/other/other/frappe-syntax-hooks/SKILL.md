---
name: frappe-syntax-hooks
description: >
  Use when configuring Frappe hooks.py for app events, scheduler tasks,
  document events, fixtures, boot session, jenv customization, or website
  routing. Covers v14/v15/v16 including extend_doctype_class. Keywords:
  hooks.py, doc_events, scheduler_events, fixtures, app_include_js,
  override_whitelisted_methods, extend_doctype_class.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Configuration Hooks (hooks.py)

Configuration hooks in hooks.py enable custom apps to extend Frappe/ERPNext
behavior. This skill covers ALL non-document-event hooks. For `doc_events`
(validate, on_submit, on_update, etc.), see **frappe-syntax-hooks-events**.

## Quick Reference — Hook Categories

| Category | Key Hooks | Reference |
|----------|-----------|-----------|
| App metadata | `app_name`, `app_title`, `required_apps` | Below |
| Frontend assets | `app_include_js/css`, `web_include_js/css` | Below |
| Install/migrate | `before_install`, `after_install`, `after_migrate` | Below |
| Scheduler | `hourly`, `daily`, `cron`, `*_long` | [scheduler-events.md](references/scheduler-events.md) |
| Session/auth | `on_login`, `on_logout`, `auth_hooks` | [bootinfo.md](references/bootinfo.md) |
| Request middleware | `before_request`, `after_request` | [request-lifecycle.md](references/request-lifecycle.md) |
| Permissions | `permission_query_conditions`, `has_permission` | [permissions.md](references/permissions.md) |
| DocType overrides | `override_doctype_class`, `doctype_js` | [overrides.md](references/overrides.md) |
| Website/portal | `website_route_rules`, `portal_menu_items` | [request-lifecycle.md](references/request-lifecycle.md) |
| File handling | `before_write_file`, `write_file` | Below |
| Email | `override_email_send`, `default_mail_footer` | Below |
| PDF | `pdf_header_html`, `pdf_footer_html` | Below |
| Jinja | `jinja.methods`, `jinja.filters` | Below |
| Boot/client data | `extend_bootinfo`, `notification_config` | [bootinfo.md](references/bootinfo.md) |
| Data/fixtures | `fixtures`, `global_search_doctypes` | Below |
| Method overrides | `override_whitelisted_methods`, `standard_queries` | [overrides.md](references/overrides.md) |

---

## Decision Tree — Which Hook Do I Need?

```
What do you want to achieve?
|
+-- ADD JS/CSS to desk or portal?
|   +-- Desk --> app_include_js / app_include_css
|   +-- Portal --> web_include_js / web_include_css
|   +-- Specific form --> doctype_js
|   +-- List view --> doctype_list_js
|
+-- RUN periodic background tasks?
|   +-- < 5 min execution --> hourly / daily / weekly / monthly
|   +-- 5-25 min execution --> hourly_long / daily_long / etc.
|   +-- Exact time needed --> cron
|   See: frappe-syntax-hooks > scheduler-events.md
|
+-- SEND data to client at page load?
|   +-- extend_bootinfo
|
+-- MODIFY controller of existing DocType?
|   +-- v16+ --> extend_doctype_class (RECOMMENDED)
|   +-- v14/v15 --> override_doctype_class (last app wins)
|
+-- MODIFY API endpoint?
|   +-- override_whitelisted_methods
|
+-- CUSTOMIZE permissions?
|   +-- List filtering --> permission_query_conditions
|   +-- Document-level --> has_permission
|
+-- REACT to document save/submit/delete?
|   +-- See frappe-syntax-hooks-events skill
|
+-- EXPORT/IMPORT configuration?
|   +-- fixtures
|
+-- SETUP on install or migrate?
|   +-- after_install / after_migrate
|
+-- ADD custom Jinja functions?
|   +-- jinja.methods / jinja.filters
|
+-- CUSTOMIZE website routing?
|   +-- website_route_rules
|   See: request-lifecycle.md for full routing pipeline
|
+-- INTERCEPT every request/response?
|   +-- before_request / after_request
|   See: request-lifecycle.md for lifecycle flow
|
+-- CUSTOM page rendering?
|   +-- page_renderer hook
|   See: request-lifecycle.md for renderer architecture
```

---

## 1. App Metadata Hooks

ALWAYS include these in every hooks.py:

```python
app_name = "myapp"
app_title = "My App"
app_publisher = "My Company"
app_description = "Custom ERPNext extensions"
app_email = "info@mycompany.com"
app_license = "MIT"
required_apps = ["erpnext"]  # Declare dependencies
```

---

## 2. Frontend Asset Injection

```python
# Desk (backend UI) assets — loaded on EVERY desk page
app_include_js = "/assets/myapp/js/myapp.min.js"       # string or list
app_include_css = "/assets/myapp/css/myapp.min.css"

# Website/portal assets — loaded on EVERY web page
web_include_js = "/assets/myapp/js/web.min.js"
web_include_css = "/assets/myapp/css/web.min.css"

# Web form specific assets
webform_include_js = {"My Web Form": "public/js/my_webform.js"}
webform_include_css = {"My Web Form": "public/css/my_webform.css"}

# Form script extensions (extend OTHER apps' forms)
doctype_js = {"Sales Invoice": "public/js/sales_invoice.js"}

# List view script extensions
doctype_list_js = {"Sales Invoice": "public/js/sales_invoice_list.js"}

# Custom sounds
sounds = [{"name": "alert", "src": "/assets/myapp/sounds/alert.mp3", "volume": 0.5}]
```

NEVER put heavy libraries in `app_include_js` — they load on every page.

---

## 3. Installation & Migration Lifecycle

```python
before_install = "myapp.setup.before_install"
after_install = "myapp.setup.after_install"
after_sync = "myapp.setup.after_sync"            # After fixture sync
before_migrate = "myapp.setup.before_migrate"
after_migrate = "myapp.setup.after_migrate"
before_uninstall = "myapp.setup.before_uninstall"
after_uninstall = "myapp.setup.after_uninstall"
before_tests = "myapp.setup.seed_test_data"
```

All accept a single dotted-path string. The function receives no arguments.

---

## 4. Scheduler Events

See [scheduler-events.md](references/scheduler-events.md) for full reference.

```python
scheduler_events = {
    "all": ["myapp.tasks.every_minute"],            # ~60s interval
    "hourly": ["myapp.tasks.hourly_check"],         # default queue, 5 min timeout
    "daily": ["myapp.tasks.daily_report"],
    "weekly": ["myapp.tasks.weekly_cleanup"],
    "monthly": ["myapp.tasks.monthly_summary"],
    "daily_long": ["myapp.tasks.heavy_sync"],       # long queue, 25 min timeout
    "cron": {
        "0 9 * * 1-5": ["myapp.tasks.weekday_morning"]  # cron expression
    }
}
```

ALWAYS run `bench --site sitename migrate` after changing scheduler_events.
NEVER define task functions with arguments — they receive none.

---

## 5. Session & Authentication Hooks

```python
on_login = "myapp.auth.on_login"                     # Receives login_manager
on_logout = "myapp.auth.on_logout"                   # No arguments
on_session_creation = "myapp.auth.on_session_creation"  # No arguments
auth_hooks = ["myapp.auth.validate_request"]          # List of validators
```

Execution order: `on_login` --> session created --> `on_session_creation` --> `extend_bootinfo`.

---

## 6. Request/Response Middleware

See [request-lifecycle.md](references/request-lifecycle.md) for the full request
lifecycle flow, page renderer architecture, and router API.

```python
before_request = ["myapp.middleware.before_request"]   # List of dotted paths
after_request = ["myapp.middleware.after_request"]
before_job = ["myapp.middleware.before_job"]            # Before background job
after_job = ["myapp.middleware.after_job"]              # After background job
```

---

## 7. Permission Hooks

See [permissions.md](references/permissions.md) for full reference.

```python
permission_query_conditions = {
    "Sales Invoice": "myapp.permissions.si_query_conditions"
}
has_permission = {
    "Sales Invoice": "myapp.permissions.si_has_permission"
}
```

ALWAYS check `if not user: user = frappe.session.user` in handlers.
ALWAYS use `frappe.db.escape(user)` in SQL — NEVER string interpolation.
`permission_query_conditions` works ONLY with `get_list`, NOT `get_all`.

---

## 8. DocType Class Overrides

See [overrides.md](references/overrides.md) for full reference.

```python
# v14+ — Full replacement (LAST installed app wins)
override_doctype_class = {
    "Sales Invoice": "myapp.overrides.CustomSalesInvoice"
}

# v16+ — Mixin-based extension (ALL apps coexist) [RECOMMENDED]
extend_doctype_class = {
    "Address": ["myapp.extensions.AddressMixin"]
}
```

ALWAYS call `super().method()` in overrides. Forgetting super() breaks core logic.

---

## 9. Website & Portal Hooks

```python
# URL routing
website_route_rules = [
    {"from_route": "/custom-page/<name>", "to_route": "Custom Page"}
]
website_redirects = [
    {"source": "/old-url", "target": "/new-url"}
]
website_catch_all = "myapp.www.custom_404"

# Homepage
homepage = "my-custom-home"
role_home_page = {"Sales User": "sales-dashboard"}
get_website_user_home_page = "myapp.utils.get_home_page"

# Portal sidebar
portal_menu_items = [{"title": "My Orders", "route": "/orders", "role": "Customer"}]
standard_portal_menu_items = [{"title": "My Items", "route": "/my-items"}]

# Template overrides
base_template = "myapp/templates/base.html"
website_context = {"brand_html": "<b>My Brand</b>"}
update_website_context = "myapp.context.update_context"
```

---

## 10. File Handling Hooks

```python
before_write_file = "myapp.files.before_write"      # Pre-save hook
write_file = "myapp.files.custom_write"              # Replace file storage (e.g., S3/CDN)
delete_file_data_content = "myapp.files.custom_delete"  # Replace file deletion
```

Use `write_file` to redirect file storage to cloud providers (S3, GCS, Azure Blob).

---

## 11. Email Hooks

```python
override_email_send = "myapp.email.custom_send"       # Replace email backend
get_sender_details = "myapp.email.get_sender"          # Override From address
default_mail_footer = "myapp.email.get_footer"         # HTML footer for all emails
```

---

## 12. PDF Hooks

```python
pdf_header_html = "myapp.pdf.get_header"               # Custom PDF header
pdf_body_html = "myapp.pdf.get_body"                    # Custom PDF body wrapper
pdf_footer_html = "myapp.pdf.get_footer"                # Custom PDF footer
# pdf_generator = "myapp.pdf.generate"                  # [v16+] Replace PDF engine
```

---

## 13. Jinja Hooks

```python
# Add custom methods available in Jinja templates
jinja = {
    "methods": ["myapp.jinja_utils.get_balance"],
    "filters": ["myapp.jinja_utils.format_iban"]
}
```

```python
# myapp/jinja_utils.py
def get_balance(customer):
    """Usage in template: {{ get_balance(doc.customer) }}"""
    return frappe.db.get_value("Customer", customer, "outstanding_amount") or 0

def format_iban(value):
    """Usage in template: {{ bank_account|format_iban }}"""
    if not value: return ""
    return " ".join([value[i:i+4] for i in range(0, len(value), 4)])
```

---

## 14. Boot & Client Data

See [bootinfo.md](references/bootinfo.md) for full reference.

```python
extend_bootinfo = "myapp.boot.extend_boot"
notification_config = "myapp.notifications.get_config"
```

NEVER put secrets/API keys in bootinfo — it is sent to the browser.
NEVER run heavy queries in bootinfo — it runs on EVERY page load.

---

## 15. Data & Fixtures

```python
fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "My App"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "My App"]]},
    {"dt": "Role", "filters": [["name", "like", "MyApp%"]]}
]

global_search_doctypes = {"My DocType": {"index": 10}}
ignore_links_on_delete = ["Communication", "Activity Log"]
calendars = ["My Event DocType"]
clear_cache = "myapp.cache.clear_custom_cache"
```

ALWAYS use filters in fixtures — NEVER export unfiltered (exports everything).
NEVER put transactional data (Sales Invoice, Stock Entry) in fixtures.

---

## 16. Method Overrides

See [overrides.md](references/overrides.md) for full reference.

```python
override_whitelisted_methods = {
    "frappe.client.get_count": "myapp.overrides.custom_get_count"
}
standard_queries = {
    "Customer": "myapp.queries.customer_query"
}
```

ALWAYS match the original method signature exactly when overriding.

---

## Version Differences

| Hook | v14 | v15 | v16+ |
|------|-----|-----|------|
| `extend_doctype_class` | -- | -- | NEW |
| `extend_bootinfo` | Yes | Yes | Yes |
| `auth_hooks` | Yes | Yes | Yes |
| `after_sync` | Yes | Yes | Yes |
| `before_uninstall` | -- | Yes | Yes |
| `after_uninstall` | -- | Yes | Yes |
| `website_path_resolver` | -- | Yes | Yes |
| All other hooks | Yes | Yes | Yes |

---

## Critical Rules

1. ALWAYS run `bench --site sitename migrate` after ANY hooks.py change
2. NEVER import frappe at module level in hooks.py — it runs before init
3. ALWAYS use dotted paths (`"myapp.module.function"`) — NEVER lambdas
4. NEVER commit in hook handlers — Frappe manages transactions
5. ALWAYS test hooks in a dev environment before deploying

---

## Anti-Patterns Summary

| Wrong | Correct |
|-------|---------|
| No filters in fixtures | ALWAYS filter by module/app |
| Secrets in bootinfo | ONLY public config in bootinfo |
| Heavy queries in bootinfo | Cache or minimize data |
| `get_all` with permission hooks | Use `get_list` for permission filtering |
| Override without `super()` | ALWAYS call `super().method()` first |
| Scheduler tasks with args | Tasks receive NO arguments |
| Skip `bench migrate` | ALWAYS migrate after hook changes |

Full anti-patterns: [anti-patterns.md](references/anti-patterns.md)

---

## Reference Files

| File | Contents |
|------|----------|
| [hooks.md](references/hooks.md) | Complete hooks catalog by category |
| [scheduler-events.md](references/scheduler-events.md) | Scheduler frequencies, cron syntax, timeouts |
| [permissions.md](references/permissions.md) | Permission hooks in detail |
| [overrides.md](references/overrides.md) | DocType class override patterns |
| [bootinfo.md](references/bootinfo.md) | extend_bootinfo, session hooks, notification_config |
| [examples.md](references/examples.md) | Working hooks.py examples for each category |
| [request-lifecycle.md](references/request-lifecycle.md) | Request lifecycle, routing pipeline, page renderers, router API |
| [anti-patterns.md](references/anti-patterns.md) | Common hook mistakes and corrections |

For document lifecycle events (doc_events), see: **frappe-syntax-hooks-events**
