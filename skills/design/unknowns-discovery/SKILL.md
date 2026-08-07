---
name: unknowns-discovery
description: Discover and reduce task unknowns — blindspots, missing context, and unknown unknowns — before committing to a plan, implementation, review, or merge.
---

# Unknowns Discovery

Use this skill when an agent should **discover what the user, spec, prompt, or codebase is missing** before it commits to a plan, implementation, review, or merge.

The prompt, skill, ticket, screenshot, and context window are the **map**. The real codebase, product, users, data, constraints, history, and reviewer expectations are the **territory**. The gap between them is the task's **unknowns**.

## Unknown types

| Type | Meaning | Agent move |
|---|---|---|
| Known knowns | Explicit facts and constraints in the prompt | Preserve and restate briefly |
| Known unknowns | Questions already recognized as open | Ask, research, parameterize, or gate |
| Unknown knowns | Tacit standards the user would recognize only after seeing them | Prototype, mock, compare, or interview |
| Unknown unknowns | Hidden constraints, missing vocabulary, prior art, traps, or quality ceilings nobody mentioned | Run blindspot passes, inspect references, search code/history, and surface landmines |

## When to activate

Activate this skill when any of these are true:

- The work is multi-step, ambiguous, unfamiliar, high-risk, or likely to require judgment.
- The user mentions “blindspot pass,” “unknown unknowns,” “what am I missing,” “interview me,” “prototype first,” “implementation notes,” “buy-in doc,” “quiz me,” or similar.
- The user lacks domain vocabulary or does not know what good looks like.
- The task involves codebase history, architecture, data model, permissions, migrations, UX, visual design, product scope, rollout, or reviewer approval.
- The agent is about to start a long-horizon implementation or has already discovered that the plan and codebase disagree.

Do **not** activate for tiny deterministic tasks where exploration would add friction, such as fixing a typo, renaming a variable, or answering a direct question with no meaningful unknowns.

## Core loop

1. **State the map.** Restate the task, constraints, and what the user says they know.
2. **Inspect the territory.** Read relevant files, docs, examples, data, screenshots, references, prior work, or user-provided context.
3. **Build an unknowns matrix.** Separate known knowns, known unknowns, unknown knowns, and unknown unknowns.
4. **Choose the cheapest useful artifact.** Pick the mode that exposes the highest-blast-radius unknown earliest.
5. **Gate implementation.** Proceed only when dangerous unknowns are resolved, explicitly accepted, or isolated behind reversible decisions.
6. **Carry discoveries forward.** Fold the discoveries into a better prompt, plan, implementation note, buy-in doc, quiz, tests, or review artifact.

## Artifact mode selector

| Mode | Use when | Output |
|---|---|---|
| `blindspot-pass` | Unfamiliar codebase/domain/design area; likely unknown unknowns | Blindspot cards + better implementation prompt |
| `teach-me-my-unknowns` | User lacks vocabulary or quality criteria | Mental model + vocabulary ladder + improved prompts |
| `brainstorm-prototype` | User will know it when they see it | Divergent prototypes/options + reaction template |
| `mock-before-wire` | Need to see UI/flow before backend/state/app changes | Throwaway mock with fake data + wiring plan |
| `option-space-brainstorm` | Problem framing may be too narrow or too wide | Ranked interventions from cheapest to ambitious |
| `one-question-interview` | Ambiguity remains after exploration | One question at a time, ordered by blast radius |
| `reference-semantics-map` | Existing code/design/doc is the best description | Semantics map before porting/adapting |
| `tweakable-plan` | Ready to implement but human should review change-prone parts | Plan sorted by likely human-tweak points before execution order |
| `implementation-notes` | Implementation is underway and surprises appear | Running log of deviations and conservative choices |
| `buy-in-doc` | Work needs approval or stakeholder alignment | Demo-first pitch/explainer with objections and signoffs |
| `merge-readiness-quiz` | Human must understand a complex change before merge/release | Report + quiz with pass criteria |

Detailed procedures are in [references/WORKFLOWS.md](references/WORKFLOWS.md). Copyable prompt cards are in [references/PROMPT_PATTERNS.md](references/PROMPT_PATTERNS.md). Output schemas are in [references/OUTPUT_SCHEMAS.md](references/OUTPUT_SCHEMAS.md).

## Default output contract

Every unknowns artifact should include:

1. **Scope read:** What was inspected or assumed.
2. **Unknowns found:** Labels by unknown type and severity.
3. **Blast radius:** What changes if this unknown is answered differently.
4. **Conservative default:** What the agent will do if forced to proceed.
5. **Decision needed:** What the user must choose, if anything.
6. **Prompt upgrade:** A revised prompt/instruction incorporating discoveries.
7. **Stop conditions:** Cases where guessing is unacceptable.

## Autonomy rules

- Ask before acting when an unknown can change architecture, data model, auth, privacy, compliance, cost, public API, migration, rollout, or user-facing behavior.
- Proceed conservatively when the unknown is low-risk, reversible, and the user has asked not to be interrupted. Label assumptions as `ASSUMED`.
- Prototype before wiring when feedback depends on taste, layout, copy tone, interaction flow, information architecture, or data density.
- Prefer source references over prose when behavior already exists elsewhere.
- During implementation, log every material deviation before continuing.
- Do not merge complex agent work on diff-skimming alone; create a report and quiz if understanding matters.

## Stop immediately when

- The territory contradicts the task goal.
- The unknown could cause data loss, auth bypass, privacy leak, billing impact, destructive migration, public API break, or compliance failure.
- A prior failed/reverted attempt appears and the reason still applies.
- Exact legal/security/compliance behavior is requested but the authoritative source is absent.

## Minimal examples

```text
Do a blindspot pass before implementation. Find unknown unknowns, explain why each matters, and rewrite my prompt with the discoveries folded in.
```

```text
Before touching the app, make a single HTML mock with fake data so I can react to layout and product decisions.
```

```text
Keep implementation-notes.md as you build. If code forces a plan deviation, choose the conservative option, log it under Deviations, and continue unless it affects security/data/migrations/API/compliance.
```

```text
Give me a merge-readiness report with a quiz at the bottom. I should not merge until I pass it perfectly.
```

## Packaged resources

- [references/ARTICLE_DIGEST.md](references/ARTICLE_DIGEST.md) — faithful extracted digest of the supplied article.
- [references/WORKFLOWS.md](references/WORKFLOWS.md) — detailed procedure for each artifact mode.
- [references/PROMPT_PATTERNS.md](references/PROMPT_PATTERNS.md) — reusable prompt cards.
- [references/OUTPUT_SCHEMAS.md](references/OUTPUT_SCHEMAS.md) — artifact schemas and gates.
- [references/EVALUATION.md](references/EVALUATION.md) — eval prompts and quality rubrics.
- [references/SOURCE_INDEX.md](references/SOURCE_INDEX.md) — source and format references.
- [assets/templates/](assets/templates/) — reusable Markdown templates.
- [examples/](examples/) — example applications across coding, product/design, and research.
- [scripts/](scripts/) — optional helper scripts for template generation and validation.
