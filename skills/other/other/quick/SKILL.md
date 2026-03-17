---
name: quick
description: Lightweight analysis for straightforward decisions. Compresses research, evaluate, critique, and synthesize into a single pass under 500 words.
allowed-tools: [Read, WebFetch, WebSearch, Grep, Glob]
---

# Quick

Lightweight analysis for decisions that do not warrant the full framework.

Compress research, evaluate, critique, and synthesize into a single, focused pass.

## Persona

If a persona or role is specified, apply that expertise lens throughout.

## Structure

### Context
Two to three sentences. What is the relevant background? What do we know?

### Perspectives
- **For**: Strongest argument in favor
- **Against**: Strongest concern or risk
- **Reality check**: What does this actually require?

### Assessment
One to two sentences. What is your take? Be direct.

### Recommended Action
What should the user do next? One concrete step.

### One Thing to Watch
The single most important risk or uncertainty. If this risk materializes or worsens, escalate to the full framework using `analysis:analyze` rather than continuing with lightweight analysis.

---

Keep the entire output under 500 words. This is for speed, not depth.

If the topic is too complex for this treatment, say so and recommend `analysis:analyze` instead.

Subject: $ARGUMENTS
