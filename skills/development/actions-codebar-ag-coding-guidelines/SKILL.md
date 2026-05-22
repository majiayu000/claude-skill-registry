---
name: actions
description: Single-purpose business logic classes that encapsulate one well-defined business operation. Actions are the primary location for business logic in Laravel applications, invoked from controllers, commands, or jobs.
---

**Name:** Actions
**Description:** Single-purpose business logic classes that encapsulate one well-defined business operation. Actions are the primary location for business logic in Laravel applications, invoked from controllers, commands, or jobs.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Actions/**/*.php, laravel, php, backend, business-logic, action

## Rules

- Action classes live in `app/Actions/`
- Each action represents **one single business operation** — if you can't describe it in a single sentence, split it up
- Use a clear verb-noun naming pattern: `CreateInvoice`, `SendPasswordResetEmail`, `ArchiveExpiredSubscriptions`
- Never use vague names like `InvoiceAction` or `UserHandler`
- Actions expose a single public `execute()` method
- Keep the constructor for dependency injection only
- Actions are resolved via the service container
- Never include HTTP concerns (request, response, redirects) in an action
- Never put multi-domain orchestration in an action — use a Service instead
- Never put reusable formatting or utility logic in an action — use a Helper

## Examples

```php
namespace App\Actions;

use App\Models\Invoice;
use App\Models\Order;
use App\Notifications\InvoiceCreatedNotification;

class CreateInvoice
{
    public function __construct(
        private readonly GenerateInvoicePdf $generatePdf,
    ) {}

    public function execute(Order $order): Invoice
    {
        $invoice = Invoice::create([
            'order_id' => $order->id,
            'amount'   => $order->total,
            'due_date' => now()->addDays(30),
        ]);

        $this->generatePdf->execute($invoice);

        $order->user->notify(new InvoiceCreatedNotification($invoice));

        return $invoice;
    }
}
```

```php
// Controller usage
class InvoiceController extends Controller
{
    public function store(StoreInvoiceRequest $request, CreateInvoice $action): JsonResponse
    {
        $order = Order::findOrFail($request->validated('order_id'));
        $invoice = $action->execute($order);

        return new JsonResponse(new InvoiceResource($invoice), 201);
    }
}

// Command usage
class GenerateInvoicesCommand extends Command
{
    public function handle(CreateInvoice $action): int
    {
        Order::pending()->each(fn ($order) => $action->execute($order));

        return self::SUCCESS;
    }
}
```

## Anti-Patterns

- Putting HTTP concerns (`Request`, `Response`, redirects) inside an action
- Creating multi-step orchestration across domains in a single action (use a Service)
- Naming an action vaguely: `InvoiceAction`, `UserHandler`, `DataProcessor`
- Adding multiple `execute()` methods or public methods beyond the single operation
- Adding business logic in a constructor — use `execute()` for that
- Performing database queries unrelated to the action's single responsibility

## References

- [Laravel Service Container](https://laravel.com/docs/container)
- Related: `Services/SKILL.md` — for multi-domain orchestration
- Related: `Jobs/SKILL.md` — for deferring actions to the queue
- Related: `Controllers/SKILL.md` — for how controllers delegate to actions
