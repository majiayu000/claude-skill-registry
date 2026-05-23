---
name: pm-retrospective-facilitation
description: Facilitate file-based retrospective after task completion with worker agents (Developer, Tech Artist, QA). Playtest session is now a separate phase.
category: retrospective
---

# Retrospective Skill

> "Quality over speed – every completed task deserves reflection."

> **IMPORTANT**: Playtest is now a SEPARATE phase. This skill handles worker retrospective contributions ONLY.

**NOTE FOR EVENT-DRIVEN MODE:**
Use native Read/Write tools for all message operations. Messages are stored as JSON files in `.claude/session/messages/`.

## When to Use This Skill

Use when:

- `prd.json.items[{taskId}].status === "passed"` (QA validated)
- Before assigning the next task
- NEVER skip retrospective

## Quick Start

1. Create `.claude/session/retrospective.txt` with template
2. Set `prd.json.items[{taskId}].status = "in_retrospective"`
3. Send `retrospective_initiate` to Developer, Tech Artist, QA (**NOT Game Designer**)
4. **EXIT** - supervisor will restart you when messages arrive
5. On wake-up: If all 3 workers contributed → read separate files → merge → synthesize
6. **Commit changes with git**: `[ralph] [pm] {taskId} retrospective: Worker contributions synthesized`
7. Set status to `retrospective_synthesized`
8. **⚠️ DO NOT EXIT! Continue to Phase 2 (Playtest) using the router table**

**P1 FIX: Workers now write to separate contribution files (prevents race conditions):**

- `.claude/session/retro-contributions-developer-{taskId}.json`
- `.claude/session/retro-contributions-techartist-{taskId}.json`
- `.claude/session/retro-contributions-qa-{taskId}.json`
- PM reads all 3 files and merges them into synthesized retrospective

### Retrospective Contribution Acknowledgment Pattern (v2.1)

**When workers send retrospective_contribution messages:**

1. PM receives `retrospective_contribution` message from worker
2. PM reads contribution file
3. **PM sends `message_acknowledged` to watchdog using `Confirm-MessageReceipt`**
4. PM deletes original message from queue
5. PM continues until all workers contributed or timeout

```powershell
# After reading messages
. "$PSScriptRoot\.claude\scripts\message-queue.ps1"
Initialize-MessageQueue -SessionDir ".\.claude\session"

$messages = Get-PendingMessages -Agent "pm"

# CRITICAL: Confirm receipt immediately
Confirm-MessageReceipt -Agent "pm" -Messages $messages

# Process messages...
foreach ($msg in $messages) {
    if ($msg.type -eq "retrospective_contribution") {
        # ... handle contribution ...
    }
    Invoke-AcknowledgeMessage -MessageId $msg.id -Agent "pm"
}
```

**Contribution message format:**
```json
{
  "id": "msg-pm-{agent}-retro-{timestamp}",
  "from": "{agent}",
  "to": "pm",
  "type": "retrospective_contribution",
  "priority": "low",
  "payload": {
    "taskId": "{taskId}",
    "contributor": "{agent}",
    "contributionFile": ".claude/session/retro-contributions-{agent}-{taskId}.json"
  },
  "timestamp": "{ISO-8601}",
  "status": "pending"
}
```

**Watchdog triggers `retrospective_complete` when:**
- All 3 workers (Developer, Tech Artist, QA) have sent contributions
- OR timeout reached (configurable, default 10 minutes per worker)

**⚠️ CRITICAL: Playtest is a SEPARATE Phase**

After retrospective completes, use the `pm-retrospective-playtest-session` skill to request playtest from Game Designer.

### When to SKIP Playtest (feat-tps-003 precedent, 2026-01-27)

**Playtest is NOT required for:**

- Bug fixes (non-gameplay related)
- Camera/visual adjustments
- Test infrastructure (CI/CD, tooling)
- Backend-only changes without visual impact
- Documentation-only changes

**Playtest IS required for:**

- Gameplay mechanics (movement, shooting, physics)
- Visual features (shaders, materials, effects)
- UI/UX changes (HUD, menus, interactions)
- Character/weapon behavior changes
- Multiplayer features

**Rationale:** Playtesting is time-consuming for the Game Designer and should be focused on features that directly impact gameplay experience. Technical fixes can be validated through code review and automated tests.

### When to EXCUSE Tech Artist from Retrospective (feat-tps-004 precedent, 2026-01-27)

**Tech Artist excusal criteria:**

- Tech Artist is working on TIER_0_BLOCKER task unrelated to current retrospective
- Task has no visual/shader component requiring Tech Artist input
- Task is architectural, backend, or test infrastructure

**When to excuse:**

1. Check `prd.json.agents.techartist.currentTaskId`
2. If Tech Artist working on TIER_0_BLOCKER (e.g., bugfix-shader-001)
3. And current retrospective task is non-visual (e.g., camera value fix)
4. **THEN excusal is appropriate**

**Example from feat-tps-004:**

```
Task: feat-tps-004 (Camera Shoulder Offset Fix)
Tech Artist Status: Working on bugfix-shader-001 (TIER_0_BLOCKER)
Task Type: Camera value fix (non-visual, no shader component)
Decision: EXCUSE Tech Artist from retrospective
```

**When NOT to excuse:**

- Task involves shaders, materials, or visual effects
- Task involves 3D models or animations
- Tech Artist has no blocking tasks
- Tech Artist contributed to implementation

**Retrospective file format with excusal:**
```markdown
### Tech Artist Perspective

**EXCUSED** - Tech Artist is working on bugfix-shader-001 (TIER_0_BLOCKER)
This task has no visual/shader component requiring Tech Artist input.
```

---

## State Flow

```
passed → in_retrospective → retrospective_synthesized → (CONTINUE to Phase 2)
```

**⚠️ CRITICAL: After setting `retrospective_synthesized`, DO NOT EXIT!**

**Continuation steps:**
1. Check if playtest is required (see decision matrix below)
2. If YES: Use `Skill("pm-retrospective-playtest-session")` → `playtest_complete`
3. If NO: Skip to `Skill("pm-organization-prd-reorganization")` → `prd_refinement`

**Next phases** (handled by other skills):

- `retrospective_synthesized` → `playtest_phase` OR `prd_refinement` (decision required)
- `playtest_complete` → `prd_refinement` (via pm-organization-prd-reorganization skill)
- `prd_refinement` → `cleanup_completed` (inline in pm-workflow)
- `cleanup_completed` → `skill_research` (via pm-improvement-skill-research skill)
- `skill_updates_applied` → `task_ready` (via pm-organization-task-selection skill)
- `task_ready` → `test_plan_ready` (via pm-planning-test-planning skill)
- `test_plan_ready` → `assigned` (assign to worker, THEN exit)

## Decision Framework

| Status                        | Action                                                          |
| ----------------------------- | --------------------------------------------------------------- |
| Just passed QA                | Create retrospective.txt, set in_retrospective                  |
| Sent retrospective_initiate   | **EXIT** - supervisor restarts you when messages arrive         |
| On wake-up: incomplete        | Check state, if incomplete → **EXIT again**                     |
| All THREE workers contributed | Synthesize, **commit**, set retrospective_synthesized, **EXIT** |

**Event-driven principle: PM checks state on wake-up and either proceeds or exits. NO polling, NO timers.**

## Progressive Guide

### Level 1: Create Retrospective File

```markdown
# Retrospective: {{TASK_ID}} - {{TASK_TITLE}}

**Started**: {{ISO_TIMESTAMP}}
**Task**: {{TASK_ID}}

## Status: WAITING_FOR_AGENTS

---

## Task Summary

**Title**: {{TASK_TITLE}}
**Category**: {{CATEGORY}}
**Completed At**: {{ISO_TIMESTAMP}}

## Retrospective Sections

### Developer Perspective (to be filled by Developer Agent)

<!-- WAITING for developer to add their points -->

### Tech Artist Perspective (to be filled by Tech Artist Agent)

<!-- WAITING for Tech Artist to add their points -->

### QA Perspective (to be filled by QA Agent)

<!-- WAITING for QA to add their points -->

### PM Synthesis (to be filled by PM Agent)

<!-- WAITING for all THREE worker agents to contribute -->

---

## Completion Status

- [ ] Developer contributed
- [ ] Tech Artist contributed
- [ ] QA contributed
- [ ] PM synthesized and completed

## Action Items

<!-- To be filled by PM after synthesis -->
```

### Level 2: Track Agent Contributions

```javascript
// Check if Developer contributed
const devSection = retrospective.match(/### Developer Perspective\n([\s\S]*?)###/);
const devContributed = devSection && !devSection[1].includes('WAITING');

// Check if Tech Artist contributed
const taSection = retrospective.match(/### Tech Artist Perspective\n([\s\S]*?)###/);
const taContributed = taSection && !taSection[1].includes('WAITING');

// Check if QA contributed
const qaSection = retrospective.match(/### QA Perspective\n([\s\S]*?)###/);
const qaContributed = qaSection && !qaSection[1].includes('WAITING');

// Update checkboxes
if (devContributed) updateCheckbox('Developer contributed', true);
if (taContributed) updateCheckbox('Tech Artist contributed', true);
if (qaContributed) updateCheckbox('QA contributed', true);
```

### Level 2.5: Send Retrospective Messages (Workers Only)

**⚠️ CRITICAL: This phase is for worker contributions ONLY. Game Designer playtest is separate.**

**Use native Read/Write tools for all message operations:**

```json
// Message format for sending to workers
// Write to: .claude/session/messages/{agent}/cmd/{timestamp}.json

{
  "id": "msg-retro-{timestamp}",
  "from": "pm",
  "to": "developer",
  "type": "retrospective_initiate",
  "payload": {
    "taskId": "{taskId}",
    "taskTitle": "{taskTitle}",
    "retrospectiveFile": ".claude/session/retrospective.txt"
  },
  "timestamp": "{ISO-8601-UTC}"
}
```

**Send retrospective_initiate to each worker:**

1. Write to `.claude/session/messages/developer/cmd/{timestamp}.json`
2. Write to `.claude/session/messages/techartist/cmd/{timestamp}.json`
3. Write to `.claude/session/messages/qa/cmd/{timestamp}.json`

```json
// Example: .claude/session/messages/developer/cmd/20250126-120000.json
{
  "id": "msg-retro-20250126-120000",
  "from": "pm",
  "to": "developer",
  "type": "retrospective_initiate",
  "payload": {
    "taskId": "feat-001",
    "taskTitle": "Implement TPS camera controls",
    "retrospectiveFile": ".claude/session/retrospective.txt"
  },
  "timestamp": "2025-01-26T12:00:00.000Z"
}
```

**Check for responses using Read tool:**

```bash
# Use Glob to find messages in your inbox
Glob(".claude/session/messages/pm/msg-*.json")

# Read each message file using Read tool
# Look for type "retrospective_contribution"
```

**Message Flow:**

```
Retrospective Phase:
PM             Developer      TechArtist       QA
 │                 │               │            │
 │──retrospective_initiate──►│               │            │
 │──retrospective_initiate───────────────────►│            │
 │──retrospective_initiate──────────────────────────────►│
 │                                                      │
 │◄─────────────────────────────────────────────────────┤
 │     (All workers contribute via messages)             │
```

**Expected Responses:**

| Agent       | Message Type                 | What They Contribute                           |
| ----------- | ---------------------------- | ---------------------------------------------- |
| Developer   | `retrospective_contribution` | Implementation challenges, technical insights  |
| Tech Artist | `retrospective_contribution` | Visual quality, asset challenges, performance  |
| QA          | `retrospective_contribution` | Validation findings, test coverage, bugs found |

### Level 2.6: Supervisor Message Coordination (CRITICAL - NO LOOPS, NO TIMERS)

**Supervisor monitors message queues and wakes PM when all 3 workers contributed.**

**Event-driven flow (NO loops, NO timers, NO blocking):**

```bash
# After sending retrospective_initiate:
# 1. EXIT immediately - supervisor monitors messages and wakes you when complete
# 2. On wake-up, all workers should have contributed

# When PM wakes up (supervisor signals all complete):
# Use Glob to check for messages in your inbox:
Glob(".claude/session/messages/pm/msg-*.json")

# P1 FIX: Check for retrospective_contribution messages from workers
# Track which workers have contributed via messages (more reliable than file watching)
```

**Key principles:**

- **NO loops** - no `while`, no `foreach`, no `for`
- **NO timers** - no `Start-Sleep`, no timeouts
- **Message-based coordination** - workers send contribution messages
- **Supervisor wakes PM** - when all 3 workers sent contribution messages
- **Timeout escalation** - supervisor sends reminders to idle agents after 5 minutes

### Level 3: PM Synthesis

**P1 FIX: Workers send contribution messages AND write files. Use messages to track completion.**

**BEFORE synthesizing - verify ALL conditions met:**

1. ✅ Check inbox for `retrospective_contribution` messages from developer, techartist, qa
2. ✅ All 3 required workers have sent contribution messages
3. ✅ `.claude/session/retrospective-developer.json` exists (verified by message)
4. ✅ `.claude/session/retrospective-techartist.json` exists (verified by message)
5. ✅ `.claude/session/retrospective-qa.json` exists (verified by message)

**If NOT all 3 workers contributed via messages → EXIT and wait for next wake-up**

**Step 1: Read messages to confirm all workers contributed**

```bash
# Use Glob to find messages in your inbox:
Glob(".claude/session/messages/pm/msg-*.json")

# For each message file, use Read tool to check if type == "retrospective_contribution"
# Track which agents have contributed:
$contributedAgents = {}
For each message:
  If type == "retrospective_contribution":
    $contributedAgents[message.from] = true

# If NOT all 3 workers (developer, techartist, qa) contributed → EXIT and wait
```

**Step 2: Read all contribution files**

```bash
# Use Read tool to read contribution files
Read(".claude/session/retrospective-developer.json")
Read(".claude/session/retrospective-techartist.json")
Read(".claude/session/retrospective-qa.json")
```

**Step 3: Merge into retrospective.txt**

```markdown
# Build markdown from JSON contributions and write using Write tool

# Format each agent's contribution into markdown sections

# Write merged retrospective.txt using Write tool:

File: .claude/session/retrospective.txt

# Retrospective: {taskId} - {taskTitle}

**Started**: {timestamp}
**Task**: {taskId}

---

### Developer Perspective

**Implementation Decisions**:

- (from developer contribution)

**Technical Challenges Faced**:

- (from developer contribution)

**What Worked Well**:

- (from developer contribution)

**Areas for Improvement**:

- (from developer contribution)

**Lessons Learned**:

- (from developer contribution)

_**Contributed by**: Developer Agent | {timestamp}_

### Tech Artist Perspective

(Similar sections from tech artist contribution)

### QA Perspective

(Similar sections from QA contribution)

### PM Synthesis

**Summary**:

- Task accomplished: {taskTitle}
- Contributors: Developer, Tech Artist, QA
- All contributions received via separate files (P1 FIX - no race conditions)
```

**Step 3: Clean up contribution files**

```bash
# Remove contribution files using Bash
rm .claude/session/retrospective-developer.json 2>/dev/null || true
rm .claude/session/retrospective-techartist.json 2>/dev/null || true
rm .claude/session/retrospective-qa.json 2>/dev/null || true
```

**Step 3: Add PM synthesis**

When ALL conditions met, add synthesis covering:

```markdown
### PM Synthesis

**Summary**:

- Task accomplished: {{what was done}}
- Time taken: {{actual vs expected}}
- Challenges: {{unexpected issues}}

**Quality Assessment**:

- Developer insights: {{from dev section}}
- Tech Artist insights: {{from TA section}}
- QA validation: {{from qa section}}
- Code quality: {{combined assessment}}
- Visual quality: {{from TA section}}

**Risk Identification**:

- Technical risks: {{dependencies, performance}}
- Project risks: {{timeline, complexity}}
- Quality risks: {{technical debt, shortcuts}}

**Iteration Estimation**:

- Remaining tasks: {{count}}
- Estimated iterations: {{calculation}}
- Buffer needed: {{risk adjustment}}

**PRD Updates**:

- New risks discovered: {{list}}
- Description clarifications: {{if any}}
- New tasks from retrospective: {{list}}
```

**⚠️ CRITICAL: After synthesis, MUST commit before exiting:**

```bash
# Commit retrospective synthesis
git add .claude/session/retrospective.txt prd.json
git commit -m "[ralph] [pm] {taskId} retrospective: Worker contributions synthesized

- Synthesized contributions from Developer, Tech Artist, QA
- Identified {count} new tasks from findings
- Updated risk assessment

PRD: {taskId} | Agent: pm | Iteration: {iteration}"
```

Then set status and exit:

```bash
# Use Edit tool to update prd.json:
# 1. Set currentTask.status = "retrospective_synthesized"
# 2. Clear prd.json.session.retro section

# Exit for context reset
```

## Anti-Patterns

❌ **DON'T:**

- Skip retrospective even for "simple" tasks
- Synthesize before ALL THREE worker agents contribute
- Send playtest_request to Game Designer (use pm-playtest-session skill instead)
- Use `Start-Sleep` or timers - **NO polling, NO waiting**
- Use `while` loops - **blocks the process**
- Use `foreach` or `for` loops - **blocks the process**
- Forget to commit after synthesis
- Move to next phase without setting correct status

✅ **DO:**

- Send messages, then **EXIT** - let supervisor wake you when agents respond
- Check state on wake-up, proceed or **EXIT again** based on conditions
- Process ONE message per wake-up max (use `Select-Object -First 1`)
- Send `retrospective_initiate` to Developer, Tech Artist, QA **ONLY**
- **Commit changes** after synthesis before setting status and exiting
- Set status to `retrospective_synthesized` before exiting
- Use pm-playtest-session skill for the next phase

## Checklist

**Initial setup:**

- [ ] Created retrospective.txt with template
- [ ] Set `prd.json.items[{taskId}].status = "in_retrospective"`
- [ ] Initialized retrospective state in prd.json.session

**Messages sent:**

- [ ] Sent `retrospective_initiate` to Developer
- [ ] Sent `retrospective_initiate` to Tech Artist
- [ ] Sent `retrospective_initiate` to QA
- [ ] Did NOT send any message to Game Designer (handled in next phase)
- [ ] Exited to wait for worker responses

**Final verification before synthesis:**

- [ ] Developer contributed their perspective
- [ ] Tech Artist contributed their perspective
- [ ] QA contributed their perspective
- [ ] PM synthesis includes all sections
- [ ] Action items documented

**After synthesis:**

- [ ] **Committed changes** with git commit message
- [ ] Status set to `retrospective_synthesized`
- [ ] Cleared retrospective batching state from prd.json.session
- [ ] Exited for context reset (next phase will invoke playtest)

## Post-Retrospective Phases

After retrospective completes with status `retrospective_synthesized`:

1. **Playtest Phase** (use `pm-retrospective-playtest-session` skill):
   - Send `playtest_session_request` to Game Designer
   - Receive `playtest_session_report` with screenshots
   - Review findings, update PRD if needed
   - Set status to `playtest_complete`

2. **PRD Refinement Phase** (use `pm-organization-prd-reorganization` skill):
   - Extract tasks from GDD if updated
   - Create tasks from retrospective findings
   - Reorganize PRD priorities and dependencies
   - Send `prd_analysis_request` to Game Designer

3. **Acceptance Criteria Phase** (MANDATORY before task assignment):
   - Select next task with Game Designer input
   - Send `acceptance_criteria_request` to Game Designer
   - Receive `acceptance_criteria` with success criteria and test plan
   - Incorporate into task definition
   - Set status to `task_ready`

4. **Skill Research Phase** (use `pm-improvement-skill-research` skill):
   - Improve skills for ALL FIVE agents based on retrospective
   - Commit skill improvements
   - Set status to `completed`

5. **Complete**:
   - Delete retrospective.txt
   - Assign next task (now with proper acceptance criteria)

## Reference

- [pm-retrospective-playtest-session](../pm-retrospective-playtest-session/SKILL.md) — Playtest phase (next after retrospective)
- [pm-organization-prd-reorganization](../pm-organization-prd-reorganization/SKILL.md) — PRD refinement phase
- [pm-improvement-skill-research](../pm-improvement-skill-research/SKILL.md) — Skill research phase
- [shared-messaging](../shared-messaging/SKILL.md) — Message protocol
