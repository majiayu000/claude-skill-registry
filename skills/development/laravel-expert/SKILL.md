---
name: laravel-expert
description: Especialista em desenvolvimento Laravel para criação de Models, Controllers, Migrations, Seeders, Form Requests, Resources, Policies, Jobs, Events, Listeners, Notifications e Service Providers seguindo convenções oficiais. Usar quando precisar criar componentes Laravel, implementar funcionalidades seguindo best practices, configurar relacionamentos Eloquent, criar APIs RESTful, implementar queues e eventos, ou resolver dúvidas sobre arquitetura Laravel.
---

# Laravel Expert

Skill para desenvolvimento Laravel seguindo convenções oficiais e best practices.

## Convenções de Nomenclatura

```
Model:          singular, PascalCase        → User, EventContract
Controller:     PascalCase + Controller     → UserController, EventContractController
Migration:      snake_case com timestamp    → 2024_01_15_create_users_table
Seeder:         PascalCase + Seeder         → UserSeeder
Factory:        PascalCase + Factory        → UserFactory
Request:        PascalCase + Request        → StoreUserRequest, UpdateUserRequest
Resource:       PascalCase + Resource       → UserResource, UserCollection
Policy:         PascalCase + Policy         → UserPolicy
Job:            PascalCase + Job            → ProcessPaymentJob
Event:          PascalCase descritivo       → UserRegistered, PaymentProcessed
Listener:       PascalCase descritivo       → SendWelcomeEmail
Notification:   PascalCase descritivo       → InvoicePaid
Middleware:     PascalCase                  → EnsureUserIsAdmin
```

## Estrutura de Arquivos

```
app/
├── Http/
│   ├── Controllers/
│   │   └── Api/           # Controllers de API separados
│   ├── Requests/          # Form Requests para validação
│   ├── Resources/         # API Resources
│   └── Middleware/
├── Models/
├── Services/              # Business logic (não nativo, recomendado)
├── Repositories/          # Data access (não nativo, recomendado)
├── Actions/               # Single-action classes
├── Policies/
├── Jobs/
├── Events/
├── Listeners/
└── Notifications/
```

## Criação de Componentes

### Model com Relacionamentos

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\SoftDeletes;

class Contract extends Model
{
    use HasFactory, SoftDeletes;

    protected $fillable = [
        'client_id',
        'event_date',
        'value',
        'status',
    ];

    protected $casts = [
        'event_date' => 'date',
        'value' => 'decimal:2',
        'status' => ContractStatus::class, // Enum casting
    ];

    // Relacionamentos
    public function client(): BelongsTo
    {
        return $this->belongsTo(Client::class);
    }

    public function payments(): HasMany
    {
        return $this->hasMany(Payment::class);
    }

    // Scopes
    public function scopeActive($query)
    {
        return $query->where('status', ContractStatus::Active);
    }

    public function scopeByPeriod($query, $start, $end)
    {
        return $query->whereBetween('event_date', [$start, $end]);
    }

    // Accessors & Mutators (Laravel 9+)
    protected function formattedValue(): Attribute
    {
        return Attribute::make(
            get: fn () => 'R$ ' . number_format($this->value, 2, ',', '.')
        );
    }
}
```

### Controller RESTful

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreContractRequest;
use App\Http\Requests\UpdateContractRequest;
use App\Http\Resources\ContractResource;
use App\Models\Contract;
use Illuminate\Http\Resources\Json\AnonymousResourceCollection;

class ContractController extends Controller
{
    public function index(): AnonymousResourceCollection
    {
        $contracts = Contract::with(['client', 'payments'])
            ->latest()
            ->paginate(15);

        return ContractResource::collection($contracts);
    }

    public function store(StoreContractRequest $request): ContractResource
    {
        $contract = Contract::create($request->validated());

        return new ContractResource($contract->load('client'));
    }

    public function show(Contract $contract): ContractResource
    {
        return new ContractResource($contract->load(['client', 'payments']));
    }

    public function update(UpdateContractRequest $request, Contract $contract): ContractResource
    {
        $contract->update($request->validated());

        return new ContractResource($contract->fresh('client'));
    }

    public function destroy(Contract $contract): \Illuminate\Http\Response
    {
        $contract->delete();

        return response()->noContent();
    }
}
```

### Form Request

```php
<?php

namespace App\Http\Requests;

use App\Enums\ContractStatus;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class StoreContractRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Contract::class);
    }

    public function rules(): array
    {
        return [
            'client_id' => ['required', 'exists:clients,id'],
            'event_date' => ['required', 'date', 'after:today'],
            'value' => ['required', 'numeric', 'min:0'],
            'status' => ['required', Rule::enum(ContractStatus::class)],
        ];
    }

    public function messages(): array
    {
        return [
            'client_id.required' => 'O cliente é obrigatório.',
            'event_date.after' => 'A data do evento deve ser futura.',
        ];
    }
}
```

### API Resource

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class ContractResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'event_date' => $this->event_date->format('Y-m-d'),
            'event_date_formatted' => $this->event_date->format('d/m/Y'),
            'value' => $this->value,
            'value_formatted' => $this->formatted_value,
            'status' => $this->status->value,
            'status_label' => $this->status->label(),
            'client' => new ClientResource($this->whenLoaded('client')),
            'payments' => PaymentResource::collection($this->whenLoaded('payments')),
            'created_at' => $this->created_at->toISOString(),
        ];
    }
}
```

## Migration Best Practices

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('contracts', function (Blueprint $table) {
            $table->id();
            $table->foreignId('client_id')->constrained()->cascadeOnDelete();
            $table->date('event_date')->index();
            $table->decimal('value', 10, 2);
            $table->string('status', 20)->default('pending')->index();
            $table->text('notes')->nullable();
            $table->timestamps();
            $table->softDeletes();

            // Índices compostos para queries frequentes
            $table->index(['status', 'event_date']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('contracts');
    }
};
```

## Service Layer Pattern

Para lógica de negócio complexa, usar Services:

```php
<?php

namespace App\Services;

use App\Models\Contract;
use App\Models\Payment;
use Illuminate\Support\Facades\DB;

class ContractService
{
    public function createWithPayments(array $data, array $payments): Contract
    {
        return DB::transaction(function () use ($data, $payments) {
            $contract = Contract::create($data);

            foreach ($payments as $payment) {
                $contract->payments()->create($payment);
            }

            return $contract->load('payments');
        });
    }

    public function calculateTotalReceivable(Contract $contract): float
    {
        $paid = $contract->payments()
            ->where('status', 'paid')
            ->sum('amount');

        return $contract->value - $paid;
    }
}
```

## Referências Adicionais

- **Eloquent avançado**: Ver `references/eloquent-advanced.md`
- **Queues e Jobs**: Ver `references/queues.md`
- **Events e Listeners**: Ver `references/events.md`
- **Testing**: Ver `references/testing.md`
