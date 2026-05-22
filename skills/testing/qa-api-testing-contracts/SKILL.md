---
name: qa-api-testing-contracts
description: API testing and contract validation. Design and execute schema validation, contract tests, negative testing, and change safety for REST, GraphQL, and gRPC APIs. Use when you need API test plans, contract testing, or CI quality gates.
---

# QA API Testing and Contracts

## When to Use This Skill

Use this skill when you need to:

- Design API test plans for REST, GraphQL, or gRPC services.
- Implement contract testing with Pact or consumer-driven workflows.
- Set up schema validation in CI/CD pipelines.
- Review API changes for backward compatibility.
- Define quality gates for API releases.

## Scope

- Validate API schemas and enforce contracts.
- Design functional, negative, and edge case tests.
- Plan mocking and consumer driven contracts.
- Define CI gates and release safety checks.
- Align API tests with SLOs and error budgets.

## Ask For Inputs

- API type (REST, GraphQL, gRPC) and schemas (OpenAPI, SDL, proto).
- Environments and authentication methods.
- Critical endpoints and business flows.
- Data constraints, idempotency, and rate limits.
- Change cadence and backward compatibility policy.
- Current test tooling and CI pipeline.

## Workflow

1. Confirm API surface and schema sources.
2. Establish contract rules (breaking vs non breaking).
3. Generate schema validation tests.
4. Create functional tests for happy paths.
5. Add negative, boundary, and auth tests.
6. Add consumer contract tests or mocks as needed.
7. Define CI gates, reporting, and rollback triggers.

## Outputs

- API test plan and coverage map by endpoint.
- Contract validation suite and schema checks.
- Negative and security test list.
- Mock and test data strategy.
- CI quality gates and release checklist.

## Quality Checks

- Fail fast on schema violations and breaking changes.
- Ensure tests are deterministic and data stable.
- Separate functional tests from load or resilience tests.
- Keep contract tests aligned with versioning policy.

## Templates

- `templates/api-test-plan.md` for coverage planning.
- `templates/contract-change-checklist.md` for breaking change review.
- `templates/schema-validation-matrix.md` for schema tooling and CI stages.

## Resources

- `resources/contract-testing-patterns.md` for change safety guidance.

## Related Skills

- Use [dev-api-design](../dev-api-design/SKILL.md) for API design decisions.
- Use [qa-testing-strategy](../qa-testing-strategy/SKILL.md) for overall testing strategy.
- Use [qa-resilience](../qa-resilience/SKILL.md) for chaos and reliability testing.
- Use [software-security-appsec](../software-security-appsec/SKILL.md) for API security review.
