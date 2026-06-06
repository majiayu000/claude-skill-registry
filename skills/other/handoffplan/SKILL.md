---
name: handoffplan
description: Run /handoff to capture session data, then write a phased implementation plan that references it. Creates beads for tracking.
user_invocable: true
triggers:
  - handoffplan
  - handoff with a plan
  - make this into a plan
  - create a plan and handoff
  - plan this out
argument-hint: [optional context about what to plan]
---

# Handoff Plan

**IMPORTANT: This skill writes files. You MUST NOT be in Claude Code's built-in plan mode.**
If you are currently in plan mode, **exit plan mode first** (use ExitPlanMode) before proceeding. This skill produces plan *files* — it does not use Claude Code's plan mode feature. They are different things.

**Step 1: Run `/handoff` to create the data file — FULL TWO-PHASE PROCESS.**

Execute the full `/handoff` skill first, including the **mandatory two-phase write process**:
- **Phase 1:** Write the handoff file (all sections, narrative + evidence)
- **Phase 2 (MANDATORY for Deep and Chunked passes):** Read it back, scan conversation for uncaptured data, use Edit to expand toward the ceiling (800 lines for 1M context)

This is not optional. The handoff is the data store — a thin handoff produces a thin plan. Follow the handoff skill's mining-pass detection, line count checks, and gap research pass exactly as specified.

**Do NOT skip or abbreviate the handoff.** Do NOT skip Phase 2. If the handoff is under 500 lines on a Chunked pass, you haven't mined deep enough — go back and expand before writing the plan.

**Do NOT ask to close the session after the handoff.** Skip Step 8 of the handoff skill — the close prompt happens after the plan is written, not after the handoff.

**Do NOT enter Claude Code plan mode at any point.** This skill writes files and commits. Plan mode is not used.

**This skill creates a plan for the NEXT session to execute.** The handoff captures data. The plan defines work. Beads track phases. Then you commit, close, and give the user a paste prompt that tells the next session to start executing Phase 1 immediately — no onboarding, no exploration, just code. The next session gets full clean context because it's a fresh session.

**Arguments:** $ARGUMENTS

---

**CHECKPOINT before Step 2:** Count the handoff's lines. Check its mining-pass minimum (Quick: 150/250, Deep: 300, Chunked: 500 — see handoff skill's Line Budget table). If the handoff is under its pass minimum, STOP. Run the handoff's Phase 2 gap research pass now — read back what you wrote, scan the conversation for uncaptured data, and Edit to expand. Do not proceed to the plan with a thin handoff. The plan's quality is bounded by the handoff's quality.

---

**Step 2: Write the plan file.**

Once the handoff file exists, write the plan. The plan lives in the **same directory** as the handoff, with the **same slug**:

- Handoff: `HANDOFF_{chain_tag}_{slug}_{date}.md` (already written — or `HANDOFF_{slug}_{date}.md` if no beads)
- Plan: `PLAN_{chain_tag}_{slug}_{date}.md` (write this now — mirror the handoff's naming)

### What makes a good plan

**If arguments were provided** (check `$ARGUMENTS` above): use them as a soft hint for framing the Problem Statement and phasing. They may suggest the epic scope, priority order, or what the user considers the first phase. Let them shape emphasis, but the handoff data is still the authority on what was actually tried and discovered.

The plan is an **action document**. It answers "what do we do next and how?" It should be:

- **Grounded in the handoff data.** Every phase should trace back to evidence. Don't propose approaches that contradict what "What We Tried" showed didn't work.
- **Specific enough to execute without the conversation.** Someone reading just the plan + handoff should be able to start coding. No vague "investigate X" — say what to investigate, where, and what outcome you expect.
- **Honest about what we don't know.** If a phase has uncertainty, say so and include how to handle both outcomes.
- **Referencing, not duplicating.** Data lives in the handoff. The plan points to it: "See Evidence section in {handoff_file}". Don't copy tables or measurement lists into the plan.

### Line budget: 120-250 lines

Scale with the number of phases and complexity. A 2-phase plan is shorter than a 5-phase plan.

### Plan Structure

```markdown
# {One-line summary of what we're planning}

**Date:** {YYYY-MM-DD}
**Status:** PLANNED
**Bead(s):** {active bead IDs, or "none"}
**Epic:** {parent epic/initiative name, if any}
**Chain:** `{chain_tag}` seq `{N}` (copied from paired handoff)
**Context:** See `{handoff_file_name}` for session data, test results, and prior approaches.

---

## Problem Statement

{3-5 sentences. What are we solving? Why does it matter? What's broken or missing?
Be specific — include key numbers from the handoff.
Reference the handoff for full data: "See Evidence & Data in {handoff_file}".}

## Key Findings

{5-8 bullet summary of the discoveries from this session (and prior sessions) that drive the plan.
These are CONCLUSIONS, not raw data — the raw data is in the handoff.
Each bullet should connect to a phase: "→ drives Phase N" to show the data-to-action link.}

## Anti-Goals (What NOT To Do)

{Approaches explicitly rejected and why. Things the next session should NOT attempt.
Pull from "What We Tried" and "Key Decisions" in the handoff.
2-5 bullets. Skip only if no approaches were rejected.}

## Plan

### Phase 1: {name}

**Goal:** {One sentence — what this phase achieves and why it matters}

**Why this approach:** {1-2 sentences connecting this to the evidence. Why THIS and not the alternatives tried/rejected?}

{Detailed implementation steps — explain HOW, not just WHAT:
- Specific functions/methods to change and what the change is
- New parameters, their defaults, and WHY those defaults (connect to evidence)
- The before→after for each change (old behavior → new behavior)
- Edge cases to handle and how
- How this connects to the findings above
6-10 bullet points.}

**Files:** {files to modify/create, with brief note on what changes in each}
**Validates with:** {specific test commands, expected outputs, success criteria with numbers}
**Rollback:** {what to revert if this phase makes things worse}

### Phase 2: {name}

**Goal:** {One sentence}
**Why this approach:** {1-2 sentences}

{Same level of detail. 6-10 bullet points.}

**Files:** {files}
**Validates with:** {criteria}
**Rollback:** {revert plan}

### Phase N: {name} (as many as needed, prefer 2-5)

{Same format.}

## Dependencies & Order

{What must happen before what. Which phases can run in parallel.
2-5 bullets.}

## Risks & Mitigations

{What could go wrong AND what to do about it. For each:
- The risk
- How likely (based on evidence from the handoff)
- The mitigation or fallback
3-6 bullets.}

## Success Criteria

{How do we know the plan worked? Specific, measurable outcomes.
Reference baseline numbers from the handoff.
Include both "minimum viable success" and "full success" if applicable.
3-6 bullets.}

## Quick Start

```bash
# Restore full context
cat {handoff_file_path}

# Prior context (if OV available)
# /memory-recall {topic keywords}

# Key source files for Phase 1
{3-5 files to read before starting}

# Baseline data to reference
{path to test results / measurement files}

# Verify starting state
{test command to confirm things work before changing anything}

# First concrete action
{THE specific code change or command to begin Phase 1}
```
```

---

**Step 3: Create beads for phases (if available).**

```bash
bd create --title="Phase 1: {name}" --description="{what and why}" --type=task --priority=2
bd create --title="Phase 2: {name}" --description="{what and why}" --type=task --priority=2
# Add dependencies between phases
bd dep add {phase2_id} {phase1_id}
```

If tasks are already in_progress, update their notes:
```bash
bd update {id} --notes "Plan written. See {plan_file_path}"
```

**Step 4: Persist to memory (if available).**

```bash
bd remember "Plan written to {plan_path}, handoff to {handoff_path}. Next: Phase 1 — {first action}"
```

**Step 5: Report.**

Tell the user concisely:
- Both files written and their paths
- Line counts for each
- The "First Action" from Quick Start
- Beads created for each phase (if available)

**Step 6: Commit and close.**

This skill always closes the session. The next session executes the plan with full clean context.

1. **Commit all session work:**
   ```bash
   git status -s
   git diff --stat
   ```
   Stage all changed/new files relevant to this session's work, then commit:
   ```
   session: {slug} [{chain_tag}]

   {One-line summary of what this session accomplished}

   Handoff: {handoff_filename}
   Plan: {plan_filename}
   Bead(s): {bead_ids or "none"}

   Generated with [Claude Code](https://claude.ai/code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```
   Be surgical — only commit files related to this session's work. If `git status` shows unrelated changes from other sessions, mention them but don't commit them.

2. **Output the ready-to-paste prompt:**
   ```
   -------------------------------------------------------
   PASTE THIS INTO YOUR NEXT SESSION:
   -------------------------------------------------------
   Read `{plan_file_path}` and `{handoff_file_path}` (seq {N}, {chain_tag}).
   Execute the plan starting at Phase 1. Beads are already created with dependencies.

   Your first actions:
   1. Read the plan file
   2. Create a task for each phase (TaskCreate) so you can track progress
   3. Claim Phase 1: `bd update {phase1_bead} --claim`
   4. Read the source files listed in the plan's Quick Start
   5. Start coding Phase 1's first concrete action: {first_action}

   For phases the plan marks as parallelizable, use the Agent tool to run them concurrently in worktrees.

   Do NOT onboard, explore, or ask questions. The plan has everything. Build.
   -------------------------------------------------------
   ```

3. Tell the user: "Session closed. Paste that into a fresh session to start executing Phase 1 with full context."

---

## Rules

1. **Handoff first, always.** Run the full `/handoff` skill. Don't abbreviate it. Don't skip steps. The plan depends on the handoff being thorough.
2. **Plan references handoff, never duplicates.** Data lives in the handoff. The plan points to it.
3. **Every phase traces to evidence.** "Why this approach" must connect to findings from the handoff.
4. **Anti-Goals prevent re-work.** Explicitly state what NOT to do based on prior failures.
5. **Phases explain HOW, not just WHAT.** "Remove is_low_onset param, compute own onset from low_flux using 3.0x median threshold" not "modify the detector."
6. **Success criteria use baseline numbers.** Reference the handoff's Evidence & Data section.
7. **Rollback per phase.** Every phase must say what to revert if it makes things worse.
8. **Same naming for paired files.** Mirror the handoff filename: `HANDOFF_Proj-abc_foo_date.md` + `PLAN_Proj-abc_foo_date.md` (or without chain tag if no beads).
9. **Always close the session.** This skill mines, plans, and closes. The next session executes with full clean context. Don't try to execute in the same session — context is exhausted from mining.
10. **Chain metadata propagates.** The PLAN file must copy the Chain line from its paired HANDOFF file. Same chain-id, same seq. This lets cleanup find both files together.
11. **The paste prompt is an execution prompt, not an onboarding prompt.** The difference between `/handoff` and `/handoffplan` is what the next session does. After `/handoff`, the next session onboards and explores. After `/handoffplan`, the next session reads the plan and starts coding Phase 1 immediately.
