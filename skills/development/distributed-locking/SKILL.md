---
name: distributed-locking
description: >
  RFC-44 compliant distributed locking patterns for Java services. Covers PostgreSQL
  advisory locks and Redis-based locking, migration workflows, and common patterns.
  Use when implementing or migrating distributed locking mechanisms.
compatibility: Java projects with PostgreSQL or Redis
metadata:
  version: "1.0.0"
  technology: java
  category: infrastructure
  tags:
    - java
    - distributed-locking
    - rfc-44
    - postgresql
    - redis
---

# Distributed Locking

RFC-44 compliant distributed locking patterns for Java services.

## When to use this skill

- Implementing distributed locking for scheduled jobs
- Migrating from legacy locking mechanisms
- Choosing between PostgreSQL and Redis locking
- Migrating from Fabric8 leader election
- Migrating from incubated in-repo libraries

## Skill Contents

### Sections

- [When to use this skill](#when-to-use-this-skill) (L24-L31)
- [Quick Start](#quick-start) (L54-L96)
- [Implementation Options](#implementation-options) (L97-L107)
- [Common Patterns](#common-patterns) (L108-L130)
- [References](#references) (L131-L139)
- [Related Rules](#related-rules) (L140-L143)
- [Related Skills](#related-skills) (L144-L149)

### Available Resources

**📚 references/** - Detailed documentation
- [lock patterns](references/lock-patterns.md)
- [migration workflow](references/migration-workflow.md)
- [redis integration](references/redis-integration.md)
- [troubleshooting](references/troubleshooting.md)

---

## Quick Start

### 1. Add Dependencies (PostgreSQL)

```toml
# gradle/libs.versions.toml
[versions]
distributed-locking-api = "2.0.0"
distributed-locking-postgres-jooq = "2.0.0"

[libraries]
distributed-locking-api = { module = "com.bitso.commons:distributed-locking-api", version.ref = "distributed-locking-api" }
distributed-locking-postgres-jooq = { module = "com.bitso.commons:distributed-locking-postgres-jooq", version.ref = "distributed-locking-postgres-jooq" }
```

### 2. Create Configuration Bean

```java
@Configuration
public class DistributedLockConfiguration {
    @Bean
    DistributedLockManager<Long> distributedLockManager(
            @Qualifier("write-dslcontext") DSLContext dslContext) {
        return new JooqPostgresSessionDistributedLockManager(dslContext);
    }
}
```

### 3. Use in Scheduled Jobs

```java
@Scheduled(cron = "${job.cron:-}", zone = "UTC")
public void scheduledJob() {
    try (var lock = distributedLockManager.tryLock("job-lock")) {
        if (!lock.acquired()) {
            log.info("Job already running on another instance");
            return;
        }
        doWork();
    }
}
```

## Implementation Options

RFC-44 supports **two valid locking implementations**:

| Implementation | When to Use |
|----------------|-------------|
| **PostgreSQL Advisory Locks** (Default) | Services with PostgreSQL available |
| **Redis Locking** (Allowed) | Services without PostgreSQL, or with justified Redis use case |

> **Important**: Redis-based locking is NOT deprecated. It is explicitly supported per RFC-44.

## Common Patterns

### Try-with-resources Pattern

```java
try (var lock = distributedLockManager.tryLock("lock-key")) {
    if (!lock.acquired()) {
        return;
    }
    executeTask();
}
```

### Vavr Pattern

```java
Try.withResources(() -> distributedLockManager.tryLock("lock-key"))
    .of(lock -> Option.of(lock)
        .filter(DistributedLock::acquired)
        .onEmpty(() -> log.info("Lock not acquired"))
        .peek(l -> doWork()));
```

## References

| Reference | Description |
|-----------|-------------|
| [references/migration-workflow.md](references/migration-workflow.md) | Step-by-step migration guide |
| [references/lock-patterns.md](references/lock-patterns.md) | RFC-44 lock patterns |
| [references/redis-integration.md](references/redis-integration.md) | Redis-based locking setup |
| [references/troubleshooting.md](references/troubleshooting.md) | Common issues and solutions |

## Related Rules

- `.cursor/rules/java-distributed-locking-rfc44.mdc` - Full RFC-44 reference

## Related Skills

| Skill | Purpose |
|-------|---------|
| [gradle-standards](../gradle-standards/SKILL.md) | Dependency configuration |
| [java-testing](../java-testing/SKILL.md) | Testing lock mechanisms |
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → java/skills/distributed-locking/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

