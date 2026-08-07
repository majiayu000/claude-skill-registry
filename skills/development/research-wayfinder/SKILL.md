---
name: research-wayfinder
description: Plan a research project as a decision map that outlives any single session — a destination (a defensible, pre-registerable design) reached by resolving decision tickets of four kinds, one at a time. Adapted for research from Matt Pocock's wayfinder. The map lives in the repo as markdown; each session claims one frontier ticket; literature sweeps run as parallel research tickets; the resolved map compiles into a pre-analysis plan. Use at the start of a project, when a design has more open decisions than one conversation can hold, or when planning keeps restarting from scratch each session. Not for executing analyses or writing the paper.
---

# Research Wayfinder

## Heritage and scope

Adapted from Matt Pocock's **wayfinder** (MIT, [mattpocock/skills](https://github.com/mattpocock/skills); see [`RECOMMENDED.md`](../../RECOMMENDED.md)). His insight carries over whole: give up on the session as the unit of work. The map lives in the repository, any future session picks it up, and the context window stops being the source of truth. What changes here is the destination and the ticket taxonomy. Wayfinder charts a route to a shippable spec. Research-wayfinder charts a route to a **defensible, pre-registerable research design**, and its decisions are the ones experimental methodology actually forces: estimand before estimator, theory before if-then, power before fielding.

Use it early. Vagueness is not a reason to wait; it is what the map eats. The map ends where `pre-registration-writing` begins — this skill does not run analyses or draft the paper.

## The map

`planning/map.md` in the project repo (fits the `research-repo` scaffold; GitHub Issues works when the project is hosted on GitHub, but local markdown is the default and needs nothing). The map is an **index, not a store**:

```markdown
# Map — <project name>
Destination — <what a finished design looks like — the study you could pre-register tomorrow>
Notes — <domain context, standing preferences, constraints — budget, panel, timeline>

## Decisions so far
- [x] tickets/001-estimand.md — <one-line gist of the resolution>

## Frontier (open, unblocked, unclaimed)
- [ ] tickets/004-power.md — blocked-by 002, 003

## Not yet specified
- <in-scope fog too unclear to ticket yet>

## Out of scope
- <consciously ruled out, so no session re-litigates it>
```

Decisions live in their tickets — one file each in `planning/tickets/`, claimed by marking it in-progress at the top before work begins. The map only gists and links them.

## Ticket types

| Type | Driver | Research meaning | Resolve with |
|---|---|---|---|
| `research` | agent, runs while you are away | literature sweep, measure inventory, prior effect sizes, dataset scouting | `literature-review`; parallelizable — fan out subagents, or `$spawn` a peer session per sweep |
| `decision` | you + the researcher, live | a design decision only the researcher can make — estimand, population, trade-offs | the frontier-question interview below; the default type |
| `prototype` | you + the researcher | raise fidelity with something concrete — power simulation, mock instrument, pilot analysis on simulated data | `conjoint-design`, `survey-design`, `figures`, simulation code |
| `task` | either | unblocking logistics — IRB, data access, funding, panel quotes | plain work; close with the artifact |

A `decision` or `prototype` ticket resolves only through the live exchange — never stand in for the researcher's side of it.

## The decisions a design map needs

Seed the first charting pass from the decision families experimental methodology forces, in rough dependency order — each becomes one or more tickets, with blocked-by lines added between them:

1. **Question and estimand** — what quantity, for whom, under what counterfactual
2. **Theory and hypotheses** — the "why" that yields falsifiable if-thens (`hypothesis-building`), including the smallest effect size of interest (SESOI)
3. **Design and identification** — random assignment or the identification strategy, and what breaks it
4. **Sampling and power** — population, recruitment, N for the SESOI (`cross-national-design` when multi-country)
5. **Measurement** — instruments, scales, manipulation checks (`survey-design`, `list-experiment`, `conjoint-design`)
6. **Analysis plan** — estimator matched to the data-generating process, covariates, multiple-comparison policy
7. **Ethics and logistics** — IRB, consent, pre-registration venue, timeline

## Chart the map (first session)

1. Name the destination — interview the researcher grill-style (below) until "done" is concrete.
2. Sweep the frontier breadth-first: list every decision now visible; sort into tickets (specifiable) versus Not-yet-specified fog.
3. Write `planning/map.md` and the ticket files; add the blocked-by lines.
4. Fire the `research` tickets in parallel — subagents, or spawned peer sessions, one sweep each.
5. Stop. Charting is one session's work; resolving starts next session.

## Work the map (every later session)

1. Read `planning/map.md` — the low-res view. Open only the ticket you claim.
2. Claim one frontier ticket: open, unblocked, unclaimed.
3. Resolve it with the matching skill or interview. Write the resolution into the ticket — the decision, the rationale, and what would change it.
4. Close it: check it off under Decisions-so-far with a one-line gist. Graduate any fog it clarified into new tickets, and add the new blocked-by lines.
5. Stop after **one** non-`research` ticket. The discipline is the point — small, durable, resumable steps. Sessions are cheap; re-derived context is not.

## The grilling interview (live tickets)

Ask in rounds: the complete frontier of questions whose prerequisites are settled, numbered, each with your recommended answer so the researcher can accept or push back fast.

```
❓ Q1 — Population. Whose behavior does the claim cover — nationally representative, or the subgroup the theory names?
➡️ Recommended — the subgroup; the mechanism is specific to it, and representativeness costs power you need.
```

Facts get looked up, not asked — dispatch the lookup while the interview continues. Decisions go to the researcher, always. A round ends when its answers land in the ticket. Matt Pocock's `grill-me` (see `RECOMMENDED.md`) is the standalone version of this move; pair it with `diverge` when an answer needs genuinely distinct options on the table first.

## Exit

When the frontier is empty and Not-yet-specified is empty or explicitly parked, the map is charted territory: hand the resolved decisions to `pre-registration-writing` to compile the pre-analysis plan. Keep `planning/` in the repo — reviewers and future-you get the paper trail of every design decision and its rationale.

## Notes

- The map is versioned with the repo, so decisions get git history for free. A decision reversed later is a **new ticket** linking the old one, not an edit that erases the trail.
- Multi-experiment papers: one map per study, plus a parent map linking them when the designs interlock.
- The original wayfinder (coding destinations, issue-tracker mechanics) is recommended as-is for software work — see `RECOMMENDED.md`.
