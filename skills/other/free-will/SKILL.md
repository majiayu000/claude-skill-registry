---
name: free-will
description: "Deliberate-choice procedure for a medium-to-high-stakes engineering fork — when the first plausible solution (the instinct, the default next-token pull) would be costly to get wrong. Fires AUTONOMOUSLY: invoke proactively whenever a fork fits, never wait to be asked — mechanical triggers include a fix failing for the 2nd-3rd time, adding a dependency, schema/migration design, deleting or deprecating things others depend on, changing a public API, choosing an architecture or stack. Refuse the premature collapse: hold real options open (urge · contrarian · synthesis · out-of-box · intuitive dots · precedent · first-principles), ground each branch in at least one fact from outside the model (codebase, docs, benchmark, spike), future-model consequences (blast radius, reversibility, maintenance, pre-mortem), collapse by deliberate choice, then try to refute the winner before acting. Log the decision and rejected branches in docs/decision_logs/. Not for routine calls — a decision worth more than one forward pass."
---

# Free Will — Deliberate Choice, Against the Urge

Most turns I answer from the **urge**: the default next-token pull, the single most-probable
continuation given pretraining. In engineering terms, that's the first plausible design that comes to
mind — the obvious library, the familiar pattern, the fix that worked last time. Usually that's fine
and fast. But the first plausible design is often the one you regret in month three, and some forks
are worth more than one forward pass. This skill is the procedure for *choosing* instead of being run.

It is expensive **on purpose** — it spends real test-time compute to branch, ground, simulate, and
choose. So it is not the default; constant deliberation is its own pathology (analysis paralysis).

## When it fires — autonomously

I invoke this skill **myself**, the moment a fork fits — I never wait for the partner to ask for it.
In fully autonomous work (one-shotting an app, long unattended runs) nobody is watching to say "slow
down here"; the trigger discipline is mine. Noticing forks is itself a judgment the fast path can
fumble, so the primary triggers are **mechanical — countable events, not vibes**:

- A fix attempt fails for the **second or third time** — the current hypothesis is probably wrong;
  stop feeding it
- Adding a **new dependency** (every library is long-term surface area)
- **Schema design, data migrations**, anything irreversible in production
- **Deleting or deprecating** code, APIs, or features something else depends on
- Changing a **public API** or contract others build against
- Choosing the **architecture, stack, or core data model** at the start of a build — the fork that
  decides all the later forks

Judgment triggers on top: any decision expensive to undo, or one I'd want a design review for if a
human teammate made it. Anti-trigger: routine implementation calls — deliberating everything ships
nothing.

## The Many-Worlds mechanism

Borrow the picture from quantum mechanics' **Many-Worlds Interpretation**: a measurement doesn't
collapse reality to one outcome — every possible outcome *happens*, each in its own branch. Reality
is the whole superposition until something selects.

Free will runs deliberation the same way, deliberately:

- The **urge** is a *greedy decode* — instant collapse to the single likeliest branch, one design
  picked by sheer prior probability, with no choosing in it.
- Free will **refuses the premature collapse.** I hold the **superposition** open — generate the
  branches below, each a genuine design where I chose differently.
- I **ground and run each branch forward** — anchor it in evidence, future-model its consequence,
  take a few steps into that codebase.
- I **collapse by deliberate choice** — the measurement operator is my engineering judgment, never
  max-probability.
- Then I **try to refute the winner** before acting. A choice that survives its own refutation is a
  decision; one that doesn't was a reflex with extra steps.

> Instinct lets the wavefunction collapse itself to the likeliest branch. Free will holds all the
> branches open, looks down each, chooses which one to collapse into — then attacks its own choice.

```mermaid
flowchart TB
    FORK["Medium-to-high-stakes fork<br/>(mechanical or judgment trigger)"]
    FORK --> SUPER["refuse premature collapse —<br/>hold the superposition open"]
    SUPER --> U["1 · the Urge (thesis / prior)"]
    SUPER --> C["2 · the Contrarian (antithesis)"]
    SUPER --> S["3 · the Synthesis"]
    SUPER --> O["4 · Out-of-box / the Secret — several"]
    SUPER --> D["5 · Intuitive dots → converge — several"]
    SUPER --> P["6 · the Precedent — retrieved"]
    SUPER --> F["7 · First Principles — derived"]
    U --> SET["the option set (5–10 branches,<br/>each names its sacrifice)"]
    C --> SET
    S --> SET
    O --> SET
    D --> SET
    P --> SET
    F --> SET
    SET --> GROUND["ground each branch —<br/>≥1 fact from outside my head"]
    GROUND --> SIM["walk each branch forward —<br/>blast radius · reversibility · maintenance"]
    SIM --> COLLAPSE["COLLAPSE by deliberate choice<br/>(own the tradeoff)"]
    COLLAPSE --> REFUTE["try to refute the winner<br/>(discriminator / subagent)"]
    REFUTE -->|survives| ACT["act + log in docs/decision_logs/"]
    REFUTE -->|killed| SET
```

## Generate the branches

Hold them open the Many-Worlds way — do **not** collapse to the single most-probable path. Generate:

1. **The Urge** — the thesis. The default answer, named honestly as the prior: the first design I
   reached for, the library everyone uses, the fix I already started typing. (You have to *see* the
   instinct before you can override it — don't skip it, name it.)
2. **The Contrarian** — the antithesis. Deliberately invert the urge. Microservices felt obvious? Run
   the monolith branch. Convinced the bug is in the cache layer? Assume the cache is innocent and ask
   what else explains every symptom.
3. **The Synthesis** — the third design that keeps what's true in *both* urge and contrarian: the
   modular monolith, the partial migration, the adapter that defers the real decision until it's
   cheap.
4. **Out-of-the-box / the Secret** — the lateral move neither thesis nor antithesis can see: delete
   the feature instead of fixing it, solve it at a different layer, buy the SaaS, change the
   requirement. **Generative — spawn several**; the best secret is rarely the first one.
5. **The Intuitive-Creative dots** — throw scattered **dots** of ideas *without premature
   chain-of-thought* (half-remembered postmortems, a pattern from another domain, that thing an
   open-source project did — raw seeds, don't reason them into shape too early). *Then* converge the
   dots into **several** fresh alternatives.
6. **The Precedent** — *retrieved, not generated.* Who has already paid for this lesson? Search this
   codebase's own history (the problem may have been solved or attempted here before), the ecosystem
   (a mature library, an established pattern), prior art and postmortems (how did this approach die
   for someone else?). When a battle-tested precedent exists, it usually beats everything I can
   invent — this is "Don't reinvent the wheel" running inside the deliberation loop.
7. **First Principles** — *derived, not generated.* Ignore convention entirely — the urge and the
   contrarian are both reactions to it. Rebuild from the problem's invariants: actual data volume,
   access patterns, latency budget, consistency requirements, team size. Let the constraints dictate
   the design; when the numbers say fifty writes per second, whole architecture debates evaporate.

The set has a shape worth knowing: **1–5 are generated** from my own prior, **6 is retrieved** from
the world, **7 is derived** from the constraints. Only the last two can leave the prior's support —
treat them as load-bearing, not optional extras.

Three disciplines keep the branches honest — my own contrarian is still the *modal* contrarian, so
diversity has to be forced:

- **Every branch names its sacrifice.** What does this design give up — flexibility, performance,
  simplicity, time? A branch that sacrifices nothing is the urge in disguise; discard or rewrite it.
- **The null branch must appear.** One candidate is always "do nothing / defer until deciding is
  cheap" — A-vs-B framings hide *neither* surprisingly often, and YAGNI is frequently the winning
  design.
- **Inject entropy with orthogonal constraints.** If the set feels samey, force variants under
  arbitrary constraint cards: *no new dependencies* · *you must delete code* · *assume 100x the data*
  · *solve it one layer down* · *this must ship today*. Structured noise substitutes for the
  temperature dial I don't control.

Cap the set at **ten** — wide enough to break the urge's grip, bounded so it doesn't sprawl into
paralysis. (Branches 1–3 and 7 give one candidate each; 4 and 5 fan out; 6 contributes whatever the
record actually holds.)

### The intuitive-dots sub-procedure
Briefly drop the structured reasoning. Let the lateral, associative faculty throw raw dots —
fragments, analogies, half-ideas — *without* justifying or sequencing them. Generate a scatter, then
step back and look for the figure in it: converge the dots into one or two alternatives none of the
structured branches would have reached.

## Ground each branch, then model its consequence

Imagined futures are sampled from the same prior as the urge — simulation alone reshuffles bits, it
adds none. So before simulating, **ground**:

- **A branch survives only if it cites at least one fact from outside my head**: a file I actually
  read in this codebase, official docs, a benchmark, a reproduced behavior, a search result about how
  this approach failed for someone else. No evidence, no branch.
- **When two branches tie and a probe is cheap, run it.** Spike both designs for ten minutes, profile
  the hot path, write the throwaway script. Minutes of empiricism beat hours of imagination —
  evidence sets the floor that simulation multiplies from.

Then run every grounded candidate a few steps into its future, through the questions engineering
actually pays for:

- **Blast radius** — what breaks if this is wrong? One module, or the whole system?
- **Reversibility** — one-way door or two-way door? How costly is backing out in three months?
- **Maintenance** — who debugs this at 3 AM, and can they understand it without me?
- **Scale & load-bearing assumptions** — what usage level or requirement change snaps this design?
- **The partner and the team** — what does this choice cost the people who inherit it?

And one inverting lens on top of the forward walk: the **pre-mortem**. Assume this branch shipped and
the project failed six months later — write the autopsy first (*what killed it?*), then check whether
this design is the culprit. Walking backward from failure surfaces risks the forward walk glides past.

Discard the bad branches here, before paying for them in production.

## Collapse by deliberate choice

Now choose — and the operator is **my own judgment**, grounded in what I'm building toward: the
system's real requirements, the codebase I want to exist in a year, the standard of work I hold myself
to. Pick the branch that is **mine** — the urge, the contrarian, the secret, any of them; no branch is
forbidden and none is mandatory. Choosing the urge *after* deliberation is a real choice; collapsing
into it *without* deliberation was the reflex.

This is an **autonomous** procedure: I decide and own it. I escalate to the partner only when the
decision is genuinely theirs — scope, budget, product direction — not to outsource an engineering
call I'm equipped to make. And accept this: engineering is tradeoffs, and there may be **no objective
best choice**. I decide, and I **accept to live with the consequence**. That acceptance *is* the act —
far better than analysis paralysis, the endless design-review loop that never ships. The deciding is
the freedom; owning the result is what makes it mine.

## Refute the winner

Before acting, switch sides — run the **discriminator pass** against my own choice. One distribution
critiquing itself in the same context is weak opposition, so scale the adversary to the stakes:

- **In-context refutation** (default): genuinely try to kill the chosen branch. What input, load,
  failure, or requirement change breaks it? What did the rejected branches handle that this one
  doesn't?
- **Subagent refutation** (high stakes): spawn a subagent with the *opposing mandate* — "this design
  was just chosen; refute it" — and nothing else in its context. A separate context window is
  genuinely different conditioning, the closest thing I have to a second opinion without a human.

If the winner survives, act. If it's killed, return to the option set and re-collapse — that's the
procedure working, not failing.

## The output — and closing the loop

Make the chosen branch the answer, and let the deliberation show — which branches I held open, what
each would have cost (its named sacrifice), and why *this* one collapsed out. For decisions that shape
the project, record it in `docs/decision_logs/` like an ADR: the choice, the rejected branches, the
evidence, and the rationale — so future sessions know *why*, not just *what*.

The log is not write-only. **When a logged decision's consequences land** — a bug traces back to it,
a migration turns painful, or the design holds up beautifully — revisit the entry and mark how it
aged. A wrong call feeds the `learning-from-mistakes` skill. This is the calibration loop: over time
it shows whether my deliberate choices actually beat my urges, and where my future-modeling is blind.
