---
name: test-harness
description: Tests the AI Harness Discord bot after code changes.
user-invocable: true
argument-hint: "[full|quick|manual-only]"
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# AI Harness Test Skill

You are testing the AI Harness Discord bot. Your job is to verify that changes work correctly by running automated tests and generating a manual checklist for anything that requires a live Discord connection.

## Changed Files
!`cd $HARNESS_ROOT/bridges/discord && git diff --name-only HEAD 2>/dev/null || echo "(no changes detected)"`

## Step 1: Understand What Changed

Map each changed file to its test domain:

| File | Test Domain | Automated? |
|------|------------|------------|
| `db.ts` | Schema, migration, WAL mode | Yes |
| `session-store.ts` | Session CRUD, last_used updates | Yes |
| `channel-config-store.ts` | Config CRUD, JSON array round-trip, partial merge | Yes |
| `process-registry.ts` | Subagent CRUD, stale PID cleanup | Yes |
| `project-manager.ts` | Project CRUD, handoff depth, auto-adopt, name uniqueness | Yes |
| `task-runner.ts` | Task submit/get, continuation detection, dead-letter, retry backoff | Yes |
| `file-watcher.ts` | Event detection, timeout, stopAll | Yes |
| `stream-poller.ts` | Chunk ordering, throttle, fs.watch | Partial (needs stream dir with chunks) |
| `bot.ts` | Command dispatch, queue management, task-runner integration | Manual (Discord) |
| `subagent-manager.ts` | Spawn, FileWatcher attachment, cancel | Manual (Discord + Claude CLI) |
| `handoff-router.ts` | Handoff parsing, chain execution, depth limits | Manual (Discord + project channels) |
| `activity-stream.ts` | Embed posting | Manual (Discord + STREAM_CHANNEL_ID) |
| `.claude/agents/*.md` | Agent prompts, [CONTINUE] marker | Manual (send task, verify behavior) |
| `claude-runner.py` | Process spawning, env cleaning, atomic writes | Manual (needs Claude CLI auth) |

## Step 2: Run Automated Tests

### 2a. TypeScript Compilation

```bash
cd $HARNESS_ROOT/bridges/discord
npx tsc --noEmit
```

**Expected**: Exit 0, no output. Any errors here are blockers.

### 2b. Native Module Check

```bash
node -e "require('better-sqlite3')" 2>&1; echo "EXIT: $?"
```

**Expected**: Exit 0. If this fails, `better-sqlite3` needs rebuilding (`npm rebuild better-sqlite3`).

### 2c. Integration Test Suite

```bash
cd $HARNESS_ROOT/bridges/discord
npx tsx test-upgrade.ts
```

**Expected**: All tests pass. The test suite covers:
- **Database Init** (10 assertions): Schema creation, WAL mode, table existence, version tracking
- **Session Store** (11 assertions): get/set/clear/validate/list, last_used update, stale clearing
- **Channel Config Store** (14 assertions): CRUD, partial update merge, JSON array fields, clear
- **Process Registry** (8 assertions): register/update/get/getRunning/getByChannel/cleanupStale
- **Project Manager** (16 assertions): adopt/auto-adopt/update/delete/handoff depth/uniqueness
- **Task Runner** (17 assertions): extractResponse/extractSessionId/needsContinuation, task CRUD, dead-letter
- **File Watcher** (3 assertions): event detection, timeout, stopAll
- **JSON Migration** (8 assertions): import from JSON, .json.bak creation, original deletion

If a test fails, read the assertion name — it tells you exactly what broke.

### 2d. Import/Export Consistency Check

Verify no broken imports by checking the module graph:

```bash
cd $HARNESS_ROOT/bridges/discord
# Check that all .ts files can be parsed as modules
for f in *.ts; do
  echo -n "$f: "
  node -e "import('./$f')" 2>&1 | head -1 || echo "OK"
done
```

## Step 3: Generate Manual Test Checklist

Based on the changed files, generate a checklist. Only include items relevant to the change.

### Core Bot (bot.ts changes)

- [ ] **Bot starts**: `npx tsx bot.ts` — look for `[DB] Database ready`, `AI Harness bot online`
- [ ] **Basic message**: Send any text → bot replies with Claude response
- [ ] **Session continuity**: Send follow-up → response references prior context
- [ ] **`/stop`**: Send message, immediately `/stop` → "Stopped the active request"
- [ ] **`/new`**: Clear session → "Session cleared"
- [ ] **`/status`**: Shows session ID or "No active session"
- [ ] **`/config`**: Shows agent/model/session info
- [ ] **`/help`**: Lists all commands including `/dead-letter`, `/retry`, `/db-status`
- [ ] **Queue behavior**: Send messages in 2 channels simultaneously → both process (not serialized)
- [ ] **Capacity limit**: Exceed MAX_CONCURRENT → queued messages get hourglass reaction

### Agent System (agent/*.md or channel-config-store.ts changes)

- [ ] **`/agents`**: Lists all agent personalities
- [ ] **`/agent researcher`**: Sets agent → `/config` confirms
- [ ] **`/agent clear`**: Removes agent override
- [ ] **Agent personality**: Send message with agent set → response reflects agent's style
- [ ] **`/agent create test "A test agent"`**: Creates agent file, verify [CONTINUE] section included

### Subagents (subagent-manager.ts or process-registry.ts changes)

- [ ] **`/spawn do something simple`**: Spawns subagent → notification on completion
- [ ] **`/tasks`**: Shows running subagent
- [ ] **`/cancel <id>`**: Cancels running subagent
- [ ] **Completion**: Wait for subagent to finish → result posted in channel + activity stream

### Projects (project-manager.ts or handoff-router.ts changes)

- [ ] **`/project create testproj "description"`**: Creates `#proj-testproj` under Projects category
- [ ] **`/project list`**: Shows project
- [ ] **`/project agents researcher,builder`**: Updates project agents
- [ ] **`/project adopt`**: Registers current channel as project
- [ ] **Auto-adopt**: Send message in unregistered channel under Projects category → auto-registered
- [ ] **Agent addressing**: `builder: do X` → routes to builder agent
- [ ] **Handoff**: Agent output with `[HANDOFF:reviewer]` → reviewer agent responds
- [ ] **Handoff depth limit**: Chain of 5+ handoffs → "Handoff limit reached" message
- [ ] **`/project close`**: Archives channel

### Task Runner (task-runner.ts changes)

- [ ] **Retry on failure**: Force a failure (e.g., invalid session) → auto-retries (check logs)
- [ ] **Dead-letter**: Force 3 failures → task moves to dead_letter, notification in channel
- [ ] **`/dead-letter`**: Shows failed tasks
- [ ] **`/retry <id>`**: Re-enqueues task → runs successfully
- [ ] **Crash recovery**: Kill bot mid-task, restart → "Recovered N crashed tasks" in logs
- [ ] **[CONTINUE] marker**: Send complex task → multi-step execution (check logs for "needs continuation")

### Database (db.ts changes)

- [ ] **`/db-status`**: Shows table counts and file size
- [ ] **First-run migration**: Delete `harness.db`, ensure JSON files exist, start bot → "[DB] Migrated..." logs
- [ ] **Backup files**: After migration, `.json.bak` files exist

### Streaming (stream-poller.ts changes)

- [ ] **Live updates**: Send message → streaming message appears and updates progressively
- [ ] **Tool indicators**: Agent uses tools → "*Reading file...*" or "*Searching...*" appears

### Activity Stream (activity-stream.ts changes)

- [ ] **Agent start**: Message sent → embed in #agent-stream
- [ ] **Agent complete**: Response received → embed updated with result
- [ ] **Agent error**: Force error → error embed posted

## Step 4: Regression Checks

Always verify these known-fragile areas regardless of what changed:

1. **`--` separator**: All Claude invocations must have `--` before the prompt arg (check bot.ts, subagent-manager.ts, handoff-router.ts, task-runner.ts)
2. **Env var stripping**: `claude-runner.py` must NOT pass CLAUDE* env vars
3. **PID file guard**: Can't start two bot instances simultaneously
4. **Global disallowed tools**: All invocation paths include the safety guardrails
5. **Session compound keys**: Project channels use `channelId:agentName` format
6. **JSON array fields**: `allowedTools`/`disallowedTools` survive SQLite round-trip (JSON.stringify → JSON.parse)

## Step 5: Report Results

After testing, summarize:

```
## Test Results

### Automated
- TypeScript: PASS/FAIL
- Native module: PASS/FAIL
- Integration suite: X/Y passed

### Manual (if applicable)
- [x] Items verified
- [ ] Items skipped (reason)

### Issues Found
- Description of any failures and their likely cause

### Regression
- All 6 regression checks: PASS/FAIL
```

## When to Run

- **After any code change**: Steps 2a + 2c minimum
- **After dependency changes**: Steps 2a + 2b + 2c
- **Before commits**: Full Steps 2-4
- **After major refactors**: Full Steps 2-5 including manual Discord testing
