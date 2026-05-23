---
name: enums
description: >-
  Cria e gerencia Enums PHP 8.1+ com archtechx/enums e suas 7 traits helpers. Use quando precisar criar enums, adicionar traits de enum, ou trabalhar com enums tipados em Laravel.
compatibility: PHP 8.1+, archtechx/enums
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

# enums

## Resumo
Cria e mantém Enums PHP 8.1+ usando archtechx/enums com 7 traits helpers.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `models` | Para usar enums em cast de Models |
| `i18n` | Para enums traduzíveis |
| `testing` | Para testar enums |
| `architecture` | Para usar enums em DTOs |

## Instalação

```bash
composer require archtechx/enums
```

## Quando usar

Use esta skill quando:
- Criar ou modificar enums PHP no projeto Laravel
- Precisar de métodos helpers para enums (names, values, options, etc.)
- Implementar comparações entre enums
- Adicionar metadados aos cases do enum
- Cast enums em modelos Eloquent
- Validar inputs usando enums

## Os 7 Traits Disponíveis

### 1. InvokableCases - Invocação de Enums

Permite obter o valor de um backed enum ou o nome de um pure enum através de "invocação".

```php
use ArchTech\Enums\InvokableCases;

enum TaskStatus: int
{
    use InvokableCases;

    case INCOMPLETE = 0;
    case COMPLETED = 1;
    case CANCELED = 2;
}

// Chamada estática - retorna o valor
TaskStatus::INCOMPLETE();  // 0

// Invocação de instância
$status = TaskStatus::INCOMPLETE;
$status();  // 0

// Como chave de array (muito útil!)
$config = [
    TaskStatus::INCOMPLETE() => ['color' => 'gray'],
    TaskStatus::COMPLETED() => ['color' => 'green'],
];
```

### 2. Names - Lista de Nomes

Retorna array com os nomes dos cases.

```php
use ArchTech\Enums\Names;

enum TaskStatus: int
{
    use Names;

    case INCOMPLETE = 0;
    case COMPLETED = 1;
}

TaskStatus::names();
// ['INCOMPLETE', 'COMPLETED']
```

### 3. Values - Lista de Valores

Retorna array com os valores dos cases (ou nomes para pure enums).

```php
use ArchTech\Enums\Values;

enum TaskStatus: int
{
    use Values;

    case INCOMPLETE = 0;
    case COMPLETED = 1;
}

TaskStatus::values();
// [0, 1]
```

### 4. Options - Array Associativo

Retorna array associativo `nome => valor`.

```php
use ArchTech\Enums\Options;

enum TaskStatus: int
{
    use Options;

    case INCOMPLETE = 0;
    case COMPLETED = 1;
}

TaskStatus::options();
// ['INCOMPLETE' => 0, 'COMPLETED' => 1]

// stringOptions() - gera HTML <option>
TaskStatus::stringOptions();
// <option value="0">Incomplete</option>
// <option value="1">Completed</option>
```

### 5. From - From/Name Resolution

Adiciona `from()` e `tryFrom()` para pure enums, e `fromName()`/`tryFromName()` para todos.

```php
use ArchTech\Enums\From;

enum Role
{
    use From;

    case ADMIN;
    case USER;
}

Role::from('ADMIN');          // Role::ADMIN
Role::tryFrom('GHOST');       // null
Role::fromName('ADMIN');      // Role::ADMIN (para backed enums)
```

### 6. Metadata - Metadados com Atributos

Permite adicionar metadados aos cases usando atributos PHP 8.

```php
use ArchTech\Enums\Metadata;
use ArchTech\Enums\Meta\Meta;

#[Meta(Description::class, Color::class)]
enum TaskStatus: int
{
    use Metadata;

    #[Description('Tarefa Pendente')] #[Color('yellow')]
    case PENDING = 0;

    #[Description('Concluída')] #[Color('green')]
    case COMPLETED = 1;
}

// Acessar metadados
TaskStatus::PENDING->description();  // 'Tarefa Pendente'
TaskStatus::PENDING->color();        // 'yellow'
```

**Criar MetaProperty personalizada:**

```php
use ArchTech\Enums\Meta\MetaProperty;

#[Attribute]
class Icon extends MetaProperty
{
    // Personalizar nome do método
    public static function method(): string
    {
        return 'icon';
    }

    // Transformar valor
    protected function transform(mixed $value): mixed
    {
        return "fa-{$value}";
    }

    // Valor padrão
    public static function defaultValue(): mixed
    {
        return 'fa-circle';
    }
}
```

**PHPDoc para suporte de IDE:**

```php
/**
 * @method string description()
 * @method string color()
 * @method string icon()
 */
#[Meta(Description::class, Color::class, Icon::class)]
enum TaskStatus: int
{
    use Metadata;

    #[Description('Pendente')] #[Color('yellow')] #[Icon('clock')]
    case PENDING = 0;
}
```

### 7. Comparable - Comparações

Permite comparar enums com `is()`, `isNot()`, `in()` e `notIn()`.

```php
use ArchTech\Enums\Comparable;

enum TaskStatus: int
{
    use Comparable;

    case PENDING = 0;
    case COMPLETED = 1;
}

TaskStatus::PENDING->is(TaskStatus::PENDING);           // true
TaskStatus::PENDING->isNot(TaskStatus::COMPLETED);      // true
TaskStatus::PENDING->in([TaskStatus::PENDING, TaskStatus::COMPLETED]);  // true
TaskStatus::PENDING->notIn([TaskStatus::COMPLETED]);    // true
```

## Integração com Laravel

### Cast em Modelos Eloquent

```php
use Illuminate\Database\Eloquent\Model;

class Task extends Model
{
    protected $casts = [
        'status' => TaskStatus::class,
    ];
}

// Uso
$task->status = TaskStatus::COMPLETED;
$task->save();  // Salva como integer no banco

// Recupera automaticamente como enum
$task->status;  // TaskStatus::COMPLETED (instância)
$task->status->value;  // 1
```

### Validação em Requests

```php
use Illuminate\Validation\Rule;

// Usando valores do enum
'status' => 'required|in:' . implode(',', TaskStatus::values())

// Usando Enum rule (Laravel 10+)
'status' => ['required', Rule::enum(TaskStatus::class)];
```

### Migration

```php
// Para backed enum int
$table->tinyInteger('status');

// Para backed enum string
$table->string('status');
```

## Padrões de Uso Recomendados

### Enum para Status com Metadata

```php
use ArchTech\Enums\{Metadata, Comparable, Options};
use ArchTech\Enums\Meta\Meta;

/**
 * @method string description()
 * @method string color()
 * @method string icon()
 */
#[Meta(Description::class, Color::class, Icon::class)]
enum TaskStatus: int
{
    use Metadata, Comparable, Options;

    #[Description('Pendente')] #[Color('yellow')] #[Icon('clock')]
    case PENDING = 0;

    #[Description('Em Andamento')] #[Color('blue')] #[Icon('spinner')]
    case IN_PROGRESS = 1;

    #[Description('Concluída')] #[Color('green')] #[Icon('check')]
    case COMPLETED = 2;

    #[Description('Cancelada')] #[Color('red')] #[Icon('times')]
    case CANCELED = 3;
}
```

### Enum para Permissões

```php
use ArchTech\Enums\{Comparable, From};

enum Permission: string
{
    use Comparable, From;

    case USER_READ = 'user.read';
    case USER_WRITE = 'user.write';
    case USER_DELETE = 'user.delete';
    case POST_READ = 'post.read';
    case POST_WRITE = 'post.write';
    case POST_DELETE = 'post.delete';

    // Verificar se é permissão de usuário
    public function isUserPermission(): bool
    {
        return str_starts_with($this->value, 'user.');
    }

    // Verificar se é permissão de post
    public function isPostPermission(): bool
    {
        return str_starts_with($this->value, 'post.');
    }
}

// Uso
if ($user->permission->is(Permission::USER_READ)) {
    // ...
}

if ($permission->isUserPermission()) {
    // ...
}
```

### Enum para Configuração

```php
use ArchTech\Enums\{InvokableCases, Values};

enum PaymentGateway: string
{
    use InvokableCases, Values;

    case STRIPE = 'stripe';
    case PAYPAL = 'paypal';
    case MERCADO_PAGO = 'mercadopago';
}

// Em arquivo de config
return [
    'gateways' => [
        PaymentGateway::STRIPE() => [
            'secret' => env('STRIPE_SECRET'),
            'webhook' => env('STRIPE_WEBHOOK'),
        ],
        PaymentGateway::PAYPAL() => [
            'secret' => env('PAYPAL_SECRET'),
            'webhook' => env('PAYPAL_WEBHOOK'),
        ],
    ],
];
```

## Diretório de Enums

No Laravel, mantenha enums em `app/Enums`:

```
app/
└── Enums/
    ├── TaskStatus.php
    ├── Permission.php
    ├── PaymentGateway.php
    └── MetaProperties/         # Atributos customizados
        ├── Description.php
        ├── Color.php
        └── Icon.php
```

## Referências Adicionais

- [Repositório GitHub](https://github.com/archtechx/enums)
- [Packagist](https://packagist.org/packages/archtechx/enums)
- [PHP 8.1 Enums](https://www.php.net/manual/pt_BR/language.types.enumerations.php)
