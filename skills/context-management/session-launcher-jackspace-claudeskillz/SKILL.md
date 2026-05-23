---
name: session-launcher
description: Restores full context when user says "hi-ai" or starts a new conversation. Searches project files, loads memory indexes, reads session state, and creates visual dashboard showing current project, recent decisions, active blockers, and quick actions. Use when user says "hi-ai", "continue", "restore context", or starts a fresh conversation.
---

# Session Launcher

## Purpose

Zero context loss between conversations. When a new session starts, this skill:
1. Searches for project context files
2. Loads memory indexes and past decisions
3. Reads session state
4. Creates visual dashboard with actionable links
5. Makes you immediately productive

**For SDAM users**: Compensates for lack of episodic memory by externalizing all session context.
**For ADHD users**: Eliminates "where was I?" friction - instant continuation.
**For dyschronometria**: Shows explicit timestamps on all context.

## Activation Triggers

- User says: "hi-ai"
- User says: "continue", "restore context", "what was I working on"
- Start of new conversation (proactively offer)

## Core Workflow

### 1. Search for Context Files

Check these locations in order:

```bash
# Current project context
./.context/current.json
./.context/session.json
./DECISIONS.md
./README.md

# User's memory storage
/home/toowired/.claude-memories/index.json
/home/toowired/.claude-sessions/current.json
/home/toowired/.claude-sessions/projects/
```

### 2. Load Memory Index

Read `/home/toowired/.claude-memories/index.json`:

```json
{
  "total_memories": N,
  "memories": [
    {
      "id": "unique-id",
      "type": "DECISION|BLOCKER|CONTEXT|PREFERENCE|PROCEDURE",
      "content": "the memory",
      "timestamp": "ISO8601",
      "tags": ["tag1", "tag2"],
      "project": "project-name"
    }
  ]
}
```

Extract:
- Recent decisions (last 7 days)
- Active blockers (status != "resolved")
- Project context (matching current directory)
- User preferences

### 3. Identify Current Project

Determine project from:
1. Current working directory name
2. `.context/project.txt` if exists
3. Git repository name: `basename $(git rev-parse --show-toplevel 2>/dev/null)`
4. Ask user if unclear

### 4. Create Session Dashboard

Generate HTML file at `/home/toowired/.claude-artifacts/session-dashboard-{timestamp}.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Session Restored</title>
    <style>
        body {
            font-family: monospace;
            max-width: 1200px;
            margin: 40px auto;
            padding: 20px;
            background: #1e1e1e;
            color: #d4d4d4;
        }
        .section {
            background: #252526;
            border: 1px solid #3e3e42;
            border-radius: 6px;
            padding: 20px;
            margin: 20px 0;
        }
        .section h2 {
            margin-top: 0;
            color: #4ec9b0;
            border-bottom: 1px solid #3e3e42;
            padding-bottom: 10px;
        }
        .timestamp {
            color: #858585;
            font-size: 0.9em;
        }
        .decision {
            background: #2d2d30;
            padding: 10px;
            margin: 10px 0;
            border-left: 3px solid #4ec9b0;
        }
        .blocker {
            background: #2d2d30;
            padding: 10px;
            margin: 10px 0;
            border-left: 3px solid #f48771;
        }
        .action {
            display: inline-block;
            background: #0e639c;
            color: white;
            padding: 8px 16px;
            margin: 5px;
            border-radius: 4px;
            text-decoration: none;
        }
        .metric {
            font-size: 2em;
            color: #4ec9b0;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>🚀 Session Restored</h1>
    <p class="timestamp">Restored at: {current_timestamp}</p>

    <div class="section">
        <h2>📁 Current Project</h2>
        <div class="metric">{project_name}</div>
        <p>Location: <code>{project_path}</code></p>
        <p>Last worked: <span class="timestamp">{last_session_time}</span></p>
    </div>

    <div class="section">
        <h2>🎯 Recent Decisions (Last 7 Days)</h2>
        {for each recent decision:}
        <div class="decision">
            <strong>{decision.content}</strong>
            <div class="timestamp">{decision.timestamp} - {relative_time}</div>
            {if decision.tags:}<p>Tags: {tags_joined}</p>{endif}
        </div>
        {endfor}
    </div>

    <div class="section">
        <h2>🚧 Active Blockers</h2>
        {for each active blocker:}
        <div class="blocker">
            <strong>{blocker.content}</strong>
            <div class="timestamp">{blocker.timestamp} - {relative_time}</div>
        </div>
        {endfor}
        {if no blockers:}<p>✅ No active blockers</p>{endif}
    </div>

    <div class="section">
        <h2>📊 Memory Stats</h2>
        <p>Total memories: <span class="metric">{total_memories}</span></p>
        <p>Decisions: {decision_count} | Blockers: {blocker_count} | Procedures: {procedure_count}</p>
    </div>

    <div class="section">
        <h2>⚡ Quick Actions</h2>
        <a href="file:///home/toowired/.claude-memories/index.json" class="action">View All Memories</a>
        <a href="file://{project_path}" class="action">Open Project</a>
        <a href="file:///home/toowired/.claude-artifacts/" class="action">View Artifacts</a>
    </div>
</body>
</html>
```

### 5. Output Summary

After creating dashboard, output to user:

```
🚀 Session Restored

📁 Project: {project_name}
📍 Location: {project_path}
🕐 Last worked: {relative_time}

📝 Recent Decisions ({count}):
{for each decision (max 5):}
  • {decision.content} ({relative_time})
{endfor}

🚧 Active Blockers ({count}):
{for each blocker:}
  • {blocker.content} ({relative_time})
{endfor}

💾 Memory: {total_memories} total memories loaded

📊 Dashboard: {dashboard_path}

✅ Full context restored. Ready to continue!

What would you like to work on?
```

## Memory Integration

### Reading Memories

Always check memory index for:
- Project-specific context
- User preferences (tech stack, coding style)
- Past decisions affecting current work
- Similar past problems/solutions

### Time Anchoring (for Dyschronometria)

Convert all timestamps to relative format:
- "2 hours ago"
- "3 days ago"
- "Last Tuesday"
- Include ISO timestamp for precision

### Context Filtering

Filter memories by:
1. **Project match**: `memory.project === current_project`
2. **Recency**: Last 30 days weighted higher
3. **Type priority**: BLOCKER > DECISION > CONTEXT > PROCEDURE
4. **Relevance**: Tag matching if available

## Session State Management

### Saving Session State

Before ending conversation (if user says "goodbye", "see you", "done for now"):

1. Create/update `/home/toowired/.claude-sessions/current.json`:

```json
{
  "project": "project-name",
  "project_path": "/full/path",
  "last_active": "ISO8601_timestamp",
  "last_files": [
    "/path/to/file1.js",
    "/path/to/file2.py"
  ],
  "last_topic": "Brief description of what we were working on",
  "next_actions": [
    "Suggested next step 1",
    "Suggested next step 2"
  ]
}
```

2. Update memory index with session summary:

```json
{
  "type": "NOTE",
  "content": "Session ended: {brief_summary_of_work}",
  "timestamp": "ISO8601",
  "tags": ["session", "project-name"],
  "project": "project-name"
}
```

### Project-Specific Sessions

For multi-project users, maintain:

```
/home/toowired/.claude-sessions/projects/
├── boostbox.json
├── toolhub.json
├── 88dimensions.json
└── mcp-stack.json
```

Each contains project-specific state.

## Visual Dashboard Features

### For Aphantasia Users

Always provide:
- **Concrete metrics** (numbers, counts)
- **Visual structure** (HTML dashboard)
- **Explicit links** (clickable file paths)
- **Status indicators** (✅ ❌ 🚧 emojis)

### For ADHD Users

Dashboard must:
- **Load instantly** (<2 seconds)
- **Show quick actions** (immediate next steps)
- **Highlight blockers** (red/urgent visual treatment)
- **Provide direct links** (one-click access to files)

### For SDAM Users

Dashboard must:
- **Externalize all context** (no assumption of memory)
- **Show time anchors** (when things happened)
- **Display decision history** (what was decided)
- **Link to artifacts** (proof of past work)

## Error Handling

### If No Context Found

```
👋 Hi! This looks like a fresh start.

I couldn't find existing session context, so let's establish some:

1. What project are you working on?
2. Should I create a memory index for you?
3. Would you like to start tracking decisions?

(I'll create the necessary directories and get you set up)
```

### If Memory Index Corrupted

```
⚠️ Memory index appears corrupted.

Creating backup at: /home/toowired/.claude-memories/backups/index-{timestamp}.json
Initializing fresh index...

✅ Fresh index created. Previous memories backed up.
```

### If Multiple Projects Detected

```
🤔 I found context for multiple projects:

1. BOOSTBOX (last active: 2 days ago)
2. Tool Hub (last active: 5 days ago)
3. MCP Stack (last active: 1 week ago)

Which project would you like to work on?
```

## Integration with Other Skills

### Memory Manager

- Queries memory-manager for structured memory search
- Defers complex memory operations to memory-manager
- Uses memory-manager's categorization system

### Context Manager

- Works with context-manager to maintain `.context/` directory
- Reads context-manager's structured data
- Updates session state via context-manager

### Error Debugger

- Surfaces recent blockers for error-debugger to consider
- Checks if current error matches past error memories

## Quick Reference

### File Locations

- **Memory index**: `/home/toowired/.claude-memories/index.json`
- **Current session**: `/home/toowired/.claude-sessions/current.json`
- **Project sessions**: `/home/toowired/.claude-sessions/projects/{name}.json`
- **Dashboards**: `/home/toowired/.claude-artifacts/session-dashboard-*.html`

### Trigger Phrases

- "hi-ai" (primary)
- "continue"
- "restore context"
- "what was I working on"
- "where did we leave off"

### Success Criteria

✅ User says "hi-ai" and is immediately productive
✅ No need to explain "what we were working on"
✅ All past decisions visible
✅ Active blockers surfaced
✅ Context restored in <2 seconds
