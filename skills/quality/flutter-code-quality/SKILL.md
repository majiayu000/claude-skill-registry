---
description: "Flutter code quality: linting, DCM, analysis_options.yaml, static analysis. Use when setting up code standards or fixing analysis warnings."
version: "1.0.0"
updated: "2026-01-07"
---

# Flutter Code Quality

Comprehensive guide for maintaining code quality in Flutter through linting and static analysis.

## Quick Reference

```bash
flutter analyze --no-fatal-infos
dart format --set-exit-if-changed lib test
dart run build_runner build --delete-conflicting-outputs
```

## analysis_options.yaml

```yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
    - "lib/core/generated/**"
  language:
    strict-casts: true
    strict-inference: true

linter:
  rules:
    # Error Prevention
    avoid_print: true
    cancel_subscriptions: true
    close_sinks: true
    prefer_const_constructors: true
    prefer_final_fields: true
    unawaited_futures: true

    # Style
    always_declare_return_types: true
    prefer_single_quotes: true
    require_trailing_commas: true
```

## Common Fixes

### prefer_const_constructors
```dart
// BAD
Text('Hello')
// GOOD
const Text('Hello')
```

### cancel_subscriptions
```dart
@override
void dispose() {
  _subscription.cancel();
  super.dispose();
}
```

### unawaited_futures
```dart
// Explicit fire-and-forget
unawaited(fetchData());
```

## Related Skills
- **flutter-development**: General patterns
- **flutter-testing**: Test patterns
