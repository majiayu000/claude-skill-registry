---
name: angular-i18n-maintenance
description: Maintain runtime i18n in Angular apps using `@ngx-translate/core` by replacing new hardcoded UI text with translation keys, `TranslatePipe`, and synchronized entries in all locale JSON files. Use when adding labels, headings, buttons, messages, placeholders, or titles in projects that already use JSON locale files.
---

# Angular i18n Maintenance

Keep new user-facing text translatable in Angular projects that already run runtime i18n with `@ngx-translate/core`.

## Purpose and Trigger Conditions

Apply this skill when all are true:
- The project already uses runtime translation (`@ngx-translate/core`, `TranslatePipe`, locale JSON files).
- New user-facing copy is being introduced or changed.
- The copy appears in templates or translated attribute bindings.

Do not use this skill to bootstrap i18n from scratch.

## Mandatory Preflight

1. Confirm runtime i18n is present:
   - Find `@ngx-translate/core` usage and `TranslatePipe`/`TranslateModule` usage.
2. Discover locale file set:
   - Identify the locale directory and all locale JSON files (for example `public/i18n/*.json` or `assets/i18n/*.json`).
3. Detect key style from existing files:
   - Flat keys (`"dashboard.title": "..."`) or nested keys (`"dashboard": { "title": "..." }`).
4. Determine default/reference locale:
   - Usually `en.json`; otherwise use the project’s configured default locale.

If any preflight step fails, stop and report the blocker before editing content.

## Deterministic Workflow

1. Define the translation key
- Create one stable key for each new phrase using existing project naming patterns.
- Prefer dot notation style consistent with the repository.
- Do not split one phrase across multiple keys unless the project already does so for that exact case.

2. Replace hardcoded template text
- Static text: `{{ 'feature.section.label' | translate }}`
- Interpolated text: `{{ 'feature.section.message' | translate:{ name: user.name } }}`
- Attribute binding: `[placeholder]="'common.search' | translate"`, `[title]="'common.info' | translate"`

3. Add the key to locale files
- Add the same key path to every locale JSON file discovered in preflight.
- Use the default locale wording as the source value.
- For locales without confirmed translation, temporarily copy default-locale text and record a follow-up outside JSON.

4. Preserve file conventions
- Keep the project’s existing key structure (flat or nested).
- Keep valid JSON syntax and formatting conventions.

## Verification Checklist

- [ ] New key follows existing naming/style conventions.
- [ ] Template/attribute no longer contains newly introduced hardcoded user-facing text.
- [ ] Key exists in every locale JSON file.
- [ ] Interpolation parameter names are consistent across locales.
- [ ] Locale files remain valid JSON.
- [ ] Unrelated locale entries are unchanged.

## Failure Handling

- Missing locale files: stop and report missing files; request explicit file creation path.
- Mixed key conventions in same locale set: follow dominant convention and note inconsistency.
- Malformed locale JSON: stop and report exact file and parse issue; do not rewrite blindly.
- Non-static/dynamic content request: do not force key extraction if text is runtime-generated data.

## References

- Practical patterns and detection rules: [reference.md](reference.md)
- Before/after snippets: [examples.md](examples.md)
