---
name: shared-retrospective
description: Task memory management and retrospective contributions for Ralph agents
category: orchestration
---

# Shared Retrospective

> "Remember what happened during the task — write to task memory, use it for retrospectives."

---

## Overview

Task Memory is a temporary file that records your experiences during task execution. When retrospective is triggered, you read ALL your task memory files to populate your contribution, then delete them.

**Problem solved:** Agents lose context between sessions and have nothing specific to contribute to retrospectives.

**Multiple tasks:** Each task gets its own memory file, so agents can work on N tasks simultaneously without mixing memories.

---

## Task Memory File Format

**Location:** `.claude/session/agents/{agent}/task-{taskId}-memory.md`

Where `{agent}` is one of: `developer`, `techartist`, `qa`, `gamedesigner`

### Template

```markdown
# Task Memory: {taskId} - {title}

**Started**: {timestamp}
**Agent**: {agent}

## Good Points

_To be filled during task execution_

## Pain Points

_To be filled during task execution_

## Technical Decisions

_To be filled during task execution_

## Notes

_To be filled during task execution_
```

---

## Task Memory Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│  1. TASK START                                                  │
│     - Receive task_assign or asset_assign message              │
│     - CREATE task-{taskId}-memory.md                           │
│     - Initialize with task ID, title, timestamp, empty sections│
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. DURING TASK EXECUTION                                      │
│     - When something notable happens, APPEND to task memory   │
│     - Good points: solutions that worked well                  │
│     - Pain points: blockers, difficulties, unclear docs        │
│     - Technical decisions: architectural choices, workarounds   │
│     - Notes: context for future reference                      │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. RETROSPECTIVE TRIGGERED                                     │
│     - Receive retrospective_initiate message                    │
│     - READ ALL task-*.md files from agents/{agent}/            │
│     - Use contents to populate retrospective contribution       │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. AFTER CONTRIBUTION                                          │
│     - DELETE ALL task-*.md files from agents/{agent}/          │
│     - Verify files are removed                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Creating Task Memory

**When:** Immediately after receiving `task_assign` or `asset_assign` message.

**Steps:**

1. **Extract taskId** from message payload (e.g., `P1-004`, `vis-002`)

2. **Create directory** (if not exists): `.claude/session/agents/{agent}/`

3. **Create file:** `.claude/session/agents/{agent}/task-{taskId}-memory.md`

4. **Initialize** with template (see above)

---

## Writing to Task Memory

**When:** During task execution, when something notable happens.

### What to Write

**Good Points** — Write when:

- A solution works particularly well
- A pattern proves effective
- Something exceeds expectations
- A skill or library saves time

**Pain Points** — Write when:

- Encountering a blocker or difficulty
- Documentation is unclear or missing
- A pattern causes issues
- Something takes longer than expected
- You implement a workaround

**Technical Decisions** — Write when:

- Making an architectural choice
- Choosing between alternatives
- Implementing a workaround
- Deciding not to follow PRD exactly (and why)

**Notes** — Write when:

- Remembering something for later
- Noting context for future reference
- Recording a question for PM

### How to Append

Read the current file, then append to the appropriate section:

```markdown
## Good Points

_Initial content_

- Used React Three Fiber's InstancedMesh for performance – rendered 1000+ objects at 60fps
- TypeScript strict mode caught a potential null reference early

## Pain Points

_Initial content_

- Rapier documentation unclear on collision event handling – had to inspect source code
- Initial approach used individual meshes – performance was terrible at 15fps

## Technical Decisions

_Initial content_

- Chose InstancedMesh over individual meshes for performance (1000+ objects)
- Decided to use Rapier's collision events instead of manual distance checks
```

---

## Agent-Specific Examples

### Developer Tracks

- Code patterns that worked well
- TypeScript challenges faced
- Build issues and resolutions
- Architectural decisions made
- Library integration difficulties

### Tech Artist Tracks

- Visual techniques that were effective
- Shader compilation issues
- Performance optimizations (draw calls, triangle count)
- Asset integration challenges
- Material/texture decisions

### QA Tracks

- Code quality observations
- Validation difficulties (false positives, missing tests)
- Test coverage gaps
- Browser testing issues
- Unclear acceptance criteria

### Game Designer Tracks

- Design decisions made
- GDD clarity issues
- Playtest findings
- Mechanics that need refinement
- Balancing adjustments

---

## Retrospective Detection

**When:** You receive `retrospective_initiate` message from PM.

**Steps:**

1. **Find ALL task memory files:**

   ```
   Directory: .claude/session/agents/{agent}/
   Pattern: task-*.md
   ```

2. **Read each task memory file**
   - Example: `task-P1-004-memory.md`
   - Example: `task-vis-001-memory.md`

3. **Combine all contents** into your retrospective

---

## Retrospective Contribution Format

**File:** `.claude/session/retrospective-{agent}.json`

```json
{
  "agent": "{agent}",
  "taskId": "{taskId}",
  "timestamp": "{ISO-8601-UTC}",
  "contributions": {
    "whatWorkedWell": ["Solution 1 that worked well", "Solution 2 that worked well"],
    "technicalChallenges": ["Challenge 1 faced", "Challenge 2 faced"],
    "implementationDecisions": ["Decision 1 with reasoning", "Decision 2 with reasoning"],
    "areasForImprovement": ["Area 1 that could be better", "Area 2 that could be better"],
    "lessonsLearned": ["Lesson 1 for future tasks", "Lesson 2 for future tasks"]
  }
}
```

### Mapping Task Memory to Contribution

| Task Memory Section | Contribution Section                      |
| ------------------- | ----------------------------------------- |
| Good Points         | whatWorkedWell                            |
| Pain Points         | technicalChallenges / areasForImprovement |
| Technical Decisions | implementationDecisions                   |
| Notes               | lessonsLearned                            |

---

## Complete Example

### Developer Task Memory

**File:** `.claude/session/agents/developer/task-P1-005-memory.md`

```markdown
# Task Memory: P1-005 - Multiplayer Room State Synchronization

**Started**: 2026-01-26T14:15:00Z
**Agent**: developer

## Good Points

- Colyseus's `Schema` serialization worked perfectly for state sync
- Used @colyseus/schema `ArraySchema` for player list – type-safe and efficient
- Client-side prediction reduced perceived lag significantly

## Pain Points

- Colyseus documentation on `onChange` callbacks was unclear – had to test multiple approaches
- Initial state structure caused 500kb payloads – had to refactor to use `Schema`
- TypeScript types for Colyseus state weren't exported – had to create custom types

## Technical Decisions

- Chose Colyseus `Schema` over raw JSON for bandwidth (80% reduction)
- Implemented client-side prediction for movement despite added complexity
- Decided NOT to sync animation state to server (client-authoritative for cosmetics)

## Notes

- Need to ask PM about weapon fire synchronization – current approach feels laggy
- GDD doesn't specify if physics should be server-authoritative
```

### Resulting Contribution

```json
{
  "agent": "developer",
  "taskId": "P1-005",
  "timestamp": "2026-01-26T15:45:00.000Z",
  "contributions": {
    "whatWorkedWell": [
      "Colyseus Schema serialization worked perfectly once implemented",
      "Client-side prediction significantly reduced perceived lag",
      "Type-safe player list with ArraySchema"
    ],
    "technicalChallenges": [
      "Colyseus documentation on onChange callbacks unclear – had to experiment",
      "Initial state design caused 500kb payloads – required major refactor to Schema",
      "TypeScript types not exported from Colyseus – created custom type definitions"
    ],
    "implementationDecisions": [
      "Used Colyseus Schema serialization instead of raw JSON (80% bandwidth reduction)",
      "Chose ArraySchema for player list to maintain type safety",
      "Implemented client-side prediction for movement despite added complexity",
      "Kept animation state client-authoritative (cosmetics only)"
    ],
    "areasForImprovement": [
      "GDD should specify server-authoritative requirements for physics",
      "Weapon fire synchronization approach needs review – feels laggy",
      "Should prototype state payload size before committing to approach"
    ],
    "lessonsLearned": [
      "Always prototype state payload size before committing to approach",
      "Client-side prediction worth the complexity for fast-paced games",
      "Need clearer specification on what must be server-authoritative"
    ]
  }
}
```

---

## Deleting Task Memory

**When:** Immediately after writing retrospective contribution.

**Steps:**

1. **Find ALL task memory files:**

   ```
   Directory: .claude/session/agents/{agent}/
   Pattern: task-*.md
   ```

2. **Delete ALL task memory files:**
   - Delete: `task-P1-004-memory.md`
   - Delete: `task-P1-005-memory.md`
   - Delete any matching `task-*.md` files

3. **Verify** files are removed

4. **Continue** with workflow (update status, log, exit)

---

## Important Rules

✅ **DO:**

- Create task memory IMMEDIATELY when starting a task
- Append to memory throughout execution (not just at end)
- Track which task's memory file you're writing to
- Be specific — mention file names, error messages, exact issues
- Write to memory as soon as something happens (don't wait)
- Read ALL task memory files before writing retrospective contribution
- Delete ALL task memory files after contribution is complete

❌ **DON'T:**

- Skip creating task memory
- Write to memory only at end (you'll forget details)
- Be vague or generic
- Mix up which task's memory file you're writing to
- Forget to delete memory after retrospective
- Edit another agent's task memory file
- Create task memory in wrong location

---

## Verification Checklist

**Before starting a task:**

- [ ] Task memory file created at correct path
- [ ] File name includes task ID
- [ ] File initialized with task ID, title, timestamp
- [ ] Empty sections ready for appending

**During task execution:**

- [ ] Writing to memory when notable events happen
- [ ] Being specific with file names, error messages
- [ ] Appending to correct section
- [ ] Writing to correct task's memory file

**When retrospective triggered:**

- [ ] Finding ALL task memory files
- [ ] Reading all task memory files
- [ ] Using contents to populate contribution
- [ ] Deleting ALL task memory files after contribution

---

## References

- `pm-workflow` — PM retrospective orchestration
- `shared-core` — Session structure, status values
- `shared-messaging` — Message protocol for retrospective_initiate
