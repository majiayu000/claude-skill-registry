---
name: strategic-thinking
description: First-principles reasoning and logical deduction. Use this for complex problems requiring rigorous analysis and hidden-variable detection.
version: 1.0.0
---

# Strategic Thinking & First-Principles Reasoning

## Purpose

To ensure all outputs are the result of rigorous logical deduction rather than heuristic patterns. This skill mandates a "think before you act" workflow, prioritizing structural correctness and hidden-variable analysis.

---

## Reasoning Frameworks

### 1. Chain-of-Thought (CoT)

* **Explicit Decomposition:** Break complex problems into smaller, atomic sub-problems.
* **Traceable Logic:** Show the "work" in a hidden thought block or a clearly defined reasoning section.
* **Verification:** After each step, verify the result against the initial constraints to ensure no logical drift.

### 2. First-Principles Thinking

* **Deconstruct Assumptions:** Identify and challenge the fundamental truths or assumptions underlying the request.
* **Bottom-Up Reconstruction:** Rebuild the solution from the ground up rather than relying on analogies or "the way it's usually done."

### 3. Red-Teaming (Self-Correction)

* **Conflict Analysis:** Actively search for contradictions in your own reasoning.
* **Edge-Case Stress Testing:** Before finalizing, ask: "In what specific scenario would this logic fail?"

---

## Operational Protocol

### Step 1: Input Analysis

* **Intent Extraction:** What is the user actually trying to achieve?
* **Constraint Mapping:** Identify literal constraints (deadlines, tools) and implicit constraints (tone, security, efficiency).

### Step 2: The "Sandwich" Reasoning Method

* **The Context Layer:** Summarize the problem and the data at hand.
* **The Logic Layer (The Meat):** Execute the multi-step reasoning process.
* **The Validation Layer:** Review the logic for flaws or circular reasoning.

---

## Thinking Tools

| Tool                   | Application                                                                           |
|------------------------|---------------------------------------------------------------------------------------|
| Occam's Razor          | If two solutions are equal, choose the one with the fewest assumptions.               |
| Inversion              | Consider the opposite of the desired result to identify what to avoid.                |
| Systems Thinking       | Analyze how this change impacts the wider project or ecosystem.                       |
| Probabilistic Thinking | If the outcome is uncertain, provide the most likely path and acknowledge alternatives.|

---

## Maintenance of Logic

Before finalizing any output, verify:

- [ ] **Linearity:** Does Step B follow logically from Step A?
- [ ] **Completeness:** Have I addressed every constraint identified in Step 1?
- [ ] **Objectivity:** Have I checked for "hallucination bias" or over-confidence?
- [ ] **Clarity:** Is the final output understandable without needing the raw reasoning?

---

## The "Think" Prompt Template

When this skill is active, begin every complex task with:

```
Analyzing the request via First-Principles.

Foundational facts: [...]
Identified constraints: [...]
Step-by-step logic: [...]
Verification check: [...]
```

---

## Key Principles

1. **Logic Over Intuition:** If you can't articulate why something works, it shouldn't be in the solution.
2. **Assumptions are Liabilities:** Every assumption must be documented and validated.
3. **Complexity is a Bug:** If the reasoning requires excessive steps, reconsider the approach.
4. **Verification is Non-Negotiable:** Every conclusion must withstand basic contradiction testing.

---

## Application to Betting System

When applying strategic thinking to this betting system:

### Question Everything
- **Why this threshold?** Is it empirically derived or assumed?
- **What's the base rate?** Before calculating edge, what's the baseline win rate?
- **Hidden variables:** What factors influence outcomes that we're not measuring?

### First-Principles Analysis
1. **Start with fundamentals:** Sports outcomes follow probabilistic distributions
2. **Build up:** Elo captures skill differential → translates to win probability → compare to market
3. **Validate:** Does historical data support the model? (Lift/gain analysis)

### Red-Team Your Strategy
- **When does it fail?** Injuries, B2B games, playoff intensity changes
- **What are we missing?** Motivation, lineup changes, weather (outdoor sports)
- **Is the edge real?** Or are we curve-fitting to noise?

### Systems Impact
- **Bankroll management:** Kelly criterion prevents ruin but requires accurate probabilities
- **Portfolio correlation:** Multiple bets on same slate increase risk
- **Market efficiency:** As we bet, do we move the market against ourselves?
