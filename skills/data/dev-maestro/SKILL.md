---
name: dev-maestro
description: Start Dev Maestro dashboard for MASTER_PLAN.md tasks. Use when user says "start maestro", "open kanban", or "show tasks". Also use when tasks show wrong status (PLANNED instead of DONE) - see Parser Troubleshooting section.
---

# Dev Maestro Skill

## QUICK REFERENCE

| Item | Value |
|------|-------|
| URL | http://localhost:PORT |
| Install | `~/.dev-maestro` |
| Default Port | 6010 |

## WHEN TO USE

- User says "start maestro" / "open kanban" / "show tasks"
- User wants to see MASTER_PLAN.md visually
- User asks about task status in Kanban view
- Task shows wrong status in Dev Maestro (e.g., "PLANNED" instead of "DONE")
- User reports "task still shows as planned" after marking it done

## WHEN NOT TO USE

- User is working on their main project (Dev Maestro is a tool, not a target)
- User didn't mention Dev Maestro
- You're tempted to "improve" or extend Dev Maestro

## WORKFLOW

### Step 0: Ask User for Port Preference

Before installing or starting, ask the user:

> "What port should Dev Maestro run on? (default: 6010)"

Use their answer for PORT in all subsequent commands. If they say "default" or don't specify, use 6010.

### Step 1: Check if Already Running

```bash
curl -s http://localhost:PORT/api/status 2>/dev/null && echo "RUNNING" || echo "NOT RUNNING"
```

### Step 2: Install if Needed (Foolproof Method)

**Download first, then run (avoids terminal line-wrap issues):**

```bash
curl -sSL "https://raw.githubusercontent.com/endlessblink/dev-maestro/main/install.sh" -o /tmp/dm-install.sh
```

```bash
bash /tmp/dm-install.sh -m /path/to/docs/MASTER_PLAN.md
```

### Step 3: Start with Custom Port

```bash
cd ~/.dev-maestro && PORT=PORT npm start &
```

### Step 4: Verify

```bash
sleep 3 && curl -s http://localhost:PORT/api/status
```

### Step 5: Tell User

> "Dev Maestro is running at http://localhost:PORT"

## API ENDPOINTS

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /api/status | Check if running |
| GET | /api/master-plan | Get tasks from MASTER_PLAN.md |
| GET | /api/health/quick | Project health summary |
| POST | /api/task/add | Add task (body: `{"title":"..."}`) |

## ANTI-SIDETRACKING RULES

1. **Don't build features for Dev Maestro** - It's a separate project
2. **Don't add MCP wrappers** - REST API via curl is sufficient
3. **Don't refactor Dev Maestro code** - Stay focused on user's actual task
4. **Use curl directly** - No abstractions needed

## TROUBLESHOOTING

**Port in use:**
```bash
lsof -ti:PORT | xargs kill -9 && cd ~/.dev-maestro && PORT=PORT npm start &
```

**MASTER_PLAN.md not found:**
```bash
# Check current path
curl -s localhost:PORT/api/status | jq '.masterPlanPath'

# Reconfigure
cd ~/.dev-maestro && ./install.sh --reconfigure
```

## PARSER TROUBLESHOOTING (Task Shows Wrong Status)

**Full SOP**: `docs/sop/SOP-028-dev-maestro-task-sync.md`

### QUICK FIX (Do This First!)

When a task shows wrong status (e.g., "IN PROGRESS" instead of "DONE"):

```bash
# 1. Find ALL occurrences of the task
grep -n "TASK-XXX" docs/MASTER_PLAN.md

# 2. Update EACH location with consistent status (strikethrough + ✅ DONE)

# 3. Restart Dev Maestro (CRITICAL - clears server cache)
lsof -i :6010 -t | xargs kill 2>/dev/null
cd ~/.dev-maestro && nohup npm start > /tmp/dev-maestro.log 2>&1 &

# 4. Hard refresh browser (CRITICAL - clears browser cache)
# Press Ctrl+Shift+R (not just F5)
```

### Why This Happens

MASTER_PLAN.md has tasks in **multiple locations**:
1. **Summary table** (~lines 25-200) - `| ~~**TASK-XXX**~~ | ✅ **DONE** ... |`
2. **Detailed sections** - `### ~~TASK-XXX~~: Title (✅ DONE)`

Dev Maestro parses BOTH. If they disagree, you get wrong status.

### Marking Tasks Done Correctly

Update ALL occurrences:

| Location | What to Change |
|----------|----------------|
| Summary table ID | Add `~~` strikethrough: `~~**TASK-XXX**~~` |
| Summary table title | Add `✅ **DONE**` prefix |
| Summary table status column | Change to `✅ **DONE** (date)` |
| Detailed section header | `### ~~TASK-XXX~~: Title (✅ DONE)` |
| Detailed section `**Status**:` line | `**Status**: ✅ DONE (date)` |

### Verify Fix

```bash
# All occurrences should show DONE/strikethrough
grep "TASK-XXX" docs/MASTER_PLAN.md
```

### Debug via Browser Console

```javascript
// Open DevTools (F12) at http://localhost:6010/kanban/
// Look for this in console after page load:
[DEBUG] TASK-XXX: { status: 'done', progress: 100, title: '...' }
```

### Parser Recognizes These Sections Only

- `## Ideas`
- `## Roadmap`
- `## Current Status`
- `## Active Work`
- `## Known Issues`
- `## Archive`
- `## Technical Debt`

**Unrecognized sections** (e.g., `## PWA Prerequisites`) don't reset the parser state, which can cause issues.

### Parser Status Detection

The parser looks for these patterns (in order):

| Pattern | Detected Status |
|---------|-----------------|
| `~~` in ID | done |
| `DONE`, `FIXED`, `✅` in any cell | done |
| `REVIEW`, `👀` | review |
| `IN PROGRESS`, `🔄` | in-progress |
| `PAUSED`, `⏸️` | paused |
| Default | todo |

### Known Bug Patterns

1. **Caching**: Browser/server cache shows old status → Restart + hard refresh
2. **Inconsistent marking**: Table says DONE but detailed section says PLANNED
3. **Missing strikethrough**: ID not struck through even if status says DONE
