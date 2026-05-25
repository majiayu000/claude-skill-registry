---
name: intent
description: Turn rough ideas into clear work orders before planning or building. Use when request is vague like "add a button", "make it better", "fix the thing". Triggers on ambiguous or underspecified requests. Produces a brief with scope, acceptance criteria, and stop conditions.
---

Clarify WHAT before building anything. Every criterion must be testable by a stranger. Clarity over completeness — a partial spec with boolean criteria beats a thorough spec with vague ones.

A brief with invented details is worse than a shorter brief grounded in what the user said — assumptions compound silently downstream.

## Workflow

### Step 1: Understand

State what you heard in 1-2 sentences. If the task arrives with structured input (proposal, design, specs, task list), extract and validate — don't re-clarify.

### Step 2: Close gaps

Loop using AskUserQuestion — up to 3 questions per round, max 8 rounds. At least one question across all rounds should be "what should this NOT do?"

After each round, list remaining unknowns — things you'd have to invent if you wrote the brief right now. If the list is non-empty, ask another round targeting those unknowns. If empty, move to step 3.

### Step 3: Echo

Compress to one sentence (≤35 words): deliverable + top constraint.

Use AskUserQuestion to confirm:
- **Lock it in** — proceed to assumptions review
- **Edit something** — revise, then re-echo
- **Explore risks** — surface failure scenarios, then return to this choice

### Step 4: Review assumptions

Before generating the brief, list every detail you would need to invent — things the user never stated (numbers, thresholds, scope boundaries, tech choices).

Present each assumption via AskUserQuestion with "Accept" and 2-3 concrete alternatives. Batch unrelated assumptions together, separate dependent ones.

If there are zero assumptions, skip to step 5.

### Step 5: Recommended practices

If the task is straightforward with clear precedent, skip to step 6.

Present best practices, thresholds, and standards the agent would add beyond what the user stated. Each with a one-line rationale explaining why it matters.

Use AskUserQuestion (multiSelect) so the user can cherry-pick which to promote into acceptance criteria. Selected items become acceptance criteria in the brief. Unselected items stay in a "Recommended Practices" section as suggestions.

### Step 6: Emit brief

Only after steps 4 and 5 are complete. The core brief contains only what came from the user or was approved in steps 4-5. Scale sections to task stakes — a small fix doesn't need 5 non-goals.

Structure:
- OBJECTIVE (1 line)
- NON-GOALS (3-5)
- CONSTRAINTS
- ACCEPTANCE — only criteria from user answers (step 2), approved assumptions (step 4), or promoted practices (step 5). A shorter honest list beats a padded one.
- STOP CONDITIONS (3-5 observable failures)
- RECOMMENDED PRACTICES — unselected items from step 5, kept as suggestions for reference.

## Boundaries

User owns intent. If they say "I know what I want," proceed without clarification. When interpretations diverge, present options — never pick for them.
