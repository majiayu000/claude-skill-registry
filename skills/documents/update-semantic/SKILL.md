---
name: update-semantic
description: Append insights and updates to semantic notes (People, Projects, Areas, Insights, Resources). Preserves existing content while adding new dated entries.
disable-model-invocation: true
allowed-tools: Read, Write, Bash
---

# Update Semantic Sub-Skill

Appends new content to semantic notes based on daily review synthesis. Handles multiple note types and preserves existing content.

## Input Arguments

Arguments are passed as key-value pairs:
- `vault`: Path to the vault
- `updates`: JSON array of updates to apply

**Update format:**
```json
{
  "updates": [
    {
      "type": "person",
      "path": "02_Areas/People/SarahK.md",
      "section": "Interactions",
      "content": "2026-02-14: Discussed career growth goals. She's interested in tech lead path."
    },
    {
      "type": "project",
      "path": "01_Projects/2026-03-15-platform-migration.md",
      "section": "Progress",
      "content": "2026-02-14: API design finalized. Ready for implementation."
    },
    {
      "type": "insight",
      "path": "02_Areas/Insights/delegation.md",
      "section": "Evidence",
      "content": "2026-02-14: Letting Sarah lead the design review freed up 2 hours."
    },
    {
      "type": "resource",
      "path": "03_Resources/articles/distributed-systems.md",
      "section": "Notes",
      "content": "Captured from daily review. Key insight: CAP theorem tradeoffs."
    }
  ]
}
```

## Instructions

### 1. Parse Updates

Parse the `updates` JSON array. Validate each update has:
- `type` - One of: person, project, insight, area, resource
- `path` - Relative path from vault root
- `section` - Target section heading in the note
- `content` - Content to append

### 2. Process Each Update

For each update:

#### 2.1 Resolve Full Path

```
$VAULT/{update.path}
```

#### 2.2 Check File Exists

If file doesn't exist:
- Log warning: "Note not found: {path}"
- Add to `skipped` array with reason
- Continue to next update

#### 2.3 Read Existing Content

Read the full content of the semantic note.

#### 2.4 Find Target Section

Locate the section heading matching `## {section}`:
- If exact match found → append after section content
- If section not found → append new section at end

#### 2.5 Append Content

Insert the new content:
- Add a blank line before the new content
- Prepend content with bullet point if not already formatted
- Preserve any existing content in the section

**Example transformation:**

Before:
```markdown
## Interactions

- 2026-02-10: Onboarding check-in
```

After:
```markdown
## Interactions

- 2026-02-10: Onboarding check-in
- 2026-02-14: Discussed career growth goals. She's interested in tech lead path.
```

#### 2.6 Write Updated File

Write the modified content back to the file.

### 3. Handle New Notes (Optional)

If `type` is `resource` and file doesn't exist, create a minimal note:

```markdown
---
created: {date}
source: daily-review
---

# {title extracted from path}

## Notes

- {content}
```

For other types, skip creation (user should create the note structure).

### 4. Return Result

**Success:**
```json
{
  "success": true,
  "applied": [
    { "path": "02_Areas/People/SarahK.md", "section": "Interactions", "status": "appended" },
    { "path": "01_Projects/2026-03-15-platform-migration.md", "section": "Progress", "status": "appended" }
  ],
  "skipped": [
    { "path": "02_Areas/Insights/new-concept.md", "reason": "file_not_found" }
  ],
  "created": [
    { "path": "03_Resources/articles/distributed-systems.md", "status": "created" }
  ]
}
```

**Partial success:**
```json
{
  "success": true,
  "partial": true,
  "applied": [...],
  "skipped": [...],
  "message": "Some updates skipped. See details above."
}
```

**Failure:**
```json
{
  "success": false,
  "error": "invalid_updates",
  "message": "Failed to parse updates JSON"
}
```

## Semantic Note Paths by Type

| Type | Expected Path Pattern | Default Section |
|------|----------------------|-----------------|
| person | `02_Areas/People/{Name}.md` | Interactions |
| project | `01_Projects/{date-name}.md` | Progress |
| insight | `02_Areas/Insights/{topic}.md` | Evidence |
| area | `02_Areas/{name}.md` | Notes |
| resource | `03_Resources/{category}/{name}.md` | Notes |

## Safety

- Always read before write to preserve existing content
- Never delete or overwrite existing section content
- Only append to existing sections
- Skip updates for non-existent files (except resources)
- Log all actions for transparency
