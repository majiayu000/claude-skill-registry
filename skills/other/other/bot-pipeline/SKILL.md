---
name: bot-pipeline
description: |
  Coordinate work between registered bots via inbox/outbox pattern. Pass tasks to specialist agents (Cody, researcher, seo, contentwriter, etc.) and consolidate results.
  
  MANDATORY TRIGGERS: delegate to, pass to, send to bot, coordinate with, hand off to, bot pipeline, delegate task
---

# Bot Pipeline Coordination

Pass work between registered bots using the inbox/outbox handoff pattern.

## Available Bots

| Bot | Workspace | Specialty |
|-----|-----------|-----------|
| cody | workspace-cody | Coding, implementation |
| researcher | workspace-researcher | Research, web search |
| seo | workspace-seo | SEO optimization |
| contentwriter | workspace-contentwriter | Content, copy |
| marketing | workspace-marketing | Marketing campaigns |
| data-analyst | workspace-data-analyst | Data analysis |

## Workflow

### 1. Receive Task
- Check orchestrator's inbox for new tasks: `~/.openclaw/workspace-orchestrator/inbox/`
- Read task from `instructions.md` in inbox

### 2. Route to Specialist
For each bot, the path pattern is:
```
~/.openclaw/workspace-<bot>/inbox/instructions.md
~/.openclaw/workspace-<bot>/outbox/results.md
~/.openclaw/workspace-<bot>/status.json
```

**To delegate to a bot:**
1. Write task to `<bot>/inbox/instructions.md`
2. Update `<bot>/status.json` with `{"state": "pending", "task": "description"}`
3. Notify the bot via sessions_send or let it check on next turn

### 3. Monitor Progress
Check `status.json` for each bot:
- `pending` - Task assigned, not started
- `running` - Bot is working
- `completed` - Results ready in outbox/
- `failed` - Error occurred

### 4. Collect Results
When bot status = completed:
1. Read results from `<bot>/outbox/results.md`
2. Clear the outbox after reading
3. Update status to `{"state": "ready"}`

### 5. Consolidate
Combine results from all bots into final deliverable.

## Example: Product Launch Task

```python
# 1. Read incoming task
task = read("~/.openclaw/workspace-orchestrator/inboxinstructions.md")

# 2. Delegate to researcher
write("~/.openclaw/workspace-researcher/inbox/instructions.md", """
Research brief: [product name]
- Competitor analysis
- Target audience insights
- Keyword research
Deliver to outbox/results.md
""")
write("~/.openclaw/workspace-researcher/status.json", '{"state": "pending", "task": "research"}')

# 3. Delegate to contentwriter (after researcher completes)
# ... wait for researcher status = completed

# 4. Collect and consolidate
research_results = read("~/.openclaw/workspace-researcher/outbox/results.md")
```

## File Paths (for reference)

```python
ORCHESTRATOR_INBOX = "~/.openclaw/workspace-orchestrator/inbox"
ORCHESTRATOR_OUTBOX = "~/.openclaw/workspace-orchestrator/outbox"

BOT_BASE = "~/.openclaw/workspace-{bot}"
BOT_INBOX = f"{BOT_BASE}/inbox/instructions.md"
BOT_OUTBOX = f"{BOT_BASE}/outbox/results.md"
BOT_STATUS = f"{BOT_BASE}/status.json"
```

## Key Principles

1. **Always write instructions first** - Don't assume bot knows context
2. **Check status before reading outbox** - Don't race condition
3. **Clear outbox after reading** - Prevent duplicate processing
4. **Handle failures gracefully** - Log errors, try alternatives
5. **Consolidate explicitly** - Don't leave gaps between handoffs
