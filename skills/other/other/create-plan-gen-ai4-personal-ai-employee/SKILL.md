---
name: create-plan
description: |
  Create structured Plan.md files for items in /Needs_Action. Analyzes each pending
  item against Company_Handbook.md rules and Business_Goals.md, determines required
  steps, and creates a plan with checkboxes in /Plans. Use when new items arrive and
  need a structured action plan before processing.
---

# Create Plan

Generate structured Plan.md files for pending vault items.

## Workflow

### 1. Read Context
- Read `vault/Company_Handbook.md` for processing rules and priorities
- Read `vault/Business_Goals.md` for business context and metrics

### 2. Analyze Pending Items
For each `.md` file in `vault/Needs_Action/`:
- Parse YAML frontmatter to extract: type, priority, source, status
- Skip items that already have `status: planned`
- Determine action type (email, file_drop, linkedin_*, etc.)

### 3. Create Plan
For each item, create a `PLAN_YYYYMMDD_HHMMSS_<source>.md` in `vault/Plans/`:

```markdown
---
type: plan
plan_id: "PLAN_..."
source_file: "original_file.md"
action_type: email|file_drop|linkedin_*
priority: high|medium|low
created: ISO-8601
status: pending
requires_approval: true|false
---

# Plan Title

**Source**: original_file.md
**Priority**: high

## Objective
What needs to be accomplished

## Steps
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3 (REQUIRES APPROVAL)

## Context Notes
- Relevant handbook rules
- Business goal alignment

## Approval Status
Status of any required approvals
```

### 4. Determine Approval Requirements
Actions that ALWAYS require approval:
- `payment`, `email_send`, `linkedin_post`, `social_post`
- `file_delete`, `external_api_call`, `new_contact_email`

Auto-approved actions:
- `file_organize`, `log_create`, `dashboard_update`, `plan_create`

### 5. Log Results
Log each plan creation to `vault/Logs/YYYY-MM-DD.json`

## Important Rules
- Always cross-reference Company_Handbook.md before creating a plan
- High-priority items: include the 1-hour response time note
- Never skip the approval step for sensitive actions
- Plans are proposals - they don't execute actions themselves
