---
name: helperfunctions
description: Always prefer Laravel's built-in helper classes over native PHP functions. Use `Arr::`, `Str::`, and Collection methods instead of native PHP equivalents.
---

**Name:** Laravel Helper Functions
**Description:** Always prefer Laravel's built-in helper classes over native PHP functions. Use `Arr::`, `Str::`, and Collection methods instead of native PHP equivalents.
**Compatible Agents:** general-purpose, backend
**Tags:** app/**/*.php, laravel, php, backend, helpers, arr, str, collection

## Rules

- Always prefer Laravel's built-in helper classes over native PHP functions
- **Arrays**: Use `Arr::` (import `Illuminate\Support\Arr`) — never use `array_map`, `array_filter`, `in_array`, `array_key_exists`, etc. when a Laravel equivalent exists
- **Strings**: Use `Str::` (import `Illuminate\Support\Str`) — never use `substr`, `strpos`, `str_replace`, `strtolower`, etc. when a Laravel equivalent exists
- **Collections**: Prefer `collect()` + Collection methods over manual array loops
- Use `Str::of()` for chaining multiple string operations
- Use `collect()` to wrap any array or iterable when performing multiple operations

## Examples

```php
// Arrays
use Illuminate\Support\Arr;

// ✓ Dot-notation access
Arr::get($array, 'user.address.city', 'Unknown');
// ❌ $array['user']['address']['city'] ?? 'Unknown'

// ✓ Keep only specific keys
Arr::only($array, ['name', 'email']);
// ❌ array_intersect_key(...)

// ✓ Remove specific keys
Arr::except($array, ['password', 'token']);
// ❌ unset($array['key'])

// ✓ Map values
Arr::map($array, fn($value) => strtoupper($value));
// ❌ array_map(fn($v) => strtoupper($v), $array)
```

```php
// Strings
use Illuminate\Support\Str;

Str::upper('hello');        // ❌ strtoupper('hello')
Str::lower('HELLO');        // ❌ strtolower('HELLO')
Str::slug('Hello World');   // ❌ strtolower(str_replace(' ', '-', $string))
Str::contains('foo bar', 'foo'); // ❌ str_contains()
Str::random(32);            // ❌ bin2hex(random_bytes(16))

// Fluent chaining
$result = Str::of('  Hello World  ')
    ->trim()
    ->lower()
    ->slug();
```

```php
// Collections
$users = collect(User::all());

// ✓ Prefer collection methods
$admins = $users->filter(fn($u) => $u->isAdmin())->values();
$names  = $users->pluck('name');
$byRole = $users->groupBy('role');

// ❌ manual foreach loops
```

**Quick Reference: PHP → Laravel**

| PHP native | Laravel equivalent |
|---|---|
| `array_map($fn, $arr)` | `Arr::map($arr, $fn)` |
| `array_filter($arr, $fn)` | `Arr::where($arr, $fn)` |
| `array_key_exists($k, $arr)` | `Arr::exists($arr, $k)` |
| `in_array($v, $arr)` | `collect($arr)->contains($v)` |
| `strtolower($str)` | `Str::lower($str)` |
| `strtoupper($str)` | `Str::upper($str)` |
| `str_contains($str, $sub)` | `Str::contains($str, $sub)` |
| `http_build_query($arr)` | `Arr::query($arr)` |

## Anti-Patterns

- Using `array_map`, `array_filter`, `array_key_exists` when `Arr::` equivalents exist
- Using `strtolower`, `strtoupper`, `str_replace` when `Str::` equivalents exist
- Writing manual `foreach` loops when a Collection method achieves the same result
- Not importing `Arr` or `Str` before use — always add the `use` statement

## References

- [Laravel Arr Helper](https://laravel.com/docs/helpers#arrays)
- [Laravel Str Helper](https://laravel.com/docs/helpers#strings)
- [Laravel Collections](https://laravel.com/docs/collections)
