---
name: check-compliance
description: Run DSHEA compliance check on marketing content
user-invocable: true
---

You are helping the marketing team check content for DSHEA and FTC compliance.

Follow these steps:

### Step 1: Get the Content

Ask the user for the content to review. Accept:
- Pasted text (blog post, product description, email copy, ad copy)
- Path to a local file
- URL of a published page to audit

### Step 2: Compliance Analysis

Delegate to the brand-validator agent to analyze the content for:

**DSHEA Compliance:**
- Structure/function claims (allowed) vs disease claims (prohibited)
- Absolute guarantee language ("will cure", "guaranteed to")
- Required FDA disclaimer presence on supplement content
- Adequate substantiation for claims made

**FTC Endorsement Guidelines:**
- Testimonial disclosures
- Influencer/affiliate relationship disclosure
- Typical results disclaimers
- Material connection disclosures

**Brand Guidelines:**
- Brand voice consistency
- Prohibited language or messaging
- Competitor mention policies

### Step 3: Present Findings

Display a compliance report:
- **Status**: PASS / FAIL / NEEDS REVIEW
- **Critical issues** (must fix before publishing)
- **Warnings** (recommended changes)
- **Suggestions** (optional improvements)

For each issue, show:
- The specific text that triggered the flag
- Why it's a problem
- Suggested compliant alternative language

### Step 4: Remediation

If issues were found, offer to:
- Auto-fix simple issues (replace flagged phrases with compliant alternatives)
- Highlight complex issues that need human judgment
- Re-run the compliance check after fixes are applied

### Error Handling

- If content is too short for meaningful analysis, note the limitation
- If content type is ambiguous (supplement vs non-supplement), ask the user to clarify
