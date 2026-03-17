---
name: beta-test-cycles
description: This skill should be used when the user asks to "run beta test cycle", "run next cycle", "test static patterns", "analyze test failures", "improve pass rate", or wants to systematically improve command generation quality through iterative testing and pattern refinement. Provides structured workflow for running test cycles, analyzing failures, implementing fixes, and documenting results.
version: 1.0.0
---

# Beta Test Cycles Skill

## What This Skill Does

This skill provides a systematic workflow for improving static pattern matchers through iterative test cycles. Use this approach to:
- Analyze test failures by root cause
- Fix patterns through strategic reordering and refinement
- Document improvements with measurable metrics
- Achieve high pass rates (80%+) efficiently

**Core principle**: Fix patterns systematically by understanding specificity hierarchy and matching logic, not by adding more patterns.

## When to Use This Skill

Activate this skill when:
- Running beta test cycles for static pattern matchers
- Analyzing test suite failures to identify root causes
- Improving command generation pass rates
- Reordering patterns for specificity
- Fixing pattern over-matching or under-matching issues
- Documenting cycle results with metrics

**Example triggers:**
- "Run the next beta test cycle"
- "Analyze why these tests are failing"
- "Improve the static matcher pass rate"
- "Fix pattern ordering issues"

## Core Workflow

### Phase 1: Run Test Suite

Execute the test suite and capture results:

```bash
# Build the project
cargo build --release

# Run test suite
./target/release/caro test --backend static --suite .claude/beta-testing/test-cases.yaml > /tmp/cycle-N-results.txt

# Review results
cat /tmp/cycle-N-results.txt
```

**Key metrics to track:**
- Overall pass rate (percentage)
- Passing tests by category
- Failing tests by category
- Pattern count

### Phase 2: Analyze Failures by Root Cause

Categorize each failure into one of these root causes:

1. **Pattern Ordering Issue**: More general pattern matches before more specific pattern
   - **Symptom**: Test expects specific output but gets generic output
   - **Example**: Test "find Python files modified today" matches generic "files modified today" pattern
   - **Fix**: Reorder specific pattern before general pattern

2. **Pattern Over-Matching**: Pattern matches queries it shouldn't
   - **Symptom**: Pattern incorrectly matches queries from different categories
   - **Example**: Japanese pattern with optional keyword "files" matches English queries
   - **Fix**: Remove optional keywords or tighten regex

3. **Pattern Under-Matching**: Pattern doesn't match intended queries
   - **Symptom**: Expected pattern doesn't match, returns "No static pattern match found"
   - **Example**: Japanese query doesn't match because pattern requires English keyword "find"
   - **Fix**: Remove restrictive required keywords or adjust regex

4. **Missing Pattern**: No pattern exists for this query type
   - **Symptom**: Multiple related test failures, no candidate pattern
   - **Fix**: Add new pattern (use sparingly - reordering usually better)

**Priority**: Address ordering issues first (highest ROI), then over/under-matching, finally missing patterns.

### Phase 3: Implement Fixes

Apply fixes based on root cause analysis:

#### Fix Type 1: Pattern Reordering

Move specific patterns before general patterns. See `references/pattern-ordering-strategy.md` for detailed specificity calculation.

**Quick specificity guide:**
- More required keywords = more specific
- More constraints (size, location, file type, time) = more specific
- Regex-only patterns (empty keywords) = highly specialized

**Example reordering:**
```rust
// Before (Pattern 46 at end, Pattern 1 at beginning)
Pattern 1: "files modified today" (3 keywords: file, modified, today)
...
Pattern 46: "Python files modified today" (4 keywords: python, file, modified, today)

// After (reorder Pattern 46 → Pattern 1)
Pattern 1: "Python files modified today" (4 keywords) ← More specific, checks first
Pattern 2: "files modified today" (3 keywords) ← General fallback
```

#### Fix Type 2: Keyword Adjustment

**Remove optional keywords** when pattern over-matches:
```rust
// Before (over-matching English queries)
PatternEntry {
    required_keywords: vec![],
    optional_keywords: vec!["find".to_string(), "files".to_string()],
    regex_pattern: Some(Regex::new(r"[ぁ-んァ-ヶー一-龯]").unwrap()),
    // ...
}

// After (regex-only matching)
PatternEntry {
    required_keywords: vec![],
    optional_keywords: vec![],  // Empty forces regex-only
    regex_pattern: Some(Regex::new(r"[ぁ-んァ-ヶー一-龯]").unwrap()),
    // ...
}
```

**Remove restrictive required keywords** when pattern under-matches:
```rust
// Before (requires English "find" for Japanese query)
required_keywords: vec!["find".to_string()]

// After (no English keywords required)
required_keywords: vec![]
```

#### Fix Type 3: Regex Refinement

Tighten or loosen regex patterns as needed. See `references/pattern-ordering-strategy.md` for regex design patterns.

### Phase 4: Build and Test

After implementing fixes:

```bash
# Build
cargo build --release

# Run tests
./target/release/caro test --backend static --suite .claude/beta-testing/test-cases.yaml

# Save results
./target/release/caro test --backend static --suite .claude/beta-testing/test-cases.yaml > /tmp/cycle-N-results.txt
```

**Verification checklist:**
- [ ] Build succeeds without errors
- [ ] Target tests now pass
- [ ] No new test failures introduced (regressions)
- [ ] Pass rate improved

### Phase 5: Document Results

Create cycle documentation following the template in `references/cycle-documentation.md`.

**Required sections:**
1. **Executive Summary**: Pass rate change, key achievements
2. **Improvements Made**: Detailed description of each fix
3. **Results Comparison**: Before/after metrics table
4. **Pattern Impact Analysis**: Which reorderings/fixes worked
5. **Lessons Learned**: Insights for future cycles
6. **Next Steps**: Priority improvements for next cycle

**Key metrics to document:**
- Overall pass rate (before → after, percentage change)
- Passing tests by category (before → after)
- Pattern count (net change)
- Complete categories count

See `examples/cycle-analysis.md` for a real example from Cycle 8.

### Phase 6: Commit and Push

Commit changes with descriptive message:

```bash
# Stage changes
git add src/backends/static_matcher.rs .claude/beta-testing/cycles/cycle-N-*.md

# Commit with detailed message
git commit -m "fix(static): [Cycle N] <summary>

- Fix 1 description
- Fix 2 description
- Category X: before% → after% (+N tests)
- Overall pass rate: before% → after% (passing/total tests, N complete categories)
- Pattern count: before → after

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Push to remote
git push origin main
```

## Pattern Matching Logic

Understanding how patterns match is critical for effective fixes. The matching logic in `static_matcher.rs` follows this hierarchy:

1. **Regex check first** (lines 598-603): If regex exists AND matches → return immediately
2. **Keyword fallback** (lines 606-619): If regex doesn't match OR doesn't exist:
   - Check ALL required keywords present
   - Count optional keywords
   - Match if: `optional_count > 0 OR pattern.regex_pattern.is_none()`

**Key insight**: Optional keywords act as a fallback when regex doesn't match. For patterns that should ONLY match via regex (like i18n), remove all optional keywords.

## Pattern Design Guidelines

Based on matching logic, three pattern types emerge:

1. **Regex-only patterns**: Empty required_keywords + empty optional_keywords + regex
   - Use for: i18n queries, highly specialized patterns
   - Example: Japanese filename search

2. **Keyword-only patterns**: Keywords + no regex (or very loose regex)
   - Use for: General queries with clear keywords
   - Example: "files modified today"

3. **Hybrid patterns**: Keywords + regex (both must be relevant)
   - Use for: Specific queries with both keyword and structural requirements
   - Example: "Python files modified in last 7 days"

## Success Metrics

Track these metrics across cycles:

**Per-Cycle Metrics:**
- Pass rate improvement (percentage points)
- Tests fixed (count)
- Patterns added/removed (net change)
- Categories completed (count)

**Cumulative Metrics:**
- Overall pass rate trend
- Total pattern efficiency (passing tests ÷ pattern count)
- Category completion rate

**Efficiency Indicators:**
- ROI: Tests fixed per pattern change
- Reordering success rate (should be 100%)
- Regression rate (should be 0%)

## Best Practices

### DO

✅ **Prioritize reordering over adding patterns**
- Pattern reordering has infinite ROI (0 patterns → +N tests)
- Adding patterns increases maintenance burden
- Most failures are ordering issues, not missing patterns

✅ **Batch related reorderings together**
- Move all file-type-specific patterns before general patterns in one cycle
- Higher success rate, clearer intent, better documentation

✅ **Remove optional keywords for specialized patterns**
- Forces regex-only matching
- Prevents false positives
- Ideal for i18n and domain-specific patterns

✅ **Document specificity reasoning**
- Explain why Pattern A is more specific than Pattern B
- Count required keywords + constraints
- Future maintainers will thank you

✅ **Test after every change**
- Catch regressions immediately
- Verify fix worked as intended
- Document unexpected side effects

### DON'T

❌ **Don't add patterns without exhausting reordering options**
- Reordering is almost always the better fix
- New patterns increase complexity
- Pattern proliferation hurts maintainability

❌ **Don't adjust keywords without understanding matching logic**
- Optional keywords create fallback matching
- Removing required keywords increases false positives
- Read the matching logic first

❌ **Don't batch unrelated changes**
- One fix per commit when debugging
- Batch only proven patterns (like final reorderings)
- Makes bisecting failures easier

❌ **Don't skip documentation**
- Insights fade quickly
- Patterns repeat across cycles
- Future cycles build on lessons learned

❌ **Don't ignore false positives**
- Over-matching is as bad as under-matching
- Check that fixes don't break other categories
- Run full test suite, not just target tests

## Common Patterns

### Pattern 1: File-Type-Specific Before General

**Scenario**: Test "find Python files modified today" matches generic "files modified today"

**Fix**: Move file-type-specific pattern before general pattern
- Python-specific (4 keywords) → Position N
- General files (3 keywords) → Position N+1

**Success rate**: 100% (never fails when applied correctly)

### Pattern 2: Constraint-Specific Before General

**Scenario**: Test "disk usage by directory, sorted" matches "disk usage by folder"

**Fix**: Move pattern with more constraints before pattern with fewer
- With "sorted" constraint (4 keywords) → Position N
- Without "sorted" (3 keywords) → Position N+1

**Success rate**: 100% (specificity hierarchy)

### Pattern 3: Regex-Only for Specialized Patterns

**Scenario**: i18n pattern with optional English keywords matches English queries

**Fix**: Remove all keywords to force regex-only matching
- Before: `optional_keywords: vec!["find", "files"]`
- After: `optional_keywords: vec![]`

**Success rate**: 100% (eliminates keyword fallback)

## Automation Opportunities

Consider automating these tasks with scripts in `scripts/`:

1. **Pattern specificity scoring**: Calculate and sort patterns by specificity
2. **False positive detection**: Test each pattern against all test queries
3. **Regression testing**: Compare results across cycles
4. **Cycle report generation**: Auto-generate portions of cycle documentation

See `scripts/` directory for available automation utilities.

## Additional Resources

### Reference Files

For detailed guidance, consult:
- **`references/pattern-ordering-strategy.md`** - Comprehensive pattern specificity calculation, ordering rules, and reordering workflow
- **`references/cycle-documentation.md`** - Template and guidelines for documenting cycle results
- **`references/matching-logic-deep-dive.md`** - Detailed analysis of StaticMatcher matching logic

### Example Files

Real-world examples in `examples/`:
- **`examples/cycle-analysis.md`** - Complete Cycle 8 analysis showing all sections
- **`examples/pattern-reordering.md`** - Before/after examples of successful reorderings

### Scripts

Utilities in `scripts/`:
- **`scripts/run-cycle.sh`** - Automated cycle execution workflow
- **`scripts/analyze-failures.sh`** - Parse test output and categorize failures

## Quick Reference

### Cycle Workflow Summary

1. **Run tests** → Capture results
2. **Analyze failures** → Categorize by root cause
3. **Fix patterns** → Reorder, adjust keywords, refine regex
4. **Build and test** → Verify improvements
5. **Document** → Create cycle markdown with metrics
6. **Commit** → Descriptive message with metrics

### Specificity Hierarchy

```
Most Specific (check first)
↓
File-type + Time + Location + Size
File-type + Time
File-type + Location
File-type
General query
↓
Least Specific (check last)
```

### Common Fixes

| Problem | Fix | Example |
|---------|-----|---------|
| General matches before specific | Reorder by keyword count | Python files (4 kw) before files (3 kw) |
| Over-matching English queries | Remove optional keywords | i18n pattern: empty optional_keywords |
| Under-matching target queries | Remove restrictive required kw | Japanese pattern: remove "find" requirement |
| Conflicting specific forms | Swap + tighten regex | 1GB with-exec before 1GB without-exec |

## Implementation Workflow

To run a beta test cycle:

1. **Prepare**: Ensure test suite exists at `.claude/beta-testing/test-cases.yaml`
2. **Run Phase 1**: Execute test suite, save results
3. **Run Phase 2**: Analyze each failure, categorize by root cause
4. **Run Phase 3**: Implement fixes (prefer reordering, batch related changes)
5. **Run Phase 4**: Build and test, verify no regressions
6. **Run Phase 5**: Document results following template
7. **Run Phase 6**: Commit with metrics, push to remote

**Target**: Each cycle should improve pass rate by 3-10 percentage points through surgical fixes.

**Milestone**: Aim for 80%+ pass rate (product delivers on promises), then 85%+ (excellent), then category completions.

Focus on pattern reordering and strategic keyword adjustments over pattern proliferation for maximum efficiency and maintainability.
