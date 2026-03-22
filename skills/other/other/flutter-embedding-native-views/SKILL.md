---
name: "flutter-embedding-native-views"
description: "Embeds native Android, iOS, or macOS views into a Flutter app. Use when integrating complex native components like maps or web views."
metadata:
  model: "models/gemini-3.1-pro-preview"
  last_modified: "Thu, 12 Mar 2026 22:20:28 GMT"

---
# Integrating Platform Views and Web Content

## Contents
- [Platform Views Architecture](#platform-views-architecture)
- [Web Embedding Architecture](#web-embedding-architecture)
- [Workflow: Implementing Android Platform Views](#workflow-implementing-android-platform-views)
- [Workflow: Implementing iOS Platform Views](#workflow-implementing-ios-platform-views)
- [Workflow: Embedding Flutter in Web Applications](#workflow-embedding-flutter-in-web-applications)
- [Examples](#examples)

## Platform Views Architecture

Platform Views allow embedding native views (Android, iOS, macOS) directly into a Flutter application, enabling the application of transforms, clips, and opacity from Dart.

### Android Implementations (API 23+)
Choose the appropriate implementation based on your performance and fidelity requirements:
*   **Hybrid Composition:** Renders Flutter content into a texture and uses `SurfaceFlinger` to compose both. 
    *   *Pros:* Best performance and fidelity for Android views.
    *   *Cons:* Lowers overall application FPS. Certain Flutter widget transformations will not work.
*   **Texture Layer (Texture Layer Hybrid Composition):** Renders Platform Views into a texture. Flutter draws them via the texture and renders its own content directly into a Surface.
    *   *Pros:* Best performance for Flutter rendering. All transformations work correctly.
    *   *Cons:* Quick scrolling (e.g., WebViews) can be janky. `SurfaceView` is problematic (breaks accessibility). Text magnifiers break unless Flutter is rendered into a `TextureView`.

### iOS & macOS Implementations
*   **iOS:** Uses Hybrid Composition exclusively. The native `UIView` is appended to the view hierarchy.
    *   *Limitations:* `ShaderMask` and `ColorFiltered` widgets are not supported. `BackdropFilter` has composition limitations.
*   **macOS:** Uses Hybrid Composition (`NSView`). 
    *   *Limitations:* Not fully functional in current releases (e.g., gesture support is unavailable).

### Performance Mitigation
Mitigate performance drops during complex Dart animations by rendering a screenshot of the native view as a placeholder texture while the animation runs.

## Web Embedding Architecture

Embed Flutter into existing web applications (Vanilla JS, React, Angular, etc.) using either Full Page mode or Embedded (Multi-view) mode.

*   **Full Page Mode:** Flutter takes over the entire browser window. Use an `iframe` if you need to constrain the Flutter app without modifying the Flutter bootstrap process.
*   **Embedded Mode (Multi-view):** Render Flutter into specific HTML elements (`div`s). Requires `multiViewEnabled: true` during engine initialization.
    *   Manage views from JavaScript using `app.addView()` and `app.removeView()`.
    *   In Dart, replace `runApp` with `runWidget`.
    *   Manage the dynamic list of views using `WidgetsBinding.instance.platformDispatcher.views` and render them using `ViewCollection` and `View` widgets.

## Workflow: Implementing Android Platform Views

Follow this sequential workflow to implement a Platform View on Android.

**Task Progress:**
- [ ] 1. Determine the composition mode (Hybrid vs. Texture Layer).
- [ ] 2. Implement the Dart widget.
- [ ] 3. Implement the native Android View and Factory.
- [ ] 4. Register the Platform View in the Android host.
- [ ] 5. Run validator -> review rendering -> fix manual invalidation issues.

### 1. Dart Implementation
If using **Hybrid Composition**, use `PlatformViewLink`, `AndroidViewSurface`, and `PlatformViewsService.initSurfaceAndroidView`.
If using **Texture Layer**, use the `AndroidView` widget.

### 2. Native Implementation
Create a class implementing `io.flutter.plugin.platform.PlatformView` that returns your native `android.view.View`.
Create a factory extending `PlatformViewFactory` to instantiate your view.

### 3. Registration
Register the factory in your `MainActivity.kt` (or plugin) using `flutterEngine.platformViewsController.registry.registerViewFactory`.

*Note: If your native view uses `SurfaceView` or `SurfaceTexture`, manually call `invalidate` on the View or its parent when content changes, as they do not invalidate themselves automatically.*

## Workflow: Implementing iOS Platform Views

Follow this sequential workflow to implement a Platform View on iOS.

**Task Progress:**
- [ ] 1. Implement the Dart widget using `UiKitView`.
- [ ] 2. Implement the native iOS View (`FlutterPlatformView`) and Factory (`FlutterPlatformViewFactory`).
- [ ] 3. Register the Platform View in `AppDelegate.swift` or the plugin registrar.
- [ ] 4. Run validator -> review composition limitations -> fix unsupported filters.

## Workflow: Embedding Flutter in Web Applications

Follow this sequential workflow to embed Flutter into an existing web DOM.

**Task Progress:**
- [ ] 1. Update `flutter_bootstrap.js` to enable multi-view.
- [ ] 2. Update `main.dart` to use `runWidget` and `ViewCollection`.
- [ ] 3. Implement JavaScript logic to add/remove host elements.
- [ ] 4. Run validator -> review view constraints -> fix CSS conflicts.

### 1. JavaScript Configuration
In `flutter_bootstrap.js`, initialize the engine with `multiViewEnabled: true`.
Use the returned `app` object to add views: `app.addView({ hostElement: document.getElementById('my-div') })`.

### 2. Dart Configuration
Replace `runApp()` with `runWidget()`.
Create a root widget that listens to `WidgetsBindingObserver.didChangeMetrics`.
Map over `WidgetsBinding.instance.platformDispatcher.views` to create a `View` widget for each attached `FlutterView`, and wrap them all in a `ViewCollection`.

## Examples

### Example: Android Texture Layer (Dart)
```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class NativeAndroidView extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    const String viewType = 'my_native_view';
    final Map<String, dynamic> creationParams = <String, dynamic>{};

    return AndroidView(
      viewType: viewType,
      layoutDirection: TextDirection.ltr,
      creationParams: creationParams,
      creationParamsCodec: const StandardMessageCodec(),
    );
  }
}
```

### Example: Web Multi-View Initialization (JavaScript)
```javascript
_flutter.loader.load({
  onEntrypointLoaded: async function(engineInitializer) {
    let engine = await engineInitializer.initializeEngine({
      multiViewEnabled: true,
    });
    let app = await engine.runApp();
    
    // Add a view to a specific DOM element
    let viewId = app.addView({
      hostElement: document.querySelector('#flutter-host-container'),
      initialData: { customData: 'Hello from JS' }
    });
  }
});
```

### Example: Web Multi-View Root Widget (Dart)
```dart
import 'dart:ui' show FlutterView;
import 'package:flutter/widgets.dart';

void main() {
  runWidget(MultiViewApp(viewBuilder: (context) => const MyEmbeddedWidget()));
}

class MultiViewApp extends StatefulWidget {
  final WidgetBuilder viewBuilder;
  const MultiViewApp({super.key, required this.viewBuilder});

  @override
  State<MultiViewApp> createState() => _MultiViewAppState();
}

class _MultiViewAppState extends State<MultiViewApp> with WidgetsBindingObserver {
  Map<Object, Widget> _views = {};

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _updateViews();
  }

  @override
  void didChangeMetrics() => _updateViews();

  void _updateViews() {
    final newViews = <Object, Widget>{};
    for (final FlutterView view in WidgetsBinding.instance.platformDispatcher.views) {
      newViews[view.viewId] = _views[view.viewId] ?? View(
        view: view,
        child: Builder(builder: widget.viewBuilder),
      );
    }
    setState(() => _views = newViews);
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ViewCollection(views: _views.values.toList(growable: false));
  }
}
```
