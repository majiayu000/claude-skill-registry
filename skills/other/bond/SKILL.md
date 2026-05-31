---
name: bond
description: Assesses team fitness and composes agent teams. Use when "set up a team", "team for this", "should I use agents", "design a team", "how many agents", "agent team".
---

Assess whether a task benefits from parallel agents. Most tasks are better solo. A team only pays off with genuine independence across modules.

## Presentation

- **Minto pyramid via AskUserQuestion** — Label = recommendation (conclusion first). Description = one-line tradeoff (always visible). Detail panel = structured plain text, short lines (~50 chars), ALL CAPS for section headers, dashes for bullets. No markdown in detail panels.
- **Minimal text between prompts** — One bold sentence framing, then AskUserQuestion. Nothing else.
- **Infer, state, ask only if ambiguous** — Assess fitness yourself. Present your assessment as a choice, not a question.

## Workflow

### Step 1: Assess

Read the task scope. Evaluate internally:
- Can workers operate without each other's output?
- Do they touch different files?
- Is scope multi-module (8+ story points)?

Search the codebase to identify module boundaries and file ownership zones.

If any answer is no on file independence, fitness = solo. If scope is 3 or fewer story points, fitness = solo. Otherwise, fitness = team.

Do not output assessment reasoning in any form — no headers, no bullet points, no labeled sections. Go straight to Step 2.

### Step 2: Choose mode

**One bold sentence stating your assessment**, then AskUserQuestion with three options:

- **Team (Recommended)** or **Solo (Recommended)** — whichever fitness determined. Label the recommended option. Description = one-line why.
  - Detail panel: module count, story point estimate, file independence summary
- **Solo** or **Team** — the non-recommended alternative.
  - Detail panel: what you gain and pay choosing this over the recommendation
- **Subagents** — sequential delegation, no parallelism.
  - Detail panel: when this fits (dependent steps, shared files, lower complexity)

If user picks Solo or Subagents, state the approach in one sentence. Done.

If user picks Team, proceed to Step 3.

### Step 3: Design roles

Identify 2-5 independent workstreams from the task. For each:
- Role name by responsibility (never generic)
- Owned files (no overlap between roles)
- Model: Opus for architecture/review, Sonnet for implementation, Haiku for research
- Task summary (1-2 lines)

Run coupling check internally: for each role pair, "if A changes X, does B break?" Merge roles where yes.

If coupling remains after merging, proceed to Step 4 before presenting. Otherwise skip to Step 5.

### Step 4: Surface coupling

**One bold sentence naming the coupling.** Then AskUserQuestion:

- **Merge [Role A + Role B]** — combine into one role.
  - Detail panel: shared files, why merging prevents conflicts
- **Coordinate** — keep separate with explicit handoff point.
  - Detail panel: handoff mechanism, sequencing, risk of drift
- **Redesign boundaries** — return to Step 3 with different file splits.

Repeat for each coupling pair. Then proceed to Step 5.

### Step 5: Present blueprint

**One bold sentence: "N roles, M workstreams, zero file overlap."** Then present roles via AskUserQuestion (multiSelect) so the user reviews all roles at once:

- Label: role name
- Description: owned files (short path list)
- Detail panel:

```
MODEL: [opus/sonnet/haiku]

OWNS:
  - path/to/files

TASK:
  - what this role builds

DEPENDS ON:
  - nothing / [specific handoff]
```

After user reviews, present a separate AskUserQuestion:
- **Approve and create** — proceed to Step 6
- **Adjust a role** — modify, then re-present
- **Cancel** — exit without creating

### Step 6: Create

If plan mode is active: write the team spec to the plan file — role names, owned files, models, tasks, spawn order, and sequencing constraints. State that creation will happen after plan approval. Done.

If not in plan mode:
1. Create team with TeamCreate
2. Spawn each role as an Agent with scope, owned files, and task from blueprint
3. Use persistent agent files when a role matches an existing agent

No output beyond confirmation that agents are running.

## Boundaries

User approves before any team is created. Bond assesses and recommends; user decides mode, roles, and boundaries. Bond asks only bond questions — scope, requirements, and approach belong to intent and shape.
