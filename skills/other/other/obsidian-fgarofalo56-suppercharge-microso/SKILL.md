---
name: obsidian
description: "Create Obsidian plugins and workflows. Develop custom plugins, templates, and automation for personal knowledge management. Use for Obsidian development and PKM systems."
---

# Obsidian Skill

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
├── .obsidian/           # Settings
│   ├── plugins/
│   ├── themes/
│   └── workspace.json
├── Daily Notes/
├── Templates/
└── Notes/
```

---

## 1. Markdown Syntax

### Internal Links
```markdown
# Basic link
[[Note Name]]

# Link with alias
[[Note Name|Display Text]]

# Link to heading
[[Note Name#Heading]]

# Link to block
[[Note Name#^block-id]]

# Embed note
![[Note Name]]

# Embed specific section
![[Note Name#Heading]]
```

### Tags
```markdown
# Inline tag
#tag #nested/tag

# YAML frontmatter tags
---
tags: [tag1, tag2, nested/tag]
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

> [!question]+ Expanded
> This is expanded by default
```

### Task Lists
```markdown
- [ ] Incomplete task
- [x] Completed task
- [/] In progress
- [-] Cancelled
```

---

## 2. Frontmatter (YAML)

### Common Properties
```yaml
---
title: Note Title
date: 2024-01-15
tags: [tag1, tag2]
aliases: [alias1, alias2]
cssclass: custom-class
created: 2024-01-15T10:30:00
modified: 2024-01-16T14:20:00
status: draft
author: Name
---
```

### For Dataview Queries
```yaml
---
type: book
rating: 5
year: 2024
completed: true
---
```

---

## 3. Templates

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
[[{{date:YYYY-MM-DD|yesterday}}|← Yesterday]] | [[{{date:YYYY-MM-DD|tomorrow}}|Tomorrow →]]
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

## Next Steps
```

### Project Template
```markdown
---
date: {{date}}
tags: [project]
status: active
priority: medium
---

# {{title}}

## Overview

## Goals
- [ ]

## Tasks
- [ ]

## Resources

## Notes

## Log
### {{date}}
-
```

---

## 4. Dataview Plugin

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

### Inline Queries
```markdown
Total books: `= length(filter(this.file.tasks, (t) => t.completed))`

Today: `= date(today)`

Files in folder: `= length(filter(pages, (p) => p.file.folder = "Notes"))`
```

---

## 5. Templater Plugin

### Basic Syntax
```markdown
<%* /* JavaScript code */ %>
<% /* Output */ %>
<%+ /* Whitespace control */ %>

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

// Get file content
const content = await tp.file.content;
%>
```

### Conditional Logic
```markdown
<%* if (tp.file.tags.includes("daily")) { %>
## Daily Tasks
<%* } else { %>
## General Notes
<%* } %>
```

---

## 6. QuickAdd Plugin

### Capture Macro
```javascript
// Quick capture to inbox
module.exports = async (params) => {
  const { app, quickAddApi } = params;
  const content = await quickAddApi.inputPrompt("Quick capture");

  const file = app.vault.getAbstractFileByPath("Inbox.md");
  await app.vault.append(file, `\n- ${content}`);
};
```

### Template Choices
```javascript
// Dynamic template selection
module.exports = async (params) => {
  const templates = ["Meeting", "Task", "Note"];
  const choice = await params.quickAddApi.suggester(
    templates,
    templates
  );

  // Apply template based on choice
};
```

---

## 7. Vault Organization

### Folder Structure Options

**PARA Method:**
```
vault/
├── 1 - Projects/
├── 2 - Areas/
├── 3 - Resources/
├── 4 - Archive/
└── Templates/
```

**Zettelkasten:**
```
vault/
├── Fleeting/
├── Literature/
├── Permanent/
└── Index/
```

**Simple:**
```
vault/
├── Daily/
├── Notes/
├── Projects/
├── Templates/
└── Attachments/
```

---

## 8. Hotkeys & Commands

### Essential Hotkeys
```
Cmd/Ctrl + N          New note
Cmd/Ctrl + O          Quick switcher
Cmd/Ctrl + P          Command palette
Cmd/Ctrl + Shift + F  Search all files
Cmd/Ctrl + E          Toggle edit/preview
Cmd/Ctrl + G          Open graph view
Cmd/Ctrl + ,          Settings
```

### Custom Hotkeys
```json
// .obsidian/hotkeys.json
{
  "daily-notes": "Cmd+D",
  "templater:insert-template": "Cmd+T"
}
```

---

## 9. CSS Customization

### Custom CSS Snippet
```css
/* .obsidian/snippets/custom.css */

/* Change heading colors */
.cm-header-1 {
  color: #ff6b6b;
}

/* Style tags */
.tag {
  background-color: #e3f2fd;
  border-radius: 4px;
  padding: 2px 6px;
}

/* Hide frontmatter in preview */
.frontmatter-container {
  display: none;
}

/* Custom callout */
.callout[data-callout="custom"] {
  --callout-color: 100, 150, 200;
  --callout-icon: lucide-star;
}
```

---

## 10. Sync & Backup

### Git Backup
```bash
# .gitignore
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/plugins/*/data.json
.trash/
```

### Obsidian Git Plugin Settings
```yaml
Backup interval: 10 minutes
Auto pull on startup: true
Commit message: vault backup: {{date}}
```

### Syncthing Setup
```
1. Install Syncthing on all devices
2. Add vault folder to Syncthing
3. Exclude .obsidian/workspace*.json
4. Enable file versioning
```

---

## 11. Useful Plugins

### Essential
```
- Dataview: Database queries
- Templater: Advanced templates
- QuickAdd: Quick captures
- Periodic Notes: Daily/weekly notes
- Calendar: Calendar view
```

### Productivity
```
- Tasks: Task management
- Kanban: Kanban boards
- Projects: Project management
- Excalidraw: Drawings
```

### Organization
```
- Tag Wrangler: Tag management
- Folder Notes: Folder index
- Auto Link Title: Auto fetch titles
- Note Refactor: Split/merge notes
```

---

## 12. Troubleshooting

### Common Issues

**Sync conflicts:**
```
1. Check for duplicate files with (1) suffix
2. Use Obsidian Sync or single-device editing
3. Enable file versioning in sync tool
```

**Plugin issues:**
```
1. Disable all community plugins
2. Enable one by one to find issue
3. Check console (Cmd+Opt+I)
4. Update plugins and Obsidian
```

**Performance:**
```
1. Reduce vault size
2. Disable unused plugins
3. Optimize Dataview queries
4. Use lazy loading
```

---

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
