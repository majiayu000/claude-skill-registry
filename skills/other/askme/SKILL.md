---
name: askme
description: 'Use when a task is ambiguous, maximum clarification is needed before planning, or the user requests exhaustive, collaborative, or adversarial askme mode. Runs Verbalized Sampling, fires batched clarifying questions, and confirms intent before planning proceeds. Not for source or remote-system changes; not for a single fork — use decide.'
---

# Ask me

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Ambiguous task, maximum clarification needed, or explicit exhaustive/collaborative/adversarial askme mode. |
| Authority | Read-only: no file, VCS, credential, paid, published, deployed, or remote mutation. Emits chat output only. |
| Side effect | Verbalized Sampling output and batched question sets written to chat; nothing persisted. |
| Done | Every clarifying question is answered or discharged and intent is confirmed. |

## Inputs

- The user's task or request (required).
- Optional mode argument: `exhaustive` (default), `collaborative`, or `adversarial`. Auto-detected from invoking phrasing; an explicit mode argument always overrides auto-detection. Callers with no mode arg get `exhaustive`.
- An ask-user tool exposing single-select and multi-select questions (the harness equivalent of `AskUserQuestion`). Required to fire question batches; if absent, fall back to sequential chat prompts.

## Procedure

1. **Select mode.** Auto-detect from invoking phrasing: `help me refine`, `walk through with me`, `let's brainstorm`, `share tips` → collaborative; `poke holes`, `stress-test`, `grill`, `find weaknesses` → adversarial; anything else or no qualifier → exhaustive. An explicit mode argument always wins over auto-detection.

2. **exhaustive mode — Verbalized Sampling (VS).** Sample multiple intent hypotheses; assign each a probability weight on a 0–1 scale; state the falsifier (the specific observation or scenario that would invalidate it) per hypothesis. Expand hypothesis depth as ambiguity, risk, or architectural surface grows; keep it concise when scope is truly narrow. Render the VS block in this format before the first question fire:
```
1. [Weight: 0.42] hypothesis here
   - Falsifier: [observation or scenario that would invalidate this]

2. [Weight: 0.28] hypothesis here
   - Falsifier: [observation or scenario that would invalidate this]
```

3. **exhaustive mode — exploration.** Deliberately seek unconventional, underexplored, and edge-case possibilities relating to the user's objective, drawing on context and plausible but non-obvious requirements. Include at least 3 edge cases (at least 5 if architectural); stop expanding once additional cases no longer change decisions. Broaden sampling if no clear leader emerges. Synthesize surviving hypotheses into one consolidated direction before responding.

4. **collaborative mode.** Do not run VS. Two-way tip-sharing dialogue: surface one of the agent's own observations or tips back to the user as a counter-tip per round; let depth emerge through exchange. No scoring, no ranked sample. Stop when the user signals convergence.

5. **adversarial mode.** Run VS once at the start to map the design tree, then walk the tree one fork at a time. Per fork: state the question, recommend an answer with a one-sentence rationale, wait for the user, and do not proceed on assumed answers. Resolve dependencies parents-first; do not descend into children while a parent is unresolved.

6. **Escalation (collaborative → adversarial).** Promote mid-session when any of these fire: (a) ambiguity cardinality ≥ 2 valid architectural decisions surface from a single user message; (b) the user references "the function" / "that file" without a concrete path; (c) the user describes a goal without a verifiable done signal. These signal patterns are guidance, not a hard rule; the user can always override mode via argument.

7. **Fire clarifying questions via the ask-user tool.** The "maximum possible number" is bounded by the tool's per-fire cap (4); for larger sets fire multiple sequential batches ordered by dependency. Per question: a full sentence ending in `?`; a `header` chip ≤ 12 characters; `multiSelect` false for single-pick mutually-exclusive axes, true only for additive subset picks (feature toggles, optional sub-tasks). Per option: a 1–5 word `label` with `(Recommended)` appended to and placed first for the recommended choice; a one-sentence trade-off `description`; an optional `preview` (markdown or monospace box) for visual comparisons, single-select only, skipped when the difference is purely conceptual. Never add an explicit "Other" option — free-text "Other" is auto-provided on every question, and free-text notes go in the `annotations` response field. Use this tool only to clarify requirements or choose between approaches during planning, not to ask "is the plan ready?".

8. **Antipattern — never generate an override-checklist.** Never emit a single `multiSelect: true` checklist where unticked means "default stands"; it collapses independent axes into one list. When the brief calls for the user to rarely have to type, route the intent into N per-axis single-select questions (≤ 4 per fire), each axis's `(Recommended)` option carrying the default. Reserve `multiSelect` strictly for additive picks.

9. **VS render timing.** Render the VS block immediately before the first question fire of a planning session; subsequent intra-session fires need not repeat the VS preamble unless the survivor set materially changed.

10. **Harness mapping.** If the harness exposes only single-question prompts, fire them sequentially in dependency order — the shape (clarifying questions with one Recommended each) is what matters, and batching is an optimization. Map `(Recommended)` to whatever default-marker convention the harness uses; the rationale belongs in the description body either way. If no multi-pick mechanism exists, decompose additive picks into N independent single-selects.

11. **Stop.** Terminate when every clarifying question is answered or discharged and intent is confirmed. Do not proceed on non-trivial changes without visible VS (exhaustive) or completed fork resolution (adversarial).

## Failure and recovery
- Unresolved fork / blocking unknown (adversarial): stop; report the blocking unknown and the unresolved fork. Do not assume an answer or descend into children.
- No clear leader after broadened sampling (exhaustive): broaden sampling further or surface the decision point with concrete options and trade-offs. Do not silently pick.
- User refuses to answer or signals non-convergence: record the discharged questions and the open ambiguity. Do not pretend intent is confirmed.
- Ask-user tool unavailable: fall back to sequential single-question chat prompts in dependency order; if no question tool exists at all, emit the question set as chat text and await replies.
- Partial-result rule: a partially answered batch is not done; re-fire only the unanswered axes, not the whole batch.
- Non-mutation rule: nothing is written to disk, VCS, credentials, or remote state at any point. Recovery is re-asking, never rollback. The blocked/non-converged result is an explicit list of open ambiguities and discharged questions, not a fabricated confirmation.

## Output
Chat output only: the VS block (exhaustive, or once at the start of adversarial), the batched question sets, and a terminal intent summary stating the consolidated direction, assumptions, and discharged questions. No file, persisted artifact, or state transition is produced.
