---
name: Dart Best Practices
description: General purity standards for Dart development.
metadata:
  labels: [dart, clean-code]
  triggers:
    files: ['**/*.dart']
    keywords: [import, final, const, var, global]
---

# Dart Best Practices

## **Priority: P1 (OPERATIONAL)**

Best practices for writing clean, maintainable Dart code.

- **Scoping**:
  - No global variables.
  - Private globals (if required) must start with `_`.
- **Immutability**: Use `const` > `final` > `var`.
- **Config**: Use `--dart-define` for secrets. Never hardcode API keys.
- **Naming**: Follow [effective-dart](https://dart.dev/guides/language/effective-dart) (PascalCase classes, camelCase members).
- **Strings**: Prefer single quotes; use double quotes only for interpolation needs.
- **Trailing Commas**: Always use trailing commas for multi-line literals/params.
- **Expression Bodies**: Prefer `=>` for single-expression functions/getters.
- **Collections**:
  - Use `.map`, `.where`, `.fold`, `.any` over manual loops when clarity improves.
  - Type empty collections (`<String>[]`, `<String, User>{}`) to avoid `dynamic`.
  - Use collection `if`/`for` and spread operators for composable lists/maps.
- **Async**: Always `await` futures unless intentionally fire-and-forget.

```dart
import 'models/user.dart'; // Good
import 'package:app/models/user.dart'; // Avoid local absolute
```
