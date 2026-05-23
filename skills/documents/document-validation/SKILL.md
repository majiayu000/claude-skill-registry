---
name: document-validation
description: Validate workflow documents against templates. Use when verifying PRD, execution plan, or user story files before HITL approval - checks required frontmatter fields and sections against templates.
---

# Document Validation Skill

**Purpose:** Validate workflow documents against template requirements
**Trigger:** Called by reviewer agent before HITL approval
**Input:** Document path, document type (prd | execution-plan | user-story)
**Output:** `{valid, document_type, issues[], checked_fields[], checked_sections[]}`

---

## Workflow

### 1. Detect Document Type

| Pattern                        | Document Type  |
| ------------------------------ | -------------- |
| `project_id` in frontmatter    | PRD            |
| `total_stories` in frontmatter | Execution Plan |
| `story_id` in frontmatter      | User Story     |

### 2. Parse Document

1. Extract YAML frontmatter (between `---` markers)
2. Parse frontmatter fields
3. Extract markdown sections (H2 headers)

### 3. Validate Against Checklist

Run type-specific validation (see checklists below).

---

## PRD Checklist

**Frontmatter:** `project_id`, `title`, `version`, `status`, `owner`, `created`, `updated`

**Sections:** `## 1. Executive Summary`, `## 2. Problem Statement`, `## 3. Solution Overview`, `## 4. Requirements`, `## 5. Scope`, `## 6. Epic Summary`, `## 7. Success Criteria`

---

## Execution Plan Checklist

**Frontmatter:** `project_id`, `title`, `status`, `total_stories`, `total_complexity`, `total_waves`, `owner`, `created`, `updated`

**Sections:** `## Summary`, `## Wave Strategy Overview`, `## User Stories Index`, `## Wave N:` (at least one)

---

## User Story Checklist

**Frontmatter:** `story_id`, `epic_id`, `title`, `status`, `complexity`, `wave`, `agent`, `dependencies`, `created`, `updated`

**Sections:** `## User Story`, `## Acceptance Criteria`, `## Technical Details`, `## Definition of Done`

---

## Issue Types

| Issue Type        | Description                       | Severity |
| ----------------- | --------------------------------- | -------- |
| `missing_field`   | Required frontmatter field absent | CRITICAL |
| `missing_section` | Required markdown section absent  | CRITICAL |
| `invalid_format`  | Field value format incorrect      | WARNING  |
| `empty_section`   | Section exists but empty          | WARNING  |

---

## Output Structure

```json
{
  "valid": true|false,
  "document_type": "prd|execution-plan|user-story",
  "issues": [{"type": "...", "field|section": "...", "message": "..."}],
  "checked_fields": [{"field": "...", "status": "pass|fail"}],
  "checked_sections": [{"section": "...", "status": "pass|fail"}]
}
```

---

## Integration

**Called by:** `reviewer` agent, `hitl-approval` skill, `/ms` command

**References:**

- PRD template: `../prd-creation/templates/prd-template.md`
- Execution plan template: `../execution-plan-creation/templates/execution-plan-template.md`
- User story template: `../user-story-creation/templates/user-story-template.md`

**Next:** Valid -> HITL approval; Invalid -> return to authoring agent
