---
name: create-adr
description: Create MADR-format Architecture Decision Record. Use when recording an architectural decision, documenting a technical choice, or creating an ADR.
---

# ADR Creation Skill

## Purpose

Create Architecture Decision Records (ADRs) using the **MADR** (Markdown Any Decision Records) format. ADRs capture important architectural decisions and their context for future reference.

## Smart Interaction

### ASK the User When:

- **Creating new ADR**: Confirm ADR number (auto-suggest next available)
- **Deleting ADR**: Always confirm, suggest "Deprecated" status instead
- **Superseding ADR**: Confirm which ADR is being replaced

### PROCEED Autonomously When:

- **Updating existing ADR**: Add consequences discovered during implementation
- **Linking ADRs**: Add related ADR links
- **Fixing typos**: Non-destructive corrections
- **Updating status**: Proposed → Accepted after team approval

## Instructions

When creating an ADR:

1. **Find the next ADR number** by checking `/docs/architecture/decisions/`
2. **Use the MADR template** at `templates/madr.md`
3. **Output to** `/docs/architecture/decisions/NNNN-[kebab-case-title].md`

## Template

Use the template at: `.claude/skills/create-adr/templates/madr.md`

## ADR Naming Convention

Format: `NNNN-kebab-case-title.md`

Examples:

- `0001-use-supabase-for-database.md`
- `0002-tanstack-query-for-state.md`
- `0003-fumadocs-for-documentation.md`

## Status Definitions

| Status     | Meaning                                 |
| ---------- | --------------------------------------- |
| Proposed   | Under discussion, not yet decided       |
| Accepted   | Decision has been made and applies      |
| Deprecated | No longer applies, but kept for history |
| Superseded | Replaced by another ADR (link to it)    |

## When to Create an ADR

Create an ADR when:

- Choosing between technologies/libraries
- Defining architectural patterns
- Making decisions that affect multiple parts of the system
- Making decisions that are hard to reverse
- Team needs to understand "why" something was done

## Output Location

All ADRs go to: `/docs/architecture/decisions/NNNN-title.md`

## Quality Checklist

Before completing:

- [ ] ADR number is sequential (check existing ADRs)
- [ ] Title is clear and descriptive
- [ ] Context explains the problem, not the solution
- [ ] Decision is stated clearly
- [ ] Consequences cover positive, negative, and neutral
- [ ] At least 2 options were considered
- [ ] Related links are included
- [ ] YAML frontmatter has title and description

## Examples

### Creating New ADRs (Will Ask User)

- "Create an ADR for choosing Supabase" → Ask: Confirm number 0001?
- "Record the decision to use TanStack Query" → Suggest next number

### Updating Existing ADRs (Autonomous)

- "Mark ADR-001 as accepted" → Updates status
- "Add implementation notes to ADR-003" → Adds to Notes section
- "Link ADR-002 to ADR-005" → Adds to Related section

### Status Changes

- "Deprecate ADR-002" → Updates status, adds deprecation note
- "ADR-003 supersedes ADR-001" → Updates both ADRs with cross-references
