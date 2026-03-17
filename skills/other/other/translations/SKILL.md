---
name: translations
description: Translation and localization conventions for Laravel. Use when adding user-facing strings, creating translation files, or working with lang/ directory.
---

**Name:** Translations
**Description:** Translation and localization conventions for Laravel. Use when adding user-facing strings, creating translation files, or working with lang/ directory.
**Compatible Agents:** general-purpose, frontend, backend
**Tags:** lang/**/*.php, lang/**/*.json, resources/views/**/*.blade.php, app/**/*.php, translations, localization, i18n

## Rules

- Never hardcode user-facing text — always use `__()` or `@lang()`
- This project supports **English (`en`)** and **German (`de`)** — add keys to both locales when creating new translations
- Use **namespaced keys** (`lang/{locale}/{group}.php`) for domain-specific terms (e.g. `sprints.`, `organizations.`)
- Use **JSON keys** (`lang/{locale}.json`) for generic UI labels (Save, Back, Cancel, etc.)
- Use `:placeholder` for dynamic values in translation strings
- Case matters — `Organizations.foo` is not the same as `organizations.foo`
- Run translation tests after changes: `php artisan test --filter=MissingTranslation`
- Automated detection: `MissingTranslationTest.php` scans for `__()`, `trans()`, and `@lang()` and verifies every key exists in every locale

## Examples

```php
// lang/en/sprints.php — namespaced keys for domain-specific strings
return [
    'step_locked' => 'This step is locked.',
    'create_success' => 'Sprint :name was created successfully.',
];

// Usage
__('sprints.step_locked');
__('sprints.create_success', ['name' => $sprint->name]);
```

```json
// lang/de.json — generic UI labels
{
    "Save": "Speichern",
    "Back": "Zurück",
    "Cancel": "Abbrechen"
}

// Usage
__('Save');
__('Back');
```

```blade
{{-- In Blade templates — always use translation helpers --}}
<button type="submit">{{ __('Save') }}</button>
<p>{{ __('sprints.step_locked') }}</p>
<p>{{ __('Configure the :provider API key.', ['provider' => $provider]) }}</p>
```

```php
// In PHP — use trans() or __()
throw new ValidationException(__('validation.required', ['attribute' => 'email']));
Log::info(__('sprints.import_started', ['count' => $count]));
```

## Anti-Patterns

- Hardcoding user-facing strings like `'Save'` or `'This step is locked.'` directly in views or PHP
- Adding a translation key to only one locale (en or de)
- Using namespaced keys for generic labels — use JSON for Save, Back, Cancel
- Using JSON keys for domain-specific terminology — use PHP files with namespaces
- Forgetting `:placeholder` syntax for dynamic values: `__('Welcome, :name')` with `['name' => $user->name]`
- Assuming case-insensitive key lookup — keys are case-sensitive
- Not running `php artisan test --filter=MissingTranslation` after adding or changing translations

## References

- [Laravel Localization](https://laravel.com/docs/localization)
- [Translation Helper](https://laravel.com/docs/helpers#method-__)
- Related: `Blade/SKILL.md` — use `__()` in Blade for all user-facing text
- Related: `PHPUnit/SKILL.md` — MissingTranslationTest validates translation coverage
