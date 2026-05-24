---
name: Dart Tooling & CI
description: Standards for analysis, linting, formatting, and automation.
metadata:
  labels: [tooling, linting, automation]
  triggers:
    files: ['analysis_options.yaml', 'pubspec.yaml', 'build.yaml']
    keywords: [analysis_options, lints, format, build_runner, cider, husky]
---

# Tooling & CI

## **Priority: P1 (HIGH)**

Standards for code quality, formatting, and generation.

## Implementation Guidelines

- **Linter**: Use `analysis_options.yaml`. Enforce `always_use_package_imports` and `require_trailing_commas`.
- **Formatting**: Use `dart format . --line-length 80`. Run on every commit.
- **DCM**: Use `dart_code_metrics` for complexity checks (Max cyclomatic complexity: 15).
- **Build Runner**: Always use `--delete-conflicting-outputs` with code generation.
- **CI Pipeline**: All PRs MUST pass `analyze`, `format`, and `test` steps.
- **Imports**: Group imports: `dart:`, `package:`, then relative.
- **Documentation**: Use `///` for public APIs. Link symbols using `[Class]`.
- **Linting Commands**:
  - `flutter analyze --fatal-infos --fatal-warnings`
  - `dart run dart_code_metrics:metrics analyze lib`
- **Pre-commit**: Keep `lefthook.yml` in sync with analyze/format/metrics commands.

## Code

```yaml
# analysis_options.yaml
analyzer:
  errors:
    todo: ignore
    missing_required_param: error
linter:
  rules:
    - prefer_single_quotes
    - unawaited_futures
```

## Related Topics

language | testing
