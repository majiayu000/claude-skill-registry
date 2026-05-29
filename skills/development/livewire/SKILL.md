---
name: livewire
description: Laravel Livewire conventions for building interactive UI without custom JavaScript. Components are PHP classes with reactive properties, computed properties, and event dispatching.
---

**Name:** Livewire Components
**Description:** Laravel Livewire conventions for building interactive UI without custom JavaScript. Components are PHP classes with reactive properties, computed properties, and event dispatching.
**Compatible Agents:** general-purpose, frontend
**Tags:** app/Livewire/**/*.php, resources/views/livewire/**/*.blade.php, laravel, php, frontend, livewire, interactive

## Rules

- Use **Livewire** for all interactive UI — no custom JavaScript unless absolutely necessary
- Follow existing Livewire component patterns in the project
- Keep component logic in the PHP class; keep Blade templates declarative
- One Livewire component per feature/concern
- Use public properties for reactive data
- Use computed properties (`#[Computed]`) for derived data
- Use `wire:model` for two-way binding, `wire:click` for actions
- Keep components small and focused — extract sub-components when they grow
- Use form objects (`Livewire\Form`) for complex form handling
- Dispatch events for cross-component communication

## Examples

```php
namespace App\Livewire;

use App\Actions\CreateInvoice;
use App\Models\Invoice;
use Livewire\Attributes\Computed;
use Livewire\Component;

class InvoiceList extends Component
{
    public string $search = '';

    #[Computed]
    public function invoices()
    {
        return Invoice::where('title', 'like', "%{$this->search}%")
            ->paginate(15);
    }

    public function delete(int $invoiceId): void
    {
        $invoice = Invoice::findOrFail($invoiceId);
        $this->authorize('delete', $invoice);
        $invoice->delete();
    }

    public function render()
    {
        return view('livewire.invoice-list');
    }
}
```

```blade
{{-- Blade template — declarative, no logic --}}
<div>
    <input wire:model.live="search" type="text" placeholder="Search invoices...">

    @foreach ($this->invoices as $invoice)
        <div>
            {{ $invoice->title }}
            <button wire:click="delete({{ $invoice->id }})">Delete</button>
        </div>
    @endforeach

    {{ $this->invoices->links() }}
</div>
```

```php
// Livewire Form Object for complex forms
use Livewire\Form;

class InvoiceForm extends Form
{
    public string $title = '';
    public int $order_id = 0;
    public ?string $notes = null;

    public function rules(): array
    {
        return [
            'title'    => ['required', 'string', 'max:255'],
            'order_id' => ['required', 'integer', 'exists:orders,id'],
            'notes'    => ['nullable', 'string'],
        ];
    }
}
```

```php
// Cross-component event dispatching
$this->dispatch('invoice-created', invoiceId: $invoice->id);

// Listening for events
#[On('invoice-created')]
public function refreshList(int $invoiceId): void { ... }
```

## Anti-Patterns

- Writing custom JavaScript when Livewire can handle the interaction
- Putting display logic in the PHP class instead of the Blade template
- Growing a single component to handle multiple unrelated features
- Using `wire:model` without `.live` or `.lazy` when immediate reactivity is not needed (unnecessary requests)
- Not using form objects for forms with more than 3-4 fields

## References

- [Livewire Documentation](https://livewire.laravel.com/)
- Related: `Blade/SKILL.md` — Blade templates used by Livewire components
- Related: `Actions/SKILL.md` — Livewire components delegate business logic to Actions
