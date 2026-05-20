---
name: testing
description: >-
  Cria testes com Pest PHP incluindo Feature, Unit, HTTP e Datasets. Use quando precisar escrever testes, criar test suites, ou implementar TDD em projetos Laravel com Pest.
compatibility: PHP 8.2+, Laravel 11+, Pest 2.x+
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

# testing

## Resumo
Cria e mantém testes com Pest PHP para Feature, Unit, HTTP, Actions e Policies.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `qa` | Para validação completa de qualidade |
| `coder` | Para criar testes durante implementação |
| `architecture` | Para testar Actions e Policies |
| `models` | Para criar Factories e testar Models |
| `cicd` | Para pipelines de teste |
| `pr-review` | Para verificar cobertura em PRs |

## Quando usar

Use esta skill sempre que:
- Escrever testes para novas features
- Aumentar cobertura de testes
- Refatorar testes existentes
- Criar mocks customizados
- Testar Actions, Policies, Models
- Testar endpoints HTTP
- Criar datasets para testes
- Configurar testes de multi-tenancy

## Instalação e Configuração

### Instalar Pest

```bash
composer require pestphp/pest --dev --with-all-dependencies
php artisan pest:install
```

### Estrutura de Testes

```
tests/
├── Feature/              # Testes de funcionalidade
│   ├── Http/
│   │   ├── Controllers/
│   │   └── Resources/
│   ├── Actions/
│   ├── Policies/
│   └── Jobs/
├── Unit/                 # Testes unitários
│   ├── Models/
│   ├── Enums/
│   └── Services/
└── Pest.php              # Configuração Pest
```

## Criar Teste

```bash
# Feature test
php artisan make:test ProductTest --pest

# Unit test
php artisan make:test Models/ProductTest --pest --unit
```

## Testes de HTTP

### Teste Básico de Endpoint

```php
<?php

use function Pest\Laravel\{actingAs, get};
use App\Models\User;
use App\Models\Product;

it('can view products list', function () {
    $user = User::factory()->create();
    Product::factory()->count(3)->create();

    actingAs($user)
        ->get(route('products.index'))
        ->assertOk()
        ->assertSee(__('messages.resources.products'))
        ->assertViewHas('products');
});

it('cannot view products without auth', function () {
    get(route('products.index'))
        ->assertRedirect(route('login'));
});
```

### Teste com Dados

```php
it('can create a product', function () {
    $user = User::factory()->create();
    $category = Category::factory()->create();

    actingAs($user)
        ->post(route('products.store'), [
            'name' => 'Test Product',
            'price' => 100.00,
            'category_id' => $category->id,
        ])
        ->assertRedirect(route('products.index'))
        ->assertSessionHas('success');

    $this->assertDatabaseHas('products', [
        'name' => 'Test Product',
        'price' => 10000, // em centavos
        'category_id' => $category->id,
    ]);
});
```

## Testes de Actions

```php
<?php

use App\Actions\Product\CreateProductAction;
use App\DataObjects\Product\CreateProductData;
use App\Models\Tenant;
use function Pest\Laravel\{assertDatabaseHas};

it('creates a product successfully', function () {
    // Arrange
    $tenant = Tenant::factory()->create();
    $data = CreateProductData::fromRequest([
        'name' => 'Test Product',
        'price' => 100.00,
        'category_id' => Category::factory()->create()->id,
    ]);

    // Act
    $product = CreateProductAction::run($tenant, $data);

    // Assert
    expect($product->name)->toBe('Test Product');
    assertDatabaseHas('products', [
        'id' => $product->id,
        'tenant_id' => $tenant->id,
    ]);
});

it('throws exception when product limit exceeded', function () {
    $tenant = Tenant::factory()->create();
    $tenant->plan->update(['limits' => ['products' => 1]]);

    Product::factory()->create(['tenant_id' => $tenant->id]);

    $data = CreateProductData::fromRequest([
        'name' => 'Second Product',
        'price' => 100.00,
    ]);

    expect(fn() => CreateProductAction::run($tenant, $data))
        ->toThrow(ProductLimitExceededException::class);
});
```

## Testes de Policies

```php
<?php

use App\Models\Product;
use App\Models\User;
use App\Policies\ProductPolicy;

it('allows owner to view product', function () {
    $user = User::factory()->create();
    $product = Product::factory()->create(['tenant_id' => $user->tenant_id]);

    expect((new ProductPolicy)->view($user, $product))->toBeTrue();
});

it('denies non-owner to view product', function () {
    $user = User::factory()->create();
    $otherTenant = Tenant::factory()->create();
    $product = Product::factory()->create(['tenant_id' => $otherTenant->id]);

    expect((new ProductPolicy)->view($user, $product))->toBeFalse();
});

it('allows creation when within limit', function () {
    $user = User::factory()->create();
    $user->tenant->plan->update(['limits' => ['products' => 10]]);

    expect((new ProductPolicy)->create($user))->toBeTrue();
});
```

## Testes de Models

```php
<?php

use App\Models\Product;

it('has a category', function () {
    $product = Product::factory()
        ->for(Category::factory())
        ->create();

    expect($product->category)->toBeInstanceOf(Category::class);
});

it('can check if is active', function () {
    $activeProduct = Product::factory()->active()->create();
    $inactiveProduct = Product::factory()->inactive()->create();

    expect($activeProduct->isActive())->toBeTrue();
    expect($inactiveProduct->isActive())->toBeFalse();
});

it('uses correct table name', function () {
    expect((new Product())->getTable())->toBe('products');
});
```

## Datasets

### Criar Dataset

```php
<?php

use App\Enums\ProductStatus;

dataset('product_statuses', [
    'active' => [ProductStatus::ACTIVE, true],
    'inactive' => [ProductStatus::INACTIVE, false],
    'draft' => [ProductStatus::DRAFT, false],
]);

it('correctly determines if product is viewable', function ($status, $expected) {
    $product = Product::factory()->create(['status' => $status]);

    expect($product->isViewable())->toBe($expected);
})->with('product_statuses');
```

### Dataset com Objetos

```php
dataset('users', [
    'admin' => fn() => User::factory()->admin()->create(),
    'regular' => fn() => User::factory()->create(),
    'guest' => null,
]);

it('can access dashboard based on role', function ($user) {
    if ($user) {
        actingAs($user)
            ->get('/dashboard')
            ->assertOk();
    } else {
        get('/dashboard')
            ->assertRedirect('/login');
    }
})->with('users');
```

## Mocking

### Mock Events

```php
<?php

use App\Events\ProductCreated;
use Illuminate\Support\Facades\Event;

it('dispatches product created event', function () {
    Event::fake([ProductCreated::class]);

    CreateProductAction::run($tenant, $data);

    Event::assertDispatched(ProductCreated::class, function ($event) use ($product) {
        return $event->product->id === $product->id;
    });
});

it('does not dispatch event on validation error', function () {
    Event::fake([ProductCreated::class]);

    // Tentativa inválida
    // ...

    Event::assertNotDispatched(ProductCreated::class);
});
```

### Mock Mail

```php
<?php

use Illuminate\Support\Facades\Mail;
use App\Mail\ProductCreatedMail;

it('sends email when product is created', function () {
    Mail::fake();

    CreateProductAction::run($tenant, $data);

    Mail::assertSent(ProductCreatedMail::class, function ($mail) use ($product) {
        return $mail->product->id === $product->id;
    });
});
```

### Mock Queue

```php
<?php

use Illuminate\Support\Facades\Queue;
use App\Jobs\ProcessProductImage;

it('queues image processing job', function () {
    Queue::fake();

    CreateProductAction::run($tenant, $data);

    Queue::assertPushed(ProcessProductImage::class, function ($job) use ($product) {
        return $job->product->id === $product->id;
    });
});
```

### Mock Storage

```php
<?php

use Illuminate\Support\Facades\Storage;

it('uploads product image', function () {
    Storage::fake('s3');

    $file = UploadedFile::fake()->image('product.jpg');

    // Upload
    $path = $file->store('products', 's3');

    Storage::disk('s3')->assertExists($path);
});
```

### Mock Notifications

```php
<?php

use Illuminate\Support\Facades\Notification;
use App\Notifications\ProductCreatedNotification;

it('sends notification when product is created', function () {
    Notification::fake();

    CreateProductAction::run($tenant, $data);

    Notification::assertSentTo(
        $tenant->owner,
        ProductCreatedNotification::class
    );
});
```

## Helpers Pest/Laravel

### actingAs

```php
actingAs($user)
    ->get('/dashboard')
    ->assertOk();
```

### get, post, put, delete, patch

```php
get('/products')
    ->assertOk();

post('/products', $data)
    ->assertRedirect();

put('/products/1', $data)
    ->assertRedirect();

delete('/products/1')
    ->assertRedirect();
```

### assertDatabaseHas, assertDatabaseMissing

```php
assertDatabaseHas('products', [
    'name' => 'Test Product',
]);

assertDatabaseMissing('products', [
    'name' => 'Deleted Product',
]);
```

### assertSoftDeleted

```php
assertSoftDeleted('products', [
    'id' => $productId,
]);
```

## Testes de Multi-tenancy

```php
<?php

it('tenant can only see their products', function () {
    $tenant1 = Tenant::factory()->create();
    $tenant2 = Tenant::factory()->create();

    Product::factory()->count(3)->create(['tenant_id' => $tenant1->id]);
    Product::factory()->count(5)->create(['tenant_id' => $tenant2->id]);

    actingAs($tenant1->owner)
        ->get(route('products.index'))
        ->assertViewHas('products', function ($products) use ($tenant1) {
            return $products->count() === 3
                && $products->every->tenant_id === $tenant1->id;
        });
});

it('cannot access another tenant product', function () {
    $tenant1 = Tenant::factory()->create();
    $tenant2 = Tenant::factory()->create();
    $product = Product::factory()->create(['tenant_id' => $tenant2->id]);

    actingAs($tenant1->owner)
        ->get(route('products.show', $product))
        ->assertForbidden();
});
```

## Testes de Jobs

```php
<?php

use App\Jobs\SyncProductInventory;
use function Pest\Laravel\{assertDatabaseHas};

it('syncs product inventory', function () {
    $product = Product::factory()->create();

    SyncProductInventory::dispatchSync($product);

    assertDatabaseHas('products', [
        'id' => $product->id,
        'inventory_synced_at' => now(),
    ]);
});
```

## Plugins Recomendados

### Pest Parallel

```bash
composer require pestphp/pest-plugin-parallel --dev
```

```php
// tests/Pest.php
use Pest\Parallel\Paratest;

Paratest::process();
```

### Coverage

```bash
php artisan pest --coverage
```

## Melhores Práticas

### ✅ FAÇA

- Use testes descritivos com `it()` e `test()`
- Siga padrão Arrange-Act-Assert
- Use factories para criar dados de teste
- Use datasets para testar múltiplos cenários
- Mock externos (Mail, Queue, Storage, Events)
- Teste exceções com `toThrow()`
- Use helpers Pest/Laravel para brevidade
- Teste authorization em Policies
- Teste validação em Form Requests
- Teste multi-tenancy separadamente
- Mantenha testes rápidos e isolados
- Use transações para rollback automático

### ❌ NÃO FAÇA

- Não teste código de framework
- Não use lógica complexa em testes
- Não deixe testes lentos sem otimização
- Não esqueça de limpar dados após testes
- Não teste múltiplas coisas em um teste
- Não dependa de ordem de testes
- Não use produção database para testes
- Não esqueça de mock serviços externos

## Checklist de Testes

Antes de finalizar QUALQUER feature:

- [ ] Testes de HTTP endpoints criados
- [ ] Testes de Actions criados
- [ ] Testes de Policies criados
- [ ] Testes de Models criados (se necessário)
- [ ] Mocks configurados (Mail, Queue, Events)
- [ ] Datasets para cenários múltiplos
- [ ] Testes de multi-tenancy (se aplicável)
- [ ] Cobertura de código verificada
- [ ] Todos testes passando

## Cobertura de Código

```bash
# Gerar relatório de cobertura
php artisan pest --coverage --min=80

# Gerar HTML coverage
php artisan pest --coverage --coverage-html=coverage
```

## Referências Cruzadas

- **Actions**: Teste Actions criadas com `laravel-actions-events`
- **Policies**: Teste Policies definidas em `laravel-architecture`
- **Exceptions**: Teste exceções de `laravel-exceptions`
- **Filament**: Teste Resources de `laravel-filament`
- **i18n**: Teste traduções de `laravel-i18n`

## Referências

- [Pest Documentation](https://pestphp.com/docs) - Documentação oficial
- [Laravel Testing](https://laravel.com/docs/testing) - Documentação Laravel
- [Pest Plugins](https://pestphp.com/docs/plugins) - Plugins disponíveis
