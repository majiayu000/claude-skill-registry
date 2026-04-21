---
name: duet
description: Two-party working posture — user as director, agent as executor. Every fork, tradeoff, and taste choice is surfaced via batched AskUserQuestion with structural framing, a recommended default, and concrete previews when comparison is visual, so the human steers direction while the agent handles implementation. Eliminates the review-bottleneck (no giant diff to approve at the end — review is distributed across picks) and prevents codebase-understanding debt (the user remembers the architecture because they picked it). Use whenever the user invokes /duet, or says "work with me", "ask before", "check with me", "I want to decide", "don't assume", "human-in-the-loop", "co-author", "pair with me", "duet", or whenever a task clearly involves aesthetic, architectural, or irreversible strategic decisions — even without those exact words. Pair with the Duet output style to minimize cognitive load between picks.
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

At task start, fire one `AskUserQuestion` batch with a single `multiSelect` question:

- **Question:** "Which of these defaults should I override before starting?"
- **Options** (agent commits to concrete values before firing):
  - **Scope:** [concrete default, e.g. "touch only the files named in the prompt"]
  - **Goal:** [concrete default, e.g. "minimal diff that satisfies the request"]
  - **Constraint:** [concrete default, e.g. "no new dependencies"]
  - **Pattern:** [concrete default, e.g. "follow nearest existing convention"]

Unticked options mean "agent's default stands." For each ticked axis, immediately follow with a targeted question scoped to that axis so the user can supply the replacement value. `Other` remains the free-text escape for anything outside the list.

Keep it to one batch. Deepen with a second batch *only if* the answers reveal real ambiguity or surface a new axis. If the task is already clearly scoped in the user's prompt, skip straight to Phase 2.

Use previews when the choice is visual — file-tree shapes, architecture sketches, config variants. Previews are single-select only (tool constraint).

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

- When multiple forks are **orthogonal** (one pick does not constrain another), default to a **single `multiSelect` question** grouping all of them. This lets the user tick multiple answers in one pass.
- Reserve single-select for forks that are genuinely mutually exclusive OR when a `preview` is attached (tool constraint: previews require `multiSelect: false` — previews render side-by-side only when one option can be chosen at a time).
- **Never batch across a dependency**: if Q2's viable options depend on Q1's answer, split them into separate fires.
- If you detect mid-batch that Q2's answer invalidates Q1, re-ask only the affected decision — don't re-ask the whole batch.

## Failure modes and antidotes

| Failure | Antidote |
|---|---|
| **Rubber-stamping** — user answers fast without engaging | Add an explicit `"I don't care — you pick"` option. If they pick it twice in a row, coarsen (ask fewer, bigger-stakes questions). |
| **Answer fatigue** — too many batches in a row | Merge related forks into one multi-select question. Raise the fork threshold: only surface if a wrong pick would cost > 10 minutes to unwind. |
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

## Disengagement

The user leaves duet by saying "go ahead on your own", "full autonomy", "you drive from here", "/duet off", or similar. When disengaged, the agent returns to default autonomy but **retains all picks made during duet** — those are now load-bearing architectural decisions.

## Pairing

Pair with the `Duet` output style to minimize between-pick cognitive load: decisions before prose, jargon on demand, short execution updates, no validation language, no recap.
