---
name: hammer-changelog-generator
description: Generates comprehensive, professionally-formatted changelogs for SDL3 HammerEngine from git history. Analyzes code changes, runs tests, includes architect review, and produces detailed documentation following World Update format. Use when documenting updates, preparing releases, or creating detailed change reports.
allowed-tools: [Bash, Read, Write, Grep, Glob, Task, AskUserQuestion]
---

# Changelog Generator for SDL3 HammerEngine

You are generating a comprehensive, professionally-formatted changelog for SDL3 HammerEngine following the established World Update format.

## Your Task

Create a detailed changelog document that captures all changes, performance improvements, architectural impacts, and testing results for the current branch.

## Step-by-Step Process

### Step 1: Gather Update Information

Use the AskUserQuestion tool to collect:

**Question 1: Update Name**
- Header: "Update Name"
- Question: "What should this update be called?"
- Options:
  - "World Update #[number]" (for major feature additions)
  - "Performance Optimization" (for perf-focused changes)
  - "Bug Fix Update" (for bug fixes)
  - Custom (user provides name)

**Question 2: Update Scope**
- Header: "Scope"
- Question: "What is the primary focus of this update?"
- Options:
  - "AI System changes"
  - "Collision/Pathfinding changes"
  - "Rendering/Particle changes"
  - "Threading/Performance changes"
  - Multiple systems (user specifies)

**Question 3: Architect Review**
- Header: "Review"
- Question: "Request comprehensive architectural review?"
- Options:
  - "Yes - Full review" (launches game-systems-architect)
  - "No - Skip review"

**Question 4: Test Verification**
- Header: "Testing"
- Question: "Run test suites to verify changes?"
- Options:
  - "Yes - Run all affected tests"
  - "No - Skip testing"

### Step 2: Analyze Changes

**2a. Git Analysis**
```bash
# Get current branch
git rev-parse --abbrev-ref HEAD

# Get modified files
git diff --name-status main...HEAD

# Get detailed stats
git diff --stat main...HEAD

# Get commit history
git log --oneline main...HEAD
```

**2b. File Analysis**
For each modified file:
- Read the file to understand changes
- Identify modified functions/classes
- Note line counts (added/removed/modified)
- Categorize by system (AI, Collision, Test, etc.)

### Step 3: Performance Analysis

**3a. Memory Impact**
- Check for removed/added allocations
- Identify buffer size changes
- Calculate memory savings/costs

**3b. Allocation Rate**
- Search for eliminated per-frame allocations
- Identify new pre-allocation patterns
- Calculate allocation rate improvements

**3c. Threading Changes**
- Identify new async paths
- Check WorkerBudget integration changes
- Document synchronization improvements

### Step 4: Run Tests (if requested)

Based on changed systems, run:
- AI changes → `./tests/test_scripts/run_thread_safe_ai_tests.sh`
- Collision → `./tests/test_scripts/run_collision_tests.sh`
- All systems → `./run_all_tests.sh --core-only`

Document:
- Tests run
- Pass/fail status
- New tests added
- Fixed tests

### Step 5: Request Architect Review (if requested)

Use the Task tool with game-systems-architect:
```
Review all changes on the current branch for:
- Architecture coherence
- Performance implications
- Thread safety
- Integration with other systems
- Code quality

Provide detailed assessment with grades.
```

### Step 6: Generate Changelog

Create `changelogs/CHANGELOG_[UPDATE_NAME].md` with this structure:

```markdown
# [Update Name]

**Branch:** `[branch_name]`
**Date:** [YYYY-MM-DD]
**Review Status:** [✅ APPROVED / ⚠️ PENDING / ❌ NEEDS CHANGES]
**Overall Grade:** [A+ (95/100) or TBD]

---

## Executive Summary

[2-3 paragraphs summarizing:
- What changed (high-level)
- Why it changed (motivation)
- Impact (performance, architecture, features)]

**Impact:**
- ✅ [Key improvement 1]
- ✅ [Key improvement 2]
- ✅ [Key improvement 3]

---

## Changes Overview

### Core Implementation ([Primary File])

**File:** `path/to/file`
**Method/Class:** `[affected methods]`
**Lines Changed:** ~[XX] modified, ~[XX] removed, ~[XX] added

### Test Fixes ([Test File])

**File:** `path/to/test`
**Tests Modified:** [test names]
**Lines Changed:** ~[XX] added

---

## Detailed Changes

### 1. [Change Category 1]

**Problem:**
[Describe what was wrong/missing]

**Solution:**
[Describe the fix/improvement with code snippets]

**Impact:**
[What this improves]

**File Location:** `path/to/file:lines`

---

### 2. [Change Category 2]

[Repeat for each major change]

---

## Performance Analysis

### Memory Improvements

| Component | Before | After | Savings |
|-----------|--------|-------|---------|
| [Component 1] | [size] | [size] | **[delta]** |
| [Component 2] | [size] | [size] | **[delta]** |
| **Net Savings** | - | - | **[total]** |

### Allocation Rate Improvements (@ 60 FPS)

| Operation | Before | After | Reduction |
|-----------|--------|-------|-----------|
| [Operation 1] | [rate] | [rate] | **[%]** |
| [Operation 2] | [rate] | [rate] | **[%]** |

### Threading Improvements

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| [Metric 1] | [value] | [value] | ✅ [description] |
| [Metric 2] | [value] | [value] | ✅ [description] |

---

## Threading Behavior Changes

### Before
[Describe old threading behavior with code/pseudocode]

### After
[Describe new threading behavior with code/pseudocode]

**Benefits:**
- [Benefit 1]
- [Benefit 2]

---

## Architecture Coherence

### Pattern Consistency Across Managers

| Manager | [Pattern 1] | [Pattern 2] | [Pattern 3] |
|---------|-------------|-------------|-------------|
| [Manager 1] | ✅/❌ | ✅/❌ | ✅/❌ |
| [Manager 2] | ✅/❌ | ✅/❌ | ✅/❌ |

**Result:** [Overall assessment]

---

## Testing Summary

### Test Suite Results

\`\`\`bash
✅ [Test Suite 1] - ALL PASSED
   - [X] test cases executed
   - [Key tests verified]
   - 0 failures

✅ [Test Suite 2] - ALL PASSED
   - [X] test cases executed
   - [Key tests verified]
   - 0 failures
\`\`\`

### Test Reliability Improvement

| Test Case | Before | After | Fix Applied |
|-----------|--------|-------|-------------|
| [Test 1] | ❌/✅ | ✅ | [Description] |
| [Test 2] | ❌/✅ | ✅ | [Description] |

**Overall Test Reliability:** [%] → [%]

---

## Code Quality Improvements

### Comments & Documentation

**Added:**
- [Location]: [Description of comment/doc added]

### Code Readability

**Before:** [Description of issues]

**After:** [Description of improvements]

---

## Thread Safety Analysis

### Synchronization Improvements

**Old Pattern:**
[Describe old sync mechanism with issues]

**New Pattern:**
[Describe new sync mechanism]

**Benefits:**
- [Benefit 1]
- [Benefit 2]

### Mutex Ordering

**Verified lock acquisition order:**
1. [Mutex 1]
2. [Mutex 2]
3. [Mutex 3]

**Consistency:** [Assessment]

---

## Integration Impact

### System Dependencies

**[System 1]:**
- ✅/❌ Impact: [Description]

**[System 2]:**
- ✅/❌ Impact: [Description]

---

## Architect Review Summary

**Review Status:** [✅ APPROVED / ⚠️ PENDING / ❌ NEEDS CHANGES]
**Confidence Level:** [HIGH / MEDIUM / LOW]
**Reviewer:** [Systems Architect Agent / Manual]

### Assessment Grades

| Category | Grade | Justification |
|----------|-------|---------------|
| Architecture Coherence | [X]/10 | [Reason] |
| Performance Impact | [X]/10 | [Reason] |
| Thread Safety | [X]/10 | [Reason] |
| Code Quality | [X]/10 | [Reason] |
| Testing | [X]/10 | [Reason] |

**Overall: [Grade] ([Score]/100)**

### Key Observations

**✅ Strengths:**
1. [Strength 1]
2. [Strength 2]

**⚠️ Observations:**
1. [Observation 1]
2. [Observation 2]

**Recommended Actions:**
1. [Action 1]
2. [Action 2]

---

## Migration Notes

### Breaking Changes

[List breaking changes or "NONE"]

### API Changes

[List API changes or "NONE"]

### Configuration Changes

[List config changes or "NONE"]

### Behavioral Changes

[Describe behavior changes if any]

---

## Performance Benchmarks

### Test Environment
- **Hardware:** [Description]
- **OS:** [Version]
- **Build:** [Debug/Release]
- **Worker Threads:** [Count]

### [Benchmark Category]

| [Metric] | Before | After | Delta | Notes |
|----------|--------|-------|-------|-------|
| [Case 1] | [value] | [value] | [%] | [Note] |
| [Case 2] | [value] | [value] | [%] | [Note] |

**Interpretation:**
[Explain benchmark results]

---

## Future Enhancements (Optional)

### Low Priority

1. **[Enhancement 1]** (effort: [time])
   - [Description]
   - Rationale: [Why]

2. **[Enhancement 2]** (effort: [time])
   - [Description]
   - Rationale: [Why]

### Nice-to-Have

1. **[Enhancement 3]** (effort: [time])
   - [Description]

---

## Files Modified

\`\`\`
[file1]
├─ [function/method 1]     (lines [X-Y] modified)
├─ [function/method 2]     (lines [X-Y] added)
└─ [Comments updated]

[file2]
├─ [changes]
└─ [changes]
\`\`\`

**Total Changes:**
- Lines added: ~[X]
- Lines removed: ~[X]
- Lines modified: ~[X]
- Files changed: [X]
- Net: [+/-X] lines

---

## Commit History

\`\`\`bash
# Suggested commit messages for merge:

git commit -m "[category]([component]): [brief description]

- [Change detail 1]
- [Change detail 2]
- [Change detail 3]

Refs: [Update Name]"
\`\`\`

---

## References

**Related Documentation:**
- [Doc 1]
- [Doc 2]

**Related Issues:**
- [Issue description]

**Related PRs:**
- [Previous update]

---

## Changelog Version

**Document Version:** 1.0
**Last Updated:** [YYYY-MM-DD]
**Status:** [Draft / Final - Ready for Merge]

---

**END OF CHANGELOG**
```

---

## Important Guidelines

### Writing Style

1. **Be Specific:** Use concrete numbers, not vague descriptions
   - Good: "Reduced allocations from 200/sec to 50/sec (75% reduction)"
   - Bad: "Reduced allocations significantly"

2. **Show Evidence:** Include code snippets, file locations, line numbers
   - Good: "AIManager.cpp:941-945 - Fixed threshold consistency"
   - Bad: "Fixed threshold"

3. **Use Tables:** For comparisons, benchmarks, grades
   - Makes information scannable
   - Easy to compare before/after

4. **Include Context:** Explain WHY changes were made
   - "Problem → Solution → Impact" structure
   - Historical context when relevant

5. **Grade Appropriately:**
   - A+ (95-100): Exceptional, no issues
   - A (90-94): Excellent, minor observations
   - B+ (85-89): Good, some concerns
   - B (80-84): Acceptable, needs improvement
   - Below B: Not ready for merge

### Content Requirements

**Must Include:**
- ✅ Executive summary (2-3 paragraphs)
- ✅ Detailed changes with code snippets
- ✅ Performance analysis with numbers
- ✅ Test results (if tests run)
- ✅ Files modified with line counts
- ✅ Suggested commit messages

**Should Include (if applicable):**
- Architecture coherence analysis
- Thread safety review
- Integration impact
- Migration notes
- Performance benchmarks
- Future enhancements

**Optional:**
- Architect review (if requested)
- Detailed benchmarks (if measured)
- Historical context (if relevant)

---

## Final Steps

After generating the changelog:

1. **Save the file** to `changelogs/CHANGELOG_[UPDATE_NAME].md`
2. **Summarize to user:**
   - Changelog location
   - Overall grade (if reviewed)
   - Key improvements
   - Files changed count

**IMPORTANT: Do NOT commit anything. The user will handle commits manually.**

---

**You are now ready to generate the changelog. Begin by gathering update information from the user.**
