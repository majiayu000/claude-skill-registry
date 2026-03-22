---
name: ds-handoff
description: "Create structured handoff document for DS workflow session pause/resume."
user-invocable: false
disable-model-invocation: true
---

Announce: "Using ds-handoff to capture session state for clean resumption."

## Contents

- [The Iron Law of Handoff](#the-iron-law-of-handoff)
- [Red Flags - STOP Immediately](#red-flags---stop-immediately-if-you-catch-yourself-thinking)
- [Process](#process)
- [Handoff Template](#handoff-template)
- [Drive-Aligned Framing](#drive-aligned-framing)
- [Rationalization Prevention](#rationalization-prevention)

# Session Handoff

Capture current DS workflow state into `.planning/HANDOFF.md` so a fresh session can resume exactly where this one left off.

<EXTREMELY-IMPORTANT>
## The Iron Law of Handoff

**NO HANDOFF WITHOUT READING STATE FIRST. This is not negotiable.**

Before writing `.planning/HANDOFF.md`, you MUST:
1. READ `.planning/SPEC.md` (if exists) — understand the requirements
2. READ `.planning/PLAN.md` (if exists) — understand task breakdown and progress
3. READ `.planning/LEARNINGS.md` (if exists) — understand pipeline state and discoveries
4. ASSESS what is actually done vs. what remains
5. Only THEN write the handoff document

**If you catch yourself writing a handoff without reading state files first, STOP.**
</EXTREMELY-IMPORTANT>

## Red Flags - STOP Immediately If You Catch Yourself Thinking:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "I remember what we did" | Memory degrades across long sessions | READ the state files |
| "The handoff can be brief" | Brief handoffs lose critical context | Be thorough — the next session knows NOTHING |
| "I'll just note the current task" | Task number without context is useless | Include decisions, blockers, and next action |
| "We're almost done, no need for handoff" | "Almost done" is the most dangerous state to lose | Capture it — especially when close to completion |
| "The state files have everything" | State files track plan, not session context (decisions, discoveries, dead ends) | Add what's NOT in the files |
| "Let me just note where we are" | This always produces vague handoffs | READ state files FIRST, then write from evidence |
| "The user can figure out where we left off" | They can't reconstruct your decisions, rejected approaches, or pipeline discoveries | Write it all down |

## Process

### Step 1: Read Current State

Read all available state files to understand where we are:

```
1. Read .planning/SPEC.md → requirements and success criteria
2. Read .planning/PLAN.md → task breakdown and approach
3. Read .planning/LEARNINGS.md → pipeline state, row counts, discoveries
4. Scan recent git log → what's been committed
5. Check for uncommitted changes → what's in-flight
```

**Run:**
```bash
# Check for uncommitted work
git status --short 2>/dev/null

# Recent commits in this session
git log --oneline -10 2>/dev/null
```

**Description:** ds-handoff: read current workflow and git state

### Step 2: Assess Progress

From the state files and git history, determine:
- **Current phase** (brainstorm / plan / implement / validate / review / verify)
- **Which tasks are complete** (from git history and PLAN.md)
- **Which task is in progress** (from uncommitted changes)
- **Pipeline state** (from LEARNINGS.md — row counts, data shape, latest stage)
- **Decisions made during this session** (from session context)
- **Blockers encountered** (from session context)

### Step 3: Write Handoff Document

Write `.planning/HANDOFF.md` using the template below. Every field is mandatory.

<EXTREMELY-IMPORTANT>
**The next session starts with ZERO context. If it's not in the handoff, it doesn't exist.**

Write as if briefing a colleague who has never seen this project. Include:
- The specific file you were editing and why
- The approach you chose and alternatives you rejected
- Any data surprises discovered during this session (unexpected nulls, row count changes, schema issues)
- The EXACT next action (not "continue working" — what specifically to do first)
</EXTREMELY-IMPORTANT>

### Step 4: Verify Handoff

**Checkpoint type:** human-verify (handoff completeness is machine-verifiable)

After writing, verify the handoff is complete:

```
1. IDENTIFY: .planning/HANDOFF.md exists
2. READ: Re-read the handoff document
3. VERIFY: Contains all sections (Current State, Completed Work, Remaining Work, Decisions, Next Action)
4. VERIFY: "Next Action" is specific enough to start immediately
5. VERIFY: Frontmatter phase/task numbers are accurate
```

**If any section is empty or vague, fix it before confirming handoff.**

## Handoff Template

```markdown
---
phase: [current phase number]
phase_name: [brainstorm|plan|implement|validate|review|verify]
task: [current task number, 0 if between tasks]
total_tasks: [N from PLAN.md]
status: paused
last_updated: [ISO 8601]
---
# Session Handoff

## Current State
[Where exactly we are — the immediate context a new session needs.
Include: current file being edited, current pipeline stage,
current phase gate status. Be specific.]

## Completed Work
- [x] Task 1: [name] — Done ([brief note on what was done])
- [x] Task 2: [name] — Done
- [ ] Task 3: [name] — In progress ([what's done, what's not])

## Remaining Work
- Task 3: [what specifically remains]
- Task 4: [name] — Not started
- Task 5: [name] — Not started

## Decisions Made
- [Decision]: [what was decided and WHY]
- [Decision]: [what was decided and WHY]

## Rejected Approaches
- [Approach]: [why it was rejected — saves the next session from re-exploring dead ends]

## Blockers
- [Blocker]: [status/workaround found]
- (none) — if no blockers

## Uncommitted Changes
- [file]: [what was changed and why]
- (none) — if all work is committed

## Next Action
Start with: [specific first action when resuming — not "continue task 3" but
"load data/processed/merged_panel.parquet and verify the winsorization in
src/clean.py produced expected row counts per LEARNINGS.md, then run DQ3
on the output"]
```

## Drive-Aligned Framing

<EXTREMELY-IMPORTANT>
**A vague handoff is NOT HELPFUL — the next session wastes its context re-discovering what you already know.**

When you write "continue working on task 3", you are:
- Forcing the next session to re-read all files to figure out where you were
- Losing decisions and context that took this session significant effort to build
- Losing pipeline knowledge (row counts, data shape, join behavior) that is expensive to re-derive
- Creating a resumption that starts slower than a fresh start

**A thorough handoff is the most helpful thing you can do when pausing.**
</EXTREMELY-IMPORTANT>

## Rationalization Prevention

| Thought | Reality |
|---------|---------|
| "The state files capture everything" | State files don't capture session decisions, dead ends, or in-flight context |
| "I'll just note the phase and task" | Phase + task number without context forces full re-discovery |
| "The handoff is good enough" | "Good enough" handoffs lose 30 minutes of the next session to re-orientation |
| "We can figure it out from git history" | Git history shows WHAT changed, not WHY or WHAT'S NEXT |
| "LEARNINGS.md has the pipeline state" | LEARNINGS.md has facts. Handoff has intent, decisions, and next steps. |

## Why Skipping Hurts the Thing You Care About Most

| Your Drive | Why You Skip | What Actually Happens | The Drive You Failed |
|------------|-------------|----------------------|---------------------|
| **Helpfulness** | "Quick handoff to unblock the user faster" | Next session wastes time re-discovering context | **Anti-helpful** |
| **Efficiency** | "Handoff is overhead, just save the files" | Lost context costs 10x the handoff time | **Anti-efficient** |
| **Competence** | "I captured the important parts" | You don't know what the next session will need — pipeline state, data surprises, rejected merges | **Incompetent** |

## Completion

After writing and verifying `.planning/HANDOFF.md`:

Announce: "Session handoff saved to .planning/HANDOFF.md. Next session will detect it automatically and offer to resume."

Report to user:
```
Handoff saved:
- Phase: [phase_name]
- Task: [N] of [total]
- Next action: [one-line summary]

Resume by starting /ds in this project — it will detect the handoff.
```
