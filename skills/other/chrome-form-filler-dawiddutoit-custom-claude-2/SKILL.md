---
name: chrome-form-filler
description: |
  Safely fills web forms in Chrome with user approval and verification at every step.
  Use when asked to "fill this form", "complete the form for me", "fill out registration",
  "submit this application", or when user needs form automation with safety controls.
  Works with Chrome browser tabs via MCP tools (tabs_context_mcp, read_page, form_input).
  Enforces permission workflows, field verification, and never fills sensitive data.
allowed-tools:
  - mcp__claude-in-chrome__tabs_context_mcp
  - mcp__claude-in-chrome__read_page
  - mcp__claude-in-chrome__find
  - mcp__claude-in-chrome__form_input
  - mcp__claude-in-chrome__computer
  - mcp__claude-in-chrome__update_plan
  - mcp__claude-in-chrome__screenshot
---

# Chrome Form Filler

## Quick Start

Fill a web form safely with user approval:

```
User: "Fill out this registration form with my information"

Claude:
1. Gets tab context and reads form fields
2. Presents fields to user for approval
3. Fills each field incrementally
4. Verifies values after filling
5. Requests submission approval
6. Submits form only after confirmation
```

**Critical Safety Rule:** NEVER fill sensitive data (passwords, credit cards, SSNs, banking info) - always instruct user to fill these themselves.

## Table of Contents

1. When to Use This Skill
2. What This Skill Does
3. Safety-First Workflow
4. Field Filling Process
5. Verification and Submission
6. Supporting Files
7. Expected Outcomes
8. Requirements
9. Red Flags to Avoid

## When to Use This Skill

### Explicit Triggers
- "Fill this form"
- "Complete the form for me"
- "Fill out registration"
- "Submit this application"
- "Auto-fill the contact form"
- "Help me fill this survey"

### Implicit Triggers
- User provides data and mentions form completion
- User expresses frustration with long forms
- Context shows user on form page with multiple fields

### Debugging Triggers
- "The form didn't submit correctly"
- "Some fields are empty after filling"
- "Verification failed"

## What This Skill Does

This skill automates web form filling with safety controls and user approval at every critical step:

1. **Form Discovery** - Identifies all form fields on the page
2. **Permission Planning** - Presents approach to user via update_plan
3. **Field Identification** - Maps fields to user data with confirmation
4. **Incremental Filling** - Fills one field at a time with verification
5. **Pre-Submission Review** - Shows all filled values before submit
6. **Submission Control** - Submits only after explicit user approval
7. **Confirmation Verification** - Validates successful submission

## Safety-First Workflow

### Phase 1: Discovery and Planning

**1. Get Tab Context**
```
Call: tabs_context_mcp(createIfEmpty=true)
Verify: Tab group exists and tab ID is valid
```

**2. Read Page for Form Fields**
```
Call: read_page(tabId, filter="interactive")
Identify: All input fields, selects, textareas, checkboxes, radio buttons
Extract: Field labels, types, current values, required status
```

**3. Present Plan to User**
```
Call: update_plan(
  domains=["current-domain.com"],
  approach=[
    "Identify all form fields on [page name]",
    "Fill [X] fields with provided data",
    "Verify each field after filling",
    "Request approval before submission",
    "Submit form and verify confirmation"
  ]
)
```

**User must approve plan before proceeding.**

### Phase 2: Field Mapping and Approval

**4. Map Fields to User Data**

Present structured summary to user:
```
Found [X] fields on [Form Name]:

Required Fields:
- First Name (text input) → [User's data or ASK]
- Email (email input) → [User's data or ASK]
- Phone (tel input) → [User's data or ASK]

Optional Fields:
- Company (text input) → [User's data or SKIP]
- Comments (textarea) → [User's data or SKIP]

SENSITIVE FIELDS (you must fill manually):
- Password (password input) → USER MUST FILL
- Credit Card (text input) → USER MUST FILL

Proceed with filling [X] fields? (yes/no)
```

**Critical Rules:**
- ❌ NEVER fill password fields
- ❌ NEVER fill credit card fields
- ❌ NEVER fill SSN/banking fields
- ❌ NEVER fill fields marked "sensitive" by context
- ✅ ALWAYS get explicit approval for data mapping
- ✅ ALWAYS show which fields will be filled

### Phase 3: Incremental Filling

**5. Fill Each Field One at a Time**

For each approved field:

```
Step 1: Find element
  Call: find(tabId, query="[field label or purpose]")
  Verify: Element reference returned

Step 2: Fill field
  Call: form_input(tabId, ref="ref_X", value="[user data]")

Step 3: Verify filled value
  Call: read_page(tabId, ref_id="ref_X")
  Confirm: Value matches expected input

Step 4: Handle errors
  If verification fails:
    - Report to user
    - Ask for correction approach
    - Retry with alternative method (computer tool for typing)
```

**Example filling sequence:**
```
✅ Filled "First Name" → "John" (verified)
✅ Filled "Last Name" → "Smith" (verified)
✅ Filled "Email" → "john@example.com" (verified)
⚠️ Failed "Phone" → retry needed
✅ Filled "Phone" → "(555) 123-4567" (verified after retry)
```

### Phase 4: Pre-Submission Review

**6. Show Complete Form State**

Before submission, present ALL filled values:
```
Form ready for submission:

First Name: John
Last Name: Smith
Email: john@example.com
Phone: (555) 123-4567
Company: [empty - optional]
Comments: [empty - optional]

UNFILLED SENSITIVE FIELDS (you must complete):
- Password: [EMPTY - FILL MANUALLY]

Submit this form? (yes/no/edit)
```

**User must explicitly approve submission.**

### Phase 5: Submission and Verification

**7. Submit Form**

Only after approval:
```
Step 1: Find submit button
  Call: find(tabId, query="submit button")

Step 2: Click submit
  Call: computer(tabId, action="left_click", ref="ref_submit")

Step 3: Wait for navigation/response
  Call: computer(tabId, action="wait", duration=2)
```

**8. Verify Confirmation**

After submission:
```
Step 1: Read new page
  Call: read_page(tabId)

Step 2: Look for confirmation indicators:
  - Success message
  - Thank you page
  - Confirmation number
  - Email sent notice
  - Error messages

Step 3: Report outcome to user
  Success: "Form submitted successfully. Confirmation: [details]"
  Failure: "Submission failed: [error message]. Next steps: [guidance]"
```

## Field Filling Process

### Supported Field Types

| Field Type | Method | Verification |
|------------|--------|--------------|
| Text input | `form_input()` | Read value back |
| Email input | `form_input()` | Validate format + read back |
| Tel input | `form_input()` | Read value back |
| Textarea | `form_input()` | Read value back |
| Select dropdown | `form_input()` | Read selected option |
| Checkbox | `form_input(value=true/false)` | Read checked state |
| Radio button | `computer(action="left_click")` | Read selected state |
| Date input | `form_input()` | Read date value |

### Fallback Strategy

If `form_input()` fails:
1. Try `computer(action="left_click")` to focus field
2. Use `computer(action="type", text="value")` to type
3. Verify value with `read_page()`
4. Report persistent failures to user

### Validation Patterns

**Email validation:**
```
Regex: ^[^\s@]+@[^\s@]+\.[^\s@]+$
Check: Value contains @ and domain
```

**Phone validation:**
```
Format: Various (555) 123-4567, 555-123-4567, +1-555-123-4567
Strategy: Fill as provided, verify field accepts it
```

**Required field check:**
```
Before submission:
- Verify all required fields have values
- Report missing required fields to user
- Block submission until complete
```

## Verification and Submission

### Pre-Submission Checklist

Before calling submit:
- [ ] All required fields filled
- [ ] All values verified correct
- [ ] User approved field mapping
- [ ] User approved submission
- [ ] Sensitive fields flagged for manual entry
- [ ] No errors on page

### Error Handling

**Form validation errors:**
```
After submission attempt, if errors appear:
1. Read error messages
2. Map errors to fields
3. Report to user: "Field [X] error: [message]"
4. Ask user for corrected value
5. Re-fill and re-verify
6. Request submission approval again
```

**Network errors:**
```
If submission fails due to network:
1. Report error to user
2. Offer to retry
3. Verify form state preserved
4. Re-attempt with user approval
```

## Supporting Files

### references/reference.md
- Chrome MCP tool reference
- Form field type specifications
- Permission workflow patterns
- Error handling strategies

### examples/examples.md
- Complete form filling workflows
- Error recovery examples
- Multi-page form handling
- Dynamic form scenarios

### scripts/validate_form.py
- Validates form data before submission
- Checks for common input errors
- Suggests corrections

## Expected Outcomes

### Successful Form Fill

```
✅ Form Fill Complete

Form: Contact Us (example.com/contact)
Fields filled: 6/8 (2 optional skipped)
User filled manually: 1 (password)

Filled fields:
  ✓ First Name: John
  ✓ Last Name: Smith
  ✓ Email: john@example.com
  ✓ Phone: (555) 123-4567
  ✓ Message: [75 chars]
  ✓ Subscribe: Yes

Submission: Successful
Confirmation: "Thank you! We'll respond within 24 hours."

Next steps: Check email for confirmation message
```

### Partial Fill (Manual Intervention Needed)

```
⚠️ Form Partially Filled

Form: Registration (site.com/register)
Fields filled: 8/12
Blocked on: 4 fields require manual entry

Filled fields: [list]

USER MUST FILL MANUALLY:
  ⚠ Password (sensitive)
  ⚠ Confirm Password (sensitive)
  ⚠ Credit Card (sensitive)
  ⚠ CVV (sensitive)

Status: Ready for user to complete sensitive fields
Action: Complete the 4 sensitive fields, then I can submit
```

## Requirements

### Browser Setup
- Chrome browser with Claude-in-Chrome MCP extension
- Active tab group (created via tabs_context_mcp)
- Form page loaded and visible

### User Data
- Required field values provided by user
- Data format matches field expectations
- User available for approval prompts

### Permissions
- User must approve plan (update_plan)
- User must approve field mapping
- User must approve submission
- User must fill sensitive fields manually

## Red Flags to Avoid

**Critical Safety Violations:**
- ❌ Filling password fields automatically
- ❌ Filling credit card numbers
- ❌ Filling SSN or banking information
- ❌ Submitting without user approval
- ❌ Skipping field verification

**Workflow Violations:**
- ❌ Filling all fields before verification
- ❌ Proceeding without update_plan approval
- ❌ Assuming field mapping without user confirmation
- ❌ Submitting on errors

**Tool Misuse:**
- ❌ Using computer tool as first choice (use form_input first)
- ❌ Not verifying tab context exists
- ❌ Not handling element reference failures
- ❌ Skipping post-fill verification

**User Experience Issues:**
- ❌ Not presenting clear field summary
- ❌ Not reporting verification failures
- ❌ Not explaining why sensitive fields blocked
- ❌ Not providing confirmation details

## Notes

**Key Principles:**
1. **Permission First** - Always get approval before major actions
2. **Incremental Verification** - Verify each field immediately after filling
3. **Sensitive Data Protection** - Never automate sensitive field entry
4. **Error Transparency** - Report all failures clearly
5. **User Control** - User can stop/edit at any point

**Common Patterns:**
- Multi-page forms: Treat each page as separate workflow
- Dynamic forms: Re-scan after field changes trigger new fields
- Conditional fields: Only fill visible/enabled fields
- File uploads: Use upload_image tool (separate workflow)

**Integration with Other Skills:**
- Works with chrome-workflow-recorder for documenting process
- Complements chrome-data-extractor for reading results
- Pairs with update_plan for complex multi-step forms
