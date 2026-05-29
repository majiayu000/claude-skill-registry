---
name: kodex-fix-incorrect
description: Correct factually incorrect Kodex topic content
user-invocable: false
allowed-tools:
  - Glob
  - Grep
  - Read
  - AskUserQuestion
  - mcp__plugin_mermaid-collab_mermaid__kodex_query_topic
  - mcp__plugin_mermaid-collab_mermaid__kodex_update_topic
  - mcp__plugin_mermaid-collab_mermaid__kodex_list_topics
---

# Kodex Fix Incorrect

Correct factually incorrect Kodex topic content.

## Overview

This sub-skill is invoked by `kodex-fix` when a topic is flagged as incorrect. It focuses on the specific inaccuracy described in the flag and verifies against actual code.

---

## Step 1: Get Existing Topic and Flag Details

Query the existing topic to understand the current content:

```
Tool: mcp__plugin_mermaid-collab_mermaid__kodex_query_topic
Args: { "project": "<cwd>", "name": "<topic-name>" }
```

Review the flag description to understand what's incorrect. Extract:
- Current content (conceptual, technical, files, related)
- File paths from the 'files' section
- The specific inaccuracy mentioned in the flag

**If topic not found:**
```
Topic not found. This may need kodex-fix-missing instead.
```
Return to parent skill.

---

## Step 2: Verify the Inaccuracy

Focus on the specific inaccuracy mentioned in the flag. Read the files mentioned in the topic to compare what they actually contain versus what the topic claims:

```
Tool: Read
Args: { "file_path": "<file-from-topic>" }
```

Compare:
- What the topic claims
- What the code actually does

Identify the specific incorrect statement(s) by examining the implementation. Focus specifically on the inaccuracy flagged rather than a general review.

---

## Step 3: Research Correct Information

Use Grep to find actual implementations and verify what the code actually does:

```
Tool: Grep
Args: { "pattern": "<function-or-concept>", "path": "<project-root>" }
```

Build accurate understanding of how things actually work in the codebase. Research the specific behavior that contradicts what the topic currently documents.

---

## Step 4: Generate Corrected Content

Update the sections that contain the inaccuracy. Focus corrections on:
- The specific inaccuracy from the flag
- Any related incorrect statements discovered during research
- Keep accurate parts unchanged

Generate corrected versions of affected sections (conceptual, technical, files, related as needed).

---

## Step 5: Validate with User

Present the correction for user validation:

```
**Correction:**

The flag said: "[flag description]"
I found: "[actual behavior from code]"

Updated content:
[corrected section]

Is this correction accurate?
1. Yes
2. No - needs adjustment
```

Use AskUserQuestion to get user feedback. If user selects **2**, ask for corrections and regenerate.

---

## Step 6: Create Draft

Call kodex_update_topic to create a draft with the corrected content:

```
Tool: mcp__plugin_mermaid-collab_mermaid__kodex_update_topic
Args: {
  "project": "<cwd>",
  "name": "<topic-name>",
  "content": { "conceptual": "...", "technical": "...", "files": "...", "related": "..." },
  "reason": "Corrected inaccuracy: [brief description of the correction]"
}
```

Return to parent skill after draft is created.

---

## Error Handling

| Error | Action |
|-------|--------|
| Topic not found | Return to parent, suggest kodex-fix-missing |
| Files not readable | Skip, note in content |
| User rejects content | Ask for corrections, regenerate |
| MCP tool failure | Display error, suggest retry |

---

## Integration

**Called by:** kodex-fix (parent skill)
**Returns to:** kodex-fix after creating draft

**Related skills:**
- `kodex-fix` - Parent skill that orchestrates flag fixes
- `kodex-fix-outdated` - Update stale content
- `kodex-fix-incomplete` - Fill missing sections
- `kodex-fix-missing` - Create new topics
- `using-kodex` - Query and flag topics
