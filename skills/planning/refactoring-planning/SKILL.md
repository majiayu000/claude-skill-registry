---
name: refactoring-planning
description: Plan refactoring work by identifying core components and structuring tasks
---

# Refactoring Planning Skill

This skill guides the planning phase of refactoring work. It helps identify which components need scaffolding tests, how to structure the migration path, and how to break work into verifiable tasks.

**When to use:** Any refactoring that touches multiple files, changes architectural patterns, or modifies public interfaces.

---

## Planning Workflow

### Step 1: Define the Refactoring Goal

Before analyzing code, articulate clearly:

```markdown
## Refactoring Goal

**Current state:** [How the code is structured now]
**Target state:** [How the code should be structured after]
**Why:** [Business/technical driver for this change]
**Scope boundary:** [What is explicitly OUT of scope]
```

A refactoring without a clear goal becomes scope creep.

### Step 2: Map the Affected Code

Identify all code that will change:

```bash
# Find files in the target area
Glob: internal/handlers/**/*.go
Glob: pkg/services/**/*.go

# Find callers of functions being changed
Grep: "FunctionBeingMoved\|TypeBeingChanged"

# Find tests that exercise this code
Glob: **/*_test.go | grep -l "TestHandler\|TestService"
```

Create an impact map:

```markdown
## Impact Map

**Directly modified:**
- internal/handlers/user.go (moving logic to service)
- internal/handlers/order.go (moving logic to service)

**Indirectly affected (callers):**
- cmd/api/main.go (wiring changes)
- internal/middleware/auth.go (imports service)

**Test files:**
- internal/handlers/user_test.go
- internal/handlers/order_test.go
```

### Step 3: Identify Core Components to Scaffold

Not everything needs scaffolding tests. Focus on components where behavior preservation is critical.

#### Always Scaffold

| Component Type | Why | How to Find |
|----------------|-----|-------------|
| **Public API surface** | External contracts must not change | Exported functions, HTTP handlers, CLI commands |
| **Data boundaries** | I/O behavior is hard to verify otherwise | DB queries, external API calls, file operations |
| **Business logic with complex rules** | Easy to introduce subtle bugs | Functions with multiple conditionals, calculations |
| **Functions called by many others** | Changes ripple widely | High fan-in in call graph |

#### Skip Scaffolding

| Component Type | Why |
|----------------|-----|
| Internal helpers with single caller | Will be tested through their caller |
| Code with comprehensive existing tests | Existing tests serve as scaffolding |
| Code being deleted | Nothing to preserve |
| Pure data structures | No behavior to capture |

#### Detection Techniques

**Find public API surface:**
```go
// Exported functions in the affected packages
Grep: "^func [A-Z]" internal/handlers/*.go
```

**Find high fan-in functions:**
```bash
# Count references to each function
Grep: "ProcessOrder" --include="*.go" | wc -l
Grep: "ValidateUser" --include="*.go" | wc -l
```

**Find data boundaries:**
```go
// Database operations
Grep: "\.Query\|\.Exec\|\.Get\|\.Select" internal/handlers/*.go

// External API calls
Grep: "http\.Get\|http\.Post\|client\." internal/handlers/*.go

// File operations
Grep: "os\.Open\|os\.Create\|ioutil\." internal/handlers/*.go
```

**Find complex business logic:**
```go
// Functions with multiple conditionals
Grep: "if.*{" internal/handlers/user.go | wc -l  // High count = complex
```

### Step 4: Define Test Input Categories

For each component to scaffold, identify input categories:

```markdown
## Component: CreateUser (internal/handlers/user.go:45)

**Input categories:**
1. Valid user (happy path)
2. Duplicate email (constraint violation)
3. Invalid email format (validation)
4. Missing required fields (validation)
5. Unicode in name (edge case)
6. Maximum length fields (boundary)

**Expected outputs to capture:**
- HTTP status code
- Response body structure
- Database state changes (if any)
- Error messages (exact text matters for client compatibility)
```

### Step 5: Assess Risk and Complexity

Rate each component:

| Component | Risk | Complexity | Scaffolding Priority |
|-----------|------|------------|---------------------|
| CreateUser | High (public API) | Medium | **Must scaffold** |
| validateEmail | Low (internal) | Low | Skip (tested via CreateUser) |
| OrderService.Process | High (business logic) | High | **Must scaffold** |
| formatResponse | Low (utility) | Low | Skip |

### Step 6: Design the Migration Path

Determine the order of changes to minimize risk:

```markdown
## Migration Path

**Phase 1: Scaffolding (no behavior changes)**
1. Generate scaffolding tests for CreateUser, GetUser, UpdateUser
2. Generate scaffolding tests for OrderService.Process
3. Verify all scaffolding tests pass

**Phase 2: Extract (preserve behavior)**
1. Create UserService with same signatures
2. Move logic from handlers to UserService
3. Handler delegates to UserService
4. Verify scaffolding tests still pass

**Phase 3: Refine (allowed behavior changes)**
1. Update error messages (breaking change, documented)
2. Add new validation rules
3. Update scaffolding tests to match new behavior

**Phase 4: Cleanup**
1. Replace scaffolding tests with proper unit tests
2. Remove dead code
3. Update documentation
```

---

## Output: Refactoring Spec

The planning phase produces a refactoring spec that execution can follow:

```yaml
refactoring:
  id: RF-2026-001
  title: "Extract UserService from HTTP handlers"
  goal: "Separate business logic from HTTP handling for testability"

  scope:
    in_scope:
      - internal/handlers/user.go
      - internal/handlers/order.go
    out_of_scope:
      - Authentication logic (separate refactor)
      - Database schema changes

  core_components:
    - name: CreateUser
      location: internal/handlers/user.go:45
      type: http_handler
      risk: high
      scaffold_inputs:
        - category: valid_user
          description: "Complete valid user payload"
        - category: duplicate_email
          description: "Email that already exists"
        - category: invalid_format
          description: "Malformed email address"
        - category: missing_fields
          description: "Required fields omitted"

    - name: GetUser
      location: internal/handlers/user.go:89
      type: http_handler
      risk: medium
      scaffold_inputs:
        - category: existing_user
          description: "Valid user ID"
        - category: not_found
          description: "Non-existent user ID"
        - category: invalid_id
          description: "Malformed user ID"

    - name: ProcessOrder
      location: internal/handlers/order.go:34
      type: http_handler
      risk: high
      scaffold_inputs:
        - category: valid_order
          description: "Complete valid order"
        - category: insufficient_inventory
          description: "Order exceeds available stock"
        - category: invalid_payment
          description: "Payment validation fails"

  migration_path:
    - phase: scaffolding
      tasks:
        - id: RF-001
          title: "Generate scaffolding tests for user handlers"
          components: [CreateUser, GetUser, UpdateUser, DeleteUser]
          criteria:
            - "Scaffolding tests exist for all input categories"
            - "All tests pass against current implementation"

    - phase: extract
      tasks:
        - id: RF-002
          title: "Create UserService interface and implementation"
          depends_on: [RF-001]
          criteria:
            - "UserService struct exists in internal/services/"
            - "All user business logic moved to UserService"
            - "Handlers delegate to UserService"
            - "All RF-001 scaffolding tests pass"

        - id: RF-003
          title: "Create OrderService interface and implementation"
          depends_on: [RF-001]
          criteria:
            - "OrderService struct exists in internal/services/"
            - "All order business logic moved to OrderService"
            - "Handlers delegate to OrderService"
            - "All RF-001 scaffolding tests pass"

    - phase: cleanup
      tasks:
        - id: RF-004
          title: "Replace scaffolding with unit tests"
          depends_on: [RF-002, RF-003]
          criteria:
            - "UserService has dedicated unit tests"
            - "OrderService has dedicated unit tests"
            - "Handler tests verify delegation only"
            - "Scaffolding tests removed"
            - "Test coverage >= 80%"

  success_criteria:
    - "All scaffolding tests pass after each phase"
    - "No changes to public API contracts"
    - "No changes to database schema"
    - "Test coverage maintained or improved"
```

---

## Integration with RECALL

### Before Planning

Query for related architectural decisions:
```
recall_search({query: "[area being refactored] architecture", types: ["decision", "pattern"]})
```

### After Planning

Log the refactoring plan:
```
flight_recorder_log({
  type: "decision",
  content: "Planned refactoring: [title]",
  rationale: "[why this approach]",
  metadata: {
    refactoring_id: "RF-2026-001",
    components_affected: ["CreateUser", "GetUser", ...],
    propagate: true
  }
})
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|--------------------|
| Refactor everything at once | High risk, hard to debug failures | Phase the work, verify after each phase |
| Skip scaffolding for "simple" changes | "Simple" changes break things too | Scaffold public APIs regardless of perceived simplicity |
| Scaffold internal helpers | Wastes time, tests are brittle | Test internal helpers through public interfaces |
| Change behavior during "refactoring" | Conflates two types of changes | Separate refactoring (preserve behavior) from enhancement (change behavior) |
| No explicit scope boundary | Scope creep inevitable | Define out-of-scope explicitly before starting |

---

## Checklist

Before handing off to execution:

```markdown
- [ ] Refactoring goal clearly articulated
- [ ] Target state explicitly defined
- [ ] Scope boundaries documented (in AND out)
- [ ] Impact map complete (direct + indirect)
- [ ] Core components identified with risk assessment
- [ ] Input categories defined for each scaffolded component
- [ ] Migration path ordered to minimize risk
- [ ] Success criteria measurable and specific
- [ ] Related RECALL decisions queried and considered
- [ ] Refactoring plan logged to flight recorder
```
