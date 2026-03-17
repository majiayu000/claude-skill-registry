---
name: iOS Localization & Assets
description: Standards for String Catalogs, L10n, and Asset Management.
metadata:
  labels: [ios, localization, l10n, assets, xcassets]
  triggers:
    files: ['**/*.stringcatalog', '**/*.xcassets', '**/*.strings']
    keywords: [LocalizedStringResource, NSLocalizedString, String(localized:)]
---

# iOS Localization & Assets Standards

## **Priority: P1**

## Implementation Guidelines

### Localization (L10n)

- **String Catalogs (.stringcatalog)**: Use for primary localization in Xcode 15+. It provides a visual editor and compile-time checks for missing translations.
- **Native Implementation**: Use `String(localized: "key")` or `LocalizedStringResource`. Avoid manual `NSLocalizedString` where possible.
- **Pluralization**: Use String Catalogs' built-in pluralization support instead of complex code logic.
- **Formatting**: Use `Formatted` API for dates, numbers, and currencies to respect the user's locale.

### Asset Management

- **Asset Catalogs (.xcassets)**: Keep assets organized. Use folders with "Provides Namespace" enabled for large projects.
- **SF Symbols**: Use for standard icons to ensure consistency and accessibility.
- **Vector Assets**: Use PDF or SVG and enable "Preserve Vector Data" for resolution independence.

### Best Practices

- **Hardcoded Strings**: Never use hardcoded strings in UI. Every user-facing string must be localized.
- **Base Bundle**: Ensure `Base` localization is complete before adding other languages.

## Anti-Patterns

- **Manual String Formatting**: `**No manual currency symbol concat**: Use NumberFormatter or .formatted(.currency).`
- **Loose Asset Files**: `**No loose png/jpg files in repo**: Always use Asset Catalogs.`
- **Untranslated Keys**: `**No placeholder strings**: Ensure 100% coverage in String Catalogs.`

## References

- [L10n & Asset Organization](references/implementation.md)
