---
name: java
description: Build, review, and refactor Java backend services (Spring Boot). Use for tasks like REST API design, controllers/services/repositories, PostgreSQL persistence (JPA/MyBatis), migrations, configuration, security (Spring Security), observability, testing, performance tuning, and production hardening.
---

# java

Use this skill for Java 后端服务（通常 Spring Boot）开发与评审。

## Defaults (unless repo dictates otherwise)

- Framework: Spring Boot
- Build: Maven or Gradle (follow repo)
- API: REST + JSON, explicit DTOs
- DB: PostgreSQL, migrations via Flyway/Liquibase if present

## Recommended structure

- `controller/`：HTTP layer（request/response DTO、参数校验、错误码映射）
- `service/`：业务编排与事务边界（domain logic orchestration）
- `repository/`：持久化（JPA repository / MyBatis mapper）
- `domain/`：领域模型（实体、值对象、聚合根）
- `config/`：配置（Web/Security/Serialization）
- `integration/`：第三方调用（HTTP clients, MQ）
- `common/`：通用工具（logging, id, time, error）
- `test/`：单测/集成测试

## Workflow

1) Clarify contract
- Endpoint list, auth requirements, error codes, id format.
- Consistency with existing API versioning (`/v1/...`) and response envelope.

2) API design & validation
- Use DTOs; do not expose entities directly.
- Bean Validation (`@Valid`, `@NotNull`, etc.) for input.
- Standardize error responses (code/message/details).

3) Persistence & migrations
- Define schema and migration scripts (Flyway/Liquibase).
- Add indexes for query paths; ensure constraints align with requirements.
- Avoid N+1 queries (fetch joins, batch sizes, projections).

4) Transactions & consistency
- Define transaction boundaries at service layer (`@Transactional`).
- Keep read-only transactions where possible.
- Idempotency for write endpoints when needed.

5) Security
- Spring Security: authentication (JWT/session), authorization (roles/scopes).
- Secrets via env/config server; never commit credentials.
- Safe logging (no PII), rate limiting if required.

6) Observability
- Structured logs with correlation/request IDs.
- Metrics (latency, error rate, DB timings); tracing if available.

7) Testing
- Unit tests for services and domain logic.
- Integration tests for repositories and controllers (Testcontainers if used).
- Keep tests deterministic and fast.

## Output expectations when making changes

- Keep diffs localized; avoid broad refactors unless requested.
- Update DTOs/migrations/tests together.
- Document new config/env vars and run steps.

