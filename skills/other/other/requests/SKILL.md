---
name: requests
description: Dedicated Form Request validation classes for all controller input. Every endpoint that accepts user input must use a `FormRequest` class — validation never happens directly inside a controller.
---

**Name:** Form Request Validation
**Description:** Dedicated Form Request validation classes for all controller input. Every endpoint that accepts user input must use a `FormRequest` class — validation never happens directly inside a controller.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Http/Requests/**/*.php, laravel, php, backend, validation, request, form-request

## Rules

- Every controller action that accepts user input **must** use a dedicated `FormRequest` class
- Never call `$request->validate()` or `Validator::make()` inside a controller
- Place Form Requests in `app/Http/Requests/` or a subdirectory matching the domain (e.g. `Auth/`)
- Naming: `Store{Resource}Request`, `Update{Resource}Request`
- Define `authorize(): bool` with intentional access control
- Define `rules(): array` with a PHPDoc `@return` array shape annotation
- Use **array-based** rule definitions — not pipe-delimited strings
- Override `messages(): array` for user-friendly or localized error messages

## Examples

```php
class StoreInvoiceRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Invoice::class);
    }

    /**
     * @return array<string, array<int, string|object>>
     */
    public function rules(): array
    {
        return [
            'order_id' => ['required', 'integer', 'exists:orders,id'],
            'due_date' => ['required', 'date', 'after:today'],
            'notes'    => ['nullable', 'string', 'max:1000'],
        ];
    }

    public function messages(): array
    {
        return [
            'order_id.exists'  => __('The selected order does not exist.'),
            'due_date.after'   => __('The due date must be a future date.'),
        ];
    }
}
```

```php
// Custom authorization logic options
public function authorize(): bool
{
    // Allow all authenticated users
    return $this->user() !== null;

    // Scope to admin role
    return $this->user()->isAdmin();

    // Delegate to a policy
    return $this->user()->can('update', $this->route('invoice'));
}
```

## Anti-Patterns

- Using `$request->validate([...])` inside a controller
- Using pipe-delimited rules: `'required|string|max:255'` instead of `['required', 'string', 'max:255']`
- Leaving `authorize()` as a passive `return true` without a comment explaining intent
- Not using a `messages()` method when default Laravel messages are unclear to end users
- Skipping the `@return` PHPDoc annotation on `rules()` (breaks PHPStan analysis)

## References

- [Laravel Form Requests](https://laravel.com/docs/validation#form-request-validation)
- Related: `Controllers/SKILL.md` — controllers that inject and use Form Requests
- Related: `Policies/SKILL.md` — policies referenced in `authorize()`
