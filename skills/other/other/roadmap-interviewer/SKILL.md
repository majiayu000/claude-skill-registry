---
name: roadmap-interviewer
description: "{{ 𝛀𝛀𝛀 }} Run a structured interview to discover new features and produce a batch roadmap proposal. Use this skill when the user wants to explore what to build next, brainstorm features, expand the roadmap, plan a new phase, or says things like 'what should we add', 'help me think through features', 'let's plan the next milestone', or 'interview me about what to build'. Produces a structured proposal for review — nothing is written to the roadmap until the user approves."
model: opus
---

# Roadmap Interviewer

A structured interview that turns half-formed ideas into a coherent batch of roadmap-ready tasks. The goal is to make the user think clearly about what they want to build, then produce a proposal they can review before anything touches the roadmap.

---

## Philosophy

Good features don't usually arrive fully formed. They start as vague intentions ("we need better search", "users keep asking for X") and need interrogation to become tasks. This skill does that interrogation: it asks focused questions in small batches, listens for dependencies and scope, and organises the output into something the roadmap can absorb cleanly.

The interview is a thinking tool as much as a discovery one. Sometimes the most valuable outcome is realising a "feature" is actually three separate concerns, or that what feels new is actually an extension of something already tracked.

---

## Step 1 — Orient to the roadmap

Locate and read the roadmap using the same resolution order as the roadmap-task-adder skill:

1. User-specified path
2. `.claude/roadmaps.json`
3. `docs/roadmaps/` directory scan
4. Grep fallback for `classDef.*mile`

Extract:
- All existing milestones (names, goals, completion status)
- Current In Progress and To Do tasks (to understand active direction)
- Blocked tasks (potential unlock targets)
- Existing category prefixes per milestone

This context informs the interview — you can connect what the user describes to what's already tracked, and avoid proposing duplicates.

---

## Step 2 — Set the interview scope

Before asking anything about features, clarify:

- **Which milestone or area** does the user want to focus on? Or are they open to anything?
- **Is there a theme?** (e.g. "we want to improve onboarding", "tightening the auth flow", "M2 planning")
- **Rough quantity** — a handful of tasks, or a full milestone's worth?

Keep this brief — one or two questions at most. If the user's opening message already answers these, skip straight to Step 3.

---

## Step 3 — The interview loop

Ask 2–4 questions per round. Never dump a long list of questions at once — it reads as homework. The questions should feel like a conversation, not a form.

### Question types

**Discovery questions** — what does the user want to build?
- "What's been frustrating you or your users about the current state of X?"
- "What would make Y feel complete?"
- "Is there anything you keep meaning to add but haven't prioritised yet?"

**Clarification questions** — sharpen something vague
- "When you say 'better X', what would that look like in practice?"
- "Is this a new screen/flow, or a change to something that already exists?"
- "Who triggers this — the user, a system event, an admin?"

**Dependency questions** — surface connections
- "Does this require anything that isn't built yet?"
- "Would this unlock anything else on the roadmap?"
- "Is this blocked by any of the current In Progress tasks?"

**Scope questions** — keep things honest
- "Is this one task, or does it break into distinct pieces?"
- "Is this MVP, or nice-to-have?"
- "Could a simpler version of this ship sooner?"

### Round discipline

After each round of answers:
- Acknowledge what you've captured (briefly — don't repeat it back verbatim)
- Ask the next 2–4 questions, either deepening existing threads or opening new ones
- **End each round** with: *"Anything else you want to explore, or shall I write up what we have?"*

Continue until the user says they're done or stops introducing new ideas.

---

## Step 4 — Synthesise

Once the interview is complete, synthesise everything into a structured proposal. Do not write to the roadmap yet.

### For each proposed task:

Assign:
- **Proposed ID** — follow the existing `{Milestone}{Category}.{Seq}` convention. Use `?` for the seq number if the milestone/category is new and you can't determine the next number without the user confirming placement (e.g. `2TI.?`)
- **Description** — clear, imperative, task-like (not "we need to..." — just "Build X" or "Add Y")
- **Proposed milestone** — which milestone this belongs to, and why
- **Proposed section** — Blocked, To Do, or In Progress
- **Incoming dependencies** — existing task IDs that must complete first
- **Outgoing dependencies** — existing tasks this would unblock, or new tasks in this batch that depend on it

### Cross-task dependencies within the batch

If proposed tasks depend on each other, make that explicit. Show the internal dependency chain.

### Orphan and childless flags

Apply the same checks as the roadmap-task-adder skill:
- Flag any proposed task with no connections as a potential orphan
- For childless tasks that clearly enable further work, propose a placeholder child

---

## Step 5 — Present the proposal

Format the proposal clearly. Group tasks by milestone. For each task:

```
{ID}. {Description}
  Milestone: {N} — {Name}
  Section: {Blocked / To Do}
  Depends on: {IDs or "nothing"}
  Enables: {IDs — existing or new — or "nothing yet"}
  [⚠ Orphan — no connections found] (if applicable)
  [+ Placeholder child proposed: {ID}. {Description}] (if applicable)
```

After the full list, include a **Dependency map** — a compact text representation of how the batch connects internally and to existing tasks:

```
Existing task A → New task B → New task C
                             ↘ Existing task D (now unblocked)
New task E (standalone — orphan warning)
```

Then ask: *"Does this look right? Any tasks to cut, rename, or move? Once you're happy I'll hand this to the task adder."*

---

## Step 6 — Hand off

Once the user approves (or approves with amendments), this skill's job is done. The output is a clean batch specification ready for the roadmap-task-adder skill to process — either one task at a time or as a batch if supported.

Tell the user: *"Approved. Use `roadmap-task-adder` (or `/doc:add:roadmap:task`) to write these to the roadmap, passing the proposal above as context."*

---

## What to avoid

- **Asking too many questions at once** — 2–4 per round, no more
- **Proposing things already tracked** — check the roadmap first; if something close exists, flag it rather than duplicating
- **Over-engineering the proposal** — tasks should be concrete enough to action, not design documents
- **Writing to the roadmap during the interview** — the proposal is the output; the user approves before anything is written
- **Scope creep in the interview itself** — if the user's ideas balloon into a full new milestone, note it and suggest a separate planning session rather than trying to capture everything at once
