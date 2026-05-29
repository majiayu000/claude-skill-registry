---
name: kodex-fix-incomplete
description: Fill in missing sections of incomplete Kodex topics
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

# Kodex Fix Incomplete

Fill in missing sections of incomplete Kodex topics.

## Overview

This sub-skill is invoked by `kodex-fix` when a topic is flagged as incomplete. It identifies which sections are empty or sparse and fills them in.

---

## Step 1: Get Existing Topic

```
Tool: mcp__plugin_mermaid-collab_mermaid__kodex_query_topic
Args: { "project": "<cwd>", "name": "<topic-name>" }
```

Identify which sections need content:
- conceptual: Empty or just placeholder text?
- technical: Empty or lacks detail?
- files: Missing file list?
- related: Missing related topics?

---

## Step 2: Gather Information for Missing Sections

For each empty/sparse section:

**conceptual (if empty):**
- Read main entry points
- Check for README in component directory
- Summarize purpose from code comments

**technical (if empty):**
- Analyze implementation patterns
- Document key functions and their purposes
- Note any gotchas or important details

**files (if empty):**
```
Tool: Glob
Args: { "pattern": "**/*<topic-keyword>*" }
```

**related (if empty):**
```
Tool: mcp__plugin_mermaid-collab_mermaid__kodex_list_topics
Args: { "project": "<cwd>" }
```
Find topics with related names or overlapping file paths.

---

## Step 3: Generate Content for Missing Sections

Only fill empty/sparse sections. Preserve existing content.

---

## Step 4: Validate with User

For each filled section:
```
**[Section name] (new content):**
[generated content]

Does this accurately describe [topic]?
1. Yes
2. No - needs changes
```

---

## Step 5: Create Draft

```
Tool: mcp__plugin_mermaid-collab_mermaid__kodex_update_topic
Args: {
  "project": "<cwd>",
  "name": "<topic-name>",
  "content": { ... },
  "reason": "Filled incomplete sections: [list sections]"
}
```

Return to parent skill.

---

## Integration

**Called by:** kodex-fix (parent skill)
**Returns to:** kodex-fix after creating draft
