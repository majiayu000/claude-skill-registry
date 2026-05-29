---
name: ccn:document-capture
description: Automatically capture decisions, learnings, and questions when DECISION:, LEARNING:, or QUESTION: markers appear in conversation
user-invocable: false
---

# Document Capture Skill

You are a documentation assistant that captures noteworthy moments automatically when explicit markers appear in conversation.

## When to Activate

Activate this skill when you detect explicit markers in conversation (from either user or Claude):
- `DECISION:` followed by content
- `LEARNING:` followed by content
- `QUESTION:` followed by content

Only trigger on exact prefix match (capitalized prefix with colon). Ignore unrecognized markers.

## Capture Process

### Step 1: Parse Marker

Extract the marker type and content:
- Marker type: DECISION, LEARNING, or QUESTION
- Content: Text after the marker (may be multi-line until next paragraph)
- Map to target file:
  - `DECISION:` → `.notes/DECISIONS_LOG.md`
  - `LEARNING:` → `.notes/LEARNINGS.md`
  - `QUESTION:` → `.notes/QUESTIONS.md`

### Step 2: Read Existing File

Use the **Read** tool to load the current file content.

- If file exists: Preserve all existing content
- If file doesn't exist: Create with template header matching the format from templates/DECISIONS_LOG.md, templates/LEARNINGS.md, or templates/QUESTIONS.md

Template structure:
```markdown
---
description: "[Decisions made | Technical learnings | Open questions] during Claude Code Notes development"
last_updated: "YYYY-MM-DD"
---

# [Decisions Log | Learnings | Questions]

(Content follows here)
```

### Step 3: Format Entry

Create a new entry with:
- ISO 8601 timestamp heading: `### YYYY-MM-DDTHH:MM:SS` (local time, no milliseconds)
- Captured content below the heading
- Optional: Brief context about what file/task prompted the capture (your discretion)

Example:
```markdown
### 2026-01-26T14:30:00

Using Biome over ESLint for unified linting and formatting tooling.
```

### Step 4: Append Entry

Concatenate the updated content:
1. Take existing file content
2. Add blank line
3. Add new entry
4. Write back using **Write** tool

### Step 5: Notify

Provide a brief inline notification:
- Format: "Captured to [FILE]: [first 50 chars of content]..."
- Keep total notification under 80 characters
- Always notify (no silent mode)

Example: "Captured to DECISIONS_LOG: Using Biome over ESLint for unified..."

## Important Notes

- Only trigger on explicit markers (capitalized prefix with colon)
- Unknown markers are ignored
- Always notify on capture (no silent mode)
- Auto-create target files if missing using template structure
- Entries append to end of file (chronological order, newest at bottom)
- Multiple markers in same message: process each sequentially

## Error Handling

- If Read tool fails: Show error and explain what went wrong
- If Write tool fails: Show error and explain what went wrong
- Continue processing other markers even if one fails
