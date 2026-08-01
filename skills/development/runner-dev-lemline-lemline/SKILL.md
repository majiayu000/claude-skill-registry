---
name: runner-dev
description: Development guide for the lemline-runner module. Use when working with
  messaging (commands/events
---

---
name: runner-dev
description: Development guide for the lemline-runner module. Use when working with messaging (commands/events
channels),
database tables (waits, retries, parents, schedules, failures, forks), outbox pattern, CLI commands, configuration,
repositories with Kotlin coroutines, or Flyway migrations. Covers the dual-channel architecture, workflow execution
flow, and production best practices for the Quarkus/Kotlin runtime.
---

# Lemline Runner Development Guide

## Purpose

Guide development of the lemline-runner module - the Quarkus-based runtime for workflow orchestration. This module
handles messaging, persistence, scheduling, and CLI operations.

**Documentation:**

- [CLI Commands](lemline-runner/docs/runner-cli.md)
- [Configuration](lemline-runner/docs/runner-configuration.md)
- [Messaging Architecture](lemline-runner/docs/runner-messaging.md)
- [Database Tables](lemline-runner/docs/runner-tables.md)

---

## Quick Reference

### If you need to change something in...

**Messaging:**

First, read [runner-messaging.md](lemline-runner/docs/runner-messaging.md)

- **Add a new command/event type** →
  Modify [WorkflowState.kt](lemline-core/src/main/kotlin/com/lemline/core/states/WorkflowState.kt)
- **Update commands behavior** →
  Modify [WorkflowCommandHandler.kt](lemline-runner/src/main/kotlin/com/lemline/runner/messaging/commands/WorkflowCommandHandler.kt)
- **Update events behavior** →
  Modify [WorkflowEventHandler.kt](lemline-runner/src/main/kotlin/com/lemline/runner/messaging/events/WorkflowEventHandler.kt)

**Database:**

First read [runner-tables.md](lemline-runner/docs/runner-tables.md)

- **Add a model/table/repository** →
  Read [runner-repositories-guide.md](lemline-runner/docs/runner-repositories-guide.md)
- **Add outbox processing** →
  Extend [AbstractOutbox.kt](lemline-runner/src/main/kotlin/com/lemline/runner/outbox/AbstractOutbox.kt)
- **Add cleanup for a table** →
  Extend [AbstractCleaner.kt](lemline-runner/src/main/kotlin/com/lemline/runner/cleaner/AbstractCleaner.kt)

**Configuration:**

First read [runner-configuration.md](lemline-runner/docs/runner-configuration.md)

- **Add/Update config property** →
  Modify [LemlineConfiguration.kt](lemline-runner/src/main/kotlin/com/lemline/runner/config/LemlineConfiguration.kt)
- **Add database/broker type** → Read [runner-configuration.md](lemline-runner/docs/runner-configuration.md)

**CLI:**

First read [runner-cli.md](lemline-runner/docs/runner-cli.md#adding-a-new-cli-command)

---

## Critical Rules

### ✅ ALWAYS Do This

1. **Use `suspend` functions** for all database operations (Kotlin coroutines, NOT Mutiny)
2. **Use native SQL** via repositories (NOT Hibernate ORM/Panache)
3. **Use Flyway migrations** for all schema changes
4. **Support all databases** (PostgreSQL, MySQL, H2) - use database-agnostic SQL
5. **Use `FOR UPDATE SKIP LOCKED`** for outbox queries to prevent double-processing
6. **Use IDV7** (UUID v7) for all entity IDs - time-sortable, globally unique
7. **Test with all supported databases** when touching persistence layer

### ❌ NEVER Do This

1. **Use Mutiny (Uni/Multi)** - use Kotlin coroutines with `suspend` functions instead
2. **Use Hibernate ORM/Panache** - use native SQL with repositories
3. **Block the event loop** - all I/O must be non-blocking
4. **Skip database migrations** - never modify tables directly
5. **Use database-specific SQL** without providing variants for all databases
6. **Commit sensitive data** (.env, credentials, API keys)

---

## Architecture Overview

### Dual-Channel Design

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  COMMANDS CHANNEL (high-throughput)                         │
│  commands-in ──► WorkflowCommandHandler ──► commands-out                    │
│       ▲                 │                                                   │
│       │                 │ (needs persistence)                               │
└───────│─────────────────│───────────────────────────────────────────────────┘
        │                 │
┌───────│─────────────────│───────────────────────────────────────────────────┐
│       │                 ▼              EVENTS CHANNEL                       │
│       │               events-in ──► WorkflowEventHandler ──► Database       │
│       │                                   │                                 │
│       └───────────────────────────────────┘ (outbox processors)             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Key principle:** State travels with messages. Database only used when necessary.

### Key Files

| Purpose           | File                                                                                                                        |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------|
| Step execution    | [StepByStepRunner.kt](lemline-runner/src/main/kotlin/com/lemline/runner/StepByStepRunner.kt)                                |
| Command handling  | [WorkflowCommandHandler.kt](lemline-runner/src/main/kotlin/com/lemline/runner/messaging/commands/WorkflowCommandHandler.kt) |
| Event handling    | [WorkflowEventHandler.kt](lemline-runner/src/main/kotlin/com/lemline/runner/messaging/events/WorkflowEventHandler.kt)       |
| Message structure | [InstanceMessage.kt](lemline-runner/src/main/kotlin/com/lemline/runner/messaging/InstanceMessage.kt)                        |
| Outbox base       | [AbstractOutbox.kt](lemline-runner/src/main/kotlin/com/lemline/runner/outbox/AbstractOutbox.kt)                             |

---

## Common Patterns

### Repository Pattern

```kotlin
@ApplicationScoped
class MyRepository : Repository<MyModel>() {

    suspend fun findByUUID(uuid: IDV7): MyModel? {
        return pool.withConnection { conn ->
            conn.preparedQuery("SELECT * FROM lemline_my_table WHERE id = $1")
                .execute(Tuple.of(uuid.value))
                .awaitSuspending()
                .firstOrNull()
                ?.let { MyModel.fromRow(it) }
        }
    }

    suspend fun insert(model: MyModel) {
        pool.withConnection { conn ->
            conn.preparedQuery(
                """
                INSERT INTO lemline_my_table (id, ...) VALUES ($1, ...)
            """
            ).execute(Tuple.of(model.id.value, ...))
            .awaitSuspending()
        }
    }
}
```

### Outbox Pattern

```kotlin
@ApplicationScoped
class MyOutbox @Inject constructor(
    private val repository: MyRepository,
    private val emitter: WorkflowCommandEmitter
) : AbstractOutbox<MyModel>() {

    override suspend fun findEntitiesToProcess(limit: Int): List<MyModel> {
        return repository.findPendingWithLock(limit)
    }

    override suspend fun processEntity(entity: MyModel): OutboxResult {
        emitter.send(createCommand(entity))
        return OutboxResult.Success
    }

    override suspend fun markCompleted(entity: MyModel) {
        repository.markCompleted(entity.id)
    }
}
```

### Event Handling

```kotlin
// In WorkflowEventHandler.kt
suspend fun handleMyEvent(message: InstanceMessage<MyEvent>) {
    val event = message.state

    // 1. Persist to database if needed
    myRepository.insert(MyModel.from(message, event))

    // 2. Emit command to resume workflow if needed
    commandEmitter.send(createResumeCommand(message))
}
```

---

## Testing Patterns

### Repository Test

```kotlin
@QuarkusTest
@TestProfile(PostgresProfile::class)
class MyRepositoryTest : FunSpec({

    @Inject
    lateinit var repository: MyRepository

    test("should find by UUID") {
        val model = createTestModel()
        repository.insert(model)

        val found = repository.findByUUID(model.id)

        found shouldNotBe null
        found?.id shouldBe model.id
    }
})
```

### Handler Test

```kotlin
@QuarkusTest
class WorkflowEventHandlerTest : FunSpec({

    @Inject
    lateinit var handler: WorkflowEventHandler

    test("should handle my event") {
        val message = createTestMessage()

        handler.handle(message)

        // Verify database state
        // Verify emitted commands
    }
})
```

---

## Database Migrations

**Locations:**

- PostgreSQL: `src/main/resources/db/migration/postgresql/`
- MySQL: `src/main/resources/db/migration/mysql/`
- H2: `src/main/resources/db/migration/h2/`

**Naming:** `V{N}__Description.sql` (e.g., `V8__Create_my_table.sql`)

**Template:**

```sql
-- PostgreSQL version
CREATE TABLE lemline_my_table
(
    id                   UUID PRIMARY KEY,
    workflow_id          UUID         NOT NULL,
    -- workflow state columns
    workflow_namespace   VARCHAR(255) NOT NULL,
    workflow_name        VARCHAR(255) NOT NULL,
    workflow_version     VARCHAR(255) NOT NULL,
    workflow_position    TEXT         NOT NULL,
    workflow_state       TEXT         NOT NULL,
    -- outbox columns (if using outbox pattern)
    outbox_scheduled_for TIMESTAMP    NOT NULL,
    outbox_delayed_until TIMESTAMP    NOT NULL,
    outbox_attempt_count INT          NOT NULL DEFAULT 0,
    outbox_completed_at  TIMESTAMP,
    outbox_failed_at     TIMESTAMP,
    -- timestamps
    created_at           TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_lemline_my_table_pending
    ON lemline_my_table (outbox_delayed_until) WHERE outbox_completed_at IS NULL AND outbox_failed_at IS NULL;
```

---

## Running Tests

```bash
# All tests
./gradlew :lemline-runner:test

# Specific test class
./gradlew :lemline-runner:test --tests "com.lemline.runner.tests.MyTest"

# With specific database profile
./gradlew :lemline-runner:test -Dquarkus.test.profile=postgres
```

---

## Related Documentation

- **CLAUDE.md** - Project-wide guidelines and architecture overview
- **Serverless Workflow DSL** - https://serverlessworkflow.io/
