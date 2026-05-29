---
name: manage-adr
description: Manage Architectural Decision Records (ADRs) with CRUD operations, automatic numbering, and AsciiDoc formatting
user-invocable: false
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, Skill
---

# ADR Management Skill

Manage Architectural Decision Records (ADRs) stored in `doc/adr/` directory.

## Purpose

Provide structured management of architectural decisions:

- **Create** ADRs with automatic numbering and template
- **Read** ADR content by number
- **Update** ADR status through lifecycle
- **Delete** ADRs when necessary
- **List** all ADRs with optional filtering
- **Validate** ADR format using ref-documentation

## Available Workflows

| Workflow | Purpose | Script Used |
|----------|---------|-------------|
| **list-adrs** | List all ADRs with optional filtering | `manage-adr.py list` |
| **create-adr** | Create new ADR from template | `manage-adr.py create` |
| **read-adr** | Read ADR content | `manage-adr.py read` |
| **update-adr** | Update ADR status | `manage-adr.py update` |
| **delete-adr** | Delete ADR (with confirmation) | `manage-adr.py delete` |
| **validate-adr** | Validate ADR format | ref-documentation workflows |

## Workflow: list-adrs

List all ADRs with optional status filtering.

### Parameters

- `status` (optional): Filter by status (Proposed, Accepted, Deprecated, Superseded)

### Steps

**Step 1: Execute List**

```bash
python3 .plan/execute-script.py pm-documents:manage-adr:manage-adr list [--status {status}]
```

**Step 3: Parse Output**

Parse JSON output containing ADR list with metadata.

### Output

```json
{
  "success": true,
  "operation": "list",
  "count": 3,
  "adrs": [
    {"number": 1, "title": "Use PostgreSQL", "status": "Accepted", "path": "doc/adr/001-Use_PostgreSQL.adoc"},
    {"number": 2, "title": "Adopt Quarkus", "status": "Proposed", "path": "doc/adr/002-Adopt_Quarkus.adoc"}
  ]
}
```

## Workflow: create-adr

Create a new ADR with automatic numbering.

### Parameters

- `title` (required): ADR title
- `status` (optional, default: "Proposed"): Initial status

### Steps

**Step 1: Create ADR**

```bash
python3 .plan/execute-script.py pm-documents:manage-adr:manage-adr create --title "{title}" [--status "{status}"]
```

**Step 3: Parse Output**

Extract created file path from JSON output.

**Step 4: Open for Editing**

Read the created file and inform user to fill in content sections.

**Step 5: Validate Format**

```
Skill: pm-documents:ref-documentation
Execute workflow: validate-format
Parameters:
  target: {created_path}
```

### Output

```
ADR Created: doc/adr/004-{title}.adoc
Number: ADR-004
Status: Proposed

Next steps:
1. Edit doc/adr/004-{title}.adoc to fill in:
   - Context
   - Decision
   - Consequences
   - Alternatives
2. Update status to "Accepted" when approved
```

## Workflow: read-adr

Read ADR content by number.

### Parameters

- `number` (required): ADR number (1, 2, 3, etc.)

### Steps

**Step 1: Read ADR**

```bash
python3 .plan/execute-script.py pm-documents:manage-adr:manage-adr read --number {number}
```

**Step 3: Display Content**

Show ADR metadata and content to user.

## Workflow: update-adr

Update ADR status through lifecycle.

### Parameters

- `number` (required): ADR number
- `status` (required): New status (Proposed, Accepted, Deprecated, Superseded)

### Steps

**Step 1: Update ADR**

```bash
python3 .plan/execute-script.py pm-documents:manage-adr:manage-adr update --number {number} --status {status}
```

**Step 3: Confirm Update**

Report updated status to user.

## Workflow: delete-adr

Delete ADR with confirmation.

### Parameters

- `number` (required): ADR number
- `force` (required): Must be true to confirm deletion

### Steps

**Step 1: Delete ADR**

```bash
python3 .plan/execute-script.py pm-documents:manage-adr:manage-adr delete --number {number} --force
```

**Step 3: Confirm Deletion**

Report deletion to user.

## Workflow: validate-adr

Validate ADR format using ref-documentation skill.

### Parameters

- `number` (required): ADR number to validate

### Steps

**Step 1: Find ADR Path**

Use list-adrs workflow to get ADR path by number.

**Step 2: Validate Format**

```
Skill: pm-documents:ref-documentation
Execute workflow: validate-format
Parameters:
  target: {adr_path}
```

**Step 3: Report Results**

Report validation results to user.

## Integration with ref-documentation

This skill integrates with `ref-documentation` for:

- **Format validation**: Ensures AsciiDoc formatting compliance
- **Link verification**: Validates cross-references
- **Content review**: Reviews ADR content quality

## ADR Lifecycle

```
Proposed → Accepted → [Deprecated | Superseded]
```

| Status | Meaning |
|--------|---------|
| Proposed | Under discussion, not yet approved |
| Accepted | Approved and active |
| Deprecated | No longer relevant or applicable |
| Superseded | Replaced by another ADR |

## ADR Template Structure

Each ADR contains these sections:

1. **Status** - Current lifecycle status
2. **Context** - Problem context and background
3. **Decision** - The architectural decision made
4. **Consequences** - Positive, negative outcomes and risks
5. **Alternatives Considered** - Options that were not chosen
6. **References** - Related documents and links

## File Naming Convention

ADRs follow this naming pattern:

```
doc/adr/{NNN}-{Title_With_Underscores}.adoc
```

Examples:
- `doc/adr/001-Use_PostgreSQL_for_Persistence.adoc`
- `doc/adr/002-Adopt_Quarkus_Framework.adoc`
- `doc/adr/003-Implement_CQRS_Pattern.adoc`

## References

- [ref-documentation SKILL](../ref-documentation/SKILL.md) - Format validation
