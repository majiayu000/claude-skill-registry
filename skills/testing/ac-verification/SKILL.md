---
name: ac-verification
description: Verify that implemented code meets acceptance criteria from user stories. Use when validating story completion - performs code inspection, test execution, and manual checks against each AC criterion.
---

# AC Verification Skill

**Purpose:** Verify implemented code meets acceptance criteria (AC) defined in user stories
**Trigger:** Called by validation-phase or /audit after code implementation
**Input:** User stories with AC, implemented files, test suite
**Output:** `{verified, results[], unmet_criteria[]}`

---

## Workflow Steps

### 1. Extract Acceptance Criteria

For each user story ({PROJECT}-{EPIC}-{NNN}):

1. Read story file (extract AC list)
2. Parse AC checkbox format: `- [x]` (complete) or `- [ ]` (incomplete)
3. Record AC text and current status
4. Note associated implementation files/tests

### 2. Verify Each Criterion

For each AC in the story:

**a. Code Inspection:**

1. Check if referenced file exists
2. Check if referenced function/class exists
3. Verify property/method signatures match AC description
4. If file missing → Record as UNMET

**b. Test Execution:**

1. Locate test file (standard: `__tests__/{filename}.test.{ts,js}` or `.spec.{ts,js}`)
2. Run test suite: `pnpm test --run {test_file}`
3. Parse test results:
   - All tests passing → Record as PASSED
   - Tests failing → Record as FAILED + error details
   - No tests found → Proceed to manual check

**c. Manual Check Prompts:**

For UI/UX or non-automatable criteria:

1. Ask user: "Verify AC: {ac_text}"
2. User response: yes/no/skip
3. Record response + timestamp

### 3. Aggregate Results

Compile per-story verification:

```json
{
  "story_id": "prj-epc-001",
  "title": "User Authentication",
  "ac_total": 4,
  "ac_passed": 3,
  "ac_failed": 1,
  "ac_results": [
    {
      "criterion": "User can login with email + password",
      "status": "pass",
      "method": "test_execution",
      "test_file": "src/__tests__/auth.test.ts",
      "tests_passed": 2
    },
    {
      "criterion": "Invalid credentials rejected",
      "status": "fail",
      "method": "test_execution",
      "error": "Test 'Invalid credentials' failed: expected 401"
    },
    {
      "criterion": "Login button is visible on mobile",
      "status": "pending",
      "method": "manual_check",
      "prompt_sent": true
    }
  ]
}
```

### 4. Overall Verdict

**VERIFIED (100% pass):**

- All AC passed code inspection OR test execution
- All manual checks completed (user confirmed)
- Update story: Status → ✅ Verified
- Mark AC checkboxes: `- [x]`

**UNMET (any AC failed):**

- List failed/incomplete AC
- Record verification method failures (missing files, test failures)
- Return control to execution for remediation
- Update story: Status → ⚠️ AC Not Met + details

**PARTIAL (manual pending):**

- Some AC verified, some manual pending
- Await user responses
- Lock story until all checks complete

---

## Verification Methods

| Method          | When to Use                       | Result          |
| --------------- | --------------------------------- | --------------- |
| Code Inspection | File/function existence checks    | Pass/Fail       |
| Test Execution  | Automated test suites available   | Pass/Fail/Error |
| Manual Check    | UI/UX or non-automatable criteria | Yes/No/Skip     |

---

## Failure Handling

**Missing Implementation File:**

```
AC: "User model stores email address"
Method: Code Inspection
Result: FAIL - File 'src/models/User.ts' not found
Action: Return to execution for file creation
```

**Test Failure:**

```
AC: "Invalid password rejected"
Method: Test Execution
Result: FAIL - test 'rejects invalid password' failed
Error: Expected status 401, got 200
Action: Return to execution for code fix
```

**Manual Confirmation Required:**

```
AC: "Login form validation error displays in red"
Method: Manual Check
Prompt: "Verify AC: Login form validation error displays in red"
User Response: "yes" or "no"
Action: Record response, proceed or flag remediation
```

---

## Output Structure

**Success Output:**

```json
{
  "verified": true,
  "status": "complete",
  "summary": {
    "stories_verified": 5,
    "total_ac": 18,
    "ac_passed": 18,
    "ac_failed": 0,
    "verification_time_ms": 12500
  },
  "results": [
    {
      "story_id": "prj-epc-001",
      "ac_total": 4,
      "ac_passed": 4,
      "ac_failed": 0,
      "status": "verified"
    }
  ],
  "unmet_criteria": []
}
```

**Failure Output:**

```json
{
  "verified": false,
  "status": "blocked",
  "summary": {
    "stories_verified": 5,
    "total_ac": 18,
    "ac_passed": 15,
    "ac_failed": 3,
    "verification_time_ms": 12500
  },
  "results": [
    {
      "story_id": "prj-epc-002",
      "ac_total": 4,
      "ac_passed": 3,
      "ac_failed": 1,
      "status": "unmet",
      "failed_ac": [
        {
          "criterion": "Password reset email sent within 30 seconds",
          "method": "test_execution",
          "error": "Test timeout: email not sent"
        }
      ]
    }
  ],
  "unmet_criteria": [
    "prj-epc-002: AC 2 - Password reset email sent within 30 seconds",
    "prj-epc-003: AC 1 - File upload supports .pdf files",
    "prj-epc-005: AC 3 - Admin dashboard shows user count"
  ]
}
```

---

## Integration

**Called by:**

- `validation-phase` skill (after execution)
- `/audit` command (post-implementation)
- `/build` command (acceptance validation)

**Calls:**

- File system checks (Read tool)
- Test execution (`pnpm test --run`)
- User prompts (for manual verification)

**Next step:** If verified → proceed to report-phase; If unmet → return to execution-phase

---

## Example: AC Verification Workflow

**Input Story:**

```markdown
# prj-epc-001: User Authentication

## Acceptance Criteria

- [ ] User can login with email + password
- [ ] Invalid credentials rejected with 401 status
- [ ] User session persists after logout + login
- [ ] Login button is visible on mobile (manual check)

## Implementation Status

Test File: src/**tests**/auth.test.ts
Files Modified: src/auth.ts, src/services/AuthService.ts
```

**Verification Process:**

```
1. AC #1: "User can login with email + password"
   → Run src/__tests__/auth.test.ts
   → Test 'login with valid credentials' passes
   → Status: PASS

2. AC #2: "Invalid credentials rejected with 401 status"
   → Run src/__tests__/auth.test.ts
   → Test 'login rejects invalid credentials' passes
   → Status: PASS

3. AC #3: "User session persists after logout + login"
   → Check file: src/services/AuthService.ts exists ✓
   → Run src/__tests__/auth.test.ts
   → Test 'session persists' passes
   → Status: PASS

4. AC #4: "Login button is visible on mobile (manual)"
   → Prompt user: "Verify: Login button visible on mobile?"
   → User confirms: "yes"
   → Status: PASS

Result: ALL AC VERIFIED ✓
Update Story: Status → ✅ Verified, mark all AC checkboxes [x]
```

---

## Success Criteria

- All AC mapped to code/tests
- Code inspection completes without errors
- Test execution passes or gracefully handles failures
- Manual checks prompted for non-automatable AC
- Clear output indicating pass/fail per AC
- Story file updated with verification status
- Unmet AC clearly documented for remediation
