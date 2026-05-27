---
name: collab-clear
description: Ask user about clearing context, then proceed to next skill
user-invocable: true
allowed-tools: mcp__plugin_mermaid-collab_mermaid__*, Read
---

# Collab Clear

Asks user whether to clear context before proceeding.

## Step 1: Ask User

```
Tool: mcp__plugin_mermaid-collab_mermaid__render_ui
Args: {
  "project": "<cwd>",
  "session": "<session>",
  "ui": {
    "type": "Card",
    "props": { "title": "Context Management" },
    "children": [{ "type": "Markdown", "props": { "content": "Clear context and start fresh?" } }],
    "actions": [
      { "id": "yes", "label": "Yes, clear", "primary": true },
      { "id": "no", "label": "No, continue" }
    ]
  },
  "blocking": true
}
```

If UI times out, ask in terminal.

## Step 2: Get Next Skill

```
Tool: mcp__plugin_mermaid-collab_mermaid__complete_skill
Args: { "project": "<cwd>", "session": "<session>", "skill": "collab-clear" }
```

## Step 3: Handle Choice

**If user chose "Yes, clear":**
1. Save snapshot with next_skill as activeSkill
2. Update state: hasSnapshot = true
3. Display: "Context saved. Triggering /clear..."
4. Invoke /clear (user will run /collab to resume)

**If user chose "No, continue":**
1. Invoke result.next_skill directly (skip the clear)
