---
name: document-format
description: Create properly formatted documents for the knowledge base. Use when creating tasks, projects, bookmarks, companies, meetings, people, or research entries. Provides templates, frontmatter schemas, and management guidelines for each document type in the Database system.
---

# Document Format

Create documents following workspace conventions and schemas defined in the Database system.

## Overview

This workspace uses a structured Database system with well-defined schemas for different document types. All schemas, templates, and conventions are maintained in [`Database/Schemas/`](../../../Database/Schemas/).

**When to use this skill:**
- Creating new tasks, projects, meetings, people, companies, or bookmarks
- Understanding how to structure document frontmatter
- Learning when to create and update specific document types
- Following workspace conventions for file naming and linking

## Quick Start

1. **Identify the document type** you need to create (task, project, person, etc.)
2. **Read the schema** from `Database/Schemas/README.md` to see all available types
3. **Navigate to the specific schema folder** (e.g., `Database/Schemas/Task/`)
4. **Read the schema README** for complete specifications and examples
5. **Use the template** provided in that folder to create your document

## Loading Schemas

### Schema Index

Start by reading the schema index to understand available document types:

```
Database/Schemas/README.md
```

This index provides:
- Complete list of available schemas
- Quick reference table with locations and descriptions
- Guidelines for creating new schemas
- Common frontmatter patterns
- Integration with Obsidian Bases

### Individual Schemas

Each schema is documented in its own folder:

```
Database/Schemas/
├── Task/
│   ├── README.md      # Complete schema specification
│   └── template.md    # Ready-to-use template
├── Project/
│   ├── README.md
│   └── template.md
├── Person/
│   ├── README.md
│   └── template.md
├── Company/
│   ├── README.md
│   └── template.md
├── Meeting/
│   ├── README.md
│   └── template.md
├── Bookmark/
│   ├── README.md
│   └── template.md
└── Document/
    ├── README.md
    ├── template-research.md
    └── template-prd.md
```

## Schema Documentation Structure

Each schema README includes:

1. **Location** - Where documents of this type are stored
2. **Filename Convention** - How to name new files
3. **When to Create** - Triggers and scenarios for creating this document type
4. **When to Update** - What changes should trigger updates
5. **Frontmatter Schema** - Required and optional properties with types
6. **Tag Conventions** - Standardized tagging patterns
7. **Viewing Documents** - Available Obsidian Bases views
8. **Best Practices** - Common patterns and recommendations
9. **Examples** - Real-world examples with different configurations

## Workflow for Creating Documents

### Step 1: Load the Schema

Read the appropriate schema README:
```
Database/Schemas/[Type]/README.md
```

Example: For creating a task, read `Database/Schemas/Task/README.md`

### Step 2: Copy the Template

Use the template as a starting point:
```
Database/Schemas/[Type]/template.md
```

### Step 3: Fill in Properties

Follow the schema specification:
- Add all **required properties**
- Add **optional properties** as needed
- Use correct **property types** (string, date, wikilink, array, enum)
- Follow **tag conventions**
- Use proper **filename convention**

### Step 4: Save in Correct Location

Place the file in the appropriate Database folder:
```
Database/[Types]/Your-File-Name.md
```

## Common Conventions

### Frontmatter Requirements

All Database documents must include:
```yaml
---
type: documenttype  # Required: task, project, person, company, meeting, bookmark
created: YYYY-MM-DD # Recommended: ISO 8601 date format
tags: [...]         # Recommended: for filtering
---
```

### Linking Between Documents

Use wikilinks to create relationships:
```yaml
# Link to a person
assignee: "[[Database/People/Team-Member]]"

# Link to a project
project: "[[Database/Projects/AGI-Assistant]]"

# Link to multiple items
team:
  - "[[Database/People/Person-One]]"
  - "[[Database/People/Person-Two]]"
```

### File Naming Patterns

Follow consistent naming based on document type:
- **Tasks**: Descriptive title case: `Integrate-Zep-Memory.md`
- **Projects**: Project name: `AGI-Assistant.md`
- **People**: First-Last: `Alice-Smith.md`
- **Companies**: Company name: `Placeholder-Labs.md`
- **Meetings**: Date-based: `2026-01-15-Meeting-Title.md`
- **Bookmarks**: Descriptive: `Claude-API-Docs.md`

### Date Formats

Always use ISO 8601 (YYYY-MM-DD):
```yaml
created: 2026-01-15
due: 2026-01-31
meeting_date: 2026-01-20
```

## Schema Extension

To create a new document type or modify existing schemas:

1. Read `Database/Schemas/README.md` section "Creating a New Schema"
2. Follow the documented structure for schema folders
3. Include README.md with complete specification
4. Provide template.md for easy document creation
5. Create corresponding `.base` file for Obsidian Bases views
6. Update the schema index

## Integration with Obsidian Bases

All schemas are designed to work with Obsidian Bases plugin:

- **Filter** documents by frontmatter properties
- **Group** by status, priority, person, project, etc.
- **Sort** by dates, priorities, or custom fields
- **View** as tables, kanbans, cards, or lists
- **Query** related documents using relationship fields

Each document type has pre-configured views in `Database/[Types].base` files.

## Best Practices

1. **Always read the schema first** - Don't guess frontmatter properties
2. **Use templates** - Start from provided templates to ensure consistency
3. **Maintain relationships** - Link related documents for bidirectional navigation
4. **Update frontmatter** - Keep metadata current (status, dates, counters)
5. **Follow conventions** - Use standardized naming, tagging, and linking patterns
6. **Leverage queries** - Use embedded Base queries to show related data inline

## Examples

### Creating a Task

1. Read `Database/Schemas/Task/README.md`
2. Copy from `Database/Schemas/Task/template.md`
3. Fill in required properties (type, status, priority, assignee, created)
4. Add optional properties (project, due, blocked_by)
5. Save to `Database/Tasks/Your-Task-Name.md`

### Creating a Project

1. Read `Database/Schemas/Project/README.md`
2. Copy from `Database/Schemas/Project/template.md`
3. Fill in required properties (type, status, priority, lead, total_tasks, completed_tasks)
4. Add optional properties (team, start_date, target_date, budget)
5. Save to `Database/Projects/Your-Project-Name.md`

### Creating a Person

1. Read `Database/Schemas/Person/README.md`
2. Copy from `Database/Schemas/Person/template.md`
3. Determine person type (team member, external contact, industry leader)
4. Fill in appropriate properties for that type
5. Save to `Database/People/First-Last.md` or `Team/First-Last.md`

## Troubleshooting

**Q: Which schema should I use?**
A: Read `Database/Schemas/README.md` - it has a table mapping use cases to schemas.

**Q: What if none of the schemas fit?**
A: Check if `Database/Schemas/Document/` (free-form content) works, or propose a new schema following the extension guidelines.

**Q: How do I create skills for workflows or automations?**
A: Skills go in `Database/Skills/` (not schemas). Use the `/skill-creator` skill to create user-editable skills. Add `cron` frontmatter field for scheduled execution (e.g., `cron: "0 9 * * 1-5"` for weekdays at 9am).

**Q: How do I know what properties are required?**
A: Each schema README has a "Frontmatter Schema" section with required vs optional properties.

**Q: Can I add custom properties?**
A: Yes, schemas define minimum required properties. You can add additional properties as needed.

**Q: How do I link documents together?**
A: Use wikilinks in frontmatter: `project: "[[Database/Projects/Project-Name]]"`. See schema READMEs for relationship fields.

## Summary

This skill helps you create properly formatted documents by:
1. Directing you to schema documentation in `Database/Schemas/`
2. Explaining how to read and use schema specifications
3. Providing templates and examples
4. Enforcing workspace conventions

Always start by loading the schema index, then read the specific schema README for the document type you're creating.
