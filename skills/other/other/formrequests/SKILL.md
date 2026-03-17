---
name: formrequests
description: Dedicated validation classes for all controller input. Form Requests encapsulate validation rules, authorization, and error messages outside of controllers.
---

**Name:** Form Requests
**Description:** Dedicated validation classes for all controller input. Form Requests encapsulate validation rules, authorization, and error messages outside of controllers.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Http/Requests/**/*.php, app/Http/Controllers/**/*.php, laravel, php, backend, validation, form-request

## Rules

- Every controller action that accepts user input **must** use a dedicated `FormRequest` class
- Never call `$request->validate()` or `Validator::make()` inside a controller
- Place Form Requests in `app/Http/Requests/` or a subdirectory matching the domain (e.g. `Auth/`)
- Naming pattern: `Store{Resource}Request`, `Update{Resource}Request`
- Match the resource name to the controller: `StoreSprintController` → `StoreSprintRequest`
- Define `authorize(): bool` with proper authorization logic — never leave it as a passive `return true` without intention
- Define `rules(): array` with a PHPDoc `@return` array shape
- Use **array-based** rule definitions, not pipe-delimited strings
- Add `messages(): array` when validation messages need localization or extra clarity

## Examples

```php
class StoreSprintRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user() !== null;
    }

    /**
     * @return array<string, array<int, string|object>>
     */
    public function rules(): array
    {
        return [
            'title'  => ['required', 'string', 'max:255'],
            'locale' => ['required', Locale::validationRule()],
        ];
    }

    public function messages(): array
    {
        return [
            'title.required' => __('A title is required.'),
        ];
    }
}
```

```php
// Controller usage — inject the FormRequest
class StoreSprintController extends Controller
{
    public function __invoke(StoreSprintRequest $request, CreateSprint $action): JsonResponse
    {
        $sprint = $action->execute($request->validated());

        return new JsonResponse(new SprintResource($sprint), 201);
    }
}
```

```php
// Authorization using a policy
public function authorize(): bool
{
    return $this->user()->can('create', Post::class);
}

// Scoped to an admin role
public function authorize(): bool
{
    return $this->user()->isAdmin();
}
```

## Anti-Patterns

- Calling `$request->validate()` inside a controller — always use a FormRequest
- Using pipe-delimited rule strings: `'required|string|max:255'` instead of `['required', 'string', 'max:255']`
- Leaving `authorize()` as `return true` without documenting why all users are permitted
- Not adding a `messages()` method for user-facing validation errors that need clarity

## References

- [Laravel Form Requests](https://laravel.com/docs/validation#form-request-validation)
- Related: `Controllers/SKILL.md` — controllers that use Form Requests
- Related: `Policies/SKILL.md` — `can()` used in `authorize()` method
