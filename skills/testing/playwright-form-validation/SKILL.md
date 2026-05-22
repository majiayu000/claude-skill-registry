---
name: playwright-form-validation
description: |
  Automates form validation testing by submitting invalid data and capturing error states
  using Playwright browser automation. Use when you need to "test form validation", "check
  validation errors", "test invalid inputs", "verify error messages", or perform comprehensive
  form testing. Triggers on validation testing requests, QA workflows, or form compliance checks.
  Works with web forms, input fields, and validation frameworks across any web application.
allowed-tools:
  - mcp__playwright__browser_navigate
  - mcp__playwright__browser_snapshot
  - mcp__playwright__browser_fill_form
  - mcp__playwright__browser_click
  - mcp__playwright__browser_wait_for
  - mcp__playwright__browser_take_screenshot
  - Write
  - Read
  - Bash
---

# Playwright Form Validation Tester

Automates comprehensive form validation testing by systematically submitting invalid data, capturing validation messages, and generating detailed test reports.

## Quick Start

Test a login form's validation:

```bash
# User asks: "Test the validation on the login form at example.com/login"

# Skill will:
# 1. Navigate to form
# 2. Test empty email field
# 3. Test invalid email format
# 4. Test empty password field
# 5. Test valid submission
# 6. Generate report with screenshots
```

**Output:** Validation report showing all error messages, missing validations, and screenshots of each error state.

## Table of Contents

1. When to Use This Skill
2. What This Skill Does
3. Instructions
4. Supporting Files
5. Expected Outcomes
6. Integration Points
7. Expected Benefits
8. Success Metrics
9. Requirements
10. Red Flags to Avoid
11. Notes

## 1. When to Use This Skill

### Explicit Triggers
- "Test form validation on [URL]"
- "Check validation errors for this form"
- "Test invalid inputs on the signup form"
- "Verify error messages are displayed"
- "Run validation tests on [form]"

### Implicit Triggers
- QA testing workflows requiring form validation checks
- Accessibility audits checking error message clarity
- Security testing for input sanitization
- Regression testing after form changes
- Documentation of validation behavior

### Debugging Triggers
- "Why isn't this form showing validation errors?"
- "Are all required fields validated?"
- "What validation messages does this form show?"
- "Check if email validation is working"

## 2. What This Skill Does

This skill performs systematic form validation testing:

1. **Field Discovery** - Identifies all form fields and their types
2. **Empty Value Testing** - Submits form with each field empty
3. **Invalid Format Testing** - Tests common invalid patterns (email, phone, etc.)
4. **Boundary Testing** - Tests min/max lengths and values
5. **Valid Submission** - Verifies successful submission with valid data
6. **Error Capture** - Screenshots and catalogs all validation messages
7. **Report Generation** - Creates comprehensive validation report

## 3. Instructions

### Overview

The validation testing workflow has 7 main steps:

1. Navigate to form and capture initial state
2. Identify all form fields and their constraints
3. Test empty field validation for required fields
4. Test invalid format validation (email, phone, etc.)
5. Test boundary values (min/max lengths and values)
6. Test valid submission to verify success path
7. Generate comprehensive validation report

### Quick Workflow Example

```typescript
// 1. Navigate and snapshot
await browser_navigate({ url: "https://example.com/login" });
await browser_snapshot({ filename: "initial.md" });

// 2. Test empty email
await browser_fill_form({
  fields: [{ name: "Email", type: "textbox", ref: "ref_1", value: "" }]
});
await browser_click({ element: "Submit", ref: "ref_submit" });
await browser_take_screenshot({ filename: "empty-email.png" });

// 3. Test invalid email format
await browser_navigate({ url: "https://example.com/login" }); // Reset
await browser_fill_form({
  fields: [{ name: "Email", type: "textbox", ref: "ref_1", value: "invalid" }]
});
await browser_click({ element: "Submit", ref: "ref_submit" });
await browser_take_screenshot({ filename: "invalid-email.png" });

// 4. Test valid submission
await browser_navigate({ url: "https://example.com/login" });
await browser_fill_form({
  fields: [
    { name: "Email", type: "textbox", ref: "ref_1", value: "test@example.com" },
    { name: "Password", type: "textbox", ref: "ref_2", value: "ValidPass123!" }
  ]
});
await browser_click({ element: "Submit", ref: "ref_submit" });
await browser_take_screenshot({ filename: "success.png" });

// 5. Generate report using template
```

### Key Testing Patterns

**Empty Fields** - Test each required field with empty value
**Invalid Formats** - Test email (`invalid`), phone (`abc`), URL (`not-url`)
**Boundaries** - Test min/max length (`"short"`, `"a".repeat(101)`)
**Cross-Field** - Test password mismatch, invalid date ranges
**Valid Data** - Verify success path works

### Detailed Workflow

For complete step-by-step instructions with all code examples, see:
- `references/detailed-workflow.md` - Full workflow with code samples
- `references/validation-patterns.md` - Field type testing patterns
- `examples/examples.md` - Complete form testing examples

## 4. Supporting Files

- **references/validation-patterns.md** - Common validation patterns and test cases for different field types
- **examples/examples.md** - Complete validation test examples for common forms (login, signup, checkout)
- **templates/validation-report-template.md** - Markdown template for validation reports
- **scripts/parse_validation_errors.py** - Helper to extract validation messages from snapshots

## 5. Expected Outcomes

### Successful Validation Test

```markdown
✅ Form Validation Test Complete

Form: Login Form (https://example.com/login)
Fields tested: 2 (email, password)
Validations found: 4
Missing validations: 0

Results by field:

Email Field:
✅ Empty value - "Email is required"
✅ Invalid format - "Please enter a valid email address"

Password Field:
✅ Empty value - "Password is required"
✅ Too short - "Password must be at least 8 characters"

Valid submission: ✅ Success (redirected to dashboard)

Screenshots saved: 5
Report: .claude/artifacts/2025-12-20/validation-report-login-form.md
```

### Validation Issues Found

```markdown
⚠️ Form Validation Issues Detected

Form: Signup Form (https://example.com/signup)
Fields tested: 5
Validations found: 3
Missing validations: 2

Issues:

❌ Phone field - No validation for invalid format
   Tested: "abc123", "12-34" → No error message shown

❌ Age field - No validation for negative values
   Tested: "-5" → Submission accepted

Recommendations:
1. Add phone number format validation
2. Add min value constraint to age field
3. Consider adding password strength indicator

Report: .claude/artifacts/2025-12-20/validation-report-signup-form.md
```

## 6. Integration Points

### With Quality Gates
- Run validation tests as part of QA workflow
- Include in pre-release testing checklist
- Automate regression testing for form changes

### With Accessibility Testing
- Verify error messages are clear and descriptive
- Check that errors are associated with fields (aria-describedby)
- Validate screen reader compatibility

### With Security Testing
- Verify input sanitization on client side
- Check for XSS vulnerabilities in error messages
- Test SQL injection patterns in text fields

### With Documentation
- Auto-generate validation documentation from reports
- Create field reference guides with validation rules
- Document error message copy for style guides

## 7. Expected Benefits

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Time to test form** | 30 min (manual) | 2 min (automated) | 93% reduction |
| **Test coverage** | 40% (spot checks) | 100% (systematic) | 2.5x increase |
| **Bugs found** | 2-3 (missed edge cases) | 8-10 (comprehensive) | 3x increase |
| **Documentation** | None → Screenshots + report | Manual notes → Auto-generated | Consistent |
| **Regression testing** | Rarely done | Automated | Reliable |

## 8. Success Metrics

A validation test is successful when:

✅ All form fields identified and cataloged
✅ Empty value validation tested for required fields
✅ Invalid format validation tested for typed fields (email, phone, etc.)
✅ Boundary values tested for constrained fields (min/max)
✅ Valid submission verified with success confirmation
✅ All validation messages captured and documented
✅ Screenshots saved for each error state
✅ Validation report generated with findings
✅ Missing validations identified and reported
✅ Recommendations provided for improvements

## 9. Requirements

**Browser Automation:**
- Playwright MCP server configured
- Browser installed via `mcp__playwright__browser_install`
- Active browser session

**Tools:**
- `mcp__playwright__browser_navigate` - Navigate to form URL
- `mcp__playwright__browser_snapshot` - Capture form structure and errors
- `mcp__playwright__browser_fill_form` - Fill field values
- `mcp__playwright__browser_click` - Submit form
- `mcp__playwright__browser_wait_for` - Wait for validation to appear
- `mcp__playwright__browser_take_screenshot` - Capture error states
- `Write` - Generate validation report
- `Read` - Parse snapshots for validation messages

**Knowledge:**
- Common validation patterns (email, phone, URL, etc.)
- HTML form field types and attributes
- Validation message extraction from snapshots
- Markdown report formatting

**Environment:**
- `.claude/artifacts/{YYYY-MM-DD}/` directory for reports
- Write permissions for screenshots

## 10. Red Flags to Avoid

Common mistakes when testing form validation:

- [ ] **Not waiting for validation** - Click submit and immediately capture without waiting for messages
- [ ] **Testing only one field** - Missing comprehensive coverage of all fields
- [ ] **Ignoring field types** - Using same invalid pattern for all fields
- [ ] **Not testing boundaries** - Missing min/max length and value constraints
- [ ] **Skipping valid submission** - Not verifying success path works
- [ ] **Missing screenshots** - Not capturing visual proof of error states
- [ ] **Incomplete report** - Not documenting all findings systematically
- [ ] **Not clearing previous values** - Leaving field values from previous tests
- [ ] **Ignoring client-side vs server-side** - Not distinguishing validation types
- [ ] **Not checking accessibility** - Missing aria-invalid, aria-describedby attributes

## 11. Notes

**Best Practices:**

1. **Test systematically** - One field at a time, one validation at a time
2. **Clear between tests** - Reset form to clean state before each test
3. **Wait appropriately** - Give validation time to appear (1-2 seconds)
4. **Capture everything** - Screenshot + snapshot for each error state
5. **Document clearly** - Use descriptive filenames and report sections

**Validation Types to Test:**

- **Required field** - Empty value submission
- **Format validation** - Email, phone, URL, date patterns
- **Length constraints** - Min/max character limits
- **Value constraints** - Min/max numeric values
- **Pattern matching** - Regex validation (password strength, username format)
- **Cross-field validation** - Password confirmation, date ranges
- **Custom business rules** - Age restrictions, allowed domains

**Common Validation Messages:**

- "This field is required"
- "Please enter a valid email address"
- "Password must be at least 8 characters"
- "Please enter a valid phone number"
- "Value must be between X and Y"

**Report Organization:**

- Save all artifacts to dated directory: `.claude/artifacts/{YYYY-MM-DD}/`
- Use consistent naming: `validation-{testname}-{fieldname}.png`
- Include all screenshots in report with relative paths
- Provide actionable recommendations, not just findings

**Progressive Disclosure:**

- For simple forms (2-3 fields), include full results inline
- For complex forms (10+ fields), reference detailed results in report file
- Always provide summary statistics up front
- Link to screenshots rather than embedding them in conversation
