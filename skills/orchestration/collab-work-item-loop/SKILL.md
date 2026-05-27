---
name: collab-work-item-loop
description: The core orchestration loop that processes work items one at a time
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - mcp__plugin_mermaid-collab_mermaid__*
---

# Work Item Loop

The core orchestration loop that processes work items one at a time.

---

## Step 4: Work Item Loop

### 4.1 Read Design Doc

```bash
cat .collab/<name>/documents/design.md
```

### 4.2 Parse Work Items

Use `parseWorkItems()` helper to extract items from design doc:
- Find all `### Item N:` sections
- Extract Title, Type, and Status fields
- Return list of work items

See **Helper Functions** in main collab skill for `parseWorkItems()` implementation.

### 4.3 Find First Pending Item

```
pending_item = items.find(i => i.status == "pending")
```

**If no pending items:**
```
All work items documented. Proceeding to validation...
```
→ Invoke **ready-to-implement** skill
→ **END** (ready-to-implement takes over)

**If pending item found:** Continue to 4.4

### 4.4 Update State

Update collab state via MCP:
```
Tool: mcp__plugin_mermaid-collab_mermaid__update_session_state
Args: {
  "project": "<absolute-path-to-cwd>",
  "session": "<session-name>",
  "currentItem": <item-number>
}
```
Note: `lastActivity` is automatically updated by the MCP tool.

### 4.5 Route by Type

**If type is `bugfix`:**
```
Processing bugfix: <item-title>
Invoking systematic-debugging for investigation...
```
→ Invoke skill: collab-compact
→ Invoke **systematic-debugging** skill

**If type is `task`:**
```
Processing task: <item-title>
Invoking brainstorming for planning...
```
→ Invoke skill: collab-compact
→ Invoke **brainstorming** skill
→ After brainstorming completes, invoke skill: collab-compact
→ After collab-compact completes, invoke **task-planning** skill

**If type is `code`:**
```
Processing code: <item-title>
Invoking brainstorming for design...
```
→ Invoke skill: collab-compact
→ Invoke **brainstorming** skill
→ After brainstorming completes, invoke skill: collab-compact
→ After collab-compact completes, invoke **rough-draft** skill (includes feature/refactor/spike work)

### 4.6 Mark Item Documented

After the invoked skill returns, use patch to update the work item status:

```
Tool: mcp__plugin_mermaid-collab_mermaid__patch_document
Args: {
  "project": "<cwd>",
  "session": "<name>",
  "id": "design",
  "old_string": "### Item <N>: <title>\n**Type:** <type>\n**Status:** pending",
  "new_string": "### Item <N>: <title>\n**Type:** <type>\n**Status:** documented"
}
```

This is more efficient than reading and rewriting the entire document.

### 4.7 Clear Current Item

Update collab state via MCP:
```
Tool: mcp__plugin_mermaid-collab_mermaid__update_session_state
Args: {
  "project": "<absolute-path-to-cwd>",
  "session": "<session-name>",
  "currentItem": null
}
```
Note: `lastActivity` is automatically updated by the MCP tool.

### 4.8 Continue Loop

→ Go back to **Step 4.1** (continue processing next pending item)
