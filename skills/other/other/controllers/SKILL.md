---
name: controllers
description: Thin HTTP entry points that validate input, delegate to Actions or Services, and return a response. Controllers contain no business logic.
---

**Name:** Controllers
**Description:** Thin HTTP entry points that validate input, delegate to Actions or Services, and return a response. Controllers contain no business logic.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Http/Controllers/**/*.php, laravel, php, backend, controller, http, request-response

## Rules

- Keep controllers **thin** — delegate business logic to Services, Actions, or Jobs
- Controllers handle: request validation, calling a service/job, returning a response
- No direct database queries or complex logic in controller methods
- Use dedicated `FormRequest` classes for all validation — never call `$request->validate()` or `Validator::make()` inside a controller
- Use invokable controllers (`__invoke`) for single-action endpoints
- Name invokable controllers after the action: `StoreInvoiceController`, `ProcessWebhookController`
- Return JSON responses from API controllers
- Return views from web controllers
- Use appropriate HTTP status codes (200, 201, 422, 403, etc.)
- Enforce authorization at the controller level using `$this->authorize()`, via Form Request `authorize()`, or route middleware

## Examples

```php
// Invokable single-action controller
class StoreInvoiceController extends Controller
{
    public function __invoke(StoreInvoiceRequest $request, CreateInvoice $action): JsonResponse
    {
        $order = Order::findOrFail($request->validated('order_id'));
        $invoice = $action->execute($order);

        return new JsonResponse(new InvoiceResource($invoice), 201);
    }
}
```

```php
// Resource controller — thin, delegates to actions
class InvoiceController extends Controller
{
    public function index(): JsonResponse
    {
        return new JsonResponse(InvoiceResource::collection(Invoice::paginate()));
    }

    public function store(StoreInvoiceRequest $request, CreateInvoice $action): JsonResponse
    {
        $this->authorize('create', Invoice::class);

        $order = Order::findOrFail($request->validated('order_id'));
        $invoice = $action->execute($order);

        return new JsonResponse(new InvoiceResource($invoice), 201);
    }

    public function destroy(Invoice $invoice, DeleteInvoice $action): JsonResponse
    {
        $this->authorize('delete', $invoice);
        $action->execute($invoice);

        return new JsonResponse(null, 204);
    }
}
```

## Anti-Patterns

- Calling `$request->validate()` directly in a controller (use a FormRequest)
- Writing database queries directly in a controller
- Putting business logic in a controller method
- Using resource controllers with 7 methods when only 1-2 are needed (use invokable controllers)
- Not using appropriate HTTP status codes in responses
- Performing authorization inside Actions instead of at the controller level

## References

- [Laravel Controllers](https://laravel.com/docs/controllers)
- Related: `FormRequests/SKILL.md` — all input validation
- Related: `Actions/SKILL.md` — the business logic controllers delegate to
- Related: `Policies/SKILL.md` — authorization enforced in controllers
