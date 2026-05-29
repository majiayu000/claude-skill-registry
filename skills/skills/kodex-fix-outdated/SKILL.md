---
name: kodex-fix-outdated
description: Update an outdated Kodex topic by analyzing codebase changes since topic was written
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

# Kodex Fix Outdated

Update an outdated Kodex topic by analyzing codebase changes and regenerating content based on current implementation.

## Overview

This skill updates a topic that has been flagged as outdated. It analyzes the codebase to identify what has changed since the topic was written, gathers new information, and generates updated content sections for user validation.

**Use when:**
- A topic has been flagged as outdated
- Codebase has evolved significantly since topic documentation
- Implementation details in the topic no longer reflect current code
- Topic references files or patterns that have changed

---

## Step 1: Get Existing Topic

Retrieve the topic from Kodex to understand its current state.

### 1.1 Query the Topic

Use the `kodex_query_topic` tool to fetch the topic:

```
Tool: mcp__plugin_mermaid-collab_mermaid__kodex_query_topic
Args: {
  "project": "<absolute-path-to-cwd>",
  "name": "<topic-name>",
  "include_content": true
}
```

### 1.2 Extract Current Content

From the returned topic, extract:
- **name**: Topic identifier
- **title**: Human-readable title
- **content.conceptual**: Current conceptual overview
- **content.technical**: Current technical details
- **content.files**: Current file references
- **content.related**: Current related topics

### 1.3 Identify Empty Sections

Mark which sections are empty or minimal:
- Empty conceptual (just placeholder text)
- Empty technical
- Empty files listing
- Empty related topics

---

## Step 2: Analyze Codebase for Changes

Explore the codebase to identify what has changed since the topic was written.

### 2.1 Extract File References from Topic

Parse the current `content.files` section to identify files mentioned in the topic.

### 2.2 Check File Existence and Changes

For each file mentioned:
- Use `Glob` to verify the file still exists
- Use `Read` to get current content
- Compare with any older patterns mentioned in the topic

### 2.3 Scan for Related Code Patterns

Use `Grep` to search for:
- Key terms from the topic (functions, classes, concepts)
- Related files in the same directories
- Implementation patterns that may have changed
- Comments or documentation in the code

### 2.4 Identify Structural Changes

Look for:
- New subdirectories or modules
- Renamed or moved files
- Major refactoring indicators
- New dependencies (package.json, requirements.txt, etc.)

### 2.5 Summarize Changes

Create a summary of:
- Files that have changed significantly
- New files relevant to this topic
- Removed or deprecated files
- Major architectural changes

---

## Step 3: Generate Updated Content

Create new content based on current codebase state.

### 3.1 Update Conceptual Section

Regenerate the conceptual overview based on current code:
- What is the main purpose of this topic area?
- What key concepts are currently implemented?
- What are the main components or modules?
- How do they relate to the broader system?

### 3.2 Update Technical Section

Write technical details based on current implementation:
- Architecture patterns in use
- Key functions, classes, or components
- Interfaces and contracts
- Dependencies and integrations
- Configuration or setup requirements

### 3.3 Update Files Section

List the current relevant files:
- Use `Glob` to find all relevant files in the topic area
- Organize by subdirectory if applicable
- Include brief descriptions of what each file does

### 3.4 Update Related Topics

Identify related topics:
- Other Kodex topics that interact with this area
- Cross-references to other sections of the codebase
- Dependencies on external systems

---

## Step 4: Validate with User

Present the updated content sections for user approval.

### 4.1 Display Changes

Show the user:
- What sections were updated
- Before/after comparison for major sections
- Summary of discovered changes in codebase

### 4.2 Present Updated Sections

Display the proposed updates in this format:

```
## Updated Conceptual
[conceptual content]

## Updated Technical
[technical content]

## Updated Files
[files listing]

## Updated Related Topics
[related topics]
```

### 4.3 Ask for Approval

Use `AskUserQuestion` to get user feedback:

```
These sections have been updated based on current codebase analysis.

Do you want to:
1. Approve all changes and create draft
2. Review and edit specific sections
3. Cancel (no changes)
```

### 4.4 Handle Revisions

If user wants to revise:
- Ask which section(s) to modify
- Offer suggestions or alternatives
- Re-display updated sections until user approves

---

## Step 5: Create Draft

Submit the updated topic as a draft using the kodex_update_topic tool.

### 5.1 Prepare Update Args

Build the arguments for the update:

```
Tool: mcp__plugin_mermaid-collab_mermaid__kodex_update_topic
Args: {
  "project": "<absolute-path-to-cwd>",
  "name": "<topic-name>",
  "content": {
    "conceptual": "<updated conceptual>",
    "technical": "<updated technical>",
    "files": "<updated files>",
    "related": "<updated related>"
  },
  "reason": "Updated based on codebase analysis: [brief summary of changes]"
}
```

### 5.2 Call kodex_update_topic

Submit the draft:
- Topic is updated as a draft version
- Human review is required before publishing
- The reason field documents why the update was needed

### 5.3 Report Success

Confirm to user:

```
Updated topic draft created: [topic-name]

Updated sections:
- Conceptual overview
- Technical details
- Files listing
- Related topics

The draft is pending human review before going live.
Use the Kodex dashboard to review and approve changes.
```

---

## Error Handling

| Error | Action |
|-------|--------|
| Topic not found | Report error, exit gracefully |
| Cannot read referenced files | Log warning, skip file, continue with analysis |
| Grep/Glob failures | Log error, continue with available info |
| User cancels at validation | Exit with no changes |
| Update tool fails | Report error with details |

---

## MCP Tools Reference

| Tool | Purpose |
|------|---------|
| `kodex_query_topic` | Fetch existing topic content |
| `kodex_update_topic` | Create draft with updated content |
| `kodex_list_topics` | List existing topics (optional, for context) |

---

## Integration

**Sub-skill** - Called by parent skills like `using-kodex` when user flags a topic as outdated.

**Related skills:**
- `using-kodex` - Query and flag existing topics
- `kodex-fix-incorrect` - Fix inaccurate information
- `kodex-fix-incomplete` - Fill missing sections
- `kodex-fix-missing` - Create new topics for missing areas
