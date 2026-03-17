---
name: Android Tooling & Linting
description: Standards for Static Analysis (Detekt, Ktlint) and CI/CD Checks
metadata:
  labels: [android, tooling, lint, detekt]
  triggers:
    files: ['build.gradle.kts', 'detekt.yml']
    keywords: ['detekt', 'ktlint', 'lint']
---

# Android Tooling Standards

## **Priority: P1**

## Implementation Guidelines

### Static Analysis

- **Detekt**: Enforce code complexity rules (LongMethod, LargeClass). Fail build on high complexity.
- **Ktlint**: Enforce formatting style (Indent, Spacing). Use `jlleitschuh` plugin.
- **Android Lint**: Treat warnings as errors in CI (`abortOnError = true`).

### CI Gates

- **Pre-commit**: Run lightweight checks (formatting) locally.
- **Pipeline**: Run full checks (Detekt + Lint + Unit Tests) on Pull Request.

## Anti-Patterns

- **Suppress**: `**No @Suppress**: Fix the root cause.`
- **Manual Formatting**: `**No Manual Format**: Auto-format on save.`

## References

- [Configuration](references/implementation.md)
