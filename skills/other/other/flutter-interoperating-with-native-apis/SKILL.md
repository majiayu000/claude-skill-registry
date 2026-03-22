---
name: "flutter-interoperating-with-native-apis"
description: "Interoperates with native platform APIs on Android, iOS, and the web. Use when accessing device-specific features not available in Dart or calling existing native code."
metadata:
  model: "models/gemini-3.1-pro-preview"
  last_modified: "Thu, 12 Mar 2026 22:21:02 GMT"

---
# Integrating Platform-Specific Code in Flutter

## Contents
- [Core Concepts & Terminology](#core-concepts--terminology)
- [Binding to Native C/C++ Code (FFI)](#binding-to-native-cc-code-ffi)
- [Implementing Platform Channels & Pigeon](#implementing-platform-channels--pigeon)
- [Hosting Native Platform Views](#hosting-native-platform-views)
- [Integrating Web Content & Wasm](#integrating-web-content--wasm)
- [Workflows](#workflows)

## Core Concepts & Terminology
- **FFI (Foreign Function Interface):** The `dart:ffi` library used to bind Dart directly to native C/C++ APIs.
- **Platform Channel:** The asynchronous message-passing system (`MethodChannel`, `BasicMessageChannel`) connecting the Dart client (UI) to the host platform (Kotlin/Java, Swift/Objective-C, C++).
- **Pigeon:** A code-generation tool that creates type-safe Platform Channels.
- **Platform View:** A mechanism to embed native UI components (e.g., Android `View`, iOS `UIView`) directly into the Flutter widget tree.
- **JS Interop:** The modern, Wasm-compatible approach to interacting with JavaScript and DOM APIs using `package:web` and `dart:js_interop`.

## Binding to Native C/C++ Code (FFI)
Use FFI to execute high-performance native code or utilize existing C/C++ libraries without the overhead of asynchronous Platform Channels.

### Project Setup
*   **If creating a standard C/C++ integration (Recommended since Flutter 3.38):** Use the `package_ffi` template. This utilizes `build.dart` hooks to compile native code, eliminating the need for OS-specific build files (CMake, build.gradle, podspec).
    ```bash
    flutter create --template=package_ffi <package_name>
    ```
*   **If requiring access to the Flutter Plugin API or Play Services:** Use the legacy `plugin_ffi` template.
    ```bash
    flutter create --template=plugin_ffi <plugin_name>
    ```

### Implementation Rules
*   **Symbol Visibility:** Always mark C++ symbols with `extern "C"` and prevent linker discarding during link-time optimization (LTO).
    ```cpp
    extern "C" __attribute__((visibility("default"))) __attribute__((used))
    ```
*   **Dynamic Library Naming (Apple Platforms):** Ensure your `build.dart` hook produces the exact same filename across all target architectures (e.g., `arm64` vs `x86_64`) and SDKs (`iphoneos` vs `iphonesimulator`). Do not append architecture suffixes to the `.dylib` or `.framework` names.
*   **Binding Generation:** Always use `package:ffigen` to generate Dart bindings from your C headers (`.h`). Configure this in `ffigen.yaml`.

## Implementing Platform Channels & Pigeon
Use Platform Channels when you need to interact with platform-specific APIs (e.g., Battery, Bluetooth, OS-level services) using the platform's native language.

### Pigeon (Type-Safe Channels)
Always prefer `package:pigeon` over raw `MethodChannel` implementations for complex or frequently used APIs.
1.  Define the messaging protocol in a standalone Dart file using Pigeon annotations (`@HostApi()`).
2.  Generate the host (Kotlin/Swift/C++) and client (Dart) code.
3.  Implement the generated interfaces on the native side.

### Threading Rules
*   **Main Thread Requirement:** Always invoke channel methods destined for Flutter on the platform's main thread (UI thread).
*   **Background Execution:** If executing channel handlers on a background thread (Android/iOS), you must use the Task Queue API (`makeBackgroundTaskQueue()`).
*   **Isolates:** To use plugins/channels from a Dart background `Isolate`, ensure it is registered using `BackgroundIsolateBinaryMessenger.ensureInitialized(rootIsolateToken)`.

## Hosting Native Platform Views
Use Platform Views to embed native UI components (e.g., Google Maps, native video players) into the Flutter widget tree.

### Android Platform Views
Evaluate the trade-offs between the two rendering modes and select the appropriate one:
*   **If requiring perfect fidelity, accessibility, or SurfaceView support:** Use **Hybrid Composition** (`PlatformViewLink` + `AndroidViewSurface`). This appends the native view to the hierarchy but may reduce Flutter's rendering performance.
*   **If prioritizing Flutter rendering performance and transformations:** Use **Texture Layer** (`AndroidView`). This renders the native view into a texture. Note: Quick scrolling may drop frames, and `SurfaceView` is problematic.

### iOS Platform Views
*   iOS exclusively uses Hybrid Composition.
*   Implement `FlutterPlatformViewFactory` and `FlutterPlatformView` in Swift or Objective-C.
*   Use the `UiKitView` widget on the Dart side.
*   *Limitation:* `ShaderMask` and `ColorFiltered` widgets cannot be applied to iOS Platform Views.

## Integrating Web Content & Wasm
Flutter Web supports compiling to WebAssembly (Wasm) for improved performance and multi-threading.

### Wasm Compilation
*   Compile to Wasm using: `flutter build web --wasm`.
*   **Server Configuration:** To enable multi-threading, configure your HTTP server to emit the following headers:
    *   `Cross-Origin-Embedder-Policy: credentialless` (or `require-corp`)
    *   `Cross-Origin-Opener-Policy: same-origin`
*   *Limitation:* WasmGC is not currently supported on iOS browsers (WebKit limitation). Flutter will automatically fall back to JavaScript if WasmGC is unavailable.

### Web Interop
*   **If writing new web-specific code:** Strictly use `package:web` and `dart:js_interop`.
*   **Do NOT use:** `dart:html`, `dart:js`, or `package:js`. These are incompatible with Wasm compilation.
*   **Embedding HTML:** Use `HtmlElementView.fromTagName` to inject arbitrary HTML elements (like `<video>`) into the Flutter Web DOM.

---

## Workflows

### Workflow: Creating a Native FFI Integration
Use this workflow when binding to a C/C++ library.

- [ ] **Task Progress:**
  - [ ] 1. Run `flutter create --template=package_ffi <name>`.
  - [ ] 2. Place C/C++ source code in the `src/` directory.
  - [ ] 3. Ensure all exported C++ functions are wrapped in `extern "C"` and visibility attributes.
  - [ ] 4. Configure `ffigen.yaml` to point to your header files.
  - [ ] 5. Run `dart run ffigen` to generate Dart bindings.
  - [ ] 6. Modify `hook/build.dart` if linking against pre-compiled or system libraries.
  - [ ] 7. Run validator -> `flutter test` -> review errors -> fix.

### Workflow: Implementing a Type-Safe Platform Channel (Pigeon)
Use this workflow when you need to call Kotlin/Swift APIs from Dart.

- [ ] **Task Progress:**
  - [ ] 1. Add `pigeon` to `dev_dependencies`.
  - [ ] 2. Create `pigeons/messages.dart` and define data classes and `@HostApi()` abstract classes.
  - [ ] 3. Run the Pigeon generator script to output Dart, Kotlin, and Swift files.
  - [ ] 4. **Android:** Implement the generated interface in `MainActivity.kt` or your Plugin class.
  - [ ] 5. **iOS:** Implement the generated protocol in `AppDelegate.swift` or your Plugin class.
  - [ ] 6. **Dart:** Import the generated Dart file and call the API methods.
  - [ ] 7. Run validator -> verify cross-platform compilation -> review errors -> fix.

### Workflow: Embedding a Native Platform View
Use this workflow when embedding a native UI component (e.g., a native map or camera view).

- [ ] **Task Progress:**
  - [ ] 1. **Dart:** Create a widget that conditionally returns `AndroidView` (or `PlatformViewLink`) for Android, and `UiKitView` for iOS based on `defaultTargetPlatform`.
  - [ ] 2. **Android:** Create a class implementing `PlatformView` that returns the native Android `View`.
  - [ ] 3. **Android:** Create a `PlatformViewFactory` and register it in `configureFlutterEngine`.
  - [ ] 4. **iOS:** Create a class implementing `FlutterPlatformView` that returns the native `UIView`.
  - [ ] 5. **iOS:** Create a `FlutterPlatformViewFactory` and register it in `application:didFinishLaunchingWithOptions:`.
  - [ ] 6. Run validator -> test on physical Android and iOS devices -> review UI clipping/scrolling issues -> fix.
