# BDD Scenario Design Skill

> Version: 1.0.0
> Compiler: skill-compiler/1.0.0
> Last Updated: 2026-01-25

Transform bead acceptance criteria into well-formed Gherkin scenarios.

## When to Activate

Use this skill when:
- After claiming bead
- Design scenarios
- Write feature file
- Convert acceptance criteria to Gherkin
- BDD scenario design

## Core Principles

### 1. Prose Is Authoritative

The prose acceptance criteria are the contract; Gherkin is the executable encoding.

*Scenarios must satisfy the prose, not replace it. If Gherkin diverges, prose wins.*

### 2. Declarative Over Imperative

Describe WHAT the system does, not HOW it does it.

*Implementation details change; behavior contracts should be stable.*

### 3. One When-Then Per Scenario

Each scenario tests one behavior with one action and one outcome.

*Focused scenarios are easier to understand, maintain, and debug when they fail.*

### 4. Single-Digit Step Count

Scenarios should have 1-9 steps total; if more, decompose into multiple scenarios.

*Long scenarios indicate mixed concerns or missing abstractions.*

### 5. No UI Details

Scenarios describe domain behavior, not button clicks or form fills.

*UI changes frequently; domain behavior is stable.*

---

## Workflow

### Phase 1: Parse Acceptance Criteria

Extract testable conditions from bead specification.

1. Read bead description and acceptance_criteria field
2. Identify distinct testable behaviors (each becomes a scenario)
3. Note edge cases and error conditions
4. Identify required pre-conditions (Given clauses)

**Outputs:** List of behaviors to test, Pre-conditions for each behavior, Edge cases to cover

### Phase 2: Design Scenarios

Structure behaviors as Gherkin scenarios.

1. For each behavior, write Feature description
2. Write scenario title as behavior statement
3. Write Given steps for pre-conditions
4. Write When step for the action (exactly one)
5. Write Then step(s) for outcomes (1-2 typically)
6. Add typed placeholders for variable data

**Outputs:** Feature description, Scenario structures

### Phase 3: Apply Best Practices

Refine scenarios for clarity and maintainability.

1. Check step count is single-digit
2. Verify no UI implementation details
3. Ensure declarative language (what, not how)
4. Parameterize with Scenario Outline if testing multiple inputs
5. Check for fixture opportunities (repeated data patterns)

**Outputs:** Refined scenarios, Fixture candidates

### Phase 4: Write Feature File

Produce the final .feature file.

1. Create file at tests/features/{bead-id}.feature
2. Write Feature header with description
3. Write Background if common Given steps exist
4. Write each Scenario or Scenario Outline
5. Add Examples tables for Scenario Outlines

**Outputs:** Complete .feature file

---

## Gherkin Syntax Reference

### Feature Structure

```gherkin
Feature: <Feature Name>
  <Optional multi-line description>
  
  Background:
    Given <common setup step>
    
  Scenario: <Behavior description>
    Given <pre-condition>
    When <action>
    Then <expected outcome>
    And <additional outcome>
    
  Scenario Outline: <Parameterized behavior>
    Given <condition with <param:type>>
    When <action with <param:type>>
    Then <outcome with <param:type>>
    
    Examples:
      | param |
      | value1 |
      | value2 |
```

### Step Keywords

| Keyword | Purpose | Rules |
|---------|---------|-------|
| Given | Set up pre-conditions | Can have multiple |
| When | Perform the action | Exactly one per scenario |
| Then | Verify outcomes | At least one per scenario |
| And | Continue previous keyword | Takes role of preceding keyword |
| But | Negative continuation | Less common, use sparingly |

### Typed Placeholders

For rstest-bdd parameter binding:

| Syntax | Type | Example |
|--------|------|---------|
| `<name:string>` | String | `<email:string>` |
| `<name:int>` | Integer | `<count:int>` |
| `<name:float>` | Float | `<price:float>` |
| `<name:word>` | Single word | `<status:word>` |
| `<name>` | Inferred | `<value>` |

---

## Patterns

| Pattern | When | Do | Why |
|---------|------|-----|-----|
| **Behavior-First Naming** | Naming a scenario | `Scenario: <action> should <expected outcome>` | Makes failure messages self-explanatory |
| **Typed Placeholders** | Steps have variable data | Use `<name:type>` format | Enables rstest-bdd parameter binding |
| **Background For Common Setup** | Multiple scenarios share Given steps | Extract to Background block | Reduces duplication |
| **Scenario Outline For Variations** | Same behavior with different inputs | Use Examples table | One scenario tests multiple cases |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Example | Instead |
|--------------|---------|---------|
| **Imperative Steps** | `When I click the submit button` | `When I create the user` |
| **UI Details** | `Given the login form is displayed` | `Given I am not authenticated` |
| **Long Scenarios** | 10+ steps | Split into multiple focused scenarios |
| **Multiple When Clauses** | Two When steps | One When per scenario |
| **Then Without Verification** | `Then the page loads` | `Then the user is created` |

---

## Mapping Acceptance Criteria to Scenarios

### Process

1. **Read each criterion** as a behavior statement
2. **Identify the happy path** - the main success scenario
3. **Identify edge cases** - what can go wrong?
4. **Identify variations** - multiple inputs leading to same outcome?

### One Criterion, Multiple Scenarios

A single acceptance criterion often maps to multiple scenarios:

| Criterion | Scenarios |
|-----------|-----------|
| "User creation works" | Success case, validation errors, duplicate handling |
| "Search returns results" | Results found, no results, search error |

### Coverage Checklist

For each acceptance criterion:
- [ ] Happy path scenario exists
- [ ] Error cases covered
- [ ] Edge cases covered
- [ ] Boundary conditions tested

---

## Quality Checklist

Before completing scenario design:

- [ ] Each acceptance criterion mapped to one or more scenarios
- [ ] Scenario titles describe behavior clearly
- [ ] Single When clause per scenario
- [ ] Step count is single-digit
- [ ] No UI implementation details
- [ ] Declarative language throughout
- [ ] Typed placeholders for parameters
- [ ] Feature file created at tests/features/{bead-id}.feature
- [ ] Prose acceptance criteria satisfied by scenarios

---

## Examples

### Converting User Creation Criteria to Gherkin

**Acceptance Criteria:**
```
User creation succeeds with valid email and password.
Invalid email format returns error.
Duplicate email returns conflict error.
```

**Feature File:**
```gherkin
Feature: User Creation
  As a new user
  I want to create an account
  So that I can access the system

  Scenario: Creating user with valid data should succeed
    Given no user exists with email <email:string>
    When I create a user with email <email:string> and password <password:string>
    Then the user should be created successfully
    And the user should be able to authenticate

  Scenario: Creating user with invalid email should fail
    When I create a user with email "not-an-email" and password "valid123"
    Then the creation should fail with error "invalid_email_format"

  Scenario: Creating user with duplicate email should fail
    Given a user exists with email "existing@example.com"
    When I create a user with email "existing@example.com" and password "valid123"
    Then the creation should fail with error "email_already_exists"
```

### Using Scenario Outline for Variations

**Acceptance Criteria:**
```
Validation rejects passwords under 8 characters, over 128 characters,
and without at least one digit.
```

**Feature File:**
```gherkin
Scenario Outline: Password validation rejects invalid passwords
  When I validate password <password:string>
  Then validation should fail with error <error:string>

  Examples:
    | password     | error                    |
    | "short"      | "password_too_short"     |
    | "NoDigits"   | "password_needs_digit"   |
```

---

## File Organization

```
tests/
  features/
    beadsmith-e12.2.feature    # Named after bead ID
    beadsmith-e12.3.feature
    shared/
      authentication.feature   # Shared scenarios
```

---

## Next Steps

After completing scenario design:

1. Invoke **bdd-step-implementation** skill to write step definitions
2. Wire steps to fixtures from the fixture registry
3. Enter **bdd-red-green-refactor** cycle for implementation

---

## References

- [Gherkin Reference](https://cucumber.io/docs/gherkin/reference/) - Full syntax documentation
- [rstest-bdd](https://github.com/oknozor/rstest-bdd) - Rust BDD framework
- [docs/adr/005-bdd-integration.md](../docs/adr/005-bdd-integration.md) - Architecture decision
- [skills/bdd-step-implementation](../skills/bdd-step-implementation/) - Next skill in workflow
