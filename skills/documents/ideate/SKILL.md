---
name: ideate
description: Grounded divergent idea generation — scan the codebase, generate many candidate directions across parallel generators, critique all behind a reject-by-default gate, and write the survivors plus the rejection rationale for the losers to docs/ideation/<slug>.md (markdown by default; an HTML view is opt-in via `format:html`). Use when the user says "let's brainstorm", "what should we build", "what should we build next", "any ideas for", or "/ideate". Generates candidate directions and routes the survivors onward to askme for intent-clarification; it does not clarify intent itself and does not plan.
metadata:
  short-description: Grounded divergent generation → survivors + rejection rationale → docs/ideation/
---

# Ideate — grounded divergent generation behind a reject-by-default gate

`ideate` turns a vague subject into a bounded set of candidate directions that survived critique, with the rejected candidates kept and explained rather than dropped. Flow: ground the subject in the real codebase (dispatch-first), generate many candidates across parallel generators, critique all, then write the survivors plus the rejection rationale for the losers. It writes one surface by default: the operating repo's `docs/ideation/<slug>.md`, markdown — always the canonical surface. The opt-in `format:html` flag additionally renders a human-reading HTML view derived from that markdown (`references/html-rendering.md`); it never replaces the markdown and never changes the default output. Idea selection is reject-by-default — a candidate earns a place by surviving the critique, never by default.

`Op:` of an ideate run is `extend` — a new ideation doc is a load-bearing capability added to the repo's decision record.

Adapted from EveryInc/compound-engineering-plugin (MIT).

## Auto-invoke

<auto_invoke>
<trigger_phrases>
- "let's brainstorm"
- "what should we build"
- "what should we build next"
- "any ideas for"
- "ideas for"
</trigger_phrases>
Fire automatically on a trigger phrase or on `/ideate`. The reject-by-default critique below still decides which candidates earn a place in the doc — auto-firing is permission to evaluate behind that gate, not permission to fabricate ideas to look productive. If the subject is unidentifiable, ask one clarifying question (or hand off to `askme`) and stop; do not generate against an unknown subject.
<manual_override>`/ideate [subject]` runs immediately without waiting for a trigger phrase. The remainder of `$ARGUMENTS` after stripping any leading flag is the subject. `ideate format:html [subject]` additionally renders the opt-in HTML view; the default stays markdown-only.</manual_override>
</auto_invoke>

## When to Apply

- The user opens with a brainstorm phrase, asks what to build, or invokes `/ideate` on a subject.
- The subject is divergent (many possible directions) and needs candidate generation before any one direction is chosen.
- A repo exists to ground the scan, or the subject names a concrete in-repo surface.

## When NOT to Apply

- **Intent on a single direction already in hand** — that is `askme`'s territory: it clarifies intent via Verbalized Sampling, it does not generate directions.
- **The anchor itself is in question** (what diagnosis / guiding policy the repo steers by) — that is `strategy`'s territory; `ideate` diverges *within* an anchor, it does not set one.
- **A direction is already chosen and needs implementation units** — that is `plan`. `ideate` stops at survivors plus an `askme` handoff; it never plans.
- **Subject unidentifiable after one clarifying question** — stop; do not generate against nothing.

## Support files — read on demand

Don't bulk-load at start. Read at the step that needs it; pass the relevant content into any subagent you spawn.

- `references/ideation-method.md` — the generate → critique → survivor-rationale method: the axis × frame divergence matrix, the verbatim generator and critic agent prompts, the survivor/rejection output schema, and the `docs/ideation/<slug>.md` section structure. Read at Phase 2 and Phase 5.
- `references/html-rendering.md` — how to render the canonical markdown to a self-contained HTML view. Read only when a run carries `format:html`.

## Workflow

### Phase 1 — Ground the scan (dispatch-first)

Ungrounded ideation is fabrication. Before generating, ground the subject in the real codebase. Defer to ODIN's Dispatch-First protocol — escalate Explore agents by scope: **1** for a single known concern, **3** for multiple concerns or unknown scope, **5** for a cross-module or architectural survey. Auto-skip to direct reads only for a single file under 50 LOC. **Seed the grounding scope with `STRATEGY.md`:** the grounding Explore agent(s) read it (when present at the repo root) as optional upstream grounding so candidates stay on-anchor, and fold its diagnosis/guiding-policy into the returned summary; if absent, note that in one line and proceed — strategy grounding never blocks. (In an auto-skip run, the orchestrator reads it directly.)

Explore agents are read-only and return architecture / pattern / constraint summaries with `file:line` cites. Use token-efficient discovery only: `fd -e <ext> --max-results 50`, `ast-grep run -p 'PATTERN' -l <lang> -C 1` or `git --no-pager grep -n -C 2 'pattern'`, preview with `bat -P -p -n -r START:END file`, structure with `eza --tree --level=2`. The output is a grounding summary every later candidate must cite against. If the scan cannot identify the subject, route to `askme` and stop.

### Phase 2 — Generate candidates (parallel, read-only)

Read `references/ideation-method.md`. Dispatch the generator subagents **in one tool-call message**, each seeded with the grounding summary and a **distinct axis × frame assignment** so they diverge instead of converging on the one salient reading. Each generator returns ~6–8 raw candidates, every candidate carrying a basis (`file:line` or `external:<source>`). Generators **write nothing**. Sequential dispatch invalidates the divergence contract.

### Phase 3 — Critique all (reject by default)

Dispatch a critic over the full raw candidate pool. **Every candidate is rejected by default**; it survives only by clearing the critique filters — grounded (the cited basis holds), feasible (buildable in this repo), non-duplicate (not a restatement of a peer survivor), load-bearing (the direction would change a decision). The critic tags each candidate `survive | reject` with a one-line reason. A rejection without a reason is invalid output.

### Phase 4 — Reviewer-gated merge

Dispatch a Reviewer subagent to audit the critic's verdicts against completeness / consistency / accuracy / scope. The Reviewer's output is the adjudicated set: the **survivors** and the **rejection rationale** for the losers. The Reviewer is the single adjudication authority — the orchestrator applies its set, does not rescue a rejected candidate, and does not re-litigate an accepted one.

### Phase 5 — Assemble and write

1. Build `docs/ideation/<slug>.md` per the section structure in `references/ideation-method.md`: subject + grounding summary, **Survivors** (each: idea, rationale, evidence cite), **Rejected** (each: idea + one-line rejection rationale — losers are explained, never silently dropped), and the next step. **Markdown is the canonical surface, always written.** Slug is the sanitized subject.
2. `mkdir -p docs/ideation/`, then write `docs/ideation/<slug>.md`.
3. **Read the file back** to confirm it landed as intended.
4. **Opt-in HTML view — only if the run carries `format:html`.** Read `references/html-rendering.md` and render `docs/ideation/<slug>.html` as a self-contained view derived from the markdown read back in step 3; read it back and verify content parity with the markdown. Default (no flag) runs skip this step — the output is markdown only.
5. **Gated auto-commit** — stage ONLY what this run wrote: `git add docs/ideation/<slug>.md` (and `docs/ideation/<slug>.html` when `format:html`). **Never `git add -A`.** Commit with an `Op: extend` trailer. Read-back precedes staging.

### Phase 6 — Route onward to askme

Hand the survivors to `askme` to clarify intent on the chosen direction(s) before any planning. `ideate` ends here. Do not jump to `plan` — the chosen direction needs intent-clarification first.

## Constitutional Rules (Non-Negotiable)

1. **Op-cell is `extend`.** Every commit body carries `Op: extend`.
2. **No ungrounded ideation.** Phase 1 is a precondition, not optional. Every candidate cites a basis (`file:line` or `external:<source>`); a candidate with no basis is dropped before critique.
3. **Reject by default.** The critique rejects every candidate unless it earns survival, and every loser carries a recorded rejection rationale. Silent drops and optimistic ranking are both rejected — ranking buries weak ideas, the gate cuts them and says why.
4. **The Reviewer audit is the single adjudication authority.** The orchestrator applies the Reviewer's survivor set and rejection rationale; it neither rescues rejected candidates nor re-litigates accepted ones.
5. **Markdown is the canonical surface, always written.** `docs/ideation/<slug>.md` is written every run and is the source of truth the `askme` handoff reads. HTML is opt-in via `format:html` and only ever a view derived from that markdown — it never replaces it and never changes the default output.
6. **Stage only what this run wrote.** `git add docs/ideation/<slug>.md` (plus `docs/ideation/<slug>.html` when `format:html`), never `git add -A`, and only after reading each file back.
7. **Generators in one tool-call message.** Parallel dispatch with distinct axis × frame assignments; sequential dispatch is rejected at the validation gate.
8. **Routes to `askme`, never straight to `plan`.** If any rule here conflicts with `~/.claude/claude/system-prompt-baseline.md`, the baseline wins.

## Validation Gates

| Gate | Pass Criteria | Blocking |
|---|---|---|
| Subject identified | Phase 1 scan grounded the subject; a basis exists | Yes — else route to `askme` and stop |
| Strategy grounding | `STRATEGY.md` folded into the grounding scope if present; absence noted in one line; never blocked | No |
| Grounding dispatched | Explore agent(s) per the 1/3/5 escalation returned summaries | Yes |
| Single-message generation | All generator subagents launched in one tool-call message | Yes |
| Every candidate grounded | Each carries a `file:line` or `external:` basis | Yes — ungrounded candidates dropped |
| Critique applied to all | Every candidate has a `survive \| reject` verdict + reason | Yes |
| Reviewer audit | Survivor set + rejection rationale audited before write | Yes |
| Canonical markdown written | `docs/ideation/<slug>.md` written every run, regardless of flag | Yes |
| HTML view parity | If `format:html`: `<slug>.html` derived from the markdown, single self-contained file, content parity | Yes when `format:html` |
| Doc read back | Each written file re-read after write to confirm it landed | Yes |
| Stage scope | Only this run's `docs/ideation/<slug>.{md,html}` staged; no `git add -A` | Yes |

## Commits

One ideation doc per commit, `Op: extend` trailer in the body (a load-bearing addition to the repo's decision record). Stage only what `ideate` wrote — `git add docs/ideation/<slug>.md` (and `docs/ideation/<slug>.html` when `format:html`), never other dirty files, never `git add -A`. Read each file back before staging. Publish by the operating repo's normal flow.

## Anti-patterns

- **Generating before grounding.** Ideas with no cited basis are fabrication. Scan first.
- **Dropping losers silently.** The rejection rationale is part of the deliverable; an unexplained reject is lost signal.
- **Optimistic ranking instead of reject-by-default.** Ranking keeps weak ideas at the bottom of the list; the gate cuts them and records why.
- **Parallel generators converging on the obvious reading.** Without distinct axis × frame assignments, every generator returns the same idea — the parallelism buys nothing.
- **Jumping to `plan`.** `ideate` ends at a survivor set handed to `askme`, not an implementation plan.
- **`git add -A`.** Stages unrelated dirty files. Stage what this run wrote by path.
- **HTML by default, or content only in the HTML.** HTML is opt-in (`format:html`) and always a view derived from the markdown; anything in the view but not the markdown is drift.

## Disambiguation

- **vs `askme`** — `askme` clarifies intent on a direction already in hand (Verbalized Sampling questions); it does not generate directions. `ideate` generates the candidate directions and routes its survivors to `askme` for intent-clarification before planning.
- **vs `strategy`** — `strategy` sets the anchor (the diagnosis and guiding policy the repo steers by); it is upstream grounding `ideate` reads, not a generator. `ideate` diverges within that anchor; `strategy` decides the anchor.
- **vs `plan`** — `plan` turns a chosen, clarified direction into implementation units. `ideate` never plans; it stops at survivors plus the `askme` handoff.

## Operating surface

`ideate` writes one surface by default: the operating repo's `docs/ideation/<slug>.md` (markdown, the canonical surface). With `format:html` it additionally writes `docs/ideation/<slug>.html`, a view derived from that markdown. Everywhere else it is read-only — Explore, generator, critic, and Reviewer subagents write nothing. Staging is scoped to the file(s) this run wrote; no writes to undefined or doubly-owned locations.
