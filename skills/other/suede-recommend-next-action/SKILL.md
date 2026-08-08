---
name: suede-recommend-next-action
description: "Next-action selector for this pack: reads current repo, terminal, plan, or handoff state, scores 2-4 candidate moves against goal alignment, unblocking, evidence, urgency, and leverage, and returns one recommended action plus a short, self-contained copy/paste prompt — expanding into a full operator prompt or granular steps only on request. Use when the user asks 'what's next', 'what should I do next', 'recommend the next move', 'give me the prompt', 'expand prompt', or 'make it granular', especially after a review, audit, plan, or stalled task. NOT FOR: executing the recommended action without the user's separate authorization, or coordinating a multi-lane build across specialists (use suede-agent-teams)."
---

# Suede Recommend Next Action

Recommend one action and package it as a short runnable prompt. Inspect
current state read-only; do not execute the recommended action unless the
user separately authorizes execution. Keep the full operator contract hidden
until the user asks to expand it.

## Recommendation Workflow

1. Resolve the target and the user's actual done outcome from the current
   request, conversation, handoff, plan, repo, or live surface.
2. Check only the evidence needed to distinguish the next move. Prefer, in
   order: current terminal/repo/live state, current source documents, current
   plans or handoffs, then older memory.
3. Generate 2-4 candidate actions internally. Exclude work already verified as
   complete, adjacent cleanup, and actions outside the user's authorized scope.
4. Score each candidate from 0-2 on every criterion below. Recommend the
   highest total.

| Criterion | 2 points | 1 point | 0 points |
|---|---|---|---|
| Goal alignment | Directly produces the user's done signal | Required prerequisite | Merely adjacent |
| Unblocking | Unlocks a core path or at least two downstream steps | Unlocks one step | Unlocks nothing known |
| Evidence | Confirmed by current source | Confirmable with one read-only check | Depends on an assumption |
| Urgency | Active failure, deadline, security risk, or release gate | Needed for the active milestone | No current pressure |
| Leverage | Fits one focused session and prevents rework or creates a reusable result | Bounded work with moderate payoff | Unscoped, multi-day, or low-payoff work |

5. Break ties by preferring a required prerequisite, then current-evidence
   verification, then the more reversible action. If the top two remain within
   one point and target ambiguity would change the answer, run at most three
   additional read-only checks. If still tied, show both choices and state the
   single fact that decides between them.
6. Turn the recommendation into a 2-4 sentence quick prompt. Keep the scoring
   and full operator contract internal unless the user asks to compare choices,
   `expand prompt`, or `make it granular`.

## Routing Rules

- If a repo or task already has its own plan, progress doc, issue tracker, or
  project board, do not create a second one. Treat its recorded next step as
  one candidate, verify it against current source, and recommend the winner —
  don't replace the existing tracker.
- If the user needs options explored before a commitment can be made, say so
  and offer to brainstorm instead of forcing a single recommendation.
- If missing evidence is the real blocker, make the smallest read-only check
  the recommended action and generate a prompt for that check.

## Prompt Levels

### Quick Prompt (Default)

Write 2-4 sentences that another capable agent can paste and run:

1. Name the selected skill or lane, exact target, and one concrete outcome.
2. Include the single current fact, scope boundary, or preservation rule most
   likely to change execution.
3. Name the observable done signal and its verification.
4. Add a stop condition only when a material blocker is plausible.

Do not dump field labels, the score breakdown, a long evidence list, or numbered
implementation steps by default. After the prompt, add exactly:

```text
Say "expand prompt" for the full operator version or "make it granular" for exact steps and commands.
```

### Expanded Prompt (On Request)

When the user says `expand prompt`, render the full self-contained prompt below.
Include only applicable fields and never leave placeholders such as `TBD` or
`<path>`.

```text
Use $<skill> to complete this task.

Target: <exact repo, worktree, route, URL, document, account, or surface>
Objective: <one concrete outcome>
Current verified state:
- <fresh fact and its source>
Authorized scope: <read-only, local edits, live mutation, or other exact boundary>
Preserve: <dirty work, copy, data, identities, or other invariants>
Source-truth order: <current sources in precedence order>

Required work:
1. <smallest complete sequence>

Done signal: <observable proof>
Verification:
- <command, readback, screenshot, URL, test, or response>
Stop and report if: <material ambiguity, unsafe mutation, failed gate, or missing authority>

Return: outcome, changed surfaces, verification evidence, caveats, and status.
```

### Granular Prompt (On Request)

When the user says `make it granular`, render the expanded prompt and decompose
`Required work` into atomic numbered steps. Include exact commands, absolute
paths, mutation checkpoints, expected readbacks, and stop conditions wherever
current evidence supports them. Do not invent missing commands or values; make
resolving a missing decisive fact the first step.

For multi-lane work spanning more than one specialist, start expanded and
granular prompts with `$suede-agent-teams` so the coordination lane owns the
handoff. For a single-lane task, start with the specialist the recommendation
names directly. Use exact absolute paths, URLs, handles, branch names, and
verification commands when current evidence provides them.

## Output Format

```text
Recommended action: <one sentence>
Why now: <one evidence-backed sentence>

Quick prompt: <2-4 runnable sentences>

Say "expand prompt" for the full operator version or "make it granular" for exact steps and commands.
```

Show the route, score, evidence list, confidence, or alternatives only when the
user asks for rationale or when the unresolved tie rule requires them. When the
recommendation is an evidence-gathering step, state that in `Why now` without
loading the expanded prompt.

## Boundaries

- Do not mutate files, repos, deployments, accounts, messages, or live systems
  while recommending.
- Do not load the expanded or granular prompt by default.
- Do not repeat a broad audit when one current execution lane can be selected.
- Do not invent paths, URLs, skill availability, status, metrics, owners, or
  completion evidence.
- Do not recommend vague actions such as "keep working", "improve the app", or
  "do more research". Name a command, artifact, decision, edit, or verification
  result.
- Do not hide a blocker. If authority or a decisive fact is missing, make its
  resolution the next action.

## Routing

- Need multi-lane coordination across specialists -> use `suede-agent-teams`.
- Need help picking which single skill fits a request -> read this pack's
  router (`suede-workflow-skills`) or ask directly.
- Need idea exploration before selecting a move -> brainstorm directly with
  the user instead of forcing a single recommendation.
- Need execution -> use the specialist named in the generated prompt.
