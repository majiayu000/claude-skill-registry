---
skill: form
description: Quick-create a form submission note
context: fork
arguments:
  - name: type
    description: Form type (DPIA, CyberRisk, TPRM, IAF, ChangeRequest, Other)
    required: true
  - name: project
    description: Project name (without "Project - " prefix)
    required: true
---

# /form Skill

Quick-create a form submission tracking note.

## Usage

```
/form DPIA MyDataIntegration
/form CyberRisk "MaintenanceSystem"
/form TPRM VendorTooling
/form IAF "AIIncidentProcessor"
/form ChangeRequest OpDef
```

## Instructions

1. **Parse arguments**:
   - First word = formType
   - Remaining = project name (handle quotes for multi-word)

2. **Validate formType** against allowed values:
   - DPIA
   - CyberRisk
   - TPRM
   - IAF
   - ChangeRequest
   - Other

3. **Find matching project** (fuzzy match):
   - Search for `Project - *{{project}}*.md`
   - If not found, ask user to confirm project name

4. **Create form submission note**:

   **Filename**: `Form Submission - {{formType}} for {{project}}.md`

   **Location**: Root directory (same as other content notes)

5. **Populate frontmatter**:

```yaml
---
type: FormSubmission
title: "{{formType}} for {{project}}"
formType: { { formType } }
status: draft
project: "[[Project - {{project}}]]"
requestingTeam: { { lookup from table below } }
submittedDate: null
responseDate: null
expiryDate: null
referenceNumber: null
attachments: []
created: { { today } }
modified: { { today } }
tags: [activity/compliance, { { domain_tag } }] # See tag lookup table below
---
```

6. **Requesting team and tag lookup**:

| formType      | requestingTeam           | domain_tag        |
| ------------- | ------------------------ | ----------------- |
| DPIA          | Data Privacy             | domain/data       |
| CyberRisk     | Cyber Security           | domain/security   |
| TPRM          | Procurement              | domain/security   |
| IAF           | Cyber Delivery Assurance | domain/security   |
| ChangeRequest | Change Management        | domain/operations |
| Other         | (ask user)               | (ask user)        |

7. **Generate body content**:

```markdown
# {{formType}} for {{project}}

## Form Details

| Field               | Value                     |
| ------------------- | ------------------------- |
| **Form Type**       | {{formType}}              |
| **Status**          | draft                     |
| **Project**         | [[Project - {{project}}]] |
| **Requesting Team** | {{requestingTeam}}        |
| **Submitted**       | -                         |
| **Response**        | -                         |
| **Reference**       | -                         |

## Summary

<!-- Brief description of what this form submission covers -->

## Key Information Provided

<!-- Main points you included in the form -->

- System/service name:
- Data classification:
- Third parties involved:
- Key risks identified:

## Attachments

<!-- Link screenshots or PDFs of the submitted form here -->
<!-- Example: ![[+Attachments/dpia-screenshot.png]] -->

## Response / Outcome

<!-- What was the result? Any conditions or follow-up required? -->

## Notes

<!-- Any additional context or follow-up actions -->
```

8. **Confirm creation** and remind user to:
   - Fill in key information
   - Update status when submitted
   - Add attachment links to screenshots/PDFs
   - Add reference number when received

## Form Type Descriptions

| Type              | Purpose                                         | Typical Questions                                      |
| ----------------- | ----------------------------------------------- | ------------------------------------------------------ |
| **DPIA**          | Assess data protection risks for new processing | Personal data types, legal basis, retention, transfers |
| **CyberRisk**     | Evaluate cyber security risks                   | Architecture, controls, vulnerabilities, mitigations   |
| **TPRM**          | Assess third-party vendor risks                 | Vendor security posture, data handling, contracts      |
| **IAF**           | Initial cyber assessment for new projects       | Scope, data, integrations, compliance requirements     |
| **ChangeRequest** | Request infrastructure/system changes           | What, why, when, impact, rollback plan                 |

## Example Output

After `/form DPIA MyDataIntegration`:

```
Created: Form Submission - DPIA for MyDataIntegration.md

Next steps:
1. Fill in the summary and key information
2. When you submit, update status to "submitted" and add submittedDate
3. Add screenshots/PDFs to +Attachments/ and link them
4. Add reference number when you receive acknowledgement
```
