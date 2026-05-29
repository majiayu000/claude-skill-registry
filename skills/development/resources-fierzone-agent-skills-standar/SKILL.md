---
name: Android Resources & Localization
description: Standards for Strings, Drawables, and Localization
metadata:
  labels: [android, resources, localization, xml]
  triggers:
    files: ['strings.xml', '**/*Screen.kt']
    keywords: ['stringResource', 'plurals', 'R.string']
---

# Android Resources Standards

## **Priority: P2**

## Implementation Guidelines

### Strings

- **No Hardcoding**: UI text MUST be in `strings.xml`.
- **Formatting**: Use format args (`%s`, `%d`) instead of concatenation.
- **Plurals**: Use `<plurals>` for quantities.

### Assets / Drawables

- **Vectors**: Prefer VectorDrawables (`.xml`) over RASTER images.
- **Dark Mode**: Use `values-night` or Theme attributes (`MaterialTheme.colorScheme.primary`) instead of hardcoded colors.

## Anti-Patterns

- **Concatenation in UI**: `**No String Concat**: Use resource templates.`
- **Hardcoded Strings**: `**No hardcoded text**: Extract to XML.`

## References

- [XML Structure](references/implementation.md)
