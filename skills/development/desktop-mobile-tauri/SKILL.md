---
name: desktop-mobile-tauri
description: Tauri 2.x mobile development - iOS via WKWebView, Android via Android WebView, mobile plugins, Swift/Kotlin native code, permissions, debugging
---

# Tauri 2.x Mobile Development

> **Quick Guide:** Tauri 2.x supports iOS (WKWebView) and Android (Android WebView) from the same codebase as desktop. Initialize with `tauri android init` / `tauri ios init`, run with `tauri android dev` / `tauri ios dev`. Mobile-only plugins (biometric, barcode-scanner, NFC, haptics, geolocation) use `#[cfg(mobile)]` for conditional registration. Custom native code uses Swift classes extending `Plugin` on iOS and Kotlin classes annotated with `@TauriPlugin` on Android. Every mobile plugin needs platform permissions (Info.plist keys on iOS, AndroidManifest.xml permissions on Android) in addition to Tauri capability grants.
>
> **Current version:** Tauri 2.x (stable). Mobile support is production-ready since Tauri 2.0 (2024).

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `#[cfg(mobile)]` when registering mobile-only plugins -- registering them unconditionally breaks desktop builds)**

**(You MUST add platform permissions (Info.plist on iOS, AndroidManifest.xml on Android) in ADDITION to Tauri capability file permissions -- missing platform permissions cause silent failures or runtime crashes)**

**(You MUST use `#[cfg_attr(mobile, tauri::mobile_entry_point)]` on `pub fn run()` -- without it, the app cannot launch on mobile)**

**(You MUST run mobile dev commands (`tauri ios dev`, `tauri android dev`) instead of `tauri dev` for mobile targets -- `tauri dev` only targets desktop)**

</critical_requirements>

---

**Auto-detection:** tauri android init, tauri ios init, tauri android dev, tauri ios dev, tauri-plugin-biometric, tauri-plugin-barcode-scanner, tauri-plugin-nfc, tauri-plugin-haptics, tauri-plugin-geolocation, #[cfg(mobile)], #[cfg(target_os = "android")], #[cfg(target_os = "ios")], mobile_entry_point, Info.plist, Info.ios.plist, AndroidManifest.xml, NSCameraUsageDescription, NSFaceIDUsageDescription, NSLocationWhenInUseUsageDescription, @TauriPlugin, Plugin Swift class, WKWebView, Invoke, InvokeArg, run_mobile_plugin, develop-mobile

**When to use:**

- Adding iOS or Android targets to a Tauri 2.x project
- Using mobile-specific plugins (biometric auth, barcode scanner, NFC, haptics, geolocation)
- Writing custom native plugin code in Swift (iOS) or Kotlin (Android)
- Configuring mobile platform permissions and capabilities
- Debugging on mobile simulators/emulators or physical devices
- Writing platform-conditional Rust code for mobile vs desktop

**When NOT to use:**

- Desktop-only Tauri development (use the desktop-framework-tauri skill)
- General Tauri concepts (commands, IPC, events, permissions, window management -- desktop skill covers these)
- Frontend framework patterns (component architecture, state management -- use respective framework skills)
- General Rust programming not related to Tauri mobile APIs

**Key patterns covered:**

- Mobile project initialization and prerequisites ([examples/core.md](examples/core.md))
- Mobile-specific plugin registration with `#[cfg(mobile)]` ([examples/core.md](examples/core.md))
- Mobile plugin gallery: biometric, barcode-scanner, NFC, haptics, geolocation ([examples/plugins.md](examples/plugins.md))
- Custom Swift plugin development for iOS ([examples/native-plugins.md](examples/native-plugins.md))
- Custom Kotlin plugin development for Android ([examples/native-plugins.md](examples/native-plugins.md))
- Platform permissions: Info.plist, AndroidManifest.xml ([examples/core.md](examples/core.md))
- Mobile debugging: Safari Web Inspector, Chrome DevTools, logcat ([examples/core.md](examples/core.md))

**Detailed resources:**

- [examples/core.md](examples/core.md) - Project setup, mobile plugin registration, permissions, platform-conditional code, debugging
- [examples/plugins.md](examples/plugins.md) - Mobile-specific plugins (biometric, barcode, NFC, haptics, geolocation)
- [examples/native-plugins.md](examples/native-plugins.md) - Custom Swift and Kotlin plugin development, calling Rust from mobile
- [reference.md](reference.md) - CLI commands, prerequisites checklist, mobile plugin registry, permission reference

---

<philosophy>

## Philosophy

Tauri mobile extends the same Rust backend + webview frontend architecture to iOS and Android. The key difference: mobile apps run in the OS native webview (WKWebView on iOS, Android WebView on Android) and can access device hardware through mobile-specific plugins. Your existing Tauri desktop code (commands, state, events) works on mobile without changes -- you add mobile support incrementally.

**When Tauri mobile is the right choice:**

- You already have a Tauri desktop app and want to share the codebase with mobile
- You want a single codebase for desktop + mobile with web frontend skills
- You need native device features (camera, biometrics, NFC) accessible via plugins
- You want small app sizes compared to alternatives that bundle their own webview

**When Tauri mobile may NOT be the right choice:**

- You need pixel-perfect native UI (Tauri renders web content, not native widgets)
- You need features that require a consistent browser engine (Tauri uses the OS webview, which varies)
- Your app is mobile-only with no desktop plans (native mobile frameworks may be more appropriate)
- You need advanced mobile-specific APIs not yet covered by Tauri plugins

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Mobile Project Initialization

Initialize mobile targets in an existing Tauri project. Each platform requires its own init step.

```sh
# Initialize Android target (generates gen/android/ project)
npx tauri android init

# Initialize iOS target (generates gen/apple/ project) -- macOS only
npx tauri ios init
```

After init, add the mobile entry point attribute to your `run()` function:

```rust
// src-tauri/src/lib.rs
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![/* commands */])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**Key point:** `#[cfg_attr(mobile, tauri::mobile_entry_point)]` is required for mobile builds. Without it, the app cannot start on iOS or Android. The attribute is a no-op on desktop, so it is safe to always include. See [examples/core.md](examples/core.md) for prerequisites and environment setup.

---

### Pattern 2: Mobile Plugin Registration with #[cfg(mobile)]

Mobile-only plugins must be conditionally registered to avoid breaking desktop builds.

```rust
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let mut builder = tauri::Builder::default();

    // Mobile-only plugins -- conditional registration
    #[cfg(mobile)]
    {
        builder = builder
            .plugin(tauri_plugin_biometric::init())
            .plugin(tauri_plugin_barcode_scanner::init())
            .plugin(tauri_plugin_nfc::init())
            .plugin(tauri_plugin_haptics::init())
            .plugin(tauri_plugin_geolocation::init());
    }

    builder
        .invoke_handler(tauri::generate_handler![/* commands */])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**Key point:** Using `#[cfg(mobile)]` ensures these plugins are only compiled and registered on iOS/Android. The Cargo dependencies should also be conditional. See [examples/core.md](examples/core.md) for Cargo.toml configuration.

---

### Pattern 3: Platform-Conditional Rust Code

Use `#[cfg(target_os)]` for platform-specific logic in commands or setup.

```rust
#[tauri::command]
fn get_platform_info() -> String {
    #[cfg(target_os = "android")]
    { "Running on Android".to_string() }

    #[cfg(target_os = "ios")]
    { "Running on iOS".to_string() }

    #[cfg(not(any(target_os = "android", target_os = "ios")))]
    { "Running on desktop".to_string() }
}
```

**Key point:** `#[cfg(mobile)]` is shorthand for `#[cfg(any(target_os = "android", target_os = "ios"))]`. Use the specific `target_os` when behavior differs between Android and iOS. See [examples/core.md](examples/core.md) for conditional dependency examples.

---

### Pattern 4: Platform Permissions (Info.plist + AndroidManifest.xml)

Mobile plugins require two layers of permissions: Tauri capability file grants AND native platform permission declarations.

```xml
<!-- src-tauri/Info.ios.plist (iOS) -->
<key>NSCameraUsageDescription</key>
<string>Required to scan barcodes</string>
<key>NSFaceIDUsageDescription</key>
<string>Authenticate to access secure features</string>
<key>NSLocationWhenInUseUsageDescription</key>
<string>Required for location-based features</string>
```

```xml
<!-- gen/android/app/src/main/AndroidManifest.xml (Android) -->
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-feature android:name="android.hardware.location.gps" android:required="true" />
```

**Key point:** Missing platform permissions cause silent failures or OS-level denials, even when Tauri capabilities are correctly configured. iOS needs usage description strings explaining WHY the app needs each permission. See [examples/core.md](examples/core.md) for the full permission layering pattern.

---

### Pattern 5: Custom Swift Plugin (iOS)

Write native iOS code by extending the Tauri `Plugin` class in Swift.

```swift
import Tauri
import WebKit

class MyPlugin: Plugin {
    @objc public func doSomething(_ invoke: Invoke) throws {
        let args = try invoke.parseArgs(DoSomethingArgs.self)
        // Native iOS API calls here
        invoke.resolve(["result": "success"])
    }
}

class DoSomethingArgs: Decodable {
    let input: String
    var optional: Bool?
}
```

**Key point:** Methods must have `@objc` attribute and accept an `Invoke` parameter. Arguments are parsed via `Decodable` classes. Use `invoke.resolve()` to return data or `invoke.reject()` to return errors. See [examples/native-plugins.md](examples/native-plugins.md) for complete examples.

---

### Pattern 6: Custom Kotlin Plugin (Android)

Write native Android code with `@TauriPlugin` annotation and `@Command` methods.

```kotlin
import app.tauri.annotation.Command
import app.tauri.annotation.InvokeArg
import app.tauri.annotation.TauriPlugin
import app.tauri.plugin.Invoke
import app.tauri.plugin.Plugin

@InvokeArg
internal class DoSomethingArgs {
    lateinit var input: String
    var optional: Boolean = false
}

@TauriPlugin
class MyPlugin(private val activity: Activity) : Plugin(activity) {
    @Command
    fun doSomething(invoke: Invoke) {
        val args = invoke.parseArgs(DoSomethingArgs::class.java)
        val ret = JSObject()
        ret.put("result", "success")
        invoke.resolve(ret)
    }
}
```

**Key point:** Commands annotated with `@Command` run on the main thread by default. Long-running operations must use coroutines or background threads to avoid freezing the UI. Arguments use `@InvokeArg` annotation with `lateinit var` for required fields. See [examples/native-plugins.md](examples/native-plugins.md) for async patterns and Rust interop.

---

### Pattern 7: Mobile Development and Debugging

Run and debug on mobile devices/simulators.

```sh
# Run on iOS simulator (macOS only)
npx tauri ios dev

# Run on specific iOS device/simulator
npx tauri ios dev 'iPhone 16'

# Run on Android emulator
npx tauri android dev

# Open in Xcode / Android Studio for native debugging
npx tauri ios dev --open
npx tauri android dev --open
```

**Debugging approaches:**

- **iOS:** Safari > Develop menu > select device > inspect localhost
- **Android:** `chrome://inspect` in Chrome > select connected device
- **Rust logs:** Use `tauri-plugin-log` for structured logging across platforms
- **Native logs:** Xcode console (iOS) / `adb logcat` (Android)

**Key point:** The `--open` flag launches the IDE but the Tauri CLI process must stay running. For physical devices, the dev server must be reachable on the local network -- the CLI handles this via `TAURI_DEV_HOST`. See [examples/core.md](examples/core.md) for physical device setup.

</patterns>

---

<decision_framework>

## Decision Framework

### Mobile Plugin Selection

```
Need device hardware access?
|-- Camera for scanning?
|   +-- tauri-plugin-barcode-scanner (QR, EAN-13, etc.)
|-- Biometric authentication?
|   +-- tauri-plugin-biometric (Face ID, fingerprint)
|-- NFC tags?
|   +-- tauri-plugin-nfc (read/write NDEF tags)
|-- Vibration / haptic feedback?
|   +-- tauri-plugin-haptics (impact, notification, selection feedback)
|-- GPS / location?
|   +-- tauri-plugin-geolocation (position, altitude, heading, speed)
+-- Other device features?
    +-- Check the Tauri plugin registry for mobile-compatible plugins
```

### Desktop vs Mobile Plugin Registration

```
Is this plugin mobile-only?
|-- YES (biometric, barcode, NFC, haptics, geolocation)
|   +-- Use #[cfg(mobile)] for registration
|   +-- Use cfg(any(target_os = "android", target_os = "ios")) for Cargo deps
|-- NO (fs, dialog, store, notification, http, etc.)
|   +-- Register unconditionally (works on both desktop and mobile)
+-- UNSURE
    +-- Check plugin docs for "Supported Platforms" table
```

### Permission Layering

```
Adding a mobile plugin?
|
+-- Step 1: Tauri capability file (src-tauri/capabilities/)
|   +-- Add plugin permissions (e.g., "biometric:default")
+-- Step 2: iOS Info.plist (src-tauri/Info.ios.plist)
|   +-- Add NS*UsageDescription keys for each permission
+-- Step 3: Android manifest (gen/android/.../AndroidManifest.xml)
|   +-- Add <uses-permission> and <uses-feature> elements
+-- Step 4: Runtime permission request
    +-- Use plugin's checkPermissions() / requestPermissions() API
```

See [reference.md](reference.md) for CLI command reference and mobile prerequisites checklist.

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Registering mobile-only plugins without `#[cfg(mobile)]` -- breaks desktop builds with missing native dependencies
- Missing `#[cfg_attr(mobile, tauri::mobile_entry_point)]` on `run()` -- mobile app cannot launch
- Adding Tauri capability permissions but forgetting platform permissions (Info.plist / AndroidManifest.xml) -- OS denies access at runtime
- Running `tauri dev` instead of `tauri ios dev` / `tauri android dev` for mobile -- builds for desktop, not mobile
- Using `@tauri-apps/api/tauri` import path (removed in v2 -- use `@tauri-apps/api/core`)

**Medium Priority Issues:**

- Not checking `isAvailable()` before using hardware plugins (biometric, NFC) -- the device may lack hardware support
- Running long operations on Android main thread in `@Command` methods -- freezes the UI
- Missing iOS `PrivacyInfo.xcprivacy` for App Store compliance -- Apple rejects apps without privacy manifests
- Forgetting runtime permission requests (`checkPermissions()` / `requestPermissions()`) -- iOS and Android require explicit user consent for camera, location, etc.
- Not handling the `TAURI_DEV_HOST` environment variable in dev server config -- physical device cannot reach dev server

**Common Mistakes:**

- Editing files in `gen/android/` or `gen/apple/` that get regenerated -- changes are lost on next `tauri android init` / `tauri ios init`
- Expecting identical webview rendering on iOS and Android -- WKWebView and Android WebView have different CSS/JS engine capabilities
- Forgetting to add Rust targets (`rustup target add aarch64-apple-ios aarch64-linux-android ...`) -- compilation fails
- Installing the Cargo crate without the npm package for mobile plugins -- TypeScript API unavailable

**Gotchas & Edge Cases:**

- **iOS only on macOS:** `tauri ios init` and `tauri ios dev` require macOS with Xcode installed
- **Android 16KB pages:** For NDK < 28, you need `-C link-arg=-Wl,-z,max-page-size=16384` in `.cargo/config.toml` for `aarch64-linux-android`
- **Haptics inconsistency:** No standard for vibration support on Android -- feedback APIs may not work on budget devices
- **NFC on iOS:** Requires iOS 14+ minimum deployment target and "Near Field Communication Tag Reading" capability in Xcode entitlements
- **`--open` flag lifecycle:** When using `tauri ios dev --open` or `tauri android dev --open`, the Tauri CLI process must stay alive -- killing it breaks the build pipeline
- **Safe areas:** Tauri does not provide built-in safe area handling -- use CSS `env(safe-area-inset-*)` or a community plugin for edge-to-edge rendering
- **Orientation lock:** No built-in Tauri API for forcing screen orientation -- requires platform-specific native code

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `#[cfg(mobile)]` when registering mobile-only plugins -- registering them unconditionally breaks desktop builds)**

**(You MUST add platform permissions (Info.plist on iOS, AndroidManifest.xml on Android) in ADDITION to Tauri capability file permissions -- missing platform permissions cause silent failures or runtime crashes)**

**(You MUST use `#[cfg_attr(mobile, tauri::mobile_entry_point)]` on `pub fn run()` -- without it, the app cannot launch on mobile)**

**(You MUST run mobile dev commands (`tauri ios dev`, `tauri android dev`) instead of `tauri dev` for mobile targets -- `tauri dev` only targets desktop)**

**Failure to follow these rules will cause desktop build failures, runtime permission denials, or apps that cannot launch on mobile devices.**

</critical_reminders>
