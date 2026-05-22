---
document_name: "code-quality.skill.md"
location: ".claude/skills/code-quality.skill.md"
codebook_id: "CB-SKILL-CODEQUAL-001"
version: "1.0.0"
date_created: "2026-01-03"
date_last_edited: "2026-01-03"
document_type: "skill"
purpose: "Procedural guide for maintaining high code quality standards"
category: "skills"
subcategory: "development"
skill_metadata:
  category: "development"
  complexity: "intermediate"
  estimated_time: "varies"
  prerequisites:
    - "Access to codebase"
    - "Understanding of project standards"
related_docs:
  - "standards/code-patterns.md"
  - "standards/naming-conventions.md"
maintainers:
  - "head-cook"
status: "active"
tags:
  - "skill"
  - "code-quality"
  - "standards"
  - "development"
ai_parser_instructions: |
  This skill covers code quality procedures.
  Section markers: === SECTION ===
  Procedure markers: <!-- PROCEDURE:name:START/END -->
  Checklists use - [ ] format.
---

# Code Quality Skill

[!FIXED!]
## Purpose

This skill provides procedures for maintaining high code quality standards. It covers code review preparation, refactoring guidelines, and quality checks.

**When to use:**
- Before submitting code for review
- During refactoring
- When reviewing others' code
- When quality issues are identified
[!FIXED!]

---

=== PREREQUISITES ===
<!-- AI:PREREQUISITES:START -->

Before using this skill:

- [ ] Access to @ref(CB-STD-PATTERNS-001) if exists
- [ ] Access to @ref(CB-STD-NAMING-001) if exists
- [ ] Understanding of project's linter/formatter settings
- [ ] Test framework available

<!-- AI:PREREQUISITES:END -->

---

=== PROCEDURE: PRE-REVIEW CHECKLIST ===
<!-- PROCEDURE:pre-review:START -->

Run this checklist before submitting code for review.

### Automated Checks

1. **Run linter**
   ```bash
   # Example for JavaScript
   npm run lint

   # Fix auto-fixable issues
   npm run lint:fix
   ```

2. **Run formatter**
   ```bash
   # Example for Prettier
   npm run format
   ```

3. **Run tests**
   ```bash
   npm test
   ```

4. **Check coverage**
   ```bash
   npm run test:coverage
   ```

### Manual Checks

- [ ] No commented-out code
- [ ] No console.log/print debug statements
- [ ] No hardcoded values (use constants)
- [ ] No magic numbers
- [ ] All functions have purpose comments (if complex)
- [ ] Variable names are descriptive
- [ ] Error handling is appropriate
- [ ] No duplicate code (DRY)
- [ ] Functions are single-purpose
- [ ] File length is reasonable (<300 lines preferred)

### Self-Review Questions

- [ ] Does this code do what the specification requires?
- [ ] Would I understand this code in 6 months?
- [ ] Are edge cases handled?
- [ ] Are error messages helpful?
- [ ] Is this the simplest solution?

<!-- PROCEDURE:pre-review:END -->

---

=== PROCEDURE: REFACTORING ===
<!-- PROCEDURE:refactor:START -->

### When to Refactor

| Trigger | Action |
|---------|--------|
| Function > 50 lines | Extract helper functions |
| Duplication detected | Create shared utility |
| Deep nesting (>3 levels) | Flatten with early returns |
| Complexity score > 10 | Simplify logic |
| Unclear naming | Rename for clarity |

### Refactoring Steps

1. **Write tests first**
   - Ensure existing behavior is covered
   - Tests should pass before AND after refactoring

2. **Make small changes**
   - One refactoring at a time
   - Commit between refactorings
   - Keep changes reversible

3. **Verify tests still pass**
   - After each change
   - No behavior change unless intentional

4. **Document in buildlog**
   ```markdown
   | HH:MM | #micro-decision | Refactored payment processing to use strategy pattern | CB-ARCH-OVERVIEW |
   ```

### Common Refactorings

| Problem | Solution |
|---------|----------|
| Long function | Extract Method |
| Large class | Extract Class |
| Feature envy | Move Method |
| Duplicated code | Extract shared function |
| Long parameter list | Introduce Parameter Object |
| Switch statements | Replace with Polymorphism |

<!-- PROCEDURE:refactor:END -->

---

=== PROCEDURE: NAMING ===
<!-- PROCEDURE:naming:START -->

### General Rules

- Names should reveal intent
- Use pronounceable names
- Use searchable names
- Avoid encodings (Hungarian notation)

### Naming Patterns

| Type | Pattern | Example |
|------|---------|---------|
| Boolean | is/has/can/should prefix | `isActive`, `hasPermission` |
| Function | verb phrase | `calculateTotal`, `validateInput` |
| Event handler | handle prefix | `handleClick`, `handleSubmit` |
| Collection | plural | `users`, `items` |
| Constants | UPPER_SNAKE | `MAX_RETRIES`, `API_URL` |

### Name Length Guidelines

| Scope | Length |
|-------|--------|
| Loop variable | 1-3 chars (`i`, `idx`) |
| Local variable | Short, clear |
| Function | Descriptive |
| Class | Very descriptive |
| Global | Long, specific |

<!-- PROCEDURE:naming:END -->

---

=== PROCEDURE: ERROR HANDLING ===
<!-- PROCEDURE:errors:START -->

### Error Handling Guidelines

1. **Fail fast**
   - Validate inputs early
   - Return early on error conditions

2. **Be specific**
   - Use specific error types
   - Include context in error messages

3. **Don't swallow errors**
   ```javascript
   // BAD
   try { doSomething() } catch (e) { }

   // GOOD
   try { doSomething() } catch (e) {
     logger.error('Failed to do something', { error: e });
     throw e;
   }
   ```

4. **Handle at appropriate level**
   - Don't catch if you can't handle
   - Let errors bubble up when appropriate

### Error Message Format

```
[What happened]: [Why it matters]: [What to do]

Example:
"Failed to load user profile: User ID not found: Please verify the user exists"
```

<!-- PROCEDURE:errors:END -->

---

=== PROCEDURE: DOCUMENTATION ===
<!-- PROCEDURE:documentation:START -->

### When to Document

- Complex algorithms
- Non-obvious business logic
- Public APIs
- Configuration options
- Workarounds for known issues

### When NOT to Document

- Obvious code
- Self-explanatory functions
- Standard patterns

### Comment Format

```javascript
/**
 * Calculates the discounted price based on user tier.
 *
 * Premium users get 20% off, Gold users get 10% off.
 * Discounts don't stack with sale prices.
 *
 * @param {number} price - Original price in cents
 * @param {string} userTier - User membership tier
 * @returns {number} Final price in cents
 */
function calculateDiscountedPrice(price, userTier) { ... }
```

### Inline Comments

```javascript
// Use local timezone for display but UTC for storage
const displayDate = formatLocal(date);
const storageDate = date.toISOString();
```

<!-- PROCEDURE:documentation:END -->

---

=== PROCEDURE: TESTING ===
<!-- PROCEDURE:testing:START -->

### Test Structure

```
Arrange: Set up test data and conditions
Act: Execute the code under test
Assert: Verify the results
```

### Test Naming

```javascript
describe('calculateDiscount', () => {
  it('should apply 20% discount for premium users', () => { ... });
  it('should return original price for basic users', () => { ... });
  it('should throw error for negative prices', () => { ... });
});
```

### Coverage Guidelines

| Type | Target |
|------|--------|
| Unit tests | 80%+ line coverage |
| Critical paths | 100% coverage |
| Edge cases | All identified cases |
| Error paths | All error conditions |

### What to Test

- [ ] Happy path (expected inputs)
- [ ] Edge cases (boundaries, empty, null)
- [ ] Error conditions
- [ ] Security-sensitive operations

<!-- PROCEDURE:testing:END -->

---

=== ANTI-PATTERNS ===
<!-- AI:ANTIPATTERNS:START -->

| Anti-Pattern | Why Bad | Alternative |
|--------------|---------|-------------|
| God objects | Unmaintainable | Split by responsibility |
| Deep nesting | Hard to read | Early returns, extraction |
| Premature optimization | Wastes time | Profile first |
| Copy-paste | Duplication | Extract shared code |
| Magic numbers | Unclear intent | Named constants |
| Commented code | Clutter | Delete (git has history) |
| Long functions | Hard to test | Extract methods |
| Global state | Side effects | Dependency injection |

<!-- AI:ANTIPATTERNS:END -->

---

=== QUALITY METRICS ===
<!-- AI:METRICS:START -->

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Test coverage | >80% | Coverage tool |
| Cyclomatic complexity | <10 per function | Linter rule |
| Function length | <50 lines | Linter rule |
| File length | <300 lines | Manual review |
| Nesting depth | <3 levels | Linter rule |

<!-- AI:METRICS:END -->

---

=== RELATED DOCUMENTS ===
<!-- AI:RELATED:START -->

| Document | Codebook ID | Relationship |
|----------|-------------|--------------|
| code-patterns.md | CB-STD-PATTERNS-001 | Pattern standards |
| naming-conventions.md | CB-STD-NAMING-001 | Naming rules |
| pr-review.skill.md | CB-SKILL-PRREVIEW-001 | Review procedures |

<!-- AI:RELATED:END -->
