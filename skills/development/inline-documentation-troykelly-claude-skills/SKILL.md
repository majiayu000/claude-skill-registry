---
name: inline-documentation
description: Use when writing code - ensure complete JSDoc, docstrings, and inline comments assuming documentation will be generated from code
allowed-tools: []
model: opus
---

# Inline Documentation

## Overview

Document code assuming docs will be generated from it.

**Core principle:** Future developers (including you) will read this code. Help them.

**Announce at use:** "I'm adding complete inline documentation for this code."

## What to Document

### Always Document

| Element | Documentation Required |
|---------|----------------------|
| Public functions/methods | Full JSDoc/docstring |
| Public classes | Class-level documentation |
| Public interfaces/types | Description of purpose |
| Exported constants | What they control |
| Complex logic | Why, not what |
| Non-obvious decisions | Explain reasoning |

### Skip Documentation For

| Element | Why |
|---------|-----|
| Private trivial helpers | Self-evident |
| Single-line getters | Obvious from name |
| Standard patterns | Well-known idioms |
| Test files | Tests are documentation |

## TypeScript/JavaScript (JSDoc)

### Function Documentation

```typescript
/**
 * Calculates the total price including tax and discounts.
 *
 * @description Applies discounts before tax calculation.
 * Discounts are applied in order of magnitude (largest first).
 *
 * @param items - Line items to calculate
 * @param taxRate - Tax rate as decimal (e.g., 0.08 for 8%)
 * @param discounts - Optional discount codes to apply
 * @returns Total price after discounts and tax
 *
 * @throws {ValidationError} If taxRate is negative
 * @throws {InvalidDiscountError} If discount code is invalid
 *
 * @example
 * ```typescript
 * const total = calculateTotal(
 *   [{ price: 100 }, { price: 50 }],
 *   0.08,
 *   ['SAVE10']
 * );
 * // Returns: 145.80 (150 - 10% discount = 135, + 8% tax)
 * ```
 */
function calculateTotal(
  items: LineItem[],
  taxRate: number,
  discounts?: string[]
): number {
  // Implementation
}
```

### Class Documentation

```typescript
/**
 * Manages user authentication and session lifecycle.
 *
 * @description Handles login, logout, session refresh, and
 * multi-device session management. Uses JWT for stateless
 * authentication with Redis for session invalidation tracking.
 *
 * @example
 * ```typescript
 * const auth = new AuthService(config);
 * const session = await auth.login(credentials);
 * await auth.logout(session.id);
 * ```
 */
class AuthService {
  /**
   * Creates an AuthService instance.
   *
   * @param config - Authentication configuration
   * @param config.jwtSecret - Secret for signing JWTs
   * @param config.sessionTtl - Session time-to-live in seconds
   */
  constructor(private config: AuthConfig) { }

  /**
   * Authenticates a user and creates a session.
   *
   * @param credentials - User credentials
   * @returns Session object with tokens
   * @throws {InvalidCredentialsError} If authentication fails
   */
  async login(credentials: Credentials): Promise<Session> { }
}
```

### Interface Documentation

```typescript
/**
 * Configuration for the caching layer.
 *
 * @description Controls cache behavior including TTL,
 * invalidation strategy, and storage backend selection.
 */
interface CacheConfig {
  /** Time-to-live in seconds. Default: 3600 */
  ttl: number;

  /** Maximum items to cache. Default: 1000 */
  maxSize: number;

  /**
   * Storage backend to use.
   * - 'memory': In-process LRU cache
   * - 'redis': Distributed Redis cache
   */
  backend: 'memory' | 'redis';

  /** Redis connection string (required if backend is 'redis') */
  redisUrl?: string;
}
```

## Python (Docstrings)

### Function Documentation

```python
def calculate_total(
    items: list[LineItem],
    tax_rate: float,
    discounts: list[str] | None = None
) -> float:
    """Calculate the total price including tax and discounts.

    Applies discounts before tax calculation. Discounts are applied
    in order of magnitude (largest first).

    Args:
        items: Line items to calculate.
        tax_rate: Tax rate as decimal (e.g., 0.08 for 8%).
        discounts: Optional discount codes to apply.

    Returns:
        Total price after discounts and tax.

    Raises:
        ValidationError: If tax_rate is negative.
        InvalidDiscountError: If discount code is invalid.

    Example:
        >>> total = calculate_total(
        ...     [LineItem(price=100), LineItem(price=50)],
        ...     0.08,
        ...     ['SAVE10']
        ... )
        >>> total
        145.80  # 150 - 10% = 135, + 8% tax
    """
    pass
```

### Class Documentation

```python
class AuthService:
    """Manages user authentication and session lifecycle.

    Handles login, logout, session refresh, and multi-device
    session management. Uses JWT for stateless authentication
    with Redis for session invalidation tracking.

    Attributes:
        config: Authentication configuration.
        redis: Redis client for session tracking.

    Example:
        >>> auth = AuthService(config)
        >>> session = await auth.login(credentials)
        >>> await auth.logout(session.id)
    """

    def __init__(self, config: AuthConfig) -> None:
        """Create an AuthService instance.

        Args:
            config: Authentication configuration including
                JWT secret and session TTL.
        """
        pass
```

## Inline Comments

### When to Use

```typescript
// Complex algorithms
function dijkstra(graph: Graph, start: Node): Map<Node, number> {
  // Use priority queue for O(E log V) complexity
  // instead of linear search O(V²)
  const queue = new PriorityQueue<Node>();

  // Initialize all distances to infinity except start
  const distances = new Map<Node, number>();

  // ... implementation with strategic comments
}
```

### Explain Why, Not What

```typescript
// BAD: Explains what (obvious from code)
// Increment counter by 1
counter++;

// GOOD: Explains why (not obvious)
// Retry count starts at 1 because initial attempt doesn't count
counter++;
```

### Link to Context

```typescript
// Per RFC 7519, JWT expiry is in seconds since epoch
const exp = Math.floor(Date.now() / 1000) + ttlSeconds;

// See issue #234 for why we can't use the simpler approach
const result = complexWorkaround();
```

### Mark Non-Obvious Behavior

```typescript
// IMPORTANT: Order matters here - auth must run before rate limit
app.use(authMiddleware);
app.use(rateLimitMiddleware);

// WARNING: This modifies the input array in place
items.sort((a, b) => a.priority - b.priority);
```

## Documentation Checklist

For each public element:

### Functions/Methods
- [ ] Brief description (first line)
- [ ] Detailed description (if complex)
- [ ] All parameters documented
- [ ] Return value documented
- [ ] Exceptions documented
- [ ] Example provided (if non-obvious usage)

### Classes
- [ ] Class purpose described
- [ ] Usage example provided
- [ ] All public methods documented
- [ ] Public properties documented

### Interfaces/Types
- [ ] Purpose described
- [ ] Each property documented
- [ ] Valid values noted (for enums/unions)

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| No documentation | Document all public APIs |
| Stale documentation | Update docs with code changes |
| Obvious comments | Only document non-obvious |
| Missing examples | Add examples for complex APIs |
| Copy-paste docs | Write specific documentation |

## Generating Documentation

### TypeScript

```bash
# Using TypeDoc
npx typedoc src/index.ts --out docs

# Using TSDoc
npx @microsoft/api-extractor run
```

### Python

```bash
# Using Sphinx
sphinx-apidoc -o docs/source src/
sphinx-build docs/source docs/build

# Using pdoc
pdoc --html src/ -o docs/
```

## Integration

This skill is applied by:
- `issue-driven-development` - Step 7
- `comprehensive-review` - Documentation criterion

This skill ensures:
- Maintainable code
- Onboarding ease
- Generated documentation quality
- API discoverability
