---
name: frappe-core-logging
description: >
  Use when implementing logging, error tracking, or monitoring in Frappe
  v14-v16. Covers frappe.logger() for file-based logging,
  frappe.log_error() for Error Log DocType entries, request logging,
  Sentry integration, and production logging patterns. Prevents common
  mistakes with print(), swapped log_error arguments, and sensitive data.
  Keywords: frappe.logger, log_error, Error Log, logging, Sentry,
  monitor, request logging, error tracking, debug, production.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "3.0"
---

# Frappe Logging & Error Tracking

## Three Logging Mechanisms

| Mechanism | Storage | Use For |
|-----------|---------|---------|
| `frappe.logger()` | File (rotating) | Application logging, debug info, audit trails |
| `frappe.log_error()` | Database (Error Log DocType) | Errors visible in admin UI, persistent tracking |
| `frappe.log()` / `frappe.errprint()` | stderr / request-scoped | Quick debugging only (NOT for production) |

---

## Decision Tree

```
Need to log something?
│
├─ Application logging (info, debug, warnings)?
│  └─ frappe.logger("my_module").info("message")
│     → Writes to sites/{site}/logs/my_module.log
│
├─ Error that admins should see in Desk UI?
│  └─ frappe.log_error(title="Short desc", message=traceback)
│     → Creates Error Log document (queryable, auto-cleanup)
│
├─ Quick debug during development?
│  └─ frappe.errprint(variable) — shows in console
│     → NEVER leave in production code
│
├─ Track all HTTP requests?
│  └─ Set enable_frappe_logger: true in site_config.json
│     → Logs to frappe.web.log
│
├─ Performance monitoring?
│  └─ Set monitor: true in site_config.json
│     → Logs to monitor.json.log (JSON, per-request metrics)
│
└─ External error tracking (Sentry)?
   └─ Set FRAPPE_SENTRY_DSN environment variable
      → Auto-captures unhandled exceptions
```

---

## Quick Reference — frappe.logger()

```python
# Get a logger for your module (ALWAYS specify module name)
logger = frappe.logger("my_app")

# Standard Python logging levels
logger.debug("Detailed diagnostic info")
logger.info("Normal operations: processed 50 records")
logger.warning("Something unexpected but recoverable")
logger.error("Operation failed", exc_info=True)
logger.critical("System-level failure")

# Full signature
frappe.logger(
    module=None,          # Logger name + log filename
    with_more_info=False, # Auto-log request form_dict
    allow_site=True,      # Log under site's logs/ directory
    filter=None,          # Custom logging.Filter
    max_size=100_000,     # Max bytes per log file (100KB default)
    file_count=20         # Rotated files retained (20 default)
)
```

**Log location:** `sites/{site}/logs/{module}.log`
**Rotation:** RotatingFileHandler — 100KB per file, 20 backups (~2MB total per logger)

### Default Log Levels

| Mode | Level | Effect |
|------|-------|--------|
| Development (`_dev_server`) | WARNING | Debug/info suppressed |
| Production | ERROR | Only errors and above |

```python
# Change level dynamically
frappe.utils.logger.set_log_level("DEBUG")
```

---

## Quick Reference — frappe.log_error()

```python
# ALWAYS use keyword arguments (title/message can swap otherwise)
frappe.log_error(
    title="Payment gateway timeout",          # Short description (140 chars max)
    message=frappe.get_traceback(),            # Full error details
    reference_doctype="Payment Entry",        # Related DocType
    reference_name="PE-00001"                 # Related document
)

# Minimal — auto-captures current traceback
try:
    risky_operation()
except Exception:
    frappe.log_error(title="Operation failed")
```

**Error Log cleanup:** Auto-deletes after 30 days. Manual: `frappe.whitelist: clear_error_logs()`

### Auto-Captured Exceptions

Unhandled exceptions (HTTP 500+) are automatically logged to Error Log.

**Excluded from auto-capture:**
- `frappe.AuthenticationError`
- `frappe.CSRFTokenError`
- `frappe.SecurityException`
- `frappe.InReadOnlyMode`

---

## Production Configuration

### site_config.json Keys

| Key | Value | Effect |
|-----|-------|--------|
| `enable_frappe_logger` | `true` | HTTP request logging → `frappe.web.log` |
| `logging` | `2` | Log all SQL queries (debug only!) |
| `monitor` | `true` | Request/job metrics → `monitor.json.log` |
| `disable_error_snapshot` | `true` | Disable auto-capture of exceptions |

### Environment Variables

| Variable | Effect |
|----------|--------|
| `FRAPPE_STREAM_LOGGING=1` | Log to stderr instead of files |
| `FRAPPE_SENTRY_DSN=<dsn>` | Enable Sentry error tracking |
| `ENABLE_SENTRY_DB_MONITORING` | Track SQL queries in Sentry |
| `SENTRY_TRACING_SAMPLE_RATE` | Performance tracing rate (0.0-1.0) |

### Production Log Files

| File | Content |
|------|---------|
| `logs/web.error.log` | HTTP errors (supervisor) |
| `logs/web.log` | Gunicorn stdout |
| `logs/worker.error.log` | Background job errors |
| `logs/frappe.log` | Default frappe logger |
| `logs/frappe.web.log` | HTTP request metadata |
| `logs/monitor.json.log` | Performance metrics (JSON) |
| `sites/{site}/logs/*.log` | Per-site application logs |

---

## Anti-Patterns

| NEVER | ALWAYS | Why |
|-------|--------|-----|
| `print("debug info")` | `frappe.logger("mod").info(...)` | print() disappears in production |
| `frappe.log_error("info msg")` | `frappe.logger().info(...)` | log_error creates Error Log docs, clutters admin UI |
| `frappe.logger()` (no module) | `frappe.logger("my_module")` | No-module mixes with framework logs |
| `frappe.log_error(title, msg)` positional | `frappe.log_error(title=t, message=m)` | Positional args can swap (known quirk) |
| Log passwords/tokens | Mask sensitive data | SiteContextFilter only masks form_dict |
| `frappe.log()` in production | `frappe.logger()` | frappe.log() is debug-only, request-scoped |
| Leave `logging=2` in prod | Only during debugging | Logs ALL SQL queries, massive I/O |

---

## Version Differences

| Feature | v14 | v15+ |
|---------|:---:|:----:|
| `frappe.logger()` | Yes | Yes |
| `frappe.log_error()` | Yes | + `defer_insert` kwarg |
| Error Log trace_id | -- | Added |
| Error Log metadata | -- | JSON request/job context |
| Error snapshots | File-based + scheduled collection | Direct DB insert |
| Sentry integration | Basic | Enhanced (DB monitoring, profiling) |
| `guess_exception_source()` | -- | Identifies which app caused error |
| `FRAPPE_STREAM_LOGGING` | Yes | Yes |

---

## Reference Files

- [Logger API & Patterns](references/logger-patterns.md) — frappe.logger() advanced usage
- [Error Tracking](references/error-tracking.md) — Error Log, Sentry, monitoring
