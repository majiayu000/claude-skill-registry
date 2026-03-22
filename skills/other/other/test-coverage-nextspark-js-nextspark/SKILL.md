---
name: test-coverage
description: |
  Test coverage metrics and registry system for this Next.js application.
  Covers FEATURE_REGISTRY, FLOW_REGISTRY, TAGS_REGISTRY, and coverage metrics interpretation.
  Use this skill when evaluating test coverage, identifying gaps, or planning testing priorities.
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# Test Coverage Skill

Understand and use the test coverage registry system.

## Overview

The **registries** are files that document what exists in the system and its test coverage state.

| Registry | Contents | Location |
|----------|----------|----------|
| FEATURE_REGISTRY | System features | /devtools/features |
| FLOW_REGISTRY | User flows | /devtools/flows |
| TAGS_REGISTRY | Test tags | /devtools/tags |
| COVERAGE_SUMMARY | Aggregated metrics | testing-registry.ts |

## When to Use This Skill

- Evaluating current test coverage
- Identifying coverage gaps
- Planning testing priorities
- Generating coverage reports
- Understanding test distribution

## Registry Structures

### FEATURE_REGISTRY

Lists all system features with coverage state:

```typescript
FEATURE_REGISTRY = {
  'checkout': {
    name: 'Checkout',
    description: 'Purchase process',
    entities: ['orders', 'payments'],
    tests: ['checkout.cy.ts'],
    coverage: 'full'  // full | partial | none
  },
  'inventory': {
    name: 'Inventory Management',
    description: 'Stock management',
    entities: ['inventory', 'warehouses'],
    tests: [],
    coverage: 'none'
  }
}
```

| Coverage | Meaning |
|----------|---------|
| `full` | Has tests covering main flows |
| `partial` | Has some tests but gaps exist |
| `none` | No documented tests |

### FLOW_REGISTRY

Lists user flows with coverage state:

```typescript
FLOW_REGISTRY = {
  'login': {
    name: 'User Login',
    steps: ['Visit login', 'Enter credentials', 'Submit', 'Redirect'],
    entities: ['users', 'sessions'],
    tests: ['auth/login.cy.ts'],
    coverage: 'full'
  },
  'returns': {
    name: 'Process Returns',
    steps: ['Find order', 'Request return', 'Approve', 'Refund'],
    entities: ['orders', 'returns', 'payments'],
    tests: [],
    coverage: 'none'
  }
}
```

A flow without coverage means no automated tests verify that user path end-to-end.

### TAGS_REGISTRY

Lists all test tags with distribution:

```typescript
TAGS_REGISTRY = {
  '@smoke': { count: 15, files: ['login.cy.ts', 'products.cy.ts'] },
  '@uat': { count: 52, files: [...] },
  '@api': { count: 75, files: [...] },
  '@entity-products': { count: 20, files: ['products.cy.ts'] }
}
```

| Tag | Purpose | Typical Count |
|-----|---------|---------------|
| @smoke | Critical quick tests | 10-20 |
| @uat | User acceptance tests | 40-60% |
| @api | API tests | 30-50% |
| @entity-X | Per entity | Varies |
| @flow-X | Per flow | Varies |
| @critical | Business critical | 5-15 |

### COVERAGE_SUMMARY

Aggregated coverage metrics:

```typescript
COVERAGE_SUMMARY = {
  features: {
    total: 25,
    covered: 20,
    partial: 3,
    none: 2,
    percentage: 80
  },
  flows: {
    total: 15,
    covered: 10,
    percentage: 67
  },
  entities: {
    total: 12,
    withApiTests: 12,
    withUatTests: 10,
    percentage: 100
  }
}
```

## Technical vs Functional Coverage

### Critical Distinction

| Type | What It Measures | Example |
|------|------------------|---------|
| **Technical** | If a test exists | "There are 5 tests for products" |
| **Functional** | If test verifies correctly | "Tests validate business rules" |

### Why This Matters

```
Feature: Products
Tests: 10
Technical coverage: 100% ✓

But...
- Do tests verify validations?
- Do tests cover edge cases?
- Do tests check permissions?

Functional coverage: ??? (requires manual analysis)
```

**IMPORTANT**: Registry coverage metrics are TECHNICAL. They don't indicate test quality.

## Using Coverage Metrics

### To Identify Gaps

1. Find features with `coverage: 'none'`
2. Find flows without tests
3. Find entities with gaps

### To Prioritize

Metrics help identify areas without tests, but **prioritization** must consider:

| Factor | Who Evaluates |
|--------|---------------|
| Business criticality | QA + PM |
| Bug history | QA |
| Release proximity | QA + Dev |
| Available resources | QA + Management |

### For Reporting

```markdown
## Coverage Status - Sprint 15

- Features covered: 80% (20/25)
- Flows covered: 67% (10/15)
- Critical gaps identified:
  - Feature: inventory (no tests)
  - Flow: returns (no tests)
```

## File Locations

### DevTools Pages

- **Features**: `/devtools/features`
- **Flows**: `/devtools/flows`
- **Tags**: `/devtools/tags`

### Registry Files

- `apps/dev/.nextspark/registries/testing-registry.ts`

## Commands

| Command | Description |
|---------|-------------|
| `/coverage:status` | View overall status |
| `/coverage:gaps` | Identify gaps |

## Common Questions

### Does 100% coverage mean we're good?

**Not necessarily.** 100% technical coverage means tests exist, not that they're good or complete.

### Does 0% coverage mean it's bad?

**Not necessarily.** Some areas may not need automated tests, or may be covered by manual testing.

### How do I improve coverage?

1. Identify gaps with `/coverage:gaps`
2. Prioritize by business criticality
3. Create tests for most critical areas
4. Verify tests check the right things

## Important Notes

1. **Technical ≠ Functional** - Having tests doesn't mean they test the right things
2. **Metrics guide, don't decide** - Use business context to prioritize
3. **Quality over quantity** - 10 good tests beat 100 bad ones
4. **Living documentation** - Registries should stay updated

YOU decide how to interpret these metrics and what to prioritize based on business context.
