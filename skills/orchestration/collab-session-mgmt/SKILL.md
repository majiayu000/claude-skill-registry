---
name: collab-session-mgmt
description: Detailed procedures for finding, creating, and resuming collab sessions
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - mcp__plugin_mermaid-collab_mermaid__*
---

# Session Management

Detailed procedures for finding, creating, and resuming collab sessions.

---

## Step 2: Find Sessions

```bash
ls -d .collab/*/ 2>/dev/null | xargs -I{} basename {}
```

**If sessions exist:**
1. For each session, get phase via MCP:
   ```
   Tool: mcp__plugin_mermaid-collab_mermaid__get_session_state
   Args: { "project": "<absolute-path-to-cwd>", "session": "<session-name>" }
   ```
   Returns: `{ "phase": "brainstorming", "lastActivity": "...", ... }`
2. Display list with numbered options:
   ```
   Existing sessions:

   1. bright-calm-river - brainstorming
   2. swift-green-meadow - implementation
   3. Create new session

   Select option (1-3):
   ```
3. If user selects existing session number → Jump to **Step 5: Resume Session**
4. If user selects 'new' option → Continue to **Step 3**

**If no sessions exist:** Continue to **Step 3**

---

## Step 3: Create Session

### 3.1 Ensure .gitignore

```bash
if [ -f .gitignore ]; then
  git check-ignore -q .collab 2>/dev/null || echo ".collab/" >> .gitignore
fi
```

**Note:** Only modifies `.gitignore` if it already exists. Does not create a new `.gitignore` file.

### 3.2 Generate or Choose Name

1. Generate a suggested name:
   ```
   Tool: mcp__plugin_mermaid-collab_mermaid__generate_session_name
   Args: {}
   ```
   Returns: `{ name: "bright-calm-river" }`

2. Present options to user:
   ```
   Generated session name: bright-calm-river

   1. Use this name
   2. Pick my own name

   Select option (1-2):
   ```

3. If user selects "1. Use this name":
   - Use the generated name
   - Continue to Step 3.3

4. If user selects "2. Pick my own name":
   a. Prompt: "Enter session name (alphanumeric and hyphens only):"
   b. Validate input:
      - Must match pattern: /^[a-zA-Z0-9-]+$/
      - Must not be empty
   c. If invalid:
      - Show error: "Invalid name. Use only letters, numbers, and hyphens."
      - Return to step 4a (re-prompt)
   d. If valid:
      - Use the custom name
      - Continue to Step 3.3

### 3.3 Initialize Session State

Initialize collab-state.json via MCP (creates folder and design.md automatically):

```
Tool: mcp__plugin_mermaid-collab_mermaid__update_session_state
Args: {
  "project": "<absolute-path-to-cwd>",
  "session": "<session-name>",
  "phase": "brainstorming",
  "currentItem": null
}
```

Note: `lastActivity` is automatically updated. The `design.md` file is auto-created by `sessionRegistry.register()` when any MCP tool is first called for this session.

### 3.4 Set Environment Variable

Set the session path environment variable for hooks:

```bash
export COLLAB_SESSION_PATH="$(pwd)/.collab/<name>"
```

### 3.5 Invoke gather-session-goals

```
Invoke skill: gather-session-goals
```

This skill will:
- Ask user what they want to accomplish
- Classify each item as code/bugfix/task
- Write Work Items section to design doc
- All items start with `Status: pending`

After gather-session-goals returns → Jump to **Work Item Loop** (see collab-work-item-loop skill)

---

## Step 5: Resume Session

When user selects an existing session from Step 2.

### 5.1 Check for Context Snapshot

```
Tool: mcp__plugin_mermaid-collab_mermaid__has_snapshot
Args: { "project": "<absolute-path-to-cwd>", "session": "<session-name>" }
```
Returns: `{ "exists": true }` or `{ "exists": false }`

**If snapshot exists:**

1. Load snapshot:
   ```
   Tool: mcp__plugin_mermaid-collab_mermaid__load_snapshot
   Args: { "project": "<absolute-path-to-cwd>", "session": "<session-name>" }
   ```
   Returns: `{ "version": 1, "timestamp": "...", "activeSkill": "...", "currentStep": "...", ... }`

2. Display restoration message:
   ```
   Restoring from context snapshot...
   Active skill: <activeSkill>
   Step: <currentStep>
   ```

3. Delete snapshot (one-time use):
   ```
   Tool: mcp__plugin_mermaid-collab_mermaid__delete_snapshot
   Args: { "project": "<absolute-path-to-cwd>", "session": "<session-name>" }
   ```

4. Update state:
   ```
   Tool: mcp__plugin_mermaid-collab_mermaid__update_session_state
   Args: { "project": "<absolute-path-to-cwd>", "session": "<session-name>", "hasSnapshot": false }
   ```

5. Invoke the active skill directly:
   - If activeSkill == "brainstorming" → Invoke brainstorming skill
   - If activeSkill == "rough-draft" → Invoke rough-draft skill
   - If activeSkill == "executing-plans" → Invoke executing-plans skill

**STOP** - skill takes over from here.

**If no snapshot:** Continue to 5.2 (existing resume behavior, route by phase)

### 5.2 Set Environment Variable

```bash
export COLLAB_SESSION_PATH="$(pwd)/.collab/<name>"
```

### 5.3 Read State

```
Tool: mcp__plugin_mermaid-collab_mermaid__get_session_state
Args: { "project": "<absolute-path-to-cwd>", "session": "<session-name>" }
```
Returns: `{ "phase": "...", "lastActivity": "...", "currentItem": ..., ... }`

### 5.4 Display Session Info

```
Session Resumed: <name>
Phase: <phase>
Dashboard: http://localhost:3737

Checking work item status...
```

### 5.5 Invoke ready-to-implement

**Always** route through ready-to-implement for resume:

```
Invoke skill: ready-to-implement
```

ready-to-implement will:
- If pending items exist → return with `action: "return_to_loop"` → Go to **Work Item Loop** (see collab-work-item-loop skill)
- If all documented → proceed to rough-draft (on user confirmation)
