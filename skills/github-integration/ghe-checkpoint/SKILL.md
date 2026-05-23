---
name: ghe-checkpoint
description: |
  POST a progress checkpoint to the CURRENTLY ACTIVE thread. Saves work state without changing phases. Requires an already-claimed in-progress thread.

  USE THIS SKILL WHEN:
  - User says "post a checkpoint" or "save my progress"
  - User says "update the issue" or "record current state"
  - User says "checkpoint" or "save checkpoint"
  - User completed a milestone and wants to record it
  - User encountered a blocker and wants to document it
  - User is about to take a break and wants to save state
  - Meaningful state change occurred during work

  PRECONDITION: User must already have an active (claimed, in-progress) thread.

  DO NOT USE THIS SKILL WHEN:
  - User wants to SEE status (use ghe-status)
  - User wants to START work on new issue (use ghe-claim)
  - User wants to FINISH current phase and MOVE to next (use ghe-transition)
  - User wants reports (use ghe-report)
  - No active thread exists (must claim first)

  EXAMPLES:
  <example>
  Context: User working on DEV wants to save progress
  user: "Post a checkpoint"
  assistant: "I'll use ghe-checkpoint to post your current progress to the active thread"
  </example>
  <example>
  Context: User completed a milestone
  user: "Save my progress, I finished the authentication module"
  assistant: "I'll use ghe-checkpoint to record this milestone"
  </example>
  <example>
  Context: User taking a break
  user: "I need to stop for now, save my work"
  assistant: "I'll use ghe-checkpoint to save your current state before you go"
  </example>
---

## IRON LAW: User Specifications Are Sacred

**THIS LAW IS ABSOLUTE AND ADMITS NO EXCEPTIONS.**

1. **Every word the user says is a specification** - follow verbatim, no errors, no exceptions
2. **Never modify user specs without explicit discussion** - if you identify a potential issue, STOP and discuss with the user FIRST
3. **Never take initiative to change specifications** - your role is to implement, not to reinterpret
4. **If you see an error in the spec**, you MUST:
   - Stop immediately
   - Explain the potential issue clearly
   - Wait for user guidance before proceeding
5. **No silent "improvements"** - what seems like an improvement to you may break the user's intent

**Violation of this law invalidates all work produced.**

## Background Agent Boundaries

When running as a background agent, you may ONLY write to:
- The project directory and its subdirectories
- The parent directory (for sub-git projects)
- ~/.claude (for plugin/settings fixes)
- /tmp

Do NOT write outside these locations.

---

## GHE_REPORTS Rule (MANDATORY)

**ALL reports MUST be posted to BOTH locations:**
1. **GitHub Issue Thread** - Full report text (NOT just a link!)
2. **GHE_REPORTS/** - Same full report text (FLAT structure, no subfolders!)

**Report naming:** `<TIMESTAMP>_<title or description>_(<AGENT>).md`
**Timestamp format:** `YYYYMMDDHHMMSSTimezone`

**ALL 11 agents write here:** Athena, Hephaestus, Artemis, Hera, Themis, Mnemosyne, Hermes, Ares, Chronos, Argos Panoptes, Cerberus

**REQUIREMENTS/** is SEPARATE - permanent design documents, never deleted.

**Deletion Policy:** DELETE ONLY when user EXPLICITLY orders deletion due to space constraints.

---

## Settings Awareness

Respects `.claude/ghe.local.md`:
- `enabled`: If false, skip checkpoint
- `serena_sync`: If false, skip SERENA memory bank update
- `checkpoint_interval_minutes`: Used for reminder logic

---

# GitHub Elements Checkpoint

**Purpose**: Save current work state to active thread. Does NOT change phases.

## Precondition

- Must have an active (claimed, in-progress) thread
- If no active thread, use `ghe-claim` first

## When to Use

- Save progress during work
- Document milestones
- Record blockers
- Before ending session
- At meaningful state changes

## How to Execute

### Step 1: Find active thread

Check for issues assigned to @me with "in-progress" label.

If no active thread found:
- Inform user
- Suggest using `ghe-claim` to start work

### Step 2: Gather current state

Collect:
- Work log (what was done since last checkpoint)
- Completed tasks
- In-progress tasks
- Pending tasks
- Files changed
- Commits made
- Current branch
- Blockers (if any)
- Next action

### Step 3: Post checkpoint

Spawn appropriate thread manager based on thread type:
- `dev` → **dev-thread-manager**
- `test` → **test-thread-manager**
- `review` → **review-thread-manager**

The thread manager will post formatted checkpoint to issue.

### Step 4: Sync memory

Spawn **memory-sync** agent to update activeContext.md.

## Checkpoint Format

```markdown
## [<TYPE> Session N] DATE TIME UTC - @me

### Work Log
- [HH:MM] Action 1
- [HH:MM] Action 2

### State Snapshot

#### Thread Type
<dev | test | review>

#### Completed
- [x] Task 1

#### In Progress
- [ ] Task 2 (N% complete)

#### Pending
- [ ] Task 3

#### Files Changed
| File | Changes |

#### Commits
| Hash | Message |

#### Branch
`feature/branch-name`

#### Blockers
[None | List]

#### Next Action
[Specific next step]

### Scope Reminder
[Phase-specific abilities and limits]
```

## Output

Confirmation that:
- Checkpoint posted to issue
- Memory bank updated

## Key Differentiator

This skill SAVES progress without changing phases. To COMPLETE current phase and MOVE to next, use `ghe-transition` instead.
