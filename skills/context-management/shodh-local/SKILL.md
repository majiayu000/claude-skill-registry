---
name: shodh-local
summary: Local-first cognitive memory for AI agents with semantic recall, GTD todos, and knowledge graph.
description: Local Shodh-Memory v0.1.74 (offline cognitive memory for AI agents). Use for persistent remembering, semantic recall, GTD todos/projects, knowledge graph. Triggers: \"remember/save/merke X\", \"recall/Erinnere/search memories about Y\", \"todos/add/complete\", \"projects\", \"proactive context\", \"what learned about Z\". Server localhost:3030 (amber-seaslug), key in TOOLS.md. Hebbian learning, 3-tier (working/session/LTM), TUI dashboard.
---

# Shodh-Local (v0.1.74)

Local-first brain for OpenClaw. Offline, learns with use.

## Config (TOOLS.md)
- **Binary**: `./shodh-memory-server` (or add to PATH)
- **Server**: `localhost:3030`
- **Data**: `./shodh-data`
- **Key**: `<YOUR-API-KEY>` (X-API-Key, generate via shodh-memory-server)
- **Manage**: `process` tool (session `amber-seaslug`)
- **TUI**: `cd tools/shodh-memory && ./shodh-tui` (graph/activity)

## Quick Use
```
KEY='<YOUR-API-KEY>'
curl -s -X POST http://localhost:3030/api/remember \\
-H &quot;Content-Type: application/json&quot; -H &quot;X-API-Key: $KEY&quot; \\
-d &#39;{&quot;user_id&quot;: &quot;henry&quot;, &quot;content&quot;: &quot;Test memory&quot;, &quot;memory_type&quot;: &quot;Learning&quot;, &quot;tags&quot;: [&quot;test&quot;]}&#39;
```

## Core Tools
- **Remember**: `/api/remember` (types: Learning/Observation/Conversation/Task/Preference)
- **Recall**: `/api/recall` (semantic) | `/api/recall/tags`
- **Proactive**: `/api/proactive_context` (auto-relevant)
- **Todos**: `/api/todos/add` | `/api/todos` | `/api/todos/complete`
- **Projects**: `/api/projects/add` | `/api/projects`
- **Summary**: `/api/context_summary`

Full API: [reference/api.md](reference/api.md)

## Best Practices
- **User ID**: `henry` (main), `openclaw` (system), `task-XYZ` (sub-agents)
- **Tags**: Always add for filtering (e.g. [&quot;openclaw&quot;, &quot;project-backend&quot;])
- **Before reply**: Recall recent context for continuity
- **Heartbeat**: Check todos daily
- **Maintenance**: Restart server weekly (`process kill amber-seaslug` + restart)

Read [reference/examples.md](reference/examples.md) for OpenClaw patterns.