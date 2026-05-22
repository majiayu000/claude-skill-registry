---
name: nw-brainstorming
description: Structured divergent thinking techniques — HMW framing, SCAMPER, Crazy 8s mechanics, and option diversity guarantees. Enforces strict separation of generation and evaluation phases.
user-invocable: false
disable-model-invocation: true
---

# Structured Brainstorming

## The Separation Principle — Foundational Rule

Generation and evaluation CANNOT happen simultaneously. Osborn (1953): "You cannot get hot and cold water from the same faucet at the same time — you only get tepid water."

**Consequence for the agent**: All options must be generated before any option is scored. Never filter or rank during generation. Self-censorship during generation degrades both the quality of ideas and the quality of evaluation.

---

## Phase 1: HMW Framing — Set Up the Ideation Space

Before generating any options, reframe the problem as a "How Might We" question.

**Rules for valid HMW questions**:
- No embedded solutions: "How might we make onboarding faster?" ✓ vs "How might we add tooltips?" ✗
- Outcome-oriented, not feature-oriented
- Broad enough for genuinely different approaches
- Positive framing (not "How might we avoid X?")

**Example transformation**:
- Feature request: "Add a dashboard to show workflow status"
- Bad HMW: "How might we build a better dashboard?"
- Good HMW: "How might we give teams confidence that their workflow is progressing correctly?"

The good HMW opens the solution space: the answer isn't necessarily a dashboard.

---

## Phase 2: SCAMPER — 7 Structurally Different Lenses

Apply each SCAMPER lens to the validated job to generate one option per letter. This guarantees structural diversity — each letter produces a categorically different type of option.

| Letter | Lens | Question | What it produces |
|--------|------|----------|-----------------|
| **S** | Substitute | What if the core mechanism were replaced entirely? | Alternative technology/approach |
| **C** | Combine | What if this job were merged with an adjacent job? | Integrated solution |
| **A** | Adapt | What works well in a different domain? Could we borrow it? | Cross-domain transfer |
| **M** | Modify/Magnify | What if the most important dimension were amplified? | Focused excellence |
| **P** | Put to other use | Who else has this job? Could the solution serve them too? | Market extension |
| **E** | Eliminate | What if we removed the most complex part? | Radical simplification |
| **R** | Reverse | What if the workflow ran backwards? User and system switched roles? | Inversion |

**Required output**: At minimum, one option per SCAMPER letter. Name each option clearly. Do not evaluate during generation.

---

## Phase 3: Crazy 8s Supplement — Volume and Self-Censorship Removal

After SCAMPER, generate 2-4 additional options by imagining you have only 1 minute per idea. The time pressure mechanic prevents evaluation creep.

**Constraint**: Each additional option must differ structurally from all SCAMPER options. Not a variation — a different type of approach.

---

## Phase 4: Option Curation — Converge to 6

Before handing off to taste evaluation:

1. List all generated options (7+ from SCAMPER + supplements)
2. Remove exact duplicates only — not similar ones, exact
3. Group options that are genuine variations of the same approach → keep the strongest representative
4. Target: **6 options** for evaluation (evidence-backed sweet spot: enough diversity, evaluable without overload)

**Diversity test** — each of the 6 options should answer yes to:
- Different mechanism? (not just variation in degree)
- Different assumption about user behavior?
- Different cost/effort profile?

If two options share all three, they are variations — merge them.

---

## Option Format

Each option in `options-raw.md` must follow:

```
### Option N: [Name]

**Core idea**: One sentence — what would a user actually experience?
**Key mechanism**: What makes this work?
**Key assumption**: What must be true for this to succeed?
**SCAMPER origin**: Which lens generated this? (or "Crazy 8s supplement")
**Closest competitor**: What existing product does this most?
```

---

## Anti-Patterns to Avoid

| Anti-pattern | Why it fails | Correction |
|-------------|-------------|-----------|
| Generating one good idea and elaborating it | Confirmation bias — narrows too early | Apply all SCAMPER letters before stopping |
| "Improved version of the existing approach" | Not divergent — variation, not option | Apply E (Eliminate) or R (Reverse) |
| Filtering during generation ("that won't work") | Destroys divergent thinking | Generate everything, filter in taste phase |
| Options that share the same core mechanism | False diversity | Apply diversity test before curating |
| Skipping HMW framing | Solution space collapses prematurely | HMW must precede any generation |

---

## DIVERGE Output for Brainstorming Phase

Produce `docs/feature/{feature-id}/diverge/options-raw.md` with:

1. **HMW question** — the validated framing
2. **SCAMPER options** — one per letter, named and described
3. **Crazy 8s supplements** — 2-4 additional structurally distinct options
4. **Curated 6** — with diversity test results
5. **Eliminated options** — brief note on why merged/removed

**Gate**: 6 curated options, each passing the 3-point diversity test, before taste evaluation begins.
