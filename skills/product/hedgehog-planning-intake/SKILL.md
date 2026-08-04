---
name: hedgehog-planning-intake
description: Use once per project, at the start, on any core — Phase 0 (running the vendored BMAD-METHOD planning shelf) is shared by every core; Phase 1 (mining `04-prd.md` into intent records plus the Add-ons decision) is full-stack-app's own procedure, run again on a scoped pass when new domain scope enters play. Invoked by the `planner` agent after Phase 0 core selection; don't run standalone. landing-page runs this skill's Phase 0, then mines the same archive through `hedgehog-landing-loop`'s own planning-intake section, that core's counterpart to this skill's Phase 1. An authored core runs this skill's Phase 0, then `hedgehog-core-design`, then this skill's Phase 1 mining against the designed layer sequence.
---

# Hedgehog Planning Intake

Turns a person's description of a problem into planning material, by
running the vendored BMAD-METHOD planning shelf (Phase 0, shared by both
cores) and mining its output. On full-stack-app that mining is this
skill's own Phase 1, into intent records written via `hedgehog intent
add`; on landing-page it's `hedgehog-landing-loop`'s planning-intake
section, into a subject/audience/job statement. This is the mechanics
`planner` calls once its Phase 0 core-selection check has picked a core —
the interpretive judgment (which Feature becomes which intent, Confirm &
Lock either way) belongs to `planner`; this skill (Phase 0, and Phase 1 on
full-stack-app) and `hedgehog-landing-loop` (landing-page's own mining)
are the fixed procedures that judgment runs inside.

## Phase 0 — BMAD elicitation (every core)

State the BMAD attribution, then run the vendored shelf in full
sequence, every time — no per-project skip logic, no reduced default
set:

1. `bmad-brainstorming` (`skills/BMAD/core-skills/bmad-brainstorming`) —
   diverge on the idea before locking anything.
2. `bmad-product-brief` (`skills/BMAD/bmm-skills/1-analysis/bmad-product-brief`)
   — the product brief.
3. `bmad-prfaq` (`skills/BMAD/bmm-skills/1-analysis/bmad-prfaq`) — vets
   the idea press-release-style.
4. `bmad-prd` (`skills/BMAD/bmm-skills/2-plan-workflows/bmad-prd`) — the
   PRD, including its Glossary (entities, relationships, cardinality).
5. `bmad-ux` (`skills/BMAD/bmm-skills/2-plan-workflows/bmad-ux`) — the UX
   spec, `DESIGN.md` + `EXPERIENCE.md`.
6. `bmad-deep-recon` (`skills/BMAD/core-skills/bmad-deep-recon`) —
   market/competitive/user-voice research.

Any skill may itself invoke `bmad-advanced-elicitation`
(`skills/BMAD/core-skills/bmad-advanced-elicitation`) at its own pause
points — that's expected, let it run.

Write each skill's output to `.hedgehog/BMAD/`, per the fixed layout:

```
.hedgehog/BMAD/
  00-manifest.md        # attribution + pinned version + date + which skills ran
  01-brainstorming.md
  02-brief.md
  03-prfaq.md
  04-prd.md
  05-ux-spec/
    DESIGN.md
    EXPERIENCE.md
  06-research.md
```

Every file/folder carries a one-line attribution header. `00-manifest.md`
states the source repo, pinned version (`skills/BMAD/ATTRIBUTION.md` has
the pinned commit), date, and which skills ran.

`.hedgehog/BMAD/` is archival and immutable once written, on every core.
Nothing in `hedgehog-loop`'s day-to-day operation, `hedgehog-bootstrap`,
or `reviewer` reads this folder live — `planner` reads it exactly once,
right after the shelf completes, to mine it (this skill's Phase 1 below
on full-stack-app; `hedgehog-landing-loop`'s planning-intake section on
landing-page). After that it's historical record only, the same
relationship the commit log has to a merged PR.

## Phase 1 — Mining (full-stack-app only)

landing-page's counterpart to this Phase 1 is
`hedgehog-landing-loop`'s own planning-intake section, run once Phase 0
above completes: it mines the same `.hedgehog/BMAD/` archive into a
subject/audience/job statement, in place of the intents this Phase 1
produces.

Read `.hedgehog/BMAD/04-prd.md` only — §3 Glossary and §4 Features.
Nothing else in `.hedgehog/BMAD/` is read again: brainstorming, brief,
PR-FAQ, and deep-recon existed to produce a good PRD, and the UX spec is
read later, once per module, by `ux-planner`, not by this mining pass.
Mining is mechanical, not interpretive — one graph row per PRD element,
per this table:

| PRD element | Graph row |
| --- | --- |
| §4 Feature | one `intents` row — the feature's description already reads as `goal` + `outcome` |
| FR "Consequences (testable)" item | `requirements` row, `kind='acceptance'` |
| Feature-specific NFR / cross-cutting rule | `requirements` row, `kind='rule'` |
| §3 Glossary relationship/cardinality | `intent_dependencies` row (the referencing feature's intent depends on the referenced feature's intent) |

Procedure:

1. **Walk §4 Features top to bottom.** For each Feature, that's one
   intent: `id` a short kebab-case slug of the Feature's name, `goal` and
   `outcome` drawn directly from the Feature's description (split the
   description across the two if it names both the capability and the
   result; otherwise the same sentence can serve both).
2. **Walk that Feature's FRs.** Each FR's "Consequences (testable)" list
   items become that intent's `requirements` with `kind='acceptance'`,
   one per item, verbatim or lightly tightened — no rephrasing that
   changes what's being tested.
3. **Collect any NFR or cross-cutting rule scoped to that Feature**
   (not a project-wide NFR with no single owning Feature) as a
   `requirements` row with `kind='rule'` on that intent.
4. **Walk §3 Glossary relationships and cardinality.** Each relationship
   between two entities that belong to different Features' intents
   becomes one `intent_dependencies` row: the intent for the entity
   holding the foreign key depends on the intent for the entity it
   references. A relationship entirely inside one Feature's entities
   produces no row — it's already the same intent.
5. **Run the Add-ons decision** (`planner`'s own judgment call — see that
   agent's "The Add-ons decision") for Auth, Queue, and Mobile.
6. **Run Confirm & Lock** (below) before writing anything.
7. **Write each intent via `hedgehog intent add`** — one invocation per
   Feature: `--acceptance` per row from step 2, `--rule` per row from step
   3, `--depends-on` per row from step 4, or an equivalent `--file
   <path.json>` batch matching the same shape (`{ id, goal, outcome,
   rules, acceptance, depends_on, priority }`). This is Phase 1's only
   write to the build graph.
8. **Write `.hedgehog/addons.yaml`** with the Add-ons decision from step 5.
9. **Fill root `CLAUDE.md`'s `{{PROJECT_NAME}}` and `{{PROJECT_SUMMARY}}`
   placeholders**, first run only, then delete the installer's HTML
   comment block at the top of that file. Leave every other line
   untouched.

On a later run (new scope entering play), skip steps 8 and 9 unless new
scope genuinely changes an add-on trigger or the project's identity
itself changed — mine only the PRD's new or changed Features into
additional `hedgehog intent add` calls, never re-add or edit an intent
already in the graph.

## Confirm & Lock

Everything through Phase 1 mining is provisional and cheap to change —
nothing has been written yet. This stage is the last point before that
stops being true, so it's a hard stop, not a recap in passing.

🔒 **Confirm & Lock**. Show, in full, not condensed:

- Each intent about to be added: `id`, `goal`, `outcome`, its
  `requirements` (rule/acceptance), and its `depends_on` list.
- The Add-ons decision (Auth / Queue / Mobile, each explicitly on or
  off, with the one-line reason).
- Which BMAD skills ran and where their output lives
  (`.hedgehog/BMAD/`).

Then state plainly what happens on confirmation, before it happens:

> This writes each intent above via `hedgehog intent add` and the
> Add-ons decision to `.hedgehog/addons.yaml`, then shows the compiled
> graph with `hedgehog status`. Phase A build (schema first) starts on
> the first ready task once that closes. Anything wrong or missing — say
> so now; it's a normal edit before this point, and a Correction Protocol
> entry after. Confirm to proceed, or tell me what to change.

Wait for an explicit go-ahead. A revision here is just another mining
pass — update the draft, re-run this stage, don't write anything until
the confirmation holds. Once confirmed, after every `hedgehog intent add`
call lands, run `hedgehog status` and show it in full as the graph's
confirmation view.
