---
name: kodex-fix
description: Fix flagged Kodex topics by generating updated content
user-invocable: true
allowed-tools:
  - AskUserQuestion
  - mcp__plugin_mermaid-collab_mermaid__kodex_list_flags
  - mcp__plugin_mermaid-collab_mermaid__kodex_list_topics
---

# Kodex Fix

Fix flagged Kodex topics by generating updated content.

## Overview

This skill lists open Kodex flags and routes to the appropriate sub-skill based on flag type. After the sub-skill creates a draft, the user can review and approve it in the Kodex UI.

**Use when:**
- You see open flags in the Kodex dashboard
- A topic has been flagged as outdated, incorrect, incomplete, or missing

---

## Step 1: List Open Flags

Query for open flags:

```
Tool: mcp__plugin_mermaid-collab_mermaid__kodex_list_flags
Args: { "project": "<absolute-path-to-cwd>", "status": "open" }
```

**If no open flags:**
```
No open flags to fix.

Use the Kodex dashboard to view all flags or /kodex-init to create new topics.
```
**STOP** - exit the skill.

---

## Step 2: Select Flag

Present flags to user:

```
Open flags:

1. [outdated] topic-name: Description of the issue
2. [incorrect] another-topic: Description of the issue
3. [missing] new-topic: Description of the issue

Which flag do you want to fix?
```

Use AskUserQuestion with multiple choice.

---

## Step 3: Route to Sub-Skill

Based on the selected flag's type:

| Flag Type | Sub-Skill |
|-----------|-----------|
| outdated | Invoke skill: kodex-fix-outdated |
| incorrect | Invoke skill: kodex-fix-incorrect |
| incomplete | Invoke skill: kodex-fix-incomplete |
| missing | Invoke skill: kodex-fix-missing |

Pass the topic name and flag description to the sub-skill.

---

## Step 4: Completion

After sub-skill returns:

```
Draft created for [topic-name].

Review and approve the draft in the Kodex UI:
- Go to Kodex > Drafts
- Review the content
- Click "Approve" to publish (this will auto-resolve the flag)

Fix another flag?

1. Yes
2. No
```

If user selects **1 (Yes)**: Return to Step 1
If user selects **2 (No)**: Exit skill

---

## Error Handling

| Error | Action |
|-------|--------|
| MCP tool failure | Display error, suggest retry |
| Flag not found | Refresh list, flag may have been resolved |

---

## Integration

**Standalone skill** - Does not require an active collab session.

**Related skills:**
- `kodex-fix-outdated` - Update stale content
- `kodex-fix-incorrect` - Fix factual errors
- `kodex-fix-incomplete` - Fill missing sections
- `kodex-fix-missing` - Create new topics
- `using-kodex` - Query and flag topics
- `kodex-init` - Bootstrap topic stubs
