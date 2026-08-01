---
name: desktop-plugins-tauri
description: Tauri 2.x official plugin ecosystem, plugin APIs, permissions, and custom plugin development
---

# Tauri 2.x Plugin Ecosystem

> **Quick Guide:** Tauri plugins follow a dual-install pattern: Cargo crate (Rust backend) + npm package (JS frontend). Every plugin must be registered with `.plugin()` in Rust AND have permissions granted in a capability file. Missing any step causes runtime errors, not compile errors. Custom plugins use `tauri::plugin::Builder` with optional mobile support (Swift/Kotlin). There are 30+ official plugins covering fs, http, dialog, store, notification, shell, updater, sql, log, stronghold, deep-link, global-shortcut, and more.
>
> **Current version:** Tauri 2.x (stable). All plugins require Rust 1.77.2+.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST complete ALL four installation steps for every plugin: 1) cargo add crate, 2) npm install bindings, 3) `.plugin()` registration in Rust, 4) permissions in capability file -- missing any step causes runtime errors)**

**(You MUST scope plugin permissions in capability files -- never grant unscoped `fs:allow-read-text-file` or `http:default` without URL restrictions)**

**(You MUST use `@tauri-apps/plugin-*` npm packages for JS bindings -- not `@tauri-apps/api/*` which is the core API)**

**(You MUST use `#[cfg(desktop)]` guard when registering desktop-only plugins -- mobile builds will fail otherwise)**

**(You MUST use `tauri::plugin::Builder` with an `init()` convention when creating custom plugins -- not raw command registration)**

</critical_requirements>

---

**Auto-detection:** tauri-plugin, @tauri-apps/plugin, tauri_plugin, plugin registration, .plugin(), tauri-plugin-fs, tauri-plugin-http, tauri-plugin-store, tauri-plugin-dialog, tauri-plugin-notification, tauri-plugin-shell, tauri-plugin-updater, tauri-plugin-log, tauri-plugin-sql, tauri-plugin-stronghold, tauri-plugin-deep-link, tauri-plugin-global-shortcut, tauri-plugin-autostart, tauri-plugin-clipboard-manager, tauri-plugin-window-state, tauri-plugin-single-instance, tauri-plugin-barcode-scanner, tauri-plugin-biometric, tauri-plugin-os, tauri-plugin-process, custom plugin, plugin development, npx tauri plugin new

**When to use:**

- Installing and configuring official Tauri plugins
- Using plugin JavaScript APIs from the frontend
- Scoping plugin permissions in capability files
- Creating custom plugins with Rust backend + optional JS API
- Adding mobile support (Swift/Kotlin) to custom plugins
- Choosing between plugins for a specific use case (store vs stronghold, fs vs dialog)

**When NOT to use:**

- Tauri core framework patterns (commands, invoke, state, events, tray, windows -- use the framework skill)
- Frontend framework patterns (component architecture, state management -- use respective framework skills)
- General Rust programming not related to Tauri plugin APIs
- Build tool or bundler configuration (separate tooling concern)

**Key patterns covered:**

- Four-step plugin installation pattern ([examples/core.md](examples/core.md))
- Data & storage plugins: fs, store, sql, stronghold ([examples/data-storage.md](examples/data-storage.md))
- System integration plugins: shell, notification, clipboard, dialog, os, process ([examples/system.md](examples/system.md))
- App lifecycle plugins: updater, deep-link, autostart, single-instance, window-state, global-shortcut ([examples/lifecycle.md](examples/lifecycle.md))
- Networking plugins: http, log, websocket, upload ([examples/networking.md](examples/networking.md))
- Mobile-only plugins: barcode-scanner, biometric, geolocation, haptics, nfc ([examples/mobile.md](examples/mobile.md))
- Custom plugin development: Builder pattern, commands, config, lifecycle hooks, mobile support ([examples/custom-plugins.md](examples/custom-plugins.md))

**Detailed resources:**

- [examples/core.md](examples/core.md) - Installation pattern, permission scoping, multi-plugin registration
- [examples/data-storage.md](examples/data-storage.md) - fs, store, sql, stronghold plugin APIs
- [examples/system.md](examples/system.md) - shell, notification, clipboard, dialog, os, process APIs
- [examples/lifecycle.md](examples/lifecycle.md) - updater, deep-link, autostart, single-instance, window-state, global-shortcut
- [examples/networking.md](examples/networking.md) - http, log, websocket, upload
- [examples/mobile.md](examples/mobile.md) - barcode-scanner, biometric, geolocation, haptics, nfc
- [examples/custom-plugins.md](examples/custom-plugins.md) - Custom plugin scaffolding, Builder, mobile (Swift/Kotlin)
- [reference.md](reference.md) - Full plugin registry table, permission patterns, platform support matrix

---

<philosophy>

## Philosophy

Tauri plugins extend the core framework with native capabilities through a **dual-architecture** design: a Rust backend crate providing the implementation, and an npm package providing typed JavaScript bindings. This separation enforces security -- every plugin operation must be explicitly permitted in a capability file.

**Plugin architecture principles:**

- **Security by default**: Plugins do nothing until permissions are granted. Permissions are scoped per-window and can restrict operations to specific paths, URLs, or commands.
- **Dual install**: Rust crate handles native operations; npm package provides the typed JS API. Both are required.
- **Platform awareness**: Some plugins are desktop-only (shell, autostart, global-shortcut), some are mobile-only (barcode-scanner, biometric, haptics), and many work on both.
- **Convention over configuration**: All official plugins follow the same four-step install pattern. Custom plugins use `tauri::plugin::Builder` with an `init()` export.

**When to use plugins vs custom commands:**

- Need file system, HTTP, notifications, or other OS features? Use the official plugin.
- Need custom business logic that runs in Rust? Write a Tauri command (framework skill).
- Need a reusable native capability shared across projects? Write a custom plugin.

**When NOT to use a plugin:**

- The JS Web API already covers the need (e.g., `navigator.clipboard` for simple text copy in some contexts)
- A custom Tauri command is simpler for a one-off operation
- The plugin is mobile-only but your app is desktop-only (or vice versa)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Four-Step Plugin Installation

Every official plugin requires exactly four steps. Missing any step causes runtime errors, not compile errors.

```sh
# Step 1: Add Rust crate
cargo add tauri-plugin-store

# Step 2: Add JS bindings
npm add @tauri-apps/plugin-store

# Step 3: Register plugin in Rust (src-tauri/src/lib.rs)
# .plugin(tauri_plugin_store::Builder::new().build())

# Step 4: Add permissions to capability file (src-tauri/capabilities/main.json)
# "store:default"
```

**Why all four steps:** Cargo crate = backend implementation, npm package = typed JS bindings, `.plugin()` = runtime activation, capability permission = frontend authorization. Any missing piece causes a runtime error with an unhelpful message.

**Shortcut:** `cargo tauri add <plugin>` handles steps 1 and 3 automatically. You still need npm install (step 2) and permissions (step 4).

See [examples/core.md](examples/core.md) for multi-plugin registration and permission scoping.

---

### Pattern 2: Permission Scoping

Plugins operate under least-privilege. Scope permissions to specific paths, URLs, or commands.

```json
{
  "permissions": [
    "core:default",
    {
      "identifier": "fs:allow-read-text-file",
      "allow": [{ "path": "$APPDATA/**" }]
    },
    {
      "identifier": "http:default",
      "allow": [{ "url": "https://api.example.com/**" }]
    }
  ]
}
```

**Why scoping matters:** Unscoped `fs:allow-read-text-file` grants access to ANY file on the system. Unscoped `http:default` allows requests to ANY domain. Always restrict to the minimum required scope.

See [examples/core.md](examples/core.md) for shell command scoping and window-specific permissions.

---

### Pattern 3: Desktop-Only Plugin Guard

Desktop-only plugins (shell, autostart, global-shortcut, single-instance, window-state, positioner) must be wrapped in `#[cfg(desktop)]` to prevent mobile build failures.

```rust
tauri::Builder::default()
    .setup(|app| {
        #[cfg(desktop)]
        {
            app.handle().plugin(tauri_plugin_autostart::init(
                tauri_plugin_autostart::MacosLauncher::LaunchAgent,
                None,
            ));
            app.handle().plugin(tauri_plugin_global_shortcut::Builder::new().build());
        }
        Ok(())
    })
```

**Key point:** Without `#[cfg(desktop)]`, the Rust compiler will fail on mobile targets because these crates do not support iOS/Android.

---

### Pattern 4: Store vs Stronghold vs SQL

Three storage plugins serve different needs:

| Plugin     | Use Case                   | Encryption     | Query                            | Platform |
| ---------- | -------------------------- | -------------- | -------------------------------- | -------- |
| Store      | App preferences, settings  | No             | Key-value only                   | All      |
| Stronghold | Secrets, API keys, tokens  | Yes (Argon2)   | Key-value only                   | Desktop  |
| SQL        | Structured data, relations | No (app-level) | Full SQL (SQLite/MySQL/Postgres) | All      |

**Decision:** User preferences and simple config? Store. Sensitive credentials? Stronghold. Structured relational data? SQL.

See [examples/data-storage.md](examples/data-storage.md) for complete API examples for each.

---

### Pattern 5: Updater with Signed Releases

The updater plugin requires cryptographic signatures -- this cannot be disabled. Updates check an endpoint, verify the signature, download, and install.

```typescript
import { check } from "@tauri-apps/plugin-updater";
import { relaunch } from "@tauri-apps/plugin-process";

const update = await check();
if (update) {
  await update.downloadAndInstall((event) => {
    // event.event: "Started" | "Progress" | "Finished"
  });
  await relaunch();
}
```

**Key point:** Generate signing keys with `cargo tauri signer generate`. Set `TAURI_SIGNING_PRIVATE_KEY` during builds. The public key goes in `tauri.conf.json`. Losing the private key means you cannot ship updates to existing users.

See [examples/lifecycle.md](examples/lifecycle.md) for endpoint JSON format and Rust API.

---

### Pattern 6: Custom Plugin Development

Custom plugins use `tauri::plugin::Builder` with the `init()` convention.

```rust
use tauri::plugin::{Builder, TauriPlugin};
use tauri::Runtime;

#[tauri::command]
fn my_command() -> String {
    "Hello from plugin".into()
}

pub fn init<R: Runtime>() -> TauriPlugin<R> {
    Builder::new("my-plugin")
        .invoke_handler(tauri::generate_handler![my_command])
        .setup(|app, _api| {
            // Initialize state, start background tasks
            Ok(())
        })
        .build()
}
```

**Key points:** Plugin commands are invoked as `plugin:my-plugin|my_command` from JS. Scaffold a full plugin project with `npx @tauri-apps/cli plugin new <name>`. The template includes `desktop.rs`, `mobile.rs`, permissions, and JS bindings.

See [examples/custom-plugins.md](examples/custom-plugins.md) for lifecycle hooks, configuration, and mobile support.

</patterns>

---

<decision_framework>

## Decision Framework

### Plugin Selection

```
What native capability do you need?
|
+-- File system read/write?
|   +-- tauri-plugin-fs (scoped to specific directories)
|
+-- File/folder picker dialog?
|   +-- tauri-plugin-dialog (open, save, message, ask)
|
+-- HTTP requests bypassing CORS?
|   +-- tauri-plugin-http (scope to specific domains)
|
+-- Persistent key-value storage?
|   +-- Sensitive data (tokens, keys)? -> tauri-plugin-stronghold
|   +-- App preferences/settings? -> tauri-plugin-store
|
+-- Relational/structured data?
|   +-- tauri-plugin-sql (SQLite, MySQL, PostgreSQL)
|
+-- System notifications?
|   +-- tauri-plugin-notification (check permissions first on macOS/mobile)
|
+-- Run external processes?
|   +-- tauri-plugin-shell (desktop only, scope allowed commands)
|
+-- Auto-update?
|   +-- tauri-plugin-updater (requires signed releases)
|
+-- Structured logging?
|   +-- tauri-plugin-log (targets: stdout, file, webview)
|
+-- Custom URL scheme handling?
|   +-- tauri-plugin-deep-link (configure per-platform)
|
+-- System-wide keyboard shortcuts?
|   +-- tauri-plugin-global-shortcut (desktop only)
|
+-- Launch on system startup?
|   +-- tauri-plugin-autostart (desktop only)
|
+-- Single app instance?
|   +-- tauri-plugin-single-instance (desktop only)
|
+-- Remember window position/size?
|   +-- tauri-plugin-window-state (desktop only)
|
+-- Clipboard access?
|   +-- tauri-plugin-clipboard-manager
|
+-- Mobile camera/scanner?
|   +-- tauri-plugin-barcode-scanner (mobile only)
|
+-- Biometric auth?
|   +-- tauri-plugin-biometric (mobile only)
|
+-- OS/platform info?
|   +-- tauri-plugin-os
|
+-- App restart/exit?
    +-- tauri-plugin-process
```

### Custom Plugin vs Custom Command

```
Is this a reusable capability shared across projects?
+-- YES -> Custom plugin (npx @tauri-apps/cli plugin new)
+-- NO  -> Is it complex enough to need its own permission model?
    +-- YES -> Custom plugin
    +-- NO  -> Regular Tauri command (simpler, framework skill)
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Missing any of the four installation steps (cargo, npm, `.plugin()`, permissions) -- causes runtime error with unhelpful message
- Unscoped filesystem permissions (`fs:allow-read-text-file` without path restriction) -- grants access to entire filesystem
- Unscoped HTTP permissions (`http:default` without URL pattern) -- allows requests to any domain
- Unscoped shell execute (`shell:allow-execute` without command allowlist) -- allows running arbitrary commands
- Using `@tauri-apps/api/*` imports for plugin functionality -- plugins use `@tauri-apps/plugin-*` packages
- Registering desktop-only plugins without `#[cfg(desktop)]` -- breaks mobile builds
- Losing the updater signing private key -- makes shipping updates to existing users impossible

**Medium Priority Issues:**

- Using Store plugin for sensitive data (API keys, tokens) -- Store is NOT encrypted, use Stronghold
- Not checking `isPermissionGranted()` before sending notifications on macOS/mobile
- Granting `shell:allow-execute` when only `shell:allow-open` (URLs/files) is needed
- Missing `sql:allow-execute` permission (default only includes read operations)
- Forgetting to call `stronghold.save()` after modifications (changes are lost)

**Common Mistakes:**

- Installing the cargo crate but forgetting the npm package (or vice versa)
- Using `cargo tauri add` and assuming all four steps are done (npm install and permissions still needed)
- Not scoping HTTP plugin URLs -- allows the app to make requests to arbitrary servers
- Using the updater plugin on mobile (it is desktop-only)
- Expecting Store data to persist across app reinstalls (store location depends on app identifier)

**Gotchas & Edge Cases:**

- **Plugin init variants**: Some plugins use `.init()` (fs, dialog, shell, notification), others use `Builder::new().build()` (store, updater, global-shortcut, log) -- check each plugin's docs
- **Store autoSave**: When `autoSave: false`, you must call `store.save()` manually. When `autoSave` is a number, it debounces saves by that many milliseconds.
- **SQL default permissions**: Only read operations (select, load, close) are granted by default -- `sql:allow-execute` must be added explicitly for INSERT/UPDATE/DELETE
- **Stronghold platform**: Desktop-only. Store data as `Uint8Array` (not strings) -- use `TextEncoder`/`TextDecoder` for string conversion
- **Deep link desktop**: On desktop, deep links arrive as command-line arguments. Combine with single-instance plugin to handle links when the app is already running.
- **Global shortcut conflicts**: Registering a shortcut already bound system-wide (e.g., `Ctrl+C`) silently fails or overrides the system binding depending on the OS
- **Window-state plugin**: Automatically restores window position/size on startup with zero JS code needed -- just register the plugin
- **Plugin registration order**: Does not matter. Each `.plugin()` call is independent.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST complete ALL four installation steps for every plugin: 1) cargo add crate, 2) npm install bindings, 3) `.plugin()` registration in Rust, 4) permissions in capability file -- missing any step causes runtime errors)**

**(You MUST scope plugin permissions in capability files -- never grant unscoped `fs:allow-read-text-file` or `http:default` without URL restrictions)**

**(You MUST use `@tauri-apps/plugin-*` npm packages for JS bindings -- not `@tauri-apps/api/*` which is the core API)**

**(You MUST use `#[cfg(desktop)]` guard when registering desktop-only plugins -- mobile builds will fail otherwise)**

**(You MUST use `tauri::plugin::Builder` with an `init()` convention when creating custom plugins -- not raw command registration)**

**Failure to follow these rules will cause silent runtime errors, security vulnerabilities from unscoped permissions, or broken mobile builds.**

</critical_reminders>
