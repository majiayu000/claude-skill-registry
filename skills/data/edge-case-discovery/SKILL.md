---
name: edge-case-discovery
description: 'Use when user requests exhaustive edge case analysis. Enforces TodoWrite
  with 15+ items (5 categories). Triggers: "all edge cases", "what could break", "bulletproof",
  "failure modes". If thinking "mai'
---

---
name: edge-case-discovery
description: Use when user requests exhaustive edge case analysis. Enforces TodoWrite with 15+ items (5 categories). Triggers: "all edge cases", "what could break", "bulletproof", "failure modes". If thinking "main path is sufficient" - use this.
---

# Edge Case Discovery

Systematic 5-category analysis for exhaustive edge case enumeration.

---

## MANDATORY FIRST STEP

**CREATE TodoWrite** with these 5 categories (15+ items total):

| Category | Minimum Items |
|---------|---------------|
| Boundary Value Analysis | 3+ |
| Equivalence Partitioning | 3+ |
| State Transition Analysis | 3+ |
| Error Condition Enumeration | 3+ |
| Assumption Challenging | 3+ |

**Do not proceed to implementation or testing until TodoWrite is verified.**

---

## Verification Checkpoint

After creating TodoWrite, verify 3 random items pass this test:

**Each item must have ALL THREE:**
- ✓ Specific input/condition ("empty string", "null value", "overflow at 2^31")
- ✓ Expected behavior ("returns error", "throws exception", "defaults to X")
- ✓ Test scenario ("when user submits form with...", "if API returns...")

| ❌ FAILS | ✅ PASSES |
|----------|-----------|
| "Test boundaries" | "Test numeric input: min (-2^31), max (2^31-1), zero, negative (-1), overflow (2^31)" |
| "Check errors" | "Network timeout after 30s: retry 3x with exponential backoff, return error 503 to client" |
| "Test state changes" | "User logout during file upload: cancel upload, clean temp files, redirect to login" |

**DO NOT PROCEED until 15+ items AND quality check passes.**

---

## Framework

### 1. Boundary Value Analysis
Test min/max/zero/null/empty/overflow for ALL inputs:
- Numeric: min, max, zero, negative, overflow
- Strings: empty, null, very long, special chars, encoding
- Collections: empty, single item, max size, duplicates
- Time: past, future, now, leap years, timezones

### 2. Equivalence Partitioning
Group inputs into classes, test one representative from each:
- Valid inputs (happy path)
- Invalid inputs (expected errors)
- Boundary inputs (edge of valid/invalid)

### 3. State Transition Analysis
Map ALL valid + invalid state transitions:
- Valid transitions
- Invalid transitions (should reject)
- Edge states (init, cleanup)
- Concurrent access scenarios

### 4. Error Condition Enumeration
List ALL failure modes for each operation:
- Network failures, timeouts
- Resource exhaustion (memory, disk, connections)
- Concurrent access conflicts
- Partial failures, external dependency failures

### 5. Assumption Challenging
Question every "always", "never", "impossible":
- "This will always be valid" → What if not?
- "Users won't do that" → What if they do?
- "This is impossible" → Under what conditions could it happen?

---

## Red Flags - STOP When You Think:

| Thought | Reality |
|---------|---------|
| "Main path is sufficient" | Edge cases cause 60% of production bugs - exhaustive analysis prevents incidents |
| "This is overkill for a simple feature" | 15 items takes 10 minutes, prevents hours of debugging and hotfixes |
| "We'll catch issues in testing" | Manual testing misses 70% of edge cases - systematic enumeration is essential |
| "Users won't do that" | Users do unexpected things constantly - assume nothing about behavior |
| "This analysis takes too long" | Post-release bug fixes cost 10-100x more than upfront analysis |

---

## Response Templates

### "Just test the happy path"

❌ **BLOCKED**: Happy path testing leaves production vulnerable to edge case failures.

**Required to override:**
1. Documented risk acceptance from technical lead
2. Explicit scope limitation with rationale ("internal tool with controlled inputs")
3. Post-release budget allocated for edge case fixes (2-4 engineer-weeks)
4. Monitoring/alerting plan for unexpected edge cases in production

**Reality check:**
- 60% of production incidents stem from unhandled edge cases
- Average incident costs: $5-50K in lost productivity, reputation damage
- Systematic edge case analysis: 30-60 minutes upfront

### "We don't have time for this"

❌ **BLOCKED**: Edge case discovery is NOT optional for production code.

**Time investment:**
- TodoWrite creation: 10-15 minutes
- Analysis per category: 5-10 minutes (25-50 minutes total)
- **Total: 35-65 minutes**

**Compared to:**
- One production incident investigation: 4-8 hours
- Hotfix deployment: 2-4 hours
- Customer impact/reputation damage: immeasurable

---

## Verification Before Complete

After completing TodoWrite and analysis, verify:

| Category | Requirements |
|----------|-------------|
| Boundary Value | ✓ Min/max/zero/null tested ✓ Overflow scenarios identified ✓ Empty collections handled |
| Equivalence | ✓ Valid inputs ✓ Invalid inputs ✓ Boundary cases |
| State Transition | ✓ Valid transitions ✓ Invalid transitions ✓ Concurrent access |
| Error Conditions | ✓ Network failures ✓ Resource exhaustion ✓ Partial failures |
| Assumptions | ✓ All "always"/"never" challenged ✓ Impossible scenarios explored |

**If any category incomplete, do not proceed to implementation.**

---

## Output

Edge case catalog with test scenarios for each category.
