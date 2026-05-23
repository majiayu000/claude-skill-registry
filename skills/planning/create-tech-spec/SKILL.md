---
name: create-tech-spec
description: Create a new Technical Specification for implementation details
argument-hint: <spec-title> [--rfc RFC-XXXX]
---

# create-tech-spec

**Category**: Technical Architecture

## Usage

```bash
/create-tech-spec <spec-title> [--rfc RFC-XXXX]
```

## Arguments

- `<spec-title>`: Required - Descriptive title for the Tech Spec (will be kebab-cased for filename)
- `--rfc RFC-XXXX`: Optional - Link to RFC that this spec implements

## Execution Instructions

When this command is run, Claude Code should:

1. **Determine Tech Spec Number**
   - Scan `tech-specs/` directory (all subdirectories) for existing files
   - Find highest TS-XXXX number
   - Increment by 1 for new spec
   - If no specs exist, start with TS-0001

2. **Create Directory Structure** (if not exists)
   ```
   tech-specs/
   ├── draft/
   ├── approved/
   ├── reference/
   └── archive/
       └── YYYY/
   ```

3. **Generate Tech Spec File**
   - Convert title to kebab-case: "User Authentication API" → "user-authentication-api"
   - Create file: `tech-specs/draft/TS-XXXX-<kebab-title>.md`
   - Use template from skill references

4. **Populate Metadata**
   - Set `tech_spec_id` to new number
   - Set `title` from argument
   - Set `status` to DRAFT
   - Set `decision_ref` to RFC if provided
   - Set `created` and `last_updated` to today's date
   - Leave `author` for user to fill

5. **If RFC provided, validate and link**
   - Check RFC exists
   - Add link in metadata
   - Suggest copying relevant technical details from RFC

6. **Confirm Creation**
   ```
   Created TS-XXXX: <title>

   Location: tech-specs/draft/TS-XXXX-<kebab-title>.md
   Status: DRAFT
   RFC Link: RFC-XXXX (if provided)

   Next steps:
   1. Fill in the Executive Summary
   2. Document the Design Overview with architecture diagram
   3. Complete API and Data Model sections
   4. When ready: /tech-spec-status TS-XXXX --set APPROVED
   ```

## Template Reference

Use the template from:
`plugins/devops-data/skills/technical-specification/references/tech-spec-template.md`

## Example Usage

```bash
# Standalone tech spec
/create-tech-spec User Authentication API

# Tech spec implementing an RFC
/create-tech-spec Payment Gateway Integration --rfc RFC-0042
```

Creates:
- `tech-specs/draft/TS-0001-user-authentication-api.md`
- `tech-specs/draft/TS-0002-payment-gateway-integration.md`

## Validation

- Title must be provided (not empty)
- Title should be 2-6 words for clarity
- If RFC provided, verify it exists and is APPROVED
- Warn if similar Tech Spec already exists

## Error Handling

- If `tech-specs/` directory doesn't exist, create it with full structure
- If title is empty, prompt user for title
- If RFC not found, warn but allow creation
- If similar spec exists, ask for confirmation
