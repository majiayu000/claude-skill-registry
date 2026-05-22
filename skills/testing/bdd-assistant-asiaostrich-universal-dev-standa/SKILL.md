---
name: bdd
scope: partial
description: |
  Guide developers through Behavior-Driven Development workflow.
  Use when: writing BDD scenarios, using Gherkin syntax, Given-When-Then format, feature files, Three Amigos collaboration.
  Keywords: BDD, behavior-driven, Given When Then, Gherkin, Cucumber, scenario, feature file, step definition, 行為驅動開發.
---

# BDD Assistant

> **Language**: English | [繁體中文](../../locales/zh-TW/skills/bdd-assistant/SKILL.md)

**Version**: 1.0.0
**Last Updated**: 2026-01-19
**Applicability**: Claude Code Skills

---

## Purpose

This skill guides developers through the Behavior-Driven Development workflow, helping them:
- Conduct Discovery sessions to explore requirements
- Write effective Gherkin scenarios in Given-When-Then format
- Create reusable step definitions
- Integrate BDD with TDD for implementation
- Maintain living documentation

---

## Quick Reference

### BDD Workflow Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│  🔍 DISCOVERY Phase                                              │
│  □ Stakeholders identified (Business, Dev, QA)                  │
│  □ User story discussed and understood                          │
│  □ Concrete examples collected (Example Mapping)                │
│  □ Edge cases identified                                        │
│  □ Questions answered or noted for follow-up                    │
├─────────────────────────────────────────────────────────────────┤
│  📝 FORMULATION Phase                                            │
│  □ Scenarios use correct Gherkin syntax                         │
│  □ Scenarios are declarative (WHAT, not HOW)                    │
│  □ Business language used (no technical jargon)                 │
│  □ Each scenario is independent and self-contained              │
│  □ Scenarios have 5-10 steps maximum                            │
│  □ Scenarios reviewed by stakeholders                           │
├─────────────────────────────────────────────────────────────────┤
│  ⚙️ AUTOMATION Phase                                             │
│  □ Step definitions created for all steps                       │
│  □ Step definitions are reusable                                │
│  □ Scenarios fail initially (RED)                               │
│  □ TDD used for unit-level implementations                      │
│  □ All scenarios pass (GREEN)                                   │
│  □ Code refactored and clean                                    │
└─────────────────────────────────────────────────────────────────┘
```

### Gherkin Quick Reference

| Keyword | Purpose | Example |
|---------|---------|---------|
| `Feature` | Container for scenarios | `Feature: User Login` |
| `Scenario` | Single test case | `Scenario: Successful login` |
| `Given` | Set up initial context | `Given I am on the login page` |
| `When` | Trigger action | `When I enter valid credentials` |
| `Then` | Assert outcome | `Then I should see my dashboard` |
| `And`/`But` | Continue previous | `And I should see a welcome message` |
| `Background` | Common setup | Runs before each scenario |
| `Scenario Outline` | Data-driven | Template with Examples table |

### Declarative vs Imperative

```gherkin
# ❌ BAD - Imperative (too detailed, UI-focused)
Scenario: Login
  Given I navigate to "http://example.com/login"
  And I click on the username field
  And I type "john@example.com"
  And I click on the password field
  And I type "secret123"
  And I click the submit button
  Then I should see "Dashboard" in the page title

# ✅ GOOD - Declarative (behavior-focused)
Scenario: Successful login with valid credentials
  Given I am a registered user
  When I login with valid credentials
  Then I should see my dashboard
```

---

## Three Amigos Quick Reference

| Role | Focus | Questions to Ask |
|------|-------|------------------|
| **Business** (PO/BA) | What & Why | "What's the value?", "Who are the users?" |
| **Development** | How | "What's the technical impact?", "Dependencies?" |
| **Testing** (QA) | What if | "What could go wrong?", "Edge cases?" |

---

## Workflow Assistance

### Discovery Phase Guidance

When exploring requirements:

1. **Example Mapping**
   ```
   🟡 User Story: "User can login"
        │
        ├─ 🔵 Rule: "Users must be authenticated"
        │      ├─ 🟢 Example: Valid credentials → login success
        │      └─ 🟢 Example: Invalid credentials → error message
        │
        ├─ 🔵 Rule: "Account lockout after failures"
        │      ├─ 🟢 Example: 3 failures → account locked
        │      └─ 🟢 Example: Locked account → cannot login
        │
        └─ 🔴 Question: Password expiration policy?
   ```

2. **Questions to Ask**
   - What's the happy path?
   - What could go wrong?
   - What are the boundary conditions?
   - What's explicitly out of scope?

### Formulation Phase Guidance

When writing scenarios:

1. **Feature File Structure**
   ```gherkin
   Feature: Feature name
     As a [role]
     I want [feature]
     So that [benefit]

     Background:
       Given common preconditions

     Scenario: Descriptive scenario name
       Given [initial context]
       When [action]
       Then [expected outcome]
   ```

2. **Scenario Style Guidelines**
   - One behavior per scenario
   - Use business language
   - Keep steps declarative
   - Aim for 5-10 steps maximum
   - Make scenarios independent

### Automation Phase Guidance

When implementing:

1. **Step Definition Best Practices**
   ```typescript
   // ✅ Good: Reusable, parameterized
   Given('I have {int} items in my cart', (count) => { ... });

   // ❌ Bad: Specific to one scenario
   Given('I have 3 widgets in my cart', () => { ... });
   ```

2. **BDD + TDD Integration**
   ```
   BDD Scenario (feature level)
        │
        └──▶ Step Definitions
                │
                └──▶ TDD Cycle (unit level)
                      🔴 Write failing unit test
                      🟢 Implement minimal code
                      🔵 Refactor
   ```

---

## Integration with Other Workflows

### BDD + SDD

When working with Spec-Driven Development:

```gherkin
# Reference spec in feature file
# @spec SPEC-001
@SPEC-001
Feature: User Authentication
  Implements SPEC-001 user authentication requirements.

  @AC-1
  Scenario: Successful login
    # Acceptance Criterion 1 from SPEC-001
    ...
```

### BDD + TDD

```
Scenario Level (BDD)           Unit Level (TDD)
─────────────────────          ─────────────────
Scenario: Checkout    ──────▶  test_calculate_total()
  Given cart items             test_apply_discount()
  When checkout                test_create_order()
  Then order created           test_send_email()
```

### BDD + ATDD

```
ATDD: Acceptance Criteria (business sign-off)
  │
  └──▶ BDD: Feature Files (Gherkin scenarios)
         │
         └──▶ TDD: Unit Tests (implementation)
```

---

## Configuration Detection

This skill supports project-specific configuration.

### Detection Order

1. Check `CONTRIBUTING.md` for "Disabled Skills" section
   - If this skill is listed, it is disabled for this project
2. Check `CONTRIBUTING.md` for "BDD Standards" section
3. Check for existing `.feature` files in the codebase
4. If not found, **default to standard BDD practices**

### First-Time Setup

If no configuration found and context is unclear:

1. Ask: "This project hasn't configured BDD preferences. Which BDD tool do you use?"
   - Cucumber (JavaScript/TypeScript)
   - Behave (Python)
   - SpecFlow (C#)
   - Other

2. After selection, suggest documenting in `CONTRIBUTING.md`:

```markdown
## BDD Standards

### BDD Tool
- Cucumber.js

### Feature File Location
- `features/` directory

### Scenario Style
- Declarative (behavior-focused)
- Business language required
- Max 10 steps per scenario
```

---

## Detailed Guidelines

For complete standards, see:
- [BDD Core Standard](../../core/behavior-driven-development.md)
- [BDD Workflow Guide](./bdd-workflow.md)
- [Gherkin Quick Reference](./gherkin-guide.md)

For related standards:
- [TDD Standards](../../core/test-driven-development.md)
- [ATDD Standards](../../core/acceptance-test-driven-development.md)
- [Testing Standards](../../core/testing-standards.md)

---

## Anti-Patterns Quick Detection

| Symptom | Likely Problem | Quick Fix |
|---------|----------------|-----------|
| Scenarios break on UI changes | Imperative style | Use declarative language |
| Business can't read scenarios | Technical jargon | Use business language |
| Scenarios pass but features don't work | Missing scenarios | Better Discovery sessions |
| Too many scenarios | Scenario explosion | Use Scenario Outlines |
| Step definitions duplicated | Not reusable | Extract to helpers |

---

## Related Standards

- [Behavior-Driven Development](../../core/behavior-driven-development.md) - Core BDD standard
- [Acceptance Test-Driven Development](../../core/acceptance-test-driven-development.md) - ATDD standard
- [Test-Driven Development](../../core/test-driven-development.md) - TDD standard
- [Spec-Driven Development](../../core/spec-driven-development.md) - SDD workflow
- [Testing Standards](../../core/testing-standards.md) - Testing framework
- [TDD Assistant](../tdd-assistant/SKILL.md) - TDD skill

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-19 | Initial release |

---

## License

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
