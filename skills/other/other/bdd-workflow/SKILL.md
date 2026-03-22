---
name: bdd-workflow
description: Behaviour-Driven Development, Red-Green-Refactor cycle for test-driven development
category: Testing BDD
---

# Skill: bdd-workflow

## What I do

I teach Behaviour-Driven Development at all levels — unit specs (RSpec, Ginkgo, Jest's describe/it), integration tests, and acceptance tests (Gherkin/Cucumber). BDD is a mindset: describe behaviour in domain language, drive development outside-in. The framework is secondary.

## When to use me

- Writing BDD-style unit tests with RSpec, Ginkgo, or Jest's describe/it blocks
- Writing acceptance tests before implementation (outside-in)
- Defining feature behaviour with stakeholders using Gherkin
- Structuring Ginkgo/Gomega specs with Describe/Context/It
- Translating user stories into executable specifications
- Ensuring tests describe behaviour, not implementation

## Core principles

1. **Behaviour over implementation** — Describe what the system does, not how it does it
2. **Shared language** — Use domain terms that stakeholders, testers, and developers all understand
3. **Outside-in** — Start from the acceptance test, work inward to unit tests
4. **Given/When/Then** — Structure every scenario: precondition, action, expected outcome
5. **Living documentation** — Specs are the authoritative source of truth for behaviour

## Patterns & examples

**Gherkin specification (feature file):**
```gherkin
Feature: User registration
  As a new user
  I want to create an account
  So that I can access the platform

  Scenario: Successful registration
    Given no user exists with email "alice@example.com"
    When I register with email "alice@example.com" and password "Str0ng!Pass"
    Then a user account should be created
    And a welcome email should be sent

  Scenario: Duplicate email
    Given a user exists with email "alice@example.com"
    When I register with email "alice@example.com" and password "Str0ng!Pass"
    Then I should see an error "email already registered"
    And no new account should be created
```

**Ginkgo BDD in Go (outside-in):**
```go
Describe("UserService", func() {
    var svc *UserService

    BeforeEach(func() {
        svc = NewUserService(mockRepo)
    })

    Context("when registering a new user", func() {
        It("creates the account and sends welcome email", func() {
            err := svc.Register("alice@example.com", "Str0ng!Pass")
            Expect(err).NotTo(HaveOccurred())
            Expect(mockRepo.FindByEmail("alice@example.com")).NotTo(BeNil())
        })
    })

    Context("when email already exists", func() {
        BeforeEach(func() {
            mockRepo.Add(&User{Email: "alice@example.com"})
        })

        It("returns a conflict error", func() {
            err := svc.Register("alice@example.com", "Str0ng!Pass")
            Expect(err).To(MatchError(ErrEmailExists))
        })
    })
})
```

**BDD vs TDD:**

| Aspect | TDD | BDD |
|--------|-----|-----|
| Focus | Code correctness | System behaviour |
| Language | Developer-centric | Domain-centric |
| Scope | Unit level | Acceptance + unit |
| Starting point | Inside-out | Outside-in |
| Test format | Assert/Expect | Given/When/Then |

**The outside-in cycle:**
```
1. Write acceptance test (Gherkin/Ginkgo) → RED
2. Write unit test for first component needed → RED
3. Implement component → GREEN
4. Refactor → GREEN
5. Repeat steps 2-4 until acceptance test passes
```

## Anti-patterns to avoid

- ❌ **Testing implementation** (`It("calls the database")`) — Test behaviour, not mechanics
- ❌ **Incidental details in scenarios** — Don't include IDs, timestamps, or internal data in Gherkin
- ❌ **Skipping the acceptance test** — Going straight to unit tests loses the outside-in benefit
- ❌ **Too many scenarios per feature** — Focus on key paths; extract edge cases to unit tests
- ❌ **Developer-only language** — If stakeholders can't read it, it's not BDD
- ❌ **Form field typing in steps** (`env.TypeText()`) — Create data via domain/service layer, not by typing into form UI
- ❌ **Form navigation in steps** (`Tab`, `ClearTextField`) — Steps should bypass form mechanics entirely

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Testing-BDD/BDD Workflow.md`

## Related skills

- `ginkgo-gomega` - BDD testing framework for Go
- `cucumber` - Gherkin runner for executable specifications
- `godog` - Go-specific Gherkin runner
- `clean-code` - Apply during the refactor phase
- `tdd-first` - Enforces test-first discipline; ensures every BDD cycle starts with a failing test
- `vhs` - Automated TUI acceptance testing via terminal recordings
