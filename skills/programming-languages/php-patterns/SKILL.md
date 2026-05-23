---
name: php-patterns
description: Implementação de Design Patterns em PHP moderno incluindo Repository, Service Layer, Factory, Strategy, Observer, Decorator, Adapter, e Specification. Usar para arquitetura de aplicações, desacoplamento de código, implementação de SOLID, criação de camadas de abstração, e estruturação de código enterprise.
---

# PHP Patterns

Design Patterns para PHP 8.x com foco em aplicações Laravel/enterprise.

## Repository Pattern

Abstrai acesso a dados e permite trocar implementações.

```php
// Interface
interface ContractRepositoryInterface
{
    public function find(int $id): ?Contract;
    public function findOrFail(int $id): Contract;
    public function all(): Collection;
    public function create(array $data): Contract;
    public function update(Contract $contract, array $data): Contract;
    public function delete(Contract $contract): bool;
    public function findByClient(int $clientId): Collection;
}

// Implementação Eloquent
class EloquentContractRepository implements ContractRepositoryInterface
{
    public function __construct(
        private Contract $model
    ) {}

    public function find(int $id): ?Contract
    {
        return $this->model->find($id);
    }

    public function findOrFail(int $id): Contract
    {
        return $this->model->findOrFail($id);
    }

    public function all(): Collection
    {
        return $this->model->all();
    }

    public function create(array $data): Contract
    {
        return $this->model->create($data);
    }

    public function update(Contract $contract, array $data): Contract
    {
        $contract->update($data);
        return $contract->fresh();
    }

    public function delete(Contract $contract): bool
    {
        return $contract->delete();
    }

    public function findByClient(int $clientId): Collection
    {
        return $this->model->where('client_id', $clientId)->get();
    }
}

// Service Provider binding
$this->app->bind(ContractRepositoryInterface::class, EloquentContractRepository::class);
```

## Service Layer Pattern

Encapsula lógica de negócio complexa.

```php
class ContractService
{
    public function __construct(
        private ContractRepositoryInterface $repository,
        private PaymentService $paymentService,
        private NotificationService $notifications,
        private EventDispatcherInterface $events
    ) {}

    public function create(CreateContractDTO $dto): Contract
    {
        DB::beginTransaction();
        
        try {
            $contract = $this->repository->create($dto->toArray());
            
            if ($dto->generateInvoice) {
                $this->paymentService->generateInvoice($contract);
            }
            
            $this->events->dispatch(new ContractCreated($contract));
            
            DB::commit();
            return $contract;
            
        } catch (Throwable $e) {
            DB::rollBack();
            throw $e;
        }
    }

    public function cancel(Contract $contract, string $reason): Contract
    {
        if (!$contract->canBeCancelled()) {
            throw new ContractCannotBeCancelledException($contract);
        }

        $contract = $this->repository->update($contract, [
            'status' => ContractStatus::Cancelled,
            'cancelled_at' => now(),
            'cancellation_reason' => $reason,
        ]);

        $this->notifications->notifyContractCancelled($contract);
        $this->events->dispatch(new ContractCancelled($contract));

        return $contract;
    }
}
```

## Factory Pattern

Criação de objetos complexos.

```php
interface NotificationFactory
{
    public function create(string $type, array $data): Notification;
}

class ConcreteNotificationFactory implements NotificationFactory
{
    public function create(string $type, array $data): Notification
    {
        return match($type) {
            'email' => new EmailNotification($data),
            'sms' => new SmsNotification($data),
            'push' => new PushNotification($data),
            'slack' => new SlackNotification($data),
            default => throw new InvalidNotificationTypeException($type),
        };
    }
}

// Uso com container
class NotificationService
{
    public function __construct(
        private NotificationFactory $factory
    ) {}

    public function send(string $type, array $data): void
    {
        $notification = $this->factory->create($type, $data);
        $notification->send();
    }
}
```

## Strategy Pattern

Algoritmos intercambiáveis.

```php
interface PricingStrategy
{
    public function calculate(Contract $contract): float;
}

class StandardPricing implements PricingStrategy
{
    public function calculate(Contract $contract): float
    {
        return $contract->baseValue;
    }
}

class DiscountPricing implements PricingStrategy
{
    public function __construct(
        private float $discountPercentage
    ) {}

    public function calculate(Contract $contract): float
    {
        return $contract->baseValue * (1 - $this->discountPercentage / 100);
    }
}

class TieredPricing implements PricingStrategy
{
    public function calculate(Contract $contract): float
    {
        return match(true) {
            $contract->baseValue >= 10000 => $contract->baseValue * 0.85,
            $contract->baseValue >= 5000 => $contract->baseValue * 0.90,
            $contract->baseValue >= 1000 => $contract->baseValue * 0.95,
            default => $contract->baseValue,
        };
    }
}

// Context
class PricingCalculator
{
    public function __construct(
        private PricingStrategy $strategy
    ) {}

    public function setStrategy(PricingStrategy $strategy): void
    {
        $this->strategy = $strategy;
    }

    public function calculate(Contract $contract): float
    {
        return $this->strategy->calculate($contract);
    }
}
```

## Specification Pattern

Regras de negócio compostas.

```php
interface Specification
{
    public function isSatisfiedBy(Contract $contract): bool;
}

class ActiveContractSpecification implements Specification
{
    public function isSatisfiedBy(Contract $contract): bool
    {
        return $contract->status === ContractStatus::Active;
    }
}

class MinimumValueSpecification implements Specification
{
    public function __construct(
        private float $minimumValue
    ) {}

    public function isSatisfiedBy(Contract $contract): bool
    {
        return $contract->value >= $this->minimumValue;
    }
}

// Composite specifications
class AndSpecification implements Specification
{
    public function __construct(
        private Specification $left,
        private Specification $right
    ) {}

    public function isSatisfiedBy(Contract $contract): bool
    {
        return $this->left->isSatisfiedBy($contract) 
            && $this->right->isSatisfiedBy($contract);
    }
}

// Trait para fluent interface
trait ComposableSpecification
{
    public function and(Specification $other): Specification
    {
        return new AndSpecification($this, $other);
    }

    public function or(Specification $other): Specification
    {
        return new OrSpecification($this, $other);
    }
}

// Uso
$spec = (new ActiveContractSpecification())
    ->and(new MinimumValueSpecification(1000));

$eligibleContracts = $contracts->filter(
    fn($c) => $spec->isSatisfiedBy($c)
);
```

## Action Pattern (Single Action Classes)

```php
class CreateContractAction
{
    public function __construct(
        private ContractRepositoryInterface $repository,
        private EventDispatcherInterface $events
    ) {}

    public function execute(CreateContractDTO $dto): Contract
    {
        $contract = $this->repository->create($dto->toArray());
        $this->events->dispatch(new ContractCreated($contract));
        return $contract;
    }
}

// Controller limpo
class ContractController
{
    public function store(
        StoreContractRequest $request,
        CreateContractAction $action
    ): ContractResource {
        $contract = $action->execute(
            CreateContractDTO::fromRequest($request)
        );
        return new ContractResource($contract);
    }
}
```

## DTO Pattern

```php
readonly class CreateContractDTO
{
    public function __construct(
        public int $clientId,
        public float $value,
        public DateTimeImmutable $eventDate,
        public ContractStatus $status = ContractStatus::Pending,
        public ?string $notes = null,
    ) {}

    public static function fromRequest(Request $request): self
    {
        return new self(
            clientId: $request->integer('client_id'),
            value: $request->float('value'),
            eventDate: new DateTimeImmutable($request->string('event_date')),
            status: ContractStatus::tryFrom($request->string('status')) ?? ContractStatus::Pending,
            notes: $request->string('notes'),
        );
    }

    public static function fromArray(array $data): self
    {
        return new self(
            clientId: $data['client_id'],
            value: (float) $data['value'],
            eventDate: new DateTimeImmutable($data['event_date']),
            status: ContractStatus::from($data['status'] ?? 'pending'),
            notes: $data['notes'] ?? null,
        );
    }

    public function toArray(): array
    {
        return [
            'client_id' => $this->clientId,
            'value' => $this->value,
            'event_date' => $this->eventDate->format('Y-m-d'),
            'status' => $this->status->value,
            'notes' => $this->notes,
        ];
    }
}
```

## Estrutura de Diretórios Recomendada

```
app/
├── Actions/           # Single-action classes
├── DTOs/              # Data Transfer Objects
├── Repositories/
│   ├── Contracts/     # Interfaces
│   └── Eloquent/      # Implementações
├── Services/          # Business logic
├── Specifications/    # Business rules
├── Factories/         # Object creation
└── Strategies/        # Interchangeable algorithms
```
