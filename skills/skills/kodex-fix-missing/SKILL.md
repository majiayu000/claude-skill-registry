---
name: kodex-fix-missing
description: Create new Kodex topics for missing documentation
user-invocable: false
allowed-tools:
  - Glob
  - Grep
  - Read
  - AskUserQuestion
  - mcp__plugin_mermaid-collab_mermaid__kodex_create_topic
  - mcp__plugin_mermaid-collab_mermaid__kodex_list_topics
---

# Kodex Fix Missing

Create new Kodex topics for missing documentation.

## Overview

This sub-skill is invoked by `kodex-fix` when a topic is flagged as missing. It researches the codebase to create a complete new topic.

---

## Step 1: Understand What's Needed

The flag description indicates what topic should exist.
Extract the topic name and any hints about what it should cover.

---

## Step 2: Research the Topic

Search for files matching the topic name:

```
Tool: Glob
Args: { "pattern": "**/*<topic-name>*" }
```

Search for references:

```
Tool: Grep
Args: { "pattern": "<topic-keyword>", "path": "<project-root>" }
```

Read relevant files to understand the component.

---

## Step 3: Identify Topic Scope

Determine:
- Which files belong to this topic?
- What is the main purpose?
- How does it relate to other components?

If unclear, ask user:

```
I found these potential files for [topic]:
- path/to/file1.ts
- path/to/file2.ts

Should I include all of these, or is the scope different?
```

---

## Step 4: Generate All 4 Sections

Create complete topic content:

- **conceptual**: High-level description
- **technical**: Implementation details, patterns, gotchas
- **files**: List of related source files
- **related**: Links to other Kodex topics

---

## Step 5: Validate with User

Present the full draft:

```
**New Topic: [topic-name]**

[Full content preview]

Does this accurately describe [topic-name]?
1. Yes
2. No - needs changes
```

---

## Step 6: Create Draft

```
Tool: mcp__plugin_mermaid-collab_mermaid__kodex_create_topic
Args: {
  "project": "<cwd>",
  "name": "<topic-name>",
  "title": "<Topic Title>",
  "content": { "conceptual": "...", "technical": "...", "files": "...", "related": "..." }
}
```

Return to parent skill.

---

## Error Handling

| Error | Action |
|-------|--------|
| No matching files | Ask user for guidance |
| Ambiguous scope | Present options, let user choose |
| Topic name too generic | Ask for clarification |

---

## Integration

**Called by:** kodex-fix (parent skill)
**Returns to:** kodex-fix after creating draft
