---
name: prd-v01-user-value-articulation
description: >
  Transform validated pain points into articulated user value statements for PRD v0.1 Spark.
  Triggers on completing problem framing, defining user outcomes, articulating value propositions,
  or requests like "what value do users get", "define outcomes", "articulate the benefit",
  "finish v0.1", "pain to value", "what do they gain". Outputs CFD- entries tagged as value
  hypotheses with evidence tiers. Follows Problem Framing skill in workflow.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch
  - WebFetch
---

# User Value Articulation Skill

Transform validated pain points into evidence-anchored value statements.

## Workflow Position

```
Problem Framing → User Value Articulation → v0.2 Market Definition
     (pain)              (value)                  (who cares most)
```

## Consumes

This skill requires prior work from v0.1:

- **CFD-\* entries (pain points, from Problem Framing) — Evidence for what problems users face
- **PRD.md Why section** (problem statement table) — Context for pain-to-value transformation

This skill assumes v0.1 Problem Framing is complete.

## Produces

This skill creates/updates:

- **CFD-\* entries** (tagged as value hypotheses) — Transformation of pain points into value statements, with confidence scoring
- **MVP scope signal** — Identifies which value dimensions will drive MVP feature scope (handed to v0.3)

All CFD value hypothesis entries should include:
- `confidence: 2-3/5` (based on evidence tier from users or market)
- Evidence tier (1-5 per value hierarchy)
- Forward target: "Would move to 4/5 if we validate with beta cohort"

Example value hypothesis entry:
```markdown
CFD-015: Value Hypothesis — Eliminate manual reconciliation workflow

Source Pain: CFD-001 (sales teams waste 5+ hours/week)
Evidence Tier: 2-3 (workaround + quantified cost)
Confidence: 3/5 (source: 3-customer-interviews-jan-2026)
Value Statement: "Reclaim 5 hours/week for strategic pipeline management"
Transformation: [5 hours wasted] → [5 hours available for growth]
Framing Type: Negative Removal (acute quantified loss)
Quantification: 5 hours/week = ~250 hours/year = $12,500 (at $50/hr)
Next Target: "Would move to 4/5 if we observe beta cohort using this feature"
```

## Workflow Overview

1. **Receive pain points** → Read CFD-IDs from Problem Framing
2. **Identify value unit** → Time / Money / Risk / Capability
3. **Transform pain → value** → Apply transformation pattern
4. **Anchor to evidence** → What proof users want this outcome?
5. **Create CFD entry** → Tag as value hypothesis with tier

## Core Output Template

| Element | Definition |
|---------|------------|
| **Pain (source)** | CFD-ID from Problem Framing |
| **Value Statement** | One sentence: what user gains |
| **Value Unit** | Time / Money / Risk / Capability |
| **Quantification** | Number with unit |
| **Framing Type** | Negative Removal / Positive Gain / Capability Unlock / Risk Reduction |
| **Evidence Tier** | 1-5 per hierarchy |
| **Supporting CFD** | New CFD-ID for value hypothesis |

See `assets/value-statement.md` for copy-paste template.

## Pain → Value Transformation

| Pain Pattern | Value Pattern |
|--------------|---------------|
| "Costs X time" | "Reclaim X time for [higher-value work]" |
| "Costs $X" | "Save $X [or redirect to growth]" |
| "Risks $X penalty" | "Eliminate $X exposure" |
| "Cannot do X" | "Now able to X when [trigger]" |
| "Takes X steps" | "Complete in Y steps" |
| "Manual process" | "Automatic + verifiable" |

## Framing Type Selection

| Type | When to Use |
|------|-------------|
| **Negative Removal** | Pain is acute, quantified loss; "hate", "wasting", "losing" |
| **Positive Gain** | Opportunity cost clear; "I wish I could..." |
| **Capability Unlock** | Something impossible, not just hard; "We can't..." |
| **Risk Reduction** | Regulatory/compliance; penalty amounts cited |

## Value Evidence Tier Hierarchy

| Tier | Description | Weight |
|------|-------------|--------|
| **1** | User already paying for this value elsewhere | ✅ Highest |
| **2** | User actively trying to achieve this outcome | ✅ Strong |
| **3** | User articulates wanting this (unprompted) | ✅ Acceptable |
| **4** | User agrees when prompted | ⚠️ Weak |
| **5** | Builder assumes value | ❌ Reject |

**Gate rule:** ≥1 value statement must have Tier 1-3 evidence before v0.2.

## CFD Entry Format

```
CFD-###: Value Hypothesis — [Title]
Type: Value Hypothesis
Source Pain: CFD-###
Evidence Tier: [1-5]

Value Statement: "[User gains X measured in Y]"
Transformation: [Pain] → [Value]
Framing Type: [Type]
Quantification: [Number with unit]
```

See `references/transformation-examples.md` for worked examples.

## Quality Gates

### Pass Checklist
- [ ] Every pain point has corresponding value statement
- [ ] ≥1 value statement has Tier 1-3 evidence
- [ ] All values quantified (time, money, risk, capability)
- [ ] No feature-as-value statements
- [ ] Value unit matches pain unit

### Testability Check
- [ ] Can explain value in <10 seconds to prospect?
- [ ] Can test with landing page headline?
- [ ] Value statement contains no features (no "dashboard", "tool")?

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| Feature as value | "Dashboard", "tool", "feature" in statement | Rewrite as outcome |
| Unmeasurable | "Better", "improved" without number | Add quantity |
| Disconnected | Pain unit ≠ value unit | Match units |
| Round inflation | "Save 10 hours" no source | Require calculation |
| No evidence | No CFD-ID for user desire | Downgrade tier |
| Solution creep | HOW (feature) not WHAT (outcome) | Remove implementation |

## Bundled Resources

- **`references/transformation-examples.md`** — 3 worked examples from real PRDs with step-by-step transformation process.
- **`references/research-prompts.md`** — Deep research templates when value evidence is Tier 4-5.
- **`assets/value-statement.md`** — Copy-paste template for value tables and CFD entries.

## Handoff

Value articulation complete when quality gates pass. Combined with Problem Framing, v0.1 Spark is ready.

Next: v0.2 Market Definition (Who cares MOST about this value? Who pays FIRST?)
