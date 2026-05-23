---
name: code-comments
description: Write clear, plain-spoken code comments and documentation that lives alongside the code. Use when writing or reviewing code that needs inline documentation—file headers, function docs, architectural decisions, or explanatory comments. Optimized for both human readers and AI coding assistants who benefit from co-located context.
---

# Code Comments

Write documentation that lives with the code it describes. Plain language. No jargon. Explain the *why*, not the *what*.

## Core Philosophy

**Co-location wins.** Documentation in separate files drifts out of sync. Comments next to code stay accurate because they're updated together.

**Write for three audiences:**
1. Future you, six months from now
2. Teammates reading unfamiliar code
3. AI assistants (Claude, Copilot) who see one file at a time

**The "why" test:** Before writing a comment, ask: "Does this explain *why* this code exists or *why* it works this way?" If it only restates *what* the code does, skip it.

## Documentation Levels

### File Headers

Every file should open with a brief explanation of its purpose and how it fits into the larger system.

```typescript
// UserAuthContext.tsx
//
// Manages authentication state across the app. Wraps the root component
// to provide login status, user info, and auth methods to any child.
//
// Why a context instead of Redux: Auth state is read-heavy and rarely
// changes mid-session. Context avoids the ceremony of actions/reducers
// for something this simple.
```

```swift
// NetworkRetryPolicy.swift
//
// Handles automatic retry logic for failed network requests.
// Uses exponential backoff with jitter to avoid thundering herd
// when the server comes back online after an outage.
//
// Used by: APIClient, BackgroundSyncManager
// See also: NetworkError.swift for error classification
```

**Include:**
- What this file/module is responsible for
- Why it exists (if not obvious from the name)
- Key relationships to other parts of the codebase
- Any non-obvious design decisions

### Function & Method Documentation

Document the contract, not the implementation.

```typescript
/**
 * Calculates shipping cost based on weight and destination.
 *
 * Uses tiered pricing: under 1lb ships flat rate, 1-5lb uses
 * regional rates, over 5lb triggers freight calculation.
 *
 * Returns $0 for destinations we don't ship to rather than
 * throwing—caller should check `canShipTo()` first if they
 * need to distinguish "free shipping" from "can't ship."
 */
function calculateShipping(weightLbs: number, zipCode: string): number
```

```python
def sync_user_preferences(user_id: str, prefs: dict) -> SyncResult:
    """
    Pushes local preference changes to the server and pulls remote changes.

    Conflict resolution: server wins for security settings, local wins
    for UI preferences. See PREFERENCES.md for the full conflict matrix.

    Called automatically on app foreground. Can also be triggered manually
    from Settings > Sync Now.
    """
```

**Include:**
- What the function accomplishes (not how)
- Non-obvious parameter constraints or edge cases
- What the return value means, especially for ambiguous cases
- Side effects (network calls, file writes, state mutations)

**Skip for:** Simple getters, obvious one-liners, private helpers with descriptive names.

### Inline Comments

Use sparingly. When you need them, explain the reasoning.

```typescript
// Debounce search by 300ms to avoid hammering the API on every keystroke.
// 300ms feels responsive while cutting API calls by ~80% in user testing.
const debouncedSearch = useMemo(
  () => debounce(executeSearch, 300),
  [executeSearch]
);
```

```swift
// Force unwrap is safe here—viewDidLoad guarantees the storyboard
// connected this outlet. If it's nil, we want to crash immediately
// rather than fail silently later.
let tableView = tableView!
```

```python
# Process oldest items first. Newer items are more likely to be
# modified again, so processing them last reduces wasted work.
queue.sort(key=lambda x: x.created_at)
```

### Architectural Comments

For code that embodies important design decisions, explain the tradeoffs.

```typescript
// ARCHITECTURE NOTE: Event Sourcing for Cart
//
// Cart state is rebuilt from events (add, remove, update quantity)
// rather than stored directly. This lets us:
// - Show complete cart history to users
// - Replay events for debugging
// - Retroactively apply promotions to past actions
//
// Tradeoff: Reading current cart state requires replaying all events.
// We cache the computed state in Redis with 5min TTL to keep reads fast.
// Cache invalidation happens in CartEventHandler.
```

```swift
// WHY COORDINATOR PATTERN
//
// Navigation logic lives here instead of in view controllers because:
// 1. VCs don't need to know about each other (loose coupling)
// 2. Deep linking becomes straightforward—just call coordinator methods
// 3. Navigation is testable without instantiating UI
//
// The tradeoff is more files and indirection. Worth it for apps with
// 10+ screens; overkill for simple apps.
```

### TODO Comments

Make them actionable and traceable.

```typescript
// TODO(pete): Extract to shared util once mobile team needs this too.
// Blocked on: Mobile API parity (see MOBILE-123)

// HACK: Workaround for Safari flexbox bug. Remove after dropping Safari 14.
// Bug report: https://bugs.webkit.org/show_bug.cgi?id=XXXXX

// FIXME: Race condition when user rapidly toggles. Need to cancel
// in-flight requests. Reproduced in issue #892.
```

## Language-Specific Patterns

See [references/language-examples.md](references/language-examples.md) for detailed examples in:
- TypeScript/JavaScript (JSDoc, TSDoc patterns)
- Swift (documentation comments, MARK pragmas)
- Python (docstrings, type hint documentation)
- React/Next.js (component documentation patterns)

## Writing Style

**Plain language.** Write like you're explaining to a smart colleague who doesn't have context.

**Active voice.** "This function validates..." not "Validation is performed..."

**Be specific.** "Retries 3 times with 1s backoff" not "Handles retries."

**Skip the obvious.** If the code says `user.isAdmin`, don't comment "checks if user is admin."

**Date things that expire.** Workarounds, version-specific code, and temporary solutions should note when they can be removed.

**Reference constants, don't duplicate values.** When a behavior is controlled by a constant, reference it by name—don't restate its value in the comment.

```rust
// Bad: duplicates the value, will drift when constant changes
/// Returns true if stale (not updated in last 5 minutes)
pub fn is_stale(&self) -> bool { ... }

// Good: references the constant
/// Returns true if stale (not updated within [`STALE_THRESHOLD_SECS`])
pub fn is_stale(&self) -> bool { ... }
```

Unit translations for magic numbers are fine (`1048576 // 1MB`) since they add clarity, not duplication.
