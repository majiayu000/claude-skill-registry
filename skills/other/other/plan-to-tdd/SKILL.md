---
name: plan-to-tdd
description: Transform feature plans into test-driven implementation using Outside-In methodology. This skill should be used when converting documented plans from docs/plan/ into testable code w/ proper test structure (Unit, Integration, E2E).
---

# Plan-to-TDD

Transform feature plans → test-driven implementation using Outside-In methodology.

## When to Use

Invoke when:
- Converting plan docs from `docs/plan/YYYY/MM/` to code
- Designing test structure for new features
- Applying TDD w/ architectural awareness
- Bridging system design to implementation

## Prerequisites

- Reference: `.claude/skills/test-levels` for Unit/Integration/E2E guidance
- Plan files in `docs/plan/YYYY/MM/YYYY_MM_DD_HHmm__FEATURE_NAME.md`

## Related Skills

| Skill | Location | Phase |
|-------|----------|-------|
| `doc-navigator` | `.claude/skills/doc-navigator` | Load/Design - find existing patterns |
| `uiux-toolkit` | `.claude/skills/uiux-toolkit` | Verify - 9-domain UX evaluation |
| `test-levels` | `.claude/skills/test-levels` | Plan/Execute - test distribution |

---

## Outside-In Workflow

```
SYSTEM DESIGN → INTEGRATION TESTS (Red) → TDD UNITS → E2E VALIDATION
```

### Phase Flow

```
┌─────────────────────────────────────────────────┐
│ 1. SYSTEM DESIGN                                │
│    Components → Contracts → Dependencies        │
└────────────────────┬────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────┐
│ 2. INTEGRATION TESTS (Red)                      │
│    Validate component contracts - tests FAIL    │
└────────────────────┬────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────┐
│ 3. TDD UNIT PHASE                               │
│    Red → Green → Refactor per unit              │
└────────────────────┬────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────┐
│ 4. E2E VALIDATION                               │
│    Complete user journey verification           │
└─────────────────────────────────────────────────┘
```

---

## Execution Steps

### Step 1: Load Plan

**Input:** `docs/plan/YYYY/MM/YYYY_MM_DD_HHmm__FEATURE_NAME.md`

**Extract:**
1. User story & acceptance criteria
2. Components & dependencies
3. Data flows
4. Technical constraints

**Expected structure:**
```markdown
# Feature: [Name]

## User Story
As a [user], I want to [action] so that [benefit].

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Components
- Component A: Description
- Component B: Description

## Data Flow
1. Step 1
2. Step 2
```

### Step 2: Define Contracts

For each component boundary:

```typescript
interface [Component]Contract {
  input: {
    type: string;
    validation: string[];
    source: string; // sender component
  };
  output: {
    type: string;
    successCase: string;
    errorCases: string[];
  };
  dependencies: string[];
}
```

### Step 3: Generate Tests

#### E2E Tests (Complete Car)
```typescript
// tests/e2e/[feature].spec.ts
describe('[Feature] - User Journey', () => {
  test('User can [action] successfully', async () => {
    // Arrange → Act → Assert
  });
  test('User sees error when [condition]', async () => {
    // Error path from user perspective
  });
});
```

#### Integration Tests (Engine + Transmission)
```typescript
// tests/integration/[component].test.ts
describe('[ComponentA] → [ComponentB]', () => {
  test('Contract: [description]', async () => {
    // Validates the "arrow" in system design
  });
  test('Handles timeout gracefully', async () => {
    // Test architectural assumptions
  });
});
```

#### Unit Tests (Individual Parts)
```typescript
// tests/unit/[module].test.ts
describe('[Module]', () => {
  test('returns [expected] when [condition]', () => {
    // Red → Green → Refactor
  });
  test('throws [error] when [invalid input]', () => {
    // Edge cases
  });
});
```

### Step 4: Implementation Order

```
1. Scaffold        Create files & empty interfaces
       ↓
2. E2E (Red)       Failing E2E for user journey
       ↓
3. Integration     For each boundary:
   (Red)           - Failing integration test
                   - Validates contract
       ↓
4. TDD Cycle       For each unit:
   (Red→Green→     - Failing unit test
    Refactor)      - Min code to pass
                   - Refactor for clarity
       ↓
5. Integration     Run integration (should pass)
   (Green)
       ↓
6. E2E (Green)     Run E2E (should pass)
       ↓
7. Refactor        Clean up, optimize
```

---

## The Bridge: Design → Mocks

System design arrow becomes mock:

```
┌─────────────┐    ┌─────────────┐
│ OrderService│───▶│InventorySvc│
└─────────────┘    └─────────────┘
```

```typescript
const mockInventoryService = {
  checkStock: jest.fn(),
};

describe('OrderService', () => {
  test('throws OutOfStockException when inventory = 0', () => {
    mockInventoryService.checkStock.mockReturnValue(0);
    expect(() => orderService.placeOrder(item))
      .toThrow(OutOfStockException);
  });
});
```

**Key insight:** TDD validates architectural contracts:
- Timeouts in design → Test timeout handling
- Error responses → Test error handling
- Data transforms → Test transformations

---

## Test Pain → Design Fix

| Pain Signal | Design Issue | Fix |
|-------------|--------------|-----|
| 50+ lines mock setup | Too coupled | Split into smaller services |
| Needs real DB | Missing abstraction | Add repository interface |
| Can't test isolated | Circular deps | Restructure dependency graph |
| Brittle tests | Leaky abstractions | Strengthen contracts |

**When pain detected:**
1. Stop coding
2. Document the pain
3. Return to design
4. Refactor architecture
5. Resume TDD

---

## Output Artifacts

Generate in `/docs/features/[feature]/`:
- `DESIGN.md` - System design doc
- `CONTRACTS.md` - Interface contracts
- `TEST-PLAN.md` - Test structure & order
- `IMPLEMENTATION.md` - Build plan w/ tasks

---

## Quick Reference

```bash
# Load & parse plan
/load-plan [plan-path]

# Extract components
/extract-components [plan-path]

# Generate contracts
/define-contracts [plan-path]

# Generate test scaffolds
/generate-tests [plan-path]

# Start TDD w/ first red test
/tdd-start [plan-path]

# List plans
/list-plans
/list-plans --month 2024-03
```

---

## Test Distribution (from test-levels)

| Level | Question | Location |
|-------|----------|----------|
| Unit | "Does this fn work?" | `tests/unit/` |
| Integration | "Do parts connect?" | `tests/integration/` |
| E2E | "Does flow work?" | `tests/e2e/` |

**Pyramid:** Many unit → Some integration → Few E2E
