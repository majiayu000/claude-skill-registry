---
name: review-verification-protocol
description: Mandatory verification steps for all code reviews to reduce false positives. Load this skill before reporting ANY code review findings.
user-invocable: false
---

# Review Verification Protocol

This protocol MUST be followed before reporting any code review finding. Skipping these steps leads to false positives that waste developer time and erode trust in reviews.

## Hard gates (sequenced)

Run these **in order**. Do not move to the next gate until its **pass** condition is met (objective evidence, not internal certainty).

1. **Read** — Open the file and read the **full** enclosing function, method, property, or type (not only the diff hunk).  
   **Pass:** You can name the symbol and cite at least one line **outside** the changed lines that shows control flow, scope, or use relevant to the finding.

2. **Reference** (required before any “unused”, “dead code”, or “never called” claim) — Search the workspace for the identifier and for imports/`@objc`/`#selector`/SPM symbols that could reference it.  
   **Pass:** Recorded outcome: match count or list, or explicit “zero matches in repo” *before* asserting unused.

3. **Upstream** (required before “missing validation” or “missing error handling”) — Inspect the immediate caller, parent `View` / coordinator / `ViewModel`, app or scene delegate pipeline, or documented framework behavior that might already enforce the rule.  
   **Pass:** One sentence naming where responsibility lives, or “checked caller + framework path; still missing” with which layer you checked.

4. **Severity** — Before assigning Critical or Major, map the issue to [Severity Calibration](#severity-calibration) and exclude style-only or [Informational](#informational-no-action-required) items.  
   **Pass:** Chosen label matches a bullet under that severity; otherwise downgrade, reclassify as Informational, or omit.

5. **Submit** — Each retained finding uses `[FILE:LINE]` plus a one-line proof; complete [Before Submitting Review](#before-submitting-review) steps 1–7 for this review.  
   **Pass:** Every step satisfied or the finding was removed or downgraded.

The checklist below expands these gates by issue type; use both.

## Pre-Report Verification Checklist

Before flagging ANY issue, verify:

- [ ] **I read the actual code** - Not just the diff context, but the full function/class
- [ ] **I searched for usages** - Before claiming "unused", searched all references
- [ ] **I checked surrounding code** - The issue may be handled elsewhere (guards, earlier checks)
- [ ] **I verified syntax against current docs** - Apple APIs evolve (Swift concurrency, SwiftUI lifecycle, new SDKs); when syntax may have changed, confirm against current Apple documentation
- [ ] **I distinguished "wrong" from "different style"** - Both approaches may be valid
- [ ] **I considered intentional design** - Checked comments, CLAUDE.md, architectural context

## Verification by Issue Type

### "Unused Variable/Function"

**Before flagging**, you MUST:
1. Search for ALL references in the codebase (grep/ripgrep or IDE references)
2. Check if it's `public`/`open` and used by other modules or targets (SPM, app extensions)
3. Check if it's used via Objective-C runtime, `#selector`, key paths, or dynamic dispatch
4. Verify it's not a delegate/callback the framework invokes by contract

**Common false positives:**
- SwiftUI state (`@State`, `@Binding`, `@Observable`) that drives updates even when the binding looks “unused” in one branch
- Symbols referenced from Interface Builder, asset catalogs, `#Preview`, tests, or other targets
- `@objc`, `#selector`, or dynamic dispatch to a symbol search may not show as plain call sites

### "Missing Validation/Error Handling"

**Before flagging**, you MUST:
1. Check if validation exists at a higher level (caller, parent `ViewModel`, coordinator, app/scene delegate)
2. Check if the framework or type already enforces invariants (`Codable`, property wrappers, `URLSession` APIs)
3. Verify the "missing" check isn't present in a different form (e.g. `Result`, async error path, user-facing alert elsewhere)

**Common false positives:**
- Parent or router validates before this layer runs
- Errors surface via delegate, Combine pipeline, or unified logging — not every call needs local `do/catch`
- User-visible failure is handled in a single choke point (e.g. one alert coordinator)

### "Type Assertion/Unsafe Cast"

**Before flagging**, you MUST:
1. Confirm it's actually an assertion, not an annotation
2. Check if the type is narrowed by runtime checks before the point
3. Verify if framework or prior step guarantees the type (parsed JSON, Core Data fetch, async loader result)

**Valid patterns often flagged incorrectly:**
```swift
// Type annotation, NOT forced unwrap
let data: UserData = await loader()

// Type narrowing makes this safe
if let user = data as? User {
  user.name  // Swift knows this is User
}
```

### "Potential Memory Leak/Race Condition"

**Before flagging**, you MUST:
1. Verify cleanup is actually missing (not `deinit`, `onDisappear`, `cancel()`, or `store` teardown elsewhere)
2. Check if `Task` cancellation, `AsyncSequence` termination, or Combine subscription disposal is handled after awaits
3. Confirm the view or object can actually deallocate or invalidate during the async operation

**Common false positives:**
- `[weak self]` or `[unowned self]` already used where needed
- `Task` is cancelled when the view disappears (reviewer missed the link)
- Operation finishes before lifetime issues are possible

### "Performance Issue"

**Before flagging**, you MUST:
1. Confirm the code runs frequently enough to matter (SwiftUI body / layout vs one-off action)
2. Verify the optimization would have measurable impact (Instruments or clear hot path)
3. Check if the framework already mitigates this (SwiftUI diffing, lazy containers, `@Observable` granularity)

**Do NOT flag:**
- Allocations in infrequent actions (sheet presentation, button tap)
- Linear work on small collections without evidence of scale
- Short-lived value types in event handlers when profiling doesn’t justify change

## Severity Calibration

### Critical (Block Merge)

**ONLY use for:**
- Security vulnerabilities (injection, auth bypass, data exposure)
- Data corruption bugs
- Crash-causing bugs in happy path
- Breaking changes to public APIs

### Major (Should Fix)

**Use for:**
- Logic bugs that affect functionality
- Missing error handling that causes poor UX
- Performance issues with measurable impact
- Accessibility violations

### Minor (Consider Fixing)

**Use for:**
- Code clarity improvements
- Documentation gaps
- Inconsistent style (within reason)
- Non-critical test coverage gaps

### Informational (No Action Required)

**Use for:**
- Improvements that require adding new dependencies or modules
- Suggestions for net-new code that didn't exist in the codebase before (new modules, test suites, abstractions)
- Architectural ideas for future consideration
- Test infrastructure suggestions (new mock libraries, behaviour extraction)
- Optimizations without measurable impact in the current context

**These are NOT review blockers.** They should be noted for the author's awareness but must not appear in the actionable issue count. The Verdict should ignore informational items entirely.

### Do NOT Flag At All

- Style preferences where both approaches are valid
- Optimizations with no measurable benefit
- Test code not meeting production standards (intentionally simpler)
- Library/framework internal code (generated Swift, SPM vendored sources, Xcode-generated)
- Hypothetical issues that require unlikely conditions

## Valid Patterns (Do NOT Flag)

### Swift

| Pattern | Why It's Valid |
|---------|----------------|
| `guard let` early return | Standard Swift pattern for unwrapping, not excessive nesting |
| `weak self` in closures | Required for breaking retain cycles, not unnecessary |
| `@State` / `@Binding` property wrappers | SwiftUI state management primitives |
| Optional chaining (`foo?.bar?.baz`) | Safe access pattern, not error suppression |
| `as?` conditional cast | Safer than force cast, correct for type narrowing |

### SwiftUI

| Pattern | Why It's Valid |
|---------|----------------|
| `@StateObject` in parent, `@ObservedObject` in child | Correct ownership pattern |
| View body computed property without caching | SwiftUI manages re-rendering efficiently |
| `AnyView` for heterogeneous lists | Valid when `@ViewBuilder` or generics aren't practical |
| `EnvironmentObject` injection | Standard SwiftUI dependency injection |
| `PreferenceKey` for child-to-parent data | Correct alternative to callbacks for layout data |

### Testing

| Pattern | Why It's Valid |
|---------|----------------|
| `XCTAssertEqual` without custom message | Default messages are often sufficient |
| `async let` in test methods | Valid for concurrent test setup |
| `@MainActor` test classes | Required when testing UI-bound code |
| Mock objects without protocol conformance | Simple test doubles are acceptable |

### General

| Pattern | Why It's Valid |
|---------|----------------|
| `+?` lazy quantifier in regex | Prevents over-matching, correct for many patterns |
| Direct string concatenation | Simpler than template literals for simple cases |
| Multiple returns in function | Can improve readability |
| Comments explaining "why" | Better than no comments |

## Context-Sensitive Rules

### Swift Optionals

Flag force unwrap (`!`) **ONLY IF ALL** of these are true:
- [ ] Value CAN actually be nil at runtime
- [ ] No prior `guard let` or `if let` protects the access
- [ ] Not in test code or prototype
- [ ] Not a `@IBOutlet` (which is conventionally force-unwrapped)

### View Body Complexity

Flag complex View body **ONLY IF**:
- [ ] Body exceeds 40 lines
- [ ] Nested components could be extracted without losing clarity
- [ ] Performance profiling shows actual rendering issues
- [ ] Not a leaf view with minimal composition

### Error Handling

Flag missing `do/catch` **ONLY IF**:
- [ ] No `Result` type wraps the throwing call
- [ ] No higher-level error handler catches this
- [ ] The error would cause a crash, not just a failed operation
- [ ] User needs specific feedback for this error type

## Before Submitting Review

Final verification:
1. Re-read each finding and ask: "Did I verify this is actually an issue?"
2. For each finding, can you point to the specific line that proves the issue exists?
3. Would a domain expert agree this is a problem, or is it a style preference?
4. Does fixing this provide real value, or is it busywork?
5. Format every finding as: `[FILE:LINE] ISSUE_TITLE`
6. For each finding, ask: "Does this fix existing code, or does it request entirely new code that didn't exist before?" If the latter, downgrade to Informational.
7. If this is a re-review: ONLY verify previous fixes. Do not introduce new findings.

If uncertain about any finding, either:
- Remove it from the review
- Mark it as a question rather than an issue
- Verify by reading more code context
