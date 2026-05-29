---
name: notetaker-fundamentals
description: Use when leaving structured notes, comments, and annotations in code. Covers AI note-taking patterns, TODO formats, context preservation, and development breadcrumbs for future AI assistants and human developers.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Note-Taking Fundamentals for AI-Assisted Development

Effective note-taking patterns for AI assistants to leave meaningful context in codebases.

## Philosophy

When AI assistants make changes to code, they should leave breadcrumbs for future AI assistants and human developers. Notes should:

- **Preserve context** about why decisions were made
- **Signal uncertainty** where alternative approaches exist
- **Mark incomplete work** that needs follow-up
- **Link to relevant context** (issues, PRs, documentation)
- **Explain non-obvious patterns** that might confuse readers

## Note Formats

### AI Development Notes

Special comment format for AI-to-AI communication:

```typescript
// AI-DEV-NOTE: This function uses a cache-first strategy because
// the data rarely changes and network calls were causing performance
// issues. See performance profiling in PR #123.
```

```python
# AI-DEV-NOTE: The validation order matters here - we must check
# authentication before authorization to avoid leaking user existence.
# Alternative approach using middleware was considered but rejected
# due to increased complexity.
```

**When to use:**

- Explaining non-obvious implementation decisions
- Documenting alternative approaches that were considered
- Linking to related context (PRs, issues, discussions)
- Warning about subtle bugs or edge cases
- Preserving rationale for future refactoring decisions

### Structured TODO Comments

Enhanced TODO format with context:

```javascript
// TODO(ai/context): Extract this validation logic into a separate
// validator class. Currently duplicated in 3 places:
// - src/api/users.ts:45
// - src/api/auth.ts:78
// - src/validators/user.ts:12
// Blocked by: Waiting for PR #456 to merge validator base class
```

```go
// TODO(ai/performance): This O(n²) loop should be optimized.
// Profiling shows 45% of request time spent here when n > 100.
// Consider: hash map lookup or binary search after sorting.
// Impact: High - affects main user flow
// Effort: Medium - 2-3 hours estimated
```

**TODO Format Structure:**

```
// TODO(ai/<category>): <Brief description>
// <Additional context>
// <Alternative approaches>
// <Blockers/Dependencies>
// <Impact/Priority>
```

**Common categories:**

- `ai/refactor` - Code structure improvements
- `ai/performance` - Optimization opportunities
- `ai/security` - Security considerations
- `ai/accessibility` - A11y improvements
- `ai/testing` - Test coverage gaps
- `ai/docs` - Documentation needs
- `ai/context` - Context preservation
- `ai/edge-case` - Unhandled edge cases

### Decision Records

Inline decision records for significant choices:

```rust
// DECISION: Using Arc<RwLock<T>> instead of Mutex<T>
// RATIONALE: Read-heavy workload (95% reads, 5% writes) benefits
// from RwLock's concurrent read access. Benchmarks showed 3x throughput
// improvement with RwLock under typical load patterns.
// ALTERNATIVES_CONSIDERED:
//   - Mutex<T>: Simpler but slower for read-heavy workload
//   - atomic types: Not suitable for complex state
// DATE: 2025-12-04
// AUTHOR: Claude (AI Assistant)
```

**When to use decision records:**

- Choosing between competing patterns/libraries
- Performance trade-offs (memory vs speed, etc.)
- Architecture decisions affecting multiple files
- Security-sensitive choices
- Decisions that will be questioned later

### Context Preservation

Leaving breadcrumbs for future understanding:

```typescript
// CONTEXT: This weird-looking workaround is necessary because Safari
// doesn't support the standard API (as of v17.2). Filed webkit bug:
// https://bugs.webkit.org/show_bug.cgi?id=123456
// Remove this when Safari support lands (check caniuse.com)
if (isSafari) {
  // Fallback implementation
}
```

```python
# CONTEXT: Database migration added 'deleted_at' column (migration_003)
# but we're still using 'is_deleted' for backward compatibility during
# the transition period. Can remove 'is_deleted' after 2025-12-31
# when all old records are migrated.
```

### Uncertainty Markers

Signaling areas where AI is uncertain:

```java
// AI-UNCERTAIN: This might not handle timezone edge cases correctly
// around DST transitions. Manual review recommended by a developer
// familiar with timezone handling.
```

```swift
// AI-UNCERTAIN: Not sure if this is thread-safe in all scenarios.
// Consider adding synchronization or having a concurrency expert review.
```

## Note Placement Guidelines

### Where to Place Notes

**Good placements:**

```typescript
// AI-DEV-NOTE: Complex business logic follows - this implements the
// three-tier approval workflow described in docs/workflows.md
function processApproval(request: ApprovalRequest) {
  // Implementation...
}
```

**Bad placements:**

```typescript
function processApproval(request: ApprovalRequest) {
  const step1 = validate(request);
  // AI-DEV-NOTE: This whole function is complex
  const step2 = process(step1);
  // Bad - note is buried in implementation details
}
```

### Proximity Rules

- Place notes **immediately before** the code they describe
- For file-level notes, place at the **top after imports**
- For function-level notes, place **immediately before the function**
- For inline notes, place on the **line above** the relevant code

### Note Density

Avoid over-annotation:

```typescript
// ❌ TOO MANY NOTES
// AI-DEV-NOTE: Parsing user input
const input = parseInput(raw);
// AI-DEV-NOTE: Validating the input
const valid = validate(input);
// AI-DEV-NOTE: Processing the result
const result = process(valid);

// ✅ APPROPRIATE DENSITY
// AI-DEV-NOTE: Standard validation pipeline - parse, validate, process
// Each step can throw ValidationError which is handled by middleware
const input = parseInput(raw);
const valid = validate(input);
const result = process(valid);
```

## Cross-Referencing

### Linking to Issues/PRs

```javascript
// AI-DEV-NOTE: Implements user story from issue #1234
// See PR #1245 for discussion on alternative approaches
```

### Linking to Documentation

```python
# AI-DEV-NOTE: Algorithm explained in docs/algorithms/rate-limiting.md
# Based on token bucket algorithm: https://en.wikipedia.org/wiki/Token_bucket
```

### Linking to Other Code

```go
// AI-DEV-NOTE: Mirror of validation logic in api/v2/handlers.go:123
// Keep these in sync or extract to shared validator
```

## Note Maintenance

### Expiration Dates

For temporary notes or workarounds:

```typescript
// AI-DEV-NOTE: Temporary workaround for API v1 compatibility
// REMOVE_AFTER: 2025-12-31 (when v1 API is fully deprecated)
```

```python
# TODO(ai/temporary): Using placeholder implementation
# REPLACE_WHEN: Real authentication service is deployed
```

### Note Updates

When modifying code with existing notes:

```javascript
// AI-DEV-NOTE: [UPDATED 2025-12-04] Originally used synchronous
// processing but switched to async to prevent UI blocking.
// Previous note preserved for context.
// [ORIGINAL 2025-11-15] This processes items synchronously...
```

## Anti-Patterns

### Don't

❌ Leave vague notes

```javascript
// AI-DEV-NOTE: This is important
// Bad - no context about WHY it's important
```

❌ Over-explain obvious code

```python
# AI-DEV-NOTE: This increments the counter by 1
count += 1  # Obvious from code
```

❌ Leave notes without actionable information

```typescript
// TODO: Fix this
// Bad - no context on WHAT needs fixing or HOW
```

❌ Duplicate information already in commit messages

```java
// AI-DEV-NOTE: Added error handling
// Bad - commit message already says this
```

### Do

✅ Provide specific, actionable context

```javascript
// AI-DEV-NOTE: Order validation must happen before inventory check
// to prevent race condition where items are reserved but invalid
```

✅ Explain the "why" not the "what"

```python
# AI-DEV-NOTE: Using binary search instead of linear search because
# the dataset can exceed 10k items (profiling showed 300ms avg latency)
```

✅ Include concrete next steps

```typescript
// TODO(ai/refactor): Extract duplicate validation into shared validator
// Files to update: api/users.ts, api/teams.ts, api/projects.ts
// Estimated effort: 1-2 hours
```

✅ Link to external context

```go
// AI-DEV-NOTE: Implements RFC 6749 OAuth 2.0 Authorization Framework
// https://tools.ietf.org/html/rfc6749#section-4.1
```

## Examples by Language

### TypeScript/JavaScript

```typescript
/**
 * AI-DEV-NOTE: This function uses a debounced approach to avoid
 * excessive API calls during rapid user input. The 300ms delay
 * was determined through user testing to balance responsiveness
 * with server load. See analytics dashboard for metrics.
 *
 * TODO(ai/performance): Consider implementing request cancellation
 * for in-flight requests when user continues typing. Currently
 * we rely on server-side deduplication which isn't ideal.
 */
export function searchUsers(query: string): Promise<User[]> {
  // Implementation...
}
```

### Python

```python
# AI-DEV-NOTE: This class implements the Repository pattern to
# abstract database access. All database operations should go
# through repository methods to maintain consistency and enable
# easier testing with mock repositories.
#
# DECISION: Using async/await throughout because:
# 1. Database I/O is inherently async
# 2. Allows concurrent operations for bulk updates
# 3. Prevents blocking the event loop in FastAPI
#
# Alternative (sync SQLAlchemy) was rejected because it would
# require running in thread pools which adds complexity.

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # TODO(ai/caching): Add Redis caching layer for frequently
    # accessed users (identified from logs: user profile views
    # account for 40% of DB queries). Estimated impact: 60% reduction
    # in database load. Blocked by: Redis infrastructure setup
    async def get_by_id(self, user_id: int) -> Optional[User]:
        # Implementation...
        pass
```

### Go

```go
// AI-DEV-NOTE: This middleware implements request tracing using
// OpenTelemetry. Each request gets a unique trace ID that flows
// through the entire request lifecycle, making debugging distributed
// systems much easier.
//
// CONTEXT: We chose OpenTelemetry over custom tracing because:
// - Industry standard with wide tool support
// - Compatible with Jaeger, Zipkin, and cloud providers
// - Lower maintenance burden than custom solution
//
// Configuration is in config/telemetry.yaml
func TracingMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        // AI-UNCERTAIN: The sampling rate (10%) might be too low
        // for debugging rare issues. Consider dynamic sampling
        // based on error rates or request patterns. Needs monitoring
        // data to make informed decision.

        // Implementation...
    }
}
```

### Rust

```rust
// AI-DEV-NOTE: This implementation uses unsafe code to achieve
// zero-copy parsing. The safety invariants are:
// 1. Input buffer must outlive all returned references
// 2. No mutable aliases can exist during parsing
// 3. UTF-8 validity is checked before transmutation
//
// SAFETY: These invariants are maintained because:
// - Buffer is borrowed for 'a lifetime (enforced by type system)
// - Parser is consumed during parsing (no mutable aliases possible)
// - from_utf8_unchecked is only called after validation
//
// TODO(ai/safety): Consider adding fuzzing tests to validate
// safety assumptions under malformed input. Current test coverage
// is good for valid input but edge cases might break invariants.
unsafe fn parse_str<'a>(buf: &'a [u8]) -> Result<&'a str, ParseError> {
    // Implementation...
}
```

## Integration with Development Workflow

### Pre-Commit Review

Before committing, AI should review notes:

1. Ensure all `AI-UNCERTAIN` notes have corresponding test coverage
2. Check that `TODO(ai/*)` notes have enough context for follow-up
3. Verify links to issues/PRs are valid
4. Remove or update outdated notes

### Note Extraction

Teams can extract AI notes for review:

```bash
# Find all AI development notes
grep -r "AI-DEV-NOTE" src/

# Find all AI TODOs
grep -r "TODO(ai/" src/

# Find uncertain areas needing review
grep -r "AI-UNCERTAIN" src/
```

### Note Analytics

Track note patterns to improve AI assistance:

- Density of `AI-UNCERTAIN` notes (indicates confidence)
- Categories of `TODO(ai/*)` notes (indicates common issues)
- Age of notes (indicates maintenance burden)

## Related Skills

- code-annotation-patterns
- documentation-linking

## Resources

- [AI-Powered Documentation: Make Your Codebase Self-Explanatory](https://dev.to/yysun/ai-powered-documentation-make-your-codebase-self-explanatory-231g)
- [Top 2025 AI Documentation Tools to Boost Developer Productivity](https://max-productive.ai/ai-tools/documentation/)
- [AI for Code Documentation: Essential Tips](https://codoid.com/ai/ai-for-code-documentation-essential-tips/)
