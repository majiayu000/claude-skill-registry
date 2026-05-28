---
name: flutter-obfuscate-docs
description: "[Flutter] Flutter code obfuscation guide. Build commands, symbol files, stack trace deobfuscation, and limitations. (project)"
---

# Flutter Code Obfuscation

## What is Obfuscation?

Replaces function/class names with obscure symbols to make reverse engineering harder.

**Warning:** Obfuscation only renames symbols - it does NOT encrypt resources or provide strong security. Never store secrets in the app.

---

## Supported Platforms

| Platform | Build Targets |
|----------|---------------|
| Android | `aar`, `apk`, `appbundle` |
| iOS | `ios`, `ios-framework`, `ipa` |
| Desktop | `linux`, `macos`, `macos-framework`, `windows` |
| Web | Not supported (uses minification instead) |

---

## Build with Obfuscation

### Basic Command
```bash
flutter build <target> \
  --obfuscate \
  --split-debug-info=<symbols-directory>
```

### Examples
```bash
# Android APK
flutter build apk --obfuscate --split-debug-info=out/android

# Android App Bundle
flutter build appbundle --obfuscate --split-debug-info=out/android

# iOS
flutter build ios --obfuscate --split-debug-info=out/ios

# iOS IPA
flutter build ipa --obfuscate --split-debug-info=out/ios

# macOS
flutter build macos --obfuscate --split-debug-info=out/macos

# Windows
flutter build windows --obfuscate --split-debug-info=out/windows

# Linux
flutter build linux --obfuscate --split-debug-info=out/linux
```

**Important:** Backup the generated symbol files!

---

## Symbol Files

Generated in `<symbols-directory>`:
```
out/android/
├── app.android-arm.symbols
├── app.android-arm64.symbols
└── app.android-x64.symbols
```

**Always backup these files** - required for crash report deobfuscation.

---

## Deobfuscate Stack Traces

### Command
```bash
flutter symbolize -i <stack-trace-file> -d <symbols-file>
```

### Example
```bash
# Save crash stack trace to file
echo "crash stack trace content" > crash.txt

# Deobfuscate
flutter symbolize -i crash.txt -d out/android/app.android-arm64.symbols
```

---

## Generate Obfuscation Map

Creates JSON mapping of original → obfuscated names:

```bash
flutter build apk \
  --obfuscate \
  --split-debug-info=out/android \
  --extra-gen-snapshot-options=--save-obfuscation-map=out/android/map.json
```

**Output (map.json):**
```json
["MaterialApp", "ex", "Scaffold", "ey", "MyWidget", "ez", ...]
```

---

## Limitations

### Code That Will Break
```dart
// BAD: Runtime type checking fails after obfuscation
expect(foo.runtimeType.toString(), equals('Foo')); // ❌

// BAD: Type name comparison
if (widget.runtimeType.toString() == 'MyWidget') { } // ❌
```

### What's NOT Obfuscated
- Enum names (remain unchanged)
- String literals
- Asset paths

---

## Quick Reference

| Task | Command |
|------|---------|
| Build obfuscated APK | `flutter build apk --obfuscate --split-debug-info=out/android` |
| Build obfuscated IPA | `flutter build ipa --obfuscate --split-debug-info=out/ios` |
| Deobfuscate crash | `flutter symbolize -i crash.txt -d app.android-arm64.symbols` |
| Generate map | Add `--extra-gen-snapshot-options=--save-obfuscation-map=map.json` |
| Check options | `flutter build <target> -h` |

---

## Workflow Summary

```
1. Build with --obfuscate --split-debug-info=<dir>
2. Backup symbol files (*.symbols)
3. Distribute obfuscated app
4. When crash occurs: flutter symbolize -i <crash> -d <symbols>
```

---

## Official Docs
- [Obfuscate Dart code](https://docs.flutter.dev/deployment/obfuscate)
