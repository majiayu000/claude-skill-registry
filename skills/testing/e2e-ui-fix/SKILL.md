---
name: e2e-ui-fix
description: Fix bugs from e2e-ui-execute bug reports with Playwright MCP verification. Use after discovering bugs during E2E test execution.
context: fork
agent: general-purpose
---

# UI E2E Bug Fix Command

## User Input

```text
$ARGUMENTS
```

Extract test number (required) from arguments. Example: `/e2e-ui:fix 3` to fix bug from Test 3.

---

## Overview

This command implements a systematic bug fix workflow for bugs discovered during E2E testing:

1. **Load Bug Report**: Read bug report from docs/e2e-ui/bug-report-test-N.md (English version, for AI)
2. **Reproduce Bug**: Verify bug exists using Playwright MCP
3. **Analyze Root Cause**: Use Grep, Read, Playwright MCP for analysis
4. **Implement Fix**: Fix the underlying issue following coding principles
5. **Verify Fix**: Confirm bug resolved with Playwright MCP
6. **Write Test**: Create Playwright test to prevent regression
7. **Document**: Generate bilingual fix summary

---

## Prerequisites

- ✅ Bug report exists: `docs/e2e-ui/bug-report-test-N.md` (English version required)
- ✅ Playwright MCP server must be running
- ✅ Frontend server must be running

---

## Execution Workflow

### Step 1: Preparation

**Load Bug Report** (English version only, for AI):

- Read `docs/e2e-ui/bug-report-test-N.md` (English, for AI - NOT ko.md)
- Extract:
  - Reproduction steps
  - Expected vs actual behavior
  - Screenshots/evidence paths
  - Console errors
  - Priority level

**Read Project Configuration**:

- Read `playwright.config.ts` (or `.js`):
  - Extract base URL from `webServer.url` or `use.baseURL`
  - Extract test directory from `testDir` or `testMatch`
- Read `package.json` (in same directory):
  - Detect framework from dependencies: `next`, `react`, `vue`, etc.
- **Fallback**: If config not found, ask user for base URL and test directory

**Error Check**:

- If bug report not found → ERROR: "Bug report for Test N not found. Please run `/e2e-ui:execute N` first to discover bugs."

### Step 2: Bug Reproduction

**Use Playwright MCP to reproduce bug**:

```javascript
// Follow exact steps from bug report
browser_navigate: {base URL + route}
browser_type: {input selector, value}
browser_click: {button selector}
browser_snapshot: {capture state}
browser_take_screenshot: {evidence}
```

**Verify bug exists**:

- Follow reproduction steps exactly
- Compare actual behavior with expected behavior
- Take screenshots for before-fix evidence
- Capture console errors
- Document current state

**If bug cannot be reproduced**:

- Note in summary that bug may be already fixed
- Ask user if they want to continue or skip
- Update bug report status

### Step 3: Root Cause Analysis

**Analysis Steps**:

1. **Extract Error Details from Reproduction**:
   - Error messages from console output
   - Failed assertions or unexpected behavior
   - DOM state inconsistencies from snapshots

2. **Identify Related Components** (use Grep):
   - `Grep` to find components, handlers, or functions related to bug
   - Search for error messages in codebase
   - Identify files mentioned in stack traces
   - Locate UI components involved in the flow

3. **Read Source Files** (targeted reading):
   - `Read` relevant source files identified by Grep
   - Use offset/limit for large files (only read necessary sections)
   - Focus on code paths involved in reproduction steps
   - Check state management logic
   - Review event handlers
   - Examine API calls (if applicable)

4. **Find Root Cause**:
   - JavaScript errors → code bugs (logic errors, typos, wrong API usage)
   - Missing elements → component rendering issues (conditional rendering bugs)
   - Wrong behavior → logic errors (incorrect calculations, state bugs)
   - Network failures → API integration issues (wrong endpoints, data format)

**Tools to use**:

- `Grep`: Find relevant code patterns and files
- `Read`: Examine source files (use offset/limit for efficiency)
- Playwright MCP: Verify assumptions about behavior

**Document Findings**:

- Record root cause
- Note affected files with line numbers
- Identify fix approach

### Step 4: Fix Implementation

**Implement Fix**:

- Make minimal, focused changes
- **Strictly follow** coding principles
- Follow project coding standards
- Consider edge cases
- Add defensive checks if needed

**Fix Types**:

1. **UI Component Bugs**:
   - Fix rendering logic
   - Correct conditional rendering
   - Fix CSS/styling issues

2. **Logic Errors**:
   - Fix calculation errors
   - Correct validation logic
   - Fix state management

3. **Integration Issues**:
   - Fix API calls
   - Correct data transformations
   - Fix error handling

**Quality Checks**:

- Ensure fix doesn't break other features
- Check for similar issues elsewhere
- Review code quality

### Step 5: Fix Verification

**Use Playwright MCP to verify fix**:

```javascript
// Repeat reproduction steps
browser_navigate: {base URL + route}
browser_type: {input selector, value}
browser_click: {button selector}
browser_snapshot: {capture fixed state}
browser_take_screenshot: {after-fix evidence}
```

**Verify Expected Behavior**:

- Follow original test steps
- Confirm expected behavior now works
- Check no console errors
- Take screenshots for after-fix evidence
- Test edge cases

**If fix verification fails**:

- Return to Step 3 (Analysis)
- Document what didn't work
- Adjust fix approach

### Step 6: Write Regression Test

**Create Playwright Test** (only after fix verified):

**File Location**: Use directory from `playwright.config.ts` (testDir or testMatch)

**File Naming**: Follow project pattern from testMatch (e.g., `*.spec.ts`, `*.e2e.ts`)

**Test Structure**:

```typescript
import { test, expect } from "@playwright/test";

test.describe("Test N: {scenario name}", () => {
  test("should {expected behavior}", async ({ page }) => {
    // Navigate
    await page.goto("/route");

    // Perform actions from bug reproduction steps
    await page.fill('input[name="email"]', "test@example.com");
    await page.click('button[type="submit"]');

    // Assert expected behavior
    await expect(page.locator(".success-message")).toBeVisible();

    // Assert no errors
    // Additional assertions
  });

  // Edge case tests if needed
  test("should handle edge case", async ({ page }) => {
    // Edge case test
  });
});
```

**Test Quality**:

- Clear test description
- Follows AAA pattern (Arrange, Act, Assert)
- Includes error cases
- Has meaningful assertions
- Includes comments for clarity

### Step 7: Generate Documentation

**Create Bilingual Fix Summary**:

Files to create:

- `docs/e2e-ui/fix-summary-test-N.ko.md` (Korean)
- `docs/e2e-ui/fix-summary-test-N.md` (English)

**Update Bug Report Status**:

- Add "Fixed" status to bug report
- Link to fix summary
- Add fix date

---

## Key Rules

### ✅ MUST DO

- **Read `playwright.config.ts` and `package.json` first** for project configuration
- Read **English bug report only** (.md, NOT ko.md) - saves ~50% tokens
- **Reproduce bug first** before attempting fix
- **Strictly follow** coding principles when implementing fix
- Use Playwright MCP for verification (both before and after fix)
- Make minimal, focused fixes
- **Verify fix works** before writing test
- Write regression test in directory from playwright.config.ts
- Follow naming convention from testMatch pattern
- Create bilingual fix summary (ko.md + md)
- Take screenshots for evidence (before-fix, after-fix)
- Document root cause and solution

### ❌ NEVER DO

- **Skip reading `playwright.config.ts`** (primary source of truth)
- Read Korean bug report (ko.md) for AI analysis (waste of tokens - read .md only)
- Skip bug reproduction step
- Make fixes without understanding root cause
- Violate coding principles when editing code
- Write test code before verifying fix works
- Write tests outside directory specified in playwright.config
- Hardcode base URLs or test directories
- Make broad, sweeping changes
- Skip verification step
- Create single-language documentation
- Ignore edge cases in tests

### 🎯 Fix Quality Standards

**Good Fix**:

- Addresses root cause, not symptoms
- Minimal code changes
- Maintains code quality
- Doesn't break existing features
- Includes defensive checks
- Well-documented in code

**Good Test**:

- Reproduces original bug scenario
- Would fail before fix, pass after fix
- Tests edge cases
- Clear assertions
- Maintainable code

---

## Fix Summary Template

### Korean Version: `docs/e2e-ui/fix-summary-test-N.ko.md`

```markdown
# 버그 수정 요약: Test N

> **수정일시**: {YYYY-MM-DD HH:mm}
> **원본 버그 리포트**: [bug-report-test-N.ko.md](./bug-report-test-N.ko.md)
> **테스트 파일**: `{path/to/test.spec.ts}`

---

## 📋 버그 요약

**우선순위**: {Critical/High/Medium}

**원본 이슈**: {버그 한 줄 설명}

---

## 🔍 재현 결과

**재현 성공 여부**: ✅ 재현됨 / ❌ 재현 안됨

**재현 단계**:

1. {단계 1}
2. {단계 2}
3. {버그 발생 지점}

**수정 전 증거**:

- 스크린샷: `{path/to/before-fix-screenshot.png}`
- 콘솔 에러:
```

{콘솔 에러 메시지}

````

---

## 🔬 근본 원인 분석

**분석 방법**: {Manual Analysis / Agent: debugger / Agent: error-detective}

**근본 원인**:

{근본 원인 상세 설명}

**영향받은 파일**:

- `{file1}`: {어떤 문제}
- `{file2}`: {어떤 문제}

**원인 카테고리**: {UI Component / Logic Error / Integration Issue / etc}

---

## 🛠️ 수정 내용

**수정 접근법**: {접근 방식 설명}

**변경된 파일**:

- `{file1}`: {변경 내용}
- `{file2}`: {변경 내용}

**주요 변경사항**:

```typescript
// Before
{코드 변경 전}

// After
{코드 변경 후}
````

**수정 이유**: {왜 이렇게 수정했는지}

---

## ✅ 수정 검증

**검증 방법**: Playwright MCP 브라우저 테스트

**검증 단계**:

1. {검증 단계 1} - ✅ 통과
2. {검증 단계 2} - ✅ 통과
3. {검증 단계 3} - ✅ 통과

**수정 후 증거**:

- 스크린샷: `{path/to/after-fix-screenshot.png}`
- 콘솔 출력: {정상 출력 확인}

**예상 동작 확인**: ✅ 정상 동작 확인됨

**엣지 케이스 테스트**:

- {엣지 케이스 1}: ✅ 통과
- {엣지 케이스 2}: ✅ 통과

---

## 🧪 회귀 테스트 작성

**테스트 파일**: `{path/to/test.spec.ts}`

**테스트 커버리지**:

- [x] 원본 버그 시나리오
- [x] 예상 동작 검증
- [x] 엣지 케이스 {n}개

**주요 assertion**:

- {assertion 1}
- {assertion 2}

**테스트 실행 결과**: {✅ 통과 / 실행 예정}

---

## 📊 영향 범위

**수정 영향 범위**:

- {영향받는 기능 1}
- {영향받는 기능 2}

**부작용 확인**: {없음 / 다음 사항 확인 필요}

**추가 테스트 권장사항**:

- {권장 테스트 1}
- {권장 테스트 2}

---

## 🔑 배운 점

**기술적 인사이트**:

- {인사이트 1}
- {인사이트 2}

**향후 예방 방법**:

- {예방 방법 1}
- {예방 방법 2}

---

## 📝 메모

{추가 메모나 고려사항}

````

### English Version: `docs/e2e-ui/fix-summary-test-N.md`

```markdown
# Bug Fix Summary: Test N

> **Fixed**: {YYYY-MM-DD HH:mm}
> **Original Bug Report**: [bug-report-test-N.md](./bug-report-test-N.md)
> **Test File**: `{path/to/test.spec.ts}`

---

## 📋 Bug Summary

**Priority**: {Critical/High/Medium}

**Original Issue**: {one line bug description}

---

## 🔍 Reproduction Results

**Reproduced Successfully**: ✅ Yes / ❌ No

**Reproduction Steps**:

1. {step 1}
2. {step 2}
3. {bug occurs here}

**Before-Fix Evidence**:

- Screenshot: `{path/to/before-fix-screenshot.png}`
- Console Errors:

````

{console error messages}

````

---

## 🔬 Root Cause Analysis

**Analysis Method**: Direct Tools (Grep + Read + Playwright MCP)

**Root Cause**:

{detailed root cause explanation}

**Affected Files**:

- `{file1}`: {what issue}
- `{file2}`: {what issue}

**Cause Category**: {UI Component / Logic Error / Integration Issue / etc}

---

## 🛠️ Fix Implementation

**Fix Approach**: {approach explanation}

**Changed Files**:

- `{file1}`: {what changed}
- `{file2}`: {what changed}

**Key Changes**:

```typescript
// Before
{code before change}

// After
{code after change}
````

**Rationale**: {why fixed this way}

---

## ✅ Fix Verification

**Verification Method**: Playwright MCP Browser Testing

**Verification Steps**:

1. {verification step 1} - ✅ Pass
2. {verification step 2} - ✅ Pass
3. {verification step 3} - ✅ Pass

**After-Fix Evidence**:

- Screenshot: `{path/to/after-fix-screenshot.png}`
- Console Output: {clean output confirmed}

**Expected Behavior Confirmed**: ✅ Working as expected

**Edge Cases Tested**:

- {edge case 1}: ✅ Pass
- {edge case 2}: ✅ Pass

---

## 🧪 Regression Test

**Test File**: `{path/to/test.spec.ts}`

**Test Coverage**:

- [x] Original bug scenario
- [x] Expected behavior validation
- [x] {n} edge cases

**Main Assertions**:

- {assertion 1}
- {assertion 2}

**Test Execution Result**: {✅ Pass / Pending}

---

## 📊 Impact Scope

**Fix Impact**:

- {affected feature 1}
- {affected feature 2}

**Side Effects Check**: {None / Following needs verification}

**Additional Testing Recommendations**:

- {recommended test 1}
- {recommended test 2}

---

## 🔑 Learnings

**Technical Insights**:

- {insight 1}
- {insight 2}

**Prevention for Future**:

- {prevention method 1}
- {prevention method 2}

---

## 📝 Notes

{additional notes or considerations}

```

---

## Execution Flow Summary

```

┌─────────────────────────────────────────┐
│ 1. Preparation │
│ - Load bug report │
│ - Read playwright.config.ts │
│ - Read package.json │
└────────────────┬────────────────────────┘
│
▼
┌─────────────────────────────────────────┐
│ 2. Bug Reproduction │
│ - Use Playwright MCP │
│ - Follow reproduction steps │
│ - Take before-fix screenshots │
└────────────────┬────────────────────────┘
│
▼
┌─────────────────────────────────────────┐
│ 3. Root Cause Analysis │
│ - Use Grep to find related code │
│ - Read source files (offset/limit) │
│ - Identify root cause │
└────────────────┬────────────────────────┘
│
▼
┌─────────────────────────────────────────┐
│ 4. Fix Implementation │
│ - Make minimal changes │
│ - Follow coding principles │
└────────────────┬────────────────────────┘
│
▼
┌─────────────────────────────────────────┐
│ 5. Fix Verification │
│ - Use Playwright MCP │
│ - Verify expected behavior │
│ - Take after-fix screenshots │
└────────────────┬────────────────────────┘
│
▼
┌─────────────────────────────────────────┐
│ 6. Write Regression Test │
│ - Create test in testDir │
│ - Follow testMatch pattern │
│ - Include edge cases │
└────────────────┬────────────────────────┘
│
▼
┌─────────────────────────────────────────┐
│ 7. Documentation │
│ - Generate bilingual fix summary │
│ - Update bug report status │
│ - Report to user │
└─────────────────────────────────────────┘

````

---

## Completion Report Format

After fix completion, provide summary to user:

```markdown
## Bug Fix Complete: Test N

### 🐛 Original Bug

- **Priority**: {priority}
- **Issue**: {one line description}
- **Bug Report**: docs/e2e-ui/bug-report-test-N.md

### ✅ Fix Summary

- **Root Cause**: {root cause}
- **Fix Approach**: {approach}
- **Files Changed**: {count} files
  - {file1}
  - {file2}

### 🧪 Verification

- **Reproduction**: ✅ Bug reproduced successfully
- **Fix Verified**: ✅ Expected behavior now works
- **Test Written**: ✅ Regression test created

### 📝 Generated Files

- **Fix Summary**:
  - `docs/e2e-ui/fix-summary-test-N.ko.md` (Korean)
  - `docs/e2e-ui/fix-summary-test-N.md` (English)
- **Test File**: `{path/to/test.spec.ts}`

### 📸 Evidence

- Before-fix: `{screenshot-before.png}`
- After-fix: `{screenshot-after.png}`

### 🔄 Next Steps

1. Review fix implementation
2. Run full test suite to verify no regressions
3. Continue with next bug or test: `/e2e-ui:execute {N+1}`
````

---

## Execute

Start working according to the guidelines above.
