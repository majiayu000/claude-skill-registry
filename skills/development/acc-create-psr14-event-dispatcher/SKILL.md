---
name: acc-create-psr14-event-dispatcher
description: Generates PSR-14 Event Dispatcher implementation for PHP 8.5. Creates EventDispatcherInterface, ListenerProviderInterface, and StoppableEventInterface with event propagation. Includes unit tests.
---

# PSR-14 Event Dispatcher Generator

## Overview

Generates PSR-14 compliant event dispatcher for domain events and application events.

## When to Use

- Implementing event-driven architecture
- Domain event dispatching in DDD
- Decoupling application components
- Building CQRS systems

## Generated Components

| Component | Description | Location |
|-----------|-------------|----------|
| EventDispatcher | Dispatches events | `src/Infrastructure/Event/` |
| ListenerProvider | Provides listeners | `src/Infrastructure/Event/` |
| Stoppable Event | Base stoppable event | `src/Infrastructure/Event/` |
| Unit Tests | PHPUnit tests | `tests/Unit/Infrastructure/Event/` |

## Template: Event Dispatcher

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Event;

use Psr\EventDispatcher\EventDispatcherInterface;
use Psr\EventDispatcher\ListenerProviderInterface;
use Psr\EventDispatcher\StoppableEventInterface;

final readonly class EventDispatcher implements EventDispatcherInterface
{
    public function __construct(
        private ListenerProviderInterface $listenerProvider,
    ) {
    }

    public function dispatch(object $event): object
    {
        foreach ($this->listenerProvider->getListenersForEvent($event) as $listener) {
            if ($event instanceof StoppableEventInterface && $event->isPropagationStopped()) {
                break;
            }

            $listener($event);
        }

        return $event;
    }
}
```

## Template: Listener Provider

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Event;

use Psr\EventDispatcher\ListenerProviderInterface;

final class ListenerProvider implements ListenerProviderInterface
{
    /** @var array<class-string, array<callable>> */
    private array $listeners = [];

    public function getListenersForEvent(object $event): iterable
    {
        $eventClass = $event::class;

        yield from $this->listeners[$eventClass] ?? [];

        foreach (class_parents($eventClass) as $parent) {
            yield from $this->listeners[$parent] ?? [];
        }

        foreach (class_implements($eventClass) as $interface) {
            yield from $this->listeners[$interface] ?? [];
        }
    }

    /** @param class-string $eventClass */
    public function addListener(string $eventClass, callable $listener): void
    {
        $this->listeners[$eventClass][] = $listener;
    }
}
```

## Template: Stoppable Event

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Event;

use Psr\EventDispatcher\StoppableEventInterface;

abstract class StoppableEvent implements StoppableEventInterface
{
    private bool $propagationStopped = false;

    public function isPropagationStopped(): bool
    {
        return $this->propagationStopped;
    }

    public function stopPropagation(): void
    {
        $this->propagationStopped = true;
    }
}
```

## Template: Domain Event

```php
<?php

declare(strict_types=1);

namespace App\Domain\User\Event;

use App\Domain\User\ValueObject\UserId;
use DateTimeImmutable;

final readonly class UserCreated
{
    public function __construct(
        public UserId $userId,
        public string $email,
        public DateTimeImmutable $occurredAt = new DateTimeImmutable(),
    ) {
    }
}
```

## Template: Event Listener

```php
<?php

declare(strict_types=1);

namespace App\Application\User\Listener;

use App\Domain\User\Event\UserCreated;
use Psr\Log\LoggerInterface;

final readonly class SendWelcomeEmailListener
{
    public function __construct(
        private EmailServiceInterface $emailService,
        private LoggerInterface $logger,
    ) {
    }

    public function __invoke(UserCreated $event): void
    {
        $this->logger->info('Sending welcome email', [
            'user_id' => $event->userId->toString(),
            'email' => $event->email,
        ]);

        $this->emailService->send(
            to: $event->email,
            subject: 'Welcome!',
            template: 'emails/welcome',
        );
    }
}
```

## Template: Unit Test

```php
<?php

declare(strict_types=1);

namespace App\Tests\Unit\Infrastructure\Event;

use App\Infrastructure\Event\EventDispatcher;
use App\Infrastructure\Event\ListenerProvider;
use App\Infrastructure\Event\StoppableEvent;
use PHPUnit\Framework\Attributes\CoversClass;
use PHPUnit\Framework\Attributes\Group;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;

#[Group('unit')]
#[CoversClass(EventDispatcher::class)]
final class EventDispatcherTest extends TestCase
{
    #[Test]
    public function it_dispatches_event_to_listeners(): void
    {
        $provider = new ListenerProvider();
        $dispatcher = new EventDispatcher($provider);

        $called = false;
        $provider->addListener(TestEvent::class, function () use (&$called) {
            $called = true;
        });

        $dispatcher->dispatch(new TestEvent());

        self::assertTrue($called);
    }

    #[Test]
    public function it_stops_propagation_for_stoppable_events(): void
    {
        $provider = new ListenerProvider();
        $dispatcher = new EventDispatcher($provider);

        $callCount = 0;
        $provider->addListener(TestStoppableEvent::class, function (TestStoppableEvent $e) use (&$callCount) {
            $callCount++;
            $e->stopPropagation();
        });
        $provider->addListener(TestStoppableEvent::class, function () use (&$callCount) {
            $callCount++;
        });

        $dispatcher->dispatch(new TestStoppableEvent());

        self::assertSame(1, $callCount);
    }

    #[Test]
    public function it_returns_event_after_dispatch(): void
    {
        $provider = new ListenerProvider();
        $dispatcher = new EventDispatcher($provider);

        $event = new TestEvent();
        $result = $dispatcher->dispatch($event);

        self::assertSame($event, $result);
    }
}

final class TestEvent {}
final class TestStoppableEvent extends StoppableEvent {}
```

## Usage Example

```php
<?php

use App\Infrastructure\Event\EventDispatcher;
use App\Infrastructure\Event\ListenerProvider;

// Setup
$provider = new ListenerProvider();
$dispatcher = new EventDispatcher($provider);

// Register listeners
$provider->addListener(
    UserCreated::class,
    new SendWelcomeEmailListener($emailService, $logger),
);

$provider->addListener(
    UserCreated::class,
    new CreateUserProfileListener($profileService),
);

// Dispatch event (from domain entity or handler)
$event = new UserCreated($userId, $email);
$dispatcher->dispatch($event);
```

## DDD Integration

```php
<?php

declare(strict_types=1);

namespace App\Domain\User\Entity;

use App\Domain\User\Event\UserCreated;
use App\Domain\User\ValueObject\Email;
use App\Domain\User\ValueObject\UserId;

final class User
{
    /** @var object[] */
    private array $events = [];

    private function __construct(
        private readonly UserId $id,
        private Email $email,
    ) {
    }

    public static function create(Email $email): self
    {
        $user = new self(UserId::generate(), $email);
        $user->events[] = new UserCreated($user->id, $email->toString());

        return $user;
    }

    /** @return object[] */
    public function pullEvents(): array
    {
        $events = $this->events;
        $this->events = [];

        return $events;
    }
}
```

## Requirements

```json
{
    "require": {
        "psr/event-dispatcher": "^1.0"
    }
}
```

## See Also

- `references/templates.md` - Priority provider, async dispatcher
- `references/examples.md` - Integration examples
