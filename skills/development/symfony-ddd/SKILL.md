---
name: symfony-ddd
description: Symfony 7 with Hexagonal Architecture, Domain-Driven Design (DDD), and CQRS patterns. Use this skill when implementing backend features, creating entities, commands, queries, repositories, or working with bounded contexts.
---

# Symfony DDD - Hexagonal Architecture Skill

This skill provides guidance for implementing features in the Family Plan backend using Hexagonal Architecture, DDD, and CQRS patterns.

## Architecture Overview

The backend follows a strict layered architecture within each Bounded Context:

```
BoundedContext/
├── Domain/           # Core business logic (no dependencies)
│   ├── Entity/       # Domain entities
│   ├── ValueObject/  # Value objects
│   ├── Event/        # Domain events
│   ├── Repository/   # Repository interfaces
│   └── Exception/    # Domain exceptions
├── Application/      # Use cases (depends only on Domain)
│   ├── Command/      # Commands and handlers
│   ├── Query/        # Queries and handlers
│   └── Service/      # Application services
└── Infrastructure/   # External adapters (implements Domain interfaces)
    ├── Doctrine/     # Database repositories
    ├── Http/         # External API clients
    └── Adapter/      # Other infrastructure adapters
```

## Bounded Contexts in This Project

- `UserManagement` - Authentication, user accounts, roles
- `TaskManagement` - Tasks, templates, executions, approvals
- `PointsManagement` - Points wallets, rewards system
- `TeamManagement` - Team organization, member invitations
- `UserSettings` - User preferences
- `Notifications` - Email/SMS notifications
- `Shared` - Shared kernel (common value objects, events)

## Implementation Patterns

### 1. Creating an Entity

```php
declare(strict_types=1);

namespace App\TaskManagement\Domain\Entity;

use App\Shared\Domain\ValueObject\Uuid;
use App\TaskManagement\Domain\Event\TaskCreated;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity]
#[ORM\Table(name: 'tasks')]
final class Task
{
    private array $domainEvents = [];

    private function __construct(
        #[ORM\Id]
        #[ORM\Column(type: 'uuid')]
        private Uuid $id,

        #[ORM\Column(type: 'string', length: 255)]
        private string $name,

        #[ORM\Column(type: 'datetime_immutable')]
        private \DateTimeImmutable $createdAt
    ) {}

    public static function create(Uuid $id, string $name): self
    {
        $task = new self($id, $name, new \DateTimeImmutable());
        $task->recordEvent(new TaskCreated($id));
        return $task;
    }

    public function id(): Uuid
    {
        return $this->id;
    }

    public function name(): string
    {
        return $this->name;
    }

    private function recordEvent(object $event): void
    {
        $this->domainEvents[] = $event;
    }

    public function pullDomainEvents(): array
    {
        $events = $this->domainEvents;
        $this->domainEvents = [];
        return $events;
    }
}
```

### 2. Creating a Command and Handler

```php
// Command
declare(strict_types=1);

namespace App\TaskManagement\Application\Command;

final readonly class CreateTaskCommand
{
    public function __construct(
        public string $id,
        public string $name,
        public string $teamId
    ) {}
}

// Handler
declare(strict_types=1);

namespace App\TaskManagement\Application\Command;

use App\Shared\Domain\ValueObject\Uuid;
use App\TaskManagement\Domain\Entity\Task;
use App\TaskManagement\Domain\Repository\TaskRepositoryInterface;
use Symfony\Component\Messenger\Attribute\AsMessageHandler;

#[AsMessageHandler]
final readonly class CreateTaskHandler
{
    public function __construct(
        private TaskRepositoryInterface $taskRepository
    ) {}

    public function __invoke(CreateTaskCommand $command): void
    {
        $task = Task::create(
            Uuid::fromString($command->id),
            $command->name
        );

        $this->taskRepository->save($task);
    }
}
```

### 3. Creating a Query and Handler

```php
// Query
declare(strict_types=1);

namespace App\TaskManagement\Application\Query;

final readonly class GetTaskQuery
{
    public function __construct(
        public string $taskId
    ) {}
}

// Handler
declare(strict_types=1);

namespace App\TaskManagement\Application\Query;

use App\TaskManagement\Domain\Repository\TaskRepositoryInterface;
use Symfony\Component\Messenger\Attribute\AsMessageHandler;

#[AsMessageHandler]
final readonly class GetTaskHandler
{
    public function __construct(
        private TaskRepositoryInterface $taskRepository
    ) {}

    public function __invoke(GetTaskQuery $query): ?TaskDTO
    {
        $task = $this->taskRepository->findById(
            Uuid::fromString($query->taskId)
        );

        return $task ? TaskDTO::fromEntity($task) : null;
    }
}
```

### 4. Repository Interface and Implementation

```php
// Interface (Domain layer)
declare(strict_types=1);

namespace App\TaskManagement\Domain\Repository;

use App\Shared\Domain\ValueObject\Uuid;
use App\TaskManagement\Domain\Entity\Task;

interface TaskRepositoryInterface
{
    public function save(Task $task): void;
    public function findById(Uuid $id): ?Task;
    public function findByTeamId(Uuid $teamId): array;
}

// Implementation (Infrastructure layer)
declare(strict_types=1);

namespace App\TaskManagement\Infrastructure\Doctrine;

use App\Shared\Domain\ValueObject\Uuid;
use App\TaskManagement\Domain\Entity\Task;
use App\TaskManagement\Domain\Repository\TaskRepositoryInterface;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

final class DoctrineTaskRepository extends ServiceEntityRepository implements TaskRepositoryInterface
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Task::class);
    }

    public function save(Task $task): void
    {
        $this->getEntityManager()->persist($task);
        $this->getEntityManager()->flush();
    }

    public function findById(Uuid $id): ?Task
    {
        return $this->find($id->toString());
    }

    public function findByTeamId(Uuid $teamId): array
    {
        return $this->findBy(['teamId' => $teamId->toString()]);
    }
}
```

### 5. Value Object

```php
declare(strict_types=1);

namespace App\Shared\Domain\ValueObject;

use Symfony\Component\Uid\Uuid as SymfonyUuid;

final readonly class Uuid
{
    private function __construct(
        private string $value
    ) {}

    public static function generate(): self
    {
        return new self(SymfonyUuid::v4()->toString());
    }

    public static function fromString(string $value): self
    {
        if (!SymfonyUuid::isValid($value)) {
            throw new \InvalidArgumentException('Invalid UUID format');
        }
        return new self($value);
    }

    public function toString(): string
    {
        return $this->value;
    }

    public function equals(self $other): bool
    {
        return $this->value === $other->value;
    }
}
```

## Dependency Injection Configuration

Register repository bindings in `config/services.yaml`:

```yaml
services:
    App\TaskManagement\Domain\Repository\TaskRepositoryInterface:
        class: App\TaskManagement\Infrastructure\Doctrine\DoctrineTaskRepository
```

## CQRS Bus Usage

```php
// In Controller
use Symfony\Component\Messenger\MessageBusInterface;

#[Route('/api/tasks', methods: ['POST'])]
public function create(
    Request $request,
    MessageBusInterface $commandBus
): JsonResponse {
    $data = json_decode($request->getContent(), true);

    $commandBus->dispatch(new CreateTaskCommand(
        id: Uuid::generate()->toString(),
        name: $data['name'],
        teamId: $data['teamId']
    ));

    return new JsonResponse(['status' => 'created'], 201);
}
```

## Key Principles

1. **Domain Layer is Framework-Agnostic** - No Symfony dependencies in Domain
2. **Always Use Interfaces** - Repository interfaces in Domain, implementations in Infrastructure
3. **Named Constructors** - Use static factory methods instead of public constructors
4. **Immutable Value Objects** - Use `readonly` for value objects
5. **Rich Domain Models** - Business logic belongs in entities, not services
6. **Domain Events** - Record events in entities for side effects

## Common Mistakes to Avoid

- Putting business logic in controllers or handlers
- Using Doctrine annotations/attributes in Domain layer
- Creating anemic domain models (entities with only getters/setters)
- Skipping the interface for repositories
- Mixing bounded contexts directly (use domain events instead)
