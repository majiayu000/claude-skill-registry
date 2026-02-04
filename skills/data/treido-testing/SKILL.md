---
name: treido-testing
description: Testing specialist for Treido (Playwright + Next.js). Use for writing/debugging E2E tests, deflaking, selectors, auth state, parallel execution, and CI stability.
---

# Playwright + Next.js Testing Best Practices

Comprehensive testing optimization guide for Playwright with Next.js applications. Contains 43 rules across 8 categories, prioritized by impact to guide reliable, fast, and maintainable E2E tests.

## When to Apply

Reference these guidelines when:
- Writing new Playwright tests for Next.js apps
- Debugging flaky or failing tests
- Optimizing test execution speed
- Setting up authentication state reuse
- Configuring CI/CD pipelines for testing
- Testing Server Components and App Router features
- Reviewing test code for reliability issues

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Test Architecture | CRITICAL | `arch-` |
| 2 | Selectors & Locators | CRITICAL | `loc-` |
| 3 | Waiting & Assertions | HIGH | `wait-` |
| 4 | Authentication & State | HIGH | `auth-` |
| 5 | Mocking & Network | MEDIUM-HIGH | `mock-` |
| 6 | Next.js Integration | MEDIUM | `next-` |
| 7 | Performance & Speed | MEDIUM | `perf-` |
| 8 | Debugging & CI | LOW-MEDIUM | `debug-` |

## Quick Reference

### 1. Test Architecture (CRITICAL)

- [`arch-test-isolation`](references/arch-test-isolation.md) - Use fresh browser context for each test
- [`arch-parallel-execution`](references/arch-parallel-execution.md) - Enable parallel test execution
- [`arch-page-object-model`](references/arch-page-object-model.md) - Use Page Object Model for complex pages
- [`arch-fixtures`](references/arch-fixtures.md) - Use fixtures for shared setup
- [`arch-test-production`](references/arch-test-production.md) - Test against production builds
- [`arch-cleanup-state`](references/arch-cleanup-state.md) - Clean up test state after each test

### 2. Selectors & Locators (CRITICAL)

- [`loc-role-selectors`](references/loc-role-selectors.md) - Use role-based selectors over CSS
- [`loc-data-testid`](references/loc-data-testid.md) - Use data-testid for dynamic elements
- [`loc-label-selectors`](references/loc-label-selectors.md) - Use getByLabel for form inputs
- [`loc-text-selectors`](references/loc-text-selectors.md) - Use getByText for static content
- [`loc-avoid-xpath`](references/loc-avoid-xpath.md) - Avoid XPath selectors
- [`loc-chained-locators`](references/loc-chained-locators.md) - Chain locators for specificity
- [`loc-placeholder-selector`](references/loc-placeholder-selector.md) - Use getByPlaceholder sparingly

### 3. Waiting & Assertions (HIGH)

- [`wait-web-first-assertions`](references/wait-web-first-assertions.md) - Use web-first assertions
- [`wait-avoid-hard-waits`](references/wait-avoid-hard-waits.md) - Avoid hard waits
- [`wait-network-idle`](references/wait-network-idle.md) - Use network idle for complex pages
- [`wait-action-retries`](references/wait-action-retries.md) - Let actions auto-wait before interacting
- [`wait-soft-assertions`](references/wait-soft-assertions.md) - Use soft assertions for non-critical checks
- [`wait-custom-timeout`](references/wait-custom-timeout.md) - Configure timeouts appropriately

### 4. Authentication & State (HIGH)

- [`auth-storage-state`](references/auth-storage-state.md) - Reuse authentication with storage state
- [`auth-multiple-roles`](references/auth-multiple-roles.md) - Use separate storage states for different roles
- [`auth-session-storage`](references/auth-session-storage.md) - Handle session storage for auth
- [`auth-api-login`](references/auth-api-login.md) - Use API login for faster auth setup
- [`auth-parallel-workers`](references/auth-parallel-workers.md) - Use worker-scoped auth for parallel tests

### 5. Mocking & Network (MEDIUM-HIGH)

- [`mock-api-responses`](references/mock-api-responses.md) - Mock API responses for deterministic tests
- [`mock-intercept-modify`](references/mock-intercept-modify.md) - Intercept and modify real responses
- [`mock-har-files`](references/mock-har-files.md) - Use HAR files for complex mock scenarios
- [`mock-abort-requests`](references/mock-abort-requests.md) - Abort unnecessary requests
- [`mock-network-conditions`](references/mock-network-conditions.md) - Simulate network conditions

### 6. Next.js Integration (MEDIUM)

- [`next-wait-hydration`](references/next-wait-hydration.md) - Wait for hydration before interacting
- [`next-server-components`](references/next-server-components.md) - Test server components correctly
- [`next-app-router-navigation`](references/next-app-router-navigation.md) - Test App Router navigation patterns
- [`next-server-actions`](references/next-server-actions.md) - Test server actions end-to-end
- [`next-baseurl-config`](references/next-baseurl-config.md) - Configure baseURL for clean navigation

### 7. Performance & Speed (MEDIUM)

- [`perf-sharding`](references/perf-sharding.md) - Use sharding for large test suites
- [`perf-headless-ci`](references/perf-headless-ci.md) - Use headless mode in CI
- [`perf-browser-selection`](references/perf-browser-selection.md) - Select browsers strategically
- [`perf-reuse-server`](references/perf-reuse-server.md) - Reuse development server when possible
- [`perf-retries`](references/perf-retries.md) - Configure retries for flaky test recovery

### 8. Debugging & CI (LOW-MEDIUM)

- [`debug-trace-viewer`](references/debug-trace-viewer.md) - Use trace viewer for failed tests
- [`debug-screenshots-videos`](references/debug-screenshots-videos.md) - Capture screenshots and videos on failure
- [`debug-inspector`](references/debug-inspector.md) - Use Playwright Inspector for interactive debugging
- [`debug-ci-reporters`](references/debug-ci-reporters.md) - Configure reporters for CI integration

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Reference Files

| File | Description |
|------|-------------|
| [AGENTS.md](AGENTS.md) | Complete compiled guide with all rules |
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
