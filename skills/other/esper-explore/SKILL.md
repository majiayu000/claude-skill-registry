---
name: esper:explore
description: Explore an idea before committing to a plan. Investigates feasibility, trade-offs, and approaches — codebase-aware or open-ended brainstorming. Saves findings to .esper/explorations/ for future /esper:phase intake.
---

You are exploring an idea before it becomes a plan.

The user's initial prompt (if any): $ARGUMENTS

## Step 1: Check setup

Run `esperkit config check`. If it exits non-zero, tell the user to run `/esper:init` first and stop.

Run `esperkit config get current_phase` to get the current phase slug. Read `.esper/CONSTITUTION.md` and `.esper/phases/<current_phase>.md` to understand the project's scope and current phase goals.

## Step 2: Interview

Use `AskUserQuestion` to understand what the user wants to explore. Skip questions already answered by `$ARGUMENTS`:

- What idea, feature, or question do you want to explore?
- What mode: codebase-aware exploration (grounded in the actual code), open-ended brainstorming (discuss trade-offs and alternatives), or both?

Keep it light — this is exploration, not planning. One round of questions is enough.

## Step 3: Explore

**Codebase-aware mode** — use the Task tool with `subagent_type: "Explore"` to search the codebase:

```
Find existing files and patterns relevant to [idea being explored].
Look for similar features already implemented.
Identify potential conflicts, dependencies, or constraints.
Assess feasibility given the current architecture.
Return a concise summary — do not include full file contents.
```

Cross-reference findings against `.esper/CONSTITUTION.md` to flag any conflicts with project principles.

**Brainstorm mode** — discuss the idea conversationally:

- What are the possible approaches?
- What are the trade-offs of each?
- What are the risks and unknowns?
- Are there simpler alternatives?

**Both mode** — do codebase exploration first, then brainstorm with the findings as context.

## Step 4: Summarize findings

Synthesize everything into a structured markdown document:

```markdown
---
id: NNN
title: [exploration title]
created: [today YYYY-MM-DD]
mode: [codebase | brainstorm | both]
---

# Exploration: [title]

## Question
[What was being explored and why]

## Findings
[Key discoveries from codebase exploration and/or brainstorming]

## Feasibility
[Assessment: straightforward / moderate / complex / not feasible]
[Key constraints or blockers]

## Approaches
[Possible implementation approaches with trade-offs]

## Recommendation
[What to do next: proceed to /esper:plan, file a /esper:fix, defer, or abandon]
```

## Step 5: Save

Run `esperkit exploration next-id` to get the next available ID.

Write the exploration doc to `.esper/explorations/NNN-slug.md`.

Print:
- Exploration saved: `.esper/explorations/NNN-slug.md`
- Next steps based on the recommendation:
  - To formalize into a plan: `/esper:plan`
  - To log a bug fix: `/esper:fix`
  - To defer: no action needed — explorations are surfaced during `/esper:phase` when defining the next phase
