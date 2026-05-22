---
name: bug-fixing
category: workflow
version: 2.0.0
description: Systematic debugging and bug fixing with Australian user-friendly messages
author: Unite Group
priority: 3
triggers:
  - bug
  - fix bug
  - debug
  - error
  - issue
requires:
  - verification/verification-first.skill.md
  - verification/error-handling.skill.md
---

# Bug Fixing Workflow

## Purpose

Guide agents through systematic bug fixing: reproduction, root cause analysis, fix, and regression prevention.

## Workflow Phases

### Phase 1: Reproduce the Bug

**Objective**: Confirm bug exists and understand conditions

```markdown
1. Gather Information
   - Error message/stack trace
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (browser, OS, Australian locale)

2. Reproduce Locally
   - Follow reproduction steps
   - Observe behavior
   - Capture error details
   - Document conditions

3. Create Failing Test
   - Write test that triggers bug
   - Test should fail initially
   - Commit failing test
```

**Outputs**:
- Confirmed reproduction steps
- Failing test
- Clear error description

**If Cannot Reproduce**:
- Request more information
- Check environment differences (Australian locale settings)
- Try edge cases
- Escalate if needed

### Phase 2: Locate the Issue

**Objective**: Find where the bug originates

```markdown
1. Analyze Stack Trace
   - Find entry point
   - Follow execution path
   - Identify failing line

2. Add Logging/Debugging
   - Log inputs at key points
   - Check intermediate values
   - Verify assumptions

3. Narrow Down
   - Binary search approach
   - Isolate problematic code
   - Identify exact cause
```

**Debugging Techniques**:

**Python**:
```python
import logging
logger = logging.getLogger(__name__)

def process_data(data):
    logger.debug(f"Input: {data}")  # Check input
    result = transform(data)
    logger.debug(f"Transformed: {result}")  # Check intermediate
    return result
```

**TypeScript**:
```typescript
function processData(data: Data): Result {
    console.log('Input:', data)  // Temporary debug
    const result = transform(data)
    console.log('Result:', result)  // Temporary debug
    return result
}
```

**Remember**: Remove debug logging after fixing!

### Phase 3: Understand Root Cause

**Objective**: Understand WHY it's broken

```markdown
1. Ask Five Whys
   - Why did it fail?
   - Why was that condition true?
   - Why wasn't it handled?
   - Why did we assume that?
   - Why is the design that way?

2. Identify Category
   - Logic error
   - Edge case not handled
   - Race condition
   - Incorrect assumption
   - Missing validation
   - Performance issue
   - Australian context issue (date/currency formatting)

3. Check for Similar Issues
   - Query memory for similar bugs
   - Search codebase for pattern
   - Are other places affected?
```

**Root Cause Categories**:

| Category | Example | Fix Strategy |
|----------|---------|--------------|
| Logic Error | Wrong condition | Fix logic |
| Edge Case | Null not handled | Add validation |
| Race Condition | Async timing | Add synchronization |
| Assumption | Assumed non-null | Validate assumptions |
| Validation | No input check | Add validation |
| Performance | Slow query | Optimize |
| Locale | US date format | Apply Australian formatting |

### Phase 4: Implement Fix

**Objective**: Fix the bug properly

```markdown
1. Design Fix
   - Address root cause (not symptom)
   - Consider edge cases
   - Avoid breaking changes
   - Check performance impact
   - Ensure Australian context preserved

2. Implement Fix
   - Minimal code change
   - Follow project patterns
   - Handle errors properly (en-AU messages)
   - Add comments explaining fix

3. Verify Locally
   - Failing test now passes
   - No new test failures
   - Manual test works
   - No regressions
   - Australian context still correct
```

**Fix Patterns**:

**Add Validation**:
```python
# Before (buggy)
def divide(a, b):
    return a / b  # Crashes if b=0

# After (fixed)
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**Handle Null/None**:
```typescript
// Before (buggy)
function getName(user: User): string {
    return user.name.toUpperCase()  // Crashes if name is null
}

// After (fixed with Australian-friendly default)
function getName(user: User): string {
    return user.name?.toUpperCase() ?? 'Unknown'
}
```

**Fix Australian Date Formatting**:
```typescript
// Before (buggy - US format)
function formatDate(date: Date): string {
    return date.toLocaleDateString('en-US')  // MM/DD/YYYY
}

// After (fixed - Australian format)
function formatDate(date: Date): string {
    return date.toLocaleDateString('en-AU')  // DD/MM/YYYY
}
```

**Add Async Safety**:
```python
# Before (buggy)
async def fetch_data():
    data = requests.get(url)  # Blocks event loop

# After (fixed)
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
```

### Phase 5: Add Regression Test

**Objective**: Ensure bug doesn't come back

```markdown
1. Create Regression Test
   - Test the specific bug scenario
   - Include edge cases found
   - Test should pass now
   - Descriptive test name

2. Test Coverage
   - Cover the fix
   - Cover related edge cases
   - Update existing tests if needed

3. Verify No Regressions
   - All existing tests pass
   - No new failures introduced
   - Performance not degraded
```

**Regression Test Pattern**:
```python
def test_regression_issue_123_divide_by_zero():
    """Regression test for issue #123: Division by zero crash.

    Previously, calling divide(10, 0) would crash with ZeroDivisionError.
    Now it should raise a descriptive ValueError.
    """
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
```

### Phase 6: Document & Learn

**Objective**: Capture learnings

```markdown
1. Update Code
   - Add comment explaining fix
   - Update docstring if behavior changed
   - Note any caveats

2. Update Documentation
   - README if user-facing bug
   - API docs if behavior changed
   - Migration guide if breaking

3. Store to Memory
   - Record failure pattern
   - Store fix approach
   - Document root cause
   - Prevent similar bugs
```

### Phase 7: Create PR

**Objective**: Get fix reviewed and merged

```markdown
1. Create Bug Fix Branch
   - Branch name: `fix/agent-{issue-number}`

2. Commit Changes
   - Clear commit message
   - Reference issue number
   - Include test

3. PR Description
   - Link to issue
   - Describe bug
   - Explain fix
   - Show test evidence

4. Request Review
   - Await human approval
```

## Example: Fixing Date Display Bug (Australian)

### Phase 1: Reproduce
```
Bug Report: "Dates showing in wrong format (MM/DD/YYYY instead of DD/MM/YYYY)"

Reproduction:
1. Create invoice
2. View invoice details
3. Date displays as 01/15/2025 (should be 15/01/2025)

Created failing test:
test_invoice_date_format_australian() - FAIL
```

### Phase 2: Locate
```
Stack trace points to:
  invoice_formatter.ts:23 - formatDate()

Found issue:
  Using toLocaleDateString('en-US') instead of 'en-AU'
```

### Phase 3: Root Cause
```
Root Cause: Hardcoded US locale instead of Australian

Why?
1. Default locale was 'en-US'
2. No Australian context enforcement
3. No validation of date format output

Category: Locale/Internationalization error
```

### Phase 4: Implement Fix
```typescript
// Before (buggy)
function formatDate(date: Date): string {
    return date.toLocaleDateString('en-US')
}

// After (fixed)
function formatDate(date: Date, locale: string = 'en-AU'): string {
    // Always default to Australian format unless explicitly overridden
    return date.toLocaleDateString(locale)
}
```

### Phase 5: Regression Test
```typescript
describe('Date formatting', () => {
    it('should format dates in Australian DD/MM/YYYY format by default', () => {
        const date = new Date('2025-01-15')
        const formatted = formatDate(date)
        expect(formatted).toBe('15/01/2025')
    })

    it('regression: dates should not use US format', () => {
        const date = new Date('2025-01-15')
        const formatted = formatDate(date)
        expect(formatted).not.toBe('01/15/2025')  // Not US format
    })
})
```

### Phase 6: Document
```
Updated:
- Added docstring noting default Australian format
- Updated README with date formatting guidelines

Stored to memory:
- Failure pattern: Hardcoded locales
- Fix approach: Default to en-AU
- Root cause: Missing Australian context enforcement
```

### Phase 7: PR
```
Created: PR #234 - "fix(invoices): Use Australian date format (DD/MM/YYYY)"
Status: Awaiting review
Tests: All passing ✅
```

## Key Principles

1. **Always Reproduce First**: Don't guess at fixes
2. **Root Cause, Not Symptom**: Fix the real problem
3. **Test the Fix**: Prove it works
4. **Regression Test**: Ensure it stays fixed
5. **Learn**: Store pattern to avoid similar bugs
6. **Australian-Friendly**: Error messages in en-AU

## Common Pitfalls

❌ **Fixing without reproducing**
✅ **Reproduce reliably first**

❌ **Treating symptom not cause**
✅ **Identify and fix root cause**

❌ **No regression test**
✅ **Add test to prevent recurrence**

❌ **Introducing new bugs**
✅ **Run full test suite before committing**

❌ **Over-engineering the fix**
✅ **Minimal, targeted fix**

❌ **Forgetting Australian context**
✅ **Verify en-AU, DD/MM/YYYY, AUD throughout**

## Integration with Memory

```python
async def fix_bug(agent, bug_report):
    # Check for similar past bugs
    similar = await agent.memory.find_similar(
        query=bug_report.description,
        domain=MemoryDomain.TESTING,
        category="failure_patterns"
    )

    if similar:
        # Learn from past fixes
        past_fix = similar[0]
        logger.info(f"Similar bug fixed before: {past_fix}")

    # Proceed with fix
    fix_result = await agent.execute_fix(bug_report)

    # Store for future
    await agent.memory.store_failure(
        failure_type=fix_result.bug_category,
        context={
            "bug": bug_report.description,
            "root_cause": fix_result.root_cause,
            "fix_approach": fix_result.approach,
            "lessons": fix_result.lessons,
            "australian_context": fix_result.au_context_impact
        }
    )
```

---

**Goal**: Fix bugs systematically with tests, prevent regressions, and maintain Australian context.
