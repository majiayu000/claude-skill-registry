---
name: create-persistence-adapter
argument-hint: "[<path-to-Repository-port-file-or-domain-entity>]"
allowed-tools: Read, Write, Glob
description: Scaffold or update a complete JPA persistence adapter (outbound adapter) — entity, JPA repository, mapper, and adapter class — for a domain aggregate. Use when the user asks to "create a persistence adapter", "generate a JPA adapter", "scaffold the persistence layer", or "create an outbound db adapter". Accepts a repository port file or domain entity; generates all four files at once; updates existing files by adding missing methods or fields.
---

# Skill: create-persistence-adapter

Generates or updates up to four files per aggregate in `adapter/outbound/db/`:

- `*Entity.kt` — JPA entity mapping the aggregate to a database table
- `*JpaRepository.kt` — Spring Data `JpaRepository` interface
- `*EntityMapper.kt` — singleton `object` for entity ↔ domain conversion
- `*PersistenceAdapter.kt` — `@Component` implementing the outbound repository port

If any files already exist, the skill reads them, compares against the port interface and domain entity, and applies
only what is missing or outdated.

> Full code patterns: see [references/full-pattern.md](references/full-pattern.md)

## Pattern

```
Trigger: "Create a persistence adapter for newsletter subscription"
Input:   services/example-service/src/main/kotlin/.../port/outbound/NewsletterSubscriptionRepository.kt
Output — four files under adapter/outbound/db/:
  NewsletterSubscriptionEntity.kt          – @Entity data class
  NewsletterSubscriptionJpaRepository.kt   – JpaRepository interface
  NewsletterSubscriptionEntityMapper.kt    – object with toDomain / toEntity
  NewsletterSubscriptionPersistenceAdapter.kt – @Component implementing the port
```

## What is a Persistence Adapter?

A persistence adapter is an **outbound adapter**.
It acts as the interaction layer between your application and the database.
Your code calls it via a port interface.
It handles the translation between domain objects and the underlying storage mechanism (JPA/Spring Data).

## IMPORTANT

- Implement **every method** defined in the outbound repository port interface
- `find` throws `NoSuchElementException` when the entity is not found; `search` returns `null`
- All entity ↔ domain mapping goes through the singleton mapper `object` — never inline conversion.
- The mapper is a Kotlin `object` (singleton), not a `class` or a `companion object`
- Column names use `snake_case`; the `@Entity(name = ...)` value matches the database table name
- Enum fields use `@Enumerated(EnumType.STRING)` — never store the ordinal
- The JPA repository extends `JpaRepository<EntityClass, UUID>`
- It adds adds one `findBy<IdField>` method returning a nullable entity for kotlin-friendly `find`

## Instructions

### Step 1 – Resolve the input source

Two possible inputs:

**Option A – Repository port file path provided** (a `.kt` file under `port/outbound/`):

1. Read the file. Extract: interface name, all method signatures (names, parameter types, return types).
2. Derive the aggregate name by stripping the `Repository` suffix
   (e.g. `NewsletterSubscriptionRepository` → `NewsletterSubscription`).
3. Find the domain aggregate: `Glob **/domain/<AggregateName>.kt`. Read it to discover all fields.
4. If you can't find the matching aggregate or port pause the execution
5. Then ask the developer to provide correct information

**Option B – No argument provided**:

- Search: `Glob **/application/port/outbound/**/*.kt`.
- Filter the files to include only ones that could match as a port for a repository.
- If no files are found, inform the developer that no outbound port files were discovered, ask them to provide the port
  file path directly, then proceed as Option A. -
- If files were found list those files and ask the user which one to scaffold.
- Proceed as Option A once the user selects a file.

### Step 2 – Determine the target package and source root

Derive the base package from the repository port package
(e.g. `io.miragon.example.application.port.outbound` → base: `io.miragon.example`).

Adapter package: `<base>.adapter.outbound.db`.

Determine the source root from the port file path
(e.g. `services/example-service/src/main/kotlin/`).

Target directory: `<source-root>/<base-package-path>/adapter/outbound/db/`

### Step 3 – Check existing files and determine should-state for each

Derive the four class names from the aggregate name (e.g. `NewsletterSubscription`):

- Entity: `NewsletterSubscriptionEntity`
- JPA Repository: `NewsletterSubscriptionJpaRepository`
- Mapper: `NewsletterSubscriptionEntityMapper`
- Adapter: `NewsletterSubscriptionPersistenceAdapter`

Check which of these files already exist at the target directory.
For each file, determine its should-state as follows:

#### 3.1 Entity (`<AggregateName>Entity.kt`)

Read the domain aggregate class. For each field:

- Map domain value objects to their primitive type
  (e.g. `Email(val value: String)` → `String`, `SubscriptionId(val value: UUID)` → `UUID`)
- Derive the column name as `snake_case` of the field name
  (e.g. `registrationDate` → `registration_date`, `newsletterId` → `newsletter_id`)
- Mark enum fields with `@Enumerated(EnumType.STRING)`
- Mark the ID field with `@Id` and `@Column(name = "<id-column>", nullable = false)`

Derive the table name as `snake_case` of the aggregate class name
(e.g. `NewsletterSubscription` → `newsletter_subscription`).

Should-state: `data class` with `@Entity(name = "table_name")`, one column per aggregate field,
correct annotations.

**If file exists**: compare fields against the domain aggregate. Add missing fields, correct
outdated column names or annotations. Preserve any custom annotations already present.

**If file does not exist**: generate from the should-state above.

#### 3.2 JPA Repository (`<AggregateName>JpaRepository.kt`)

Should-state: `interface` extending `JpaRepository<EntityClass, UUID>` with exactly one
`findBy<IdField>(id: UUID): EntityClass?` query method.

**If the file exists**: check if any query methods are missing based on the port interface. Add them.

**If file does not exist**: generate from the should-state above.

#### 3.3 Mapper (`<AggregateName>EntityMapper.kt`)

Should-state: `object` with two functions:

- `toDomain(entity: EntityClass): DomainClass` — wraps each primitive in its domain value object
- `toEntity(domain: DomainClass): EntityClass` — extracts `.value` from each domain value object

**If a file exists**: check for missing field mappings and add them.

**If file does not exist**: generate from the should-state above.

#### 3.4 Adapter (`<AggregateName>PersistenceAdapter.kt`)

Should-state: `@Component` class implementing the repository port, constructor-injected JPA
repository, all port methods delegating through the mapper:

- `find` → throws `NoSuchElementException` when not found
- `search` → returns `null` when not found
- `save` → delegates to `repository.save(...)`
- `delete` → delegates to `repository.deleteById(id.value)`

**If file exists**: compare against all port methods. Add any missing ones, preserving
existing business logic.

**If file does not exist**: generate from the should-state above.

### Step 4 – Write all files

Apply all creations and updates identified in Step 3.
Use [references/full-pattern.md](references/full-pattern.md) as a concrete reference.

### Step 5 – Report

List each file created, updated, or skipped (if nothing changed) and remind the developer to:

1. Add a database migration (Flyway/Liquibase) if a new table is introduced
2. Run `/test-persistence-adapter` to generate unit tests for the adapter
3. Wire the adapter into the application service via the port interface (automatic via Spring if
   the package is within the base component-scan path)