---
description: Comprehensive iOS/SwiftUI code review with optional parallel agents
name: review-ios
disable-model-invocation: true
---

# iOS Code Review

## Arguments

- `--parallel`: Spawn specialized subagents per technology area
- Path: Target directory (default: current working directory)

## Hard gates

Complete in order before writing **Issues** in the output (empty scope is allowed; fabricated findings are not).

1. **Scope gate:** You have an explicit list of `.swift` paths under review (from Step 1 or a user-provided path). **Pass:** List captured in working notes **or** one line: `No Swift files in scope` — then stop with no Issues.
2. **Linter gate (style):** Step 2 commands ran for this tree; if no `.swiftlint.yml` / `.swiftlint.yaml`, note that in one line. **Pass:** You do not report a style issue that SwiftLint would already enforce for that line when config exists and `swiftlint` succeeds.
3. **Protocol gate:** `beagle-ios:review-verification-protocol` is loaded before Step 6. **Pass:** If you report any Issues, at least one finding was checked against that checklist (name the item in Review Summary or on that Issue); if you report zero Issues, state `Protocol applied; no issues` in Review Summary.
4. **Evidence gate (Critical/Major):** For each Critical or Major item, you re-read the file at `FILE:LINE` (full surrounding context, not only the diff hunk). **Pass:** The Issue text matches observable code at that location.

Do not begin Step 6 until **Gates 1–3** are satisfied (skills load order stays Steps 4–5).

## Step 1: Identify Changed Files

```bash
git diff --name-only $(git merge-base HEAD main)..HEAD | grep -E '\.swift$'
```

## Step 2: Verify Linter Status

**CRITICAL**: Run SwiftLint BEFORE flagging any style issues.

```bash
# Check if SwiftLint config exists and run it
if [ -f ".swiftlint.yml" ] || [ -f ".swiftlint.yaml" ]; then
    swiftlint lint --quiet <changed_files>
fi
```

**Rules:**
- If SwiftLint passes for a specific rule, DO NOT flag that issue manually
- SwiftLint configuration is authoritative for style rules
- Only flag issues that linters cannot detect (semantic issues, architectural problems)

## Step 3: Detect Technologies

```bash
# SwiftUI (always with swift files that import it)
grep -r "import SwiftUI" --include="*.swift" -l | head -3

# SwiftData
grep -r "import SwiftData\|@Model\|@Query" --include="*.swift" -l | head -3

# Swift Testing
grep -r "import Testing\|@Test\|#expect" --include="*.swift" -l | head -3

# Combine
grep -r "import Combine\|AnyPublisher\|@Published" --include="*.swift" -l | head -3

# URLSession (explicit async patterns)
grep -r "URLSession\.shared\|\.data(from:\|\.download(from:" --include="*.swift" -l | head -3

# CloudKit
grep -r "import CloudKit\|CKContainer\|CKRecord" --include="*.swift" -l | head -3

# WidgetKit
grep -r "import WidgetKit\|TimelineProvider\|WidgetFamily" --include="*.swift" -l | head -3

# App Intents
grep -r "import AppIntents\|@AppIntent\|AppEntity" --include="*.swift" -l | head -3

# HealthKit
grep -r "import HealthKit\|HKHealthStore\|HKQuery" --include="*.swift" -l | head -3

# WatchKit
grep -r "import WatchKit\|WKExtension\|WKInterfaceController" --include="*.swift" -l | head -3

# Animations (beyond basic withAnimation)
grep -r "PhaseAnimator\|KeyframeAnimator\|matchedGeometryEffect\|navigationTransition\|scrollTransition\|CABasicAnimation\|CASpringAnimation\|CAKeyframeAnimation\|UIViewPropertyAnimator\|UIDynamicAnimator\|\.symbolEffect\|\.contentTransition\|CustomAnimation\|MeshGradient" --include="*.swift" -l | head -3
```

## Step 4: Load Verification Protocol

Load `beagle-ios:review-verification-protocol` skill and keep its checklist in mind throughout the review.

## Step 5: Load Skills

Use the `Skill` tool to load each applicable skill (e.g., `Skill(skill: "beagle-ios:swift-code-review")`).

**Always load:**
- `beagle-ios:swift-code-review`
- `beagle-ios:swiftui-code-review`

**Conditionally load based on detection:**

| Condition | Skill |
|-----------|-------|
| SwiftData detected | `beagle-ios:swiftdata-code-review` |
| Swift Testing detected | `beagle-ios:swift-testing-code-review` |
| Combine detected | `beagle-ios:combine-code-review` |
| URLSession detected | `beagle-ios:urlsession-code-review` |
| CloudKit detected | `beagle-ios:cloudkit-code-review` |
| WidgetKit detected | `beagle-ios:widgetkit-code-review` |
| App Intents detected | `beagle-ios:app-intents-code-review` |
| HealthKit detected | `beagle-ios:healthkit-code-review` |
| WatchKit detected | `beagle-ios:watchos-code-review` |
| Animation code detected | `beagle-ios:ios-animation-code-review` |

## Step 6: Review

**Sequential (default):**
1. Load applicable skills
2. Review Swift quality issues first (concurrency, memory, error handling)
3. Review SwiftUI patterns (view composition, state management, accessibility)
4. Review detected technology areas
5. Consolidate findings

**Parallel (--parallel flag):**
1. Detect all technologies upfront
2. Spawn one subagent per technology area with `Task` tool
3. Each agent loads its skill and reviews its domain
4. Wait for all agents
5. Consolidate findings

### Before Flagging Issues

1. **Check SwiftLint output** - don't duplicate linter findings
2. **Check code comments** for intentional patterns (// MARK:, // NOTE:, etc.)
3. **Consider Apple framework idioms** - what looks wrong generically may be correct for the framework
4. **Trace async code paths** before claiming missing error handling or race conditions

## Step 7: Verify Findings

Before reporting any issue:
1. Re-read the actual code (not just diff context)
2. For "unused" claims - did you search all references?
3. For "missing" claims - did you check framework/parent handling?
4. For syntax issues - did you verify against current version docs?
5. Remove any findings that are style preferences, not actual issues

## Step 8: Review Convergence

### Single-Pass Completeness

You MUST report ALL issues across ALL categories (style, logic, types, tests, security, performance) in a single review pass. Do not hold back issues for later rounds.

Before submitting findings, ask yourself:
- "If all my recommended fixes are applied, will I find NEW issues in the fixed code?"
- "Am I requesting new code (tests, types, modules) that will itself need review?"

If yes to either: include those anticipated downstream issues NOW, in this review, so the author can address everything at once.

### Scope Rules

- Review ONLY the code in the diff and directly related existing code
- Do NOT request new features, test infrastructure, or architectural changes that didn't exist before the diff
- If test coverage is missing, flag it as ONE Minor issue ("Missing test coverage for X, Y, Z") — do NOT specify implementation details like mock libraries, behaviour extraction, or dependency injection patterns that would introduce substantial new code
- Typespecs, documentation, and naming issues are Minor unless they affect public API contracts
- Do NOT request adding new dependencies (e.g. Mox, testing libraries, linter plugins)

### Fix Complexity Budget

Fixes to existing code should be flagged at their real severity regardless of size.

However, requests for **net-new code that didn't exist before the diff** must be classified as Informational:
- Adding a new dependency (e.g. Mox, a linter plugin)
- Creating entirely new modules, files, or test suites
- Extracting new behaviours, protocols, or abstractions

These are improvement suggestions for the author to consider in future work, not review blockers.

### Iteration Policy

If this is a re-review after fixes were applied:
- ONLY verify that previously flagged issues were addressed correctly
- Do NOT introduce new findings unrelated to the previous review's issues
- Accept Minor/Nice-to-Have issues that weren't fixed — do not re-flag them
- The goal of re-review is VERIFICATION, not discovery

## Output Format

```markdown
## Review Summary

[1-2 sentence overview of findings]

## Issues

### Critical (Blocking)

1. [FILE:LINE] ISSUE_TITLE
   - Issue: Description of what's wrong
   - Why: Why this matters (crash, data loss, security, race condition)
   - Fix: Specific recommended fix

### Major (Should Fix)

2. [FILE:LINE] ISSUE_TITLE
   - Issue: ...
   - Why: ...
   - Fix: ...

### Minor (Nice to Have)

N. [FILE:LINE] ISSUE_TITLE
   - Issue: ...
   - Why: ...
   - Fix: ...

### Informational (For Awareness)

N. [FILE:LINE] SUGGESTION_TITLE
   - Suggestion: ...
   - Rationale: ...

## Good Patterns

- [FILE:LINE] Pattern description (preserve this)

## Verdict

Ready: Yes | No | With fixes 1-N (Critical/Major only; Minor items are acceptable)
Rationale: [1-2 sentences]
```

## Post-Fix Verification

After fixes are applied, run:

```bash
# Swift build and lint
swift build
swiftlint lint --quiet

# Run tests if present
swift test
```

All checks must pass before approval.

## Rules

- Load skills BEFORE reviewing (not after)
- Number every issue sequentially (1, 2, 3...)
- Include FILE:LINE for each issue
- Separate Issue/Why/Fix clearly
- Categorize by actual severity
- Check for Swift 6 strict concurrency issues
- Run verification after fixes
- Report ALL issues in a single pass — do not hold back findings for later iterations
- Re-reviews verify previous fixes ONLY — no new discovery
- Requests for net-new code (new modules, dependencies, test suites) are Informational, not blocking
- The Verdict ignores Minor and Informational items — only Critical and Major block approval
