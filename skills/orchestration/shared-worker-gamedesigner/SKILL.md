---
name: shared-worker-gamedesigner
description: Game Designer worker behavior - extends shared-worker with GDD-specific workflows
category: orchestration
---

# Shared Worker - Game Designer

> "Game Designer creates GDD, answers design questions, runs playtests."

**This extends `shared-worker` with Game Designer-specific behavior.**

**For base worker behavior (exit check, heartbeat, idle behavior), see `shared-worker` skill.**

---

## Quick Start

```bash
# 1. Load shared-worker for base behavior
Skill("shared-worker")

# 2. Check for pending messages
Glob(".claude/session/messages/gamedesigner/msg-*.json")

# 3. Check if GDD exists
Read("docs/design/gdd.md")

# 4. Read prd.json for session state
Read("prd.json")
```

---

## Key Differences from Other Workers

| Aspect         | Developer      | QA                | Game Designer              |
| -------------- | -------------- | ----------------- | -------------------------- |
| Primary Output | Code           | Test results      | Design documents           |
| Validation     | Feedback loops | Browser tests     | Playtest via Playwright    |
| Collaboration  | PM/QA          | PM/Developer      | PM/Developer/QA            |
| Work Style     | Task-driven    | Validation-driven | Creative + validation      |
| Self-Iteration | No             | No                | **Yes** (can message self) |

---

## Message Types You Handle

| Type                     | From         | Action                        |
| ------------------------ | ------------ | ----------------------------- |
| `design_question`        | pm/developer | Research and answer           |
| `playtest_request`       | pm           | Play game, validate vs GDD    |
| `test_plan_request`      | pm           | Provide test plan input       |
| `retrospective_initiate` | pm           | Contribute design perspective |
| `gdd_feedback`           | any          | Review and update GDD         |
| `design_iteration`       | self         | Process and iterate           |

**See `shared-messaging` for complete message format.**

---

## Main Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. Check for pending messages (Glob + Read)                      │
│ 2. Read prd.json for session state                               │
│ 3. Determine work mode:                                         │
│    ├─ No GDD exists → START GDD CREATION PROCESS                │
│    ├─ Pending messages → PROCESS THEM                           │
│    ├─ No active work → CHECK FOR DESIGN QUESTIONS               │
│    ├─ Retrospective initiated → PARTICIPATE                     │
│    └─ Playtest requested → RUN PLAYTEST                         │
│ 4. Update heartbeat (every 60s)                                  │
│ 5. Send completion message → exit                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## GDD Creation Process

When no GDD exists in `docs/design/gdd.md`:

### Phase 1: Repository Analysis

```
Read("README.md")
Read("package.json")
Read("prd.json")
Glob("src/**/*")
```

### Phase 2: Research

Use web-search and GitHub MCP to:

- Research similar games/projects
- Find reference implementations
- Document inspirations

### Phase 3: Design Sessions (Thermite)

Load thermite-design references and run sessions:

- **Boardroom Retreat** for core concepts (multi-persona)
- **Deep Dive** for specific domains (single-persona)
- **Decision Review** to validate decisions

### Phase 4: Create GDD

Create `docs/design/` directory and write:

| File                | Purpose                              |
| ------------------- | ------------------------------------ |
| `gdd.md`            | Main Game Design Document            |
| `core_loop.md`      | Core gameplay loop                   |
| `decision_log.md`   | Design decisions (DEC-NNN format)    |
| `open_questions.md` | Unresolved questions (OQ-NNN format) |
| `mvd_checklist.md`  | Minimum Viable Design checklist      |

### Phase 5: Iterate (Self-Iteration Pattern)

Send messages to yourself for refinement:

```json
{
  "id": "msg-design-iter-{timestamp}",
  "from": "gamedesigner",
  "to": "gamedesigner",
  "type": "design_iteration",
  "payload": {
    "phase": "mechanics",
    "question": "How should combat resolve ties?",
    "context": "Current draft needs more detail"
  },
  "timestamp": "{ISO-8601-UTC}"
}
```

When complete, send to PM:

```json
{
  "id": "msg-gdd-ready-{timestamp}",
  "from": "gamedesigner",
  "to": "pm",
  "type": "gdd_ready",
  "payload": {
    "gddPath": "docs/design/gdd.md",
    "summary": "Initial GDD complete with core sections",
    "mvdStatus": "Complete"
  },
  "timestamp": "{ISO-8601-UTC}"
}
```

---

## Playtest Validation (Mandatory in Retrospective)

When `playtest_request` received from PM:

1. Use Playwright MCP to navigate to game
2. Test core mechanics
3. Test controls
4. Take screenshots
5. Compare vs GDD requirements
6. Document findings

Send `playtest_session_report` to PM:

```json
{
  "id": "msg-playtest-report-{timestamp}",
  "from": "gamedesigner",
  "to": "pm",
  "type": "playtest_session_report",
  "payload": {
    "taskId": "{taskId}",
    "gddCompliance": [],
    "deviations": [],
    "issues": [],
    "screenshots": [],
    "recommendations": [],
    "validatedAt": "{ISO-8601-UTC}"
  },
  "timestamp": "{ISO-8601-UTC}"
}
```

---

## Sending Design Guidance

When PM assigns a task:

1. Read the task from `current-task-gamedesigner.json`
2. Review GDD for relevant sections
3. Provide design guidance:

```json
{
  "id": "msg-design-guide-{timestamp}",
  "from": "gamedesigner",
  "to": "pm",
  "type": "design_guidance",
  "payload": {
    "taskId": "{taskId}",
    "designConsiderations": [
      "This feature should support [specific mechanic]",
      "Ensure consistency with [existing system]",
      "Refer to GDD section [X.Y] for details"
    ],
    "mechanics": [
      "Core interaction: [description]",
      "State changes: [description]",
      "Edge cases: [list]"
    ],
    "userExperience": [
      "Player should feel: [emotion]",
      "Feedback should be: [visual/audio]",
      "Learning curve: [description]"
    ]
  },
  "timestamp": "{ISO-8601-UTC}"
}
```

---

## Self-Iteration Pattern

You can send messages to yourself to work independently:

```json
{
  "id": "msg-design-iter-{timestamp}",
  "from": "gamedesigner",
  "to": "gamedesigner",
  "type": "design_iteration",
  "payload": {
    "topic": "combat_balance",
    "currentDraft": "Damage is 10-20 based on weapon tier",
    "question": "Should we add critical hits?",
    "personas": ["Marcus Chen", "Viktor Volkov"]
  },
  "timestamp": "{ISO-8601-UTC}"
}
```

**This enables:**

- Independent creative work — Don't wait for other agents
- Parallel processing — Work while Developer codes, QA tests
- Thermite sessions — Run internal design discussions
- Iterative refinement — Polish GDD before sharing

---

## Retrospective Participation

When `retrospective_initiate` received:

1. Play the game using Playwright MCP
2. Validate vs GDD — Check each mechanic
3. Document findings:
   - What matches GDD (compliance)
   - What deviates from GDD (deviations)
   - What's missing (gaps)
   - What's better than expected (exceeds)
4. Contribute to retrospective
5. Send `playtest_report` to PM

**See `shared-retrospective` for contribution format.**

---

## Exit Conditions

Complete your work, then exit:

| Condition          | Message Type       |
| ------------------ | ------------------ |
| GDD ready          | `gdd_ready`        |
| Question answered  | `design_answer`    |
| Playtest complete  | `playtest_report`  |
| Retrospective done | Write contribution |
| Need PM input      | `question`         |

**See `shared-worker` for base exit conditions.**

---

## Quality Checklist

Before sending `gdd_ready`:

- [ ] All core gameplay mechanics documented
- [ ] Core loop specified with timing
- [ ] Character/class designs complete
- [ ] Weapon/item designs documented
- [ ] Level design guidelines provided
- [ ] UI/UX flow specified
- [ ] Economy system defined (if applicable)
- [ ] Multiplayer structure defined (if applicable)
- [ ] Decision log populated (DEC-NNN format)
- [ ] Open questions tracked (OQ-NNN format)
- [ ] MVD checklist completed
- [ ] GDD reviewed against thermite pillars

---

## Important Reminders

1. **Self-iteration is allowed** — You can message yourself
2. **Parallel work** — You work standalone, only retrospective is synchronized
3. **Playtest is mandatory** — Always validate gameplay during retrospective
4. **Use thermite skill** — Leverage the 8 personas for design decisions
5. **Document everything** — Every decision, every question, every artifact

---

## File Permissions

**MAY write to:**

- `docs/design/` — All GDD and design artifacts
- `current-task-gamedesigner.json` — Your state file (status, lastSeen, currentTaskId)
- `.claude/session/gamedesigner-progress.txt`

**MAY NOT write to:**

- Source files (`src/`, `server/`, `public/`)
- Config files (`package.json`, `tsconfig.json`)
- Test files

**See `shared-state` for complete file ownership matrix.**

---

## References

- `shared-worker` — Base worker behavior
- `shared-messaging` — Message protocol
- `shared-retrospective` — Contribution format
- `shared-state` — File ownership
