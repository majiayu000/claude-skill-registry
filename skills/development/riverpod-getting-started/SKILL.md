---
name: riverpod-getting-started
description: Install Riverpod (flutter_riverpod or riverpod), wrap the app in ProviderScope, run a hello-world provider, and optionally enable riverpod_lint and code generation. Use when starting a Flutter or Dart project with Riverpod, adding the Riverpod dependency, or setting up ProviderScope and a first provider. For version highlights see the official Riverpod docs.
---

# Riverpod — Getting Started

## Instructions

### Installing the package

Riverpod is available as a main package (Flutter: `flutter_riverpod`; Dart-only: `riverpod`). Optional packages add code generation and hooks.

**Flutter:**

```bash
flutter pub add flutter_riverpod
```

With code generation:

```bash
flutter pub add flutter_riverpod riverpod_annotation
flutter pub add dev:riverpod_generator build_runner
```

**Dart only:**

```bash
dart pub add riverpod
```

With code generation:

```bash
dart pub add riverpod riverpod_annotation
dart pub add dev:riverpod_generator build_runner
```

**Manual `pubspec.yaml` (Flutter):**

```yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_riverpod: ^2.0.0  # use latest from pub.dev

dev_dependencies:
  build_runner:
  riverpod_generator: ^2.0.0  # if using code generation
```

Then run `flutter pub get` (or `dart pub get` for Dart-only).

If using code generation, run:

```sh
dart run build_runner watch -d
```

**Note:** Some Riverpod packages may require Flutter's beta channel for compatibility with latest `json_serializable`. If `pub get` fails, try `flutter channel beta` or use Riverpod `<=3.1.0`.

### Wrap the app in ProviderScope

Widgets need a `ProviderScope` (Flutter) or a `ProviderContainer` (Dart) to read providers.

**Flutter — ProviderScope:**

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() {
  runApp(
    ProviderScope(
      child: MyApp(),
    ),
  );
}
```

**Dart only — ProviderContainer:**

```dart
final container = ProviderContainer();
final value = container.read(helloWorldProvider);
print(value);
// Don't forget to container.dispose() when done
```

### Hello world (Flutter with code generation)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'main.g.dart';

@riverpod
String helloWorld(Ref ref) {
  return 'Hello world';
}

void main() {
  runApp(ProviderScope(child: MyApp()));
}

class MyApp extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final String value = ref.watch(helloWorldProvider);
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('Example')),
        body: Center(child: Text(value)),
      ),
    );
  }
}
```

Run `dart run build_runner build` (or `watch`) to generate `main.g.dart`. Without code generation, use a manual provider (e.g. `final helloWorldProvider = Provider<String>((ref) => 'Hello world');`) and the same `ProviderScope` + `ConsumerWidget` pattern.

### Enabling riverpod_lint

Add the optional linter via `analysis_options.yaml`:

```yaml
plugins:
  riverpod_lint: ^2.0.0  # use latest from https://pub.dev/packages/riverpod_lint
```

This provides lint rules and refactorings for Riverpod. See the riverpod_lint package page for the full list.

### Going further

- **Code generation and hooks:** See the riverpod-codegen-and-hooks skill (or docs: About code generation, About hooks).
- **VS Code / Android Studio:** Consider Flutter Riverpod Snippets extensions for faster boilerplate.
