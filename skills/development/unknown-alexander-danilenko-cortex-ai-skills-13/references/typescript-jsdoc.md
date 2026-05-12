# TypeScript Documentation

Uses Microsoft Code Documentation style (TSDoc-aligned). **Documentation describes the contract — what something does and why — not how it's implemented internally.** Implementation details (algorithms, internal caching, side effects) belong in inline `//` comments inside the body, never in the doc comment.

When Context7 MCP is available, query `websites/tsdoc` for up-to-date TSDoc tag reference and syntax rules.

**Do not use `@example` blocks.**

## Formatting Rules

Every `/**` comment block places its body on a new line. One-line doc comments are not allowed because they become hard to extend and visually inconsistent.

```typescript
// WRONG — one-line doc comment
/** Unique user identifier. */
id: string;

// CORRECT — body on new line
/**
 * Unique user identifier.
 */
id: string;
```

TSDoc has two tag syntaxes. **Block tags** (`@param`, `@returns`, `@throws`, `@remarks`, `@inheritDoc`, etc.) start their own line and never use curly braces. **Inline tags** (`{@link}`) appear inside running text and require curly braces. Writing `{@param}` with braces is invalid.

**Project convention:** `@inheritDoc` is written as a bare block tag without curly braces and without a declaration reference — always `@inheritDoc` alone, never `{@inheritDoc}` or `{@inheritDoc Foo.bar}`. This diverges from the strict TSDoc spec but keeps the form consistent with other block tags in the codebase.

## Inline Implementation Comments

Doc comments (`/** */`) describe the **contract** — what something does and why, for the consumer. Inline `//` comments inside a function or method body briefly explain **how** a non-trivial block works, so both human and AI readers can grasp the key idea at a glance.

Use them sparingly — only when the block is genuinely complex enough that a reader would otherwise have to puzzle out the intent line-by-line. Keep each comment short; one line is ideal.

```typescript
// CORRECT — doc comment describes the contract; inline comment summarises
// how the body achieves it.
/**
 * Compute the next backoff delay in milliseconds.
 *
 * @param attempt - Zero-based retry attempt number.
 * @returns Delay before the next retry.
 */
function nextDelay(attempt: number): number {
  // Full jitter: cap exponential growth at 30 s, then pick a random point
  // in [0, cap] to spread retries across clients.
  const cap = Math.min(30_000, 1_000 * 2 ** attempt);
  return Math.floor(Math.random() * cap);
}

// WRONG — implementation detail leaked into the doc comment
/**
 * Compute the next backoff delay using full jitter, capping the
 * exponential at 30 s and seeding from Math.random.
 */
```

## Release Tags

Tags like `@public`, `@beta`, `@alpha`, `@internal` are omitted by default. Only include them when the user explicitly requests release-stage annotations.

## Interface Documentation

Interfaces represent abstractions — the _contract_, not the machinery behind it. Document what the consumer needs to know: purpose, parameters, return values, and thrown errors. Never describe implementation details such as internal caching strategies, database queries, retry logic, or algorithmic choices. Those belong in the implementation.

```typescript
/**
 * Service for managing user lifecycle operations.
 */
interface IUserService {
  /**
   * Create a new user account.
   *
   * @param data - Required fields for account creation.
   * @returns The newly created user.
   * @throws {ValidationError} If required fields are missing or invalid.
   */
  create(data: CreateUserDto): Promise<User>;

  /**
   * Find a user by their unique identifier.
   *
   * @param id - User's unique identifier.
   * @returns The user, or `null` if not found.
   */
  findById(id: string): Promise<User | null>;
}
```

## Interface Property Documentation

```typescript
/**
 * Data transfer object for user creation.
 */
interface CreateUserDto {
  /**
   * User's email address.
   * Must be unique across the system.
   */
  email: string;

  /**
   * User's display name.
   */
  name: string;

  /**
   * Optional phone number in E.164 format.
   */
  phone?: string;
}
```

## Implementation Documentation — `@inheritDoc` and DRY

When a class implements an interface, do not repeat documentation that already exists on the interface. The implementation doc starts with `@inheritDoc` on the first line, followed by a blank line, and then only implementation-specific details that a maintainer of this class would need — expressed exclusively through TSDoc block tags such as `@remarks` or `@see`.

**Untagged prose after `@inheritDoc` overrides the inherited description** rather than supplementing it, because TSDoc treats the free-text portion of a comment as the summary. Any note that would otherwise live as a bare paragraph must be placed inside a tag block — most commonly `@remarks` — so the inherited summary is preserved and the implementation note is additive.

**Form:** write the tag bare — no curly braces, no declaration reference. The tag always inherits from the parent declaration automatically, so references like `@inheritDoc IUserService.create` are never needed and must not be used.

```typescript
// WRONG — curly braces
/**
 * {@inheritDoc}
 */

// WRONG — declaration reference
/**
 * @inheritDoc IUserService.create
 */

// CORRECT — bare tag, no arguments
/**
 * @inheritDoc
 */
```

Always use the multi-line form, even when the comment is only `@inheritDoc`. One-line `/** @inheritDoc */` is not allowed — this keeps the form consistent with every other doc comment in the codebase:

```typescript
// WRONG — one-line doc comment
/** @inheritDoc */

// CORRECT — body on a new line
/**
 * @inheritDoc
 */
```

If there _are_ implementation notes to add, place them after a blank line inside a TSDoc tag block — never as a bare paragraph. Reach for `@remarks` only when truly necessary (see the `@remarks` section below):

```typescript
class UserService implements IUserService {
  /**
   * @inheritDoc
   *
   * @remarks
   * - The bcrypt cost factor is pinned at 12 to satisfy the SOC 2
   *   control; lowering it will fail the next audit.
   */
  async create(data: CreateUserDto): Promise<User> {
    // ...
  }

  /**
   * @inheritDoc
   */
  async findById(id: string): Promise<User | null> {
    // ...
  }
}
```

Untagged prose below `@inheritDoc` silently replaces the inherited summary, so the following is incorrect even though it looks reasonable:

```typescript
// WRONG — untagged prose overrides the inherited description
/**
 * @inheritDoc
 *
 * Some documentation clarification
 */

// CORRECT — clarification lives inside a TSDoc tag block
/**
 * @inheritDoc
 *
 * @remarks
 * - Any other documentation clarification
 */
```

Key points:

- `@inheritDoc` is always bare: no braces, no reference.
- `@inheritDoc` must be the first line of the comment body.
- A blank line separates `@inheritDoc` from any additional notes.
- Any additional notes must live inside a TSDoc tag block (`@remarks` or `@see`). Untagged prose overrides the inherited summary instead of supplementing it.
- Only add notes specific to _this_ implementation when the constraint is genuinely non-obvious — never restate the contract.
- Do not re-state parameter descriptions, return types, or thrown errors already documented on the interface.

## Function Documentation

Standalone functions (not implementing an interface) are documented fully. Describe the contract — what + why — never the implementation.

```typescript
/**
 * Calculate total cost including tax.
 *
 * @param items - Line items to sum.
 * @param taxRate - Tax rate as a decimal (e.g., 0.08 for 8%).
 * @returns Total cost with tax applied.
 * @throws {Error} If taxRate is negative or items is empty.
 */
function calculateTotal(items: Item[], taxRate = 0): number {
```

## Class Documentation

Describe the contract of the class — what it represents and why it exists — not how it works internally.

```typescript
/**
 * Connection pool with automatic health checks.
 */
class ConnectionPool {
  /**
   * Create a new pool instance.
   *
   * @param config - Pool configuration options.
   */
  constructor(private readonly config: PoolConfig) {}
}
```

## Simple Mappers and Delegators

When a **class method or standalone function** is a simple mapper or merely delegates to another function or service, document it briefly — a single-line summary is enough. Do not pad with `@param`/`@returns` if the signature is self-explanatory; the contract is already obvious from the types and the name.

**This rule does not apply to interface methods.** Interface methods always require full contract documentation — `@param`, `@returns`, `@throws` as applicable — because the interface defines the contract that consumers depend on, regardless of how trivial any particular implementation turns out to be.

```typescript
// CORRECT — interface method: full contract.
interface IUserRepository {
  /**
   * Find a user by ID.
   *
   * @param id - User's unique identifier.
   * @returns The user, or `null` if not found.
   */
  findById(id: string): Promise<User | null>;
}

// CORRECT — class method that simply delegates: brief one-liner.
class UserRepository implements IUserRepository {
  /**
   * @inheritDoc
   */
  findById(id: string): Promise<User | null> {
    return this.db.users.findUnique({ where: { id } });
  }
}

// CORRECT — standalone delegator: brief one-liner is enough.
/**
 * Format a user's display name.
 */
const formatName = (u: User): string => formatPersonName(u.first, u.last);

// WRONG — needlessly re-documents every parameter for a trivial delegator.
/**
 * Format a user's display name.
 *
 * @param u - The user whose name to format.
 * @returns The formatted display name.
 */
const formatNameVerbose = (u: User): string =>
  formatPersonName(u.first, u.last);
```

## Generic Types

```typescript
/**
 * Paginated response wrapper.
 *
 * @template T - Type of items in the data array.
 */
interface PaginatedResponse<T> {
  /**
   * Items for the current page.
   */
  data: T[];
  total: number;
  page: number;
  limit: number;
}
```

## `@remarks` — Use Sparingly

`@remarks` is **not** a must-have. Avoid it unless absolutely necessary. It is the **only** way to flag that an implementation behaves in a tricky or non-obvious way and to describe the **why** behind that behaviour — never the how. If a reader could reasonably infer the same information from the signature, the summary, or the code itself, omit `@remarks` entirely.

When you do use it, the body is **always a markdown bullet list** — even if there is only one point. This keeps the form consistent so additional points can be added later without restructuring, and makes it visually obvious which parts of a docblock are remarks. When a bullet wraps to a new line, indent the continuation to align with the text after the dash.

```typescript
/**
 * Rate limiter for outbound API calls.
 *
 * @remarks
 * - The upstream provider enforces a 100 req/s hard cap with no burst
 *   allowance. Exceeding it results in a 24-hour ban, so the limiter is
 *   intentionally pinned at 80 req/s to stay safely under the cap.
 */
class ApiRateLimiter {
```

```typescript
/**
 * Session token used for short-lived authentication.
 *
 * @remarks
 * - The 15-minute lifetime is mandated by the security review; do not
 *   extend it without re-approval.
 */
interface SessionToken {
```

```typescript
// WRONG — @remarks body written as a bare paragraph
/**
 * Session token used for short-lived authentication.
 *
 * @remarks
 * The 15-minute lifetime is mandated by the security review.
 */

// WRONG — implementation details do not belong in @remarks
/**
 * Fetch user preferences.
 *
 * @remarks
 * - Uses a Redis LRU cache with a 5-minute TTL, falling back to a
 *   PostgreSQL query via the read replica.
 */
```

## Quick Reference

| Tag | Purpose | Example |
| --- | --- | --- |
| `@param` | Parameter description | `@param name - User's name.` |
| `@returns` | Return value | `@returns The user object.` |
| `@throws` | Exception thrown | `@throws {Error} If invalid.` |
| `@remarks` | Tricky "why", use sparingly | Always a bullet list, even with one item |
| `@see` | URLs and cross-references | `@see https://example.com` |
| `@deprecated` | Mark deprecated | `@deprecated Use v2 instead.` |
| `@template` | Generic type param | `@template T - Item type.` |
| `@readonly` | Read-only property | Cannot modify |
| `@inheritDoc` | Inherit interface docs | `@inheritDoc` (bare, no braces, no reference) |
| `{@link}` | Symbol cross-link, use sparingly | `{@link IUserService}` |

## `{@link}` Usage

Use `{@link Something}` **sparingly — only when absolutely necessary.** Most cross-references read fine as plain text and clutter quickly when every type name becomes a link. Reserve `{@link}` for cases where the relationship is genuinely non-obvious from the surrounding prose.

```typescript
/**
 * Default implementation of {@link IUserService}.
 */
class UserService implements IUserService {
```

**URLs always go in `@see`, never in `{@link}`.** `@see` is the dedicated tag for external references, and tooling renders it more reliably than an inline URL link.

```typescript
/**
 * Validates input against a Zod schema.
 *
 * @see https://zod.dev/
 */
function validate(input: unknown): Result {
```

## Common Patterns

```typescript
// Optional parameters
/**
 * @param options - Optional configuration.
 */

// Default values
/**
 * @param limit - Items per page (default: 10).
 */

// Callback parameters
/**
 * Predicate for filtering items.
 *
 * @param item - Item to evaluate.
 * @returns Whether the item passes the filter.
 */
type FilterFn<T> = (item: T) => boolean;
```
