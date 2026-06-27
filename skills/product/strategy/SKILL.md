---
name: strategy
description: Interview-driven product anchor — pin intent with a VS preamble, push back on weak answers, and write or maintain STRATEGY.md (target problem, approach, persona, metrics, tracks, milestones, non-goals, marketing) at the operating repo root. Use when the user says "/strategy", "define the strategy", "what's our north star", "set our product strategy", or starts or redirects a product. Fires automatically on strategy-framing phrases; the reject-by-default gate, not the trigger, decides whether a doc is written. `plan` designs implementation and `ideate` generates directions — `strategy` anchors what the product is and reads as optional grounding for both.
metadata:
  short-description: Interview-driven STRATEGY.md product anchor at the operating repo root
---

# Strategy — interview-driven product anchor, honest by construction

`strategy` runs a sharp interview and writes one durable anchor: the operating repo's `STRATEGY.md` (peer of `README.md`). It pins intent with a VS preamble, pushes back on weak answers instead of transcribing them, and resumes in place when the file already exists. It writes exactly **one** surface — `STRATEGY.md` at the operating repo root — and nothing else.

Rigor lives in the questions, not the headings. Section names are plain English; the interview enforces the discipline. Short is a feature — the template is constrained on purpose.

`Op:` of every run is `extend`: the anchor is a load-bearing capability added or sharpened, never a refactor of existing prose.

Adapted from EveryInc/compound-engineering-plugin (MIT).

## Auto-invoke

<auto_invoke>
<trigger_phrases>
- "what's our north star"
- "define the strategy"
- "set our product strategy"
- "what are we actually building"
</trigger_phrases>
Fire automatically on a trigger phrase or when the user starts or redirects a product. The reject-by-default gate below decides whether a doc is actually written — auto-firing is permission to evaluate, not permission to fabricate a strategy the user never gave.
<manual_override>`/strategy [section]` runs immediately without waiting for a trigger phrase; an argument names a section to revisit (`approach`, `metrics`, `tracks`).</manual_override>
</auto_invoke>

## When to Apply

- Starting or redirecting a product — no `STRATEGY.md` exists and the same framing keeps getting relitigated.
- An existing `STRATEGY.md` has gone stale, or a section reads as a slogan.
- `plan` or `ideate` need upstream grounding and find no anchor.

## When NOT to Apply

- The user wants an implementation design → `plan`. Strategy says what the product is; plan says how to build a slice.
- The user wants directions or options generated → `ideate`. Strategy pins one intent; ideate diverges.
- The ask is a feature spec, backlog priority, or schedule — those live in the tracker, not the anchor.
- No human is available to answer and be pushed back on. An interview with no interviewee produces fabrication — exit.

## Reject-by-default gate

A section earns its place in `STRATEGY.md` only if it clears, in order:

1. **Specific, not vague.** Names a concrete situation or choice, and is falsifiable. Reject "better tools for X" and "be the market leader" — they survive any product.
2. **Connected.** Approach answers the target problem; tracks serve the approach; metrics could plausibly regress. A disconnected section is a slogan, not strategy.
3. **The user's, not yours.** Captured in the user's own language after pushback — not auto-completed by the agent. A fabricated strategy is worse than none.

Push back at most twice per section; then capture what the user gave and mark the section worth revisiting. **If the required sections (target problem, approach, persona, metrics, tracks) can't clear the gate, write nothing, commit nothing, and say so in one line.** A clean "not enough to anchor yet" is a valid, correct result.

## Support files — read on demand

Don't bulk-load. Read each at the step that needs it.

- `references/interview.md` — the question bank, per-section quality bar, and pushback rules for all eight sections. Load before any interview turn; improvising the pushback from memory degrades into transcription.
- `assets/strategy-template.md` — the locked section skeleton and post-write checklist. Read when assembling the draft.

## Workflow

### Phase 0 — Pin intent, then route by file state

1. **VS preamble.** Before the interview, run a short Verbalized Sampling preamble (the `askme` skill) to surface the distinct things the user could mean by "strategy" here, and pin one. Skip only when the user already stated a single unambiguous intent. Pinning the wrong frame wastes the whole interview.
2. **Route by file state.** Resolve the operating repo root once with `git rev-parse --show-toplevel`; the anchor is exactly `$root/STRATEGY.md` and nothing nested or recursively discovered. Read that one path with the native file-read tool — a not-found result is the existence signal:
   - **Absent** → first run. Announce "No STRATEGY.md — let's write it." Go to Phase 1.
   - **Present, argument names a section** → targeted update. Go to Phase 2.
   - **Present, no argument** → ask which section(s) to revisit, then Phase 2.

### Phase 1 — First-run interview

Read `references/interview.md`. Run the eight sections in document order: target problem, approach, persona, metrics, tracks, then optional milestones, non-goals, marketing. For each: ask the opening question, apply the reject-by-default gate, push back at most twice on a weak answer, then capture it in the user's own words. Required sections are 1–5; optional sections default to skip — never invent them.

### Phase 2 — Resume-in-place update

Read the existing `STRATEGY.md` in full. Summarize current state in 3–5 lines so the user sees what's on file. Re-interview only the targeted or stale sections with full pushback — do not rubber-stamp existing weak content because it's already written. **Preserve every untouched section byte-for-byte.** Update, don't clobber.

### Phase 3 — Write, read back, commit

1. **Gate check.** Required sections cleared → proceed. Not cleared → write nothing, commit nothing, say so in one line, exit.
2. Read `assets/strategy-template.md`; fill it with captured answers in the user's language. Delete unused optional sections — no empty headers. Set `last_updated` to today's ISO date.
3. Present the full draft in chat; offer one edit round.
4. Write `$root/STRATEGY.md` (the path resolved in Phase 0).
5. **Read the file back** to confirm it landed as intended.
6. **Commit.** Stage only the resolved anchor: `git -C "$root" add STRATEGY.md` — never `git add -A`. Commit with an `Op: extend` trailer. Publish by the operating repo's normal flow.
7. Note in one line that `plan` and `ideate` read it as optional grounding on their next run.

## Constitutional Rules (Non-Negotiable)

1. **Anchor, not plan.** Strategy is what the product is and why. Features → `ideate`/`plan`; schedules → the tracker. Reject creep.
2. **Rigor in the questions, not the headings.** Headers stay plain English; the interview carries the discipline.
3. **Pushback is the skill.** Transcribing a weak answer is the failure mode. Reject vague answers, quote the user back, cap at two rounds.
4. **Short is a feature.** The template is locked. Adding a section costs more than it looks — don't.
5. **No interviewee, no doc.** The gate fails closed: a trigger grants evaluation, never fabrication. Gate fails → no write, no commit.
6. **One surface.** Writes only `STRATEGY.md` at the operating repo root, and stages only that file.

## Validation Gates

| Gate | Pass criteria | Blocking |
|------|---------------|----------|
| Intent pinned | A single intent fixed via VS preamble, or stated unambiguously | Yes |
| Required sections | Target problem, approach, persona, metrics, tracks each clear the reject-by-default gate | Yes — no write on failure |
| Connection | Approach answers the problem; tracks serve the approach; metrics can regress | Yes |
| Read-back | Written `STRATEGY.md` re-read and matches intent | Yes |
| Staging | `git -C "$root" add STRATEGY.md` only; working tree otherwise untouched | Yes |

## Commits

One anchor per commit. Stage only the resolved anchor: `git -C "$root" add STRATEGY.md` — never `git add -A`. Both first-run and resume-in-place carry `Op: extend`: a new or sharpened anchor is load-bearing capability. A resume that repairs a stale section is still additive — the strategy evolved with the product, so there is no prior invariant to cite in a `Restores:` trailer, which is what would make it `correct`. Publish by the operating repo's normal flow.

## Anti-patterns

- **Transcribing weak answers.** Capturing "we want to be the market leader" verbatim. The gate exists to reject it.
- **Fabricating to look productive.** Auto-firing on a trigger and inventing a strategy the user never gave.
- **`git add -A`.** Sweeping unrelated dirty files into the strategy commit. Stage `STRATEGY.md` alone.
- **Clobbering on resume.** Regenerating the whole doc when one section was stale. Update in place.
- **Section creep.** Adding headings the template lacks because a section "felt thin." Push the rigor into the question instead.

## Disambiguation

- **vs `plan`** — `plan` designs implementation: decisions and units for building a slice, read-only over the codebase. `strategy` anchors what the product is and why. `plan` reads `STRATEGY.md` as optional grounding.
- **vs `ideate`** — `ideate` generates many directions and filters them. `strategy` pins one intent. Diverge with `ideate`; converge and anchor with `strategy`. `ideate` reads `STRATEGY.md` as optional grounding.
- **vs `askme`** — `askme` runs the Verbalized Sampling protocol to explore intent. `strategy` invokes it as the Phase 0 preamble, then writes the durable doc. `askme` asks; `strategy` records.

## Operating surface

`strategy` writes exactly one surface: the operating repo's `STRATEGY.md`. No other files, no `git add -A`, no writes to undefined locations.
