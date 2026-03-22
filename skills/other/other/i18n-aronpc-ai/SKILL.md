---
name: i18n
description: >-
  Implementa internacionalização EN/ES/PT-BR com traduções e integração de enums em Laravel. Use quando precisar adicionar traduções, localização, ou suporte multi-idioma.
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

# i18n

## Resumo
Implementa internacionalização completa (EN, ES, PT-BR) com traduções e enums.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `enums` | Para criar enums traduzíveis |
| `ux` | Para UX com mensagens traduzidas |
| `coder` | Para implementar traduções |
| `testing` | Para testar localização |

## Quando usar

Use esta skill sempre que:
- Criar qualquer feature com interface de usuário
- Adicionar novos idiomas
- Criar Enums
- Traduzir mensagens de validação
- Traduzir resources Filament
- Atualizar arquivos de tradução

## Princípios Fundamentais

### Core Rules

- **TODO texto** DEVE ser traduzido para: **English (en)**, **Spanish (es)**, **Portuguese BR (pt_BR)**
- **ZERO strings hardcoded** - todo texto voltado ao usuário deve usar `__()`
- **Chaves consistentes** - use nomenclatura semântica (ex: `messages.welcome`, não `messages.msg1`)
- **Context-aware** - organize por domínio/feature, não por página
- **Pluralização** - use pluralização do Laravel para itens contáveis
- **Fallback** - English é idioma padrão/fallback

## Estrutura de Arquivos

```
lang/
├── en/                          # English (default)
│   ├── auth.php                # Authentication & authorization messages
│   ├── enums.php               # Enum labels (status, types, roles)
│   ├── exceptions.php          # Exception messages
│   ├── fields.php              # Form field labels
│   ├── messages.php            # General UI messages
│   ├── navigation.php          # Menu & navigation items
│   ├── pagination.php          # Pagination text (Laravel default)
│   ├── passwords.php           # Password reset messages (Laravel default)
│   └── validation.php          # Validation messages (Laravel default)
├── es/                          # Spanish (Español)
│   └── (same structure)
└── pt_BR/                       # Portuguese Brazil (Português BR)
    └── (same structure)
```

## Exemplos de Arquivos de Tradução

### messages.php - General UI Messages

```php
<?php

// lang/en/messages.php
return [
    'welcome' => 'Welcome to :app',
    'dashboard' => 'Dashboard',
    'saved_successfully' => ':resource saved successfully!',
    'confirm_delete' => 'Are you sure you want to delete this :resource?',

    'resources' => [
        'business' => 'business',
        'menu_item' => 'menu item',
    ],
];

// lang/es/messages.php
return [
    'welcome' => 'Bienvenido a :app',
    'dashboard' => 'Panel de control',
    'saved_successfully' => '¡:resource guardado con éxito!',
    'confirm_delete' => '¿Estás seguro de que deseas eliminar este :resource?',

    'resources' => [
        'business' => 'negocio',
        'menu_item' => 'ítem del menú',
    ],
];

// lang/pt_BR/messages.php
return [
    'welcome' => 'Bem-vindo ao :app',
    'dashboard' => 'Painel',
    'saved_successfully' => ':resource salvo com sucesso!',
    'confirm_delete' => 'Tem certeza de que deseja excluir este :resource?',

    'resources' => [
        'business' => 'negócio',
        'menu_item' => 'item do cardápio',
    ],
];
```

### fields.php - Form Field Labels

```php
<?php

// lang/en/fields.php
return [
    'name' => 'Name',
    'email' => 'Email',
    'phone' => 'Phone',
    'description' => 'Description',
    'price' => 'Price',
];

// lang/es/fields.php
return [
    'name' => 'Nombre',
    'email' => 'Correo electrónico',
    'phone' => 'Teléfono',
    'description' => 'Descripción',
    'price' => 'Precio',
];

// lang/pt_BR/fields.php
return [
    'name' => 'Nome',
    'email' => 'E-mail',
    'phone' => 'Telefone',
    'description' => 'Descrição',
    'price' => 'Preço',
];
```

### enums.php - Enum Labels

```php
<?php

// lang/en/enums.php
return [
    'business_type' => [
        'restaurant' => 'Restaurant',
        'cafe' => 'Café',
    ],

    'order_status' => [
        'pending' => 'Pending',
        'confirmed' => 'Confirmed',
    ],
];

// lang/es/enums.php
return [
    'business_type' => [
        'restaurant' => 'Restaurante',
        'cafe' => 'Cafetería',
    ],

    'order_status' => [
        'pending' => 'Pendiente',
        'confirmed' => 'Confirmado',
    ],
];

// lang/pt_BR/enums.php
return [
    'business_type' => [
        'restaurant' => 'Restaurante',
        'cafe' => 'Cafeteria',
    ],

    'order_status' => [
        'pending' => 'Pendente',
        'confirmed' => 'Confirmado',
    ],
];
```

## Padrões de Uso

### 1. PHP (Controllers, Actions, Classes)

```php
<?php

// ✅ CORRECT - Simple translation
$message = __('messages.welcome');

// ✅ CORRECT - With parameters
$message = __('messages.saved_successfully', [
    'resource' => __('messages.resources.business')
]);

// ✅ CORRECT - Pluralization
$count = 5;
$message = trans_choice('messages.items_count', $count, ['count' => $count]);

// ❌ WRONG - Hardcoded text
$message = 'Business created successfully!';

// ❌ WRONG - Concatenation
$message = __('messages.you_have') . ' ' . $count . ' ' . __('messages.items');
```

### 2. Blade Templates

```blade
{{-- ✅ CORRECT - Simple translation --}}
<h1>{{ __('messages.dashboard') }}</h1>

{{-- ✅ CORRECT - With parameters --}}
<p>{{ __('messages.welcome', ['app' => config('app.name')]) }}</p>

{{-- ✅ CORRECT - Form labels --}}
<label>{{ __('fields.name') }}</label>

{{-- ❌ WRONG - Hardcoded text --}}
<h1>Dashboard</h1>
```

### 3. Filament (Admin & Owner Panels)

```php
<?php

use Filament\Forms;
use Filament\Tables;

// ✅ CORRECT - Form fields
Forms\Components\TextInput::make('name')
    ->label(__('fields.name'))
    ->placeholder(__('fields.name'))
    ->required();

// ✅ CORRECT - Table columns
Tables\Columns\TextColumn::make('name')
    ->label(__('fields.name'))
    ->searchable();

// ✅ CORRECT - Resource labels
public static function getNavigationLabel(): string
{
    return __('navigation.businesses');
}

public static function getLabel(): ?string
{
    return __('messages.resources.business');
}

// ❌ WRONG - Hardcoded labels
protected static ?string $navigationLabel = 'Businesses';
```

## Enums com Tradução

**CRÍTICO:** TODOS Enums DEVEM implementar interface `HasLabel` e usar translation keys.

```php
<?php

declare(strict_types=1);

namespace App\Enums;

use Filament\Support\Contracts\HasColor;
use Filament\Support\Contracts\HasLabel;

enum BusinessTypeEnum: string implements HasLabel, HasColor
{
    case RESTAURANT = 'restaurant';
    case CAFE = 'cafe';

    // ✅ CORRECT - Using translation keys
    public function label(): string
    {
        return match ($this) {
            self::RESTAURANT => __('enums.business_type.restaurant'),
            self::CAFE => __('enums.business_type.cafe'),
        };
    }

    public function color(): string
    {
        return match ($this) {
            self::RESTAURANT => 'success',
            self::CAFE => 'warning',
        };
    }

    // Helper for Filament Select
    public static function toSelectArray(): array
    {
        return collect(self::cases())
            ->mapWithKeys(fn ($case) => [$case->value => $case->label()])
            ->toArray();
    }

    // ❌ WRONG - Hardcoded labels
    public function label(): string
    {
        return match ($this) {
            self::RESTAURANT => 'Restaurant',
            self::CAFE => 'Café',
        };
    }
}
```

## Mensagens de Validação

### Custom Validation (Form Requests)

```php
<?php

declare(strict_types=1);

namespace App\Http\Requests\Business;

use Illuminate\Foundation\Http\FormRequest;

final class StoreBusinessRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'email'],
        ];
    }

    // ✅ CORRECT - Custom messages with translations
    public function messages(): array
    {
        return [
            'name.required' => __('validation.custom.name.required'),
            'email.required' => __('validation.custom.email.required'),
        ];
    }

    // ✅ CORRECT - Custom attribute names
    public function attributes(): array
    {
        return [
            'name' => __('fields.name'),
            'email' => __('fields.email'),
        ];
    }
}
```

## Pluralização

```php
<?php

// lang/en/messages.php
return [
    'items_count' => '{0} No items|{1} :count item|[2,*] :count items',
];

// lang/es/messages.php
return [
    'items_count' => '{0} Sin ítems|{1} :count ítem|[2,*] :count ítems',
];

// lang/pt_BR/messages.php
return [
    'items_count' => '{0} Nenhum item|{1} :count item|[2,*] :count itens',
];
```

**Usage:**

```php
$count = 0;
echo trans_choice('messages.items_count', $count, ['count' => $count]);
// Output: "No items" (en) / "Sin ítems" (es) / "Nenhum item" (pt_BR)

$count = 5;
echo trans_choice('messages.items_count', $count, ['count' => $count]);
// Output: "5 items" (en) / "5 ítems" (es) / "5 itens" (pt_BR)
```

## Testando Traduções

**CRÍTICO:** SEMPRE teste que traduções existem para todos os 3 idiomas.

```php
<?php

use function Pest\Laravel\{actingAs, get, post};

it('displays translated dashboard title in all languages', function () {
    actingAs(User::factory()->create());

    // Test English
    app()->setLocale('en');
    get('/dashboard')
        ->assertSee(__('messages.dashboard'));

    // Test Spanish
    app()->setLocale('es');
    get('/dashboard')
        ->assertSee(__('messages.dashboard'));

    // Test Portuguese BR
    app()->setLocale('pt_BR');
    get('/dashboard')
        ->assertSee(__('messages.dashboard'));
});

it('validates with translated error messages', function () {
    actingAs(User::factory()->create());

    app()->setLocale('en');

    post('/businesses', [])
        ->assertSessionHasErrors('name')
        ->assertSee(__('validation.required', ['attribute' => __('fields.name')]));
});

it('enum returns translated labels in all languages', function () {
    app()->setLocale('en');
    expect(BusinessTypeEnum::RESTAURANT->label())->toBe('Restaurant');

    app()->setLocale('es');
    expect(BusinessTypeEnum::RESTAURANT->label())->toBe('Restaurante');

    app()->setLocale('pt_BR');
    expect(BusinessTypeEnum::RESTAURANT->label())->toBe('Restaurante');
});

// Test that all translation keys exist
it('has all required translation keys', function () {
    $requiredKeys = [
        'messages.welcome',
        'messages.dashboard',
        'fields.name',
        'fields.email',
    ];

    foreach (['en', 'es', 'pt_BR'] as $locale) {
        app()->setLocale($locale);

        foreach ($requiredKeys as $key) {
            expect(__($key))
                ->not->toBe($key)
                ->and(__($key))
                ->not->toBeEmpty();
        }
    }
});
```

## Middleware & Detecção de Locale

```php
<?php

// config/app.php
'locale' => 'en',
'fallback_locale' => 'en',
'locales' => ['en', 'es', 'pt_BR'],

// Middleware para definir locale baseado em preferência do usuário
namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

final class SetLocale
{
    public function handle(Request $request, Closure $next)
    {
        // Priority: User preference > Session > Browser > Default
        $locale = $request->user()?->locale
            ?? session('locale')
            ?? $this->detectBrowserLocale($request)
            ?? config('app.locale');

        if (in_array($locale, config('app.locales'))) {
            app()->setLocale($locale);
            session(['locale' => $locale]);
        }

        return $next($request);
    }

    private function detectBrowserLocale(Request $request): ?string
    {
        $browserLang = substr($request->server('HTTP_ACCEPT_LANGUAGE', ''), 0, 2);

        return match ($browserLang) {
            'en' => 'en',
            'es' => 'es',
            'pt' => 'pt_BR',
            default => null,
        };
    }
}
```

## Convenção de Nomenclatura de Translation Keys

| Contexto | Padrão | Exemplo |
|----------|----------|---------|
| **Messages** | `messages.{context}.{action}` | `messages.auth.login_success` |
| **Fields** | `fields.{field_name}` | `fields.email`, `fields.password` |
| **Enums** | `enums.{enum_name}.{value}` | `enums.business_type.restaurant` |
| **Validation** | `validation.custom.{field}` | `validation.custom.email.required` |
| **Exceptions** | `exceptions.{exception_type}` | `exceptions.business_limit` |
| **Navigation** | `navigation.{item}` | `navigation.dashboard` |
| **Resources** | `messages.resources.{name}` | `messages.resources.business` |

## Melhores Práticas

### ✅ FAÇA

- Sempre use `__()` para TODO texto voltado ao usuário
- Organize translation keys por domínio/feature
- Use nomes de keys semânticos (ex: `messages.welcome`, não `messages.text1`)
- Mantenha traduções sincronizadas através de todos idiomas (EN, ES, PT-BR)
- Use replacement de parâmetros para conteúdo dinâmico (`:name`, `:count`, etc.)
- Implemente interface `HasLabel` em TODOS Enums
- Teste traduções em todos idiomas suportados
- Use pluralização para itens contáveis
- Providencie contexto em translation keys (ex: `auth.login` vs `navigation.login`)
- **Publique e traduza pacotes vendor**
- **Descomente e complete todos arrays de tradução vendor**
- **Teste traduções de pacotes vendor em todos idiomas**

### ❌ NÃO FAÇA

- Não hardcode strings de texto
- Não use strings em inglês como keys (use keys semânticas em vez disso)
- Não esqueça de adicionar traduções para novas features
- Não misture texto hardcoded com traduções
- Não use concatenação de strings para traduções
- Não skip tradução para palavras "óbvias" como "OK" ou "Cancel"
- Não use keys genéricas como `message1`, `text2`, etc.
- Não esqueça de traduzir mensagens de validação
- Não use estruturas de keys diferentes através de arquivos
- **Não deixe traduções vendor comentadas**
- **Não skip traduzindo pacotes third-party**
- **Não assuma que pacotes vendor já estão traduzidos**

## Checklist de Referência Rápida

Antes de finalizar QUALQUER feature:

- [ ] Todo texto voltado ao usuário usa `__()`
- [ ] Traduções adicionadas para EN, ES, PT-BR
- [ ] Enums implementam `HasLabel` com `__()`
- [ ] Mensagens de validação de form traduzidas
- [ ] Mensagens de sucesso/erro traduzidas
- [ ] Items de navegação traduzidos
- [ ] Labels de campos traduzidos
- [ ] Resources Filament traduzidos
- [ ] Testes verificam que traduções funcionam em todos 3 idiomas
- [ ] Sem strings hardcoded no código

## Padrões de Tradução Comuns

```php
// ✅ Success messages
return redirect()
    ->route('businesses.index')
    ->with('success', __('messages.created_successfully', [
        'resource' => __('messages.resources.business')
    ]));

// ✅ Flash messages
session()->flash('success', __('messages.saved_successfully', [
    'resource' => __('messages.resources.menu_item')
]));

// ✅ Exception messages
throw new BusinessLimitExceededException(
    message: __('exceptions.business_limit_exceeded', [
        'current' => $currentCount,
        'max' => $maxAllowed,
        'plan' => $tenant->plan->name,
    ])
);

// ✅ Filament notifications
Notification::make()
    ->title(__('messages.created_successfully', [
        'resource' => __('messages.resources.business')
    ]))
    ->success()
    ->send();
```

## Referências Cruzadas

- **Exceções**: Integrado com `laravel-exceptions` para traduções de mensagens de erro
- **Filament**: Veja `laravel-filament` para tradução completa de Resources e Widgets
- **Architecture**: Integrado com `laravel-architecture` para Enums traduzíveis
- **Actions/Events**: Integrado com `laravel-actions-events` para traduções de eventos

## Referências

- [Laravel Localization Documentation](https://laravel.com/docs/localization) - Documentação oficial
