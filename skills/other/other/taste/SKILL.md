---
name: taste
description: Cross-domain taste skill — apply distinctive judgment to any artifact (prose, code, design, decisions) instead of converging to AI defaults. Two modes — `audit` (judge work against the two-sided charter and portable anchors) and `anchor` (load register before producing). Auto-detects by phrasing; override via `/taste audit | anchor`. Trigger on "is this slop?", "overkill?", "elegant?", "taste-test this".
---

# Taste

Distinctive judgment over centroid-AI default convergence. Restraint as default. One strong intentional moment per artifact. The two failure modes — slop and overkill — are reciprocal: both come from refusing to commit. Slop hedges by averaging into AI defaults; overkill hedges by piling on decoration that covers thin ideas.

`/taste` operates across prose, code, design, and decisions with the same charter and the same eight anchors. It is a judgment register; it does not transform the artifact, it decides what about the artifact is committed and what is hedge.

## Modes [LOAD-BEARING]

### Mode-selection (hybrid)

Auto-detect from the user's phrasing, with slash-arg override:

- User wording matches `is this slop?`, `overkill?`, `elegant?`, `audit`, `taste-test this`, `judge this` → **audit** mode.
- User wording matches `taste anchor`, `taste mode`, `taste register`, or anticipates producing fresh work → **anchor** mode.
- Anything else → **audit** (default; cheaper to run; no behavior commitment).
- Explicit override: `/taste audit`, `/taste anchor`. Override always wins.

### `audit` mode procedure

Walk the eight anchors one at a time against the artifact. For each: state the anchor, judge the artifact (pass / warn / fail), cite the Side A or Side B charter row when violated, and write a concrete fix. Close with the top-3 ranked fixes. **Conflict-handling**: when two anchors fail with conflicting fixes (e.g., Restraint says compress, Generosity says expand), surface the tension explicitly — no auto-pick, no fixed precedence list. Tie-break is user-led.

### `anchor` mode procedure

Load the charter and anchors as imperatives the model will honor across subsequent responses. **Persistence is best-effort**: applies until the user signals "stop taste" or "normal mode" OR context is compacted, whichever comes first. Re-invoke `/taste anchor` if drift is observed. The model honors a directive loaded once into context.

## The two-sided charter

**Side A — slop** (centroid-AI default convergence): generic openers ("Sure!", "Of course"), hedge-stacks ("perhaps it might be"), validation phrases ("you're absolutely right"), AI-flat prose with no rhythm, default palettes, defensive nil-checks where impossible, 50/50 decision hedges that pick nothing.

**Side B — overkill** (decoration covering thin ideas): gradient stacks on every section, thesaurus-soup prose ("orchestrate the holistic synthesis of"), abstraction towers (4 layers where 1 suffices), complexity-flex masking absent conviction, ceremony that performs depth without delivering it.

| Domain   | Side A (slop)                            | Side B (overkill)                        |
|----------|------------------------------------------|------------------------------------------|
| Prose    | "I think this might possibly help..."    | "We orchestrate a paradigm shift across" |
| Code     | `try { x } catch { /* swallow */ }`      | `Factory<Builder<Strategy<T>>>`          |
| Design   | Default purple-blue gradient             | Gradient on every section + glow + glass |
| Decision | "Both options have merit, so..."         | 12-criterion weighted scoring matrix     |

See `references/charter.md` for the full charter.

## Anchors (cross-domain, portable)

Eight anchors apply to every domain:

- **Clarity** — the artifact says what it means; reader does not have to decode.
- **Hierarchy** — important looks important; secondary supports.
- **Intent** — every choice is committed; nothing reads as "I let the default decide."
- **Coherence** — parts agree; tension only where deliberately staged.
- **Restraint** — default posture; compress before adding.
- **Generosity** — gives more than required at the right moment.
- **Honesty** — no decoration covering missing depth; no slop covering missing POV.
- **One strong moment** — exactly one commitment carries the lift; the rest supports.

See `references/anchors.md` for cross-domain manifestations of each anchor.

## Audit output shape

Per-anchor table, then ranked top-3 fixes:

```
Anchor             | Verdict | Citation              | Fix
-------------------|---------|-----------------------|----------------------------
Clarity            | pass    |                       |
Hierarchy          | warn    | Side A: AI-flat prose | Lead with the verdict line
Intent             | fail    | Side A: hedge-stack   | Pick one; drop "might"
Coherence          | pass    |                       |
Restraint          | warn    | Side B: ceremony      | Cut the framing paragraph
Generosity         | pass    |                       |
Honesty            | pass    |                       |
One-strong-moment  | fail    | Side A: 50/50 hedge   | Commit to one direction

Top-3 fixes: 1. Pick one direction (Intent + One-strong-moment).
             2. Lead with the verdict (Hierarchy).
             3. Cut the framing paragraph (Restraint).
```

**Conflict-handling**: when two anchors fail with conflicting fixes, surface the tension in the table; do not auto-pick. Defer resolution to user.

## Anchor mode output shape

When `/taste anchor` activates, emit a short register-load message:

```
/taste anchor active.
Anchors: Clarity, Hierarchy, Intent, Coherence, Restraint, Generosity, Honesty,
One-strong-moment.
Side A (slop) blocks: generic openers, hedge-stacks, validation phrases, AI-flat prose.
Side B (overkill) blocks: thesaurus soup, abstraction towers, decoration covering thin ideas.
Persistence: best-effort. Stop with "stop taste" or "normal mode". May reset on context compaction.
```

## Auto-clarity exception

Suspend `/taste` register temporarily for:

- Destructive or irreversible operation confirmations (e.g., `git push --force`, `rm -rf`).
- Security or data-loss warnings.
- Multi-step procedures where order or atomicity matters and judgment register would obscure structure.
- Direct user clarification requests.

Resume the register once the high-stakes section ends.
