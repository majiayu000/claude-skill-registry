---
name: orval
description: Orval OpenAPI TypeScript client generation best practices. This skill should be used when configuring Orval, generating TypeScript clients from OpenAPI specs, setting up React Query/SWR hooks, creating custom mutators, or writing MSW mocks. Triggers on tasks involving orval.config.ts, OpenAPI codegen, API client setup, or mock generation.
---

# Orval OpenAPI Best Practices

Comprehensive guide for generating type-safe TypeScript clients from OpenAPI specifications using Orval. Contains 42 rules across 8 categories, prioritized by impact to guide automated configuration, client generation, and testing setup.

## When to Apply

Reference these guidelines when:
- Configuring Orval for a new project
- Setting up OpenAPI-based TypeScript client generation
- Integrating React Query, SWR, or Vue Query with generated hooks
- Creating custom mutators for authentication and error handling
- Generating MSW mocks for testing

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | OpenAPI Specification Quality | CRITICAL | `spec-` |
| 2 | Configuration Architecture | CRITICAL | `orvalcfg-` |
| 3 | Output Structure & Organization | HIGH | `output-` |
| 4 | Custom Client & Mutators | HIGH | `mutator-` |
| 5 | Query Library Integration | MEDIUM-HIGH | `oquery-` |
| 6 | Type Safety & Validation | MEDIUM | `types-` |
| 7 | Mock Generation & Testing | MEDIUM | `mock-` |
| 8 | Advanced Patterns | LOW | `adv-` |

## Quick Reference

### 1. OpenAPI Specification Quality (CRITICAL)

- `spec-operationid-unique` - Use unique and descriptive operationIds
- `spec-schemas-reusable` - Define reusable schemas in components
- `spec-tags-organization` - Organize operations with tags
- `spec-response-types` - Define all response types explicitly
- `spec-required-fields` - Mark required fields explicitly

### 2. Configuration Architecture (CRITICAL)

- `orvalcfg-mode-selection` - Choose output mode based on API size
- `orvalcfg-client-selection` - Select client based on framework requirements
- `orvalcfg-separate-schemas` - Separate schemas into dedicated directory
- `orvalcfg-input-validation` - Validate OpenAPI spec before generation
- `orvalcfg-baseurl-setup` - Configure base URL properly
- `orvalcfg-prettier-format` - Enable automatic code formatting

### 3. Output Structure & Organization (HIGH)

- `output-file-extension` - Use distinct file extensions for generated code
- `output-index-files` - Generate index files for clean imports
- `output-naming-convention` - Configure consistent naming conventions
- `output-clean-target` - Enable clean mode for consistent regeneration
- `output-headers-enabled` - Enable headers in generated functions

### 4. Custom Client & Mutators (HIGH)

- `mutator-custom-instance` - Use custom mutator for HTTP client configuration
- `mutator-error-types` - Export custom error types from mutator
- `mutator-body-wrapper` - Export body type wrapper for request transformation
- `mutator-interceptors` - Use interceptors for cross-cutting concerns
- `mutator-token-refresh` - Handle token refresh in mutator
- `mutator-fetch-client` - Use fetch mutator for smaller bundle size

### 5. Query Library Integration (MEDIUM-HIGH)

- `oquery-hook-options` - Configure default query options globally
- `oquery-key-export` - Export query keys for cache invalidation
- `oquery-infinite-queries` - Enable infinite queries for paginated endpoints
- `oquery-suspense-support` - Enable suspense mode for streaming UX
- `oquery-signal-cancellation` - Pass AbortSignal for request cancellation
- `oquery-mutation-callbacks` - Use generated mutation options types

### 6. Type Safety & Validation (MEDIUM)

- `types-zod-validation` - Generate Zod schemas for runtime validation
- `types-zod-strict` - Enable Zod strict mode for safer validation
- `types-zod-coerce` - Use Zod coercion for type transformations
- `types-use-dates` - Enable useDates for Date type generation
- `types-bigint-support` - Enable useBigInt for large integer support

### 7. Mock Generation & Testing (MEDIUM)

- `mock-msw-generation` - Generate MSW handlers for testing
- `mock-use-examples` - Use OpenAPI examples for realistic mocks
- `mock-delay-config` - Configure mock response delays
- `mock-http-status` - Generate mocks for all HTTP status codes
- `mock-index-files` - Generate mock index files for easy setup

### 8. Advanced Patterns (LOW)

- `adv-input-transformer` - Use input transformer for spec preprocessing
- `adv-operation-override` - Override settings per operation
- `adv-output-transformer` - Use output transformer for generated code modification
- `adv-form-data-handling` - Configure form data serialization

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules
- Example: [spec-operationid-unique](references/spec-operationid-unique.md)

## Related Skills

- For consuming generated hooks, see `tanstack-query` skill
- For mocking generated API clients, see `test-msw` skill
- For schema validation, see `zod` skill

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
