---
name: regression-test-generator
description: Generate regression tests when bugs are discovered during /debug or continuous checks. Auto-detects test framework, creates Arrange-Act-Assert tests, and links to error-log.md entries. (project)
---

<objective>
Automatically generate regression tests that capture bugs to prevent recurrence. Creates complete, framework-appropriate tests that:
1. Reproduce the bug scenario (fails before fix)
2. Verify correct behavior (passes after fix)
3. Link back to error-log.md for traceability
</objective>

<quick_start>
Generate regression test for a bug:

1. Collect bug details: error ID, symptoms, root cause, affected component
2. Detect test framework from project (Jest, Vitest, pytest, Playwright)
3. Generate test file following project patterns
4. Present to user for review: [A] Save [B] Edit [C] Skip
5. Save test to `tests/regression/` and update error-log.md

**Key principle**: Tests should FAIL before the fix is applied (proves bug exists).
</quick_start>

<prerequisites>
Before generating regression test:
- Bug has been identified with symptoms and reproduction steps
- Root cause determined (from 5 Whys or debugging)
- Component/file affected is known
- Error ID assigned (ERR-XXXX) or will be assigned

Check error-log.md to avoid duplicate tests for same error.
</prerequisites>

<workflow>
<step number="1">
**Collect bug details**

Extract from debug context:
- **Error ID**: ERR-XXXX from error-log.md (or generate new)
- **Title**: Brief description (e.g., "Dashboard timeout due to missing pagination")
- **Symptoms**: Observable behavior (error message, incorrect output)
- **Root cause**: Why the bug occurred (from 5 Whys analysis)
- **Component**: Affected file/function (e.g., `StudentProgressService.fetchExternalData`)
- **Reproduction steps**: How to trigger the bug

Example:

```yaml
error_id: ERR-0042
title: Dashboard timeout due to missing pagination
symptoms: Dashboard fails to load, timeout after 30s
root_cause: Missing pagination parameter causes over-fetching
component: src/services/StudentProgressService.ts:fetchExternalData
reproduction:
  - Navigate to /dashboard/student/123
  - Click "Load Data" button
  - Observe timeout error
```
</step>

<step number="2">
**Detect test framework**

Check project configuration (in priority order):

1. **docs/project/tech-stack.md** (if exists):
   ```bash
   grep -i "test\|jest\|vitest\|pytest\|playwright" docs/project/tech-stack.md
   ```

2. **package.json** (JavaScript/TypeScript):
   ```bash
   # Check devDependencies
   grep -E '"(jest|vitest|@playwright/test|mocha)"' package.json
   ```

3. **pyproject.toml / requirements.txt** (Python):
   ```bash
   grep -E "(pytest|unittest|nose)" pyproject.toml requirements.txt
   ```

4. **Existing test file patterns**:
   ```bash
   # JavaScript patterns
   find . -name "*.test.ts" -o -name "*.spec.ts" | head -1

   # Python patterns
   find . -name "*_test.py" -o -name "test_*.py" | head -1
   ```

5. **Defaults**:
   - JavaScript/TypeScript: Jest
   - Python: pytest
   - Document assumption in test file comment

**Output**: Framework name and test file extension (e.g., Jest → `.test.ts`)
</step>

<step number="3">
**Determine test file location**

Find appropriate location:

1. Check if `tests/regression/` exists → use it
2. Check project test structure:
   - `tests/` directory → `tests/regression/`
   - `__tests__/` directory → `__tests__/regression/`
   - Co-located tests (same dir as source) → `src/__tests__/regression/`
3. Create `tests/regression/` if no pattern found

**File naming**:
- Format: `regression-ERR-{ID}-{slug}.{ext}`
- Slug: lowercase kebab-case from title
- Examples:
  - `regression-ERR-0042-dashboard-timeout.test.ts`
  - `test_regression_err_0042_dashboard_timeout.py`
</step>

<step number="4">
**Generate test code**

Use framework-appropriate template from references/framework-templates.md.

**Structure (Arrange-Act-Assert)**:

```
Header: Error ID, title, description, root cause, link to error-log

describe/class: "Regression: ERR-XXXX - {title_short}"
  test: "should {expected} when {condition}"
    ARRANGE: Set up bug scenario (data, mocks, state)
    ACT: Execute action that caused bug
    ASSERT: Verify correct behavior (would have failed before fix)
```

**Required elements**:
- Error ID reference in comment header
- Link to error-log.md entry
- Clear test name describing expected behavior
- Setup code matching reproduction steps
- Assertion that validates the fix

See references/framework-templates.md for complete templates.
</step>

<step number="5">
**Present to user for review**

Display generated test:

```
=== Regression Test Generated ===

Error: ERR-0042 - Dashboard Timeout Due to Missing Pagination

File: tests/regression/regression-ERR-0042-dashboard-timeout.test.ts

--- Generated Test Code ---
[Full test code here]
---

This test will:
- {describe what test validates}
- {explain why test would have failed before fix}

What would you like to do?
  [A] Save test and continue
  [B] Edit test before saving
  [C] Skip generation (add to debt tracker)

>
```

**If user chooses**:
- **A (Save)**: Write file, run test, update error-log.md
- **B (Edit)**: Show edit instructions, wait for confirmation
- **C (Skip)**: Log skip reason in NOTES.md as technical debt
</step>

<step number="6">
**Save and verify**

After user approval:

1. **Write test file** to determined location
2. **Run test** to verify:
   - If bug not yet fixed: Test should FAIL (proves bug exists)
   - If bug already fixed: Test should PASS (validates fix)
3. **Update error-log.md** with regression test reference:

```markdown
**Regression Test**:
- **File**: `tests/regression/regression-ERR-0042-dashboard-timeout.test.ts`
- **Status**: Generated
- **Validates**: Pagination parameter prevents timeout
```

4. **Stage file** for commit (do not auto-commit)

**Validation**: Test file exists, runs without syntax errors, linked in error-log.md.
</step>
</workflow>

<validation>
After generating regression test, verify:

- Test file created in correct location
- Test follows project naming conventions
- Test uses Arrange-Act-Assert pattern
- Test has clear name describing expected behavior
- Error ID referenced in test header comment
- error-log.md updated with test reference
- Test runs without syntax errors
- Test behavior matches expectations (fails before fix OR passes after)
</validation>

<anti_patterns>
<pitfall name="implementation_testing">
**Don't**: Test implementation details

```javascript
// BAD: Tests internal method name
test('calls _fetchWithPagination', () => {
  expect(service._fetchWithPagination).toHaveBeenCalled();
});
```

**Do**: Test observable behavior

```javascript
// GOOD: Tests behavior user expects
test('should return paginated results within 5 seconds', async () => {
  const result = await service.fetchData(studentId);
  expect(result.length).toBeLessThanOrEqual(10);
});
```

**Why**: Implementation can change; behavior should remain stable.
</pitfall>

<pitfall name="brittle_selectors">
**Don't**: Use fragile DOM selectors

```javascript
// BAD: Breaks if CSS class changes
await page.locator('.btn-primary-xl-dashboard').click();
```

**Do**: Use accessible selectors

```javascript
// GOOD: Stable, user-focused
await page.getByRole('button', { name: 'Load Data' }).click();
```

**Why**: Regression tests should be stable across refactors.
</pitfall>

<pitfall name="no_error_link">
**Don't**: Create test without linking to error

```javascript
// BAD: No reference to error-log.md
test('dashboard loads', () => { /* ... */ });
```

**Do**: Include error ID and link

```javascript
/**
 * Regression Test for ERR-0042
 * @see specs/my-feature/error-log.md#ERR-0042
 */
test('should load dashboard within 5s (ERR-0042)', () => { /* ... */ });
```

**Why**: Traceability enables understanding why test exists.
</pitfall>

<pitfall name="testing_wrong_layer">
**Don't**: Write E2E test for unit-level bug

**Do**: Match test type to bug scope:
- Logic error in function → Unit test
- Integration failure → Integration test
- User flow broken → E2E test

**Why**: Faster feedback, more stable tests, easier maintenance.
</pitfall>
</anti_patterns>

<best_practices>
<practice name="behavior_focused_names">
Write test names that describe expected behavior:

- Format: `should {expected} when {condition}`
- Examples:
  - `should return paginated results when dataset exceeds 100 records`
  - `should complete within 5 seconds when loading dashboard`
  - `should show error message when API returns 500`

Result: Test serves as documentation, failures are self-explanatory.
</practice>

<practice name="minimal_reproduction">
Include only setup necessary to reproduce bug:

```javascript
// Include: State that triggers bug
const service = new StudentProgressService();
const result = await service.fetchData(studentWithLargeDataset);

// Exclude: Unrelated setup
// const userPrefs = loadPreferences(); // Not needed for this test
```

Result: Faster tests, clearer intent, easier maintenance.
</practice>

<practice name="assert_specific">
Make assertions specific to the bug:

```javascript
// BAD: Vague assertion
expect(result).toBeTruthy();

// GOOD: Specific to bug being prevented
expect(result.length).toBeLessThanOrEqual(10); // Pagination limit
expect(response.time).toBeLessThan(5000); // No timeout
```

Result: Test catches regressions, not false positives.
</practice>

<practice name="document_context">
Include context in test file header:

```javascript
/**
 * Regression Test for ERR-0042: Dashboard Timeout
 *
 * Bug: Dashboard failed to load due to missing pagination
 * Root Cause: API call fetched all records (1000+) instead of paginated (10)
 * Fixed: Added page_size parameter to API call
 *
 * @see specs/001-dashboard/error-log.md#ERR-0042
 */
```

Result: Future developers understand why test exists.
</practice>
</best_practices>

<success_criteria>
Regression test generation complete when:

- [ ] Bug details collected (error ID, symptoms, root cause, component)
- [ ] Test framework detected from project
- [ ] Test file location determined (follows project patterns)
- [ ] Test code generated with Arrange-Act-Assert structure
- [ ] Test presented to user for review
- [ ] User approved (A) or edited (B) test
- [ ] Test file written to correct location
- [ ] Test runs without syntax errors
- [ ] error-log.md updated with regression test reference
- [ ] Test file staged for commit
</success_criteria>

<quality_standards>
**Good regression test**:

- Clear name describing expected behavior
- Error ID in test name or comment
- Link to error-log.md entry
- Minimal setup (only what's needed to reproduce)
- Specific assertion (fails if bug reoccurs)
- Uses accessible selectors (E2E tests)
- Follows project test patterns

**Bad regression test**:

- Generic name (`test1`, `dashboard test`)
- No error reference (no traceability)
- Tests implementation details
- Brittle selectors or timing-dependent
- Vague assertions (`toBeTruthy`)
- Doesn't actually catch the bug if reintroduced
</quality_standards>

<troubleshooting>
**Issue**: Can't detect test framework
**Solution**: Check package.json, pyproject.toml manually; ask user to specify

**Issue**: No existing test directory
**Solution**: Create `tests/regression/` and document in test file comment

**Issue**: Test passes before fix applied
**Solution**: Test may not be reproducing bug correctly; review reproduction steps

**Issue**: Test fails after fix applied
**Solution**: Assertion may be testing wrong behavior; adjust to match expected post-fix state

**Issue**: User skips too many regression tests
**Solution**: Track in NOTES.md as tech debt; surface during /optimize phase
</troubleshooting>

<references>
See references/ for:
- Framework templates (Jest, Vitest, pytest, Playwright)
- Test location strategies (monorepo, co-located, centralized)
- Example regression tests (good vs bad patterns)
- Integration with error-log.md
</references>
