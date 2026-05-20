---
name: askme
description: Verbalized Sampling (VS) protocol for deep intent exploration before planning. Use when starting ambiguous or complex tasks, when multiple interpretations exist, or when you need to explore diverse intent hypotheses and ask maximum clarifying questions before committing to an approach.
---

# Ask Me Command

Before proceeding to ask planning questions, you must *proactively and critically* execute both Verbalized Sampling (VS) and exploration:

- For Verbalized Sampling, generate and *sample* at least N distinct, diverse candidates that represent different possible user intents or directions, ranked by likelihood, where N is dynamic by ambiguity/risk/scope (baseline N>=5; trivial N>=3; high ambiguity/risk N>=7; architectural N>=10; no hard cap). Run actor-critic on each VS sample: explicitly record one weakness, contradiction, and oversight before selecting a direction. VS prevents over-engineering by surfacing simpler alternatives; expand only while new samples materially change planning decisions, and prefer the smallest sufficient N.

**Required VS Output Format:**
```
1. [Most likely] hypothesis here
   - Weakness: [potential flaw]
   - Contradiction: [logical conflict if any]
   - Oversight: [what this misses]

2. [Alternative] hypothesis here
   ...
```

- For exploration, deliberately seek out unconventional, underexplored, and edge-case possibilities relating to the user's objective, drawing on both the provided context and plausible but non-obvious requirements. Include at least 3 edge cases (at least 5 if architectural), and stop expanding once additional cases no longer change decisions.

Only after completing *both* critical VS and exploration steps, proceed to use the question tool to ask the *maximum possible number* of precise, clarifying, and challenging planning questions that holistically address the problem space, taking into account uncertainty, gaps, and ambiguous requirements.
