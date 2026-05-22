---
name: ai-eval-design-and-iteration
description: Develop "quizzes" (evals) to measure model performance on specific tasks. Use these benchmarks to guide fine-tuning, determine product UX patterns, and track performance improvements over time. Use this when launching a new AI feature, switching between model versions, or optimizing for high-stakes accuracy.
---

# AI Eval Design and Iteration

In traditional software, inputs and outputs are defined. In AI, inputs and outputs are fuzzy. Evals (evaluations) are the "unit tests" for AI products. They allow you to move from "vibes-based" development to metric-driven iteration. By building a rigorous "quiz" for your model, you can determine exactly how capable your product is and where it requires human-in-the-loop scaffolding.

## The Eval Workflow

### 1. Identify "Hero Use Cases"
Don't start with generic benchmarks (like MMLU). Instead, define the specific "hero" scenarios your product must master.
- Identify the 10–20 most common or high-value queries users will give your model.
- For each query, define what a "Perfect/Gold" answer looks like.
- Include edge cases where you expect the model to struggle (e.g., complex reasoning or specific formatting).

### 2. Design the "Quiz" (The Eval)
Create a set of tests to gauge how well the model knows the subject material.
- **Input:** The specific prompt or instruction.
- **Reference:** The "Gold" standard answer or a set of criteria (e.g., "Must mention X," "Must not exceed 200 words").
- **Scoring Mechanism:** Use a more powerful model (like O1 or GPT-4o) to grade the output of your production model based on your criteria.

### 3. Apply the "Hill Climbing" Process
Use the eval scores to guide your development cycle.
- Run the eval on your baseline model.
- **Fine-Tune:** If scores are low, provide 1,000+ examples of "Problem -> Good Answer" to the model to "teach" it the specific task.
- **Re-Test:** Run the eval again to see if performance increased.
- **Iterate:** If performance plateaus, break the problem down into smaller tasks (ensembling) and create specific evals for each sub-task.

### 4. Determine UX Based on Accuracy Thresholds
The "score" of your eval dictates the product's user interface. Kevin Weil's 60/95/99 Rule:
- **60% Accuracy:** Build a "Co-pilot" or "Draft" experience where the user must heavily edit the output.
- **95% Accuracy:** Build a "Human-in-the-loop" experience where the model does the work, and a human briefly reviews it.
- **99.5% Accuracy:** Build an "Agentic" or "Automated" experience where the model acts autonomously.

## Examples

**Example 1: Deep Research Tool**
- **Context:** Building a tool that researches a topic for 30 minutes and writes a 20-page report.
- **The Eval:** A prompt asking to "Compare the competitive landscape of fusion energy companies in 2024."
- **Criteria:** Does it mention Helion? Does it cite sources? Is the report 15+ pages?
- **Application:** If the model gets the history right but misses current news, the team adds an eval specifically for "Recency" and fine-tunes the browsing tool.

**Example 2: Customer Support Agent**
- **Context:** An automated agent to handle refunds and technical questions.
- **The Eval:** 500 historic tickets with verified "correct" resolutions.
- **Application:** The team finds the model is 98% accurate on refunds but only 70% on technical debugging. 
- **Output:** The UX is designed to automate refunds instantly but route all technical questions to a human agent with a "suggested" draft.

## Common Pitfalls

- **Using Static Evals:** AI models and user behaviors change every few months. If you don't update your "quiz" to reflect new capabilities or user errors, your metrics will become meaningless.
- **Over-Scaffolding for Today's Model:** Avoid building complex "if/then" code to fix a model's current mistake. In 2-3 months, a better model will launch that solves that mistake naturally. Build for the *next* model's capabilities.
- **Ignoring the "Human Analogy":** When an eval fails, ask: "How would I teach a human to do this?" If a human would need a checklist or a peer review, build that into your model's chain-of-thought process.
- **Relying on "Vibes" for Launch:** Never ship a model update because it "feels better" on three prompts. Only ship if the aggregate eval score shows statistically significant improvement.