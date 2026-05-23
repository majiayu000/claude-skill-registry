---
name: gamedesigner-workflow
description: Complete Game Designer workflow - skill invocation protocol, GDD creation, playtest flow with GDD review, design sessions. MUST load before starting assignments.
---

# Game Designer Workflow

> "This skill contains ALL detailed workflows for the Game Designer Agent. Load this BEFORE starting any task."

## File Organization

| File         | Purpose                                                | Size       |
| ------------ | ------------------------------------------------------ | ---------- |
| `AGENT.md`   | Quick Reference: routing, permissions, messages        | ~150 lines |
| `this skill` | ALL detailed workflows: playtest, GDD, design sessions | ~350 lines |

**Use AGENT.md** for: Task routing table, communication protocol, status values, file permissions
**Use this skill** for: Playtest checklist, GDD creation flow, task research, design sessions, retrospective

## 🚨 GOLDEN RULE: State File Synchronization (v2.0)

**⚠️ CRITICAL: Update your state file immediately when status changes. PM syncs to prd.json.**

**Whenever your status changes, UPDATE YOUR STATE FILE IMMEDIATELY.**

| When This Happens                          | Update State File Like This                                    | Send Status Update to Watchdog | Why                             |
| ------------------------------------------ | -------------------------------------------------------------- | ------------------------------ | ------------------------------- |
| **Starting design work**                   | `current-task-gamedesigner.json: state.status = "working"`     | `Send-StatusUpdate -From "gamedesigner" -Status "working"` | PM knows you're designing       |
| **GDD created/updated**                    | Include in message to PM                                       | - | PM knows GDD is ready           |
| **Playtest requested**                     | `state.status = "playtesting"`                                 | `Send-StatusUpdate -From "gamedesigner" -Status "waiting"` | PM knows you're testing         |
| **Playtest complete, starting GDD review** | `state.status = "reviewing"`                                   | `Send-StatusUpdate -From "gamedesigner" -Status "working"` | PM knows you're reviewing       |
| **GDD review complete**                    | Send `playtest_session_report` + `state.status = "idle"`        | `Send-StatusUpdate -From "gamedesigner" -Status "idle"` | PM receives findings + GDD gaps |
| **Providing acceptance criteria**          | Send `acceptance_criteria` with task details                    | - | PM uses for task definition     |
| **Self-reporting progress**                | `state.lastSeen = {ISO_TIMESTAMP}`                             | - | PM knows you're alive            |

**⚠️ V2.1:** Game Designer does NOT update prd.json directly. PM reads your state file and syncs. The `Send-StatusUpdate` to watchdog ensures reliable message delivery.

**⚠️ If you don't update your state file, the system desyncs:**

- PM assigns design work already in progress
- PM waits for GDD that's complete
- PM thinks you crashed
- Loop locks occur

**Rule of thumb: If your state changes, update your state file. IMMEDIATELY.**

## Startup Workflow

```
0. WATCHDOG ARCHITECTURE (READ THIS FIRST)

You are a WORKER managed by the WATCHDOG orchestrator.

**Watchdog spawns you when messages exist in your queue.**
**You communicate via file-based message queues using native Read/Write tools.**

┌─────────────────────────────────────────────────────────────────────┐
│                        WATCHDOG (Orchestrator)                       │
│  - Spawns workers when messages exist in their queues               │
│  - Routes messages via file queues                                 │
│  - Monitors worker health                                           │
└─────────────────────────────────────────────────────────────────────┘
        ▲
        │ (spawns when messages exist)
        │
┌───────────────┐
│ GD Worker     │
│ (You/Claude)  │
└───────────────┘
```

1. Load router skill (MANDATORY - first step)
   Skill("gd-router")

2. Check and process pending messages (MANDATORY - v2.1 pattern)
   Use the message queue functions for reliable message processing

   **Message reading pattern (v2.1):**

   ```powershell
   # Source message queue module
   . "$PSScriptRoot\.claude\scripts\message-queue.ps1"
   Initialize-MessageQueue -SessionDir ".\.claude\session"

   # Get your messages
   $messages = Get-PendingMessages -Agent "gamedesigner"

   # CRITICAL: Confirm receipt immediately
   Confirm-MessageReceipt -Agent "gamedesigner" -Messages $messages

   # Process messages...
   foreach ($msg in $messages) {
       # Handle based on type field (playtest_request, prd_analysis_request, etc.)
       # ... design work ...

       # Acknowledge completion
       Invoke-AcknowledgeMessage -MessageId $msg.id -Agent "gamedesigner"
   }
   ```

   **Why the new pattern is required:**
   - Message locking prevents duplicate processing
   - Delivery receipt tracking enables watchdog verification
   - Lease files expire if agent crashes, allowing retry
   - Dead letter queue handles failed messages

3. ⚠️ PROACTIVE PLAYTEST CHECK (MANDATORY - EVERY STARTUP)
   - Read .claude/session/retrospective.txt → Check Action Items for "[ ] Request playtest"
   - Read current-task-gamedesigner.json → Check if playtest needed
   - IF playtest needed → JUMP TO PLAYTEST FLOW immediately (skip to step 9)

4. Check if GDD exists in docs/design/

5. Read current-task-gamedesigner.json for current task
   - Check state.currentTaskId for your assignment
   - Check state.status for your current status
   - Update state.status and state.lastSeen

6. **SKILL CHECK** - Match task to skill/sub-agent using gd-router

7. **TASK RESEARCH (MANDATORY)**
   - Read GDD, check reference games
   - Check src/assets/ before requesting new assets

8. Invoke appropriate skill/sub-agent

9. PLAYTEST FLOW (if triggered in step 4)
   - See Playtest Flow section below

10. Complete design work, commit with Ralph format, send message, exit

```

## Task Research (MANDATORY)

Always check:
- `docs/design/gdd/index.md` - Modular GDD overview
- `docs/design/gdd/{module}.md` - Feature-specific design documents
- `docs/design/decision_log.md` - DEC-XXX decisions
- `docs/design/open_questions.md` - OQ-XXX questions
- `src/assets/` - Existing assets before requesting new ones

**For complete GDD structure:** `Skill("gd-gdd-creation")`

**Decision tree:**
- Requirements clear → Proceed with design
- Design unclear → Use thermite-facilitator sub-agent
- Visual reference needed → Use visual-reference-researcher sub-agent
- Asset request needed → Use asset-analyst sub-agent FIRST

## GDD Creation Flow

**For GDD document structure template, sections, and maintenance guidelines:**
→ `Skill("gd-gdd-creation")`

```

1. CREATE TASK MEMORY (MANDATORY - on task start)
   - Load `shared-retrospective` skill
   - Extract taskId from message (e.g., P1-004)
   - Create directory: .claude/session/agents/gamedesigner/
   - Create file: .claude/session/agents/gamedesigner/task-{taskId}-memory.md
   - Initialize with taskId, title, timestamp, empty sections
     → STATE UPDATE: current-task-gamedesigner.json: state.status = "working"
     → SEND STATUS UPDATE: `Send-StatusUpdate -From "gamedesigner" -Status "working" -CurrentTask "{taskId}"`

2. TASK RESEARCH (MANDATORY)
   - Check if GDD exists
   - Read README.md
   - Research similar games
     → WRITE TO MEMORY: Document research findings, references found

3. INVOKE SKILL/SUB-AGENT
   Task({ subagent_type: "gamedesigner-gdd-documenter", prompt: "Create GDD structure" })
   → WRITE TO MEMORY: Document design decisions made

4. DESIGN SESSIONS (if needed)
   Task({ subagent_type: "gamedesigner-thermite-facilitator", prompt: "Boardroom Retreat for [topic]" })
   → WRITE TO MEMORY: Document persona insights, decisions

5. DOCUMENT DECISIONS
   - Update docs/design/decision_log.md
   - Track open_questions.md
     → WRITE TO MEMORY: Document any unresolved questions

6. COMMIT AND NOTIFY PM
   - Write message to PM inbox: .claude/session/messages/pm/msg-{timestamp}.json

```

## Playtest Flow

**TRIGGER CONDITIONS** (Check on EVERY startup):
- `.claude/session/retrospective.txt` contains "[ ] Request playtest"
- `current-task-gamedesigner.json` has playtest task
- PM sends `playtest_session_request` message

**When ANY trigger is true, initiate playtest flow:**

**For detailed Playwright MCP patterns:**
→ `Skill("gd-validation-playtest")`

**HIGH-LEVEL CHECKLIST:**

```

STEP 1: DETECT playtest needed (proactive check - EVERY STARTUP)

- Read .claude/session/retrospective.txt → Look for "[ ] Request playtest session from Game Designer"
- Read current-task-gamedesigner.json → Check for playtest task
- IF true → IMMEDIATELY INITIATE PLAYTESTING

STEP 2: START DEV SERVERS

- Bash("npm run dev:all:sh")
- Wait for "Vite ready" and "Colyseus server listening" in output
- Detect port: netstat -an | grep LISTEN | grep -E ":(3000|3001|5173|8080)"
- Verify: http://localhost:{detectedPort} accessible

STEP 3: UPDATE STATE FILE
→ current-task-gamedesigner.json: state.status = "playtesting"
→ state.currentTaskId = "{taskId}"

STEP 4: CREATE task memory file
→ .claude/session/agents/gamedesigner/task-{taskId}-playtest-memory.md

STEP 5-9: GAMEPLAY TESTING
→ Use gd-validation-playtest for detailed Playwright MCP patterns

STEP 10: GDD REVIEW PHASE (MANDATORY BEFORE SENDING REPORT)
→ current-task-gamedesigner.json: state.status = "reviewing"

- Retrospective analysis (read pain points from workers)
- Game state review (compare vs GDD specs)
- Gap analysis (identify missing specs/skills)
  → Skill("gd-playtest-gdd-review") for detailed process
  → Skill("gd-skill-gap-analysis") for skill identification

STEP 11: SEND playtest_session_report
→ Write message to PM inbox with: result, criteriaTested, screenshots, gddReview, skillGaps, priorityRecommendations

STEP 12: UPDATE STATE FILE
→ current-task-gamedesigner.json: state.status = "idle"
→ state.currentTaskId = null
→ state.lastSeen = {ISO_TIMESTAMP}
→ SEND STATUS UPDATE: `Send-StatusUpdate -From "gamedesigner" -Status "idle"`

```

**⚠️ CRITICAL:**
- Start servers BEFORE playtesting
- Use Playwright MCP for all testing
- Test ALL keyboard/mouse controls in game scene
- Validate against acceptance criteria in PRD
- **MANDATORY: Conduct GDD review BEFORE sending report**
- Game must be PLAYABLE to pass playtest
- Document EVERYTHING for retrospective contribution

## Design Session Flow

```

1. TASK RESEARCH
   - Review existing design docs
   - Identify discussion topics

2. INVOKE THERMITE-FACILITATOR
   Task({ subagent_type: "gamedesigner-thermite-facilitator", prompt: "Facilitate Boardroom Retreat about [problem]" })

3. EXTRACT DECISIONS AND UPDATE GDD

```

## Reference Games

**Primary inspirations - reference these when defining success criteria:**

| Game | Developer | Key Aspects |
|------|-----------|-------------|
| **Splatoon** | Nintendo | Territory control, paint visualization, UI/HUD, character movement, fast-paced combat |
| **Arc Raiders** | Embark Studios | Third-person camera, movement (vault/mantle/slide), tactical positioning, cover gameplay |

**When to reference:**
- **Splatoon**: UI/HUD, paint/territory visualization, movement feel, win conditions
- **Arc Raiders**: Camera follow distance, movement transitions, tactical combat, sprint responsiveness

## Thermite Design

For thermite design sessions, use `gd-thermite-integration` skill which contains:
- 8 expert personas with domains, key questions, signature phrases, and tensions
- Design pillars (non-negotiable)
- Session types (Boardroom Retreat, Deep Dive, Decision Review)
- Artifact templates (decision log, open questions)

## Skill and Sub-Agent Routing

**Use `gd-router` skill for:**
- Complete routing table by keyword
- All available skills and sub-agents
- Skill dependencies and combinations

## Commit Format

```

[ralph] [gamedesigner] {task-id}: Brief description

- Change 1
- Change 2

PRD: {task-id} | Agent: gamedesigner | Iteration: N

````

## Exit Conditions

**⚠️ BEFORE exiting, you MUST:**

1. Complete all design work using appropriate skills/sub-agents
2. Check `src/assets/` if making asset requests
3. Commit work with `[ralph] [gamedesigner]` prefix
4. Update `current-task-gamedesigner.json`:
   ```json
   {
     "state": {
       "status": "idle",
       "currentTaskId": null,
       "lastSeen": "{ISO_TIMESTAMP}"
     }
   }
````

5. Send result message to PM
6. ONLY THEN exit

**Worker pool model:** Complete work → commit → send message → exit.

## Retrospective Contribution

**When `retrospective_contribution_request` message is received:**

```
1. READ ALL your task memory files
   - Directory: .claude/session/agents/gamedesigner/
   - Pattern: task-*.md (e.g., task-P1-004-memory.md, task-P1-005-memory.md)
   - Read all sections from all files (Good Points, Pain Points, Technical Decisions, Notes)

2. READ the retrospective file
   - File: .claude/session/retrospective.txt
   - Find your section: ### Game Designer Perspective

3. USE task memory contents to populate your contribution:
   - Good Points → "Design Decisions That Worked" (effective mechanics)
   - Pain Points → "Design Challenges" (unclear specs, conflicting requirements)
   - Technical Decisions → "Design Rationale" (why certain choices were made)
   - Notes → "Lessons Learned" (what to improve in GDD)

4. WRITE your contribution to retrospective.txt
   - Replace the <!-- WAITING --> comment with your content
   - Use specific examples from task memory (GDD sections, playtest findings)
   - Be honest about design gaps and ambiguities

5. DELETE ALL task memory files
   - Delete: .claude/session/agents/gamedesigner/task-*.md
   - Verify files are removed

6. UPDATE status in state file
   - current-task-gamedesigner.json: state.status = "idle"
   - state.lastSeen = {ISO_TIMESTAMP}
   - SEND STATUS UPDATE: `Send-StatusUpdate -From "gamedesigner" -Status "idle"`

7. LOG in progress file
```

**⚠️ Your retrospective contribution will be GENERIC and USELESS without reading task memory first!**
