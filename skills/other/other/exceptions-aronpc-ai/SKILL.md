---
name: exceptions
description: >-
  Cria exceções customizadas renderable e reportable para HTTP e logging em Laravel. Use quando precisar criar exception handlers, exceções de domínio, ou melhorar o tratamento de erros.
compatibility: PHP 8.2+, Laravel 11+
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

# exceptions

## Resumo
Cria exceções customizadas com interfaces renderable/reportable para HTTP responses e logging.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `architecture` | Para exceções de domínio na arquitetura |
| `actions` | Para tratamento em Actions |
| `testing` | Para testar exceções |
| `qa` | Para verificar tratamento de erros |

## Quando usar

Use esta skill sempre que:
- Criar regras de negócio que violam limites
- Criar validações de domínio específicas
- Implementar autorização customizada
- Implementar erros de pagamento/billing
- Criar exceções com contexto para logging/monitoramento

## Princípios Fundamentais

**CRÍTICO:** Use exceções especializadas para erros de domínio específicos - NUNCA use `Exception` genérico.

- **Domain Exceptions** - Crie exceções customizadas para violações de regras de negócio
- **HTTP Status Mapping** - Mapeie exceções para códigos HTTP apropriados
- **Renderable** - Implemente método `render()` para respostas HTTP customizadas
- **Reportable** - Implemente método `report()` para logging/monitoramento
- **Localized Messages** - Use `__()` para mensagens de exceção (EN, ES, PT-BR)

## Estrutura de Exception

```
app/
├── Exceptions/
│   ├── Handler.php                    # Global exception handler
│   ├── Business/
│   │   ├── BusinessLimitExceededException.php
│   │   ├── BusinessNotFoundException.php
│   │   └── InvalidBusinessTypeException.php
│   ├── Tenant/
│   │   ├── TenantInactiveException.php
│   │   ├── TenantSuspendedException.php
│   │   └── UnauthorizedTenantAccessException.php
│   ├── Menu/
│   │   ├── MenuItemNotFoundException.php
│   │   ├── InvalidPriceException.php
│   │   └── MenuItemUnavailableException.php
│   └── Billing/
│       ├── InsufficientCreditsException.php
│       ├── PlanLimitExceededException.php
│       └── PaymentFailedException.php
```

## Criando Exceções Customizadas

```bash
php artisan make:exception Business/BusinessLimitExceededException
```

## Padrão de Exception

```php
<?php

declare(strict_types=1);

namespace App\Exceptions\Business;

use Exception;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

final class BusinessLimitExceededException extends Exception
{
    /**
     * Create a new exception instance.
     */
    public function __construct(
        public readonly int $currentCount,
        public readonly int $maxAllowed,
        public readonly string $planName,
    ) {
        parent::__construct(
            message: __('exceptions.business_limit_exceeded', [
                'current' => $this->currentCount,
                'max' => $this->maxAllowed,
                'plan' => $this->planName,
            ]),
            code: 403
        );
    }

    /**
     * Render exception as an HTTP response.
     */
    public function render(Request $request): JsonResponse|RedirectResponse
    {
        if ($request->expectsJson()) {
            return response()->json([
                'message' => $this->getMessage(),
                'current_count' => $this->currentCount,
                'max_allowed' => $this->maxAllowed,
                'plan_name' => $this->planName,
            ], 403);
        }

        return back()->with('error', $this->getMessage());
    }

    /**
     * Report exception (logging/monitoramento).
     */
    public function report(): void
    {
        // Log or send to monitoring service
        \Log::warning('Business limit exceeded', [
            'current' => $this->currentCount,
            'max' => $this->maxAllowed,
            'plan' => $this->planName,
        ]);
    }
}
```

## Uso em Actions

```php
<?php

declare(strict_types=1);

namespace App\Actions\Business;

use App\DataObjects\Business\CreateBusinessData;
use App\Exceptions\Business\BusinessLimitExceededException;
use App\Models\Business;
use App\Models\Tenant;
use Lorisleiva\Actions\Concerns\AsAction;

final class CreateBusinessAction
{
    use AsAction;

    public function handle(Tenant $tenant, CreateBusinessData $data): Business
    {
        // Check business limit
        $currentCount = $tenant->businesses()->count();
        $maxAllowed = $tenant->plan->limits['businesses'] ?? 0;

        if ($currentCount >= $maxAllowed) {
            throw new BusinessLimitExceededException(
                currentCount: $currentCount,
                maxAllowed: $maxAllowed,
                planName: $tenant->plan->name,
            );
        }

        // Create business
        return $tenant->businesses()->create($data->toArray());
    }
}
```

## Tipos Comuns de Exception

### Exceções de Domínio/Regra de Negócio

```php
// When resource not found
throw new BusinessNotFoundException($id);

// When validation fails
throw new InvalidBusinessTypeException($type);

// When limit exceeded
throw new BusinessLimitExceededException($current, $max, $plan);
```

### Exceções de Autorização

```php
// When tenant access denied
throw new UnauthorizedTenantAccessException($tenantId);

// When tenant is inactive
throw new TenantInactiveException($tenant);

// When tenant is suspended
throw new TenantSuspendedException($tenant, $reason);
```

### Exceções de Pagamento/Billing

```php
// When credits insufficient
throw new InsufficientCreditsException($required, $available);

// When plan limit exceeded
throw new PlanLimitExceededException($resource, $limit);

// When payment fails
throw new PaymentFailedException($transactionId, $reason);
```

## Convenção de Nomenclatura de Exceções

| Tipo | Convenção | Exemplo |
|------|----------|---------|
| **Not Found** | `*NotFoundException` | `BusinessNotFoundException` |
| **Invalid Input** | `Invalid*Exception` | `InvalidBusinessTypeException` |
| **Limit Exceeded** | `*LimitExceededException` | `BusinessLimitExceededException` |
| **Unauthorized** | `Unauthorized*Exception` | `UnauthorizedTenantAccessException` |
| **Payment** | `Payment*Exception` | `PaymentFailedException` |
| **Resource State** | `*InactiveException` | `TenantInactiveException` |
| **Business Rule** | Nome descritivo | `MenuItemUnavailableException` |

## Arquivos de Tradução

```php
// lang/en/exceptions.php
return [
    'business_limit_exceeded' => 'Business limit exceeded. You have :current businesses, but your :plan plan allows only :max.',
    'business_not_found' => 'Business not found.',
    'invalid_business_type' => 'Invalid business type: :type',
    'tenant_inactive' => 'Your account is inactive. Please contact support.',
    'tenant_suspended' => 'Your account has been suspended. Reason: :reason',
    'insufficient_credits' => 'Insufficient credits. Required: :required, Available: :available',
];

// lang/es/exceptions.php
return [
    'business_limit_exceeded' => 'Límite de negocios excedido. Tienes :current negocios, pero tu plan :plan permite solo :max.',
    // ...
];

// lang/pt_BR/exceptions.php
return [
    'business_limit_exceeded' => 'Limite de negócios excedido. Você tem :current negócios, mas seu plano :plan permite apenas :max.',
    // ...
];
```

## Mapeamento de Código HTTP

| Exception Type | HTTP Status | Descrição |
|----------------|-------------|-------------|
| **NotFoundException** | 404 | Resource not found |
| **Unauthorized** | 403 | Access denied |
| **ValidationException** | 422 | Validation failed |
| **LimitExceeded** | 403 | Resource limit exceeded |
| **PaymentFailed** | 402 | Payment required |
| **InactiveException** | 403 | Account/resource inactive |
| **SuspendedException** | 403 | Account suspended |

## Testando Exceções

```php
<?php

use App\Actions\Business\CreateBusinessAction;
use App\Exceptions\Business\BusinessLimitExceededException;

it('throws exception when business limit exceeded', function () {
    $tenant = Tenant::factory()->create(['plan_id' => 1]);
    $tenant->plan->update(['limits' => ['businesses' => 2]]);

    // Create 2 businesses (at limit)
    Business::factory()->count(2)->create(['tenant_id' => $tenant->id]);

    // Try to create 3rd business
    $data = CreateBusinessData::fromArray([
        'name' => 'New Business',
        'type' => 'restaurant',
    ]);

    expect(fn() => CreateBusinessAction::run($tenant, $data))
        ->toThrow(BusinessLimitExceededException::class, 'Business limit exceeded');
});

it('includes exception context in response', function () {
    $tenant = Tenant::factory()->create(['plan_id' => 1]);
    Business::factory()->count(2)->create(['tenant_id' => $tenant->id]);

    try {
        CreateBusinessAction::run($tenant, $data);
    } catch (BusinessLimitExceededException $e) {
        expect($e->currentCount)->toBe(2)
            ->and($e->maxAllowed)->toBe(2)
            ->and($e->planName)->toBe('Basic');
    }
});
```

## Global Exception Handler

```php
<?php

declare(strict_types=1);

namespace App\Exceptions;

use App\Exceptions\Business\BusinessLimitExceededException;
use Illuminate\Foundation\Exceptions\Handler as ExceptionHandler;
use Throwable;

final class Handler extends ExceptionHandler
{
    /**
     * A list of exception types with their corresponding custom log levels.
     */
    protected $levels = [
        BusinessLimitExceededException::class => 'warning',
    ];

    /**
     * A list of exception types that are not reported.
     */
    protected $dontReport = [
        // Exceptions that shouldn't be logged
    ];

    /**
     * Register exception handling callbacks.
     */
    public function register(): void
    {
        $this->reportable(function (Throwable $e) {
            // Send to monitoring service (Sentry, Bugsnag, etc.)
        });
    }
}
```

## Melhores Práticas

### ✅ FAÇA

- Crie exceções de domínio específicas para cada violação de regra de negócio
- Inclua dados de contexto no construtor da exceção
- Implemente `render()` para respostas HTTP customizadas
- Implemente `report()` para logging/monitoramento
- Use chaves de tradução para mensagens
- Teste exceções sendo lançadas nas Actions
- Mapeie exceções para códigos HTTP apropriados
- NÃO coloque lógica de negócio nas classes de exceção
- NÃO catch exceções apenas para relançar
- NÃO esqueça de traduzir mensagens de erro
- NÃO use `Exception` genérico sem motivo claro
- NÃO crie exceções para cada regra de validação (use Form Requests)
- NÃO esqueça de testar comportamento de exceções

## Quando Criar Exceções Customizadas

✅ Violações de regras de negócio (limits, constraints) \
✅ Erros de domínio específicos (invalid state transitions) \
✅ Falhas de autorização (tenant access, ownership) \
✅ Erros de pagamento/billing \
✅ Resource not found (quando 404 genérico não é suficiente)

❌ Erros de validação (use Form Requests) \
❌ Erros de conexão de banco (framework handles) \
❌ Erros genéricos (use built-in exceptions)

## Referências Cruzadas

- **Traduções**: Veja `laravel-i18n` para traduções de mensagens de erro em EN, ES, PT-BR
- **Actions**: Usado em Actions (veja `laravel-architecture` e `laravel-actions-events`)
- **Testes**: Veja `laravel-testing-pest` para testar exceções sendo lançadas

## Referências

- [Laravel Error Handling](https://laravel.com/docs/errors) - Documentação oficial
