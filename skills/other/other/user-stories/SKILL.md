---
name: user-stories
description: Write INVEST-compliant user stories with Given-When-Then acceptance criteria. Use when writing user stories, creating acceptance criteria, or during /design Step 4.
type: command
source: Adapted from https://github.com/alirezarezvani/claude-skills/tree/main/product-team/agile-product-owner by alirezarezvani (MIT License)
---

# User Stories

Write high-quality, INVEST-compliant user stories with testable acceptance criteria.

---

## User Story Template

```
As a [persona],
I want to [action/capability],
So that [benefit/value].
```

**Example:**
```
As a marketing manager,
I want to export campaign reports to PDF,
So that I can share results with stakeholders who don't have system access.
```

---

## Story Types

| Type | Template | Example |
|------|----------|---------|
| Feature | As a [persona], I want to [action] so that [benefit] | As a user, I want to filter search results so that I find items faster |
| Improvement | As a [persona], I need [capability] to [goal] | As a user, I need faster page loads to complete tasks without frustration |
| Bug Fix | As a [persona], I expect [behavior] when [condition] | As a user, I expect my cart to persist when I refresh the page |
| Enabler | As a developer, I need to [technical task] to enable [capability] | As a developer, I need to implement caching to enable instant search |

---

## Persona Reference

| Persona | Typical Needs | Context |
|---------|--------------|---------|
| End User | Efficiency, simplicity, reliability | Daily feature usage |
| Administrator | Control, visibility, security | System management |
| Power User | Automation, customization, shortcuts | Expert workflows |
| New User | Guidance, learning, safety | Onboarding |

Adapt personas to your project. Use specific names when possible (e.g., "store owner" instead of "end user").

---

## INVEST Criteria

Validate every story before adding it to the backlog:

| Criterion | Question | Pass If... |
|-----------|----------|------------|
| **I**ndependent | Can this be developed without other uncommitted stories? | No blocking dependencies |
| **N**egotiable | Is the implementation flexible? | Multiple approaches possible |
| **V**aluable | Does this deliver user or business value? | Clear benefit in "so that" |
| **E**stimable | Can the team estimate this? | Understood well enough to size |
| **S**mall | Can this complete in one iteration? | Reasonably scoped |
| **T**estable | Can we verify this is done? | Clear acceptance criteria |

---

## Acceptance Criteria

### Given-When-Then Template

```
Given [precondition/context],
When [action/trigger],
Then [expected outcome].
```

**Examples:**
```
Given the user is logged in with valid credentials,
When they click the "Export" button,
Then a PDF download starts within 2 seconds.

Given the user has entered an invalid email format,
When they submit the registration form,
Then an inline error message displays "Please enter a valid email address."

Given the shopping cart contains items,
When the user refreshes the browser,
Then the cart contents remain unchanged.
```

### AC Checklist

Each story should include criteria for applicable categories:

| Category | Example |
|----------|---------|
| Happy Path | Given valid input, When submitted, Then success message displayed |
| Validation | Should reject input when required field is empty |
| Error Handling | Must show user-friendly message when API fails |
| Performance | Should complete operation within 2 seconds |
| Accessibility | Must be navigable via keyboard only |

Not every category applies to every story. Use judgment.

### Minimum Criteria by Story Size

| Size | Minimum AC Count |
|------|------------------|
| Small (trivial) | 2-3 criteria |
| Medium | 4-6 criteria |
| Large | 5-8 criteria |
| Too large | Split the story |

---

## INVEST Failure Patterns

| Criterion | Red Flag | Fix |
|-----------|----------|-----|
| Independent | "After story X is done..." | Combine stories or resequence |
| Negotiable | Specific implementation in story | Focus on outcome, not solution |
| Valuable | No "so that" clause | Add benefit statement |
| Estimable | Team says "no idea" | Spike first, then story |
| Small | Too large to finish in one iteration | Split into smaller stories |
| Testable | "System should be better" | Add measurable criteria |

---

## Story Splitting

When a story is too large, split using one of these techniques:

| Technique | Example |
|-----------|---------|
| By workflow step | "Create order" -> "Add items" + "Apply discount" + "Submit order" |
| By persona | "User dashboard" -> "Admin dashboard" + "Member dashboard" |
| By data type | "Import data" -> "Import CSV" + "Import Excel" |
| By operation | "Manage users" -> "Add user" + "Edit user" + "Delete user" |
| Happy path first | "Full feature" -> "Basic flow" + "Error handling" + "Edge cases" |

---

## Common Antipatterns

### Story Antipatterns

| Antipattern | Example | Fix |
|-------------|---------|-----|
| Solution story | "Implement React component" | "Display user profile information" |
| Compound story | "Create, edit, and delete users" | Split into three stories |
| Missing persona | "The system will..." | "As an admin, I want to..." |
| No benefit | "I want to see a button" | Add "so that [benefit]" |
| Too vague | "Improve performance" | "Reduce page load to <2 seconds" |
| Technical jargon | "Implement Redis caching" | "Enable instant search results" |

### Acceptance Criteria Antipatterns

| Antipattern | Example | Fix |
|-------------|---------|-----|
| Too vague | "Works correctly" | Specific Given-When-Then |
| Implementation details | "Use PostgreSQL query" | Focus on outcome |
| Missing unhappy path | Only success scenario | Add error cases |
| Untestable | "User is happy" | Measurable behavior |
| Too many | 15+ criteria | Split the story |

---

## References

- Based on [agile-product-owner](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/agile-product-owner) by [alirezarezvani](https://github.com/alirezarezvani) (MIT License)
- Adapted and reduced to user story focus only (no sprint planning, velocity tracking, or epic breakdown)
