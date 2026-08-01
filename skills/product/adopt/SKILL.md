---
name: adopt
description: "Bring Mycelium into a project that already has code. Detects that the repo predates the framework, asks before touching anything, then reads the codebase to draft what it CAN establish (delivery, solution shape) and — the actual point — names what it cannot (purpose, strategy, real user evidence). The output is a discovery backlog with a head start, never a filled canvas."
metadata:
  instruction_budget: "60"
  framework_dependency: "mycelium"
  framework_dependency_note: "This skill is designed to run within the Mycelium framework (https://github.com/haabe/mycelium). Standalone use will skip the canvas state, theory gates, and harness behavior the skill assumes. Install: /plugin install mycelium@haabe-mycelium."
---

# Adopt (brownfield entry)

`/mycelium:start` assumes a blank page. Most projects are not a blank page. This
skill is the entry point when the code came first.

## When to Use

- A repo with existing source and no populated canvas (the SessionStart
  brownfield check points here).
- A maintainer who wants discovery on a product that already ships.
- NOT for a new idea — that is `/mycelium:start`.

## The shape of the run: two phases, one session

**Phase 1 — populate from the codebase.** Read the repo and fill in what the
code can actually establish, at the right evidence class.

**Phase 2 — patch the holes with the user, exactly as a greenfield project
would.** The gaps left by phase 1 are not a backlog to hand over. They are the
agenda for the rest of the session, worked with the same discovery discipline
`/mycelium:start` would apply — the only difference is that the canvas is not
empty when you begin.

Do not stop between the phases and present a list. Ending at a fork is the
failure this skill exists to remove: a maintainer offered "run the greenfield
brief or skip" has no good option, and "here is your discovery backlog" is the
same fork with extra steps.

**Why phase 1 cannot be the whole thing.** A codebase answers *what was built*
and *how it ships*. It is nearly silent on *why it exists* and *who decided
that*. Extraction is asymmetric, and inverted from where discovery value lives:

| scale | what code yields |
|---|---|
| L4 Delivery | STRONG — stack, release cadence, distribution, CI, test posture |
| L3 Solution | STRONG — feature surface, module structure, what shipped when |
| L2 Opportunity | INFERENCE ONLY — you see what was built, not the problem it solved. Real demand signal lives in the ISSUE TRACKER, which a clone does not contain. |
| L5 Market | THIN — category and channels, rarely positioning |
| L1 Strategy | USUALLY EMPTY |
| L0 Purpose | USUALLY NEAR-EMPTY — READMEs state a *what* and a stack, seldom a *why* |

So phase 1 reliably fills the layers that never needed discovery and leaves
empty the ones that did. That is not a defect in the extraction — it is the
map of what phase 2 has to work on. Never present a phase-1 canvas as though
discovery happened; it is a starting position, and say so.

**Watch for drift.** The sharpest thing this skill can surface is a mismatch
between what the project *says* it is and what it has *become*. A README that
describes the original scope while five years of changelog show the product
moved somewhere else is a real finding, visible in minutes, and a maintainer
recognises it immediately. Look for it explicitly: compare the stated purpose
against the feature surface and the most recent changelog entries.

## Workflow

### Step 1: Confirm before anything

Do not scan and present as a fait accompli. Say what you propose to read and ask.

> "This project has code but no Mycelium discovery state. I can read the repo
> and draft what it can establish — roughly the delivery and solution picture —
> and then show you what it cannot: purpose, strategy, and any real user
> evidence. That second list is the useful half. About N minutes. Go ahead?"

If declined, stop. Do not leave partial state. Offer `/mycelium:start` (blank
page) or nothing.

### Step 2: Read, in this order

Cheapest signal first; stop when you have enough rather than reading everything.

1. `README`, docs index — stated purpose, category, audience
2. `CHANGELOG`, release history — what the product actually became, and how fast
3. Manifest (`package.json`, `pyproject.toml`, …) — stack, distribution, scripts
4. Top-level source tree — feature surface and module boundaries
5. `CONTRIBUTING`, CI config — delivery posture
6. Tests — what the team considers worth protecting

**Do not read the whole codebase.** You are establishing shape, not
comprehension. If the repo is large, breadth beats depth.

**Issue tracker**: if the host is reachable and the user consents, open issues
are the only real L2 signal available. Without them, say L2 is un-evidenced
rather than inferring it from code.

### Step 3: Draft, with the evidence class the material actually has

Write to canvas ONLY what the code supports, and tag every entry:

```yaml
provenance:
  evidence_type: anecdotal
  source_classes:
    - internal_desk        # derived from artifacts, NOT from anyone
  evidence_sources:
    - "codebase read <date> @ <commit>: <file> — <what it showed>"
```

**HARD GUARDRAIL.** Extracted material is never `external_human`. Nobody said
it. If code-derived inference gets recorded as user evidence, the framework has
automated the consistency-as-evidence failure it exists to prevent, and a canvas
full of code-derived "evidence" is worse than an empty one. Confidence on
anything extracted starts low and says why.

**THREE TIERS, NOT TWO — and phase 2 moves material between them.** This is the
distinction that keeps the guardrail honest once the user starts talking:

| tier | what it is | when |
|---|---|---|
| `internal_desk` | inferred from artifacts. Nobody said it. | phase 1 |
| `internal_stakeholder` | the maintainer's own testimony about their own product | phase 2 |
| `external_human` | someone who is NOT the maintainer — a user, a customer | neither |

When the user confirms or corrects a phase-1 inference, that entry is upgraded
from `internal_desk` to `internal_stakeholder` — it is now testimony rather than
inference. It does NOT become `external_human`. The maintainer describing their
own product is the person closest to the assumption, not evidence against it,
and a canvas that blurs the two will read as validated when nothing outside the
project has been consulted.

Say so explicitly in the entry when you upgrade, and note what is still missing:
if no real user has been asked, the canvas should record that plainly rather
than let a well-populated file imply otherwise.

### Step 4: Show the starting position, briefly

State both halves in a few lines, then keep going. This is a checkpoint, not a
handover.

**Established from the code** — delivery and solution, plainly, flagged as
artifact-derived.

**Open** — and these are the next questions, not a report:

- Who is this for, specifically?
- What evidence exists that the problem is real?
- What would prove the idea wrong?
- Why this rather than the alternatives?
- Any drift between stated purpose and shipped behaviour.

Then say what happens next and start: *"Those are the gaps. Same questions a new
project would get, except we already know what you built. Shall we work through
them?"*

### Step 5: Patch the holes — greenfield discipline, non-empty canvas

Run the normal discovery loop against the gaps. `/mycelium:interview`'s
questioning shape is the right instrument for the L0/L1 holes; `/mycelium:jtbd-map`
or `/mycelium:user-needs-map` for L2. Invoke them, or apply their sequence
directly — what matters is that the questions get asked in this session rather
than deferred to one the user may never start.

Two things change versus greenfield, and both help:

- **Ask better questions.** You have read the code. "You describe this as X but
  the last year of changelog is mostly Y — which is it now?" beats "what are you
  trying to change, and for whom?" Use the drift finding as the opening.
- **Anchor answers against reality.** When the user states a purpose, check it
  against the feature surface. A mismatch is a finding, surfaced not corrected.

**Same exit condition as greenfield.** The canvas is done when it would pass the
same gates a new project's must — real evidence at L0/L2, human sources, honest
confidence. Artifact-derived entries do not satisfy those gates; they are
scaffolding the human answers replace or confirm. A diamond opens when the user
has chosen a scale, exactly as it would otherwise.

## What NOT to Do

- Never write a canvas the user has not seen and approved.
- Never present extracted L3/L4 as though discovery happened.
- Never mark code-derived inference `external_human`, or set confidence above
  `anecdotal` on it.
- Never modify user-owned source. Brownfield-additive: the framework adds
  capabilities, it does not touch the project's own files.
- Never claim the drift finding is a problem. Surface it; the maintainer decides
  whether it is intentional.

## Theory Citations

- Torres (CDH): opportunities come from evidence, not from reading code. Anything
  extracted at L2 is a hypothesis awaiting a human source.
- Gilad (Evidence-Guided): artifact-derived material sits at the bottom of the
  confidence ladder; label it there and let it earn its way up.
- Christensen (JTBD): a codebase shows the solution, never the job. The gap
  between them is what this skill exists to make visible.
