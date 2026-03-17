---
name: qa-api-testing-contracts
description: API testing and contract validation across REST (OpenAPI 3.1), GraphQL (SDL), and gRPC (proto). Use when you need schema linting/validation, breaking-change detection (openapi diff, GraphQL schema diff, buf breaking), consumer/provider contract tests (Pact or schema-driven), negative/security testing, and CI quality gates.
---

# QA API Testing and Contracts

Use this skill to turn an API schema into enforceable checks (lint, diff, contracts, and negative/security cases) and wire them into CI so breaking changes cannot ship silently.

## Ask For Inputs

- API type and canonical schema artifact (OpenAPI 3.1, SDL, proto) and where it lives in-repo.
- Environments, auth method(s), and how to provision stable test identities/keys.
- Critical endpoints/operations and business flows (rank by risk and revenue impact).
- Data constraints (idempotency keys, pagination, ordering), rate limits, and error format (prefer RFC 7807 `application/problem+json` for REST).
- Versioning + deprecation policy, consumer inventory, and release cadence.
- Current test tooling/CI and what “blocking” means for your org.

## Outputs (What to Produce)

- A minimal CI gate set (lint + breaking diff + contract suite) wired to PRs.
- A coverage map derived from the schema (critical operations first).
- A negative/security baseline aligned to OWASP API risks.

## Quick Start

1. Lint the schema (syntax + best-practice rules) and fix issues before writing tests.
2. Add breaking-change checks against the base branch on every PR.
3. Pick a contract strategy (CDC, schema-driven, or both) and run it in CI against an ephemeral environment.
4. Add negative/security cases for auth, validation, and error handling.
5. Make gates explicit (what blocks merge/release) and publish results.

## Workflow

### 1) Establish Contract Artifacts (Source of Truth)

- REST: single OpenAPI 3.1 file or a compiled artifact; avoid drift across fragments.
- GraphQL: checked-in SDL (and federation/composition config if relevant).
- gRPC: checked-in `.proto` + `buf.yaml` (or equivalent) with a stable module layout.

### 2) Validate the Schema (Fast, Deterministic)

- Run spec linting (Spectral / GraphQL Inspector / buf lint).
- Enforce a small, explicit ruleset (naming, descriptions, auth annotations, consistent error model).

### 3) Detect Breaking Changes (PR Gate)

- REST: OpenAPI diff with a breaking-change policy (remove/rename/type change/requiredness).
- GraphQL: schema diff with breaking checks (field removals, type changes, non-null tightening).
- gRPC: `buf breaking` (do not reuse/renumber fields; avoid changing request/response shapes incompatibly).

### 4) Execute Contract Tests (CI Gate)

Choose one or combine:

- CDC (Pact): best when many independent consumers exist and behavior matters beyond schema.
- Schema-driven (Specmatic): best when schema is the contract and you want fast coverage across operations.
- Property-based (Schemathesis): best when you want systematic edge cases and server hardening.

### 5) Add Negative + Security Cases (Minimum Set)

- AuthN/AuthZ: missing/expired token (401), insufficient scope/role (403), tenant isolation.
- Validation: missing required fields, invalid types, boundary values, empty strings, large payloads.
- Error handling: stable error shape, safe messages, correct status codes, correlation IDs.
- Abuse & limits: rate limiting (429), pagination limits, idempotency replay, retry-safe semantics.
  - For GraphQL, also validate operations checks (known/persisted queries) if you have an operation registry (GraphOS/Hive/etc.).

### 6) Define CI Quality Gates (Merge + Release)

- Pre-merge: schema lint + breaking-change diff (blocking).
- Pre-release: contract suite (blocking), plus smoke/functional tests for critical flows.
- Reporting: publish artifacts (diff report, contract verification, failing cases) and link in PR.

## Quality Checks

- Fail fast: schema violations and breaking changes block merge.
- Determinism: isolate data, freeze time where needed, avoid shared mutable fixtures.
- Flake hygiene: separate network instability from contract failures; retry only for known-transient classes.
- Alignment: contracts reflect versioning/deprecation policy and consumer inventory.
- Scope control: keep load/resilience tests separate unless explicitly requested.

## Use the Bundled Templates

- Coverage plan: `assets/api-test-plan.md`
- Release review: `assets/contract-change-checklist.md`
- Tooling map: `assets/schema-validation-matrix.md`

## AI Assistance (Use Carefully)

- Use AI to draft tests, suggest missing edge cases, and tighten matchers.
- Treat AI output as untrusted until verified against the schema and real behavior.
- Avoid uploading sensitive payloads; sanitize examples and logs.
- For a tool comparison and workflows, read `references/ai-contract-testing.md`.

## Read These When Needed

- Change safety and CDC patterns: `references/contract-testing-patterns.md`
- AI-assisted tooling and decision matrix: `references/ai-contract-testing.md`
- Curated authoritative links: `data/sources.json`

## Related Skills

- Use [dev-api-design](../dev-api-design/SKILL.md) for API design decisions.
- Use [qa-testing-strategy](../qa-testing-strategy/SKILL.md) for overall testing strategy.
- Use [qa-resilience](../qa-resilience/SKILL.md) for chaos and reliability testing.
- Use [software-security-appsec](../software-security-appsec/SKILL.md) for API security review.
