---
name: gdrive-manager
description: Manages all Google Drive operations within the claude-code folder. Use this skill for ANY Google Drive file creation, updates, or organization. Enforces folder restrictions and maintains the centralized INDEX document. Required before using raw mcp__gdrive__ tools for research documentation, experiment logs, updates, or slides.
---

# Google Drive Manager

**All Claude Code Google Drive operations MUST go through this skill** to ensure proper folder organization and automatic INDEX maintenance.

## Folder Structure

```
Google Drive/
└── claude-code/
    ├── INDEX                     # Central document with links to all docs
    ├── experiments/              # Experiment documentation (research-executor)
    ├── logs/                     # Daily/session logs
    ├── updates/                  # Weekly updates (weekly-update-writer)
    └── slides/                   # Presentations (research-slides-architect)
```

## Folder Mapping

| Document Type | Target Folder | Naming Convention |
|--------------|---------------|-------------------|
| Experiment docs | `/experiments` | `{experiment-name}` |
| Daily logs | `/logs` | `{YYYY-MM-DD}-log` |
| Weekly updates | `/updates` | `{YYYY-MM-DD}-weekly-update` |
| Presentations | `/slides` | `{presentation-name}` |

## Configuration

Folder IDs are cached in `references/folder-ids.md`. Read this file first to get the correct folder IDs.

## Workflow: Creating a Document

### Step 1: Read Folder IDs

```
Read: .claude/skills/gdrive-manager/references/folder-ids.md
```

This gives you the cached folder IDs:
- `ROOT_FOLDER_ID` - claude-code folder
- `EXPERIMENTS_FOLDER_ID` - experiments subfolder
- `LOGS_FOLDER_ID` - logs subfolder
- `UPDATES_FOLDER_ID` - updates subfolder
- `SLIDES_FOLDER_ID` - slides subfolder
- `INDEX_DOC_ID` - INDEX document

### Step 2: Determine Target Folder

Based on document type:
- Experiment documentation → use `EXPERIMENTS_FOLDER_ID`
- Daily log → use `LOGS_FOLDER_ID`
- Weekly update → use `UPDATES_FOLDER_ID`
- Presentation → use `SLIDES_FOLDER_ID`

### Step 3: Create Document in Correct Folder

**For Google Docs:**
```
mcp__gdrive__createGoogleDoc(
  name: "{document-name}",
  content: "{initial-content}",
  parentFolderId: "{FOLDER_ID}"
)
```

**For Google Slides:**
```
mcp__gdrive__createGoogleSlides(
  name: "{presentation-name}",
  slides: [...],
  parentFolderId: "{SLIDES_FOLDER_ID}"
)
```

### Step 4: Update INDEX Document

After creating any document, update the INDEX:

1. Get current INDEX content:
   ```
   mcp__gdrive__getGoogleDocContent(documentId: "{INDEX_DOC_ID}")
   ```

2. Add new entry to appropriate section

3. Update INDEX:
   ```
   mcp__gdrive__updateGoogleDoc(
     documentId: "{INDEX_DOC_ID}",
     content: "{updated-content}"
   )
   ```

4. Apply formatting (HEADING_1 for section headers)

## Workflow: Full INDEX Refresh

Use this workflow to regenerate the entire INDEX from current folder contents:

### Step 1: List All Folders

```
mcp__gdrive__listFolder(folderId: "{EXPERIMENTS_FOLDER_ID}")
mcp__gdrive__listFolder(folderId: "{LOGS_FOLDER_ID}")
mcp__gdrive__listFolder(folderId: "{UPDATES_FOLDER_ID}")
mcp__gdrive__listFolder(folderId: "{SLIDES_FOLDER_ID}")
```

### Step 2: Generate INDEX Content

```
CLAUDE-CODE GOOGLE DRIVE INDEX
Last Updated: {current-timestamp}

TL;DR
• Central index for all Claude Code research documents
• {N} experiments, {M} logs, {P} updates, {Q} slides

QUICK LINKS
• Latest Experiment: {name} - https://docs.google.com/document/d/{id}
• Today's Log: {date} - https://docs.google.com/document/d/{id}

EXPERIMENTS
• {name} - https://docs.google.com/document/d/{id} - {date}
• ...

LOGS
• {date} - https://docs.google.com/document/d/{id}
• ...

UPDATES
• {date} Weekly Update - https://docs.google.com/document/d/{id}
• ...

SLIDES
• {name} - https://docs.google.com/presentation/d/{id} - {date}
• ...
```

### Step 3: Update and Format INDEX

1. Update content: `mcp__gdrive__updateGoogleDoc`
2. Get content with indices: `mcp__gdrive__getGoogleDocContent`
3. Apply TITLE style to header
4. Apply HEADING_2 to "TL;DR"
5. Apply HEADING_1 to each section (EXPERIMENTS, LOGS, etc.)

## Initial Setup (One-Time)

If the folder structure doesn't exist yet:

### Create Folders

```
# 1. Create root folder
mcp__gdrive__createFolder(name: "claude-code")
→ Save the returned ID as ROOT_FOLDER_ID

# 2. Create subfolders
mcp__gdrive__createFolder(name: "experiments", parent: "{ROOT_FOLDER_ID}")
→ Save as EXPERIMENTS_FOLDER_ID

mcp__gdrive__createFolder(name: "logs", parent: "{ROOT_FOLDER_ID}")
→ Save as LOGS_FOLDER_ID

mcp__gdrive__createFolder(name: "updates", parent: "{ROOT_FOLDER_ID}")
→ Save as UPDATES_FOLDER_ID

mcp__gdrive__createFolder(name: "slides", parent: "{ROOT_FOLDER_ID}")
→ Save as SLIDES_FOLDER_ID
```

### Create INDEX Document

```
mcp__gdrive__createGoogleDoc(
  name: "INDEX",
  content: "CLAUDE-CODE GOOGLE DRIVE INDEX\nLast Updated: {date}\n\nTL;DR\n• Central index for all Claude Code research documents\n\nEXPERIMENTS\n(empty)\n\nLOGS\n(empty)\n\nUPDATES\n(empty)\n\nSLIDES\n(empty)",
  parentFolderId: "{ROOT_FOLDER_ID}"
)
→ Save as INDEX_DOC_ID
```

### Cache Folder IDs

Write all IDs to `.claude/skills/gdrive-manager/references/folder-ids.md`

## Validation

Before any operation:
1. Read `references/folder-ids.md`
2. If IDs are missing, search for folder: `mcp__gdrive__search(query: "claude-code")`
3. If folder doesn't exist, run Initial Setup workflow

## Link Formats

When adding links to INDEX, use these formats:
- **Google Docs**: `https://docs.google.com/document/d/{document-id}`
- **Google Slides**: `https://docs.google.com/presentation/d/{presentation-id}`
- **Google Sheets**: `https://docs.google.com/spreadsheets/d/{spreadsheet-id}`

## Critical Reminders

1. **NEVER create documents outside claude-code folder** - All research docs must be in the appropriate subfolder
2. **ALWAYS update INDEX after creating/deleting documents** - Keep the index current
3. **Use correct folder for document type** - Experiments go to /experiments, logs to /logs, etc.
4. **Format the INDEX** - Use google-docs-formatter skill for proper heading styles

## Related Skills

- **/google-docs-formatter** - Use after creating docs for proper formatting
- **research-executor** agent - Creates experiment docs in /experiments
- **weekly-update-writer** agent - Creates updates in /updates
- **research-slides-architect** agent - Creates slides in /slides
