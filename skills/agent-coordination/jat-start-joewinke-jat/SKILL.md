---
name: jat-start
description: Begin working on a JAT task. Registers agent identity, selects a task, searches memory, detects conflicts, reserves files, emits IDE signals, and starts work. Use this at the beginning of every JAT session.
metadata:
  author: jat
  version: "1.0"
---

# /skill:jat-start - Begin Working

**One agent = one session = one task.** Each session handles exactly one task from start to completion.

## Usage

```
/skill:jat-start                    # Show available tasks
/skill:jat-start task-id            # Start specific task
/skill:jat-start AgentName          # Resume as AgentName
/skill:jat-start AgentName task-id  # Resume as AgentName on task
```

Add `quick` to skip conflict checks.

## What This Does

1. **Establish identity** - Register or resume agent in Agent Registry
2. **Select task** - From parameter or show recommendations
3. **Search memory** - Surface context from past sessions
4. **Review prior tasks** - Check for duplicates and related work
5. **Start work** - Reserve files, update task status
6. **Emit signals** - IDE tracks state through jat-signal

## Step-by-Step Instructions

### STEP 1: Parse Arguments

Check what was passed: `$ARGUMENTS` may contain agent-name, task-id, both, or nothing.

```bash
# Test if a param is a valid task ID
jt show "$PARAM" --json >/dev/null 2>&1 && echo "task-id" || echo "agent-name"
```

### STEP 2: Get/Create Agent Identity

#### 2A: Check for IDE Pre-Registration

If spawned by the IDE, your identity file already exists:

```bash
TMUX_SESSION=$(tmux display-message -p '#S' 2>/dev/null)
PRE_REG_FILE=".claude/sessions/.tmux-agent-${TMUX_SESSION}"
test -f "$PRE_REG_FILE" && cat "$PRE_REG_FILE"
```

If found, use that name and skip to Step 3.

#### 2B: Register Manually (CLI only)

If no pre-registration file exists, pick a name and register:

```bash
# Generate or use provided name
am-register --name "$AGENT_NAME" --program pi --model "$MODEL_ID"
tmux rename-session "jat-${AGENT_NAME}" 2>/dev/null
```

#### 2C: Write Session Identity

For manual sessions, write the identity file so the IDE can track you:

```bash
mkdir -p .claude/sessions
echo "$AGENT_NAME" > ".claude/sessions/agent-${SESSION_ID}.txt"
```

### STEP 3: Select Task

If a task-id was provided, use it. Otherwise, show available work:

```bash
jt ready --json | jq -r '.[] | "  [P\(.priority)] \(.id) - \(.title)"'
```

If no task-id provided, display recommendations and stop here.

### STEP 4: Search Memory

Search project memory for relevant context from past sessions:

```bash
jat-memory search "key terms from task title" --limit 5
```

Returns JSON with matching chunks (taskId, section, snippet, score). Use results to:
- Incorporate lessons and gotchas into your approach
- Avoid repeating documented mistakes
- Build on established patterns

If no memory index exists, skip silently.

### STEP 5: Review Prior Tasks

Search for related or duplicate work from the last 7 days:

```bash
DATE_7D=$(date -d '7 days ago' +%Y-%m-%d 2>/dev/null || date -v-7d +%Y-%m-%d)
jt search "$SEARCH_TERM" --updated-after "$DATE_7D" --limit 20 --json
```

Look for:
- **Duplicates** (closed tasks with nearly identical titles) - ask user before proceeding
- **Related work** (same files/features) - note for context
- **In-progress** by other agents - coordinate to avoid conflicts

### STEP 6: Conflict Detection

```bash
am-reservations --json          # Check file locks
git diff-index --quiet HEAD --  # Check uncommitted changes
```

### STEP 7: Start the Task

```bash
# Update task status
jt update "$TASK_ID" --status in_progress --assignee "$AGENT_NAME"

# Reserve files you'll edit
am-reserve "relevant/files/**" --agent "$AGENT_NAME" --ttl 3600 --reason "$TASK_ID"
```

### STEP 8: Emit Signals

**Both signals are required before starting actual work.**

#### 8A: Starting Signal

```bash
jat-signal starting '{
  "agentName": "AGENT_NAME",
  "sessionId": "SESSION_ID",
  "taskId": "TASK_ID",
  "taskTitle": "TASK_TITLE",
  "project": "PROJECT",
  "model": "MODEL_ID",
  "tools": ["bash", "read", "write", "edit"],
  "gitBranch": "BRANCH",
  "gitStatus": "clean",
  "uncommittedFiles": []
}'
```

#### 8B: Working Signal

After reading the task and planning your approach:

```bash
jat-signal working '{
  "taskId": "TASK_ID",
  "taskTitle": "TASK_TITLE",
  "approach": "Brief description of implementation plan",
  "expectedFiles": ["src/**/*.ts"],
  "baselineCommit": "COMMIT_HASH"
}'
```

#### 8C: Output Banner

```
╔════════════════════════════════════════════════════════════╗
║         STARTING WORK: {TASK_ID}                           ║
╚════════════════════════════════════════════════════════════╝

Agent: {AGENT_NAME}
Task: {TASK_TITLE}
Priority: P{X}

Approach:
  {YOUR_APPROACH_DESCRIPTION}
```

## Asking Questions During Work

**Always emit `needs_input` signal BEFORE asking questions:**

```bash
jat-signal needs_input '{
  "taskId": "TASK_ID",
  "question": "Brief description of what you need",
  "questionType": "clarification"
}'
```

Question types: `clarification`, `decision`, `approval`, `blocker`, `duplicate_check`

After getting a response, emit `working` signal to resume.

## When You Finish Working

**Emit `review` signal BEFORE presenting results:**

```bash
jat-signal review '{
  "taskId": "TASK_ID",
  "taskTitle": "TASK_TITLE",
  "summary": ["What you accomplished", "Key changes"],
  "filesModified": [
    {"path": "src/file.ts", "changeType": "modified", "linesAdded": 50, "linesRemoved": 10}
  ]
}'
```

Then output:
```
READY FOR REVIEW: {TASK_ID}

Summary:
  - [accomplishment 1]
  - [accomplishment 2]

Run /skill:jat-complete when ready to close this task.
```

## Signal Reference

| Signal | When | Required Fields |
|--------|------|-----------------|
| `starting` | After registration | agentName, sessionId, project, model, gitBranch, gitStatus, tools |
| `working` | Before coding | taskId, taskTitle, approach |
| `needs_input` | Before asking questions | taskId, question, questionType |
| `review` | When work complete | taskId, taskTitle, summary |
