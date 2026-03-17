---
name: Flutter Localization
description: Standards for multi-language support using easy_localization with CSV or JSON.
metadata:
  labels: [localization, l10n, i18n, easy_localization, csv]
  triggers:
    files:
      ['**/assets/translations/*.json', '**/assets/langs/*.csv', 'main.dart']
    keywords:
      [
        localization,
        multi-language,
        translation,
        tr(),
        easy_localization,
        sheet_loader,
      ]
---

# Localization

## **Priority: P1 (STANDARD)**

Consistent multi-language support using `easy_localization`.

## Format Selection

- **CSV** (Recommended for teams with translators):
  - Non-technical editors can update easily
  - Native Google Sheets compatibility via `sheet_loader_localization`
  - Store in `assets/langs/` (common convention)
- **JSON** (Developer-friendly):
  - Nested structure support (e.g., `items_count.zero`)
  - IDE validation and autocomplete
  - Store in `assets/translations/`

Both formats work identically with `easy_localization`.

## Structure

```text
# CSV Format (Google Sheets workflow)
assets/langs/langs.csv

# OR JSON Format (nested keys)
assets/translations/
├── en.json
└── vi.json
```

## Implementation Guidelines

- **Bootstrap**: Wrap root with `EasyLocalization`. Always use `await EasyLocalization.ensureInitialized()`.
- **Lookup**: Use `.tr()` extension on strings (e.g., `'welcome'.tr()`).
- **Locale**: Change via `context.setLocale(Locale('code'))`.
- **Params**: Use `{}` placeholders; pass via `tr(args: [...])`.
- **Counting**: Use `plural()` for quantities.
- **Sheets Sync**: Use `sheet_loader_localization` to auto-generate CSV/JSON from Google Sheets.

## Anti-Patterns

- **Hardcoding**: No raw strings in UI; use keys.
- **Manual L10n**: Avoid standard `Localizations.of`; use GetX or `easy_localization` context methods.
- **Desync**: Keep keys identical across all locale files.

## Reference & Examples

For setup and Google Sheets automation:
See [references/REFERENCE.md](references/REFERENCE.md).

## Related Topics

idiomatic-flutter | widgets
