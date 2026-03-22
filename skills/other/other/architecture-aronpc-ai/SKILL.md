---
name: architecture
description: >-
  Define a arquitetura limpa de projetos Laravel com Actions, DTOs, Policies e Service Layer. Use quando precisar organizar estrutura de diretórios, definir padrões arquiteturais, ou planejar a organização de um projeto Laravel.
compatibility: PHP 8.5+, Laravel 12, laravel-actions
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

# architecture

## Resumo
Define e mantém arquitetura limpa em projetos Laravel usando Actions, DTOs e Policies.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `coder` | Para implementar seguindo a arquitetura |
| `actions` | Para Actions, Events e Jobs |
| `models` | Para Models e relações |
| `exceptions` | Para exceções de domínio |
| `testing` | Para testar Actions e Policies |
| `planner` | Para planejar arquitetura de features |

## Quando usar

Use esta skill sempre que:
- Criar novas features
- Estruturar código existente
- Refatorar seguindo clean architecture
- Definir responsabilidades de camadas
- Criar Actions, DTOs, ou Policies

## Stack Tecnológico

**Stack:** Laravel 12 + React + Inertia.js + Filament 5 + Tailwind 4

### Pontos Chave

- **Admin Panel:** Filament 5 (Super Admin)
- **Actions Pattern:** Laravel Actions (lorisleiva/laravel-actions)
- **Testing:** Pest PHP
- **i18n:** English, Spanish, Portuguese BR

## Regras de Codificação

### Core Rules

- PHP 8.5+, strict types: `declare(strict_types=1);`
- Siga pint.json, PHPStan max level
- Não use `DB::`, use `Model::query()`
- Não use `env()` fora de arquivos de configuração
- Sempre obtenha aprovação antes de novos diretórios/dependências
- Delete `.gitkeep` ao adicionar arquivos

### Laravel 12 Específico

- Commands são registrados automaticamente de `app/Console/Commands/`
- Commands são registrados automaticamente de `app/Console/Commands/`
- Use `config('app.name')` não `env('APP_NAME')`

## Estrutura do Projeto

```
app/
├── Actions/          # Lógica de negócio (NÃO Services!)
│   ├── Business/
│   ├── Tenant/
│   └── Billing/
├── DataObjects/      # Value Objects (DTOs)
│   ├── Business/
│   ├── Menu/
│   └── Order/
├── Enums/            # Todos os enums (nomes descritivos, sem sufixo)
├── Events/           # Eventos de domínio (past tense)
├── Listeners/        # Event listeners (imperative)
├── Models/           # Eloquent models (thin, sem lógica de negócio)
├── Observers/        # Model lifecycle observers
├── Http/
│   ├── Controllers/  # Thin orchestrators
│   └── Requests/     # Form Requests (validation)
└── Policies/         # Authorization logic
```

## Resumo de Arquitetura

Este projeto segue **clean architecture** com clara separação de responsabilidades:

```
┌─────────────────────────────────────────────────────────────┐
│                      HTTP REQUEST                            │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  CONTROLLER (Thin Orchestrator)                              │
│  ├─ Validate (FormRequest)                                   │
│  ├─ Authorize (Policy)                                       │
│  ├─ Build Value Object                                       │
│  └─ Call Action                                              │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  VALUE OBJECT (Data Transfer)                                │
│  ├─ Type-safe data structure                                 │
│  ├─ Immutable (readonly)                                     │
│  └─ Factory methods (fromRequest, toArray)                   │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  ACTION (Business Logic)                                     │
│  ├─ Single responsibility                                    │
│  ├─ Database operations                                      │
│  ├─ Business rules & calculations                            │
│  ├─ Call other Actions if needed                             │
│  └─ Dispatch Events                                          │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  MODEL (Data + Relationships)                                │
│  ├─ Eloquent relationships                                   │
│  ├─ Accessors & Mutators                                     │
│  ├─ Scopes                                                   │
│  └─ NO business logic                                        │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  OBSERVER / EVENT (Side Effects)                             │
│  ├─ Model lifecycle hooks (Observer)                         │
│  ├─ Send notifications                                       │
│  ├─ Update related records                                   │
│  └─ Log activities                                           │
└─────────────────────────────────────────────────────────────┘
```

## Responsabilidades de Camada

| Camada | Responsabilidade | ✅ Deve | ❌ Não Deve |
|--------|------------------|----------|---------------|
| **Controller** | Orquestração HTTP | Validate, Authorize, Delegate, Respond | Lógica de negócio, Queries de database |
| **Value Object** | Transferência de dados | Type safety, Imutabilidade | Validação, Lógica de negócio |
| **Action** | Lógica de negócio | CRUD, Cálculos, Regras, Eventos | Preocupações HTTP, Validação |
| **Model** | Dados + Relações | Relações, Casts, Scopes | Lógica de negócio, Cálculos complexos |
| **Observer** | Side effects | Lifecycle hooks, Events | Lógica de negócio core |
| **Event/Listener** | Side effects desacoplados | Notifications, Logging, Async tasks | Fluxo de negócio principal |

## Convenções de Nomenclatura

| Tipo | Convenção | Exemplo |
|------|------------|----------|
| **Enum** | Sem sufixo (Spatie) | `BusinessType`, `UserRole` |
| **Action** | Sufixo `Action` | `CreateBusinessAction`, `UpdateOrderAction` |
| **Value Object** | Sufixo `Data` | `CreateBusinessData`, `UpdateOrderData` |
| **Controller** | Plural + `Controller` | `BusinessesController`, `OrdersController` |
| **Event** | Past tense, sem sufixo | `BusinessCreated`, `OrderPlaced` |
| **Listener** | Imperativo, sem sufixo | `SendWelcomeEmail`, `NotifyAdmin` |
| **Observer** | Sufixo `Observer` | `BusinessObserver`, `OrderObserver` |
| **Policy** | Sufixo `Policy` | `BusinessPolicy`, `OrderPolicy` |
| **Form Request** | Sufixo `Request` | `StoreBusinessRequest`, `UpdateOrderRequest` |

**NOTA:** NUNCA use sufixo `Service` - use Actions!

## Comandos Comuns

### Criar Model + Migration + Factory

```bash
php artisan make:model Product -mf
```

### Criar Action

```bash
php artisan make:action CreateProduct
```

### Criar Value Object

```bash
php artisan make:class DataObjects/Product/CreateProductData
```

### Criar Form Request

```bash
php artisan make:request StoreProductRequest
```

### Criar Policy

```bash
php artisan make:policy ProductPolicy --model=Product
```

### Criar Observer

```bash
php artisan make:observer ProductObserver --model=Product
```

### Criar Test

```bash
php artisan make:test --pest ProductTest
```

## Checklist de Conclusão

Antes de finalizar QUALQUER feature:

- [ ] Testes passando (`composer test`)
- [ ] Código fixado (`composer fix`)
- [ ] Eager loading implementado (sem N+1)
- [ ] Traduções adicionadas (EN, ES, PT-BR)
- [ ] IMPLEMENTATION.md atualizado
- [ ] Documentação commitada separadamente
- [ ] Sem dependências não aprovadas

## Exemplo de Controller Thin

```php
final class BusinessController
{
    public function store(StoreBusinessRequest $request): RedirectResponse
    {
        // ✅ GOOD: Thin controller - delega para Action
        $business = CreateBusinessAction::run(
            tenant: auth()->user()->tenant,
            data: $request->validated()
        );

        return redirect()
            ->route('owner.businesses.index')
            ->with('success', __('messages.business_created'));
    }
}
```

## Exemplo de Action

```php
final class CreateBusinessAction
{
    use AsAction;

    public function handle(Tenant $tenant, CreateBusinessData $data): Business
    {
        // Check limits
        if (!$tenant->isWithinLimit('businesses')) {
            throw new BusinessLimitExceededException();
        }

        // Create business
        $business = $tenant->businesses()->create($data->toArray());

        // Increment usage
        $tenant->incrementUsage('businesses');

        // Dispatch event
        event(new BusinessCreated($business));

        return $business;
    }
}
```

## Exemplo de Value Object

```php
final readonly class CreateBusinessData
{
    public function __construct(
        public string $name,
        public string $type,
        public ?string $email = null,
        public ?string $phone = null,
    ) {}

    public static function fromRequest(array $data): self
    {
        return new self(
            name: $data['name'],
            type: $data['type'],
            email: $data['email'] ?? null,
            phone: $data['phone'] ?? null,
        );
    }

    public function toArray(): array
    {
        return [
            'name' => $this->name,
            'type' => $this->type,
            'email' => $this->email,
            'phone' => $this->phone,
        ];
    }
}
```

## Exemplo de Policy

```php
final class BusinessPolicy
{
    public function view(User $user, Business $business): bool
    {
        return $user->tenant_id === $business->tenant_id;
    }

    public function create(User $user): bool
    {
        return $user->tenant->isWithinLimit('businesses');
    }

    public function update(User $user, Business $business): bool
    {
        return $user->tenant_id === $business->tenant_id;
    }

    public function delete(User $user, Business $business): bool
    {
        return $user->tenant_id === $business->tenant_id;
    }
}
```

## Referências Cruzadas

- **Traduções**: Veja `laravel-i18n` para traduções de Enums, mensagens e interfaces
- **Exceções**: Veja `laravel-exceptions` para exceções de domínio e regras de negócio
- **Testes**: Veja `laravel-testing-pest` para testes de Actions e Policies
- **Events/Jobs**: Veja `laravel-actions-events` para patterns avançados de eventos

## Referências

- [Laravel Actions](https://laravelactions.com/) - Documentação oficial do pacote
- [Laravel Docs](https://laravel.com/docs) - Documentação oficial do Laravel
