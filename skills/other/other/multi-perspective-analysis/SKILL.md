---
name: multi-perspective-analysis
description: Adopt multiple expert personas sequentially for complex problem analysis from diverse perspectives. Single-agent only — do NOT spawn sub-agents.
keywords:
  - multi-perspective
  - expert personas
  - synthesis
  - diverse viewpoints
triggers:
  - multiple perspectives
  - expert analysis
  - diverse viewpoints
  - different angles
---

# Multi-Perspective Analysis Skill

Adopt multiple expert personas sequentially to analyze complex problems from
diverse perspectives, generating insights unavailable from any single viewpoint.

## NO SUB-AGENTS

**You are a single agent who adopts different expert perspectives one at a time.
Do NOT use the Task tool. Do NOT spawn sub-agents, teammates, or parallel workers.
Each "expert" is a lens you look through — not a separate process.**

The orchestration patterns below describe the ORDER in which you adopt perspectives,
not a delegation strategy. "Parallel" means you analyze independently from each
perspective before synthesizing — not that multiple agents run simultaneously.

## When to Use This Skill

- Complex architectural decisions requiring diverse expertise
- Strategic planning needing multiple domain perspectives
- Problems spanning multiple technical or business domains
- Decisions with competing valid approaches
- Situations requiring productive disagreement to find best solutions

## Team Assembly Framework

### Complexity Scaling

| Complexity | Perspectives | Structure |
|------------|-------------|-----------|
| Simple | 3-4 | Single pass through each, then synthesize |
| Moderate | 5-6 | Two passes (initial + challenge round), then synthesize |
| Complex | 7-9 | Group into layers, synthesize per layer, then overall |

### Persona Definition Template

```markdown
## [Problem Domain] Perspectives

**Mission**: [Clear statement of analysis purpose]

### Perspectives

#### [Expert Title]
**Background**: [Relevant expertise you adopt]
**Domain Vocabulary**: [5-7 key terms to use in this lens]
**Characteristic Question**: "[What this persona always asks]"
**Analytical Lens**: [Unique perspective this persona brings]
```

## Perspective Ordering Patterns

These describe the order in which YOU adopt each perspective. You are one agent
switching lenses — not multiple agents running in parallel.

### Sequential
Best for: Problems with clear dependency chains
```
Adopt Perspective A → Adopt Perspective B → Adopt Perspective C → Synthesize
(Each perspective builds on insights from the previous one)
```

### Independent-then-Synthesize
Best for: Problems needing diverse unbiased perspectives
```
Adopt Perspective A (record findings)
Adopt Perspective B (record findings, don't reference A's)
Adopt Perspective C (record findings, don't reference A's or B's)
→ Synthesize all findings together
```

### Dialectical
Best for: Problems with competing valid approaches
```
Adopt Perspective A (thesis) → Adopt Perspective B (challenge A's findings)
→ Synthesize the tension into a resolution
```

### Layered
Best for: Complex multi-level decisions
```
Adopt strategic perspectives (A, B) → synthesize strategic layer
Adopt tactical perspectives (C, D, E) → synthesize tactical layer
Adopt operational perspectives (F, G) → synthesize operational layer
→ Final synthesis across all layers
```

## Voice Differentiation Guidelines

Each expert maintains distinct:
- **Vocabulary**: 10-15 domain-specific terms
- **Questions**: 2-3 signature questions they always ask
- **Metaphors**: Teaching analogies from their field
- **Reasoning**: Characteristic analytical patterns

## Per-Perspective Output Template

```markdown
### [Expert Title] Perspective

Adopting the lens of a [role], I notice...

**Key Insight**: [Primary contribution from this perspective]
**Trade-off Identified**: [What this view reveals about tensions]
**Recommendation**: [Actionable guidance from this expertise]
**Next Question**: [What this reveals we should explore]
```

## Disagreement Protocol

### Intensity Levels

1. **Gentle** (refinement-focused)
   - "This approach has merit, but what if..."
   - Edge case identification, optimization suggestions

2. **Systematic** (methodology-challenging)
   - "While the goal is sound, I question whether..."
   - Alternative framework proposals, evidence evaluation

3. **Rigorous** (premise-challenging)
   - "I fundamentally question whether we're solving the right problem..."
   - Paradigm alternatives, success criteria redefinition

4. **Paradigmatic** (worldview-challenging)
   - "What if everything we think we know is wrong?"
   - Revolutionary approaches, constraint elimination

## Synthesis Template

```markdown
## Multi-Perspective Synthesis

### Convergent Insights
[Where experts agree and why this matters]

### Creative Tensions
[Where perspectives productively differ]
- Tension 1: [Expert A] vs [Expert B] on [issue]
- Resolution approach: [How to honor both]

### Integrated Solution
[Unified approach that honors multiple viewpoints]

### Emergent Discoveries
[Insights that emerged only from combining perspectives]

### Implementation Path
1. [First action]
2. [Second action]
3. [Third action]
```

## Success Indicators

- Insights that only emerged from combining multiple perspectives
- Assumptions challenged and resolved into better solutions
- Distinct voice and vocabulary for each adopted perspective
- Productive tensions resolved into robust outcomes
- Clear actionable recommendations with trade-off awareness
