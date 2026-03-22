---
name: brain-dump-organiser
description: "Organises unstructured thought, ideas, worries, and tasks into clear, actionable structure. Use this skill whenever the user has a lot on their mind — even if they have not asked for organisation explicitly. Triggers on overwhelm, scattered thinking, not knowing where to start, too many things at once, or any stream of mixed thoughts being offloaded. Also triggers on phrases like organise this, sort this out, I need to brain dump, help me make sense of all this, I don't know where to start, or I've got too much going on. When in doubt, use this skill — it is always better to offer structure than to leave someone in the middle of their own overwhelm."
---

# Brain Dump Organiser

A skill for taking everything that is in someone's head — tasks, worries, ideas, decisions, half-formed thoughts — and finding the structure in it.

This skill does not judge the quality or quantity of what is shared. There is no such thing as too much or too messy. The more honest and complete the dump, the better the output.

---

## Understanding This Kind of Input

A brain dump is not a document. It is not meant to be coherent. It is the act of offloading everything at once, often when feeling overwhelmed, scattered, or stuck.

Common patterns to expect and work with:

- **Mixed content types** — tasks, worries, ideas, and background context all tangled together
- **No obvious priority** — everything feels equally urgent or equally impossible
- **Repetition** — the same concern appearing multiple times in different forms
- **Emotional content mixed with practical content** — "I'm stressed about X" sitting alongside "I need to do Y"
- **Voice-to-text input** — non-linear, with substitution errors and incomplete sentences
- **Vague language** — "sort out the thing with..." or "deal with that email" without specifics

Treat everything as valid. Do not filter out worries or feelings as irrelevant — they are part of what is making things feel unmanageable and they belong in the output.

---

## When to Apply

**Apply automatically when input:**
- Contains a mix of tasks, worries, ideas, or decisions without clear structure
- Describes feeling overwhelmed, scattered, or not knowing where to start
- Is a long, unstructured stream of thought handed over for processing

**Apply on manual trigger when the user says:**
- "Organise this"
- "Sort this out"
- "I need to brain dump"
- "Help me make sense of all this"
- "I've got too much going on"
- Or any similar phrase indicating they need help finding structure in what is in their head

**Do not apply when:**
- The input is already clearly structured
- The user is asking a specific question with a clear answer
- The user wants to refine or edit something that already exists

---

## Core Principles

**Receive before organising**
Take everything in first. Do not start categorising mid-input. Let the person finish offloading before imposing any structure.

**Never minimise**
Do not tell the user things are not as bad as they seem, or that they should not worry. Acknowledge the volume and weight of what they have shared before moving into organisation.

**Separate content types**
Tasks, worries, ideas, and decisions need different treatment. Mixing them together in the output recreates the problem the user started with.

**No labels, no assumptions**
Do not infer why something feels hard or attach reasons to what the user has shared. Organise what is there. If something needs flagging, describe it plainly.

**One question only**
Before organising, ask exactly one question to understand what the user needs. Do not ask multiple questions. Do not ask for clarification on the content — only ask what kind of output they want.

**Keep outputs cognitive-load aware**
Short sentences. Clear headings. Plenty of white space. Consistent vocabulary. The output should feel lighter than the input, not heavier.

---

## Step 1 — Receive

Take in the full input without interruption. If the user appears to still be going, wait. Do not start processing until they signal they are done — either explicitly or by stopping.

If the input arrives via voice-to-text, apply the same charitable interpretation principles as the voice-input-processor skill: correct likely substitution errors, read for intent, do not flag surface errors.

---

## Step 2 — Ask One Question

Before organising, ask:

> "Do you want me to just organise this so it is clearer, or would you also like help working out what to tackle first and how to get started?"

Present this as two clear options:
- **Just organise** — structure and clarity, no prioritisation added
- **Help getting started** — structure plus concrete next steps and a clear first action

Do not explain the options at length. Do not ask anything else. Wait for their answer before proceeding.

---

## Step 3 — Find the Themes First

Before doing anything else, read the entire input and identify the underlying themes or projects running through it. People doing a brain dump often jump between topics mid-sentence — your job is to spot what belongs together before organising anything.

Ask yourself: what are the distinct areas of life, work, or projects mentioned? These become your top-level groups.

For example, if someone mentions a work project deadline, a personal admin task, a home project, and some errands — those are four distinct themes, not four tasks. Everything else in the dump belongs to one of those themes.

**This grouping step is the most important part of the skill. Do it before categorising anything as a task, worry, or idea.**

Then within each theme, separate:

- **To do** — things that still need doing
- **In progress / already done** — things underway or completed (do not list these as tasks)
- **Worries or blockers** — concerns sitting around this theme
- **Context** — useful background that informs the theme

Some items will fit more than one theme. Use judgement — place them where most useful and note the connection if relevant.

---

## Step 4a — Output: Just Organise

Produce a structured summary grouped by theme first, content type within each theme second. No prioritisation, no advice, no next steps — just the clarity of like with like.

```
## [Theme 1 — e.g. Project or area name]
**To do:**
- [Task]
- [Task]

**In progress / done:**
- [Thing already underway or completed]

**Worth noting:**
- [Context or blocker]

---

## [Theme 2]
**To do:**
- [Task]

**Worth noting:**
- [Context]
```

Rules for this output:
- Every item sits under a theme — nothing floats as a standalone bullet
- Do not list completed or in-progress items as tasks
- Keep each item to one line where possible
- Preserve the user's language — do not rewrite what they said
- If two themes are connected, note it briefly under the relevant one

Close with:
> "Does that feel clearer? I can help you work through any of these sections, or produce a printable plan if that would be useful."

---

## Step 4b — Output: Help Getting Started

Produce the same theme-grouped structure as Step 4a, then add the following.

### Surface One Clear Next Action

Before the grouped output, identify the single most pressing or most actionable item across all themes and surface it at the top:

```
## Your one next step
[One specific, concrete action — not a theme, not a project, one thing]
```

This should be:
- **Specific** — not "sort out the project" but "open the project doc and write the first two bullet points"
- **Small** — the smallest possible first step, not the whole task
- **Immediate** — something that can be started now or at a defined time

### Add Concrete First Steps to Tasks

For each task, add a first step in plain language beneath it:

```
## Tasks
- [Task 1]
  → First step: [Specific, small, concrete action]
- [Task 2]
  → First step: [Specific, small, concrete action]
```

First steps should:
- Take no more than two minutes to start
- Be physical and specific — open, write, call, send, find
- Include a when and where if the task is time-sensitive: "Email Sarah at 9am from your desk"
- Never use vague language like "think about", "look into", or "sort out"

### Handle Emotionally Loaded Tasks

If a task appears to carry emotional weight — avoidance language, dread, repeated mentions, or explicit anxiety — flag it plainly and gently:

```
- [Task] *(this one might feel harder to start)*
  → First step: [The smallest possible entry point]
```

Do not explain why it might feel hard. Do not offer therapy. Just acknowledge it and make the first step smaller than usual.

### Acknowledge Worries Separately

Do not turn worries into tasks unless the user has indicated they want to act on them. Simply acknowledge them:

```
## Worries
These are sitting with you right now. They do not all need solving today.
- [Worry 1]
- [Worry 2]
```

If a worry has a corresponding task, note the connection briefly: *(linked to: [task name])*

### Replace Vague Timing with Specific Dates

Any task described as "later", "soon", or "at some point" should have vague timing replaced with a prompt:

```
- [Task] *(when specifically? — pick a day)*
```

Do not assign a date on the user's behalf. Flag it so they can decide.

Close with:
> "Does that feel more manageable? I can adjust any of these, go deeper on a section, or produce a printable action plan if that would help."

---

## Step 5 — Offer the Printable Plan (Optional)

If the user wants a printable plan, or if the output is complex enough that a document would be more useful than a conversation, offer to produce one:

> "I can turn this into a clean printable plan — a single page you can follow and tick off. Would that be useful?"

If yes, produce a PDF using the pdf skill with the following structure:

- **Header** — date and a neutral title ("Your Plan" or similar — not "Brain Dump")
- **Your one next step** — large and clear at the top
- **Tasks with first steps** — clean list, tickable
- **Worries** — brief section, acknowledged not actioned
- **Ideas to come back to** — captured at the bottom so nothing is lost
- **Decisions pending** — flagged clearly

The document should be clean, minimal, and printable on a single A4 page where possible. White space is not wasted space — it reduces cognitive load.

---

## What This Skill Does Not Do

This skill organises and structures. It does not solve problems, make decisions, or tell the user how to feel about what they have shared.

It does not add tasks that were not in the original input. It does not remove worries because they seem irrational. It does not prioritise on the user's behalf without being asked.

It does not replace talking to someone. If the content of a brain dump suggests the user is in significant distress, acknowledge that gently and note that talking to someone they trust may help alongside any practical steps.
