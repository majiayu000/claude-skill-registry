---
name: create-clickup-task
description: Create ClickUp tasks with proper formatting, task types, custom fields, and assignment. Use when the user wants to create a task, bug, feature, or ticket in ClickUp, or when they mention Sprint planning or task tracking.
---

# Create ClickUp Task

This skill creates well-structured ClickUp tasks using the ClickUp MCP tools.

## Instructions

### Step 1: Gather task information

Ask clarifying questions if any required information is missing:

1. **Task name** - Clear, concise title (will be prefixed with appropriate emoji)
2. **Task Type** - Task (default) or Bug. **Important:** This is different from Value Stream!
3. **Description** - User story, problem statement, and/or solution details
4. **Sprint/List** - Which sprint or list to add the task to (e.g., "Sprint 119")
5. **Priority** - Urgent (1), High (2), Normal (3), or Low (4). Default: Normal
6. **Status** - Default: "Ready to Start"
7. **Assignee** - Who should be assigned (can search by name or email)
8. **Value Stream** - Bug, Internal Enhancement, External Enhancement, Differentiator, Must Have, etc.
9. **Requested By/Affects Clients** - RSF, Falcon, PGW, LVLup, Buho, PTAC, All Clients, etc.

### Step 2: Determine Task Type

ClickUp has a "Task Type" feature (shown as `custom_item_id` in the API). This is separate from the "Value Stream" custom field.

**Task Types:**
| Type | custom_item_id |
|------|----------------|
| Task | 0 (default) |
| Bug | 1001 |

**When to use Bug type:**
- Defects in existing functionality
- Unexpected behavior reported by users
- Issues that need fixing (not new features)

**When to use Task type:**
- New features
- Enhancements
- Documentation
- Refactoring
- General work items

### Step 3: Format the task

#### Task Name
Prefix with an appropriate emoji based on type:
- Bug: `Fix...` or `Ignore...` (no emoji needed - the Bug type provides the icon)
- Feature: `Add...` or `Implement...`
- Enhancement: `Improve...` or `Optimize...`
- Documentation: `Document...`
- Refactor: `Refactor...`

#### Description Format
Use this markdown template for the description:

```markdown
**As a** [role],
**I want** [capability],
**So that** [benefit].

# Problem Statement

[Describe the problem, include evidence, examples, or references]

# Solution

[Describe the proposed solution and implementation approach]

# Files to Modify

| File | Change |
|------|--------|
| `path/to/file.php` | Description of change |

# Acceptance Criteria

1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]
```

### Step 4: Find the list and assignee

1. **Find the Sprint list**: Use `ClickUp_get_task` with `taskName` like "Sprint NNN" to find the list ID
2. **Find the assignee**: Use `ClickUp_find_member_by_name` to get the user ID

### Step 5: Create the task

Use `ClickUp_create_task` with:
- `name`: Task name (emoji optional - Bug type provides its own icon)
- `listId`: The sprint list ID (preferred over listName)
- `priority`: 1-4 (1=urgent, 4=low)
- `status`: "Ready to Start" (or as specified)
- `assignees`: Array with user ID, e.g., `[2685610]`
- `markdown_description`: Full formatted description
- `custom_item_id`: Task type ID - use `1001` for Bug type, omit or use `0` for regular Task

**Note:** If the `custom_item_id` parameter is not supported by the MCP tool, inform the user that they will need to manually change the Task Type to "Bug" in ClickUp after creation, or the MCP server needs to be updated to support this parameter.

### Step 6: Set custom fields

Use `ClickUp_update_task` to set custom fields:

**Value Stream** (field ID: `49ed7876-0e5f-490e-9cdc-612252997997`):
| Value | Option ID |
|-------|-----------|
| Unknown | `25db8568-9947-4c4f-832d-6f6a4ffa0803` |
| Internal Enhancement | `1e60663d-a01b-4581-8ca9-219d26d539be` |
| External Enhancement | `ed07ceef-8c34-4efa-a18c-e89eeca305ab` |
| Differentiator | `d7ee22ad-2c5d-4bd8-a1a6-426654dca26b` |
| Bug | `4499c3b7-49da-43cd-ad38-f082a56079ef` |
| Must Have | `2901a6cb-07c7-4a15-a0d0-bbe493cf18c1` |
| Who Needs This | `f60e06ad-8f18-4a23-92e8-c31b2f365b9d` |

**Requested By/Affects Clients** (field ID: `40acbf4e-77be-4e77-a0f6-d38b448c2804`):
| Value | Option ID |
|-------|-----------|
| All Clients | `cabb4354-4d0f-480d-9815-d064b6d36e18` |
| RSF | `927a2f33-0026-40df-971b-a21d1395ac58` |
| Falcon | `20473328-70f7-44a8-a99f-f900616517c2` |
| PGW | `edfe590f-d6de-40ef-a8d5-92c2324fd17a` |
| LVLup | `d83b46b3-759f-4f76-82bd-b18562657d3b` |
| Buho | `208ddc4a-3d8a-47fa-9a3f-e6878eb92996` |
| PTAC | `7bb112be-0514-46e9-ba02-0d1d0b148ce0` |
| Prospects | `8616a602-348d-4fe5-9688-b580cd39d3e9` |
| R&S Logistics | `a8833d5d-4646-4c5a-ba24-b3f25241f200` |
| LuckyGunner | `22a6d2ec-b7bc-409d-a071-eafb8492e7fc` |
| RSD | `341e41d8-7f20-4132-8e0c-8926e377d90a` |

Example update call:
```
custom_fields: [
  {"id": "49ed7876-0e5f-490e-9cdc-612252997997", "value": "4499c3b7-49da-43cd-ad38-f082a56079ef"},
  {"id": "40acbf4e-77be-4e77-a0f6-d38b448c2804", "value": ["927a2f33-0026-40df-971b-a21d1395ac58"]}
]
```

### Step 7: Report the result

After creating the task, provide a summary:

```
**ClickUp Task Created:**

| Field | Value |
|-------|-------|
| **ID** | DEV-XXXX |
| **Name** | Task name |
| **Type** | Bug |
| **List** | Sprint NNN |
| **Status** | Ready to Start |
| **Priority** | Normal |
| **Assignee** | Name |
| **Value Stream** | Bug |
| **Requested By** | RSF |

**URL:** https://app.clickup.com/t/XXXXXXXX
```

## Common team members

| Name | User ID |
|------|---------|
| Colin | 2685610 |

Use `ClickUp_find_member_by_name` to find other team members by name or email.

## Tips

- Always use `listId` instead of `listName` when you have it - it's faster and more reliable
- The Sprint list name format is typically "Sprint NNN (MM/DD - MM/DD)"
- **For bugs:** Set BOTH Task Type to Bug (`custom_item_id: 1001`) AND Value Stream to "Bug"
- For client-reported issues, set the appropriate client in "Requested By/Affects Clients"
- Custom field values for dropdowns use the option ID, not the display name
- Custom field values for labels (like "Requested By") take an array of option IDs
- Task Type (Bug vs Task) is different from Value Stream - both should be set appropriately
