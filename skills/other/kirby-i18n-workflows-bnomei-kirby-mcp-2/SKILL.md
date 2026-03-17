---
name: kirby-i18n-workflows
description: Manages Kirby multi-language workflows, translations, and localized labels. Use when dealing with languages, translation keys, placeholders, or importing/exporting translations.
---

# Kirby i18n Workflows

## KB entry points

- `kirby://kb/scenarios/46-i18n-field-options-and-labels`
- `kirby://kb/scenarios/47-i18n-find-translation-keys`
- `kirby://kb/scenarios/48-i18n-import-export-translations`
- `kirby://kb/scenarios/72-filter-by-language`
- `kirby://kb/scenarios/73-language-variables-and-placeholders`

## Required inputs

- Enabled languages and default language.
- Where translation keys live and desired naming scheme.
- Which content is translated vs label-only.

## Default translation rule

- Use `t('key', 'fallback')` in templates and snippets.
- Keep stored content language-neutral when possible; translate labels at render time.
- Maintain fallback strings in the default language file.

## Import/export hint

```php
return [
  'site.title' => 'Example',
];
```

## Missing key audit

- Run `rg -F 't(' site` and compare keys with `site/languages/*.php`.
- Add missing keys to the default language file first.

## Common pitfalls

- Storing translated labels in content instead of language files.
- Using translation keys without fallback strings.

## Workflow

1. Confirm language setup with `kirby://config/languages` and locate language files via `kirby://roots`.
2. Inspect templates/snippets/controllers for translation usage; use `rg` to find `t(` calls if needed.
3. Search the KB with `kirby:kirby_search` (examples: "translate field options", "find translation keys", "import export translations", "language variables placeholders").
4. Update language files (`site/languages/*.php`) or config maps for option labels.
5. Ensure templates render translated labels (not stored keys) and use fallbacks.
6. Verify by rendering representative pages in each language (`kirby:kirby_render_page`).
