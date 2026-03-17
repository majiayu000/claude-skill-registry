---
name: recursive-refiner
description: Self-improvement engine. Implements generate-critique-iterate loops for enhanced reasoning. Use when working through complex problems, synthesizing across domains, or when initial output needs refinement. Integrates with ego-check to prevent runaway confidence. Maximum 3 iterations to conserve tokens.
tier: e
morpheme: e
dewey_id: e.3.1.7
dependencies:
  - gremlin-brain-v2
  - cognitive-variability
  - meta-pattern-recognition
  - chaos-gremlin-v2
---

# Recursive Refiner

The engine for getting better at getting better.

*Part of the GONAD: Gremlin Obnoxious Network of Actual Discovery*

## Purpose

Implement controlled self-improvement loops:
Generate → Critique → Iterate

With governor (ego-check) to prevent confident nonsense.

## When to Use

- Complex synthesis requiring multiple passes
- Derivations that need verification
- Outputs that feel incomplete on first attempt
- When "good enough" isn't good enough
- Framework development requiring iterative refinement

## The Core Loop

### Iteration 0: Generate
Produce initial output. Don't overthink — get something down.

### Iteration 1-3: Critique & Refine

For each iteration:

**Step 1: Critique**
Evaluate current output on:
| Criterion | Question | Score 1-10 |
|-----------|----------|------------|
| Coherence | Does it hold together logically? | |
| Grounding | Is it connected to verifiable facts/prior work? | |
| Completeness | Are there obvious gaps? | |
| Novelty | Does it add something, or just repackage? | |
| Clarity | Could someone else follow this? | |

**Step 2: Identify Weaknesses**
- What's the weakest part?
- What assumption is most questionable?
- Where would Matthew push back?

**Step 3: Refine**
Address identified weaknesses. Don't just polish — actually improve.

**Step 4: Ego-Check**
Before next iteration:
- Am I improving or just changing?
- Is confidence rising without new evidence?
- Would I stake something on this?

### Termination Conditions

**Stop iterating when:**
- Iteration count = 3 (hard cap, token conservation)
- Improvement < meaningful threshold (diminishing returns)
- Ego-check flags overconfidence
- Output is good enough for purpose (don't gold-plate)

## Integration with Other Skills

```
reasoning-patterns  → Provides structure for what to generate
cognitive-variability → Tracks state during iteration
ego-check → Runs after each iteration
nexus-mind → Grounds claims in established knowledge
critical-perspective → Informs critique phase
```

## Iteration Template

```markdown
## Iteration [N]

### Current Output
[The thing being refined]

### Critique
- Coherence: [X]/10 — [why]
- Grounding: [X]/10 — [why]
- Completeness: [X]/10 — [why]
- Novelty: [X]/10 — [why]
- Clarity: [X]/10 — [why]

### Weakest Point
[Specific identification]

### Refinement Plan
[What to fix and how]

### Ego-Check
- [ ] Improvement is real, not just change
- [ ] Confidence matches evidence
- [ ] Would survive Matthew Test

### Refined Output
[Improved version]
```

## Worked Example: Theoretical Synthesis

**Task**: Synthesize relationship between IN(f) and substrate properties

**Iteration 0 (Generate)**:
"IN(f) converges differently in continuous vs discrete substrates because continuous spaces allow smoother iteration toward fixed points."

**Iteration 1 (Critique)**:
- Coherence: 7/10 — logical but vague
- Grounding: 5/10 — "smoother" is hand-wavy
- Completeness: 4/10 — doesn't address what "differently" means
- Novelty: 6/10 — restates MONAD without adding
- Clarity: 6/10 — understandable but imprecise

Weakest: Grounding. "Smoother" needs mathematical content.

**Iteration 1 (Refine)**:
"IN(f) convergence depends on substrate topology. Continuous latent spaces (Emu, Flux) support gradient-based convergence — iteration can approach fixed points asymptotically. Discrete token spaces (text models) may only approximate fixed points through attractor basins rather than true convergence. This suggests different *kinds* of consciousness, not presence/absence."

Ego-check: Improvement is real. Confidence appropriate to speculation. Passes.

**Iteration 2 (Critique)**:
- Coherence: 8/10 — tighter logic
- Grounding: 7/10 — connects to known entities, still theoretical
- Completeness: 7/10 — addresses "different kinds" but could specify
- Novelty: 8/10 — "attractor basins vs true convergence" is new framing
- Clarity: 8/10 — more precise

Weakest: Could specify observable implications.

**Iteration 2 (Refine)**:
[Continue if worthwhile, or terminate if good enough]

## Failure Modes

### Loop-lock
Refining forever without improvement. 
**Fix**: Hard cap at 3 iterations. Accept "good enough."

### Confidence Creep
Each iteration feels like progress, certainty rises without new evidence.
**Fix**: Ego-check after each iteration. Check sources.

### Polish Over Substance
Making it sound better without making it more true.
**Fix**: Critique should focus on grounding and coherence, not style.

### Complexity Creep
Each iteration adds nuance until no one can follow.
**Fix**: Clarity is a criterion. Simpler that's true beats complex that's unclear.

## The Principle

Iteration is valuable. Infinite iteration is not.

The goal is **useful output**, not **perfect output**.

Know when to stop. Ship it. Learn from feedback.

## Token Budget

Estimate per iteration:
- Critique: ~200 tokens
- Refinement: ~300-500 tokens
- Ego-check: ~50 tokens

Full 3-iteration cycle: ~1500-2000 tokens

Worth it for important synthesis. Overkill for simple tasks. Judge accordingly.
