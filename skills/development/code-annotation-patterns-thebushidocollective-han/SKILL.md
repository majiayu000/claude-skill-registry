---
name: code-annotation-patterns
description: Use when annotating code with structured metadata, tags, and markers for AI-assisted development workflows. Covers annotation formats, semantic tags, and integration with development tools.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Code Annotation Patterns for AI Development

Advanced patterns for annotating code with structured metadata that supports AI-assisted development workflows.

## Annotation Categories

### Technical Debt Markers

Structured annotations for tracking technical debt:

```typescript
/**
 * @ai-tech-debt
 * @category: Architecture
 * @severity: High
 * @effort: 2-3 days
 * @impact: Maintainability, Performance
 *
 * This service class has grown to 1500+ lines and violates Single
 * Responsibility Principle. Should be split into:
 * - UserAuthService (authentication logic)
 * - UserProfileService (profile management)
 * - UserPreferencesService (settings/preferences)
 *
 * Blocking new features: User role management (#234), SSO integration (#245)
 */
class UserService {
  // Implementation...
}
```

**Severity levels:**

- `Critical`: Security vulnerabilities, data loss risks
- `High`: Significant maintainability or performance issues
- `Medium`: Code quality concerns, testing gaps
- `Low`: Minor improvements, nice-to-haves

### Security Annotations

```python
# @ai-security
# @risk-level: High
# @cwe: CWE-89 (SQL Injection)
# @mitigation: Use parameterized queries
#
# SECURITY WARNING: This function constructs SQL queries dynamically.
# Although input is validated, parameterized queries would be safer.
# Current validation regex: ^[a-zA-Z0-9_]+$
# TODO(ai/security): Migrate to SQLAlchemy ORM or use parameterized queries

def get_user_by_username(username: str):
    # Current implementation with string formatting
    query = f"SELECT * FROM users WHERE username = '{username}'"
```

### Performance Annotations

```java
/**
 * @ai-performance
 * @complexity: O(n²)
 * @bottleneck: true
 * @profiling-data: 45% of request time when n > 100
 * @optimization-target: O(n log n) or better
 *
 * This nested loop is the primary performance bottleneck for large
 * datasets. Profiling shows:
 * - n=10: 5ms avg
 * - n=100: 120ms avg
 * - n=1000: 11s avg (unacceptable)
 *
 * Optimization approaches:
 * 1. Sort + binary search: O(n log n) - estimated 95% improvement
 * 2. Hash map: O(n) - best performance but higher memory usage
 * 3. Database-level optimization: Move logic to SQL query
 */
public List<Match> findMatches(List<Item> items) {
    // O(n²) implementation
}
```

### Accessibility Annotations

```typescript
/**
 * @ai-a11y
 * @wcag-level: AA
 * @compliance-status: Partial
 * @issues:
 *   - Missing ARIA labels for icon buttons
 *   - Insufficient color contrast (3.2:1, needs 4.5:1)
 *   - Keyboard navigation incomplete
 *
 * Component needs accessibility improvements to meet WCAG 2.1 Level AA.
 * Audit completed: 2025-12-04
 * Blocking: Public sector deployment (requires AA compliance)
 */
export function SearchBar() {
  // Implementation with partial a11y support
}
```

### Testing Annotations

```go
// @ai-testing
// @coverage: 45%
// @coverage-target: 80%
// @missing-tests:
//   - Edge case: nil pointer handling
//   - Edge case: Concurrent access scenarios
//   - Integration: Database transaction rollback
//
// Test coverage is below target. Priority areas:
// 1. Error handling paths (currently untested)
// 2. Concurrent access (identified race condition in PR review)
// 3. Database edge cases (transaction boundaries)

func ProcessOrder(order *Order) error {
    // Implementation with incomplete test coverage
}
```

## Semantic Tags

### Change Impact Tags

```typescript
/**
 * @ai-change-impact
 * @breaking-change: true
 * @affects:
 *   - API consumers (public method signature changed)
 *   - Database migrations (requires schema update)
 *   - Dependent services (contract modified)
 *
 * This change modifies the public API contract. Migration guide:
 * 1. Update API clients to use new parameter format
 * 2. Run migration script: ./scripts/migrate_v2_to_v3.sh
 * 3. Update environment variables (NEW_API_KEY required)
 *
 * Backward compatibility: Supported until v4.0.0 (2026-06-01)
 */
```

### Dependency Tags

```python
# @ai-dependency
# @external-service: PaymentAPI
# @failure-mode: graceful-degradation
# @fallback: offline-payment-queue
# @sla: 99.9% uptime
# @timeout: 5000ms
#
# This function depends on external payment service. Failure handling:
# - Timeout: Queue for retry, notify user of delayed processing
# - Service down: Queue for batch processing, store transaction locally
# - Invalid response: Log error, rollback transaction, notify monitoring
#
# Circuit breaker: Opens after 5 consecutive failures, half-open after 30s

async def process_payment(transaction: Transaction) -> PaymentResult:
    # Implementation with external service dependency
```

### Configuration Tags

```rust
/// @ai-config
/// @env-vars:
///   - DATABASE_URL (required)
///   - REDIS_URL (optional, falls back to in-memory cache)
///   - LOG_LEVEL (optional, default: "info")
/// @config-file: config/production.yaml
/// @secrets:
///   - API_SECRET_KEY (must be 32+ chars)
///   - JWT_PRIVATE_KEY (RSA 2048-bit minimum)
///
/// Configuration loading order:
/// 1. Environment variables (highest priority)
/// 2. config/{environment}.yaml files
/// 3. Default values (lowest priority)

pub struct AppConfig {
    // Configuration fields
}
```

## Annotation Formats

### Inline Annotations

For single-line or small context:

```javascript
// @ai-pattern: Singleton
// @ai-thread-safety: Not thread-safe, use in single-threaded context only
const cache = createCache();
```

### Block Annotations

For complex context:

```python
"""
@ai-pattern: Factory Pattern
@ai-creational-pattern: true
@ai-rationale:
  Factory pattern used here because:
  1. Need to support multiple database backends (PostgreSQL, MySQL, SQLite)
  2. Configuration determines which implementation to instantiate
  3. Allows easy addition of new backends without modifying client code

@ai-extensibility:
  To add new database backend:
  1. Implement DatabaseBackend interface
  2. Register in BACKEND_REGISTRY dict
  3. Add configuration mapping in config/database.yaml

Example usage in docs/database-backends.md
"""
class DatabaseFactory:
    # Implementation
```

### Structured Metadata

```typescript
/**
 * @ai-metadata {
 *   "pattern": "Observer",
 *   "subscribers": ["LoggingService", "MetricsService", "AuditService"],
 *   "event-types": ["user.created", "user.updated", "user.deleted"],
 *   "async": true,
 *   "guaranteed-delivery": false
 * }
 *
 * Event bus using observer pattern for loose coupling between services.
 * Events are published async with fire-and-forget semantics (no delivery guarantee).
 * For critical events requiring guaranteed delivery, use MessageQueue instead.
 */
class EventBus {
  // Implementation
}
```

## Language-Specific Patterns

### TypeScript/JavaScript

```typescript
/**
 * @ai-hook-usage
 * @react-hooks: [useState, useEffect, useCallback, useMemo]
 * @dependencies: {useCallback: [data, filter], useMemo: [data], useEffect: [id]}
 * @optimization: useMemo prevents expensive recalculation on re-renders
 *
 * This component uses React hooks for state and side effects. Dependency arrays
 * are carefully managed to prevent unnecessary re-renders and infinite loops.
 *
 * @ai-performance-note:
 * - useMemo caches filtered results (reduces filtering from O(n) per render to once per data change)
 * - useCallback memoizes event handlers (prevents child re-renders)
 */
export function DataTable({ data, id }: Props) {
  const [filter, setFilter] = useState('');

  const handleFilter = useCallback((value: string) => {
    setFilter(value);
  }, [data, filter]); // @ai-dependency-note: Both needed for closure

  const filteredData = useMemo(() => {
    return data.filter(item => item.name.includes(filter));
  }, [data]); // @ai-optimization: Only recompute when data changes

  // Implementation...
}
```

### Python

```python
# @ai-decorator-stack
# @decorators: [retry, cache, log_execution, validate_auth]
# @execution-order: validate_auth -> log_execution -> cache -> retry -> function
#
# Decorator execution order matters:
# 1. validate_auth: Must run first to prevent unauthorized cache hits
# 2. log_execution: Log after auth but before cache to track all attempts
# 3. cache: After logging to avoid logging cache hits
# 4. retry: Innermost to retry actual function, not auth/logging

@validate_auth(roles=["admin", "operator"])
@log_execution(level="INFO")
@cache(ttl=300, key_func=lambda args: f"user:{args[0]}")
@retry(max_attempts=3, backoff=exponential)
def get_user_profile(user_id: int) -> UserProfile:
    """
    @ai-caching-strategy: Time-based (TTL=300s)
    @ai-invalidation: Manual invalidation on user.updated event
    @ai-cache-key: user:{user_id}
    """
    # Implementation
```

### Go

```go
// @ai-concurrency
// @pattern: Worker Pool
// @workers: 10 (configurable via WORKER_POOL_SIZE)
// @channel-buffer: 100
// @backpressure-handling: Blocks when buffer full
//
// This implements a worker pool pattern for concurrent processing.
// Workers are started at server initialization and kept alive for
// the server lifetime (no dynamic scaling).
//
// @ai-monitoring:
//   - Metric: worker_pool_queue_depth (current channel buffer size)
//   - Metric: worker_pool_processing_time (histogram)
//   - Alert: Queue depth > 80 for >5min (add workers)

type WorkerPool struct {
    workers   int
    jobQueue  chan Job
    resultCh  chan Result
    // fields...
}
```

### Rust

```rust
/// @ai-lifetime-annotations
/// @lifetimes: ['a, 'b]
/// @invariants:
///   - 'a must outlive 'b (parser must live longer than input)
///   - Output references bound to 'a (safe as long as input lives)
///
/// Lifetime relationships:
/// - Parser<'a> borrows input for 'a
/// - Output<'a> contains references to input (bounded by 'a)
/// - Temporary allocations use 'b (scoped to parsing only)
///
/// @ai-safety:
/// These lifetime constraints prevent dangling references by ensuring
/// the input buffer outlives all references derived from it.

pub struct Parser<'a> {
    input: &'a str,
    // fields...
}
```

## Integration with Tools

### IDE Integration

Annotations can be extracted by IDE plugins:

```bash
# Extract all AI annotations
rg "@ai-\w+" --type ts --json | jq '.text'

# Find security-related annotations
rg "@ai-security" -A 10

# Find performance bottlenecks
rg "@bottleneck: true" --type java
```

### Static Analysis

Custom linters can enforce annotation standards:

```javascript
// Example: ESLint rule to enforce @ai-security on auth functions
module.exports = {
  rules: {
    'require-security-annotation': {
      create(context) {
        return {
          FunctionDeclaration(node) {
            if (node.id.name.includes('auth') || node.id.name.includes('Auth')) {
              // Check for @ai-security annotation
            }
          }
        };
      }
    }
  }
};
```

### Documentation Generation

Extract annotations to generate documentation:

```python
# doc_generator.py
import re
from pathlib import Path

def extract_ai_annotations(file_path):
    """Extract all @ai-* annotations from file"""
    with open(file_path) as f:
        content = f.read()

    pattern = r'@ai-(\w+):\s*(.+)'
    return re.findall(pattern, content)

# Generate markdown documentation from annotations
```

## Annotation Best Practices

### Consistency

Use consistent annotation formats across codebase:

```typescript
// ✅ GOOD - Consistent format
// @ai-pattern: Strategy
// @ai-alternatives: [Template Method, State Pattern]

// @ai-pattern: Observer
// @ai-alternatives: [Event Emitter, Pub/Sub]

// ❌ BAD - Inconsistent format
// @ai-pattern: Strategy (alternatives: Template Method, State)
// Pattern: Observer | Alternatives: Event Emitter, Pub/Sub
```

### Completeness

Include all relevant metadata:

```python
# ✅ GOOD - Complete context
# @ai-security
# @risk-level: High
# @cwe: CWE-79 (XSS)
# @input-sanitization: HTML encoding applied
# @output-encoding: UTF-8
# @tested: XSS test suite in tests/security/xss_test.py

# ❌ BAD - Incomplete
# @ai-security
# Security risk here
```

### Maintainability

Keep annotations up-to-date:

```go
// ✅ GOOD - Dated and tracked
// @ai-tech-debt
// @added: 2025-12-04
// @reviewed: 2025-12-04
// @next-review: 2026-01-04

// ❌ BAD - Stale and outdated
// @ai-tech-debt
// TODO: Fix this eventually
```

## Anti-Patterns

### Don't

❌ Over-annotate obvious code

```javascript
// @ai-pattern: Variable Declaration
const user = getUser(); // Bad - obvious
```

❌ Use annotations instead of fixing code

```python
# @ai-tech-debt: This is terrible code
# @ai-security: Has vulnerabilities
# @ai-performance: Slow
# Bad - just fix the code!
```

❌ Inconsistent tag naming

```typescript
// @AI-PATTERN vs @ai-pattern vs @aiPattern
// Use consistent naming
```

### Do

✅ Annotate complex or non-obvious patterns

```rust
/// @ai-pattern: Typestate
/// @ai-compile-time-safety: true
///
/// Uses typestate pattern to enforce protocol state machine at compile time.
/// Impossible states are unrepresentable in type system.
```

✅ Provide actionable information

```java
/**
 * @ai-tech-debt
 * @action: Extract UserValidator class
 * @files-affected: [UserService.java, UserController.java, UserTest.java]
 * @effort: 3-4 hours
 * @priority: Medium
 */
```

✅ Link to external resources

```python
# @ai-algorithm: Dijkstra's shortest path
# @reference: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
# @paper: "A Note on Two Problems in Connexion with Graphs" (1959)
# @optimization: Using binary heap for O((V+E) log V) complexity
```

## Related Skills

- notetaker-fundamentals
- documentation-linking

## Resources

- [Chapter 14 Annotating Your Code | AI for Efficient Programming](https://hutchdatascience.org/AI_for_Efficient_Programming/annotating-your-code.html)
- [FREE AI Code Comment Generator - Enhance Code Clarity](https://workik.com/code-comment-generator)
- [GitLoop - AI Codebase Assistant](https://www.gitloop.com/)
