---
name: quality-update
description: Incrementally implement code quality improvements from docs/quality_review.md with tests and atomic commits. Run after /review-for-quality to apply fixes.
agent: general-purpose
allowed-tools: Read, Grep, Edit, Write, Bash
---

# Quality Update - Incremental Implementation

Systematically implement code quality improvements from the review document, making tested, atomic commits for each fix.

## Process Overview

1. **Read the quality review** from `docs/quality_review.md`
2. **Prioritize improvements** (start with Quick Wins, then High Priority)
3. **Implement fixes incrementally** (one logical change at a time)
4. **Run tests after each change** to ensure nothing breaks
5. **Make atomic commits** that capture the change and its purpose
6. **Update review document** to track progress

## Detailed Steps

### Step 1: Read and Parse Review

```bash
# Read the current quality review
Read docs/quality_review.md
```

Focus on these sections in priority order:
1. **Appendix B: Quick Wins** - Start here (fast, low risk)
2. **High Priority (This Week)** - Critical improvements
3. **Medium Priority (Next Week)** - Important but not urgent
4. Skip Low Priority items for now

### Step 2: Select Next Improvement

Choose improvements based on:
- **Risk**: Low risk first (refactoring, style fixes)
- **Dependencies**: Prerequisites before dependent work
- **Atomicity**: Each commit should be one logical change
- **Test coverage**: Ensure tests exist or add them

### Step 3: Implement the Fix

For each improvement:

1. **Read affected files** to understand current state
2. **Make the change** using Edit or Write
3. **Run linter** to ensure style compliance:
   ```bash
   bundle exec rake standard:fix
   ```
4. **Run tests** to verify correctness:
   ```bash
   bundle exec rspec
   ```
5. **Fix any test failures** before proceeding

### Step 4: Make Atomic Commit

**Commit Message Format:**
```
[Quality] Brief description of what was fixed

- Specific change made (e.g., "Extract DatabaseCheck from DoctorCommand")
- Why this improves quality (e.g., "Improves SRP and testability")
- Expert principle applied (e.g., "Sandi Metz: Single Responsibility")

Addresses: docs/quality_review.md [section reference]
```

**Example Commit:**
```bash
git add -A
git commit -m "[Quality] Fix public keyword placement in SQLiteStore

- Move all public methods to top of class
- Keep all private methods at bottom
- Improves code readability and conventional Ruby structure

Addresses: docs/quality_review.md (Jeremy Evans - Inconsistent Visibility)
"
```

### Step 5: Document Progress

After each successful commit:
- Note which item was completed
- Track how many items remain in current priority
- Identify any blockers encountered

### Step 6: Continue or Report

**Continue** to next improvement if:
- Tests pass ✅
- Commit successful ✅
- No blockers encountered ✅

**Stop and report** if:
- Tests fail after multiple fix attempts ❌
- Change introduces unexpected complexity ❌
- External dependency issue (gem version, etc.) ❌

## Commit Strategy

### Grouping Guidelines

**✅ Good atomic commits:**
- "Fix public keyword placement in SQLiteStore" (single file, style fix)
- "Extract DatabaseCheck from DoctorCommand" (single responsibility extraction)
- "Replace nil returns with NullExplanation in Recall" (consistent pattern)
- "Consolidate ENV access via Configuration class" (centralize pattern)

**❌ Too large (split these):**
- "Refactor Recall class" (too broad - split into multiple commits)
- "Fix all Sandi Metz violations" (too many changes at once)
- "Update database and add tests" (should be separate commits)

**❌ Too small (combine these):**
- "Fix typo in comment" + "Fix another typo" (combine style fixes)
- "Add space after comma" (use standard:fix instead)

### When to Split Work

Split into multiple commits when:
- Touching multiple files that serve different purposes
- Making structural change + adding tests (commit structure first, tests second)
- Fixing multiple unrelated issues from review

## Testing Requirements

**Before each commit:**
```bash
# 1. Run linter
bundle exec rake standard:fix

# 2. Run full test suite
bundle exec rspec

# 3. Check for any warnings
bundle exec rake
```

**If tests fail:**
1. Fix the test failures first
2. If fix is complex, it might need its own commit
3. Never commit broken tests

## Progress Tracking

Keep a running count:
- ✅ Quick Wins completed: X/Y
- ✅ High Priority completed: X/Y
- ⏳ Currently working on: [description]
- ❌ Blocked: [description + reason]

## Success Criteria

The skill completes successfully when:
- All Quick Wins from Appendix B are implemented ✅
- Or at least 3-5 High Priority items are completed ✅
- All tests pass ✅
- All commits follow the format above ✅
- Progress report provided ✅

## Important Notes

- **Never skip tests** - each change must pass tests before committing
- **Keep commits focused** - one logical change per commit
- **Use standard:fix** - auto-fix linting issues before committing
- **Read before editing** - understand context before making changes
- **Conservative approach** - if unsure about a change, skip it and report
- **Track time** - if a fix takes > 30 minutes, it might need planning first

## Example Session

```
1. Read docs/quality_review.md
2. Start with Quick Win: "Fix public keyword placement in SQLiteStore"
3. Read lib/claude_memory/store/sqlite_store.rb
4. Move public methods to top, private to bottom
5. Run: bundle exec rake standard:fix
6. Run: bundle exec rspec
7. Commit: "[Quality] Fix public keyword placement in SQLiteStore..."
8. Next: "Consolidate ENV access via Configuration"
9. [Continue process...]
10. Report: "Completed 5/5 Quick Wins, started 2/6 High Priority items"
```

## Error Handling

If you encounter issues:
- **Test failures**: Debug and fix, or skip and report
- **Merge conflicts**: Stop and report (user intervention needed)
- **Missing dependencies**: Stop and report
- **Unclear requirements**: Skip item and note in report

## Final Report Format

```
## Quality Update Session Report

### Completed ✅
1. [Quick Win] Fixed public keyword placement in SQLiteStore (commit: abc123)
2. [Quick Win] Consolidated ENV access via Configuration (commit: def456)
3. [High Priority] Extracted BatchQueryBuilder from Recall (commit: ghi789)

### In Progress ⏳
- Working on: Extract DatabaseCheck from DoctorCommand
- Status: 60% complete, tests passing

### Blocked ❌
- [High Priority] Split Recall.rb god object
  - Reason: Requires architectural planning, too large for automated fix
  - Recommendation: Run /review-for-quality again after completing other items

### Summary
- Quick Wins: 5/5 completed ✅
- High Priority: 2/6 completed
- Tests: All passing ✅
- Commits: 5 atomic commits made
- Time: ~2 hours

### Next Steps
1. Continue with remaining High Priority items
2. Consider running /review-for-quality again to assess progress
3. Plan architectural refactoring for Recall.rb god object
```
