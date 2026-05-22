---
name: wp-plugin-development
description: "Use when developing WordPress plugins: architecture and hooks, activation/deactivation/uninstall, admin UI and Settings API, data storage, cron/tasks, security (nonces/capabilities/sanitization/escaping), and release packaging."
compatibility: "Targets WordPress 6.9+ (PHP 8.0+). Filesystem-based agent with bash + node."
---

# WP Plugin Development

## When to use

Use this skill for plugin work such as:

- creating or refactoring plugin structure (bootstrap, includes, namespaces/classes)
- adding hooks/actions/filters
- activation/deactivation/uninstall behavior and migrations
- adding settings pages / options / admin UI (Settings API)
- security fixes (nonces, capabilities, sanitization/escaping, SQL safety)
- packaging a release (build artifacts, readme, assets)

## Inputs required

- Repo root + target plugin(s) (path to plugin main file if known).
- Where this plugin runs: single site vs multisite; WP.com conventions if applicable.
- Target WordPress + PHP versions (affects available APIs).

## Procedure

### 0) Triage and locate plugin entrypoints

1. Identify the main plugin file (contains `Plugin Name:` header)
2. Check for existing structure (includes/, admin/, public/ directories)
3. Note any existing hooks or class patterns

### 1) Follow a predictable architecture

Guidelines:

- Keep a single bootstrap (main plugin file with header).
- Avoid heavy side effects at file load time; load on hooks.
- Prefer a dedicated loader/class to register hooks.
- Keep admin-only code behind `is_admin()` (or admin hooks) to reduce frontend overhead.

Read:
- `references/structure.md`

### 2) Hooks and lifecycle (activation/deactivation/uninstall)

Activation hooks are fragile; follow guardrails:

- Register activation/deactivation hooks at top-level, not inside other hooks
- Flush rewrite rules only when needed and only after registering CPTs/rules
- Uninstall should be explicit and safe (`uninstall.php` or `register_uninstall_hook`)

Read:
- `references/lifecycle.md`

### 3) Settings and admin UI (Settings API)

Prefer Settings API for options:

- `register_setting()`, `add_settings_section()`, `add_settings_field()`
- Sanitize via `sanitize_callback`

Read:
- `references/settings-api.md`

### 4) Security baseline (always)

Before shipping:

- Validate/sanitize input early; escape output late.
- Use nonces to prevent CSRF *and* capability checks for authorization.
- Avoid directly trusting `$_POST` / `$_GET`; use `wp_unslash()` and specific keys.
- Use `$wpdb->prepare()` for SQL; avoid building SQL with string concatenation.

Read:
- `references/security.md`

### 5) Custom Post Types and REST API (if needed)

- Register CPTs/taxonomies on `init` with `show_in_rest` for Gutenberg support.
- Follow REST API conventions: proper permission callbacks, schema, prepared statements.

Read:
- `references/rest-api.md`

### 6) Hooks and extensibility

- Add action hooks at key lifecycle points for extensibility.
- Use filters for modifiable output.
- Prefix all hook names with plugin slug.

Read:
- `references/hooks.md`

### 7) Cron and scheduled tasks (if needed)

- Schedule on activation, clear on deactivation.
- **Critical:** Never use same name for cron hook and internal `do_action()`.
- Process large datasets in batches.

Read:
- `references/cron.md`

### 8) Internationalization

- Use proper text domain matching plugin slug.
- Load textdomain on `plugins_loaded`.
- Use translation functions: `__()`, `_e()`, `_x()`, `_n()`.

## Verification

- Plugin activates with no fatals/notices.
- Settings save and read correctly (capability + nonce enforced).
- Uninstall removes intended data (and nothing else).
- Run repo lint/tests (PHPUnit/PHPCS if present).
- Passes Plugin Check plugin (no errors).

## Failure modes / debugging

- Activation hook not firing:
  - Hook registered incorrectly (not in main file scope), wrong main file path, or plugin is network-activated
- Settings not saving:
  - Settings not registered, wrong option group, missing capability, nonce failure
- Security regressions:
  - Nonce present but missing capability checks; or sanitized input not escaped on output
- Cron infinite recursion:
  - Same name used for cron hook and internal `do_action()` call

Read:
- `references/debugging.md`

## Escalation

For canonical detail, consult the Plugin Handbook and security guidelines before inventing patterns.

- [Plugin Developer Handbook](https://developer.wordpress.org/plugins/)
- [Security Best Practices](https://developer.wordpress.org/plugins/security/)
- [Settings API](https://developer.wordpress.org/plugins/settings/settings-api/)
