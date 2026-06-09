---
name: project-reasoning-lens-analysis
description: |-
  Use when analyzing a project through first-principles, systems, adversarial, cost, and user lenses.
  Triggers:
practices:
- ai-assisted-dev
- design-by-contract
hexagonal_role: supporting
consumes:
- project-context
produces:
- multi-lens-analysis.md
skill_api_version: 1
metadata:
  tier: judgment
  stability: experimental
  dependencies: []
context:
  window: fork
  intent:
    mode: task
output_contract: multi-lens-analysis.md
user-invocable: false
---
# project-reasoning-lens-analysis — Multi-Lens Project Analysis

> Run a project through six independent reasoning lenses. Each lens is a different
> question-set with a different blind spot, so what one lens cannot see, another
> catches. The value is in the *contrast between lenses*, not any single pass.

## ⚠️ Critical Constraints

- **Run lenses independently before synthesizing.** Each lens MUST be applied as
  its own pass, not blended into one "general analysis."
  **Why:** A single blended pass collapses into the dominant lens (usually
  systems or first-principles) and silently drops economic and user-centric
  findings — the exact insights the method exists to surface.
  - WRONG: "Here's my overall analysis of the project: ..." (one undifferentiated take)
  - CORRECT: "First-principles: ... | Systems: ... | Adversarial: ... | Economic:
    ... | User-centric: ... | Historical: ..." (six labeled, separable passes)

- **Every finding must name its lens and a concrete artifact/decision.**
  **Why:** Unattributed findings can't be cross-checked or prioritized; the
  synthesis step depends on knowing which lens produced each claim.

- **Synthesis must flag conflicts between lenses, not average them.**
  **Why:** The economic lens saying "cut this" while the user lens says "keep it"
  is the highest-value output — a real tradeoff the owner must decide. Averaging
  it away destroys the signal.

## Why This Exists

Solo analysis (human or agent) defaults to one favored mode of thinking and is
blind to the rest. An engineer over-indexes on systems and correctness; a founder
over-indexes on economics and users; a contrarian over-indexes on red-teaming.
Each blind spot is *structural*, not a matter of effort — you cannot see what your
default lens does not ask about. Forcing six fixed lenses converts a personality
bias into a checklist, so the analysis is complete regardless of who runs it.

## Quick Start

1. Gather the project context (README, design docs, code map, goals, constraints).
2. Run each of the six lenses below as a separate pass; record findings per lens.
3. Synthesize: collect cross-lens conflicts, agreements, and the prioritized list.
4. Write `multi-lens-analysis.md` using the Output Specification format.

## The Six Lenses (run each as its own pass)

### 1. First-principles
Strip away convention. What is the irreducible problem this project solves? If you
rebuilt from scratch knowing only the goal, what would you keep and what only
exists because of inherited assumptions?
- *Asks:* Why does this part exist at all? What's assumed but never justified?
- *Blind to:* operational reality, cost, what users actually do.

### 2. Systems-thinking
Map the parts, their couplings, and the feedback loops. Where are the bottlenecks,
single points of failure, hidden dependencies, and second-order effects?
- *Asks:* What happens downstream when X changes? Where do loops amplify?
- *Blind to:* whether the system is worth building; human/economic value.

### 3. Adversarial / red-team
Attack it. How does it fail, get abused, get gamed, or break under load and bad
actors? What's the worst realistic input and the most damaging assumption?
- *Asks:* How do I break this? What did the optimist skip?
- *Blind to:* the upside, the common-case happy path, value delivered.

### 4. Economic / cost
Follow the money and the effort. What does this cost to build, run, and maintain?
What's the opportunity cost, the ROI, the cheapest path to the same outcome?
- *Asks:* Is the value worth the spend? What's the marginal cost at scale?
- *Blind to:* correctness, elegance, long-tail edge cases.

### 5. User-centric
Stand in the user's shoes. What job are they hiring this for? Where does the real
workflow diverge from the designed one? What's confusing, slow, or unsafe for them?
- *Asks:* Does this actually help a real person do a real task?
- *Blind to:* internal architecture, cost structure, attack surface.

### 6. Historical
Look at lineage and precedent. What prior art, past attempts (here or elsewhere),
and earlier decisions in this very project shaped today's state? What was tried and
abandoned, and why?
- *Asks:* Who solved this before, and what did they learn? What's the scar tissue?
- *Blind to:* novel constraints unique to *now*; first-principles reframes.

**Verification checkpoint:** before synthesis, confirm you have at least one
concrete finding per lens. A lens with zero findings usually means it wasn't
actually applied — go back and run it.

## Synthesis (after all six passes)

1. **Agreements** — findings ≥2 lenses independently surfaced (highest confidence).
2. **Conflicts** — where lenses disagree; name the tradeoff and who must decide.
3. **Singletons** — a finding only one lens caught (often the real blind spot).
4. **Prioritized actions** — ranked by impact × confidence, each tagged with its
   lens(es).

## Output Specification

Write to `multi-lens-analysis.md`:

```markdown
# Multi-Lens Analysis: <project>

## Per-Lens Findings
### First-principles
- <finding> (artifact/decision: <ref>)
### Systems-thinking
- ...
### Adversarial / red-team
- ...
### Economic / cost
- ...
### User-centric
- ...
### Historical
- ...

## Synthesis
- **Agreements:** ...
- **Conflicts (tradeoffs to decide):** ...
- **Singletons (likely blind spots):** ...

## Prioritized Actions
1. <action> — impact: H/M/L, confidence: H/M/L, lenses: [...]
```

## Quality Rubric

- All six lenses applied as separate passes, each with ≥1 concrete, attributed
  finding.
- Synthesis explicitly lists at least one cross-lens conflict OR states none exist
  and why.
- Prioritized actions each carry impact, confidence, and source lens(es).

## Examples

- **A new internal CLI tool:** first-principles questions whether it should be a
  CLI at all; systems finds it couples to a fragile daemon; adversarial finds an
  unsanitized arg; economic finds it duplicates an existing tool (cheapest path:
  delete it); user-centric finds the default flags are wrong; historical finds a
  prior abandoned version. Synthesis conflict: economic says delete, user says the
  existing tool's UX is unusable — real tradeoff for the owner.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| All findings sound the same | Lenses blended into one pass | Re-run each lens in isolation |
| A lens produced nothing | Lens skipped or context too thin | Gather more context; re-apply that lens |
| Synthesis is just a list | Conflicts averaged away | Surface disagreements explicitly as tradeoffs |
| Findings can't be acted on | No artifact/decision attached | Tie each finding to a concrete ref |

## See Also

- `/red-team` — deep adversarial-only pass when lens 3 needs to go further.
- `/council` — multi-judge consensus when a decision needs ratification.
- `/pre-mortem` — failure-first stress test of a plan before work begins.
