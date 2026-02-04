---
name: acc-check-leaky-abstractions
description: Detects leaky abstractions in PHP code. Identifies implementation details exposed in interfaces, concrete returns from abstract methods, framework leakage into domain, and infrastructure concerns in application layer.
---

# Leaky Abstractions Detector

## Overview

This skill analyzes PHP codebases for leaky abstractions — situations where implementation details "leak" through interface boundaries, violating encapsulation and creating tight coupling.

## Leaky Abstraction Types

| Type | Description | Severity |
|------|-------------|----------|
| Interface Leakage | Implementation details in interface | CRITICAL |
| Framework Leakage | Framework types in domain/application | CRITICAL |
| Return Type Leakage | Concrete types returned from abstractions | WARNING |
| Parameter Leakage | Implementation-specific parameters | WARNING |
| Exception Leakage | Infrastructure exceptions crossing boundaries | WARNING |
| Dependency Leakage | Inner dependencies exposed | INFO |

## Detection Patterns

### Phase 1: Interface Leakage

```bash
# Doctrine types in interfaces
Grep: "Collection|ArrayCollection|PersistentCollection" --glob "**/Domain/**/*Interface.php"
Grep: "Doctrine\\\\|Illuminate\\\\|Symfony\\\\" --glob "**/Domain/**/*Interface.php"

# Infrastructure types in domain interfaces
Grep: "Redis|Memcached|Elasticsearch|Guzzle|Http" --glob "**/Domain/**/*Interface.php"

# Database types in repository interfaces
Grep: "QueryBuilder|EntityManager|Connection|PDO" --glob "**/Domain/**/*RepositoryInterface.php"

# ORM annotations/attributes in interfaces
Grep: "#\\[ORM\\\\|@ORM\\\\|@Entity|@Table" --glob "**/Domain/**/*Interface.php"
```

**Example Violations:**
```php
// BAD: Leaky interface
interface UserRepositoryInterface
{
    public function findByQuery(QueryBuilder $query): Collection; // Doctrine leak!
}

// GOOD: Clean interface
interface UserRepositoryInterface
{
    /** @return User[] */
    public function findByCriteria(UserCriteria $criteria): array;
}
```

### Phase 2: Framework Leakage into Domain

```bash
# Symfony components in Domain
Grep: "use Symfony\\\\Component\\\\" --glob "**/Domain/**/*.php"
Grep: "use Symfony\\\\Contracts\\\\" --glob "**/Domain/**/*.php"

# Laravel components in Domain
Grep: "use Illuminate\\\\" --glob "**/Domain/**/*.php"

# Doctrine in Domain entities
Grep: "use Doctrine\\\\ORM\\\\Mapping" --glob "**/Domain/**/*.php"
Grep: "#\\[ORM\\\\|@ORM\\\\|@Entity|@Column|@ManyToOne" --glob "**/Domain/**/*.php"

# HTTP in Domain
Grep: "Request|Response|HttpFoundation" --glob "**/Domain/**/*.php"
```

**Domain Should NOT Contain:**
- Framework service containers
- HTTP request/response objects
- ORM annotations (use separate mapping files)
- Framework validators
- Framework events (use domain events)

### Phase 3: Return Type Leakage

```bash
# Concrete class returns from interface methods
Grep: "public function.*\):\s*[A-Z][a-z]+[A-Z]" --glob "**/*Interface.php"
# Should return interfaces, not concrete classes

# Collection returns instead of arrays
Grep: "): Collection|): ArrayCollection" --glob "**/Domain/**/*Interface.php"

# Nullable entity returns (might indicate infrastructure concern)
Grep: "): \?[A-Z][a-z]+\s*;|): null\|[A-Z]" --glob "**/*Interface.php"

# Framework response types
Grep: "): Response|): JsonResponse|): View" --glob "**/Application/**/*.php"
```

### Phase 4: Parameter Leakage

```bash
# ORM-specific parameters in domain methods
Grep: "function.*EntityManager|function.*Connection" --glob "**/Domain/**/*.php"

# Query parameters
Grep: "function.*QueryBuilder|function.*Criteria\s*\$" --glob "**/Domain/**/*.php"

# HTTP request as parameter
Grep: "function.*Request \$request" --glob "**/Application/**/*UseCase.php"
Grep: "function.*Request \$request" --glob "**/Application/**/*Handler.php"

# Framework config in domain
Grep: "function.*Config|function.*Parameters" --glob "**/Domain/**/*.php"
```

### Phase 5: Exception Leakage

```bash
# Database exceptions in domain
Grep: "throw.*Doctrine\\\\|catch.*Doctrine\\\\" --glob "**/Domain/**/*.php"
Grep: "throw.*PDOException|catch.*PDOException" --glob "**/Domain/**/*.php"

# HTTP exceptions in application
Grep: "throw.*HttpException|throw.*NotFoundHttpException" --glob "**/Application/**/*.php"

# Infrastructure exceptions crossing boundaries
Grep: "catch.*\\\\Infrastructure\\\\" --glob "**/Application/**/*.php"

# Missing exception translation
Grep: "catch.*Exception" --glob "**/Infrastructure/**/*Repository.php" -A 3
# Should translate to domain exceptions
```

### Phase 6: Dependency Leakage

```bash
# Constructor exposing internal dependencies
Grep: "__construct.*EntityManager|__construct.*Connection" --glob "**/Application/**/*.php"

# Public methods with infrastructure types
Grep: "public function.*Logger|public function.*Cache" --glob "**/Domain/**/*.php"

# Getter exposing internal state
Grep: "public function get.*\(\).*EntityManager|public function get.*\(\).*Repository" --glob "**/*.php"
```

### Phase 7: Serialization Leakage

```bash
# JSON serialization in domain
Grep: "JsonSerializable|jsonSerialize" --glob "**/Domain/**/*.php"

# Symfony serializer attributes in domain
Grep: "#\\[Serializer\\\\|#\\[Groups|@Groups" --glob "**/Domain/**/*.php"

# API platform attributes in domain
Grep: "#\\[ApiResource|#\\[ApiProperty" --glob "**/Domain/**/*.php"
```

## Report Format

```markdown
# Leaky Abstractions Report

## Summary

| Leak Type | Critical | Warning | Info |
|-----------|----------|---------|------|
| Interface Leakage | 2 | 3 | - |
| Framework Leakage | 4 | 2 | - |
| Return Type Leakage | - | 5 | 3 |
| Parameter Leakage | 1 | 4 | - |
| Exception Leakage | 2 | 3 | - |
| Dependency Leakage | - | 2 | 4 |

**Total Leaks:** 8 critical, 19 warnings, 7 info

## Critical Issues

### LEAK-001: Doctrine Collection in Interface
- **File:** `src/Domain/User/UserRepositoryInterface.php:12`
- **Issue:** ORM-specific type in domain interface
- **Code:**
  ```php
  public function findActive(): Collection;
  ```
- **Expected:**
  ```php
  /** @return User[] */
  public function findActive(): array;
  ```
- **Impact:** Domain tied to Doctrine, cannot switch ORM
- **Skills:** `acc-create-repository`

### LEAK-002: Framework in Domain Entity
- **File:** `src/Domain/Order/Entity/Order.php:8`
- **Issue:** Doctrine ORM annotations in domain entity
- **Code:**
  ```php
  use Doctrine\ORM\Mapping as ORM;

  #[ORM\Entity]
  #[ORM\Table(name: 'orders')]
  class Order
  ```
- **Expected:** Use XML/YAML mapping files in Infrastructure
- **Impact:** Domain depends on persistence framework

### LEAK-003: HTTP Request in UseCase
- **File:** `src/Application/UseCase/CreateOrderUseCase.php:23`
- **Issue:** HTTP Request in application layer
- **Code:**
  ```php
  public function __invoke(Request $request): Response
  ```
- **Expected:**
  ```php
  public function __invoke(CreateOrderCommand $command): OrderId
  ```
- **Impact:** UseCase tied to HTTP, cannot reuse in CLI
- **Skills:** `acc-create-command`, `acc-create-use-case`

## Warning Issues

### LEAK-004: PDOException Not Translated
- **File:** `src/Infrastructure/Repository/DoctrineUserRepository.php:45`
- **Issue:** Database exception not translated to domain exception
- **Code:**
  ```php
  public function save(User $user): void
  {
      $this->em->persist($user);
      $this->em->flush(); // PDOException can leak!
  }
  ```
- **Expected:**
  ```php
  public function save(User $user): void
  {
      try {
          $this->em->persist($user);
          $this->em->flush();
      } catch (UniqueConstraintViolationException $e) {
          throw new UserAlreadyExistsException($user->email());
      }
  }
  ```

### LEAK-005: Concrete Return Type
- **File:** `src/Application/Service/PaymentServiceInterface.php:15`
- **Issue:** Returns concrete class instead of interface
- **Code:**
  ```php
  public function process(Payment $payment): StripePaymentResult;
  ```
- **Expected:**
  ```php
  public function process(Payment $payment): PaymentResultInterface;
  ```

### LEAK-006: Infrastructure Logger in Domain
- **File:** `src/Domain/Order/Service/OrderValidator.php:12`
- **Issue:** Logger dependency in domain service
- **Code:**
  ```php
  public function __construct(
      private LoggerInterface $logger,
  ) {}
  ```
- **Expected:** Domain should not log, or use domain events

## Abstraction Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  Request, Response, Controller, View                         │
├─────────────────────────────────────────────────────────────┤
│                    Application Layer                         │
│  Commands, Queries, Handlers, DTOs                          │
│  ❌ No HTTP types, ❌ No framework services                  │
├─────────────────────────────────────────────────────────────┤
│                      Domain Layer                            │
│  Entities, Value Objects, Domain Services, Interfaces        │
│  ❌ No ORM, ❌ No framework, ❌ No infrastructure            │
├─────────────────────────────────────────────────────────────┤
│                   Infrastructure Layer                       │
│  Repositories, Adapters, External Services                   │
│  ✅ ORM, ✅ Framework, ✅ Database                           │
└─────────────────────────────────────────────────────────────┘
```

## Refactoring Strategies

### Interface Abstraction
| Leaky | Clean |
|-------|-------|
| `Collection` | `array` or custom `*Collection` |
| `QueryBuilder` | `Criteria` or `Specification` |
| `EntityManager` | `RepositoryInterface` |
| `Request` | `Command` / `Query` DTO |
| `Response` | Return value + Responder |

### Exception Translation
```php
// Infrastructure layer
try {
    $this->connection->execute($sql);
} catch (UniqueConstraintViolationException $e) {
    throw new DuplicateEmailException($email);
} catch (\PDOException $e) {
    throw new PersistenceException('Failed to save user', 0, $e);
}
```

### Framework Independence
```php
// Instead of Doctrine Collection
interface UserRepositoryInterface
{
    /** @return User[] */
    public function findActive(): array;
}

// Implementation can use Collection internally
class DoctrineUserRepository implements UserRepositoryInterface
{
    public function findActive(): array
    {
        return $this->createQueryBuilder('u')
            ->where('u.active = true')
            ->getQuery()
            ->getResult(); // Returns array
    }
}
```
```

## Quick Analysis Commands

```bash
# Detect leaky abstractions
echo "=== Framework in Domain ===" && \
grep -rn "use Doctrine\\|use Symfony\\|use Illuminate\\" --include="*.php" src/Domain/ && \
echo "=== ORM in Interfaces ===" && \
grep -rn "Collection|QueryBuilder|EntityManager" --include="*Interface.php" src/ && \
echo "=== HTTP in Application ===" && \
grep -rn "Request|Response|HttpFoundation" --include="*.php" src/Application/ && \
echo "=== Unhandled Exceptions ===" && \
grep -rn "throw.*PDO\|throw.*Doctrine" --include="*.php" src/Domain/ src/Application/
```

## Integration

Works with:
- `acc-structural-auditor` — Layer boundary analysis
- `acc-ddd-auditor` — Domain purity checks
- `acc-create-repository` — Clean repository interfaces
- `acc-create-anti-corruption-layer` — External system isolation

## References

- "The Law of Leaky Abstractions" — Joel Spolsky
- "Clean Architecture" (Robert C. Martin) — Dependency Rule
- "Domain-Driven Design" (Eric Evans) — Layered Architecture
