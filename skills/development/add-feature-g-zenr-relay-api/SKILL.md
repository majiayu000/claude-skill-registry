---
name: add-feature
description: Plan and implement a complete feature end-to-end across all layers
disable-model-invocation: true
---

Implement the following feature: $ARGUMENTS

This is a full-feature workflow that touches every layer. Follow the team's standards at each step.

## Phase 1 — Plan (Sofia Nakamura)
1. Define the user story: who needs this, what it does, why it matters
2. Read existing code to understand where the feature fits in the architecture
3. Identify every file that needs to change or be created
4. List acceptance criteria — what "done" looks like
5. Present the plan before writing any code

## Phase 2 — Schema & Config (Daniel Okoye + Marcus Chen)
1. Add any new typed schemas (see stack concepts) to the models/schemas file
   - Explicit types on every field — no untyped/any fields
   - Validation constraints where applicable (see stack concepts)
2. Add any new settings to the config file with the project's env prefix
3. Document new settings in the env example file with description and default

## Phase 3 — Core Layer (Alex Rivera)
*Skip if the feature doesn't touch the core/device layer.*
1. If new behavior is needed, extend the primary protocol/interface
2. Implement in both the real and mock implementations — both must stay in sync
3. Use typed exceptions from the exception hierarchy
4. Document any protocol-specific commands with clear comments

## Phase 4 — Service Logic (Alex Rivera + Janet Moore)
1. Add business logic to the service layer
   - Thread-safe: wrap external resource access in the lock mechanism
   - Rollback on partial failure for multi-entity operations
   - Audit log via the project's audit logger for any state changes
   - Typed exceptions for error conditions

## Phase 5 — API Endpoints (Daniel Okoye)
1. Add routes to the appropriate router (see project config)
   - Thin handlers — delegate to the service class
   - Auth-protected DI dependency for protected endpoints
   - Public DI dependency for unauthenticated endpoints
   - Full OpenAPI metadata: response schema, summary, description, responses (see stack concepts)
   - Static routes before parameterized routes
   - Map domain exceptions to HTTP status codes per project config

## Phase 6 — Security (Janet Moore)
1. Verify new endpoints respect auth when API key is configured
2. Verify error responses use the error response model — no stack traces or internals
3. Verify input validation via typed schemas (see stack concepts) — no raw input trusted
4. If handling secrets: use timing-safe comparison (see stack concepts), never equality operator

## Phase 7 — Tests (Priya Sharma)
1. Write tests for each new endpoint: success, validation error, device/service error
2. Write tests for new service methods: happy path, edge cases, error conditions
3. If state changes: test audit log output via log capture mechanism (see stack concepts)
4. If multi-entity operations: test rollback on partial failure
5. Add to corresponding test file (see test file mapping in project config)

## Phase 8 — Verify (All)
Run the test command and the type-check command (see project config).
Both MUST pass with zero errors.

## Phase 9 — Documentation (Sofia Nakamura)
1. Update project documentation — API endpoints table, configuration table, examples
2. Update app factory description if the feature changes API capabilities
3. Verify OpenAPI docs reflect all new endpoints