---
name: actions
description: >-
  Implementa lógica de negócio em Laravel usando Actions (lorisleiva/laravel-actions), Events, Listeners, Jobs e Observers. Use quando precisar criar actions, despachar eventos, jobs em background, ou implementar padrões event-driven em projetos Laravel.
compatibility: PHP 8.2+, Laravel 11+, laravel-actions
metadata:
  author: aronpc
  version: 1.0.0
  category: laravel
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# actions

## Resumo
Implementa lógica de negócio usando Actions, Events, Jobs e Observers.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `architecture` | Para usar Actions na arquitetura limpa |
| `realtime` | Para broadcasting de events |
| `testing` | Para testar Actions e Events |
| `exceptions` | Para tratamento de erros em Actions |
| `coder` | Para implementar Actions |

## Quando usar

Use esta skill sempre que:
- Criar lógica de negócio para Laravel
- Separar side-effects da lógica principal
- Criar background jobs
- Configurar model observers
- Implementar event-driven architecture

## Princípios Fundamentais

1. **Actions over Services** - Sempre use `lorisleiva/laravel-actions`
2. **Event-Driven** - Use Events + Listeners para side effects
3. **Observers** - Use para model lifecycle hooks
4. **Jobs** - Queue via Actions implementando `ShouldQueue`

## Criando Actions

```bash
php artisan make:action CreateBusiness
```

## Estrutura de Action

```php
<?php

declare(strict_types=1);

namespace App\Actions\Business;

use App\DataObjects\Business\CreateBusinessData;
use App\Models\Business;
use App\Models\Tenant;
use Lorisleiva\Actions\Concerns\AsAction;

final class CreateBusinessAction
{
    use AsAction;

    /**
     * Execute action.
     */
    public function handle(Tenant $tenant, CreateBusinessData $data): Business
    {
        // Check limits
        if (!$tenant->isWithinLimit('businesses')) {
            throw new \Exception('Business limit exceeded');
        }

        // Create business
        $business = $tenant->businesses()->create($data->toArray());

        // Increment usage
        $tenant->incrementUsage('businesses');

        // Dispatch event
        event(new BusinessCreated($business));

        return $business;
    }

    /**
     * Use as controller (optional).
     */
    public function asController(StoreBusinessRequest $request): Business
    {
        $data = CreateBusinessData::fromRequest($request->validated());
        return $this->handle(auth()->user()->tenant, $data);
    }

    /**
     * Run as queued job (optional).
     */
    public function asJob(Tenant $tenant, CreateBusinessData $data): void
    {
        $this->handle($tenant, $data);
    }
}
```

## Uso de Actions

```php
// Run sincronamente
CreateBusinessAction::run($tenant, $data);

// Run em background (queued)
CreateBusinessAction::dispatch($tenant, $data);

// Run com delay
CreateBusinessAction::dispatch($tenant, $data)->delay(now()->addMinutes(5));

// Run em fila específica
CreateBusinessAction::dispatch($tenant, $data)->onQueue('high');
```

## Value Objects (DTOs)

**CRÍTICO:** Actions DEVEM usar Value Objects - NUNCA passe arrays crusos.

### Por Que Usar Value Objects?

✅ Type Safety - Detecta erros em tempo de compilação \
✅ Suporte IDE - Autocompletion \
✅ Validação Centralizada - Em um lugar \
✅ Imutabilidade - Previne mutações \
✅ Self-Documenting - Contrato claro \
✅ Reusabilidade - Use across Actions/Jobs/Events

❌ Single primitive values \
❌ Eloquent models \
❌ Collections

### Criando Value Objects

```php
<?php

declare(strict_types=1);

namespace App\DataObjects\Business;

final readonly class CreateBusinessData
{
    public function __construct(
        public string $name,
        public string $type,
        public ?string $email = null,
        public ?string $phone = null,
        public ?array $settings = null,
    ) {}

    public static function fromRequest(array $data): self
    {
        return new self(
            name: $data['name'],
            type: $data['type'],
            email: $data['email'] ?? null,
            phone: $data['phone'] ?? null,
            settings: $data['settings'] ?? null,
        );
    }

    public function toArray(): array
    {
        return [
            'name' => $this->name,
            'type' => $this->type,
            'email' => $this->email,
            'phone' => $this->phone,
            'settings' => $this->settings ?? [],
        ];
    }
}
```

### Quando Usar Value Objects

✅ Action parameters (sempre para inputs complexos) \
✅ Service methods \
✅ API responses \
✅ Event payloads \
✅ Jobs data

❌ Single primitive values \
❌ Eloquent models \
❌ Collections

## Events & Listeners

**Event:**

```php
<?php

namespace App\Events;

use App\Models\Business;
use Illuminate\Foundation\Events\Dispatchable;

final class BusinessCreated
{
    use Dispatchable;

    public function __construct(public Business $business) {}
}
```

**Listener (as Action):**

```php
<?php

namespace App\Listeners;

use App\Events\BusinessCreated;
use Lorisleiva\Actions\Concerns\AsAction;

final class SendBusinessWelcomeEmail
{
    use AsAction;

    public function handle(BusinessCreated $event): void
    {
        // Send welcome email
    }
}
```

## Model Observers

```bash
php artisan make:observer BusinessObserver --model=Business
```

```php
<?php

namespace App\Observers;

use App\Models\Business;

final class BusinessObserver
{
    public function creating(Business $business): void
    {
        $business->slug = Str::slug($business->name);
    }

    public function created(Business $business): void
    {
        event(new BusinessCreated($business));
    }

    public function updating(Business $business): void
    {
        if ($business->isDirty('name')) {
            $business->slug = Str::slug($business->name);
        }
    }
}
```

**Registrar em AppServiceProvider:**

```php
public function boot(): void
{
    Business::observe(BusinessObserver::class);
}
```

## Melhores Práticas

### ✅ FAÇA

- Use Actions para toda lógica de negócio
- Use Value Objects para dados complexos
- Use Events para side-effects
- Use Observers para model lifecycle
- Use Jobs para processos longos
- Dispatch Events após mudanças de estado
- Mantenha Actions focadas (single responsibility)

### ❌ NÃO FAÇA

- Não crie Services tradicionais
- Não passe arrays crusos para Actions
- Não coloque lógica de negócio em Models
- Não esqueça de usar Events
- Não use DB facade em Actions
- Não crie Actions sem tipagem

## Referências Cruzadas

- **Estrutura Actions/DTOs**: Veja `laravel-architecture` para estrutura completa de Actions e Value Objects
- **Traduções**: Veja `laravel-i18n` para traduções de Events e mensagens de sistema
- **Exceções**: Veja `laravel-exceptions` para criar exceções customizadas em Actions
- **Testes**: Veja `laravel-testing-pest` para testes de Actions, Jobs e Events

## Referências

- `docs/07-actions-events-jobs.md` - Documentação completa
- [Laravel Actions Documentation](https://laravelactions.com/) - Documentação oficial
- [Laravel Events Documentation](https://laravel.com/docs/events) - Documentação Laravel
