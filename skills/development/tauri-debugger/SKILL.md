---
name: tauri-debugger
description: Debug Tauri 2.x desktop app issues including dialogs, CSP, plugins, and Vite integration. Triggers on Tauri dialog not opening, file save dialog doesn't work, CSP errors, virtual:pwa-register errors, click handlers not working in Tauri, XDG Portal issues on Linux.
---

# Tauri Debugger Skill

Debug Tauri 2.x desktop app issues including dialogs, CSP, plugins, and Vite integration.

## Trigger Patterns

- Tauri dialog not opening / not appearing
- File save dialog doesn't work
- CSP (Content Security Policy) errors in Tauri
- `virtual:pwa-register` errors
- Click handlers not working in Tauri
- Tauri dev vs build differences
- XDG Portal issues on Linux

## Quick Diagnostics

### 1. Check Tauri Detection in Vite

```typescript
// vite.config.ts should have:
const isTauri =
  process.env.TAURI_ENV_PLATFORM !== undefined ||  // Build
  process.env.TAURI_DEV !== undefined              // Dev

// tauri.conf.json must set TAURI_DEV in dev:
"beforeDevCommand": "TAURI_DEV=true npm run dev"
```

### 2. Check XDG Portal (Linux)

```bash
# Portal service running?
systemctl --user status xdg-desktop-portal

# zenity installed (fallback)?
which zenity || echo "INSTALL: sudo apt install zenity"

# FileChooser portal working?
gdbus call --session \
    --dest org.freedesktop.portal.Desktop \
    --object-path /org/freedesktop/portal/desktop \
    --method org.freedesktop.DBus.Properties.Get \
    org.freedesktop.portal.FileChooser version
```

### 3. Check PWA Plugin Configuration

**WRONG** (causes CSP errors):
```typescript
!isTauri && VitePWA({ ... })  // No stub modules provided!
```

**CORRECT**:
```typescript
VitePWA({
  disable: isTauri,  // Provides empty stub modules
  ...
})
```

### 4. Check Dialog Plugin (Cargo.toml)

```toml
# For Linux with XDG Portal support:
tauri-plugin-dialog = { version = "2.6", default-features = false, features = ["xdg-portal"] }

# NOTE: Can't enable both gtk3 AND xdg-portal - they conflict!
```

### 5. Check Capabilities (src-tauri/capabilities/default.json)

```json
{
  "permissions": [
    "dialog:default",
    "dialog:allow-save",
    "dialog:allow-open",
    "fs:default",
    {
      "identifier": "fs:allow-write-text-file",
      "allow": [
        { "path": "$DOWNLOAD/**" },
        { "path": "$HOME/**" }
      ]
    }
  ]
}
```

## Common Issues & Solutions

### Issue: CSP Error `virtual:pwa-register/vue`

**Symptoms**:
- Console shows "Refused to load virtual:pwa-register/vue because it does not appear in the script-src directive"
- Click handlers don't fire
- Vue events seem broken

**Root Cause**: PWA plugin conditionally excluded but import statements still exist in code. No stub modules provided.

**Solution**:
```typescript
// vite.config.ts
VitePWA({
  disable: isTauri,  // This provides empty stub modules
  ...
})
```

### Issue: `isTauri` is false during `tauri dev`

**Symptoms**:
- PWA enabled in Tauri dev mode
- Tauri-specific code not running

**Root Cause**: `TAURI_ENV_PLATFORM` only set during `tauri build`, not `tauri dev`.

**Solution**:
```json
// tauri.conf.json
{
  "build": {
    "beforeDevCommand": "TAURI_DEV=true npm run dev"
  }
}
```

### Issue: Dialog doesn't appear on Linux

**Symptoms**:
- `dialog.save()` returns immediately with no dialog
- No errors in console

**Checklist**:
1. Install zenity: `sudo apt install zenity`
2. Check XDG Portal is running: `systemctl --user status xdg-desktop-portal`
3. Use xdg-portal feature in Cargo.toml (not gtk3)
4. Ensure DISPLAY/WAYLAND_DISPLAY env vars are set

### Issue: Blocking dialog freezes app

**Symptoms**:
- App hangs when calling `blocking_save_file()`

**Root Cause**: Blocking API can't acquire GTK MainContext from certain threads.

**Solution**: Use async API instead:
```rust
#[tauri::command(async)]
async fn save_file(app: AppHandle) -> Option<PathBuf> {
    app.dialog()
        .file()
        .save_file()
        .await
        .map(|p| p.into_path())
        .flatten()
}
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `vite.config.ts` | Tauri detection, PWA disable |
| `src-tauri/tauri.conf.json` | beforeDevCommand, CSP, devUrl |
| `src-tauri/Cargo.toml` | Plugin versions and features |
| `src-tauri/capabilities/default.json` | Permissions for dialogs, fs |
| `src-tauri/src/lib.rs` | Rust commands |

## Version Compatibility

| Package | Minimum Version | Notes |
|---------|-----------------|-------|
| `@tauri-apps/plugin-dialog` | 2.6.0 | XDG Portal support |
| `@tauri-apps/plugin-fs` | 2.4.5 | Better error messages |
| `tauri-plugin-dialog` (Rust) | 2.6 | xdg-portal feature |
| `zenity` (Linux) | any | Fallback dialog renderer |

## Related Skills

- `supabase-debugger` - For Supabase connection issues in Tauri
- `dev-debugging` - General Vue/Pinia debugging
