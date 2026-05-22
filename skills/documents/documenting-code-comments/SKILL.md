---
name: documenting-code-comments
description: Standards for writing self-documenting code and best practices for when to write (and avoid) code comments. Use when auditing, cleaning up, or improving inline code documentation.
---

# Code Comment Guidelines

## Core Philosophy

**The best comment is the one you didn't need to write.**

Self-documenting code reduces maintenance burden and prevents comment drift. Studies show clear naming and structure can reduce onboarding time by up to 30%.

### Writing Style Guidelines

**Tone:** Be direct, practical, and clear. Write in a natural and relaxed tone. Be approachable and down-to-earth with some personality, but light on the slang and excessive casual terms.

**Avoid**:

<AVOID>
- Corporate buzzwords and marketing speak
- AI-sounding language or excessive enthusiasm
- Overly formal/boring documentation style
- Dramatic hyperbole about revolutionary solutions
- Em dashes (—)
- Emojis
- Sycophancy
</AVOID>

### Hierarchy of Documentation

1. **Make code self-documenting** (naming, structure, types)
2. **Use type systems** to document contracts
3. **Add comments only for WHY**, never for WHAT

---

## Refactoring: Preserve Existing Comments

**This skill's guidance applies to writing new code. When refactoring existing code, preserve comments.**

Existing comments represent institutional knowledge. Someone wrote them for a reason. During refactoring:

### Never Remove

- Comments explaining WHY something exists
- Comments warning about gotchas or edge cases
- Comments referencing external context (tickets, specs, RFCs)
- Comments documenting non-obvious business logic

### Update When Necessary

- If refactoring changes behavior the comment describes, update the comment
- If refactoring makes a workaround obsolete, update or remove with the workaround
- Add to existing comments if refactoring introduces new context

### Only Remove When

- The comment is demonstrably incorrect (doesn't match code behavior)
- The comment documents code you're deleting entirely
- The refactoring eliminates the "why" (e.g., removing a workaround makes its explanation obsolete)

```
// BAD: Stripping context during refactoring
// Before: // Retry 3x - payment gateway has transient failures (JIRA-892)
// After:  (comment removed, code unchanged)

// GOOD: Preserving context during refactoring
// Before: // Retry 3x - payment gateway has transient failures (JIRA-892)
// After:  // Retry 3x - payment gateway has transient failures (JIRA-892)

// GOOD: Updating comment when refactoring changes behavior
// Before: // Retry 3x - payment gateway has transient failures
// After:  // Retry with exponential backoff - payment gateway has transient failures
```

---

## When NOT to Write Comments

### Never Comment the Obvious

```
// ❌ BAD: Restates code
const name = user.name; // Get the user's name
items.forEach(item => process(item)); // Loop through items

// ✅ GOOD: Self-documenting
const userName = user.name;
items.forEach(processItem);
```

### Never Duplicate Type Information

```
// ❌ BAD: Types already document this
/** @param {string} email - The email string to validate */
function validateEmail(email: string): boolean {}

// ✅ GOOD: Types speak for themselves
function validateEmail(email: string): boolean {}
```

### Never Leave Stale Comments

```
// ❌ BAD: Comment doesn't match code
// Returns user's full name
const getEmail = () => user.email;

// ✅ GOOD: Remove or fix
const getEmail = () => user.email;
```

---

## When TO Write Comments

### 1. Explain WHY, Not WHAT

```
// ✅ Explains reasoning
// Use exponential backoff - service rate-limits after 3 rapid failures
const backoffMs = Math.pow(2, attempts) * 1000;

// ✅ Documents constraint
// Must run before useEffect to prevent hydration mismatch
useLayoutEffect(() => initTheme(), []);
```

### 2. Warn About Gotchas and Edge Cases

```
// ✅ Critical warning
// IMPORTANT: Assumes UTC - local timezone causes date drift
const dayStart = new Date(date.setHours(0, 0, 0, 0));

// ✅ Non-obvious behavior
// Returns null for deleted users (not undefined) - check explicitly
const user = await getUser(id);
```

### 3. Reference External Context

```
// ✅ Links to ticket
// Workaround for Safari flexbox bug (JIRA-1234)
display: '-webkit-flex';

// ✅ References specification
// Per RFC 7231 §6.5.4, return 404 for missing resources
return res.status(404);
```

### 4. Document Performance Decisions

```
// ✅ Explains optimization with data
// Map for O(1) lookup - benchmarked 3x faster than array.find() at n>100
const userMap = new Map(users.map(u => [u.id, u]));
```

### 5. Complex Business Logic

```
// ✅ Documents business rule
// Discount applies only to orders >$100 AND first-time customers
if (orderTotal > 100 && customer.orderCount === 0) {
```

---

## Comment Formatting Standards

### Single-line Comments

```
// Sentence case, no period for fragments
// Full sentences get periods.
```

### JSDoc/TSDoc for Public APIs

Only when behavior isn't obvious from signature:

```typescript
/**
Validates email format and checks domain blacklist.
  @throws {ValidationError} If format invalid or domain blacklisted
  @example
    validateEmail('user@example.com'); // OK
    validateEmail('spam@blocked.com'); // throws
*/
function validateEmail(email: string): void {}
```

### TODO Format

```
// ✅ GOOD: Actionable with ticket
// TODO(JIRA-567): Replace with batch API when available Q1 2025

// ❌ BAD: No context
// TODO: fix this later
```

---

## Refactor Before Commenting

| Instead of commenting...      | Refactor to...                                      |
| ----------------------------- | --------------------------------------------------- |
| `// Get active users`         | `const activeUsers = users.filter(u => u.isActive)` |
| `// Check if admin`           | `const isAdmin = user.role === 'admin'`             |
| `// 86400000 ms = 1 day`      | `const ONE_DAY_MS = 24 * 60 * 60 * 1000`            |
| `// Handle error case`        | Extract to `handleAuthError(err)` function          |
| `// Calculate total with tax` | `const totalWithTax = calculateTotalWithTax(items)` |

---

## Audit Checklist

When reviewing code comments:

1. **Necessity**: For new code, can it be self-documenting? For existing code, is this comment still accurate? If accurate, keep it.
2. **Accuracy**: Does comment match current code behavior?
3. **Value**: Does it explain WHY, not WHAT?
4. **Freshness**: Is it still relevant?
5. **Actionability**: If TODO, does it have a ticket reference?

---

## Language-Specific Patterns

### TypeScript/JavaScript

- Prefer TypeScript types over JSDoc type annotations
- Use `@deprecated` JSDoc tag for deprecated APIs
- Document thrown errors in JSDoc when not obvious

### Go

- Follow effective Go: first sentence is function name + verb
- Document exported functions, unexported can be brief
- Use `// Deprecated:` comment prefix

### Python

- Use docstrings for modules, classes, functions
- Follow Google or NumPy docstring format consistently
- Type hints reduce need for parameter documentation
