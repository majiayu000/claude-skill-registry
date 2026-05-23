---
name: policies
description: Centralised authorization logic for a given Eloquent model. Policies define per-ability access control and are enforced at the controller level.
---

**Name:** Policies
**Description:** Centralised authorization logic for a given Eloquent model. Policies define per-ability access control and are enforced at the controller level.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Policies/**/*.php, laravel, php, backend, policy, authorization, auth

## Rules

- Policy classes live in `app/Policies/`
- Naming: `PascalCase` with a `Policy` suffix, named after the model they protect: `InvoicePolicy`, `PostPolicy`
- Policies centralise **all authorization logic** for a given model in one place
- Create one policy for **each** model
- Define one method per ability — use standard names: `viewAny`, `view`, `create`, `update`, `delete`, `restore`, `forceDelete`
- Always enforce authorization at the **controller** level — never inside actions or services
- Laravel auto-discovers policies that follow the `ModelPolicy` naming convention
- For custom locations, register manually in `AuthServiceProvider`

## Examples

```php
namespace App\Policies;

use App\Models\Invoice;
use App\Models\User;

class InvoicePolicy
{
    public function viewAny(User $user): bool
    {
        return $user->isAdmin();
    }

    public function view(User $user, Invoice $invoice): bool
    {
        return $user->id === $invoice->user_id || $user->isAdmin();
    }

    public function create(User $user): bool
    {
        return $user->hasVerifiedEmail();
    }

    public function update(User $user, Invoice $invoice): bool
    {
        return $user->id === $invoice->user_id && $invoice->isDraft();
    }

    public function delete(User $user, Invoice $invoice): bool
    {
        return $user->isAdmin();
    }
}
```

```php
// Usage in controller
public function update(UpdateInvoiceRequest $request, Invoice $invoice): InvoiceResource
{
    $this->authorize('update', $invoice);
    // ...
}

// Usage in Form Request
public function authorize(): bool
{
    return $this->user()->can('update', $this->route('invoice'));
}

// Usage via route middleware
Route::put('/invoices/{invoice}', [InvoiceController::class, 'update'])
    ->middleware('can:update,invoice');
```

## Anti-Patterns

- Putting authorization logic directly in controllers, actions, or models
- Creating global gates instead of model-specific policies when model-based auth is appropriate
- Not creating a policy for each model
- Putting business logic inside a policy method (belongs in Actions or Services)
- Using `return true` in `authorize()` without documenting the intent

## References

- [Laravel Authorization](https://laravel.com/docs/authorization)
- Related: `Controllers/SKILL.md` — the layer where policies are enforced
- Related: `FormRequests/SKILL.md` — can use `can()` in `authorize()` method
