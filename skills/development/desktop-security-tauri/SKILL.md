---
name: desktop-security-tauri
description: Tauri 2.x deny-by-default security model, capabilities, permissions, scopes, ACL
---

# Tauri Capabilities & ACL

> **Quick Guide:** Tauri 2 uses a deny-by-default security model. Nothing is accessible unless explicitly granted in a capability file (`src-tauri/capabilities/*.json`). Capabilities bind permissions to specific windows. Permissions follow the `plugin:command` identifier pattern. Scopes restrict operations to specific paths or URLs with allow/deny lists (deny always wins). Every plugin and custom command needs a permission grant -- missing permissions cause runtime errors, not compile errors.
>
> **Current version:** Tauri 2.x (stable). Tauri 1.x used a boolean allowlist which is completely removed in v2.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST create at least one capability file in `src-tauri/capabilities/` -- without it, ALL plugin and core API calls fail at runtime)**

**(You MUST include `core:default` in every capability -- without it, basic app lifecycle commands fail)**

**(You MUST scope permissions to specific windows using the `windows` array -- a window not listed in any capability has zero IPC access)**

**(You MUST use deny scopes to restrict sensitive paths -- deny ALWAYS takes precedence over allow)**

**(You MUST use `plugin:permission-name` format for plugin permissions and plain `permission-name` for app commands)**

</critical_requirements>

---

**Auto-detection:** Tauri capabilities, src-tauri/capabilities, capability file, permissions, ACL, allow-scope, deny-scope, core:default, fs:allow, shell:allow, http:allow, permission set, remote domain, CapabilityRemote, desktop-schema.json, mobile-schema.json, scope allow deny, Tauri security, tauri permission denied, capability identifier

**When to use:**

- Creating or modifying capability files for a Tauri 2 app
- Granting permissions to specific windows or webviews
- Restricting filesystem, HTTP, or shell access with scoped permissions
- Writing custom permissions for your own Tauri commands
- Grouping permissions into permission sets
- Enabling remote domain access to Tauri APIs
- Debugging "permission denied" or "not allowed" runtime errors
- Migrating from the Tauri v1 allowlist to v2 capabilities

**When NOT to use:**

- Writing Tauri commands or IPC bridge logic (use desktop-framework-tauri)
- Plugin installation and registration (use desktop-framework-tauri)
- Window management, system tray, or menus (use desktop-framework-tauri)
- General Rust programming unrelated to Tauri ACL
- Frontend framework patterns

**Key patterns covered:**

- Capability file structure and fields ([examples/core.md](examples/core.md))
- Window-specific and platform-specific capabilities ([examples/core.md](examples/core.md))
- Scoped permissions with allow/deny lists ([examples/core.md](examples/core.md))
- Custom permission definitions in TOML ([examples/custom-permissions.md](examples/custom-permissions.md))
- Permission sets for grouping related permissions ([examples/custom-permissions.md](examples/custom-permissions.md))
- Remote domain access ([examples/core.md](examples/core.md))
- Debugging permission errors ([examples/core.md](examples/core.md))
- Migration from v1 allowlist ([reference.md](reference.md))

**Detailed resources:**

- [examples/core.md](examples/core.md) - Capability files, scoped permissions, window/platform targeting, remote access, debugging
- [examples/custom-permissions.md](examples/custom-permissions.md) - Custom permission definitions, permission sets, app-level permissions
- [reference.md](reference.md) - Permission identifier patterns, path variables, core permissions, v1 migration checklist

---

<philosophy>

## Philosophy

Tauri 2 implements a **deny-by-default** access control model. Every potentially dangerous operation (filesystem, network, shell, clipboard) is blocked until explicitly granted in a capability file. This is a fundamental shift from v1's boolean allowlist -- instead of toggling features on/off globally, you define granular permissions scoped to specific windows, platforms, and paths.

**The security hierarchy:**

1. **Capabilities** - Bind permissions to windows/webviews. A window not listed in any capability has zero IPC access.
2. **Permissions** - Define what operations are allowed or denied. Follow the `plugin:command` identifier pattern.
3. **Scopes** - Restrict WHERE operations can act (paths, URLs). Deny always supersedes allow.

**Key design decisions:**

- **Granular, not global** -- permissions are per-window, per-platform, per-path
- **Deny wins** -- if a path is denied by any scope, it is blocked even if allowed by another
- **Runtime, not compile-time** -- missing permissions cause runtime errors, not build errors. This makes debugging harder but allows dynamic permission resolution.
- **Schema-driven** -- capability files reference auto-generated schemas (`desktop-schema.json`, `mobile-schema.json`) for IDE autocompletion

**When to invest in fine-grained capabilities:**

- Multi-window apps where windows need different permission levels
- Apps handling sensitive data (credentials, financial records)
- Apps distributed publicly where security posture matters
- Apps with remote content that needs limited API access

**When simple capabilities suffice:**

- Single-window apps with straightforward needs
- Internal tools where the security boundary is less critical
- Prototypes and MVPs where iteration speed matters more

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Capability File Structure

Every Tauri 2 app needs at least one capability file in `src-tauri/capabilities/`. The file grants permissions to specific windows.

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Permissions for the main application window",
  "windows": ["main"],
  "permissions": ["core:default", "event:default", "window:default"]
}
```

**Key fields:** `identifier` (unique name), `windows` (which windows get these permissions), `permissions` (what operations are allowed). The `$schema` field enables IDE autocompletion for available permissions.

**Key rule:** All capabilities in `src-tauri/capabilities/` are auto-enabled unless you explicitly list capabilities in `tauri.conf.json`'s `app.security.capabilities` array -- in which case only the listed ones are used.

See [examples/core.md](examples/core.md) for all capability fields and patterns.

---

### Pattern 2: Scoped Permissions (Allow/Deny)

Restrict plugin operations to specific paths using inline scope objects. Deny always takes precedence.

```json
{
  "identifier": "fs:allow-read-text-file",
  "allow": [{ "path": "$APPDATA/**" }]
}
```

```json
{
  "identifier": "fs:deny-read-text-file",
  "deny": [{ "path": "$APPDATA/secrets/**" }]
}
```

**Key rule:** Deny always supersedes allow. If a path matches both an allow and a deny scope, it is blocked. Use `$APPDATA`, `$HOME`, `$RESOURCE` and other Tauri path variables -- not hardcoded OS paths.

See [examples/core.md](examples/core.md) for filesystem, HTTP, and shell scope patterns.

---

### Pattern 3: Window-Specific Capabilities

Different windows get different permission sets. An editor window gets write access; a viewer window gets read-only access.

```json
{
  "identifier": "editor-capability",
  "windows": ["editor"],
  "permissions": ["core:default", "fs:allow-write-text-file"]
}
```

```json
{
  "identifier": "viewer-capability",
  "windows": ["viewer"],
  "permissions": ["core:default", "fs:allow-read-text-file"]
}
```

**Key rule:** A window not listed in any capability's `windows` array has zero IPC access. Windows listed in multiple capabilities get the merged permissions of all matching capabilities.

See [examples/core.md](examples/core.md) for multi-window and wildcard patterns.

---

### Pattern 4: Platform-Specific Capabilities

Use the `platforms` field to restrict capabilities to specific operating systems.

```json
{
  "identifier": "desktop-features",
  "windows": ["main"],
  "platforms": ["linux", "macOS", "windows"],
  "permissions": ["core:default", "shell:allow-open", "global-shortcut:default"]
}
```

**Key rule:** Platform values are `"linux"`, `"macOS"`, `"windows"`, `"iOS"`, `"android"`. Splitting by platform prevents permission errors for platform-specific plugins.

See [examples/core.md](examples/core.md) for mobile-specific capability examples.

---

### Pattern 5: Custom Permission Definitions

Define permissions for your own Tauri commands using TOML files in `src-tauri/permissions/`.

```toml
# src-tauri/permissions/default.toml
[default]
description = "Default app permissions"
permissions = ["allow-greet", "allow-get-settings"]
```

```toml
# src-tauri/permissions/admin.toml
[[permission]]
identifier = "allow-admin-ops"
description = "Allow admin operations"
commands.allow = ["reset_database", "export_all_data"]
```

**Key point:** Tauri auto-generates `allow-*` and `deny-*` permissions for every command registered in `generate_handler![]`. Custom permission files let you group them and add scopes.

See [examples/custom-permissions.md](examples/custom-permissions.md) for permission sets and custom scope definitions.

---

### Pattern 6: Remote Domain Access

Grant remote web content access to Tauri APIs using the `remote` field with URL patterns.

```json
{
  "identifier": "remote-api-access",
  "windows": ["main"],
  "remote": {
    "urls": ["https://*.mydomain.dev"]
  },
  "permissions": ["core:default", "notification:default"]
}
```

**Key rule:** Remote URLs gain access to the specified Tauri APIs -- understand the security implications. On Linux and Android, Tauri cannot distinguish between iframe requests and window requests, so remote access should be used cautiously on those platforms.

See [examples/core.md](examples/core.md) for remote access patterns and security considerations.

</patterns>

---

<decision_framework>

## Decision Framework

### What Permissions Does My App Need?

```
What does the app do?
|-- Reads/writes files?
|   +-- tauri-plugin-fs permissions with path scopes
|-- Makes HTTP requests from Rust backend?
|   +-- tauri-plugin-http permissions with URL scopes
|-- Opens file/folder dialogs?
|   +-- tauri-plugin-dialog permissions
|-- Runs external processes?
|   +-- tauri-plugin-shell permissions (desktop only)
|-- Shows system notifications?
|   +-- tauri-plugin-notification permissions
|-- Uses persistent key-value storage?
|   +-- tauri-plugin-store permissions
+-- Basic app + window lifecycle only?
    +-- core:default is sufficient
```

### How Granular Should Capabilities Be?

```
How many windows does the app have?
|-- Single window?
|   +-- One capability file with all permissions is fine
|-- Multiple windows with SAME needs?
|   +-- One capability file listing all windows in the array
+-- Multiple windows with DIFFERENT needs?
    +-- Separate capability files per window (principle of least privilege)

Does the app need platform-specific features?
|-- Same features on all platforms?
|   +-- Omit the platforms field
+-- Different features per platform?
    +-- Separate capability files with platforms field
```

### Where to Put the Scope?

```
Is the scope for a built-in plugin?
|-- YES -> Inline in the capability file permissions array
|           { "identifier": "fs:allow-read-text-file", "allow": [...] }
+-- NO -> Is it for your custom commands?
    |-- YES -> Define in src-tauri/permissions/*.toml
    +-- NO -> It might not need a scope -- simple allow/deny suffices
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Missing `core:default` in a capability -- basic app lifecycle commands fail silently
- No capability file at all in `src-tauri/capabilities/` -- ALL IPC calls fail at runtime
- Using v1 `tauri.allowlist` in config -- completely removed in v2, does nothing
- Granting `fs:allow-read-text-file` without path scope -- allows reading ANY file on the system
- Missing `windows` array in capability -- permissions apply to no windows (useless capability)

**Medium Priority Issues:**

- Using wildcard `"windows": ["*"]` in production -- every window gets these permissions, including dynamic ones
- Not splitting capabilities by platform -- desktop-only plugins (shell, autostart, global-shortcut) cause errors on mobile
- Overly broad HTTP scopes (`http:allow-fetch` without URL scope) -- allows requests to any URL
- Granting write permissions when only read is needed -- violates least privilege

**Common Mistakes:**

- Forgetting that deny always wins -- adding a deny scope and wondering why the allow scope "doesn't work"
- Using OS paths (`/home/user/`) instead of Tauri path variables (`$HOME/`) in scopes
- Expecting compile-time errors for missing permissions -- they are runtime errors only
- Using `app.security.capabilities` in `tauri.conf.json` to list some capabilities, then wondering why unlisted capability files are ignored (explicit list overrides auto-discovery)
- Capability identifier containing digits after first character (identifiers are restricted to `[a-z]` plus hyphens)

**Gotchas & Edge Cases:**

- **Stale ACL in builds**: If you add a new permission but the build does not regenerate, the old ACL is embedded. Clean build (`cargo clean`) or ensure `build.rs` has `cargo:rerun-if-changed` for the capabilities directory
- **Schema path**: The `$schema` field must point to the correct generated schema (`../gen/schemas/desktop-schema.json` or `mobile-schema.json`). Run `cargo tauri dev` once to generate schemas
- **Merged capabilities**: A window listed in multiple capabilities gets ALL permissions from ALL matching capabilities merged together -- there is no "override" mechanism
- **Remote access on Linux/Android**: Tauri cannot distinguish iframe requests from window requests on these platforms, making remote domain restrictions less effective
- **Permission identifier format**: Plugin permissions use `plugin:permission-name`, app-defined permissions use just `permission-name` (no prefix). Using the wrong format causes "permission not found" errors
- **TOML vs JSON for permissions**: Capability files accept JSON or TOML. Custom permission definitions (in `src-tauri/permissions/`) must be TOML only

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST create at least one capability file in `src-tauri/capabilities/` -- without it, ALL plugin and core API calls fail at runtime)**

**(You MUST include `core:default` in every capability -- without it, basic app lifecycle commands fail)**

**(You MUST scope permissions to specific windows using the `windows` array -- a window not listed in any capability has zero IPC access)**

**(You MUST use deny scopes to restrict sensitive paths -- deny ALWAYS takes precedence over allow)**

**(You MUST use `plugin:permission-name` format for plugin permissions and plain `permission-name` for app commands)**

**Failure to follow these rules will cause silent runtime permission denials that do not surface at compile time.**

</critical_reminders>
