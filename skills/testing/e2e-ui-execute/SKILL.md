---
name: e2e-ui-execute
description: Implement UI E2E tests sequentially using Playwright MCP, stop on bug discovery. Use after e2e-ui-research to implement the planned test scenarios.
context: fork
agent: general-purpose
---

# UI E2E Test Implementation Command

## User Input

```text
$ARGUMENTS
```

Extract test number (if specified) and consider any additional context from user input (if not empty).

---

## Overview

1. **Check Prerequisites**:
   - Verify `docs/e2e-ui/test-targets.md` exists (English version, for AI)
   - If not exists ERROR: "Please run /e2e-ui:research first"

2. **Read Project Configuration**:
   - Read `playwright.config.ts` (or `.js`):
     - Extract test directory from `testDir` or `testMatch`
     - Extract base URL from `webServer.url` or `use.baseURL`
   - Read `package.json` (in same directory):
     - Detect framework from dependencies: `next`, `react`, `vue`, `svelte`, etc.
   - **Fallback**: If playwright.config not found, ask user for test directory and base URL

3. **Load Test Targets**:
   - Read test scenarios from document
   - Extract test number from $ARGUMENTS (if provided)
   - Identify execution order

4. **Execute Tests Sequentially**:
   - For each test scenario (in order):
     a. **Manual Testing Phase**: Verify behavior with Playwright MCP
     b. **Bug Detection**: Check for issues
     c. **Bug Handling**: If bug found, create bilingual bug report (ko.md + md) and continue
     d. **Code Writing Phase**: Write Playwright test code if passed (skip if bug)
     e. **Progress Reporting**: Update summary document

5. **Generate Documentation**:
   - Create `docs/e2e-ui/summary-test-N.md` for each completed test
   - Create `docs/e2e-ui/bug-report-test-N.ko.md` and `bug-report-test-N.md` for bugs
   - Track overall progress

6. **Report Results**:
   - List of completed tests
   - List of bugs found (with details)
   - Summary of test code created
   - Guide next steps

---

## Key Rules

### 🚨 Bug Detection (Important)

**Document and continue when these situations occur**:

1. **Page Load Failure**:
   - Navigation timeout
   - 404/500 errors
   - Blank page

2. **Element Not Found**:
   - Expected button/input missing
   - Wrong element attributes
   - Wrong page structure

3. **Interaction Failure**:
   - Click not working
   - Input text not entering
   - Form submission failure

4. **Console Errors**:
   - JavaScript errors
   - Network failures (except expected ones)
   - React errors/warnings

5. **Unexpected Behavior**:
   - Wrong navigation
   - Wrong data display
   - Missing UI elements
   - Broken functionality

**Bug Report Format** (create both ko.md and md versions):

Files to create:

- `docs/e2e-ui/bug-report-test-N.ko.md` (Korean)
- `docs/e2e-ui/bug-report-test-N.md` (English)

```markdown
## 🐛 Bug Found

**Test**: [Test N: name]
**Priority**: [Critical/High/Medium]

**What Was Being Tested**:
[description]

**Reproduction Steps**:

1. [step 1]
2. [step 2]
3. [bug occurs here]

**Expected Behavior**:
[what should happen]

**Actual Behavior**:
[what actually happened]

**Evidence**:

- Screenshot: [path]
- Console Errors: [if any]
- Page State: [snapshot info]

**Impact**:
[impact on users]
```

After creating bug report, **continue to next test** instead of stopping.

### ✅ MUST DO

- **Read `playwright.config.ts` and `package.json` first** to get project configuration
  - playwright.config.ts: test directory, base URL, test settings
  - package.json: framework detection
- Run tests **one at a time** (sequentially)
- Use Playwright MCP for **actual testing** before code writing
- **Create bilingual bug reports** (ko.md + md) when bugs found
- **Continue testing** after documenting bugs
- Write test code in **directory from playwright.config.ts** (testDir or testMatch)
- Write clean and maintainable test code
- Follow TypeScript and testing coding standards
- Generate summary for each test
- Take screenshots for evidence

### ❌ NEVER DO

- **Skip reading `playwright.config.ts`** (it's the primary source of truth)
- Run multiple tests in parallel
- Skip manual verification phase
- **Stop testing after finding bug** (should continue)
- Write test code without verifying behavior
- Create single-language bug reports (must be bilingual)
- Write test code outside directory specified in playwright.config
- Hardcode base URLs or test directories
- Ignore console errors or warnings
- Skip edge cases

### 🎯 Test Implementation Process

For each test:

1. **Manual Verification** (using Playwright MCP):

   ```
   - Navigate to page
   - Interact with UI elements
   - Take snapshots
   - Verify expected behavior
   - Check console messages
   ```

2. **Bug Check**:
   - Did everything work as expected?
   - Any errors or warnings?
   - Is behavior correct?

3. **Decision Point**:
   - ✅ **If Pass**: Proceed to write test code
   - 🐛 **If Bug Found**: Create bilingual bug report, continue to next test

4. **Write Test Code** (only if passed):

   ```typescript
   // Create test file in directory from playwright.config.ts (testDir or testMatch)
   // Follow project test patterns
   // Include assertions and error handling
   // Follow naming convention from testMatch pattern (e.g., *.spec.ts, *.e2e.ts)
   ```

5. **Documentation**:
   - Generate summary document
   - Record what was tested
   - Note observations

---

## Document Template

File to create: `docs/e2e-ui/summary-test-N.md`

````markdown
# Test N: [scenario name]

> **Created**: [YYYY-MM-DD HH:mm]
> **Related Plan**: `test-targets.md` > Test N
> **Status**: ✅ Pass / 🐛 Bug Found

---

## 🎯 Test Objective

[what this test verifies]

---

## 🧪 Manual Verification Results

**Test Steps Performed**:

1. [step 1] - ✅ Success
2. [step 2] - ✅ Success
3. [step 3] - ✅ Success

**Screenshots**:

- [screenshot 1]: `path/to/screenshot1.png`
- [screenshot 2]: `path/to/screenshot2.png`

**Console Output**:

- [relevant console messages]

**Observations**:

- [interesting findings]

---

## 📝 Generated Test Code

**File**: `[path/to/test/file.spec.ts]`

**Main Assertions**:

- [assertion 1]
- [assertion 2]

**Code Structure**:

```typescript
// Brief overview of test structure
test("scenario name", async ({ page }) => {
  // test steps
});
```
````

---

## ✅ Verification

**Test Execution**:

- Manual verification: ✅ Pass
- Code implementation: ✅ Complete
- Test successfully run: [✅ / Not yet run]

**Edge Cases Tested**:

- [edge case 1]: [result]
- [edge case 2]: [result]

---

## 📊 Coverage

**What This Test Covers**:

- [feature 1]
- [user flow 2]

**What It Doesn't Cover** (future):

- [out of scope items]

---

## 🔑 Technical Notes

- [technical decisions made]
- [workarounds if needed]
- [dependencies or setup required]

````

---

## Bug Report Template

**Create bilingual bug reports when bug found**:

Files to create:
- `docs/e2e-ui/bug-report-test-N.ko.md` (Korean version)
- `docs/e2e-ui/bug-report-test-N.md` (English version)

### Korean Version Template

```markdown
# 🐛 버그 리포트: Test N

> **발견일시**: [YYYY-MM-DD HH:mm]
> **테스트**: Test N: [시나리오 이름]
> **우선순위**: [Critical/High/Medium]

---

## 📋 버그 요약

[버그에 대한 한 문장 설명]

---

## 🔍 상세 내용

**테스트 대상**:
[테스트 시나리오 설명]

**재현 단계**:

1. [단계 1]
2. [단계 2]
3. [버그 발생 지점]

**예상 동작**:
[기대했던 동작]

**실제 동작**:
[실제 발생한 동작]

---

## 📸 증거

**스크린샷**:
- [스크린샷 1]: `path/to/screenshot.png`

**콘솔 에러**:
````

[콘솔 에러 메시지 붙여넣기]

````

**페이지 상태**:
```yaml
[페이지 스냅샷 또는 관련 HTML]
````

---

## 💥 영향도

**사용자 영향**:
[최종 사용자에게 미치는 영향]

**심각도**:
[이 우선순위 레벨인 이유]

---

## 🔄 다음 단계

1. 사용자가 버그 리포트 검토
2. 개발자가 버그 수정
3. 수정 후 `/e2e-ui:execute N`으로 이 테스트부터 재개 가능

````

### English Version Template

```markdown
# 🐛 Bug Report: Test N

> **Discovered**: [YYYY-MM-DD HH:mm]
> **Test**: Test N: [scenario name]
> **Priority**: [Critical/High/Medium]

---

## 📋 Bug Summary

[one sentence description of bug]

---

## 🔍 Details

**What Was Being Tested**:
[test scenario description]

**Reproduction Steps**:

1. [step 1]
2. [step 2]
3. [bug occurs here]

**Expected Behavior**:
[what should happen]

**Actual Behavior**:
[what actually happened]

---

## 📸 Evidence

**Screenshots**:
- [screenshot 1]: `path/to/screenshot.png`

**Console Errors**:
````

[paste console error messages]

````

**Page State**:
```yaml
[page snapshot or relevant HTML]
````

---

## 💥 Impact

**User Impact**:
[impact on end users]

**Severity**:
[why this priority level]

---

## 🔄 Next Steps

1. User reviews this bug report
2. Developer fixes the bug
3. After fix, resume: `/e2e-ui:execute N` to continue from this test

```

**Important**: After creating bug report, continue to next test instead of stopping.

---

## Execution Flow

### Initialization
1. **Read project configuration files**:
   - `playwright.config.ts`: Extract test directory, base URL, naming convention from testMatch
   - `package.json`: Detect framework from dependencies (next, react, vue, etc.)
   - **Fallback**: If config not found, ask user for test directory and base URL
2. Load test targets document (docs/e2e-ui/test-targets.md - English version, for AI)
3. Determine which tests to run
4. Check existing summaries (resume capability)

### For Each Test
1. **Announce**: "Starting Test N: [name]"
2. **Manual Testing**:
   - Use Playwright MCP tools
   - Navigate, interact, verify
   - Take screenshots
   - Check console
3. **Evaluate**:
   - Is behavior correct?
   - Any errors?
4. **Decide**:
   - If bug: Generate bilingual bug report (ko.md + md), continue to next
   - If pass: Continue to code writing
5. **Write Code** (only if passed):
   - Create test file in directory from playwright.config.ts
   - Implement test logic
   - Follow coding standards
   - Follow naming convention from testMatch pattern
6. **Document**:
   - Generate summary (if passed)
   - Generate bug report (if bug found)
   - Record findings
7. **Progress**: "Test N complete. Moving to Test N+1..."

### Completion
- Provide comprehensive summary:
  - List of tests passed with generated code
  - List of bugs found with report links
  - Overall coverage achieved
  - Recommendations for next steps

---

## Execute

Start working according to the guidelines above.
```
