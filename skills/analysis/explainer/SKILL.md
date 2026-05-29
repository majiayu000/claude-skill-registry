---
name: explainer
description: Use when explaining code, technical concepts, or implementation decisions. Provides structured approach to creating clear, understandable explanations tailored to the audience.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Explainer Skill

Create clear, insightful explanations of code, concepts, and technical decisions.

## Core Principle

**Clarity over completeness.** An explanation is only useful if it's understood.

## Explanation Process

### 1. Understand the Question

**What are they really asking?**

- Literal question: "What does this do?"
- Deeper question: "Why does this exist?" or "How does this work?"
- Context matters: Junior dev vs senior dev needs different explanations

### 2. Gather Full Context

**Read before explaining:**

- The code in question (obvious)
- Surrounding code (function, class, module)
- Related code (what calls it, what it calls)
- Tests (reveal intended behavior)
- Comments (capture original reasoning)
- Git history (understand evolution)

**Anti-pattern:** Explaining code you only partially understand

### 3. Structure the Explanation

**Start broad, then narrow:**

1. **One-sentence summary**: What it does in plain English
2. **Purpose**: Why it exists, what problem it solves
3. **High-level approach**: How it solves the problem (conceptually)
4. **Implementation details**: Specific code patterns, algorithms
5. **Edge cases**: Unusual scenarios handled
6. **Related concepts**: Connections to other parts of the system

### 4. Choose the Right Level

**Match explanation to context:**

**For "What does this do?"**

```
BAD: "It's a reducer function that takes state and action..."
GOOD: "This manages the shopping cart state. When you add/remove
       items, it updates the cart and recalculates the total."
```

**For "How does this work?"**

```
BAD: "It just loops through items and sums prices."
GOOD: "It iterates through cart items, applies discounts to each,
       then sums the discounted prices. Tax is calculated on the
       subtotal, not individual items, to avoid rounding errors."
```

**For "Why this approach?"**

```
BAD: "Because it's faster."
GOOD: "We chose this over X because: (1) handles async updates
       correctly, (2) prevents race conditions when multiple users
       modify the cart, (3) makes testing easier. Trade-off is
       slightly more complex code."
```

## Explanation Patterns

### Code Explanation Format

```markdown
## What it does

[One-sentence plain English summary]

## Purpose

[Why this code exists, what problem it solves]

## How it works

1. [High-level step 1]
2. [High-level step 2]
3. [High-level step 3]

### Key details

- [Important implementation detail 1]
- [Important implementation detail 2]

### Example

[Concrete example showing usage]

## Related

- [Link to related code/docs]
```

### Concept Explanation Format

```markdown
## [Concept Name]

[One-sentence definition]

### Why it matters

[Practical importance, when you'd use it]

### How it works

[High-level explanation without jargon]

### Example

[Concrete, relatable example]

### In our codebase

[Where we use this concept, with links]

### Common pitfalls

[What to watch out for]
```

### Decision Explanation Format

```markdown
## Decision: [What was decided]

### Context

[Situation that required a decision]

### Options considered

1. **[Option 1]**: [Brief description]
   - Pros: [Key benefits]
   - Cons: [Key drawbacks]

2. **[Option 2]**: [Brief description]
   - Pros: [Key benefits]
   - Cons: [Key drawbacks]

### Choice: [Selected option]

**Rationale:**
[Why this option was chosen over others]

### Trade-offs accepted

[What we gave up by choosing this approach]

### References

[Links to discussions, docs, related decisions]
```

## Writing Guidelines

### Be Concrete

**Bad:** "This uses a common design pattern for state management"
**Good:** "This uses the Redux pattern: all state changes go through a central store via actions and reducers"

### Use Analogies (When Helpful)

**Example:**
"Think of this like a restaurant kitchen:

- Actions are customer orders
- Reducers are chefs preparing food
- Store is the completed order waiting area"

**Warning:** Don't force analogies. If it's clearer without, skip it.

### Show, Don't Just Tell

```typescript
// BAD explanation:
// "This function filters and maps the array"

// GOOD explanation:
// "This function finds all active users and formats them for display:
const displayUsers = users
  .filter(u => u.status === 'active')  // Only show active users
  .map(u => ({                         // Convert to display format
    id: u.id,
    name: `${u.firstName} ${u.lastName}`,
    joined: formatDate(u.createdAt)
  }))
```

### Avoid Jargon (Unless Explaining Jargon)

**Bad:** "This leverages a memoized selector with referential equality optimization"
**Good:** "This caches the filtered list so we don't recalculate it every render, improving performance"

**Exception:** When explaining what jargon means:
"Memoization means caching function results so we don't recompute the same thing twice."

## Common Explanation Scenarios

### Explaining Error Messages

```markdown
## Error: "Cannot read property 'map' of undefined"

**What happened:**
You're trying to use `.map()` on something that's `undefined`.

**Where:** [Link to line]

**Why:**
The `users` array hasn't loaded yet (async), so it's `undefined`
when the component first renders.

**Fix:**
```typescript
// Before
users.map(u => ...)

// After
{users?.map(u => ...) || <Loading />}
```

**Why this works:**
`?.` is optional chaining - it only calls `.map()` if `users`
exists. If not, it shows a loading state instead.

```

### Explaining "Why Not X?"

```markdown
## Why not use X?

**Context:** [What X is]

**Reasons we chose Y instead:**

1. **[Primary reason]**: [Explanation]
2. **[Secondary reason]**: [Explanation]
3. **[Tertiary reason]**: [Explanation]

**Trade-offs:**
Y is slower than X, but the reliability benefit outweighs the
50ms performance difference.

**When X would be better:**
If we needed real-time updates (< 100ms), X would be the right choice.
```

### Explaining Legacy Code

```markdown
## Legacy: [Module Name]

**What it does:** [Current function]

**History:**
This was written in 2019 when [context]. At the time, [justification].

**Why it looks odd today:**
Modern approaches would use [better pattern], but this works and
changing it isn't worth the risk.

**If you must modify it:**
1. [Key constraint to preserve]
2. [Another constraint]
3. Add tests first (none exist currently)

**Related:** See [modern equivalent] for new code.
```

## Anti-Patterns

### ❌ Assuming Knowledge

```
BAD: "This uses HOCs to inject props via connect()"
GOOD: "This connects the component to Redux, giving it access
       to the store data it needs. See: [Redux docs link]"
```

### ❌ Over-explaining Obvious Code

```typescript
// Don't explain this:
const total = price * quantity  // Multiplies price by quantity

// Do explain this:
const total = price * quantity * (1 - discount) * TAX_RATE
// Discount applied before tax, per accounting requirements
```

### ❌ Vague References

```
BAD: "Similar to what we do in other places"
GOOD: "Similar to UserService.findActive() in services/user.ts:45"
```

### ❌ Explaining *How* When Asked *Why*

**Question:** "Why do we use a Set here instead of an Array?"

**Bad:** "A Set is initialized with `new Set()` and supports `.add()` and `.has()` methods..."

**Good:** "A Set automatically removes duplicates. We need unique user IDs, and Set handles that for us. An Array would require manual duplicate checking."

## Verification

**After explaining, check:**

- ✅ Does this answer the actual question asked?
- ✅ Is it understandable without reading it 3 times?
- ✅ Are technical terms explained or linked?
- ✅ Are there concrete examples?
- ✅ Does it avoid unnecessary complexity?
- ✅ Would someone new to the codebase understand this?

## Integration with Other Skills

- Use **code-reviewer** skill when explaining code quality issues
- Use **proof-of-work** skill when explaining behavior (show actual output)
- Use **simplicity-principles** skill when explaining why simpler is better
- Reference other skills when explaining patterns they cover

## Remember

**The best explanation is the one that's understood, not the one that's most complete.**

If in doubt, start simple and add detail only when needed.
