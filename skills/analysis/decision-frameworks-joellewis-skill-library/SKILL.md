---
name: decision-frameworks
type: domain
family: executive
rigor: standard
description: "Use when choosing between mutually exclusive strategic paths or building a repeatable decision process—constructs Decision Matrices with probability estimates and runs Pre-Mortems."
keywords: "decision-making, uncertainty, mental-models, frameworks, analysis, probabilistic"
compatibility: "Claude Code and compatible agent products"
requires: []
enhances: ["strategy-clarity", "devils-advocate", "assumption-audit"]
sources_pdf: ["Thinking in Bets (Duke)", "How to Decide (Duke)", "The Great Mental Models v1 (Parrish)", "The Great Mental Models v2 (Parrish)", "Poor Charlie's Almanack (Munger)", "Useful Not True (Sivers)"]
sources_web: ["Farnam Street: Decision-making series", "Farnam Street: Mental Models"]
---

## Overview

Decision frameworks provide the structural rigor to make high-quality choices under uncertainty. This skill transforms decision-making from an emotional "gut feel" into a probabilistic process by decoupling outcomes from process, identifying cognitive biases, and utilizing a latticework of mental models to uncover second-order consequences.

## Guiding Principles

### Principle 1: Decisions are Bets (Source: Duke, *Thinking in Bets*)
Every decision is a bet on a specific future. Shift from binary "Right/Wrong" thinking to probabilistic "Confidence" thinking. Acknowledging uncertainty (e.g., "I am 70% confident") improves decision quality and reduces the sting of bad outcomes.

### Principle 2: Anti-Resulting (Source: Duke, *Thinking in Bets*)
Do not judge a decision solely by its outcome. A "good" result can come from a "bad" process due to luck. Evaluate the *process* used at the time of the decision, not the final result.

### Principle 3: Latticework of Models (Source: Munger, *Poor Charlie's Almanack*)
You cannot make wise decisions with a single mental model. You must have a "latticework" of models from multiple disciplines (math, physics, biology, psychology) to avoid the "Man with a Hammer" syndrome.

### Principle 4: Circle of Competence (Source: Parrish, *Great Mental Models v1*)
Know the boundaries of your knowledge. Decisions made outside your circle of competence have a much higher risk of failure. If you must decide outside your circle, seek a partner with the missing expertise.

### Principle 5: Pragmatic Truth (Source: Sivers, *Useful Not True*)
When faced with multiple interpretations of a situation, choose the one that is most *useful* for making progress, even if it is not "100% true." Belief is a tool for action.

## When to Use This Skill

- When a decision involves significant "downside" risk or high uncertainty.
- When choosing between mutually exclusive strategic paths.
- When building a "Decision Journal" for organizational learning.
- When an individual or team is stuck in "Analysis Paralysis."

## When NOT to Use This Skill

- For low-stakes, reversible decisions (e.g., "Type 2" decisions). (Source: Bezos, Amazon Letter)
- When speed is the primary requirement and the cost of being wrong is negligible.

## Core Process

### Step 1: Frame the Decision
Clearly state the choice being made and the desired outcome.
1. **The Happiness Test:** Will this decision matter in 10 minutes? 10 months? 10 years? Use the result to determine how much time to spend on the decision. (Source: Duke, *How to Decide*)
2. **First Principles:** Strip away the analogies and conventional wisdom. What are the fundamental truths of this situation? (Source: Parrish, v1)

### Step 2: Build the Decision Matrix
Map the possibilities and probabilities. (Source: Duke, *How to Decide*)
1. **Options:** List all possible paths (including "Do Nothing").
2. **Outcomes:** For each path, list the possible results (Best, Worst, Average).
3. **Probabilities:** Assign a percentage chance to each outcome.

### Step 3: Apply Mental Model Stress-Tests
Use the latticework to uncover hidden flaws. (Source: Munger, Parrish)
1. **Inversion:** What would cause this decision to be a disaster? How do we avoid that?
2. **Second-Order Thinking:** Ask "And then what?" for the preferred outcome. What are the long-term consequences?
3. **Occam's Razor:** If there are two competing solutions, is the simpler one more likely to be correct? (Source: FS Blog)

### Step 4: Perform a Pre-Mortem
Imagine the decision has failed 12 months from now. (Source: Duke, *How to Decide*)
1. **Identify the Cause:** Why did it fail? (e.g., market shift, execution gap, technical debt).
2. **Mitigate:** Adjust the current plan to prevent those identified failure modes.

### Step 5: Document in the Decision Journal
Record the reasoning *at the time* to prevent hindsight bias. (Source: Duke, *Thinking in Bets*)
1. **The Context:** What did we know at the time?
2. **The Reasoning:** Why did we choose this path?
3. **The Confidence:** What was our percentage confidence in the result?

## Frameworks & Models

### The Decision Matrix (Source: Duke, *How to Decide*)
A structured table mapping:
- Option A vs. Option B.
- Probabilities of Success/Failure.
- Expected Value (Value * Probability).

### Hanlon's Razor (Source: FS Blog)
"Never attribute to malice that which is adequately explained by stupidity (or incompetence)." Use this to prevent emotional bias in interpersonal or competitive decisions.

### Map vs. Territory (Source: Parrish, *Great Mental Models v1*)
The model (the map) is not the reality (the territory). Always check if the "map" you are using for a decision matches the actual "territory" on the ground.

## Cross-Skill Invocations

- **REQUIRED SUB-SKILL:** `devils-advocate` — To stress-test the preferred option in the matrix.
- **RECOMMENDED SUB-SKILL:** `assumption-audit` — To validate the probabilities assigned in Step 2.
- **RECOMMENDED SUB-SKILL:** `mental-model-library` — For a broader set of models beyond the core three.

## Common Mistakes

1. **Resulting:** Judging a decision based on its outcome rather than the process. (Source: Duke, Ch. 1)
2. **Analysis Paralysis:** Spending more time on a decision than the "Happiness Test" justifies. (Source: Duke, Ch. 5)
3. **Overconfidence:** Stating 100% certainty in an uncertain future. (Source: Duke, Ch. 2)
4. **Hindsight Bias:** Believing you "knew it all along" after the result is known. (Source: Duke, Ch. 6)

## Diagnostic Checklist

- [ ] Have we decoupled the outcome from the decision process?
- [ ] Have we assigned probabilistic confidence scores (e.g., 60%, 80%) to our claims?
- [ ] Have we performed an "Inversion" or "Pre-Mortem" to identify failure paths?
- [ ] Is this decision within our "Circle of Competence"?
- [ ] Have we considered second-order consequences ("And then what?")?

## Sources

- Duke, *Thinking in Bets*, Ch. 1, 2, 6 — Resulting, Confidence, Decision Journal.
- Duke, *How to Decide*, Ch. 3, 4, 5 — Decision Matrix, Pre-Mortem, Happiness Test.
- Parrish, *Great Mental Models v1*, Ch. 1, 2, 4 — First Principles, Circle of Competence, Second-Order Thinking.
- Munger, *Poor Charlie's Almanack*, Ch. 2 — Latticework, Inversion.
- Sivers, *Useful Not True* — Pragmatic belief as a decision tool.
