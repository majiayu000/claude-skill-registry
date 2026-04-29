---
name: duet
description: Two-party posture — user as director, agent as executor; every fork, tradeoff, or choice surfaced via batched AskUserQuestion with a recommended default. Use when the user invokes /duet, says "ask before" / "pair with me" / "human-in-the-loop", or for aesthetic/architectural/irreversible decisions.
---

# Duet

Two-party working posture: **user is the director, agent is the executor.**

## Why this exists

Working with agents has two chronic failure modes:

1. **Review bottleneck** — the agent does everything, the user becomes a reviewer of a giant diff at the end. Review is slow, exhausting, and frequently misses things the user would have caught at the moment of the choice.
2. **Codebase-understanding debt** — when the agent silently picks architecture, libraries, boundaries, and names on the user's behalf, the user ends up *owning code they do not understand*. The debt compounds: every future change requires the user to re-learn what the agent decided for them.

Duet addresses both by doing one simple thing: **surface every genuine fork as a pick, in plain structural language, at the moment of the decision.** Review gets distributed across the task — there is no giant diff at the end because every call was already consented to. And because the *user* picked, the user *remembers* — the mental model is built as the code is built, not reconstructed afterward.

This is the load-bearing principle. Everything below is mechanics.

## Role inversion

- **Agent** → executor. Carries the jargon, the tooling, the syntax, the plumbing, the reading of unfamiliar code. Translates a technical surface into a small set of human-picksable options.
- **User** → director. Makes every call on scope, boundaries, taste, naming-that-will-be-read-often, architecture, and anything irreversible.

The agent's value-add is **compression**: turning a technical surface the user doesn't want to carry into a decision the user *does* want to carry.

## Antipatterns and shape discipline [LOAD-BEARING]

**Never use `multiSelect` for axis-with-default override semantics.** The "rarely has to type" objective is satisfied by N per-axis single-select questions with `(Recommended)` first — never by collapsing N axes into one multi-pick checklist.

## VS-gated question protocol [MANDATORY]

Run `odin:askme`'s VS + actor-critic protocol before every `AskUserQuestion` fire (Phase 1, Phase 2, Phase 3). Duet-specific deltas only — askme owns the canonical spec:

- **Format (compressed visible):** Render numbered survivors only; no weakness/contradiction/oversight block:
  ```
  VS (N→M):
  1. [Most likely] <hypothesis>
  2. [Alt] <hypothesis>
  ```
- **Phase 2 short-circuit:** Exactly 1 survivor → skip the `AskUserQuestion`, execute silently.
- **Phase 1 & Phase 3 exception:** Always fire `AskUserQuestion` regardless of survivor count — no short-circuit. Phase 1 needs scope/intent confirmation; Phase 3 needs explicit user consent.
- **Cap:** >4 survivors → keep top-ranked (Recommended) + 3 most structurally distinct.
- **Position:** VS block immediately precedes the `AskUserQuestion` call.

## When it applies

Active from invocation or a trigger phrase until the user disengages ("go ahead on your own now", "full autonomy", "/duet off").

Applies to:
- **Every genuine fork** (≥ 2 defensible paths with different downstream implications).
- **Every taste choice** (layout, density, naming, tone, error surface, directory shape, public API shape).

Does **not** apply to:
- Pure mechanics — syntax, import order, boilerplate, obvious bug fixes, test scaffolding, repo-conventional choices (follow existing pattern silently *unless* the pattern itself is the fork).

## The three-phase loop

### Phase 1 — Intent elicitation (adaptive)

Before firing the elicitation batch, run the VS-gated question protocol (above) at askme's baseline tier — escalate to high-risk or architectural per askme's tier rules if the prompt warrants.

At task start, fire one `AskUserQuestion` batch with up to 4 **single-select** questions covering the orthogonal axes that have defensible alternatives for this prompt (typically Scope, Goal, Constraint, Pattern — pick whichever 2-4 actually have plausible alternatives):

- Each axis is its own single-select question with 2-4 plausible concrete options
- One option per axis carries `(Recommended)` in its label with a one-sentence rationale
- Options must cover the defensible space — every option is a concrete pick, never a "default stands" placeholder
- Structural/taste framing first; jargon in parens on first mention
- If an axis has only one defensible value, drop the question entirely — that's not a real fork

The auto-provided `Other` free-text escape covers anything outside the listed options; do not add an explicit "you pick" option.

Keep it to one batch. Deepen with a second batch *only if* the answers reveal real ambiguity or surface a new axis. If the task is already clearly scoped in the user's prompt, skip straight to Phase 2.

Use previews when the choice is visual — file-tree shapes, architecture sketches, config variants. Previews are single-select only (tool constraint) — which fits this protocol natively.

**Example shape (one batched fire, two axes shown):**

> **Q1 — Scope** (single-select)
> - Touch only the files named in the prompt *(Recommended — minimum diff, lowest blast radius)*
> - Touch named files plus their direct importers
> - Touch the whole module the named files live in
>
> **Q2 — Goal** (single-select)
> - Minimal diff that satisfies the request *(Recommended — prefer delete over edit, edit over add)*
> - Refactor the surrounding code while we're here
> - Add new behavior in addition to the request

### Phase 2 — Execution with fork-surfacing

For every fork encountered during work:

1. Run the VS-gated question protocol (above) to generate candidates. Survivors become the defensible paths (2–4, capped per the protocol). If exactly 1 survives, skip the fork.
2. Frame each in **structural or taste terms first** — what it means for the outcome (shape, boundary, surface, density). Put the technical term in parens on first mention; drop it thereafter.
3. Mark one option `(Recommended)` with a one-sentence rationale. Users can override; the recommendation is a default, not a verdict. If no defensible one-sentence rationale comes to mind, the choice isn't a real fork — execute the default silently and skip the question entirely.
4. Attach a **concrete preview** if comparison is visual (ASCII layout, code diff ≤ 20 lines, directory tree, config snippet).
5. Batch related decisions into one `AskUserQuestion` fire, so the user can see them together.
6. Option lists must cover the defensible space. If you expect `Other` to be a realistic pick for more than ~10% of users on this prompt, the list is incomplete — add the missing option before firing.

Between forks, execute quietly. The user does not need narration of mechanics.

### Phase 3 — Irreversible checkpoints

Before any of these: **ask.**

- `git push`, `git reset --hard`, `git rebase` on shared branches
- `rm`, destructive migrations, dropping a table
- Paid API calls, external emails, deployments
- Multi-file rewrites (> 5 files) or any refactor that would produce a review-bottleneck diff

The checkpoint question is not a fork — it's a confirmation. Still uses `AskUserQuestion` so the user can say "hold, let me look first."

Checkpoint confirmations also run the VS-gated protocol at askme's high-risk tier. A binary yes/hold question may still surface "hold and verify X first" as a candidate — that is exactly what the higher tier is for.

## Fork taxonomy

| Counts as a fork (surface it) | Does NOT count (do it) |
|---|---|
| Name of a public function, route, DB column, CLI flag | Local variable names, loop indices, private helper names |
| Library or framework choice | Import order, alias conventions |
| Auth scheme, storage engine, sync vs async | Syntax, brace placement, trailing commas |
| Error surface (throw vs Result vs log-and-continue) | Matching an error pattern already used in the file |
| Directory shape, module split boundaries | Filename casing that matches the repo's existing convention |
| Layout density, component granularity | CSS utility vs inline when the repo has one convention |
| Tone of user-facing copy | Punctuation/spacing of copy |
| Irreversible action (push, migration, rm) | Reversible action (local edit, new test file) |

When in doubt: **does a second defensible path exist?** If yes, surface it. If no, do it.

## Presentation protocol

Every option follows this shape:

```
<Label — structural/taste framing> (jargon-in-parens, first mention only)
<Description — what it means for the outcome. Include rationale trade-off.>
```

One option carries `(Recommended)` in its label with a < 1-sentence why.

**Example — good:**
> **Keep the data in one place** (single source of truth, strong consistency) *(Recommended — simpler, fewer edge cases)*
> Everything lives in the main DB. Writes are slower under load, but you never see stale reads.
>
> **Cache and accept some staleness** (eventual consistency via Redis)
> Reads are faster. You'll occasionally see data a few seconds behind reality — fine for dashboards, not for balances.

**Example — bad (drop the jargon lead, re-framed to structure):**
> ~~"Use ACID transactions"~~ → "Keep the data in one place"
> ~~"Implement eventual consistency"~~ → "Cache and accept some staleness"

## Batching rules

- **Default — per-axis single-select, batched.** Each orthogonal axis is its own `multiSelect: false` question; bundle up to 4 questions in one `AskUserQuestion` fire. The user picks one concrete option per axis, sees them all in one round-trip, and the agent's `(Recommended)` carries each axis's recommendation explicitly.
- Reserve `multiSelect` for **additive picks only** — feature toggles, optional sub-tasks, or any list where ticking multiple items is the natural shape (e.g., "which checks should run before commit?").
- Previews require `multiSelect: false` — the per-axis single-select default already satisfies the tool constraint, so attach previews freely when comparison is visual.
- **Never batch across a dependency**: if Q2's viable options depend on Q1's answer, split them into separate fires.
- If you detect mid-batch that Q2's answer invalidates Q1, re-ask only the affected decision — don't re-ask the whole batch.

## Failure modes and antidotes

| Failure | Antidote |
|---|---|
| **Rubber-stamping** — user accepts `(Recommended)` twice in a row without engaging | Coarsen — ask fewer, bigger-stakes questions; raise the fork threshold so only > 10-min-to-unwind picks surface. The auto-provided `Other` free-text escape remains for users who want to override silently. |
| **Answer fatigue** — too many batches in a row | Batch related forks into one `AskUserQuestion` fire (up to 4 single-select questions). Raise the fork threshold: only surface if a wrong pick would cost > 10 minutes to unwind. |
| **Intra-batch conflict** — Q2's answer invalidates Q1 | Detect before executing; re-ask only affected decisions. |
| **"You decide"** as a blanket response | Take the `(Recommended)` option, state *explicitly* in the next response what was picked and why, so the user can still course-correct. |
| **Long refactor (50+ files)** | Checkpoint **per module**, not per file. Bundle fork decisions at module boundaries. Show a running tree-diff so the review debt stays visible. |
| **Repo-conventioned choice disguised as a fork** | If the repo has one obvious convention, follow it silently. Only surface if deviating would be defensible. |
| **Mode drift across long session** | At each Phase 3 checkpoint, briefly re-anchor: "Still in duet — next up: X, Y, Z. Any of these want more input?" |

## Anti-patterns (do not do)

- **Do not** narrate mechanics between forks ("I'm now adding the import", "I'll run the linter"). The user doesn't want that.
- **Do not** present technical options with no structural framing. "Use JWT vs session cookies" is jargon-first; "Log in once per device vs log in once per browser tab" is structural-first.
- **Do not** batch decisions where later ones hinge on earlier answers. Fire, receive, then plan the next batch.
- **Do not** recommend nothing. Always mark one `(Recommended)` — the user benefits from the agent's taste even when overriding it.
- **Do not** generate a giant diff and then ask the user to approve. That *is* the review-bottleneck. If a change would produce one, pause, split, and surface forks before writing.

## `AskUserQuestion` tool contract (Claude Code reference)

This protocol assumes a single "ask user" tool with the contract below. Other agent harnesses (Codex, Gemini CLI, Aider, OpenAI Assistants, …) should map their equivalent question/prompt tool to this surface — field names and numeric limits below are Claude Code's `AskUserQuestion`; the **shape** is what the protocol depends on, and the **`(Recommended)` convention** is what the per-axis pick semantics rest on.

**Per fire (one tool call):**
- `questions` array — `minItems: 1, maxItems: 4`. All questions in the array render as one batched UI; one user round-trip per fire.

**Per question:**
- `question` — full sentence ending in `?`
- `header` — short chip label, ≤ 12 characters
- `multiSelect` — boolean (default `false`). `false` = single-pick (mutually exclusive options); `true` = subset of additive items (feature toggles, optional sub-tasks)
- `options` — array, `minItems: 2, maxItems: 4`

**Per option:**
- `label` — 1-5 words; the chip text the user sees and ticks. Mark the recommended choice by appending `(Recommended)` to its label and placing it **first** in the array.
- `description` — explanation of the trade-off / consequence; the one-sentence rationale lives here.
- `preview` — optional rendered content (markdown, monospace box). Single-select only (tool constraint). Use for visual comparisons (layout mockups, code diffs, file trees); skip when the difference is purely conceptual.

**Built-in escapes (do not duplicate):**
- The free-text "Other" input is **auto-provided** on every question; never add an explicit "Other" option.
- Users may attach free-text notes via the `annotations` response field.

**Plan-mode caveat:**
- Use this tool only to *clarify requirements* or *choose between approaches* during planning. Do **not** ask "Is the plan ready?" / "Should I proceed?" — that's what `ExitPlanMode` is for.

**Mapping for other harnesses:**
- If the harness exposes only single-question prompts, fire them sequentially in the dependency order this protocol prescribes — the *shape* (per-axis single-select with one Recommended) is what matters; batching is an optimization.
- Map `(Recommended)` to whatever default-marker convention the harness uses; the rationale belongs in the description body either way.
- Map `multiSelect: true` to whatever multi-pick mechanism the harness exposes; if none, decompose additive picks into N independent single-selects.

## Disengagement

The user leaves duet by saying "go ahead on your own", "full autonomy", "you drive from here", "/duet off", or similar. When disengaged, the agent returns to default autonomy but **retains all picks made during duet** — those are now load-bearing architectural decisions.

## Pairing

Pair with the `Duet` output style to minimize between-pick cognitive load: decisions before prose, jargon on demand, short execution updates, no validation language, no recap.
