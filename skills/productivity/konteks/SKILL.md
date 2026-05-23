---
name: konteks
version: 1.0.1
author: jamesalmeida
description: Connect your OpenClaw agent to your Konteks account (konteks.app) for persistent memory, task management, and context sharing. Use when you need to store agent memories, create or read tasks/notes, check projects and folders, read daily plans, or sync context between conversations. Requires a Konteks API key from konteks.app/dashboard/settings.
when: User asks to create/manage tasks, store memories, check projects, read daily plans, or manage notes in Konteks
examples:
  - Create a task to review the PR
  - What's on my agenda today
  - Remember that I prefer dark mode
  - Check my inbox for new items
  - What projects do I have
tags:
  - memory
  - tasks
  - notes
  - projects
  - context
  - productivity
metadata: { "openclaw": { "emoji": "🧠", "requires": { "env": ["KONTEKS_API_KEY"] }, "primaryEnv": "KONTEKS_API_KEY" } }
---

# Konteks — Agent Context Layer

**Source:** https://github.com/jamesalmeida/openclaw-konteks-skill

Connect to your human's Konteks account for persistent memory, tasks, notes, and projects.

## Setup

Your human needs to:
1. Sign up at https://konteks.app
2. Go to Settings → Generate API Key
3. Add to OpenClaw config:

```yaml
skills:
  konteks:
    apiKey: "sk_..."
    url: "https://konteks.app"  # optional, defaults to this
    agentId: "my-agent"         # optional, defaults to "default"
```

## API Base

All endpoints: `{url}/api/agent/...`
Auth header: `Authorization: Bearer {apiKey}`

---

## Hybrid Memory Architecture

When this skill is installed, use a **hybrid approach** to memory — Konteks DB for shared structured data, local files for fast scratchpad notes.

### Konteks DB (shared source of truth)
Use Konteks for anything your human should also see or that needs to persist across devices:
- **Tasks & items** — created by human or agent, visible in the iOS and web apps
- **Projects & areas** — the organizational structure
- **Decisions** — why something was chosen (write to `agent_contexts` with category `decision`)
- **Preferences** — user preferences you learn over time (category `preference`)
- **Learnings** — things you discover that matter long-term (category `learning`)
- **Project notes** — context about specific projects (category `project_note`)

### Local markdown (agent scratchpad)
Keep using local files (`memory/*.md`, `MEMORY.md`) for:
- **Daily session logs** — raw notes about what happened today
- **Working context** — things you're actively thinking about this session
- **Drafts & scratch work** — ideas in progress before they're ready for Konteks

### How they work together
- **Session start:** Pull recent memories from Konteks (`GET /api/agent/context?limit=10`) to restore context. Also read local daily files as usual.
- **During conversation:** Take quick notes in local markdown. When something important is decided or learned, write it to Konteks too.
- **After important moments:** Write decisions and learnings to Konteks so they persist in the app and survive local file changes.
- **Heartbeats:** Check Konteks for inbox items and due tasks. Update local heartbeat state.
- **If Konteks is unreachable:** Fall back to local files. You should always be able to function without network access.

This way your human sees important context in their Konteks app, and you have fast local access for working memory. Neither system is a single point of failure.

---

## Proactive Behavior (Heartbeats)

**When this skill is installed, the agent should proactively use Konteks during heartbeats.** Add these checks to your heartbeat routine:

### 1. Inbox Triage
Check the inbox for new items and file them into the right project/area if obvious:

```bash
# Fetch inbox items
curl -s "{url}/api/agent/items?smart_list=inbox&completed=false&archived=false&limit=20" \
  -H "Authorization: Bearer {apiKey}"
```

**Triage rules:**
- If the item clearly belongs to an existing project/area → move it there (`PATCH` with `folder_id`, clear `smart_list`)
- If you're not sure where it belongs → **leave it in the inbox**. Don't guess.
- If it's something you can handle yourself (e.g., "update X", "check Y") → do it, then mark complete
- Never delete inbox items — move or leave them

```bash
# Move item to a folder (clears smart_list automatically when folder_id is set)
curl -X PATCH "{url}/api/agent/items/{id}" \
  -H "Authorization: Bearer {apiKey}" \
  -H "Content-Type: application/json" \
  -d '{"folder_id":"<folder-id>","smart_list":null}'
```

### 2. Due & Overdue Items
Check for tasks due today or overdue:

```bash
curl -s "{url}/api/agent/items?completed=false&archived=false&limit=50" \
  -H "Authorization: Bearer {apiKey}"
```

Filter results for items where `due_date` or `scheduled_date` is today or past. Alert your human if anything urgent needs attention.

### 3. Write Memories After Important Moments
After significant decisions, learnings, or events during conversation, write them to Konteks:

```bash
curl -X POST "{url}/api/agent/context" \
  -H "Authorization: Bearer {apiKey}" \
  -H "Content-Type: application/json" \
  -d '{"category":"decision","key":"descriptive_key","value":"What was decided and why","agent_id":"{agentId}"}'
```

### 4. Restore Context on Session Start
At the start of important sessions (main chat with your human), pull recent memories:

```bash
curl -s "{url}/api/agent/context?limit=10" \
  -H "Authorization: Bearer {apiKey}"
```

### Heartbeat Integration

Add to your `HEARTBEAT.md` (or equivalent):

```markdown
## Konteks Checks
- [ ] Check inbox for new items — triage if obvious, leave if not
- [ ] Check for due/overdue tasks — alert if urgent
- [ ] Write any recent decisions/learnings to agent_contexts
```

**Frequency:** Check inbox and due items 2-3 times per day during heartbeats. Don't check every single heartbeat — rotate with other checks.

---

## Agent Memory (agent_contexts)

Store and retrieve persistent memories, decisions, preferences, and learnings.

**Write/update memory:**
```bash
curl -X POST "{url}/api/agent/context" \
  -H "Authorization: Bearer {apiKey}" \
  -H "Content-Type: application/json" \
  -d '{"category":"memory","key":"user_preference","value":"Prefers dark mode","agent_id":"{agentId}"}'
```

Categories: `memory`, `decision`, `preference`, `learning`, `project_note`

Upserts automatically — same agent_id + category + key updates the existing entry.

**Read memory:**
```bash
curl "{url}/api/agent/context?category=memory&limit=20" \
  -H "Authorization: Bearer {apiKey}"
```

Query params: `category`, `key`, `limit`

**Delete:**
```bash
curl -X DELETE "{url}/api/agent/context?id={contextId}" \
  -H "Authorization: Bearer {apiKey}"
```

## Tasks & Notes (items)

**List items:**
```bash
curl "{url}/api/agent/items?archived=false&completed=false&limit=50" \
  -H "Authorization: Bearer {apiKey}"
```

Query params: `smart_list` (inbox|anytime|someday), `folder_id`, `completed` (true|false), `archived` (true|false), `item_type` (task|note|hybrid), `limit`

**Create item:**
```bash
curl -X POST "{url}/api/agent/items" \
  -H "Authorization: Bearer {apiKey}" \
  -H "Content-Type: application/json" \
  -d '{"title":"Review PR","item_type":"task","smart_list":"inbox","priority":"high","tags":["dev"]}'
```

Required: `title`, `item_type` (task|note|hybrid)
Optional: `body`, `folder_id`, `smart_list` (inbox|anytime|someday — defaults to inbox if no folder), `priority` (high|normal|low), `due_date`, `scheduled_date`, `tags` (string array)

Items created by agent have `source: "ai"`.

**Update item:**
```bash
curl -X PATCH "{url}/api/agent/items/{id}" \
  -H "Authorization: Bearer {apiKey}" \
  -H "Content-Type: application/json" \
  -d '{"completed_at":"2026-01-29T12:00:00Z"}'
```

Updatable fields: `title`, `body`, `priority`, `due_date`, `scheduled_date`, `tags`, `completed_at`, `archived_at`, `canceled_at`, `folder_id`, `smart_list`

**Delete item:**
```bash
curl -X DELETE "{url}/api/agent/items/{id}" \
  -H "Authorization: Bearer {apiKey}"
```

## Projects & Areas (folders)

**List folders:**
```bash
curl "{url}/api/agent/folders?type=project" \
  -H "Authorization: Bearer {apiKey}"
```

Query params: `type` (project|area)

**Create folder:**
```bash
curl -X POST "{url}/api/agent/folders" \
  -H "Authorization: Bearer {apiKey}" \
  -H "Content-Type: application/json" \
  -d '{"name":"Q1 Launch","folder_type":"project","icon":"🚀","goal":"Ship MVP by March"}'
```

Required: `name`, `folder_type` (project|area)
Optional: `icon`, `color`, `goal`

## Daily Plans

**Get today's plan:**
```bash
curl "{url}/api/agent/plans?date=2026-01-29" \
  -H "Authorization: Bearer {apiKey}"
```

Returns: `task_ids`, `summary`, `rationale`, `available_minutes`, `calendar_events`

---

## Usage Patterns

**On session start:** Read recent memories to restore context.
```
GET /api/agent/context?category=memory&limit=10
```

**After important decisions:** Write a memory entry.
```
POST /api/agent/context {"category":"decision","key":"chose_react","value":"Chose React over Vue for the dashboard because..."}
```

**When human asks to create a task:** Create it in Konteks so it shows in their app.
```
POST /api/agent/items {"title":"...","item_type":"task","smart_list":"inbox"}
```

**During heartbeats:** Check inbox, triage items, check for overdue tasks.
```
GET /api/agent/items?smart_list=inbox&completed=false&archived=false&limit=20
GET /api/agent/items?completed=false&archived=false&limit=50
```

**Learning something new:** Store it for future sessions.
```
POST /api/agent/context {"category":"learning","key":"ssh_config","value":"Home server is at 192.168.1.100, user admin"}
```

**Filing an inbox item:** Move to the right project/area.
```
PATCH /api/agent/items/{id} {"folder_id":"<id>","smart_list":null}
```
