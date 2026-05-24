---
name: task-router-mcp
description: Multi-agent task orchestration MCP server. Queue-based workflow where Claude Desktop assigns tasks → agents claim → execute → report completion → next task auto-assigned.
type: mcp-server
---

# Task-Router MCP Server

## Function

Coordinates multi-agent workflows via task queue. Eliminates manual handoffs.

## Architecture

```
Claude Desktop (Orchestrator)
    ↓ creates tasks
Task Queue (JSON file-based)
    ↓ agents poll
[Gemini | Claude Code | Codex CLI]
    ↓ claim → execute → complete
Next Task Auto-assigned
```

## MCP Tools

### 1. `create_task`

```json
{
  "task_id": "asset-3-generation",
  "assigned_to": "gemini",
  "status": "pending",
  "priority": "high",
  "inputs": {
    "prompt": "[full prompt text]",
    "resolution": "512x512"
  },
  "outputs": null,
  "next_task": "asset-3-validation",
  "next_assigned_to": "claude-desktop"
}
```

### 2. `claim_task`

Agent marks task as in-progress:
```json
{
  "task_id": "asset-3-generation",
  "status": "in_progress",
  "claimed_by": "gemini",
  "claimed_at": "2026-01-30T10:15:00Z"
}
```

### 3. `complete_task`

Agent reports completion:
```json
{
  "task_id": "asset-3-generation",
  "status": "completed",
  "outputs": {
    "image_path": "/downloads/asset-3-attempt-2.png",
    "notes": "Generated successfully"
  },
  "completed_at": "2026-01-30T10:18:00Z"
}
```

### 4. `list_tasks`

Query tasks by status/agent:
```json
{
  "status": "pending",
  "assigned_to": "gemini"
}
```

Returns array of matching tasks.

### 5. `rollback_task`

If validation fails, rollback to previous state:
```json
{
  "task_id": "asset-3-validation",
  "rollback_to": "asset-3-generation",
  "reason": "Score 85 (below 90 threshold)"
}
```

## Task Flow Example

**Phase: Asset 3 Generation**

1. Claude Desktop creates task:
```json
{
  "task_id": "asset-3-gen",
  "assigned_to": "gemini",
  "inputs": {"prompt": "...", "resolution": "512x512"},
  "next_task": "asset-3-validate"
}
```

2. Gemini polls queue → claims task → generates → completes:
```json
{
  "status": "completed",
  "outputs": {"image_path": "/downloads/asset-3.png"}
}
```

3. Router auto-creates next task:
```json
{
  "task_id": "asset-3-validate",
  "assigned_to": "claude-desktop",
  "inputs": {"image_path": "/downloads/asset-3.png"}
}
```

4. Claude Desktop claims → validates → scores 92 → completes
5. Router auto-creates packaging task for Claude Code

## Implementation

**File:** `/servers/task_router_mcp.py`

**Queue Storage:** `/tmp/northcote-task-queue.json`

```python
class TaskRouter:
    def __init__(self):
        self.queue_file = "/tmp/northcote-task-queue.json"
        self.tasks = self.load_queue()
    
    def create_task(self, task_data):
        task = {
            "task_id": task_data['task_id'],
            "assigned_to": task_data['assigned_to'],
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            **task_data
        }
        self.tasks.append(task)
        self.save_queue()
        return task
    
    def claim_task(self, task_id, agent):
        task = self.get_task(task_id)
        task['status'] = 'in_progress'
        task['claimed_by'] = agent
        task['claimed_at'] = datetime.now().isoformat()
        self.save_queue()
    
    def complete_task(self, task_id, outputs):
        task = self.get_task(task_id)
        task['status'] = 'completed'
        task['outputs'] = outputs
        task['completed_at'] = datetime.now().isoformat()
        
        # Auto-create next task if specified
        if task.get('next_task'):
            self.create_task({
                'task_id': task['next_task'],
                'assigned_to': task['next_assigned_to'],
                'inputs': outputs  # Previous outputs → next inputs
            })
        
        self.save_queue()
```

## Integration

**Claude Desktop Config:**
```json
{
  "mcpServers": {
    "task-router": {
      "command": "python3",
      "args": ["/path/to/task_router_mcp.py"]
    }
  }
}
```

## Agent Polling

Each agent polls queue every 30 seconds:

**Gemini (Antigravity):**
```python
while True:
    tasks = mcp.call_tool("task-router", "list_tasks", {
        "status": "pending",
        "assigned_to": "gemini"
    })
    if tasks:
        task = tasks[0]
        mcp.call_tool("task-router", "claim_task", {"task_id": task['task_id']})
        # Execute generation
        mcp.call_tool("task-router", "complete_task", {
            "task_id": task['task_id'],
            "outputs": {"image_path": result_path}
        })
    time.sleep(30)
```

## Progress Tracking

Dashboard view:
```json
{
  "total_tasks": 47,
  "completed": 23,
  "in_progress": 3,
  "pending": 21,
  "by_agent": {
    "gemini": {"completed": 10, "in_progress": 1},
    "claude-code": {"completed": 8, "in_progress": 2},
    "codex": {"completed": 5, "in_progress": 0}
  }
}
```

## Benefits

- Eliminates manual handoffs
- Progress tracking built-in
- Rollback capability
- Agent autonomy (claim tasks independently)
- Context preserved in task chain

---

*Queue-based orchestration. Manual coordination → automatic workflow.*
