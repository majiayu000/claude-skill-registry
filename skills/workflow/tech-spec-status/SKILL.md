---
name: tech-spec-status
description: Show Tech Spec details or update status through lifecycle
argument-hint: <spec-id> [--set <status>]
---

# tech-spec-status

**Category**: Technical Architecture

## Usage

```bash
/tech-spec-status <spec-id> [options]
```

## Arguments

- `<spec-id>`: Required - Tech Spec identifier (e.g., TS-0042 or just 0042)

## Options

| Option | Description |
|--------|-------------|
| `--set <status>` | Transition to new status |
| `--link-rfc <RFC-XXXX>` | Link to an RFC |

## Valid Statuses

- `DRAFT` - Being written
- `APPROVED` - Ready for implementation
- `REFERENCE` - Implementation complete
- `ARCHIVED` - Superseded or deprecated

## Execution Instructions

### View Status (no --set)

When viewing a Tech Spec:

1. **Find the Spec file**
   - Search all `tech-specs/` subdirectories
   - Match by Spec ID in filename or frontmatter

2. **Display Spec Details**

```
TS-0042: Payment Gateway Integration
======================================

Status:      APPROVED
Author:      Jane Doe
Created:     2025-12-01
Updated:     2025-12-05
RFC Link:    RFC-0042
Location:    tech-specs/approved/TS-0042-payment-gateway-integration.md

Summary:
  [First 2-3 sentences of the Executive Summary]

Valid Transitions:
  → REFERENCE  (implementation complete)
  → ARCHIVED   (superseded or deprecated)

Commands:
  /tech-spec-status TS-0042 --set REFERENCE
```

### Update Status (with --set)

When updating status:

1. **Validate Transition**

   Valid transitions:
   | From | To |
   |------|-----|
   | DRAFT | APPROVED |
   | APPROVED | REFERENCE, ARCHIVED |
   | REFERENCE | ARCHIVED |

2. **Perform Pre-transition Checks**

   For DRAFT → APPROVED:
   - Check all required sections are complete
   - Warn if placeholders remain
   - Suggest running checklist

   For APPROVED → REFERENCE:
   - Ask for implementation link (repo, PR)
   - Ask about deviations from spec

   For any → ARCHIVED:
   - Prompt for archive reason
   - Ask for link to replacement spec (if superseded)

3. **Update Spec File**
   - Update `status` in frontmatter
   - Update `last_updated` to today
   - Add `archive_date` if archiving
   - Add `archive_reason` if archiving

4. **Move File to Correct Directory**

   | Status | Directory |
   |--------|-----------|
   | DRAFT | `tech-specs/draft/` |
   | APPROVED | `tech-specs/approved/` |
   | REFERENCE | `tech-specs/reference/` |
   | ARCHIVED | `tech-specs/archive/YYYY/` |

5. **Confirm Update**

```
TS-0042 status updated: APPROVED → REFERENCE

Updated:
  - Status: REFERENCE
  - Location: tech-specs/reference/TS-0042-payment-gateway-integration.md

The spec now serves as reference documentation for the implementation.
```

## RFC Linking

Add or update RFC link:

```bash
/tech-spec-status TS-0042 --link-rfc RFC-0042
```

This updates the `decision_ref` field in the spec's frontmatter.

## Example Usage

```bash
# View spec details
/tech-spec-status TS-0042

# Mark as approved (ready for implementation)
/tech-spec-status TS-0042 --set APPROVED

# Mark as reference (implementation complete)
/tech-spec-status TS-0042 --set REFERENCE

# Archive (superseded)
/tech-spec-status TS-0042 --set ARCHIVED

# Link to RFC
/tech-spec-status TS-0042 --link-rfc RFC-0042
```

## Error Handling

- If spec not found, show search suggestions
- If invalid transition, show valid options
- If file move fails, show manual instructions
- Preserve git history when moving files (use `git mv`)

## Lifecycle Summary

```
DRAFT ─────────────▶ APPROVED
(writing)             (ready)
                         │
                         ▼
                     REFERENCE
                     (implemented)
                         │
                         ▼
                     ARCHIVED
                     (deprecated)
```
