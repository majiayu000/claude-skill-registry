---
name: theory-fidelity
description: "Audit whether the theories/methodologies a project claims to implement are faithfully operationalized — or name-dropped, partially built, distorted, or over-claimed. Source-grounds the load-bearing theories; tags the rest provisional. Run periodically alongside /framework-health."
metadata:
  instruction_budget: "55"
  framework_dependency: "mycelium"
  framework_dependency_note: "Designed to run within Mycelium (https://github.com/haabe/mycelium), where docs/theories.md provides the claimed-theory inventory. On a non-Mycelium project it audits whatever theory/methodology doc the project maintains; with no such doc it reports the absence. Install: /plugin install mycelium@haabe/mycelium."
---

# Theory Fidelity Audit

Most framework checks evaluate *process* (cycle health, gates) or *artifact performance* (evals, DORA). None of them ask the question this skill exists for: **for every theory a project claims to represent, is the mapped mechanism actually faithful to what the theory says — or is it theatre?** This is the audit of the theory→mechanism mapping itself.

The framework's own stated bar (`docs/theories.md`): *"every theory is mechanism-mapped … citations without mechanism-mapping are theatre."* This skill holds the project to that bar — including holding the theory doc to it.

## When to Use

- Quarterly, alongside `/mycelium:framework-health` (process health) — this is the theory-fidelity half.
- After adding/citing a new theory, or after editing a theory's mechanism (skill/gate/schema).
- When a citation looks decorative, or when a doc claims a mechanism you suspect doesn't exist.

## The Grading Rubric (three axes)

For each claimed theory, record:

1. **Representation** — `Mechanized` (a skill/gate/schema/canvas applies it) · `Prose-only` (cited + described, no mechanism) · `Absent`.
2. **Fidelity** (only if Mechanized):
   - `Faithful` — the mechanism matches the theory's real claims.
   - `Justified-Adaptation` — the mechanism deliberately diverges **and the rationale is documented in-repo**. Divergence with **no** documented rationale is `Distorted`, not Justified.
   - `Partial` — a faithful subset, with a named gap.
   - `Distorted` — diverges without rationale, or misrepresents the theory.
   - `Over-claim` — the theory doc claims more than the mechanism delivers (the project's own "theatre" failure mode).
   - `Name-only` — cited but not actually mechanized.
3. **Evidence-basis** — `source-grounded` (verified against the author's canonical work) · `model-knowledge` (from the agent's training — **provisional / consistency-only**).

## Workflow

1. **Build the claimed-theory inventory.** Read the project's theory doc (`docs/theories.md` for Mycelium). Tier it by load-bearing-ness if the doc does (Mycelium: Tier 1 load-bearing / Tier 2 integrated / Tier 3 citation-only). If no theory doc exists, report that absence and stop — you cannot audit fidelity against an unstated standard.

2. **Set the grounding standard (cost gate).** Source-grounding every theory is expensive; grading from model-knowledge alone is the **anti-pattern #7 trap at the meta-level** — you would be grading the project against your own paraphrase of the theory, which is consistency-as-evidence (see `harness/anti-patterns.md` #7). Default split:
   - **Load-bearing theories → source-grounded.** Use WebSearch/WebFetch to confirm the author's actual canonical claims; cite the source. Distortion in a load-bearing theory is the expensive failure.
   - **The rest → model-knowledge, every grade tagged provisional**, plus a `promotion candidate` flag for any that turn out load-bearing but under-mechanized.
   - Surface the chosen split to the user before a large run (this can fan out many agents).

3. **Map each theory to its mechanism — and READ the mechanism.** Open the cited skill/gate/schema/canvas before grading. A claim in the theory doc is not evidence of the mechanism's state; only reading the artifact is (anti-pattern #7 Read-before-claim). To grade `Justified-Adaptation`, search the repo (theory doc, philosophy doc, changelog, decision-log, the skill itself) for the documented rationale — absent rationale ⇒ `Distorted`.

4. **Grade** on the three axes. For each: the mechanism + path, representation, fidelity grade, evidence-basis, a 2–4 sentence justification citing **both** the theory's real claim and the repo mechanism, the specific gap/distortion, and a one-line fix.

5. **Premortem (how is THIS audit wrong?).** State it explicitly: model-knowledge grades inherit the same fidelity risk they measure; subagents may anchor on the project's own framing; single-pass grades have no adversarial second opinion. Name the lowest-regret findings (self-contradictions in-repo are unimpeachable regardless of theory knowledge).

6. **Devil's-advocate.** Challenge your own calls: is an "over-claim" really infidelity, or just doc imprecision? (By the project's own "no theatre" standard, an inaccurate mechanism-map *is* the failure.) Is a schema-absence a fidelity gap, or just a validation gap? (Usually the latter — say so.)

7. **Attribution-fix discipline (the Lopopolo rule).** When the audit finds a wrong citation, do **not** blind-sweep the name across the repo. Ground-truth **every** occurrence first — the same name is often attached to a *different, correct* claim elsewhere. A blind find-replace of a mis-attributed Reflexion citation once would have corrupted ~16 valid citations of the same author for an unrelated concept. Fix only the occurrences that actually carry the wrong claim.

8. **Log + recommend.** Write the scorecard to the decision-log (or a report file). Separate cheap doc-fidelity fixes from mechanism/schema builds; gate the latter on real need (JiT), not on the audit's enthusiasm.

## Output Format

```
## Theory-Fidelity Report

> **Verdict: [N theories · X Faithful · Y Partial · Z Distorted/Over-claim]** — [one-line headline; e.g. "engine faithful, theory doc is the weakest artifact"]

### Scorecard
| Theory (Author) | Representation | Fidelity | Basis | Mechanism / path |
|---|---|---|---|---|
| ... | Mechanized | **Distorted** | source-grounded | ... |

(Render Distorted / Over-claim / Name-only rows so they POP — leading bold — per Von Restorff; they are the rows the reader must not scroll past.)

### Findings (per flagged theory)
- <Theory>: <gap/distortion>, citing theory claim + repo mechanism. Evidence: source-grounded|provisional. Fix: <one line>.

### Cross-cutting patterns
- [e.g. doc-fidelity weaker than engine-fidelity; schema-gap cluster; citation errors]

### Premortem + Devil's-advocate
- [how this audit could be wrong; which grades are provisional; lowest-regret findings]

### Recommended actions (ranked; cheap doc fixes vs mechanism builds)
- ...
```

## Rules

- Never grade a load-bearing theory from model-knowledge alone — source-ground it, or tag the grade provisional and say so.
- Never blind-sweep an attribution fix — ground-truth every occurrence (step 7).
- A deliberate adaptation with documented rationale is `Justified-Adaptation`, not a failure — do not flag conscious divergence as infidelity.
- Surface large fan-outs for re-authorization before spending (scope checkpoint, G-P9).

## Theory Citations
- Argyris: triple-loop learning (the framework evaluating how faithfully it represents its own foundations).
- Goodhart: a cited theory becomes decoration the moment the citation, not the mechanism, is the target.
- Lanham et al. (2023): citations must be faithful, not after-the-fact rationalization — the discipline this skill enforces on the project.
- Mycelium anti-pattern #7 (consistency-as-evidence): grading a mechanism against one's own recollection of a theory is the meta-level instance; source-grounding is the escape.
