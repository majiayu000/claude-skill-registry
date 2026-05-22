---
name: tdd-php
description: Test-Driven Development for PHP with PHPUnit and Behat. Use this skill when writing tests, implementing features using TDD, creating unit tests, integration tests, or acceptance tests for the backend.
---

# TDD PHP Skill - Test Driven Development

This skill enforces Test-Driven Development practices for the Family Plan PHP backend using PHPUnit and Behat.

## TDD Cycle: Red-Green-Refactor

```
┌─────────────────────────────────────────┐
│  1. RED: Write a failing test           │
│     ↓                                   │
│  2. GREEN: Write minimal code to pass   │
│     ↓                                   │
│  3. REFACTOR: Improve code quality      │
│     ↓                                   │
│  (Repeat)                               │
└─────────────────────────────────────────┘
```

**CRITICAL**: Always write the test FIRST, before any production code.

## Test Types and Locations

| Type | Location | Purpose | Tools |
|------|----------|---------|-------|
| Unit | `tests/Unit/` | Test single class in isolation | PHPUnit |
| Integration | `tests/Integration/` | Test component interactions | PHPUnit + Doctrine |
| API | `tests/Api/` | Test REST endpoints | PHPUnit + WebTestCase |
| Acceptance | `features/` + `tests/Acceptance/` | BDD user scenarios | Behat |

## PHPUnit Test Patterns

### Unit Test Example

```php
declare(strict_types=1);

namespace App\Tests\Unit\TaskManagement\Domain\Entity;

use App\Shared\Domain\ValueObject\Uuid;
use App\TaskManagement\Domain\Entity\Task;
use PHPUnit\Framework\TestCase;

final class TaskTest extends TestCase
{
    public function testCreateTaskWithValidData(): void
    {
        // Arrange
        $id = Uuid::generate();
        $name = 'Clean the room';

        // Act
        $task = Task::create($id, $name);

        // Assert
        $this->assertTrue($id->equals($task->id()));
        $this->assertSame($name, $task->name());
    }

    public function testCannotCreateTaskWithEmptyName(): void
    {
        // Arrange
        $id = Uuid::generate();

        // Assert
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Task name cannot be empty');

        // Act
        Task::create($id, '');
    }
}
```

### Test Data Builders (Mother Pattern)

Located in `tests/*/Mother/`:

```php
declare(strict_types=1);

namespace App\Tests\Unit\TaskManagement\Mother;

use App\Shared\Domain\ValueObject\Uuid;
use App\TaskManagement\Domain\Entity\Task;

final class TaskMother
{
    public static function create(
        ?Uuid $id = null,
        ?string $name = null
    ): Task {
        return Task::create(
            $id ?? Uuid::generate(),
            $name ?? 'Default Task Name'
        );
    }

    public static function withName(string $name): Task
    {
        return self::create(name: $name);
    }
}
```

### Integration Test Example

```php
declare(strict_types=1);

namespace App\Tests\Integration\TaskManagement\Infrastructure;

use App\Shared\Domain\ValueObject\Uuid;
use App\TaskManagement\Domain\Entity\Task;
use App\TaskManagement\Infrastructure\Doctrine\DoctrineTaskRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;

final class DoctrineTaskRepositoryTest extends KernelTestCase
{
    private DoctrineTaskRepository $repository;
    private EntityManagerInterface $entityManager;

    protected function setUp(): void
    {
        self::bootKernel();
        $container = static::getContainer();

        $this->entityManager = $container->get(EntityManagerInterface::class);
        $this->repository = $container->get(DoctrineTaskRepository::class);

        $this->entityManager->beginTransaction();
    }

    protected function tearDown(): void
    {
        $this->entityManager->rollback();
        parent::tearDown();
    }

    public function testSaveAndRetrieveTask(): void
    {
        // Arrange
        $task = Task::create(Uuid::generate(), 'Test Task');

        // Act
        $this->repository->save($task);
        $this->entityManager->clear();

        $retrieved = $this->repository->findById($task->id());

        // Assert
        $this->assertNotNull($retrieved);
        $this->assertTrue($task->id()->equals($retrieved->id()));
    }
}
```

### API Test Example

```php
declare(strict_types=1);

namespace App\Tests\Api\TaskManagement;

use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;
use Symfony\Component\HttpFoundation\Response;

final class TaskApiTest extends WebTestCase
{
    public function testCreateTaskReturns201(): void
    {
        // Arrange
        $client = static::createClient();
        $this->authenticateClient($client);

        // Act
        $client->request('POST', '/api/tasks', [], [], [
            'CONTENT_TYPE' => 'application/json',
        ], json_encode([
            'name' => 'New Task',
            'teamId' => 'valid-team-uuid'
        ]));

        // Assert
        $this->assertResponseStatusCodeSame(Response::HTTP_CREATED);
    }

    public function testCreateTaskWithoutAuthReturns401(): void
    {
        // Arrange
        $client = static::createClient();

        // Act
        $client->request('POST', '/api/tasks');

        // Assert
        $this->assertResponseStatusCodeSame(Response::HTTP_UNAUTHORIZED);
    }

    private function authenticateClient($client): void
    {
        // Add authentication logic
    }
}
```

## Behat Acceptance Tests

### Feature File (`features/task_management/create_task.feature`)

```gherkin
Feature: Create Task
  As a team member
  I want to create a task
  So that I can track work to be done

  Background:
    Given I am authenticated as a team member

  Scenario: Successfully create a task
    When I create a task with name "Clean the kitchen"
    Then the task should be created successfully
    And the task should appear in my task list

  Scenario: Cannot create task without name
    When I try to create a task without a name
    Then I should see an error "Task name is required"

  Scenario: Cannot create task for another team
    Given there is another team "Neighbors"
    When I try to create a task for team "Neighbors"
    Then I should see an error "Access denied"
```

### Context Class (`tests/Acceptance/TaskManagement/CreateTaskContext.php`)

```php
declare(strict_types=1);

namespace App\Tests\Acceptance\TaskManagement;

use Behat\Behat\Context\Context;
use Behat\Gherkin\Node\PyStringNode;
use Symfony\Component\HttpFoundation\Response;

final class CreateTaskContext implements Context
{
    private ?Response $response = null;

    public function __construct(
        private readonly ApiClient $apiClient
    ) {}

    /**
     * @When I create a task with name :name
     */
    public function iCreateATaskWithName(string $name): void
    {
        $this->response = $this->apiClient->post('/api/tasks', [
            'name' => $name
        ]);
    }

    /**
     * @Then the task should be created successfully
     */
    public function theTaskShouldBeCreatedSuccessfully(): void
    {
        Assert::assertEquals(201, $this->response->getStatusCode());
    }
}
```

## Running Tests

```bash
# All PHPUnit tests
make phpunit
# or: docker compose exec php vendor/bin/phpunit

# Specific test file
docker compose exec php vendor/bin/phpunit --filter=TaskTest

# Specific test method
docker compose exec php vendor/bin/phpunit --filter=testCreateTaskWithValidData

# All Behat tests
make behat
# or: docker compose exec php vendor/bin/behat

# Specific Behat suite
docker compose exec php vendor/bin/behat --suite=task_management

# All backend tests
make backend-test
```

## Test Naming Conventions

- Test classes: `{ClassName}Test.php`
- Test methods: `test{WhatIsBeingTested}{ExpectedBehavior}`
- Mother classes: `{ClassName}Mother.php`
- Feature files: `snake_case.feature`

Examples:
- `testCreateTaskWithValidData` - success scenario
- `testCannotCreateTaskWithEmptyName` - failure scenario
- `testReturns404WhenTaskNotFound` - specific return behavior

## Assertions Best Practices

```php
// Preferred: specific assertions
$this->assertSame('expected', $actual);
$this->assertTrue($condition);
$this->assertInstanceOf(Task::class, $result);
$this->assertCount(3, $items);

// For exceptions
$this->expectException(TaskNotFoundException::class);
$this->expectExceptionMessage('Task not found');

// For JSON responses
$this->assertJsonStringEqualsJsonString($expected, $actual);
```

## TDD Workflow Checklist

1. [ ] Write a failing test (RED)
2. [ ] Run the test - confirm it fails
3. [ ] Write minimal code to pass (GREEN)
4. [ ] Run the test - confirm it passes
5. [ ] Refactor code (REFACTOR)
6. [ ] Run all tests - confirm nothing broke
7. [ ] Repeat for next feature

## Important Rules

- **Never skip the RED phase** - if your test passes immediately, something is wrong
- **One assertion per test** (when practical) - makes failures clear
- **Test behavior, not implementation** - tests should survive refactoring
- **Use descriptive test names** - they serve as documentation
- **Keep tests independent** - no shared state between tests
- **Fast tests** - unit tests should run in milliseconds
