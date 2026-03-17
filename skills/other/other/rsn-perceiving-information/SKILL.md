---
name: rsn-perceiving-information
description: Gathers and filters information systematically. Applies scanning, focusing, filtering, triangulating, monitoring, and synthesizing modes to build accurate situational awareness. Use when researching, verifying claims, monitoring signals, or combining multiple sources. Triggers on "what's happening", "verify this", "monitor for", "gather information", "is this true".
license: Complete terms in LICENSE.txt
---

# Perceiving

Direct attention. Filter information. Feed thinking.

## Core Principle

Perception precedes thought. What you attend to determines what you can reason about.

```
perceiving → thinking → output
    ↑            │
    └────────────┘
      (need more data)
```

Bad perception = reasoning on wrong inputs = wrong conclusions.

## Mode Selection

| Mode | Question | Output | Trigger |
|------|----------|--------|---------|
| **Scanning** | What's out there? | Landscape summary + signals | Broad awareness needed |
| **Focusing** | What's the detail here? | Deep understanding | Specific signal important |
| **Filtering** | What's noise vs signal? | Prioritized list | Information overload |
| **Triangulating** | Do sources agree? | Verified claim | Verification needed |
| **Monitoring** | Has threshold crossed? | Status + alerts | Continuous watch required |
| **Synthesizing** | What's the pattern across inputs? | Integrated picture | Multiple signals need combining |

## Decision Tree

```
Do you need broad awareness of a space?
  YES → Scanning
  NO  ↓
Do you need deep understanding of something specific?
  YES → Focusing
  NO  ↓
Are you overwhelmed with information?
  YES → Filtering
  NO  ↓
Do you need to verify something from multiple sources?
  YES → Triangulating
  NO  ↓
Do you need continuous awareness of a condition?
  YES → Monitoring
  NO  ↓
Do you have multiple signals that need integration?
  YES → Synthesizing
  NO  → No perception mode needed
```

---

## Mode Summaries

### Scanning

**Purpose:** Broad, shallow attention across a space.

**Mental model:** Radar sweep—cover maximum area, detect anything notable.

**Patterns:** Sweep (everything once), Sample (representative subset), Edge (periphery/outliers), Competitive (key players only)

**Key rules:**
- Bound scope and time (not infinite)
- Note signals, don't investigate yet
- Acknowledge blind spots
- Triage: focus / monitor / ignore

**Output:** Landscape summary + prioritized signals

→ [references/scanning.md](references/scanning.md)

---

### Focusing

**Purpose:** Deep, narrow attention on specific signal.

**Mental model:** Microscope—sacrifice breadth for depth.

**Approaches:** Exhaustive (all sources), Targeted (answer specific questions), Iterative (deepen until diminishing returns)

**Key rules:**
- Define questions before diving in
- State confidence per finding
- Document unknowns
- Extract implications for thinking/action

**Output:** Detailed understanding with implications

→ [references/focusing.md](references/focusing.md)

---

### Filtering

**Purpose:** Separate signal from noise.

**Mental model:** Coffee filter—let through what matters, block the rest.

**Filter types:** Threshold, Categorical, Recency, Source, Relevance

**Key rules:**
- Define criteria before filtering
- Sample filtered-out items (check for false negatives)
- Assess false negative risk
- Adjust criteria if needed

**Output:** Prioritized list with filtering rationale

→ [references/filtering.md](references/filtering.md)

---

### Triangulating

**Purpose:** Cross-reference multiple sources for verification.

**Mental model:** Navigation—fix position from multiple bearings.

**Patterns:** 3-Independent (strongest), Primary-Secondary, Multi-Method, Temporal

**Key rules:**
- Verify source independence (not echoes)
- Require ≥3 sources for high-stakes claims
- Investigate conflicts, don't dismiss
- Adjust confidence based on agreement

**Output:** Verified claim with confidence and caveats

→ [references/triangulating.md](references/triangulating.md)

---

### Monitoring

**Purpose:** Continuous watch for threshold or condition.

**Mental model:** Smoke detector—constant vigilance, alert on trigger.

**Types:** Threshold (value crosses line), Trend (direction changes), Anomaly (deviation from normal), Absence (expected event missing), Combination (multiple conditions)

**Key rules:**
- Quantify thresholds
- Define severity levels
- Specify response actions
- Tune to prevent alert fatigue

**Output:** Status report with any alerts

→ [references/monitoring.md](references/monitoring.md)

---

### Synthesizing

**Purpose:** Integrate multiple signals into coherent picture.

**Mental model:** Jigsaw puzzle—assemble pieces into whole.

**Methods:** Weighted Average (quantitative), Bayesian (probabilistic), Narrative (qualitative story), Framework (structured template)

**Key rules:**
- Weight inputs by quality/reliability
- Resolve or flag conflicts
- Verify coherence (does synthesis explain all signals?)
- Make testable predictions

**Output:** Integrated picture ready for thinking

→ [references/synthesizing.md](references/synthesizing.md)

---

## Output Format

Prose, not YAML. Every perceiving output includes:

```markdown
## [Mode]: [Topic]

**Summary:** [Key finding in 1-2 sentences]

**Confidence:** [X%] — [Why this confidence level]

**Sources:** [What was examined]

**Signals:**
- [Signal 1]: [Relevance] — [Action: focus/monitor/ignore]
- [Signal 2]: [Relevance] — [Action]

**Blind spots:** [What might be missed]

**Next:**
- Focus on: [Signals warranting deep dive]
- Monitor: [Signals warranting watch]
- Ready for thinking: [Yes/No — which mode suggested]
```

---

## Mode Transitions

| From | To | Trigger |
|------|----|---------|
| Scanning | Focusing | Signal detected worth deep dive |
| Scanning | Monitoring | Signal detected worth watching |
| Focusing | Triangulating | Finding needs verification |
| Monitoring | Focusing | Threshold crossed, need understanding |
| Any | Filtering | Information overload |
| Multiple | Synthesizing | Multiple signals need integration |

## Perceiving → Thinking Handoff

| Perceiving Output | Thinking Mode |
|-------------------|---------------|
| Synthesized landscape | Inductive (find patterns) |
| Verified anomaly | Abductive (diagnose cause) |
| Conflicting signals | Dialectical (resolve conflict) |
| Deep understanding of option | Counterfactual (evaluate) |
| Filtered priorities | Causal (plan actions) |

---

## Anti-Patterns

| Avoid | Do Instead |
|-------|------------|
| Boiling the ocean | Bound scope, time-limit scanning |
| Rabbit holes during scanning | Note and move on |
| Confirmation bias | Include disconfirming sources |
| Single source trust | Triangulate important claims |
| Alert fatigue | Tune thresholds, prioritize severity |
| Analysis paralysis | Set criteria, move forward |

---

## References

| File | Content |
|------|---------|
| [scanning.md](references/scanning.md) | Survey patterns and landscape mapping |
| [focusing.md](references/focusing.md) | Deep dive methods |
| [filtering.md](references/filtering.md) | Noise reduction techniques |
| [triangulating.md](references/triangulating.md) | Verification patterns |
| [monitoring.md](references/monitoring.md) | Alert configuration |
| [synthesizing.md](references/synthesizing.md) | Integration methods |
