---
name: msw
description: MSW (Mock Service Worker) best practices for API mocking in tests (formerly test-msw). This skill should be used when setting up MSW, writing request handlers, or mocking HTTP APIs. This skill does NOT cover general testing patterns (use test-vitest or test-tdd skills) or test methodology.
---

# MSW Best Practices

Comprehensive API mocking guide for MSW v2 applications, designed for AI agents and LLMs. Contains 45 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Setting up MSW for testing or development
- Writing or organizing request handlers
- Configuring test environments with MSW
- Mocking REST or GraphQL APIs
- Debugging handler matching issues
- Testing error states and edge cases

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Setup & Initialization | CRITICAL | `setup-` |
| 2 | Handler Architecture | CRITICAL | `handler-` |
| 3 | Test Integration | HIGH | `test-` |
| 4 | Response Patterns | HIGH | `response-` |
| 5 | Request Matching | MEDIUM-HIGH | `match-` |
| 6 | GraphQL Mocking | MEDIUM | `graphql-` |
| 7 | Advanced Patterns | MEDIUM | `advanced-` |
| 8 | Debugging & Performance | LOW | `debug-` |

## Quick Reference

### 1. Setup & Initialization (CRITICAL)

- `setup-server-node-entrypoint` - Use correct entrypoint for Node.js (msw/node)
- `setup-lifecycle-hooks` - Configure server lifecycle in test setup
- `setup-worker-script-commit` - Commit worker script to version control
- `setup-node-version` - Require Node.js 18+ for MSW v2
- `setup-unhandled-requests` - Configure unhandled request behavior
- `setup-typescript-config` - Configure TypeScript for MSW v2

### 2. Handler Architecture (CRITICAL)

- `handler-happy-path-first` - Define happy path handlers as baseline
- `handler-domain-grouping` - Group handlers by domain
- `handler-absolute-urls` - Use absolute URLs in handlers
- `handler-shared-resolvers` - Extract shared response logic into resolvers
- `handler-v2-response-syntax` - Use MSW v2 response syntax
- `handler-request-body-parsing` - Explicitly parse request bodies
- `handler-resolver-argument` - Destructure resolver arguments correctly
- `handler-reusability-environments` - Share handlers across environments

### 3. Test Integration (HIGH)

- `test-reset-handlers` - Reset handlers after each test
- `test-avoid-request-assertions` - Avoid direct request assertions
- `test-concurrent-boundary` - Use server.boundary() for concurrent tests
- `test-fake-timers-config` - Configure fake timers to preserve queueMicrotask
- `test-async-utilities` - Use async testing utilities for mock responses
- `test-clear-request-cache` - Clear request library caches between tests
- `test-jsdom-environment` - Use correct JSDOM environment for Jest

### 4. Response Patterns (HIGH)

- `response-http-response-helpers` - Use HttpResponse static methods
- `response-delay-realistic` - Add realistic response delays
- `response-error-simulation` - Simulate error responses correctly
- `response-one-time-handlers` - Use one-time handlers for sequential scenarios
- `response-custom-headers` - Set response headers correctly
- `response-streaming` - Mock streaming responses with ReadableStream

### 5. Request Matching (MEDIUM-HIGH)

- `match-url-patterns` - Use URL path parameters correctly
- `match-query-params` - Access query parameters from request URL
- `match-custom-predicate` - Use custom predicates for complex matching
- `match-http-methods` - Match HTTP methods explicitly
- `match-handler-order` - Order handlers from specific to general

### 6. GraphQL Mocking (MEDIUM)

- `graphql-operation-handlers` - Use operation name for GraphQL matching
- `graphql-error-responses` - Return GraphQL errors in correct format
- `graphql-batched-queries` - Handle batched GraphQL queries
- `graphql-variables-access` - Access GraphQL variables correctly

### 7. Advanced Patterns (MEDIUM)

- `advanced-bypass-requests` - Use bypass() for passthrough requests
- `advanced-cookies-auth` - Handle cookies and authentication
- `advanced-dynamic-scenarios` - Implement dynamic mock scenarios
- `advanced-vitest-browser` - Configure MSW for Vitest browser mode
- `advanced-file-uploads` - Mock file upload endpoints

### 8. Debugging & Performance (LOW)

- `debug-lifecycle-events` - Use lifecycle events for debugging
- `debug-verify-interception` - Verify request interception is working
- `debug-common-issues` - Know common MSW issues and fixes
- `debug-request-logging` - Log request details for debugging

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules
- Individual rules: `references/{prefix}-{slug}.md`

## Related Skills

- For generating MSW mocks from OpenAPI, see `orval` skill
- For consuming mocked APIs, see `tanstack-query` skill
- For test methodology, see `test-vitest` or `test-tdd` skills

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
