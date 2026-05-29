---
name: models
description: >-
  Define Models Eloquent com relações, scopes, factories e multi-tenancy. Use quando precisar criar ou modificar models Laravel, definir relacionamentos, scopes, ou implementar multi-tenancy.
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

# models

## Resumo
Cria e mantém Models Eloquent com relações, scopes, factories e multi-tenancy.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `architecture` | Para estruturar Models na arquitetura |
| `enums` | Para usar enums nos Models |
| `testing` | Para criar Factories e testar Models |
| `standards` | Para padrões de código nos Models |
| `sprint` | Para planejar Models no sprint |

## Quando usar

Use esta skill sempre que:
- Criar Models Eloquent
- Definir relações entre Models
- Criar scopes locais e globais
- Criar Factories com states
- Implementar multi-tenancy patterns
- Configurar Casts, Accessors, Mutators
- Otimizar queries e evitar N+1
- Implementar soft deletes

## Criar Model

```bash
php artisan make:model Product -mf
# -m: migration
# -f: factory
```

## Model Básico

```php
<?php

declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\{BelongsTo, HasMany};
use Illuminate\Database\Eloquent\SoftDeletes;

final class Product extends Model
{
    use HasFactory;
    use SoftDeletes;

    protected $fillable = [
        'tenant_id',
        'name',
        'price', // em centavos
        'category_id',
        'status',
    ];

    protected $hidden = [
        'deleted_at',
    ];

    protected $casts = [
        'price' => 'integer',
        'status' => ProductStatus::class,
        'created_at' => 'datetime:d/m/Y H:i',
        'updated_at' => 'datetime:d/m/Y H:i',
    ];

    protected $appends = [
        'formatted_price',
    ];

    // Relações
    public function tenant(): BelongsTo
    {
        return $this->belongsTo(Tenant::class);
    }

    public function category(): BelongsTo
    {
        return $this->belongsTo(Category::class);
    }

    public function variants(): HasMany
    {
        return $this->hasMany(Variant::class);
    }

    // Accessor
    public function getFormattedPriceAttribute(): string
    {
        return 'R$ ' . number_format($this->price / 100, 2, ',', '.');
    }

    // Mutator
    public function setPriceAttribute(float $value): void
    {
        $this->attributes['price'] = (int) ($value * 100);
    }

    // Scope local
    public function scopeActive(Builder $query): Builder
    {
        return $query->where('status', ProductStatus::ACTIVE);
    }

    public function scopeInCategory(Builder $query, int $categoryId): Builder
    {
        return $query->where('category_id', $categoryId);
    }
}
```

## Relações

### One to One (Has One)

```php
// Tenant has one Settings
public function settings(): HasOne
{
    return $this->hasOne(Settings::class);
}

// Uso
$settings = $tenant->settings;
```

### One to Many (Has Many)

```php
// Category has many Products
public function products(): HasMany
{
    return $this->hasMany(Product::class);
}

// Com ordenação
public function products(): HasMany
{
    return $this->hasMany(Product::class)->orderBy('name');
}

// Uso
$products = $category->products;
```

### Many to Many (Belongs to Many)

```php
// Product belongs to many Tags
public function tags(): BelongsToMany
{
    return $this->belongsToMany(Tag::class)
        ->withPivot('is_primary')
        ->withTimestamps();
}

// Uso
$tags = $product->tags;
$product->tags()->attach($tagId);
$product->tags()->detach($tagId);
$product->tags()->sync([$tagId1, $tagId2]);
```

### Has One Through

```php
// Mechanic has one Car through Owner
public function car(): HasOneThrough
{
    return $this->hasOneThrough(Car::class, Owner::class);
}
```

### Has Many Through

```php
// Country has many Posts through Users
public function posts(): HasManyThrough
{
    return $this->hasManyThrough(Post::class, User::class);
}
```

### Polymorphic

```php
// Model
public function comments(): MorphMany
{
    return $this->morphMany(Comment::class, 'commentable');
}

// Inverso
public function commentable(): MorphTo
{
    return $this->morphTo();
}

// Many to many polymorphic
public function tags(): MorphToMany
{
    return $this->morphToMany(Tag::class, 'taggable');
}
```

## Eager Loading

### Prevenir N+1

```php
// ❌ BAD - N+1 problem
$products = Product::all();
foreach ($products as $product) {
    echo $product->category->name; // Query para cada product
}

// ✅ GOOD - Eager loading
$products = Product::with('category')->get();
foreach ($products as $product) {
    echo $product->category->name; // Sem queries adicionais
}
```

### Eager Loading Múltiplo

```php
Product::with(['category', 'variants', 'tags'])->get();
```

### Eager Loading Condicional

```php
Product::when($includeCategory, fn ($q) => $q->with('category'))
    ->get();
```

### Eager Loading Aninhado

```php
// Carregar products -> category -> parent category
Product::with('category.parent')->get();
```

### Lazy Eager Loading

```php
$products = Product::all();
$products->load('category'); // Carregar depois
$products->loadMissing('category'); // Carregar apenas se não carregado
```

### Eager Loading com Contagem

```php
Product::withCount('variants')->get();
// Access: $product->variants_count
```

## Scopes

### Scopes Locais

```php
public function scopeActive(Builder $query): Builder
{
    return $query->where('status', 'active');
}

public function scopePriceBetween(Builder $query, int $min, int $max): Builder
{
    return $query->whereBetween('price', [$min, $max]);
}

public function scopeSearch(Builder $query, string $term): Builder
{
    return $query->where('name', 'like', "%{$term}%");
}

// Uso
Product::active()->priceBetween(1000, 5000)->search('phone')->get();
```

### Scopes Globais

```bash
php artisan make:scope TenantScope
```

```php
<?php

declare(strict_types=1);

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

final class TenantScope implements Scope
{
    public function apply(Builder $builder, Model $model): void
{
    {
        if (auth()->check()) {
            $builder->where('tenant_id', auth()->user()->tenant_id);
        }
    }
}

// No Model
protected static function booted(): void
{
    static::addGlobalScope(new TenantScope);
}

// Remover scope
Product::withoutGlobalScope(TenantScope::class)->get();
Product::withoutGlobalScopes()->get();
```

## Casts

### Cast Básicos

```php
protected $casts = [
    'price' => 'integer',
    'is_active' => 'boolean',
    'settings' => 'array',
    'created_at' => 'datetime',
    'status' => ProductStatus::class, // Enum cast
];
```

### Cast Customizado

```bash
php artisan make:cast MoneyCast
```

```php
<?php

declare(strict_types=1);

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use InvalidArgumentException;

final class MoneyCast implements CastsAttributes
{
    public function get(Model $model, string $key, mixed $value, array $attributes): int
    {
        return (int) $value;
    }

    public function set(Model $model, string $key, mixed $value, array $attributes): int
    {
        if (!is_numeric($value)) {
            throw new InvalidArgumentException('Value must be numeric');
        }

        return (int) ($value * 100); // Converter para centavos
    }
}

// No Model
protected $casts = [
    'price' => MoneyCast::class,
];
```

### Accessor e Mutator

```php
// Accessor (GET)
public function getFormattedPriceAttribute(): string
{
    return 'R$ ' . number_format($this->price / 100, 2, ',', '.');
}

// Mutator (SET)
public function setPriceAttribute(float $value): void
{
    $this->attributes['price'] = (int) ($value * 100);
}

// Uso
$product->formatted_price; // "R$ 1.234,56"
$product->price = 12.34;   // Salva como 1234
```

## Factories

### Factory Básico

```bash
php artisan make:factory ProductFactory
```

```php
<?php

declare(strict_types=1);

namespace Database\Factories;

use App\Models\Product;
use App\Models\Category;
use Illuminate\Database\Eloquent\Factories\Factory;

final class ProductFactory extends Factory
{
    protected $model = Product::class;

    public function definition(): array
    {
        return [
            'tenant_id' => Tenant::factory(),
            'name' => fake()->words(3, true),
            'price' => fake()->numberBetween(1000, 100000), // centavos
            'category_id' => Category::factory(),
            'status' => ProductStatus::ACTIVE->value,
            'description' => fake()->paragraph(),
        ];
    }
}
```

### Factory com States

```php
class ProductFactory extends Factory
{
    // State: active
    public function active(): self
    {
        return $this->state(fn (array $attributes) => [
            'status' => ProductStatus::ACTIVE->value,
        ]);
    }

    // State: inactive
    public function inactive(): self
    {
        return $this->state(fn (array $attributes) => [
            'status' => ProductStatus::INACTIVE->value,
        ]);
    }

    // State: expensive
    public function expensive(): self
    {
        return $this->state(fn (array $attributes) => [
            'price' => fake()->numberBetween(50000, 500000),
        ]);
    }
}

// Uso
Product::factory()->active()->create();
Product::factory()->inactive()->count(10)->create();
Product::factory()->expensive()->create();
```

### Factory com Relações

```php
// Product belongs to Category
public function definition(): array
{
    return [
        'category_id' => Category::factory(),
    ];
}

// Product has many Variants
public function withVariants(int $count = 3): self
{
    return $this->has(Variant::factory()->count($count));
}

// Uso
Product::factory()->withVariants(5)->create();
```

## Multi-tenancy

### TenantAware Trait

```php
<?php

namespace App\Models\Concerns;

trait TenantAware
{
    protected static function bootTenantAware(): void
    {
        static::creating(function ($model) {
            if (auth()->check() && empty($model->tenant_id)) {
                $model->tenant_id = auth()->user()->tenant_id;
            }
        });

        static::addGlobalScope(new TenantScope);
    }
}

// Uso no Model
final class Product extends Model
{
    use TenantAware;
}
```

### Tenant Scope Global

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

final class TenantScope implements Scope
{
    public function apply(Builder $builder, Model $model): void
    {
        if (auth()->check()) {
            $builder->where('tenant_id', auth()->user()->tenant_id);
        }
    }
}
```

## Soft Deletes

```php
<?php

use Illuminate\Database\Eloquent\SoftDeletes;

final class Product extends Model
{
    use SoftDeletes;
}

// Queries
Product::withTrashed()->get();        // Inclui deletados
Product::onlyTrashed()->get();       // Apenas deletados
Product::withoutTrashed()->get();    // Apenas não deletados

// Restore
$product->restore();                 // Restaurar um
Product::onlyTrashed()->restore();   // Restaurar todos

// Force delete
$product->forceDelete();             // Deletar permanentemente
```

## Events do Model

```php
protected static function booted(): void
{
    static::creating(function ($product) {
        // Antes de criar
    });

    static::created(function ($product) {
        // Após criar
        event(new ProductCreated($product));
    });

    static::updating(function ($product) {
        // Antes de atualizar
    });

    static::updated(function ($product) {
        // Após atualizar
    });

    static::deleting(function ($product) {
        // Antes de deletar
    });

    static::deleted(function ($product) {
        // Após deletar
    });
}
```

## Otimização de Queries

### Select Específico

```php
// ❌ BAD - Seleciona tudo
Product::all();

// ✅ GOOD - Seleciona apenas necessário
Product::select('id', 'name', 'price')->get();
```

### Chunk

```php
// Processar em chunks
Product::chunk(100, function ($products) {
    foreach ($products as $product) {
        // Processar
    }
});
```

### Cursor

```php
// Para grandes quantidades
foreach (Product::cursor() as $product) {
    // Processar um por vez (memória eficiente)
}
```

### Pluck

```php
// Apenas valores específicos
Product::pluck('name', 'id'); // [1 => 'Product A', 2 => 'Product B']
```

### Lazy Collection

```php
// Lazy loading
Product::lazy()->each(function ($product) {
    // Processar sob demanda
});
```

## Melhores Práticas

### ✅ FAÇA

- Use Models finos (sem lógica de negócio)
- Sempre use eager loading para relações
- Crie scopes reutilizáveis
    - Use Factories para testes
    - Implemente soft deletes quando apropriado
    - Use casts para transformação de dados
    - Valide dados no Model ou Form Request
    - Otimize queries (chunk, cursor, lazy)
    - Implemente multi-tenancy com global scopes
    - Use eventos para side effects
    - Teste Models com Pest

### ❌ NÃO FAÇA

    - Não coloque lógica de negócio em Models
    - Não use DB facade em Models
    - Não ignore N+1 queries
    - Não faça queries em loops
    - Não esqueça de indexar colunas usadas em queries
    - Não use selects * desnecessariamente
    - Não ignore soft deletes
    - Não chame Actions em Models (use eventos)

## Checklist de Model

Antes de finalizar QUALQUER Model:

- [ ] Migration criada
- [ ] Factory criada
- [ ] Fillable definido corretamente
- [ ] Casts configurados
- [ ] Relações definidas
- [ ] Scopes criados
- [ ] Accessors/Mutators se necessário
- [ ] Global scopes para multi-tenancy
- [ ] Soft deletes se necessário
- [ ] Events configurados
- [ ] Testes criados com Pest

## Referências Cruzadas

- **Architecture**: Models finos integrados com Actions de `laravel-architecture`
- **Testing**: Testar Models com `laravel-testing-pest`
- **Actions**: Lógica de negócio em `laravel-actions-events`
- **i18n**: Enums traduzíveis com `laravel-i18n`

## Referências

- [Laravel Eloquent Documentation](https://laravel.com/docs/eloquent) - Documentação oficial
- [Laravel Relationships](https://laravel.com/docs/eloquent-relationships) - Relações
- [Laravel Scopes](https://laravel.com/docs/eloquent#query-scopes) - Scopes
