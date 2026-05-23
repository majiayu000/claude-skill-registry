---
name: create-rfc
description: Create a new RFC (Request for Comments) technical specification
argument-hint: <rfc-title>
---

# create-rfc

**Category**: Technical Architecture

## Usage

```bash
/create-rfc <rfc-title>
```

## Arguments

- `<rfc-title>`: Required - Short descriptive title for the RFC (will be kebab-cased for filename)

## Execution Instructions

When this command is run, Claude Code should:

1. **Determine RFC Number**
   - Scan `rfcs/` directory (all subdirectories) for existing RFC files
   - Find highest RFC number (RFC-XXXX pattern)
   - Increment by 1 for new RFC
   - If no RFCs exist, start with RFC-0001

2. **Create Directory Structure** (if not exists)
   ```
   rfcs/
   ├── draft/
   ├── review/
   ├── approved/
   │   └── in-progress/
   ├── completed/
   └── archive/
   ```

3. **Generate RFC File**
   - Convert title to kebab-case: "API Gateway Selection" → "api-gateway-selection"
   - Create file: `rfcs/draft/RFC-XXXX-<kebab-title>.md`
   - Use template from skill references

4. **Populate Metadata**
   - Set `rfc_id` to new number
   - Set `title` from argument
   - Set `status` to DRAFT
   - Set `created` and `last_updated` to today's date
   - Leave `author` for user to fill

5. **Confirm Creation**
   ```
   Created RFC-XXXX: <title>

   Location: rfcs/draft/RFC-XXXX-<kebab-title>.md
   Status: DRAFT

   Next steps:
   1. Fill in the Overview and Problem Statement sections
   2. Define your Evaluation Criteria before analyzing options
   3. Analyze at least 2 options objectively
   4. When ready for review: /rfc-status RFC-XXXX --set REVIEW
   ```

## Template Reference

Use the template from:
`plugins/devops-data/skills/rfc-specification/references/rfc-template.md`

## Example Usage

```bash
/create-rfc API Gateway Selection
```

Creates: `rfcs/draft/RFC-0001-api-gateway-selection.md`

```bash
/create-rfc Database Migration Strategy
```

Creates: `rfcs/draft/RFC-0002-database-migration-strategy.md`

## Validation

- Title must be provided (not empty)
- Title should be 2-6 words for clarity
- Warn if similar RFC already exists (fuzzy match on title)

## Error Handling

- If `rfcs/` directory doesn't exist, create it with full structure
- If title is empty, prompt user for title
- If similar RFC exists, ask for confirmation before creating
