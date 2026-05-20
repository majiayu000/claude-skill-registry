---
name: project-plugin
description: Guide for creating native plugins in app_plugin with platform-specific implementations (project)
---

# Flutter Plugin Development Skill

This skill guides the creation of native plugins following this project's architecture.

## When to Use

Trigger this skill when:
- Creating a native plugin with platform-specific code
- Adding new platform support to an existing plugin
- User asks to "create a plugin", "add native functionality", or "implement platform-specific feature"

## Plugin Types

This project supports two plugin architectures:

| Type | Use Case | Complexity |
|------|----------|------------|
| **native_plugin** (Recommended) | Single package with all platform code | Simple |
| **native_federation_plugin** | Separate packages per platform | Complex, for public distribution |

**Default to `native_plugin`** unless the user specifically requests federation or needs to publish platform implementations as separate packages.

## Mason Templates

### Simple Plugin (Recommended)

```bash
mason make native_plugin \
  --name plugin_name \
  --description "Plugin description" \
  --package_prefix app \
  -o app_plugin

# Platform support options (all default to true):
# --support_android
# --support_ios
# --support_linux
# --support_macos
# --support_windows
# --support_web (default: false)
```

**Structure:**
```
app_plugin/
└── plugin_name/                    # Single package
    ├── lib/                        # Dart API
    ├── android/                    # Android (Kotlin)
    ├── ios/                        # iOS (Swift)
    ├── linux/                      # Linux (C++)
    ├── macos/                      # macOS (Swift)
    ├── windows/                    # Windows (C++)
    └── pubspec.yaml
```

### Federated Plugin (When User Specifies)

Use `native_federation_plugin` when:
- Publishing to pub.dev with separate platform packages
- Different teams maintain different platforms
- Need to allow third-party platform implementations

```bash
mason make native_federation_plugin \
  --name plugin_name \
  --description "Plugin description" \
  --package_prefix app \
  -o app_plugin
```

**Structure:**
```
app_plugin/
└── plugin_name/                            # Parent directory
    ├── plugin_name/                        # Main package (API)
    ├── plugin_name_platform_interface/     # Abstract interface
    ├── plugin_name_android/                # Android implementation
    ├── plugin_name_ios/                    # iOS implementation
    ├── plugin_name_linux/                  # Linux implementation
    ├── plugin_name_macos/                  # macOS implementation
    └── plugin_name_windows/                # Windows implementation
```

## Workspace Registration

### Simple Plugin

```yaml
workspace:
  - app_plugin/plugin_name
```

### Federated Plugin

```yaml
workspace:
  - app_plugin/plugin_name/plugin_name
  - app_plugin/plugin_name/plugin_name_platform_interface
  - app_plugin/plugin_name/plugin_name_android
  - app_plugin/plugin_name/plugin_name_ios
  - app_plugin/plugin_name/plugin_name_linux
  - app_plugin/plugin_name/plugin_name_macos
  - app_plugin/plugin_name/plugin_name_windows
```

## Plugin Implementation

### Dart API (lib/src/plugin_name.dart)
```dart
class PluginName {
  static final PluginName _instance = PluginName._();
  static PluginName get instance => _instance;

  static const MethodChannel _channel = MethodChannel('app_plugin_name');

  Future<PluginData> getData() async {
    final result = await _channel.invokeMethod<Map>('getData');
    return PluginData.fromMap(result ?? {});
  }
}
```

### Native Implementation (Example: Kotlin/Android)
```kotlin
class PluginNamePlugin: FlutterPlugin, MethodCallHandler {
    private lateinit var channel: MethodChannel

    override fun onAttachedToEngine(binding: FlutterPlugin.FlutterPluginBinding) {
        channel = MethodChannel(binding.binaryMessenger, "app_plugin_name")
        channel.setMethodCallHandler(this)
    }

    override fun onMethodCall(call: MethodCall, result: Result) {
        when (call.method) {
            "getData" -> result.success(mapOf("platform" to "android"))
            else -> result.notImplemented()
        }
    }
}
```

## Testing

```bash
# Test plugin
cd app_plugin/plugin_name && flutter test

# For federated plugins
cd app_plugin/plugin_name/plugin_name && flutter test
```

## Reference Implementation

`app_client_info` in `app_plugin/client_info/` demonstrates the federated pattern.

## Usage in App

```dart
import 'package:app_plugin_name/app_plugin_name.dart';

final plugin = PluginName.instance;
final data = await plugin.getData();
```
