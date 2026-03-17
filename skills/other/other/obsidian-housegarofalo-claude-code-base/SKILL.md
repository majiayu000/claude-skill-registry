---
name: obsidian
description: Create Obsidian plugins and workflows. Develop custom plugins, templates, and automation for personal knowledge management. Use for Obsidian vault setup, plugin development, Dataview queries, Templater scripts, and PKM systems. Triggers on obsidian, knowledge base, PKM, personal knowledge management, note taking, zettelkasten, dataview, templater.
---

# Obsidian Knowledge Management

Complete guide for Obsidian - knowledge base on local markdown files.

## Quick Reference

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Vault** | Folder containing notes |
| **Note** | Markdown file |
| **Link** | Connection between notes |
| **Tag** | Categorization marker |
| **Graph** | Visual note connections |

### File Structure

```
vault/
+-- .obsidian/           # Settings
|   +-- plugins/
|   +-- themes/
|   +-- workspace.json
+-- Daily Notes/
+-- Templates/
+-- Notes/
```

## Markdown Syntax

### Internal Links

```markdown
[[Note Name]]              # Basic link
[[Note Name|Display Text]] # Link with alias
[[Note Name#Heading]]      # Link to heading
[[Note Name#^block-id]]    # Link to block
![[Note Name]]             # Embed note
![[Note Name#Heading]]     # Embed specific section
```

### Tags

```markdown
#tag #nested/tag           # Inline tags

---
tags: [tag1, tag2]         # YAML frontmatter tags
---
```

### Callouts

```markdown
> [!note]
> This is a note callout

> [!warning]
> This is a warning

> [!tip]
> This is a tip

> [!info]- Collapsed
> This is collapsed by default
```

### Task Lists

```markdown
- [ ] Incomplete task
- [x] Completed task
- [/] In progress
- [-] Cancelled
```

## Frontmatter (YAML)

```yaml
---
title: Note Title
date: 2024-01-15
tags: [tag1, tag2]
aliases: [alias1, alias2]
status: draft
author: Name
---
```

## Templates

### Daily Note Template

```markdown
---
date: {{date}}
tags: [daily]
---

# {{date:dddd, MMMM D, YYYY}}

## Tasks
- [ ]

## Notes

## Journal

---
[[{{date:YYYY-MM-DD|yesterday}}|<- Yesterday]] | [[{{date:YYYY-MM-DD|tomorrow}}|Tomorrow ->]]
```

### Meeting Template

```markdown
---
date: {{date}}
tags: [meeting]
attendees:
type: meeting
---

# Meeting: {{title}}

## Attendees
-

## Agenda
1.

## Notes

## Action Items
- [ ]
```

## Dataview Plugin

### Basic Queries

```dataview
# List all notes with tag
LIST FROM #tag

# Table of notes
TABLE file.ctime as Created, status
FROM "Projects"
WHERE status = "active"
SORT file.ctime DESC

# Task list
TASK FROM "Daily Notes"
WHERE !completed
GROUP BY file.link
```

### Advanced Queries

```dataview
# Books read this year
TABLE rating, author, year
FROM #book
WHERE completed AND year = 2024
SORT rating DESC

# Upcoming deadlines
TABLE due, status
FROM "Tasks"
WHERE due >= date(today) AND due <= date(today) + dur(7 days)
SORT due ASC

# Recent notes
LIST
FROM ""
WHERE file.mday >= date(today) - dur(7 days)
SORT file.mday DESC
LIMIT 10
```

## Templater Plugin

### Basic Syntax

```markdown
<%* /* JavaScript code */ %>
<% /* Output */ %>

# Get current date
<% tp.date.now("YYYY-MM-DD") %>

# Get title
<% tp.file.title %>

# Create date with offset
<% tp.date.now("YYYY-MM-DD", 7) %>

# Cursor position
<% tp.file.cursor() %>
```

### User Prompts

```markdown
<%*
const title = await tp.system.prompt("Enter title");
const type = await tp.system.suggester(
  ["Task", "Note", "Project"],
  ["task", "note", "project"]
);
_%>

# <% title %>
Type: <% type %>
```

### File Operations

```markdown
<%*
// Move file
await tp.file.move("/Archive/" + tp.file.title);

// Rename file
await tp.file.rename("New Name");

// Create file
await tp.file.create_new("Content", "New Note");
%>
```

## Vault Organization

### PARA Method

```
vault/
+-- 1 - Projects/
+-- 2 - Areas/
+-- 3 - Resources/
+-- 4 - Archive/
+-- Templates/
```

### Zettelkasten

```
vault/
+-- Fleeting/
+-- Literature/
+-- Permanent/
+-- Index/
```

## Essential Hotkeys

```
Cmd/Ctrl + N          New note
Cmd/Ctrl + O          Quick switcher
Cmd/Ctrl + P          Command palette
Cmd/Ctrl + Shift + F  Search all files
Cmd/Ctrl + E          Toggle edit/preview
Cmd/Ctrl + G          Open graph view
```

## Essential Plugins

### Core
- Dataview: Database queries
- Templater: Advanced templates
- QuickAdd: Quick captures
- Periodic Notes: Daily/weekly notes
- Calendar: Calendar view

### Productivity
- Tasks: Task management
- Kanban: Kanban boards
- Projects: Project management
- Excalidraw: Drawings

### Organization
- Tag Wrangler: Tag management
- Folder Notes: Folder index
- Auto Link Title: Auto fetch titles
- Note Refactor: Split/merge notes

## Git Backup

```bash
# .gitignore
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/plugins/*/data.json
.trash/
```

## Best Practices

1. **Regular backups** - Git or sync service
2. **Consistent naming** - Use conventions
3. **Use templates** - Speed up note creation
4. **Link liberally** - Build knowledge graph
5. **Daily notes** - Capture everything
6. **Review regularly** - Process inbox
7. **Minimal plugins** - Only what you need
8. **Frontmatter** - Structured metadata
9. **Atomic notes** - One idea per note
10. **Document workflows** - Create guides for yourself

## When to Use This Skill

- Setting up Obsidian vaults
- Creating templates and workflows
- Writing Dataview queries
- Developing Templater scripts
- Organizing knowledge bases
- Building PKM systems
