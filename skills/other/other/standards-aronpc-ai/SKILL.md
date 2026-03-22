---
name: standards
description: >-
  Aplica padrões de código Spatie + Laravel Pint para consistência. Use quando precisar verificar ou configurar code style, padrões de nomenclatura, ou formatação de código PHP.
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

# standards

## Resumo
Mantém padrões de código Laravel baseados nas diretrizes da Spatie com Laravel Pint.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `coder` | Para seguir padrões durante implementação |
| `pr-review` | Para verificar aderência em reviews |
| `qa` | Para validação de estilo |
| `workflow` | Para pre-commit hooks |
| `architecture` | Para padrões arquiteturais |

## Quando usar

Use esta skill sempre que:
- Escrever qualquer código PHP/Laravel
- Revisar código existente
- Aplicar formatação com `composer fix`
- Manter consistência no estilo do código
- Revisar pull requests

## Princípios Fundamentais

### Core Laravel Principle

**Siga as convenções do Laravel primeiro.** Se o Laravel tem uma forma documentada de fazer algo, use-a. Só desvie quando tiver justificativa clara.

### PHP Standards

- Siga PSR-1, PSR-2 e PSR-12
- Use camelCase para strings não-públicas
- Use notação curta para nullable: `?string` não `string|null`
- Sempre especifique tipos de retorno `void` quando métodos não retornam nada

## Estrutura de Classes

### Propriedades Tipadas

Use propriedades tipadas, não docblocks:

```php
final class UserService
{
    public function __construct(
        private readonly UserRepository $repository,
        private readonly Cache $cache,
    ) {}
}
```

### Constructor Property Promotion

Use quando todas as propriedades podem ser promovidas:

```php
// ✅ TODAS as propriedades podem ser promovidas
final class UserService
{
    public function __construct(
        private readonly UserRepository $repository,
        private readonly Cache $cache,
    ) {}
}

// ❌ Algumas propriedades não podem ser promovidas
final class UserService
{
    private UserRepository $repository;
    private array $config;

    public function __construct(
        UserRepository $repository,
        array $config,
    ) {
        $this->repository = $repository;
        $this->config = $config;
    }
}
```

### Traits

Um trait por linha:

```php
final class Business extends Model
{
    use HasFactory;
    use SoftDeletes;
    use Notifiable;
}
```

## Declarações de Tipo e Docblocks

### Tipos vs Docblocks

- Use propriedades tipadas sobre docblocks
- Especifique tipos de retorno incluindo `void`
- Use sintaxe curta de nullable: `?Type` não `Type|null`
- Documente iterables com generics:

```php
/** @return Collection<int, User> */
public function getUsers(): Collection
{
    return User::all();
}
```

### Regras de Docblock

- Não use docblocks para métodos totalmente tipados (a menos que descrição seja necessária)
- **Sempre importe nomes de classes em docblocks** - nunca use nomes totalmente qualificados:

```php
use Spatie\Url\Url;

/** @return Url */
public function getUrl(): Url
{
    return Url::fromString($this->url);
}
```

- Use docblocks de uma linha quando possível: `/** @var string */`
- Tipo mais comum deve ser primeiro em docblocks multi-tipo:

```php
/** @var Collection|SomeWeirdVendor\Collection */
```

- Se um parâmetro precisa de docblock, adicione docblocks para todos os parâmetros
- Para iterables, sempre especifique tipos de chave e valor:

```php
/**
 * @param array<int, MyObject> $myArray
 * @param int $typedArgument
 */
function someFunction(array $myArray, int $typedArgument) {}
```

- Use notação de shape de array para chaves fixas, cada chave em sua própria linha:

```php
/** @return array{
 *   first: SomeClass,
 *   second: SomeClass
 * } */
```

## Fluxo de Controle

### Happy Path Last

Trate condições de erro primeiro, caso de sucesso último:

```php
// ✅ GOOD - Happy path last
if (!$user) {
    return null;
}

if (!$user->isActive()) {
    return null;
}

// Process active user...
return $this->processUser($user);
```

### Early Returns

Use early returns em vez de condições aninhadas:

```php
// ❌ BAD - Aninhado
if ($user) {
    if ($user->isActive()) {
        if ($user->hasPermission()) {
            return $this->processUser($user);
        }
    }
}

// ✅ GOOD - Early returns
if (!$user) {
    return null;
}

if (!$user->isActive()) {
    return null;
}

if (!$user->hasPermission()) {
    return null;
}

return $this->processUser($user);
```

### Separe Condições

Preira múltiplas instruções if sobre condições compostas:

```php
// ❌ BAD - Condição composta
if ($user && $user->isActive() && $user->hasPermission()) {
    return $this->processUser($user);
}

// ✅ GOOD - Condições separadas
if (!$user) {
    return null;
}

if (!$user->isActive()) {
    return null;
}

if (!$user->hasPermission()) {
    return null;
}

return $this->processUser($user);
```

### Chaves e Operadores Ternários

- **Sempre use chaves** mesmo para instruções simples
- **Operadores ternários**: cada parte em sua própria linha a menos que muito curto

```php
// Ternário curto
$name = $isFoo ? 'foo' : 'bar';

// Ternário multi-linha
$result = $object instanceof Model
    ? $object->name
    : 'A default value';

// Ternário em vez de else
$condition
    ? $this->doSomething()
    : $this->doSomethingElse();
```

## Convenções Laravel

### Rotas

- URLs: kebab-case (`/open-source`)
- Nomes de rotas: camelCase (`->name('openSource')`)
- Parâmetros: camelCase (`{userId}`)
- Use notação de tupla: `[Controller::class, 'method']`

### Controllers

- Nomes de recursos no plural (`PostsController`)
- Mantenha métodos CRUD (`index`, `create`, `store`, `show`, `edit`, `update`, `destroy`)
- Extraia novos controllers para ações não-CRUD

### Configuração

- Arquivos: kebab-case (`pdf-generator.php`)
- Chaves: snake_case (`chrome_path`)
- Adicione configs de serviço a `config/services.php`, não crie novos arquivos
- Use helper `config()`, evite `env()` fora de arquivos de config

### Artisan Commands

- Nomes: kebab-case (`delete-old-records`)
- Sempre fornecer feedback (`$this->comment('All ok!')`)
- Mostre progresso para loops, resumo no fim
- Coloque output ANTES de processar item (mais fácil para debug):

```php
$items->each(function (Item $item) {
    $this->info("Processing item id `{$item->id}`...");
    $this->processItem($item);
});

$this->comment("Processed {$items->count()} items.");
```

## Strings e Formatação

### Interpolação de Strings

Use **interpolação de strings** sobre concatenação:

```php
// ❌ BAD - Concatenação
$name = 'Hello, ' . $user->name . '!';

// ✅ GOOD - Interpolação
$name = "Hello, {$user->name}!";
```

### Enums

Use PascalCase para valores de enum:

```php
enum BusinessTypeEnum: string
{
    case RESTAURANT = 'restaurant';
    case CAFE = 'cafe';
    case BAR = 'bar';
}
```

## Comentários

### Evite Comentários

Escreva código expressivo em vez de comentários:

```php
// ❌ BAD - Comentário explicando o quê
// Check if user is active
if ($user->isActive()) {
    return $user;
}

// ✅ GOOD - Código auto-explicativo
if ($user->isActive()) {
    return $user;
}
```

### Quando Usar Comentários

Use formatação adequada quando necessário:

```php
// Single line with space after //

/*
 * Multi-line blocks start with single *
 */
```

- Refatore comentários em nomes de funções descritivas

## Espaço em Branco

- Adicione linhas em branco entre instruções para legibilidade
- Exceção: sequências de operações single-line equivalentes
- Sem linhas extras extras entre chaves `{}`
- Deixe o código "respirar" - evite formatação apertada

## Validação

Use notação de array para múltiplas regras (mais fácil para classes de regra customizadas):

```php
public function rules(): array
{
    return [
        'email' => ['required', 'email'],
        'password' => ['required', 'min:8', 'confirmed'],
    ];
}
```

Regras de validação customizadas usam snake_case:

```php
Validator::extend('organisation_type', function ($attribute, $value) {
    return OrganisationType::isValid($value);
});
```

## Templates Blade

- Indente com 4 espaços
- Sem espaços após estruturas de controle:

```blade
@if($condition)
    Something
@endif
```

## Autorização

- Policies usam camelCase: `Gate::define('editPost', ...)`
- Use palavras CRUD, mas `view` em vez de `show`

## Traduções

Use função `__()` sobre `@lang`:

```blade
{{ __('messages.welcome') }}
```

## Rotas API

- Use nomes de recursos no plural: `/errors`
- Use kebab-case: `/error-occurrences`
- Limite aninhamento profundo para simplicidade:

```php
// ✅ GOOD
/error-occurrences/1
/errors/1/occurrences

// ❌ BAD - Muito aninhado
/tenants/1/businesses/1/locations/1/menu-items/1
```

## Testes

- Mantenha classes de teste no mesmo arquivo quando possível
- Use nomes de métodos de teste descritivos
- Siga padrão arrange-act-assert

## Referência Rápida

### Convenções de Nomenclatura

| Tipo | Convenção | Exemplo |
|------|------------|----------|
| **Classes** | PascalCase | `UserController`, `OrderStatus` |
| **Methods/Variables** | camelCase | `getUserName`, `$firstName` |
| **Routes** | kebab-case | `/open-source`, `/user-profile` |
| **Config files** | kebab-case | `pdf-generator.php` |
| **Config keys** | snake_case | `chrome_path` |
| **Artisan commands** | kebab-case | `php artisan delete-old-records` |

### Estrutura de Arquivos

| Tipo | Convenção | Exemplo |
|------|------------|----------|
| **Controllers** | plural resource name + `Controller` | `PostsController` |
| **Views** | camelCase | `openSource.blade.php` |
| **Jobs** | action-based | `CreateUser`, `SendEmailNotification` |
| **Events** | tense-based | `UserRegistering`, `UserRegistered` |
| **Listeners** | action + `Listener` suffix | `SendInvitationMailListener` |
| **Commands** | action + `Command` suffix | `PublishScheduledPostsCommand` |
| **Mailables** | purpose + `Mail` suffix | `AccountActivatedMail` |
| **Resources/Transformers** | plural + `Resource`/`Transformer` | `UsersResource` |
| **Enums** | descriptive name, no prefix | `OrderStatus`, `BookingType` |

### Migrations

Não escreva métodos `down` em migrations, apenas métodos `up`:

```php
public function up(): void
{
    Schema::create('table', function (Blueprint $table) {
        // ...
    });
}
```

## Lembrete de Qualidade de Código

### PHP

- Use propriedades tipadas sobre docblocks
- Prefira early returns sobre if/else aninhados
- Use constructor property promotion quando todas as propriedades podem ser promovidas
- Evite instruções `else`
- Use interpolação de strings sobre concatenação
- Sempre use chaves para estruturas de controle

## Referências

- [Spatie Guidelines](https://spatie.be/guidelines) - Fonte oficial dos padrões
