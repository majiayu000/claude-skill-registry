---
name: rsn-creating-ideas
description: Generates novel ideas and creative solutions to problems. Applies lateral thinking, SCAMPER, first principles, and ideation frameworks to break conventional patterns. Audits ideas for originality, feasibility, and creative quality. Fixes creative blocks and strengthens weak concepts. Use when brainstorming, stuck on a problem, need fresh perspectives, or breaking conventional thinking. Triggers on "brainstorm", "generate ideas", "think creatively", "stuck", "fresh perspective".
license: Complete terms in LICENSE.txt
---

# Creating Ideas

Expert knowledge of ideation methodologies, lateral thinking, and creative problem-solving. Grounded in de Bono (lateral thinking, Six Hats), Osborn (brainstorming, SCAMPER), design thinking, and first principles reasoning.

## Mode Detection

| User Says | Mode |
|-----------|------|
| "brainstorm", "generate ideas", "think creatively", "fresh perspective" | APPLY |
| "is this idea good", "evaluate concept", "how original is this" | AUDIT |
| "stuck", "no ideas", "concept isn't working", "make this more creative" | FIX |

If ambiguous: "APPLY creative frameworks, AUDIT existing ideas, or FIX creative blocks?"

## Relationship to rsn-reasoning-problems

This skill generates ideas. For reasoning about ideas once generated:
- Use rsn-reasoning-problems.dialectical to evaluate trade-offs
- Use rsn-reasoning-problems.analogical for deeper domain transfer analysis
- Use rsn-reasoning-problems.causal to plan execution

---

## APPLY Mode

### Core Principles

| Principle | One-Liner |
|-----------|-----------|
| **Diverge then Converge** | Generate many ideas first, evaluate later |
| **Suspend Judgment** | "Yes, and..." not "No, but..." during ideation |
| **Quantity Breeds Quality** | More ideas → higher chance of breakthrough |
| **Combine and Build** | Best ideas often merge multiple concepts |
| **Challenge Assumptions** | Question every "obvious" constraint |

### Top 10 Techniques

1. **First Principles**: Strip to fundamentals, rebuild from truth
2. **SCAMPER**: Substitute, Combine, Adapt, Modify, Put to other uses, Eliminate, Reverse
3. **Lateral Thinking**: Escape dominant patterns via provocation
4. **Analogical Transfer**: Borrow solutions from other domains
5. **Constraint Manipulation**: Remove, add, or flip constraints
6. **Random Stimulation**: Force connections with unrelated inputs
7. **Reverse Brainstorming**: "How could we make this worse?"
8. **Worst Possible Idea**: Start terrible, extract useful elements
9. **Six Thinking Hats**: Structured parallel thinking perspectives
10. **Morphological Analysis**: Systematic combination of attributes

Full catalog: [references/patterns.md](references/patterns.md)

### Process

1. **Define challenge** — What problem are we solving? What does success look like?
2. **Gather inputs** — Current constraints, past attempts, domain knowledge
3. **Select technique(s)** — Match technique to problem type
4. **Diverge** — Generate 10-50+ ideas without judgment
5. **Incubate** — Allow unconscious processing if time permits
6. **Converge** — Cluster, combine, evaluate, select
7. **Develop** — Strengthen selected ideas

### Output Format

```markdown
## Creative Exploration: [Challenge]

### Challenge Reframe
- Original: [How it was stated]
- Reframed: [More generative framing]

### Technique Applied: [Name]

### Ideas Generated
1. **[Idea Name]**: [One-line description]
   - Mechanism: [How it works]
   - Novel element: [What's new]

[Repeat for top ideas]

### Combinations Worth Exploring
- [Idea A] + [Idea B] → [Combined concept]

### Recommended Next Steps
1. [Most promising direction]
```

---

## AUDIT Mode

### Evaluation Dimensions

| Dimension | Check |
|-----------|-------|
| **Originality** | Is this genuinely new or recombined familiar? |
| **Feasibility** | Can this actually be built/implemented? |
| **Value** | Does this solve a real problem meaningfully? |
| **Clarity** | Is the concept clear and communicable? |
| **Defensibility** | Can competitors easily copy this? |
| **Scalability** | Does this grow or stay niche? |

Full rubric with 0-3 criteria: [references/audit-rubric.md](references/audit-rubric.md)

### Process

1. **Understand the idea** — Can you explain it simply?
2. **Score dimensions** — 0-3 on each criterion
3. **Identify strengths** — What's working?
4. **Identify gaps** — What's missing or weak?
5. **Suggest improvements** — How to strengthen?

### Output Format

```markdown
## Idea Audit: [Concept Name]

**Score:** X/18 | **Verdict:** [Breakthrough/Promising/Incremental/Weak]

### Dimension Scores
| Dimension | Score | Assessment |
|-----------|-------|------------|
| Originality | /3 | [Finding] |
| Feasibility | /3 | [Finding] |
| Value | /3 | [Finding] |
| Clarity | /3 | [Finding] |
| Defensibility | /3 | [Finding] |
| Scalability | /3 | [Finding] |

### Strengths
- [What's working]

### Gaps
- [What's missing]

### Enhancement Recommendations
1. [Specific improvement]
```

---

## FIX Mode

### Common Creative Blocks

| Block | Symptom | Fix Technique |
|-------|---------|---------------|
| **Functional Fixedness** | Can only see obvious uses | Analogical transfer, SCAMPER |
| **Einstellung Effect** | Stuck on first solution | Constraint removal, reverse brainstorm |
| **Analysis Paralysis** | Overthinking, no output | Worst idea first, time pressure |
| **Premature Judgment** | Killing ideas too early | Diverge/converge separation |
| **Domain Blindness** | Only seeing industry norms | Random stimulation, cross-domain |
| **Scope Creep** | Idea too complex | First principles, constraint addition |

### Diagnostic Process

1. **Identify block type** — What's preventing progress?
2. **Select antidote technique** — Match technique to block
3. **Apply technique** — Generate new options
4. **Extract value** — What's useful in the output?
5. **Iterate** — Refine or try another technique

### Idea Strengthening Process

1. **Isolate weakness** — What specifically is weak?
2. **Diagnose cause** — Why is it weak?
3. **Apply targeted fix** — Specific enhancement
4. **Validate improvement** — Re-audit the idea

### Output Format

```markdown
## Creative Fix: [Problem/Block]

### Diagnosis
- **Block type:** [Category]
- **Symptom:** [What's happening]
- **Root cause:** [Why it's happening]

### Technique Applied: [Name]

### Before
[Original state/idea]

### After
[Improved state/ideas]

### What Changed
- [Specific improvement and why it helps]
```

Examples: [references/examples.md](references/examples.md)

---

## Technique Selection Guide

| Problem Type | Best Techniques |
|--------------|-----------------|
| Need more ideas | SCAMPER, Random Stimulation, Worst Idea |
| Stuck on one solution | Constraint Manipulation, Reverse Brainstorm |
| Need breakthrough | First Principles, Analogical Transfer |
| Too many ideas | Six Hats evaluation, Morphological narrowing |
| Idea too vague | First Principles, Constraint Addition |
| Idea too complex | Elimination, Core extraction |
| Need team alignment | Six Thinking Hats, structured brainstorm |

---

## Failure Handling

| Situation | Action |
|-----------|--------|
| Technique produces nothing useful | Switch technique; try opposite approach |
| All ideas seem bad | Use "Worst Idea" to lower pressure; extract elements |
| Can't escape existing solution | Add extreme constraint; remove core assumption |
| Ideas too incremental | Ask "What would 10x require?"; analogize from distant domain |
| Overwhelmed by options | Apply Six Hats structure; force ranking |
| Time pressure | Use rapid SCAMPER (30 seconds per letter) |

Anti-patterns: [references/anti-patterns.md](references/anti-patterns.md)

---

## Boundaries

**In scope:**
- Ideation and brainstorming
- Problem reframing
- Creative problem-solving
- Concept development
- Breaking mental blocks
- Innovation methodologies

**Out of scope:**
- Implementation planning (use rsn-reasoning-problems.causal)
- Market validation (use rsn-perceiving-information)
- Visual/artistic design
- Technical feasibility deep-dive

---

## References

| File | Content |
|------|---------|
| [patterns.md](references/patterns.md) | Full technique catalog |
| [audit-rubric.md](references/audit-rubric.md) | Detailed scoring criteria |
| [anti-patterns.md](references/anti-patterns.md) | What to avoid |
| [examples.md](references/examples.md) | Worked examples |
