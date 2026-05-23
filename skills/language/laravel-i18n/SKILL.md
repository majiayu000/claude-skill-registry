---
name: laravel-i18n
description: Laravel localization - __(), trans_choice(), lang files, JSON translations, pluralization. Use when implementing translations in Laravel apps.
user-invocable: false
---

# Laravel Internationalization

## Setup

```bash
php artisan lang:publish
```

Creates `lang/` directory with default language files.

---

## File Structure

```text
lang/
├── en/
│   ├── messages.php      # Short keys
│   └── validation.php
├── fr/
│   ├── messages.php
│   └── validation.php
├── en.json               # Full text keys
└── fr.json
```

---

## Configuration

```php
// config/app.php
'locale' => env('APP_LOCALE', 'en'),
'fallback_locale' => env('APP_FALLBACK_LOCALE', 'en'),
```

---

## Translation Helpers

```php
// Basic translation
__('messages.welcome')

// With replacement
__('Hello :name', ['name' => 'John'])

// JSON approach (full text as key)
__('Welcome to our application')

// Alias
trans('messages.welcome')
```

---

## PHP Translation Files

```php
// lang/en/messages.php
return [
    'welcome' => 'Welcome to our application',
    'hello' => 'Hello :name',
    'goodbye' => 'Goodbye :name, see you :time',
];
```

---

## JSON Translation Files

```json
// lang/fr.json
{
    "Welcome to our application": "Bienvenue sur notre application",
    "Hello :name": "Bonjour :name"
}
```

---

## Pluralization

```php
// lang/en/messages.php
'apples' => '{0} No apples|{1} One apple|[2,*] :count apples',
```

```php
trans_choice('messages.apples', 0);  // "No apples"
trans_choice('messages.apples', 1);  // "One apple"
trans_choice('messages.apples', 5);  // "5 apples"
```

---

## Runtime Locale

```php
use Illuminate\Support\Facades\App;

// Set locale
App::setLocale('fr');

// Get current locale
$locale = App::currentLocale();

// Check locale
if (App::isLocale('fr')) {
    // ...
}
```

---

## Middleware Example

```php
// app/Http/Middleware/SetLocale.php
public function handle(Request $request, Closure $next): Response
{
    $locale = $request->segment(1);

    if (in_array($locale, ['en', 'fr', 'de'])) {
        App::setLocale($locale);
    }

    return $next($request);
}
```

---

## Blade Usage

```blade
{{ __('messages.welcome') }}
@lang('messages.welcome')
{{ trans_choice('messages.apples', 5) }}
```

---

## Best Practices

1. **Use JSON files** for large apps with many strings
2. **PHP files** for structured, nested translations
3. **Always use placeholders** `:name` not concatenation
4. **Group by feature** in namespaces: `auth.login.title`
