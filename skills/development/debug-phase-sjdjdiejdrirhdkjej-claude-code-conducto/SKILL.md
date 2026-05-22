---
name: debug-phase
description: Systematic debugging techniques including error classification, root cause analysis (5 Whys), reproduction strategies, and error documentation. Use when debugging errors, investigating failures, analyzing stack traces, fixing bugs, or documenting errors in error-log.md. (project)
---

<objective>
Provide systematic debugging techniques for error investigation, root cause analysis, and fix implementation. Ensures errors are properly classified, root causes identified (not symptoms), and solutions documented to prevent recurrence.
</objective>

<quick_start>
Debug errors systematically:

1. Reproduce error consistently (100% reliable reproduction)
2. Classify by type (syntax/runtime/logic/integration/performance) and severity (critical/high/medium/low)
3. Isolate root cause using binary search, logging, breakpoints, or 5 Whys
4. Implement fix with failing test first (TDD)
5. Add regression tests to prevent recurrence
6. Document in error-log.md with ERR-XXXX ID

**Key principle**: Fix root causes, not symptoms. Use 5 Whys to drill down.
</quick_start>

<prerequisites>
Before debugging:
- Error can be reproduced (even if intermittent, identify conditions)
- Logs available (application logs, stack traces, network logs)
- Development environment set up for testing

Check error-log.md for similar historical errors before starting.
</prerequisites>

<workflow>
<step number="1">
**Search for similar errors**

Check error-log.md for past occurrences:

```bash
# Search by error message
grep -i "connection timeout" error-log.md

# Search by component
grep "Component: StudentProgressService" error-log.md

# Search by error type
grep "Type: Integration" error-log.md
```

If similar error found:

- Review previous fix (workaround or root cause?)
- Check if error recurred (>2 occurrences = need permanent fix)
- Note patterns (same component, same conditions, timing)

**If recurring error**: Prioritize permanent fix over workaround.
</step>

<step number="2">
**Reproduce error consistently**

Create minimal reproduction:

1. Gather context: error message, stack trace, timestamp, user actions, environment
2. Create minimal test case that triggers error 100% of time
3. If intermittent: identify conditions (timing, data state, race conditions)

Example reproduction:

```bash
# API error
curl -X POST http://localhost:3000/api/endpoint \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'

# Frontend error
# 1. Navigate to /dashboard
# 2. Click "Load Data" button
# 3. Error appears in console
```

**Validation**: Can trigger error reliably before proceeding.
</step>

<step number="3">
**Classify error**

**By type**:

- **Syntax**: Code doesn't compile/parse (typos, missing brackets, linting errors)
- **Runtime**: Code runs but crashes (null pointer, type error, uncaught exception)
- **Logic**: Code runs but wrong result (calculation error, wrong branch taken)
- **Integration**: External dependency fails (API timeout, database connection, service unavailable)
- **Performance**: Code works but too slow (timeout, memory leak, N+1 queries)

**By severity**:

- **Critical**: Data loss, security breach, total system failure
- **High**: Feature broken, blocks users from core functionality
- **Medium**: Feature degraded, workaround exists
- **Low**: Minor UX issue, cosmetic, no functional impact

Example classification:

```markdown
Type: Integration (API call to external service fails)
Severity: High (dashboard doesn't load, blocks teachers)
Component: StudentProgressService.fetchExternalData()
Frequency: 30% of requests (intermittent)
```

See references/error-classification.md for detailed matrix.
</step>

<step number="4">
**Isolate root cause**

Use systematic techniques:

**Binary search** (for large codebases):

- Add logging at midpoint of suspected code
- If error before midpoint → investigate first half
- If error after midpoint → investigate second half
- Repeat until narrowed to specific function

**Increase logging**:

```python
# Add debug logs around suspected area
logger.debug(f"Before API call: student_id={student_id}, params={params}")
response = api.fetch_data(student_id)
logger.debug(f"After API call: status={response.status}, data_len={len(response.data)}")
```

**Use breakpoints** (interactive debugging):

```bash
# Python
python -m pdb script.py

# Node.js
node inspect server.js

# Browser (Chrome DevTools)
# Set breakpoints, inspect variables, step through code
```

**Check assumptions**:

- Is variable the value you expect? (log it, don't assume)
- Is function being called when you expect? (add entry/exit logs)
- Are external dependencies available? (health check endpoints)

**Apply 5 Whys** (drill down to root cause):

```markdown
1. Why did dashboard fail to load?
   → API call to external service timed out

2. Why did API call timeout?
   → Request took >30 seconds (timeout limit)

3. Why did request take >30 seconds?
   → External service response time was 45 seconds

4. Why was external service so slow?
   → Requesting too much data (1000 records instead of 10)

5. Why requesting 1000 records?
   → Missing pagination parameter in API call

Root cause: Missing pagination parameter causes over-fetching
```

**Validation**: Root cause identified (not just symptoms). Can explain why error occurred.
</step>

<step number="5">
**Implement fix (TDD approach)**

1. Write failing test first:

```python
def test_fetch_external_data_with_pagination():
    """Test that API call includes pagination parameter"""
    service = StudentProgressService()
    result = service.fetchExternalData(student_id=123)

    assert len(result) <= 10  # Max 10 records per page
    assert result.has_next_page  # Pagination metadata present
```

2. Implement fix:

```python
# Before (broken)
def fetchExternalData(self, student_id):
    return api.get(f"/students/{student_id}/data")

# After (fixed)
def fetchExternalData(self, student_id, page_size=10):
    return api.get(
        f"/students/{student_id}/data",
        params={"page_size": page_size}
    )
```

3. Verify fix:

```bash
# Run test (should pass)
pytest tests/test_student_progress_service.py

# Manually test reproduction steps (error should not occur)
```

**Validation**: Fix addresses root cause, all tests pass, error no longer reproduces.
</step>

<step number="6">
**Add regression tests**

Prevent recurrence:

```python
# Unit test for specific bug
def test_pagination_parameter_included():
    """Regression test for ERR-0042: Missing pagination"""
    service = StudentProgressService()
    with patch('api.get') as mock_get:
        service.fetchExternalData(student_id=123)

        # Verify pagination param passed
        mock_get.assert_called_with(
            '/students/123/data',
            params={'page_size': 10}
        )

# Integration test for user flow
def test_dashboard_loads_with_large_datasets():
    """Ensure dashboard handles large datasets without timeout"""
    client = TestClient()
    response = client.get('/dashboard/student/123')

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 5  # No timeout
```

**Validation**: Tests added covering error scenario, tests pass consistently.
</step>

<step number="7">
**Document in error-log.md**

Create entry with ERR-XXXX ID:

```markdown
## ERR-0042: Dashboard Timeout Due to Missing Pagination

**Date**: 2025-11-19
**Severity**: High
**Type**: Integration
**Component**: StudentProgressService.fetchExternalData()
**Reporter**: QA team (staging environment)

### Error Description

Dashboard fails to load student progress data, showing timeout error after 30 seconds.

### Root Cause

API call to external service was missing pagination parameter, causing over-fetching of 1000+ records instead of paginated 10 records. External service took 45 seconds to respond with large dataset, exceeding 30-second client timeout.

### 5 Whys Analysis

1. Dashboard timeout → API call timeout
2. API timeout → Request took >30s
3. > 30s request → External service slow (45s)
4. Service slow → Too much data (1000 records)
5. Too much data → Missing pagination parameter

**Root cause**: Missing pagination parameter in API call

### Fix Implemented

- Added `page_size` parameter (default 10) to `fetchExternalData()`
- Modified API call to include pagination params
- Response time reduced from 45s → 2s

### Files Changed

- `src/services/StudentProgressService.ts` (lines 45-52)
- `tests/StudentProgressService.test.ts` (added regression test)

### Prevention

- Unit test: Verify pagination parameter included
- Integration test: Dashboard loads within 5s with large datasets
- Added performance monitoring alert if response time >10s

### Related Errors

- Similar to ERR-0015 (pagination missing in different service)
- Pattern: Always include pagination for external API calls
```

See references/error-log-template.md for full template.

**Validation**: error-log.md updated with complete entry, ERR-XXXX ID assigned.
</step>

<step number="8">
**Verify and close**

Final checks:

```bash
# Error no longer reproduces
# (run original reproduction steps)

# All tests pass
npm test  # or pytest, cargo test, etc.

# Logs confirm fix
# Check application logs for success

# No regressions introduced
# Run full test suite
```

Update state.yaml (if debugging during a phase):

```yaml
debug:
  status: completed
  error_id: ERR-0042
  root_cause: Missing pagination parameter
  tests_added: 2
```

**Validation**: Error resolved, documented, tests added, no regressions.
</step>
</workflow>

<validation>
After debugging, verify:

- Error reproduces consistently before fix (validated reproduction)
- Root cause identified using 5 Whys or systematic technique
- Fix addresses root cause, not symptoms
- Failing test written first (TDD approach)
- All tests pass after fix
- Regression tests added to prevent recurrence
- Error documented in error-log.md with ERR-XXXX ID
- No new errors introduced (full test suite passes)
  </validation>

<anti_patterns>
<pitfall name="symptom_fixing">
**❌ Don't**: Fix symptoms without finding root cause

- Adding try/catch to hide error
- Increasing timeout without investigating why slow
- Restarting service to "fix" memory leak

**✅ Do**: Use 5 Whys to drill down to root cause, fix underlying issue

**Why**: Symptom fixes lead to recurring errors, technical debt, unreliable system

**Example** (bad):

```python
# Symptom fix: Hide error with try/catch
try:
    data = api.fetch(student_id)
except TimeoutError:
    return []  # Return empty, ignore error
```

**Example** (good):

```python
# Root cause fix: Add pagination to prevent timeout
data = api.fetch(student_id, page_size=10)  # Paginate to reduce data
```

</pitfall>

<pitfall name="trial_and_error">
**❌ Don't**: Random changes hoping to fix issue
- Change multiple things at once
- No hypothesis about what's wrong
- No reproduction validation

**✅ Do**: Form hypothesis, change one thing, test, validate

**Why**: Can't identify what actually fixed it, might introduce new bugs

**Example** (bad workflow):

```
1. Change timeout from 30s to 60s
2. Also add retry logic
3. Also increase memory limit
4. Error gone... which change fixed it? Unknown.
```

**Example** (good workflow):

```
1. Hypothesis: Timeout too short
2. Change only timeout: 30s → 60s
3. Test: Still fails
4. Hypothesis: Data too large
5. Add pagination only
6. Test: Works! Pagination was the fix.
```

</pitfall>

<pitfall name="no_documentation">
**❌ Don't**: Fix error and move on without documentation
**✅ Do**: Document in error-log.md with root cause, fix, prevention

**Why**: Same error may recur, team can't learn from past issues

**Required in error-log.md**:

- ERR-XXXX ID
- Root cause (5 Whys analysis)
- Fix implemented
- Tests added
- Related errors (if pattern exists)
  </pitfall>

<pitfall name="no_regression_tests">
**❌ Don't**: Fix bug without adding tests
**✅ Do**: Write failing test first (TDD), add regression test

**Why**: Bug may be reintroduced later, no safety net

**Example**:

```python
# After fixing ERR-0042, add:
def test_no_timeout_with_large_datasets():
    """Regression test for ERR-0042: Pagination prevents timeout"""
    # This test will catch if pagination is removed later
```

</pitfall>

<pitfall name="insufficient_reproduction">
**❌ Don't**: Start debugging without reliable reproduction
**✅ Do**: Achieve 100% reliable reproduction before investigating

**Why**: Can't validate fix if you can't trigger error consistently

**Intermittent errors**: Identify conditions (timing, data state, race conditions) to make reproducible
</pitfall>
</anti_patterns>

<best_practices>
<practice name="5_whys_analysis">
Always use 5 Whys to find root cause:

- Ask "Why?" 5 times to drill down
- Stop when you reach actionable root cause
- Document analysis in error-log.md

Example:

```markdown
1. Why? Dashboard timeout
2. Why? API call slow
3. Why? Large dataset
4. Why? Missing pagination
5. Why? Developer didn't add parameter

Root cause: Missing pagination parameter
Fix: Add pagination to API call
```

Result: Root cause identified, not symptoms
</practice>

<practice name="tdd_approach">
Write failing test first, then implement fix:

1. Write test that reproduces error (should fail)
2. Implement fix
3. Run test (should pass)
4. Add regression test

Result: Fix validated, regression prevented
</practice>

<practice name="binary_search_debugging">
For complex codebases, use binary search:

1. Add logging at midpoint of suspected code
2. Determine if error before or after midpoint
3. Narrow to half of code
4. Repeat until isolated to specific function

Result: Quickly narrow down error location in large codebase
</practice>

<practice name="comprehensive_documentation">
Document every error in error-log.md:
- ERR-XXXX ID for reference
- Root cause (5 Whys analysis)
- Fix implemented (files changed, approach)
- Tests added (regression prevention)
- Related errors (patterns)

Result: Team learns from past errors, patterns identified
</practice>
</best_practices>

<success_criteria>
Debugging complete when:

- [ ] Error reproduces consistently (100% reproduction or conditions identified)
- [ ] Error classified by type (syntax/runtime/logic/integration/performance) and severity (critical/high/medium/low)
- [ ] Root cause identified using 5 Whys or systematic technique (not symptoms)
- [ ] Fix implemented addressing root cause
- [ ] Failing test written first (TDD approach)
- [ ] All tests pass after fix
- [ ] Regression tests added to prevent recurrence
- [ ] error-log.md updated with ERR-XXXX ID, root cause, fix, tests
- [ ] Full test suite passes (no regressions introduced)
- [ ] Error no longer reproduces with original steps
      </success_criteria>

<quality_standards>
**Good debugging**:

- Root cause identified (5 Whys completed)
- Failing test written before fix (TDD)
- Regression tests added (≥1 per error)
- Comprehensive error-log.md entry (includes root cause, fix, tests)
- No symptom fixes (addresses underlying issue)

**Bad debugging**:

- Symptom fixes (try/catch to hide error, increase timeout without investigation)
- Trial and error (change multiple things, no hypothesis)
- No tests added (no regression prevention)
- No documentation (error-log.md not updated)
- Insufficient reproduction (can't trigger error reliably)
  </quality_standards>

<troubleshooting>
**Issue**: Can't reproduce error consistently
**Solution**: Identify conditions (timing, data state, environment), use logging to capture state when error occurs

**Issue**: 5 Whys leads to "developer mistake"
**Solution**: Keep asking why - why did developer make mistake? (unclear docs, missing validation, no tests?)

**Issue**: Fix works but not sure why
**Solution**: Add detailed logging before/after fix, compare behavior, validate hypothesis

**Issue**: Error recurs after fix
**Solution**: Check if root cause was correctly identified (use 5 Whys again), verify tests actually prevent recurrence

**Issue**: Too many errors to debug
**Solution**: Prioritize by severity (critical > high > medium > low), check for common root causes (same component, same pattern)
</troubleshooting>

<references>
See references/ for:
- Error classification matrix (type × severity decision table)
- Error log template (complete ERR-XXXX format)
- Debugging techniques (binary search, logging strategies, breakpoint usage)
- Common error patterns (pagination, null checks, race conditions)
- Example error investigations (good vs bad debugging workflows)
</references>
