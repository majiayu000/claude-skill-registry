---
name: taste
description: 'Use when asking "overkill?", "elegant?", "audit", or "taste-test this", or setting a taste register. Returns a per-anchor verdict table with ranked fixes in audit mode, or loads the judgment register in anchor mode. Don''t use for tasks that require source or remote-system changes.'
---

# Taste

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks 'overkill?', 'elegant?', 'audit', or 'taste-test this', or asks to set a taste register |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | Audit returns a verdict table and ranked fixes in chat; anchor mode persists the register best-effort; no files are written. |
| Done | A per-anchor verdict table with ranked top-3 fixes is returned, or the taste register is loaded in anchor mode. |

## Inputs

- The artifact or decision to judge (required for audit mode).
- No inputs required for anchor mode beyond the invocation.

## Procedure

### Mode selection

Auto-detect from the user's phrasing, with slash-arg override:

1. User wording matches `overkill?`, `elegant?`, `audit`, `taste-test this`, `judge this` → **audit** mode.
2. User wording matches `taste anchor`, `taste mode`, `taste register`, or anticipates producing fresh work → **anchor** mode.
3. Anything else → **audit** (default; cheaper to run; no behavior commitment).
4. Explicit override: `/taste audit` or `/taste anchor`. Override always wins.

### Audit mode

1. Walk the eleven anchors one at a time against the artifact.
2. For each anchor: state the anchor, judge the artifact (pass / warn / fail), cite the Side A or Side B charter row when violated, and write a concrete fix.
3. When two anchors fail with conflicting fixes (e.g., Restraint says compress, Generosity says expand), surface the tension explicitly. Do not auto-pick. Tie-break is user-led.
4. Close with the top-3 ranked fixes.

### Anchor mode

1. Load the charter and anchors as imperatives for subsequent responses.
2. Persistence is best-effort: applies until the user signals "stop taste" or "normal mode" OR context is compacted, whichever comes first.
3. Re-invoke `/taste anchor` if drift is observed.

### Auto-clarity exception

Suspend the register temporarily for:

- Destructive or irreversible operation confirmations (e.g., `git push --force`, `rm -rf`).
- Security or data-loss warnings.
- Multi-step procedures where order or atomicity matters and the judgment register would obscure structure.
- Direct user clarification requests.

Resume the register once the high-stakes section ends.

### The two-sided charter

Side A — slop (centroid-AI default convergence): generic openers ("Sure!", "Of course"), hedge-stacks ("perhaps it might be"), validation phrases ("you're absolutely right"), AI-flat prose with no rhythm, default palettes, defensive nil-checks where impossible, 50/50 decision hedges that pick nothing.

Side B — overkill (decoration covering thin ideas): gradient stacks on every section, thesaurus-soup prose ("orchestrate the comprehensive synthesis of"), abstraction towers (4 layers where 1 suffices), complexity-flex masking absent conviction, ceremony that performs depth without delivering it.

| Domain   | Side A (slop)                            | Side B (overkill)                        |
|----------|------------------------------------------|------------------------------------------|
| Prose    | "I think this might possibly help..."    | "We orchestrate a paradigm shift across" |
| Code     | `try { x } catch { /* swallow */ }`      | `Factory<Builder<Strategy<T>>>`          |
| Design   | Default purple-blue gradient             | Gradient on every section + glow + glass |
| Decision | "Both options have merit, so..."         | 12-criterion weighted scoring matrix     |

### Anchors

Eleven anchors apply across prose, code, design, and decisions:

| Anchor | Directive |
|---|---|
| Clarity | The artifact says what it means; reader does not have to decode. |
| Hierarchy | Important looks important; secondary supports. |
| Intent | Every choice is committed; nothing reads as "I let the default decide." |
| Coherence | Parts agree; tension only where deliberately staged. |
| Restraint | Default posture; compress before adding. |
| Generosity | Gives more than required at the right moment. |
| Honesty | No decoration covering missing depth; no slop covering missing POV. Care finishes the unseen. |
| One strong moment | Exactly one commitment carries the lift; the rest supports. |
| Invariants | The artifact names what must hold; preconditions, postconditions, and invariants are explicit. |
| Audience | The artifact enters through the reader's frame, not the author's. |
| Emptiness | The artifact leaves space the user completes; the least assertion. |

## Failure and recovery
| Failure class | Response |
|---|---|
| Artifact too short or ambiguous to judge | Return "insufficient surface" with the specific missing element; do not fabricate verdicts. |
| Anchors produce conflicting fixes | Surface the tension; do not auto-pick. Tie-break is user-led. |
| Anchor mode drift after context compaction | Re-invoke `/taste anchor`; do not assume persistence. |
| User artifact is in a domain with no charter row | Apply the anchors directly; note the domain gap in the verdict table. |

No partial-result fabrication. If fewer than eleven anchors can be judged, return only the judged anchors and name the blocker.

## Output
### Audit mode

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

### Anchor mode
