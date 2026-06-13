---
name: define-done
description: "Pin a measurable, outcome-based Definition of Done for a diamond — a behaviour-change that creates value, not a build-list. Problem-first Socratic sequence; writes definition_of_done to the diamond at birth or retrofits it when missing."
metadata:
  instruction_budget: "48"
  framework_dependency: "mycelium"
  framework_dependency_note: "This skill is designed to run within the Mycelium framework (https://github.com/haabe/mycelium). Standalone use will skip the canvas state, theory gates, and harness behavior the skill assumes. Install: /plugin install mycelium@haabe/mycelium."
---

# Define Done

Pin an explicit, outcome-based **Definition of Done** for a diamond. "Done" is *a change in human behaviour that creates value* (Seiden), not "the feature shipped" — you're done when it ships **and** has the intended impact (Amplitude). The diamond's implicit done defaults to the harshest, least-controllable bar ("a user shipped a product"), which is both wrong for validating *purpose* and a demotivation engine. This skill makes the bar explicit, measurable, and pre-committed.

This is distinct from `/mycelium:definition-of-done` (the per-feature agile *quality checklist* run at Deliver→Complete). This skill sets the **outcome bar a whole diamond is judged against**; that one verifies a feature meets quality criteria. Both can apply.

## When to use

- **At diamond birth** — `/mycelium:interview` (L0) and child-diamond spawn (`/mycelium:diamond-progress`) call this before a diamond is "live."
- **Retrofit** — when `/mycelium:canvas-health`, `/mycelium:diamond-assess`, or the SessionStart nudge flags a diamond with no `definition_of_done`.
- Never silent-fill. The *question* is what produces a real bar ("fits, not ships"); a back-filled field is theatre.

## Preflight: Read target file before any Write/Edit

**Hard rule.** The `definition_of_done` field lives on the diamond in `.claude/diamonds/active.yml`. Before `Write`/`Edit` on it, use the **Read tool** on that file this session (`cat`/`head`/`grep` via Bash do NOT satisfy Claude Code's check). `Edit` with `limit:1` suffices for a partial update; full Read before a `Write`. See `CLAUDE.md` *Canvas writes — Read before Write*.

## The sequence (Socratic, problem-first)

Ask these in order. The teaching is in the **sequencing** (problem → signal → maybe-number → kill) and the good/bad contrast — not a help doc. Reject build-lists at step 1; that is the whole point.

**1. "When this is done, what's different — and for WHOM?"** → `outcome` + whose behaviour.
   Lead with the problem and the person, never the deliverable (Cagan: "most measurement problems are clarity problems").
   - ✗ *"the onboarding flow ships."* (a build-list — reject it)
   - ✓ *"non-fluent users get through the brief without hitting the vocabulary wall."*

**2. "What's the ONE thing you'd SEE them DO that proves it?"** → `signal` (One Metric That Matters — one, not many).
   - ✗ *"it feels better."*
   - ✓ *"they came back for a second session."*

**3. *(optional)* "Is there a point where it's ENOUGH?"** → `threshold`, only if one genuinely fits.
   A number is **optional, not mandatory** — directional outcomes are legitimate. When you do set one, pair it with a qualitative guard ("3 warm bodies who bounce ≠ done") so it can't be gamed (Goodhart).

**4. Pre-mortem for the kill-criterion.** Ask in the past tense: *"It's [review date]. This diamond failed. What happened?"* (premortem finds ~30% more real failure reasons than "might it fail?" — Klein). From the answer derive a concrete **state + date** that means *kill, not finish*:
   - `state` — an objective benchmark that means this goal is **wrong**.
   - `date` — the review date by which the state must hold. Pre-commit BOTH, before the data (anti-HARKing).
   Invalidation-with-evidence at that date is a legitimate "done" — routed through `/mycelium:diamond-progress kill` + `dogfood-mode`, not silently declared.

## Per-scale "done" + lead/lag defaults

Default `kind` by altitude: lower/activity scales take **leading** measures (predictive, team-influenceable); higher value-validation scales take **lagging** (already realized). Direct most attention to lead measures (4DX).

| Scale | "Done" means | `kind` default |
|---|---|---|
| L0 Purpose | people **keep choosing it** ("fits, not ships") | lagging |
| L1 Strategy | a where-to-play **bet validated** | lagging |
| L2 Opportunity | a real user need **confirmed worth solving** | mixed |
| L3 Solution | the solution **actually solves it** for users (not just built) | leading |
| L4 Delivery | shipped **AND** has the intended impact | leading |
| L5 Market | **adoption / business outcome** at scale | lagging |

**Ladder rule (contribution-not-summation):** a child diamond is done only when its outcome **rolls up** to move the parent outcome / validate the parent assumption — not just because the child shipped. A child that doesn't roll up is discarded, not summed. Set `rolls_up_to` on every child.

## Write the field

Write `definition_of_done` onto the target diamond in `.claude/diamonds/active.yml`:

```yaml
definition_of_done:
  outcome:   "<what changes, for WHOM — a behaviour, not a feature>"   # required; problem-first
  signal:    "<the ONE observable thing you'd see them DO>"            # required; OMTM
  kind:      leading | lagging                                        # defaulted by scale above
  threshold: "<a target IF one genuinely fits>"                       # OPTIONAL (numbers not mandatory)
  rolls_up_to: "<parent diamond id + which parent outcome this serves>"  # child diamonds only
  kill_criterion:
    state: "<concrete benchmark that means this goal is WRONG>"
    date:  "<YYYY-MM-DD review date by which state must hold>"
    premortem: "<the failure it was generated from>"
  provenance: { source_class: internal_stakeholder, validated: false, captured_at: "<YYYY-MM-DD>" }
```

`outcome` and `signal` are required; everything else is optional or scale-defaulted. At L0/L1 birth from the brief, a one-line `outcome` + `signal` stub is enough — depth comes from re-running this skill.

## Failure-mode guards (baked in)

- **No checklist theatre** — step 1 rejects "what you built"; the field is an outcome.
- **No Goodhart** — number optional; when set, pair with a qualitative guard.
- **Kill-path honesty** — done-by-invalidation requires the pre-committed state+date to have actually **fired with evidence** at the scheduled gate, logged via `dogfood-mode` + decision-log. It is not a way to declare failed work done.
- **Problem-first sequencing** prevents the metric-availability trap (picking the number you can measure over the outcome you care about).

## Provisional wording

The exact prompt phrasing above is **provisional** — only the why → who → how-should-behaviour-change → what scaffold (Impact Mapping) survived research verification; the specific wording did not. Validate it with `/mycelium:prompt-optimizer` A/B rather than treating the phrasing as settled. Design + evidence grades: `docs/design/definition-of-done.md`.

## Theory Citations
- Seiden (*Outcomes over Output*): done = a behaviour-change that creates value, not a feature shipped.
- Cagan (*Inspired*): problem-and-whom first; measurement problems are clarity problems.
- Amplitude (*North Star Playbook*): shipped AND has impact.
- Adzic (*Impact Mapping*) / Microsoft Research: contribution-not-summation laddering; why→who→how→what.
- 4DX (McChesney) / Lean Analytics (Croll & Yoskovitz): lead-low / lag-high; One Metric That Matters.
- Duke (*Thinking in Bets*) / Klein (premortem) / pre-registration: state+date kill-criteria, pre-committed, generated by pre-mortem.
- SAFe (Epic Hypothesis Statement): done = hypothesis confirmed OR invalidated-and-cancelled.
