---
name: writing-handoff
description: "Create structured handoff document for writing workflow session pause/resume."
user-invocable: false
disable-model-invocation: true
---

Announce: "Using writing-handoff to capture session state for clean resumption."

## Contents

- [The Iron Law of Handoff](#the-iron-law-of-handoff)
- [Red Flags - STOP Immediately](#red-flags---stop-immediately-if-you-catch-yourself-thinking)
- [Process](#process)
- [Handoff Template](#handoff-template)
- [Drive-Aligned Framing](#drive-aligned-framing)
- [Rationalization Prevention](#rationalization-prevention)

# Session Handoff

Capture current writing workflow state into `.planning/HANDOFF.md` so a fresh session can resume exactly where this one left off.

<EXTREMELY-IMPORTANT>
## The Iron Law of Handoff

**NO HANDOFF WITHOUT READING STATE FIRST. This is not negotiable.**

Before writing `.planning/HANDOFF.md`, you MUST:
1. READ `.planning/PRECIS.md` (if exists) — understand the argument and claims
2. READ `.planning/OUTLINE.md` (if exists) — understand section structure and mapping
3. READ `.planning/ACTIVE_WORKFLOW.md` (if exists) — understand current phase and progress
4. ASSESS what is actually done vs. what remains
5. Only THEN write the handoff document

**If you catch yourself writing a handoff without reading state files first, STOP.**
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## Red Flags - STOP Immediately If You Catch Yourself Thinking:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "I remember what we wrote" | Memory degrades across long sessions — sections blur together | READ the state files |
| "The handoff can be brief" | Brief handoffs lose critical context about argument direction | Be thorough — the next session knows NOTHING |
| "I'll just note the current section" | Section name without context (which claims it serves, what's drafted vs. outlined) is useless | Include decisions, argument direction, and next action |
| "We're almost done, no need for handoff" | "Almost done" is the most dangerous state to lose — one missed section derails review | Capture it — especially when close to completion |
| "The state files have everything" | State files track structure, not session context (style decisions, argument pivots, rejected framings) | Add what's NOT in the files |
| "Let me just note where we are" | This always produces vague handoffs | READ state files FIRST, then write from evidence |
| "The user can figure out where we left off" | They can't reconstruct your argument decisions, rejected framings, or section dependencies | Write it all down |
</EXTREMELY-IMPORTANT>

## Process

### Step 1: Read Current State

Read all available state files to understand where we are:

```
1. Read .planning/PRECIS.md → argument claims and commitments
2. Read .planning/OUTLINE.md → section structure and claim mapping
3. Read .planning/ACTIVE_WORKFLOW.md → current phase, style, progress
4. Read .planning/VALIDATION.md (if exists) → coverage status
5. Scan recent git log → what's been committed
6. Check for uncommitted changes → what's in-flight
```

**Run:**
```bash
# Check for uncommitted work
git status --short 2>/dev/null

# Recent commits in this session
git log --oneline -10 2>/dev/null
```

**Description:** writing-handoff: read current workflow and git state

### Step 2: Assess Progress

From the state files and git history, determine:
- **Current phase** (setup / outline / draft / validate / review / revise)
- **Which sections are complete** (from git history, drafts/ directory, ACTIVE_WORKFLOW.md)
- **Which section is in progress** (from uncommitted changes)
- **Argument state** (from PRECIS.md — which claims are drafted, which are pending)
- **Decisions made during this session** (from session context — style choices, argument pivots)
- **Blockers encountered** (from session context)

### Step 3: Write Handoff Document

Write `.planning/HANDOFF.md` using the template below. Every field is mandatory.

<EXTREMELY-IMPORTANT>
**The next session starts with ZERO context. If it's not in the handoff, it doesn't exist.**

Write as if briefing a colleague who has never seen this project. Include:
- The specific section you were drafting/reviewing and why
- The argument direction you chose and alternatives you rejected
- Any structural discoveries (sections that need merging, claims that need splitting, transitions that don't work)
- The EXACT next action (not "continue writing" — what specifically to do first)
</EXTREMELY-IMPORTANT>

### Step 4: Verify Handoff

After writing, verify the handoff is complete:

```
1. IDENTIFY: .planning/HANDOFF.md exists
2. READ: Re-read the handoff document
3. VERIFY: Contains all sections (Current State, Completed Work, Remaining Work, Decisions, Next Action)
4. VERIFY: "Next Action" is specific enough to start immediately
5. VERIFY: Frontmatter phase/section numbers are accurate
```

**If any section is empty or vague, fix it before confirming handoff.**

## Handoff Template

```markdown
---
phase: [current phase number]
phase_name: [setup|outline|draft|validate|review|revise]
section_in_progress: [current section name or "none"]
total_sections: [N from OUTLINE.md]
status: paused
last_updated: [ISO 8601]
---
# Session Handoff

## Current State
[Where exactly we are — the immediate context a new session needs.
Include: current section being drafted/revised, current phase,
current gate status, which PRECIS claims are covered. Be specific.]

## Completed Work
- [x] Section I: [name] — Drafted ([brief note on argument])
- [x] Section II: [name] — Drafted
- [ ] Section III: [name] — In progress ([what's drafted, what's not])

## Remaining Work
- Section III: [what specifically remains — which outline points are unexpanded]
- Section IV: [name] — Not started
- Validation — Not run yet

## Decisions Made
- [Style choice]: [what was decided and WHY — e.g., "Chose to lead with empirical finding rather than doctrinal framework because audience is policy-oriented"]
- [Argument direction]: [what was decided and WHY — e.g., "Framed counterargument as steelman rather than strawman to strengthen Section IV rebuttal"]

## Rejected Approaches
- [Framing]: [why it was rejected — saves the next session from re-exploring dead ends]
- [Structure]: [e.g., "Tried putting methodology in Section I but it buried the hook — moved to Section II"]

## Blockers
- [Blocker]: [status/workaround found]
- (none) — if no blockers

## Uncommitted Changes
- [file]: [what was changed and why]
- (none) — if all work is committed

## Next Action
Start with: [specific first action when resuming — not "continue Section III" but
"Open outlines/Section III (Outline).md and expand points 3.2-3.4 into prose,
focusing on the counterargument to Smith (2024) that PRECIS.md commits to addressing.
The first two subsections are drafted in drafts/Section III (Draft).md."]
```

## Drive-Aligned Framing

<EXTREMELY-IMPORTANT>
**A vague handoff is NOT HELPFUL — the next session wastes its context re-discovering what you already know.**

When you write "continue working on Section III", you are:
- Forcing the next session to re-read all files to figure out where you were
- Losing argument decisions and framing choices that took this session significant effort to develop
- Losing structural knowledge (which sections connect, which transitions work, which claims are weak) that is expensive to re-derive
- Creating a resumption that starts slower than a fresh start

**A thorough handoff is the most helpful thing you can do when pausing.**
</EXTREMELY-IMPORTANT>

## Rationalization Prevention

| Thought | Reality |
|---------|---------|
| "The state files capture everything" | State files don't capture session decisions, rejected framings, or in-flight argument pivots |
| "I'll just note the phase and section" | Phase + section name without context forces full re-discovery |
| "The handoff is good enough" | "Good enough" handoffs lose 30 minutes of the next session to re-orientation |
| "We can figure it out from git history" | Git history shows WHAT changed, not WHY or WHAT'S NEXT |
| "ACTIVE_WORKFLOW.md has the progress" | ACTIVE_WORKFLOW.md has phase tracking. Handoff has intent, decisions, and next steps. |

## Why Skipping Hurts the Thing You Care About Most

| Your Drive | Why You Skip | What Actually Happens | The Drive You Failed |
|------------|-------------|----------------------|---------------------|
| **Helpfulness** | "Quick handoff to unblock the user faster" | Next session wastes time re-discovering argument direction and section dependencies | **Anti-helpful** |
| **Efficiency** | "Handoff is overhead, just save the files" | Lost context costs 10x the handoff time — re-reading every draft to reconstruct where the argument stands | **Anti-efficient** |
| **Competence** | "I captured the important parts" | You don't know what the next session will need — rejected framings, structural discoveries, style decisions made mid-draft | **Incompetent** |

## Completion

After writing and verifying `.planning/HANDOFF.md`:

Announce: "Session handoff saved to .planning/HANDOFF.md. Next session will detect it automatically and offer to resume."

Report to user:
```
Handoff saved:
- Phase: [phase_name]
- Section: [section_in_progress] ([N] of [total] sections)
- Next action: [one-line summary]

Resume by starting /writing in this project — it will detect the handoff.
```
