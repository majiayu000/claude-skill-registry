---
name: documentation-patterns
description: Apply when writing code documentation: JSDoc comments, README files, API documentation, and inline comments.
version: 1.0.0
tokens: ~550
confidence: high
sources:
  - https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/
  - https://jsdoc.app/
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [documentation, jsdoc, readme, code-quality]
---

## When to Use

Apply when writing code documentation: JSDoc comments, README files, API documentation, and inline comments.

## Patterns

### Pattern 1: Function Documentation (JSDoc)
```typescript
// Source: https://jsdoc.app/
/**
 * Calculates the total price including tax and discounts.
 *
 * @param items - Array of cart items with price and quantity
 * @param taxRate - Tax rate as decimal (e.g., 0.1 for 10%)
 * @param discountCode - Optional discount code to apply
 * @returns Total price after tax and discounts
 * @throws {InvalidDiscountError} If discount code is invalid
 *
 * @example
 * const total = calculateTotal(
 *   [{ price: 100, quantity: 2 }],
 *   0.1,
 *   'SAVE10'
 * );
 * // Returns: 198 (200 - 10% discount + 10% tax)
 */
function calculateTotal(
  items: CartItem[],
  taxRate: number,
  discountCode?: string
): number {
  // ...
}
```

### Pattern 2: README Structure
```markdown
# Project Name

Brief description (1-2 sentences).

## Features
- Feature 1
- Feature 2

## Quick Start
\`\`\`bash
npm install
npm run dev
\`\`\`

## Usage
Basic usage example with code.

## API Reference
Link to detailed docs or brief overview.

## Configuration
Environment variables and options.

## Contributing
How to contribute.

## License
MIT
```

### Pattern 3: When to Comment
```typescript
// GOOD: Explain WHY, not WHAT
// Rate limit to prevent API abuse (max 100 req/min per user)
const rateLimiter = createRateLimiter({ max: 100, window: 60 });

// GOOD: Explain non-obvious behavior
// Sort descending because latest items should appear first
items.sort((a, b) => b.date - a.date);

// BAD: Obvious from code
// Increment counter by 1
counter++;

// BAD: Outdated comment (code changed, comment didn't)
// Check if user is admin  <-- comment says admin, code checks moderator
if (user.role === 'moderator') { }
```

### Pattern 4: Module/File Header
```typescript
/**
 * @fileoverview Authentication utilities for JWT token management.
 *
 * This module handles:
 * - Token generation and validation
 * - Refresh token rotation
 * - Session management
 *
 * @module auth/tokens
 * @see {@link https://jwt.io/introduction} for JWT spec
 */
```

### Pattern 5: TODO Comments
```typescript
// TODO: Implement caching - Issue #123
// FIXME: Race condition when multiple users update - urgent
// HACK: Workaround for library bug, remove after v2.0 upgrade
// NOTE: This relies on database trigger for audit log

// Include: action, context, reference (issue/ticket)
// TODO(john): Refactor after Q1 - JIRA-456
```

## Anti-Patterns

- **No documentation** - At minimum, public API needs docs
- **Obvious comments** - `i++ // increment i`
- **Stale comments** - Update when code changes
- **Comment instead of fix** - Don't comment bad code, fix it

## Verification Checklist

- [ ] Public functions have JSDoc
- [ ] README has quick start guide
- [ ] Complex logic has WHY comments
- [ ] No stale/outdated comments
- [ ] TODOs have issue references
