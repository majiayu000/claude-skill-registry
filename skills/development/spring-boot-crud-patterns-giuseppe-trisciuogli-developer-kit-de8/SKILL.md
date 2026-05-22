---
name: spring-boot-crud-patterns
description: Provide repeatable CRUD workflows for Spring Boot 3 services with Spring Data JPA and feature-focused architecture; apply when modeling aggregates, repositories, controllers, and DTOs for REST APIs.
allowed-tools: Read, Write, Bash
category: backend
tags: [spring-boot, java, ddd, rest-api, crud, jpa, feature-architecture]
version: 1.1.0
---

# Spring Boot CRUD Patterns

## Overview

Deliver feature-aligned CRUD services that separate domain, application, presentation, and infrastructure layers while preserving Spring Boot 3.5+ conventions. This skill distills the essential workflow and defers detailed code listings to reference files for progressive disclosure.

## When to Use

- Implement REST endpoints for create/read/update/delete workflows backed by Spring Data JPA.
- Refine feature packages following DDD-inspired architecture with aggregates, repositories, and application services.
- Introduce DTO records, request validation, and controller mappings for external clients.
- Diagnose CRUD regressions, repository contracts, or transaction boundaries in existing Spring Boot services.
- Trigger phrases: **"implement Spring CRUD controller"**, **"refine feature-based repository"**, **"map DTOs for JPA aggregate"**, **"add pagination to REST list endpoint"**.

## Prerequisites

- Java 17+ project using Spring Boot 3.5.x (or later) with `spring-boot-starter-web` and `spring-boot-starter-data-jpa`.
- Constructor injection enabled (Lombok `@RequiredArgsConstructor` or explicit constructors).
- Access to a relational database (Testcontainers recommended for integration tests).
- Familiarity with validation (`jakarta.validation`) and error handling (`ResponseStatusException`).

## Quickstart Workflow

1. **Establish Feature Structure**  
   Create `feature/<name>/` directories for `domain`, `application`, `presentation`, and `infrastructure`.
2. **Model the Aggregate**  
   Define domain entities and value objects without Spring dependencies; capture invariants in methods such as `create` and `update`.
3. **Expose Domain Ports**  
   Declare repository interfaces in `domain/repository` describing persistence contracts.
4. **Provide Infrastructure Adapter**  
   Implement Spring Data adapters in `infrastructure/persistence` that map domain models to JPA entities and delegate to `JpaRepository`.
5. **Implement Application Services**  
   Create transactional use cases under `application/service` that orchestrate aggregates, repositories, and mapping logic.
6. **Publish REST Controllers**  
   Map DTO records under `presentation/rest`, expose endpoints with proper status codes, and wire validation annotations.
7. **Validate with Tests**  
   Run unit tests for domain logic and repository/service tests with Testcontainers for persistence verification.

Consult `references/examples-product-feature.md` for complete code listings that align with each step.

## Implementation Patterns

### Domain Layer

- Define immutable aggregates with factory methods (`Product.create`) to centralize invariants.
- Use value objects (`Money`, `Stock`) to enforce type safety and encapsulate validation.
- Keep domain objects framework-free; avoid `@Entity` annotations in the domain package when using adapters.

### Application Layer

- Wrap use cases in `@Service` classes using constructor injection and `@Transactional`.
- Map requests to domain operations and persist through domain repositories.
- Return response DTOs or records produced by dedicated mappers to decouple domain from transport.

### Infrastructure Layer

- Implement adapters that translate between domain aggregates and JPA entities; prefer MapStruct or manual mappers for clarity.
- Configure repositories with Spring Data interfaces (e.g., `JpaRepository<ProductEntity, String>`) and custom queries for pagination or batch updates.
- Externalize persistence properties (naming strategies, DDL mode) via `application.yml`; see `references/spring-official-docs.md`.

### Presentation Layer

- Structure controllers by feature (`ProductController`) and expose REST paths (`/api/products`).
- Return `ResponseEntity` with appropriate codes: `201 Created` on POST, `200 OK` on GET/PUT/PATCH, `204 No Content` on DELETE.
- Apply `@Valid` on request DTOs and handle errors with `@ControllerAdvice` or `ResponseStatusException`.

## Validation and Observability

- Write unit tests that assert domain invariants and repository contracts; refer to `references/examples-product-feature.md` integration test snippets.
- Use `@DataJpaTest` and Testcontainers to validate persistence mapping, pagination, and batch operations.
- Surface health and metrics through Spring Boot Actuator; monitor CRUD throughput and error rates.
- Log key actions at `info` for lifecycle events (create, update, delete) and use structured logging for audit trails.

## Best Practices

- Favor feature modules with clear boundaries; colocate domain, application, and presentation code per aggregate.
- Keep DTOs immutable via Java records; convert domain types at the service boundary.
- Guard write operations with transactions and optimistic locking where concurrency matters.
- Normalize pagination defaults (page, size, sort) and document query parameters.
- Capture links between commands and events where integration with messaging or auditing is required.

## Constraints and Warnings

- Avoid exposing JPA entities directly in controllers to prevent lazy-loading leaks and serialization issues.
- Do not mix field injection with constructor injection; maintain immutability for easier testing.
- Refrain from embedding business logic in controllers or repository adapters; keep it in domain/application layers.
- Validate input aggressively to prevent constraint violations and produce consistent error payloads.
- Ensure migrations (Liquibase/Flyway) mirror aggregate evolution before deploying schema changes.

## References

- [HTTP method matrix, annotation catalog, DTO patterns.](references/crud-reference.md)
- [Progressive examples from starter to advanced feature implementation.](references/examples-product-feature.md)
- [Excerpts from official Spring guides and Spring Boot reference documentation.](references/spring-official-docs.md)
- [Python generator to scaffold CRUD boilerplate from entity spec.](scripts/generate_crud_boilerplate.py) Usage: `python skills/spring-boot/spring-boot-crud-patterns/scripts/generate_crud_boilerplate.py --spec entity.json --package com.example.product --output ./generated`
- Templates required: place .tpl files in `skills/spring-boot/spring-boot-crud-patterns/templates/` or pass `--templates-dir <path>`; no fallback to built-ins. See `templates/README.md`.
- Usage guide: [references/generator-usage.md](references/generator-usage.md)
- Example spec: `skills/spring-boot/spring-boot-crud-patterns/assets/specs/product.json`
- Example with relationships: `skills/spring-boot/spring-boot-crud-patterns/assets/specs/product_with_rel.json`
