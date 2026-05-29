---
skill: form-status
description: Check form submission status across projects
context: fork
arguments:
  - name: filter
    description: Optional project name, form type, or "pending"/"overdue"
    required: false
---

# /form-status Skill

Show status of form submissions across projects.

## Usage

```
/form-status                    # All forms summary
/form-status pending            # Forms awaiting response
/form-status overdue            # Forms past expected response
/form-status MyDataIntegration             # Forms for specific project
/form-status DPIA               # All DPIA submissions
/form-status CyberRisk          # All Cyber Risk assessments
```

## Instructions

1. **Search for FormSubmission notes**:
   ```
   Glob pattern: **/Form Submission*.md
   Also check: type = "FormSubmission" in frontmatter
   ```

2. **Extract metadata from each**:
   - formType (DPIA, CyberRisk, ChangeRequest, TPRM, IAF, Other)
   - status (draft, submitted, pending, approved, rejected, expired)
   - project
   - submittedDate
   - responseDate
   - expiryDate
   - requestingTeam

3. **Apply filter if provided**:
   - "pending" = status is "submitted" or "pending"
   - "overdue" = submittedDate > 30 days ago AND status not in [approved, rejected]
   - Project name = matches project field
   - Form type = matches formType field

4. **Generate report**:

```markdown
# Form Submission Status

**Generated**: {{date}}
**Filter**: {{filter or "All"}}

## Summary

| Status | Count |
|--------|-------|
| Draft | X |
| Submitted/Pending | X |
| Approved | X |
| Rejected | X |
| Expired | X |

## By Form Type

### DPIA (Data Protection Impact Assessment)
| Project | Status | Submitted | Response | Reference |
|---------|--------|-----------|----------|-----------|
| [[Project]] | pending | 2026-01-05 | - | DPIA-123 |

### CyberRisk (Cyber Security Risk Assessment)
| Project | Status | Submitted | Response | Reference |
|---------|--------|-----------|----------|-----------|

### TPRM (Third Party Risk Management)
...

### ChangeRequest
...

### IAF (Initial Assessment Form)
...

## Attention Required

### Overdue (>30 days, no response)
- [[Form Submission - DPIA for MyDataIntegration]] - submitted 2025-12-01 (41 days ago)

### Expiring Soon (<30 days to expiry)
- [[Form Submission - TPRM for MaintenanceSystem]] - expires 2026-02-10

### Drafts Not Submitted
- [[Form Submission - CyberRisk for OpDef]] - created 2026-01-03

## By Project

### [[Project - MyDataIntegration]]
- DPIA: approved (2025-11-15)
- CyberRisk: pending (submitted 2026-01-05)
- TPRM: draft

### [[Project - MaintenanceSystem]]
...
```

## Form Types Reference

| Type | Full Name | Requesting Team |
|------|-----------|-----------------|
| DPIA | Data Protection Impact Assessment | Data Privacy / Legal |
| CyberRisk | Cyber Security Risk Assessment | Cyber Security |
| TPRM | Third Party Risk Management | Procurement / Cyber |
| IAF | Initial Assessment Form | Cyber Delivery Assurance |
| ChangeRequest | Change Request / RFC | Change Management |
| Other | Other intake forms | Various |

## Status Values

| Status | Meaning |
|--------|---------|
| draft | Not yet submitted |
| submitted | Sent, awaiting acknowledgement |
| pending | Acknowledged, under review |
| approved | Approved / passed |
| rejected | Rejected / failed |
| expired | Approval expired, needs renewal |

## Quick Create

If user mentions a form they need to track, offer to create:

```
/form <type> <project>
```

Example: `/form DPIA MyDataIntegration` creates `Form Submission - DPIA for MyDataIntegration.md`
