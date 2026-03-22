---
name: impact-analysis
description: |
  Impact analysis for understanding how code changes affect the system.
  Covers git diff analysis, entity mapping, flow identification, and regression suggestions.
  Use this skill when analyzing branches, planning testing, or understanding change scope.
allowed-tools: Read, Glob, Grep, Bash(git:*)
version: 1.0.0
---

# Impact Analysis Skill

Analyze the potential impact of code changes on the system.

## Overview

Impact analysis identifies what parts of the system may be affected by a code change. Think of it like a **domino effect** - pushing one domino (making a change) may cause others to fall.

```
┌─────────────────────────────────────────────────────────────┐
│  1. Git Diff                                                │
│     ↓                                                       │
│     Gets list of modified files                             │
│                                                             │
│  2. Classification                                          │
│     ↓                                                       │
│     Groups by type: API, UI, DB, Tests                      │
│                                                             │
│  3. Entity Mapping                                          │
│     ↓                                                       │
│     Relates files to system entities                        │
│                                                             │
│  4. Flow Lookup                                             │
│     ↓                                                       │
│     Queries registries for related flows                    │
│                                                             │
│  5. Suggestions                                             │
│     ↓                                                       │
│     Generates list of potentially affected areas            │
└─────────────────────────────────────────────────────────────┘
```

## When to Use This Skill

- Analyzing a feature branch before merge
- Planning regression testing scope
- Understanding the blast radius of a change
- Identifying related tests to run
- Code review impact assessment

## Analysis Capabilities

### What It CAN Identify

| Capability | Example |
|------------|---------|
| Modified files | "5 files changed in /products" |
| Direct dependencies | "Orders depends on Products" |
| Existing tests | "3 tests cover this area" |
| Documented flows | "Checkout flow uses this component" |
| Entity relationships | "FK relationship to customers" |

### What It CANNOT Identify

| Limitation | Reason |
|------------|--------|
| Business impact | Doesn't know business rules |
| Real severity | Cannot prioritize by criticality |
| Undocumented dependencies | Only sees what's in code |
| Complex side effects | Doesn't execute the code |
| Runtime behavior | Static analysis only |

## Output Format

```markdown
## Impact Analysis: feature/new-pricing

### Files Modified (23 files)
| Type | Count | Key Files |
|------|-------|-----------|
| API | 5 | orders/service.ts, payments/route.ts |
| UI | 12 | CheckoutForm.tsx, OrderSummary.tsx |
| DB | 2 | 001_add_payment_status.sql |
| Tests | 4 | checkout.cy.ts |

### Entities Affected
- **products**: API and UI modifications
- **orders**: Potentially affected (FK relationship)
- **payments**: New functionality

### Flows Potentially Impacted
- Complete checkout flow
- Order confirmation flow
- Payment processing flow

### Regression Suggestions
| Confidence | Area | Reason |
|------------|------|--------|
| High | Product CRUD | Direct changes |
| Medium | Order totals | Uses pricing |
| Low | Sales reports | May reference products |

### Related Tests
- checkout.cy.ts (@uat, @flow-checkout)
- orders.cy.ts (@api, @entity-orders)
- payments.cy.ts (@api)
```

## Confidence Levels

| Level | Meaning | Recommendation |
|-------|---------|----------------|
| **High** | Direct dependency found | Test this area |
| **Medium** | Indirect dependency | Consider testing |
| **Low** | Possible relationship | Evaluate with context |

## Interpreting Results

### Correct Interpretation

- "Analysis suggests pricing is directly affected"
- "Orders might be affected because it uses prices"
- "Should verify with dev team about reports impact"

### Incorrect Interpretation

- "Analysis says I MUST test everything listed"
- "If not in the list, there's no risk"
- "This is the complete list of affected areas"

## Complementing the Analysis

Technical analysis should be complemented with:

### 1. Business Knowledge

- What areas are critical for the business?
- Are there special seasons or events?
- Which customers use these features?

### 2. Bug History

- Have there been bugs in these areas before?
- Are there known "fragile" areas?

### 3. Developer Conversation

- What exactly changed?
- Are there impacts the code doesn't show?
- Are there affected external dependencies?

## Usage Examples

### Analyze a Branch

```bash
# Get diff from main
git diff main...feature/checkout-v2 --name-only

# Classify files
# API: src/app/api/**
# UI: src/components/**, src/app/(routes)/**
# DB: migrations/**
# Tests: cypress/**, __tests__/**
```

### Map to Entities

```typescript
// File path patterns to entities
const entityPatterns = {
  'entities/products': 'products',
  'entities/orders': 'orders',
  'api/v1/products': 'products',
  'components/Product': 'products',
}
```

### Lookup Related Flows

```typescript
// Query FLOW_REGISTRY for flows using affected entities
const affectedFlows = Object.entries(FLOW_REGISTRY)
  .filter(([_, flow]) =>
    flow.entities.some(e => affectedEntities.includes(e))
  )
```

## Commands

| Command | Description |
|---------|-------------|
| `/impact:analyze [branch]` | Analyze branch impact |
| `/impact:regression [feature]` | Identify regression areas |

## Important Notes

1. **This is a starting point** - not a definitive list
2. **Complements human judgment** - doesn't replace it
3. **Static analysis only** - cannot predict runtime behavior
4. **Business context required** - you decide what's critical

The analysis is an **assistance tool**. YOU decide what to test and with what priority.
