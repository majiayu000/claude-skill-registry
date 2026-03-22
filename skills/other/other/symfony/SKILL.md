---
name: symfony
description: |
  Symfony 7+ framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Symfony projects, or when the user mentions Symfony.
  Provides Doctrine ORM, Twig templates, bundles, services, and security guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: php
  extensions: ".php"
---

# Symfony Framework Guide

> Applies to: Symfony 7+, PHP 8.2+, Doctrine ORM, Twig, Messenger

## Core Principles

1. **Convention Over Configuration**: Follow Symfony defaults unless there is a strong reason not to
2. **Dependency Injection**: Constructor injection for all services; avoid service locators
3. **Thin Controllers**: Controllers delegate to services; no business logic in controllers
4. **DTOs at Boundaries**: Never expose Doctrine entities directly to API consumers
5. **Events for Decoupling**: Use EventDispatcher and Messenger for side effects
6. **Explicit Configuration**: Use PHP 8 attributes for routing, ORM mapping, and validation

## Guardrails

### Version and Dependencies

- Target Symfony 7.x with PHP 8.2+
- Use Composer with `composer.lock` committed
- Use Symfony Flex for bundle management
- Pin major versions in `composer.json`; run `composer audit` before adding dependencies

### Code Style

- All files start with `declare(strict_types=1);`
- Use PSR-12 coding standard; run `php-cs-fixer fix` before committing
- Run PHPStan at level 8+ (`vendor/bin/phpstan analyse src`)
- Use PHP 8 attributes (not annotations) for routing, ORM, validation
- Follow Symfony naming: `PascalCase` classes, `camelCase` methods, `snake_case` config keys

### Controller Rules

- Extend `AbstractController` only when you need its shortcuts
- One action per method; keep under 20 lines
- Use `#[Route]` attribute on both class and method
- Use `#[MapRequestPayload]` for automatic DTO deserialization and validation
- Return `JsonResponse` for APIs; never `echo` or `die()`
- Use serialization groups to control response shape

### Entity Rules

- Use PHP 8 attributes for all Doctrine mapping (`#[ORM\Entity]`, `#[ORM\Column]`, etc.)
- Always set `repositoryClass` on entities
- Use `#[ORM\HasLifecycleCallbacks]` sparingly; prefer Doctrine event listeners
- Initialize collections in constructor: `$this->items = new ArrayCollection()`
- Use `DateTimeImmutable` for all date columns
- Add database indexes for frequently queried columns with `#[ORM\Index]`
- Fluent setters return `static` for chaining

### Service Rules

- One responsibility per service class
- All dependencies via constructor injection (use `readonly` promoted properties)
- Never inject `EntityManagerInterface` into controllers; inject repositories or services
- Use `#[AsMessageHandler]` for async operations
- Tag services only when autowiring cannot resolve

## Project Structure

```
myapp/
├── bin/
│   └── console                # Symfony CLI
├── config/
│   ├── packages/             # Per-package YAML config
│   │   ├── doctrine.yaml
│   │   ├── security.yaml
│   │   ├── messenger.yaml
│   │   └── ...
│   ├── routes/               # Route imports
│   ├── routes.yaml
│   ├── services.yaml         # Service definitions and autowiring
│   └── bundles.php           # Registered bundles
├── migrations/               # Doctrine migrations (never edit after deploy)
├── public/
│   └── index.php            # Single entry point
├── src/
│   ├── Controller/          # HTTP controllers (thin)
│   ├── Dto/                 # Request/response DTOs
│   ├── Entity/              # Doctrine entities
│   ├── Repository/          # Doctrine repositories
│   ├── Service/             # Business logic
│   ├── EventSubscriber/     # Event subscribers
│   ├── Message/             # Messenger messages
│   ├── MessageHandler/      # Messenger handlers
│   ├── Command/             # Console commands
│   ├── Form/                # Form types (web apps)
│   ├── Security/            # Voters, authenticators
│   └── Kernel.php
├── templates/               # Twig templates
├── tests/
│   ├── Controller/          # Functional tests
│   ├── Service/             # Unit tests
│   └── bootstrap.php
├── translations/            # i18n files
├── var/                     # Cache and logs (gitignored)
├── .env                     # Default env vars (committed)
├── .env.local               # Local overrides (gitignored)
├── composer.json
├── phpunit.xml.dist
└── symfony.lock
```

- `src/Dto/` keeps request/response data separate from entities
- `src/Message/` and `src/MessageHandler/` follow Messenger conventions
- `var/` is ephemeral; never store persistent data there
- `config/packages/` files are loaded by environment (`config/packages/test/`)

## Controllers and Routing

### API Controller

```php
#[Route('/api/v1/users')]
class UserController extends AbstractController
{
    public function __construct(
        private readonly UserService $userService,
    ) {}

    #[Route('', methods: ['GET'])]
    public function index(Request $request): JsonResponse
    {
        $page = $request->query->getInt('page', 1);
        $limit = $request->query->getInt('limit', 15);

        return $this->json(
            $this->userService->getPaginated($page, $limit),
            Response::HTTP_OK,
            [],
            ['groups' => 'user:read'],
        );
    }

    #[Route('', methods: ['POST'])]
    #[IsGranted('ROLE_ADMIN')]
    public function create(#[MapRequestPayload] CreateUserDto $dto): JsonResponse
    {
        return $this->json(
            $this->userService->create($dto),
            Response::HTTP_CREATED,
            [],
            ['groups' => 'user:read'],
        );
    }
}
```

### Routing Tips

- Prefer attribute routing over YAML for controller routes
- Use YAML routes only for third-party bundle prefixes
- Version API routes: `/api/v1/...`
- Type-hint entities in action signatures for automatic `ParamConverter`

## Doctrine ORM Basics

### Entity with Validation

```php
<?php

declare(strict_types=1);

namespace App\Entity;

use App\Repository\UserRepository;
use Doctrine\DBAL\Types\Types;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Validator\Constraints as Assert;

#[ORM\Entity(repositoryClass: UserRepository::class)]
#[ORM\Table(name: 'users')]
#[ORM\HasLifecycleCallbacks]
class User
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 180, unique: true)]
    #[Assert\NotBlank]
    #[Assert\Email]
    private string $email;

    #[ORM\Column(type: Types::DATETIME_IMMUTABLE)]
    private \DateTimeImmutable $createdAt;

    public function __construct()
    {
        $this->createdAt = new \DateTimeImmutable();
    }

    // Getters and fluent setters (return static)
}
```

### Repository

```php
<?php

declare(strict_types=1);

namespace App\Repository;

use App\Entity\User;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

/** @extends ServiceEntityRepository<User> */
class UserRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, User::class);
    }

    public function findOneByEmail(string $email): ?User
    {
        return $this->createQueryBuilder('u')
            ->andWhere('u.email = :email')
            ->setParameter('email', strtolower($email))
            ->getQuery()
            ->getOneOrNullResult();
    }
}
```

### Migration Workflow

```bash
php bin/console make:migration           # Generate from entity diff
php bin/console doctrine:migrations:migrate  # Apply migrations
php bin/console doctrine:schema:validate     # Check mapping vs DB
```

- Always review generated migrations before running
- Every migration must have a working `down()` method
- Never edit migrations that have been applied to production

## Twig Templates

### Layout Pattern

```twig
{# templates/base.html.twig #}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}App{% endblock %}</title>
    {% block stylesheets %}{% endblock %}
</head>
<body>
    {% block body %}{% endblock %}
    {% block javascripts %}{% endblock %}
</body>
</html>

{# templates/user/index.html.twig #}
{% extends 'base.html.twig' %}

{% block title %}Users{% endblock %}

{% block body %}
    <h1>Users</h1>
    {% for user in users %}
        <p>{{ user.name|e }}</p>
    {% else %}
        <p>No users found.</p>
    {% endfor %}
{% endblock %}
```

- Always escape output (Twig auto-escapes by default; never use `|raw` on user data)
- Use `{% include %}` for partials, `{% embed %}` for overridable partials
- Keep logic minimal in templates; compute values in controller or service

## Services and Dependency Injection

### Service Definition

```php
class UserService
{
    public function __construct(
        private readonly UserRepository $userRepository,
        private readonly EntityManagerInterface $entityManager,
        private readonly UserPasswordHasherInterface $passwordHasher,
        private readonly EventDispatcherInterface $eventDispatcher,
    ) {}

    public function create(CreateUserDto $dto): User
    {
        $user = new User();
        $user->setEmail($dto->email);
        $user->setPassword($this->passwordHasher->hashPassword($user, $dto->password));

        $this->entityManager->persist($user);
        $this->entityManager->flush();

        $this->eventDispatcher->dispatch(new UserCreatedEvent($user));

        return $user;
    }
}
```

### services.yaml Essentials

```yaml
services:
    _defaults:
        autowire: true
        autoconfigure: true

    App\:
        resource: '../src/'
        exclude:
            - '../src/DependencyInjection/'
            - '../src/Entity/'
            - '../src/Kernel.php'
```

- Rely on autowiring; only add explicit definitions when needed
- Use `#[Autowire]` attribute for non-standard parameters
- Use `#[TaggedIterator]` to inject all services with a specific tag

## Form Handling

```php
class UserType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $builder
            ->add('name', TextType::class)
            ->add('email', EmailType::class);
    }

    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults(['data_class' => User::class]);
    }
}
```

- Always bind forms to a DTO or entity via `data_class`
- Validate via constraints on the DTO/entity, not in the form type
- Use CSRF protection (enabled by default for web forms)
- For APIs, prefer `#[MapRequestPayload]` over Symfony forms

## Security Basics

### Voter Pattern

```php
class PostVoter extends Voter
{
    public const EDIT = 'POST_EDIT';
    public const DELETE = 'POST_DELETE';

    protected function supports(string $attribute, mixed $subject): bool
    {
        return in_array($attribute, [self::EDIT, self::DELETE], true)
            && $subject instanceof Post;
    }

    protected function voteOnAttribute(
        string $attribute,
        mixed $subject,
        TokenInterface $token,
    ): bool {
        $user = $token->getUser();
        if (!$user instanceof User) {
            return false;
        }

        return $subject->getAuthor() === $user || $user->getRole() === 'admin';
    }
}
```

### Security Configuration Checklist

- Use `password_hashers: auto` (Symfony picks bcrypt/argon2 automatically)
- Stateless firewalls for APIs (`stateless: true`)
- JWT authentication via `lexik/jwt-authentication-bundle` for APIs
- CSRF protection enabled for all web forms
- Use `#[IsGranted]` attribute on controller actions
- Use Voters for object-level authorization (not `is_granted('ROLE_...')` for fine-grained checks)
- Never store plain-text passwords; always use `UserPasswordHasherInterface`

## Console Commands

```php
#[AsCommand(name: 'app:import-users', description: 'Import users from CSV')]
class ImportUsersCommand extends Command
{
    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $io = new SymfonyStyle($input, $output);
        // Implementation here
        $io->success('Import complete.');
        return Command::SUCCESS;
    }
}
```

- Use `#[AsCommand]` attribute (not `configure()` for name/description)
- Return `Command::SUCCESS`, `Command::FAILURE`, or `Command::INVALID`
- Use `SymfonyStyle` for consistent output formatting
- Inject services via constructor (commands are services)

## Essential CLI Commands

```bash
# Development
symfony serve                              # Local dev server
php bin/console cache:clear                # Clear cache
php bin/console debug:router               # List all routes
php bin/console debug:container            # List all services

# Code Generation
php bin/console make:entity User
php bin/console make:controller UserController
php bin/console make:migration
php bin/console make:form UserType
php bin/console make:voter PostVoter
php bin/console make:command App:ImportUsers
php bin/console make:subscriber UserEventSubscriber
php bin/console make:message SendWelcomeEmail

# Database
php bin/console doctrine:database:create
php bin/console doctrine:migrations:migrate
php bin/console doctrine:schema:validate
php bin/console doctrine:fixtures:load

# Messenger
php bin/console messenger:consume async
php bin/console messenger:failed:show
php bin/console messenger:failed:retry

# Testing and Quality
php bin/phpunit
php bin/phpunit --coverage-html coverage
vendor/bin/phpstan analyse src
vendor/bin/php-cs-fixer fix

# Production
composer install --no-dev --optimize-autoloader
php bin/console cache:clear --env=prod
php bin/console cache:warmup --env=prod
```

## Do and Don't

### Do

- Use constructor injection with `readonly` promoted properties
- Use DTOs for all API request/response payloads
- Use Messenger for async work (emails, notifications, heavy processing)
- Use Voters for authorization logic
- Use Events for decoupling side effects from core logic
- Use serialization groups to control JSON output shape
- Use `DateTimeImmutable` for all temporal data
- Run `php bin/console doctrine:schema:validate` in CI

### Don't

- Don't put business logic in controllers (delegate to services)
- Don't flush `EntityManager` inside loops (batch with `$em->flush()` once)
- Don't use `$_GET`, `$_POST`, `$_SERVER` (use `Request` object)
- Don't hardcode config values (use `%env()%` syntax or `#[Autowire]`)
- Don't bypass the security component (no manual session/cookie auth)
- Don't create "god services" that handle everything (single responsibility)
- Don't ignore Symfony deprecation warnings (they become errors on upgrade)

## Advanced Topics

For detailed patterns and production guidance, see:

- [references/patterns.md](references/patterns.md) -- Doctrine advanced patterns, event system, Messenger, API Platform, testing, deployment

## External References

- [Symfony Documentation](https://symfony.com/doc/current/index.html)
- [Symfony Best Practices](https://symfony.com/doc/current/best_practices.html)
- [Doctrine ORM](https://www.doctrine-project.org/projects/orm.html)
- [API Platform](https://api-platform.com/)
- [Symfony Casts](https://symfonycasts.com/)
- [PHP-FIG PSR Standards](https://www.php-fig.org/psr/)
