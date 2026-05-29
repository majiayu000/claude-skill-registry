---
name: interface-management
description: Manage Interface specifications with CRUD operations, automatic numbering, and AsciiDoc formatting
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, Skill
---

# Interface Management Skill

Manage Interface specifications stored in `doc/interfaces/` directory.

## Purpose

Provide structured management of interface documentation:

- **Create** interface specs with automatic numbering and template
- **Read** interface content by number
- **Update** interface specifications
- **Delete** interfaces when necessary
- **List** all interfaces with optional filtering
- **Validate** interface format using cui-documentation

## Available Workflows

| Workflow | Purpose | Script Used |
|----------|---------|-------------|
| **list-interfaces** | List all interfaces with optional filtering | `manage-interface.py list` |
| **create-interface** | Create new interface from template | `manage-interface.py create` |
| **read-interface** | Read interface content | `manage-interface.py read` |
| **update-interface** | Update interface content | `manage-interface.py update` |
| **delete-interface** | Delete interface (with confirmation) | `manage-interface.py delete` |
| **validate-interface** | Validate interface format | cui-documentation workflows |

## Workflow: list-interfaces

List all interfaces with optional type filtering.

### Parameters

- `type` (optional): Filter by type (REST_API, Event, gRPC, Database, File, Other)

### Steps

**Step 1: Execute List**

```bash
python3 .plan/execute-script.py pm-documents:interface-management:manage-interface list [--type {type}]
```

**Step 3: Parse Output**

Parse JSON output containing interface list with metadata.

### Output

```json
{
  "success": true,
  "operation": "list",
  "count": 2,
  "interfaces": [
    {"number": 1, "title": "User Service API", "type": "REST_API", "path": "doc/interfaces/001-User_Service_API.adoc"},
    {"number": 2, "title": "Event Bus", "type": "Event", "path": "doc/interfaces/002-Event_Bus.adoc"}
  ]
}
```

## Workflow: create-interface

Create a new interface specification with automatic numbering.

### Parameters

- `title` (required): Interface name
- `type` (required): Interface type (REST_API, Event, gRPC, Database, File, Other)

### Steps

**Step 1: Create Interface**

```bash
python3 .plan/execute-script.py pm-documents:interface-management:manage-interface create --title "{title}" --type "{type}"
```

**Step 3: Parse Output**

Extract created file path from JSON output.

**Step 4: Open for Editing**

Read the created file and inform user to fill in content sections.

**Step 5: Validate Format**

```
Skill: pm-documents:cui-documentation
Execute workflow: validate-format
Parameters:
  target: {created_path}
```

### Output

```
Interface Created: doc/interfaces/003-{title}.adoc
Number: INTER-003
Type: REST_API

Next steps:
1. Edit doc/interfaces/003-{title}.adoc to fill in:
   - Contract definition (request/response)
   - Error handling
   - Authentication requirements
   - Examples
2. Add consumers and providers
```

## Workflow: read-interface

Read interface content by number.

### Parameters

- `number` (required): Interface number (1, 2, 3, etc.)

### Steps

**Step 1: Read Interface**

```bash
python3 .plan/execute-script.py pm-documents:interface-management:manage-interface read --number {number}
```

**Step 3: Display Content**

Show interface metadata and content to user.

## Workflow: update-interface

Update interface field content.

### Parameters

- `number` (required): Interface number
- `field` (required): Field to update (overview, type, input, output, errors, auth, versioning, consumers, providers)
- `value` (required): New value for the field

### Steps

**Step 1: Update Interface**

```bash
python3 .plan/execute-script.py pm-documents:interface-management:manage-interface update --number {number} --field {field} --value "{value}"
```

**Step 3: Confirm Update**

Report updated field to user.

## Workflow: delete-interface

Delete interface with confirmation.

### Parameters

- `number` (required): Interface number
- `force` (required): Must be true to confirm deletion

### Steps

**Step 1: Delete Interface**

```bash
python3 .plan/execute-script.py pm-documents:interface-management:manage-interface delete --number {number} --force
```

**Step 3: Confirm Deletion**

Report deletion to user.

## Workflow: validate-interface

Validate interface format using cui-documentation skill.

### Parameters

- `number` (required): Interface number to validate

### Steps

**Step 1: Find Interface Path**

Use list-interfaces workflow to get interface path by number.

**Step 2: Validate Format**

```
Skill: pm-documents:cui-documentation
Execute workflow: validate-format
Parameters:
  target: {interface_path}
```

**Step 3: Report Results**

Report validation results to user.

## Integration with cui-documentation

This skill integrates with `cui-documentation` for:

- **Format validation**: Ensures AsciiDoc formatting compliance
- **Link verification**: Validates cross-references
- **Content review**: Reviews interface content quality

## Interface Types

| Type | Description |
|------|-------------|
| REST_API | HTTP/REST service endpoints |
| Event | Event-driven message contracts |
| gRPC | gRPC service and message definitions |
| Database | Database schema and access contracts |
| File | File format and exchange specifications |
| Other | Other interface types |

## Interface Template Structure

Each interface specification contains these sections:

1. **Overview** - Brief description of the interface
2. **Interface Type** - REST_API, Event, gRPC, Database, File, Other
3. **Contract Definition** - Request/Input, Response/Output, Error Handling
4. **Authentication & Authorization** - Security requirements
5. **Versioning** - Version strategy and compatibility
6. **Examples** - Request and response examples
7. **Consumers** - Systems that consume this interface
8. **Providers** - Systems that provide this interface
9. **References** - Related documents and links

## File Naming Convention

Interfaces follow this naming pattern:

```
doc/interfaces/{NNN}-{Title_With_Underscores}.adoc
```

Examples:
- `doc/interfaces/001-User_Service_API.adoc`
- `doc/interfaces/002-Event_Bus_Interface.adoc`
- `doc/interfaces/003-Database_Schema_V2.adoc`

## References

- [cui-documentation SKILL](../cui-documentation/SKILL.md) - Format validation
