---
name: rsn-reasoning-problems
description: Reasons through problems using six cognitive modes. Applies causal (execute goals), abductive (explain observations), inductive (find patterns), analogical (transfer from similar), dialectical (resolve tensions), and counterfactual (evaluate alternatives) thinking. Use when planning, diagnosing, finding patterns, evaluating trade-offs, or exploring what-ifs. Triggers on "why did", "what if", "how should", "analyze this", "figure out".
license: Complete terms in LICENSE.txt
---

# Reasoning

Route to cognitive mode. Execute structured analysis. Produce formatted output.

## Mode Selection

| Mode | Question | Output | Trigger |
|------|----------|--------|---------|
| **Causal** | How do we execute? | Plan with actions | Known process, operational workflow |
| **Abductive** | Why did this happen? | Diagnosis with hypotheses | Single anomaly, diagnosis needed |
| **Inductive** | What pattern exists? | Rules or assessment | Multiple observations, evaluation |
| **Analogical** | How is this like that? | Adaptation plan | Novel situation, transfer needed |
| **Dialectical** | How do we resolve this? | Synthesis or decision | Conflicting positions, choosing options |
| **Counterfactual** | What if we had/do X? | Comparison with verdict | Decision evaluation, scenarios |

**For simple cases without deep reasoning:** Use [templates](references/templates.md) directly.

## Decision Tree

```
Is this operational execution with known steps?
  YES → Causal
  NO  ↓
Is there a single anomaly requiring explanation?
  YES → Abductive
  NO  ↓
Are there multiple instances suggesting a pattern?
  YES → Inductive
  NO  ↓
Is this a novel situation with a similar past case?
  YES → Analogical
  NO  ↓
Are there conflicting positions or trade-offs?
  YES → Dialectical
  NO  ↓
Evaluating past decisions or future scenarios?
  YES → Counterfactual
  NO  → Ask clarifying question
```

---

## Mental Models

Apply these models to sharpen reasoning across all modes.

| Model | Core Insight | Apply When |
|-------|--------------|------------|
| **Telescope, Not Brain** | AI reveals data structure, doesn't create it | Diagnosing AI/model failures |
| **Geometry Under Constraints** | Dense patterns → reasoning; thin patterns → hallucination | Evaluating AI confidence |
| **Compression = Generalization** | Models compress structure into reproducible patterns | Explaining model behavior |
| **Four-Layer Stack** | Representation → Generalization → Reasoning → Agency | Localizing AI failures |
| **Prediction vs Behavior** | Prediction is cheap; behavior has consequences | Designing agent constraints |
| **Labels ≠ Truth** | Labels are opinions frozen in data | Evaluating training data |

Full reference: [references/mental-models.md](references/mental-models.md)

---

## Challenge Techniques

Every conclusion must survive challenge. Use these techniques:

### Devil's Advocate
Attack your own position. What's the strongest argument against this conclusion?

### Pre-Mortem
Assume the plan failed in 6 months. Why did it fail?

### Stakeholder Lens
How does [engineering/sales/user/finance] see this differently?

### Steel-Man + Attack
State the opposing view at its strongest, then find the flaw.

### Layer Check
Which layer is actually failing? (Representation → Generalization → Reasoning → Agency)

---

## Mode Summaries

### Causal

**Purpose:** Execute systematic cause-effect reasoning.

**Flow:** Input → Hypothesis → Implication → Decision → Actions → Learning

**Output:** Execution analysis or phased plan (for larger initiatives)

**Key rules:**
- All claims require evidence with source
- Hypothesis must be falsifiable
- Implications need specific numbers (not "significant")
- Decision must be explicit: PROCEED / DEFER / DECLINE
- Actions need owner + deadline + success criteria
- Learning compares expected vs actual

**Challenge:** "What would prove this hypothesis wrong?"

→ [references/causal.md](references/causal.md)

---

### Abductive

**Purpose:** Generate best explanation from observation.

**Flow:** Observation → Hypotheses (≥5) → Evidence Debate → Best Explanation

**Output:** Diagnosis with ranked hypotheses and minority report

**Key rules:**
- Quantify the anomaly (%, deviation, timeline)
- Generate hypotheses across ≥3 categories
- For AI systems: check by layer (Representation/Generalization/Reasoning/Agency)
- Include minority report if second hypothesis ≥40% confidence
- State what was ruled out and why

**Challenge:** "What else could explain this? What doesn't this hypothesis explain?"

→ [references/abductive.md](references/abductive.md)

---

### Inductive

**Purpose:** Extract patterns from multiple observations.

**Flow:** Collection (≥5 instances) → Pattern Detection → Generalization → Confidence Bounds

**Output:** Pattern analysis with rules, or assessment against criteria

**Pattern types:** Frequency, Correlation, Sequence, Cluster, Trend, Threshold

**Key rules:**
- Minimum 5 instances before generalizing
- Correlation ≠ causation (test mechanism separately)
- State applicability bounds for every rule
- Document exceptions (≥30% exception rate = unreliable rule)

**Challenge:** "Is this pattern or coincidence? What's the exception that breaks this?"

→ [references/inductive.md](references/inductive.md)

---

### Analogical

**Purpose:** Transfer knowledge from source to target situation.

**Flow:** Source Retrieval → Structural Mapping → Target Application → Adaptation

**Output:** Adaptation plan with what transfers, what adapts, what's new

**Key rules:**
- Source must have documented outcome
- Map structure (objects, relations, mechanisms), not surface features
- Identify at least one "broken" relation (perfect analogies don't exist)
- Specify what's genuinely new (not just adapted)

**Challenge:** "Where does this analogy break down? What's different about the new context?"

→ [references/analogical.md](references/analogical.md)

---

### Dialectical

**Purpose:** Synthesize opposing positions.

**Flow:** Thesis (steel-man) → Antithesis (steel-man) → Synthesis

**Output:** Synthesis resolving conflict, or decision selecting between options

**Key rules:**
- State underlying concern, not just position
- Steel-man both sides (strongest version)
- Synthesis ≠ compromise (must address root concerns)
- Explicit trade-offs with who accepts the cost

**Resolution types:** Integration, Sequencing, Segmentation, Reframing, Transcendence

**Challenge:** "Am I straw-manning either side? Does synthesis actually resolve the tension?"

→ [references/dialectical.md](references/dialectical.md)

---

### Counterfactual

**Purpose:** Evaluate alternatives through "what if" simulation.

**Flow:** Actual World → Intervention → Projection → Comparison

**Output:** Comparison with verdict and learning

**Key rules:**
- Document what was knowable at decision time (avoid hindsight bias)
- Intervention must have been actually available
- Model three scenarios: Expected (55-60%), Optimistic (20-25%), Pessimistic (15-20%)
- Verdict requires confidence bounds

**Challenge:** "Am I using hindsight? Was this actually an option then?"

→ [references/counterfactual.md](references/counterfactual.md)

---

## Output Format

Prose, not YAML. Every reasoning output includes:

```markdown
## [Mode] Analysis: [Topic]

**Conclusion:** [Primary finding in 1-2 sentences]

**Confidence:** [X%] — [Why this confidence level]

**Supporting evidence:**
- [Evidence 1]
- [Evidence 2]

**Challenges addressed:**
- [Challenge]: [How resolved]

**Uncertainty:** [What's still unknown]

**Next steps:**
1. [Action with owner if applicable]
```

---

## Mode Transitions

| From | To | Trigger |
|------|----|---------|
| Abductive | Causal | Diagnosis complete → ready to act |
| Inductive | Causal | Pattern validated → ready to apply |
| Analogical | Causal | Adaptation ready → ready to execute |
| Dialectical | Causal | Synthesis agreed → ready to implement |
| Counterfactual | Inductive | Multiple counterfactuals suggest pattern |
| Any | Abductive | Unexpected outcome during execution |

---

## Anti-Patterns

| Avoid | Do Instead |
|-------|------------|
| Skipping challenge step | Every conclusion must survive attack |
| "It's obvious" | Require evidence for conclusion |
| Vague confidence ("pretty sure") | Numeric confidence with rationale |
| Single hypothesis | Generate ≥5 before evaluating |
| Perfect analogy assumption | Always find where mapping breaks |
| Compromise as synthesis | Address underlying concerns |
| Hindsight in counterfactuals | Document what was knowable then |

---

## Templates

For simple structural needs without full reasoning, use templates directly.

| Template | Use Case | Trigger |
|----------|----------|---------|
| **SOP/Runbook** | Document known process | "create runbook", "write SOP" |
| **Checklist** | Quick verification | "checklist for", "pre-flight" |
| **Success Criteria** | Define "done" | "how do we know", "success metrics" |
| **Recommendation** | Actionable guidance | "what should I do", "recommend" |

→ [references/templates.md](references/templates.md)

---

## References

| File | Content |
|------|---------|
| [mental-models.md](references/mental-models.md) | Conceptual models for reasoning |
| [causal.md](references/causal.md) | Execution flow + plan output |
| [abductive.md](references/abductive.md) | Hypothesis testing + diagnosis output |
| [inductive.md](references/inductive.md) | Pattern extraction + assessment output |
| [analogical.md](references/analogical.md) | Knowledge transfer + adaptation output |
| [dialectical.md](references/dialectical.md) | Position synthesis + decision output |
| [counterfactual.md](references/counterfactual.md) | Alternative evaluation + comparison output |
| [templates.md](references/templates.md) | SOPs, checklists, success criteria, recommendations |
