---
name: ai-product-evaluation-design
description: Transition from traditional PRDs to "Evals" (evaluations) to guide AI model behavior. Use this skill when launching new AI features, debugging unpredictable model outputs, or moving from a prompted prototype to a production-ready agent.
---

# AI Product Evaluation Design

In the era of LLMs, product development moves from writing static specifications to defining "correctness" through Evals. Since models are stochastic, you cannot "fix a bug" with a single line of code; instead, you must "hill climb" toward better behavior by building robust datasets that measure model performance against your product goals.

## The Three-Tier Evaluation Framework

Depending on the complexity of the feature, use one or more of these evaluation methods:

### 1. Deterministic Evals (Pass/Fail)
Best for extraction, tool-calling, or objective facts.
- **Goal:** Verify the model extracts the exact right data.
- **Example:** If the user says "Remind me to eat at 7 PM," the JSON output for `time` must be `19:00`.
- **Metric:** Accuracy % (Total correct / Total prompts).

### 2. Human Preference Evals (Side-by-Side)
Best for tone, creativity, and visual design (like the "Canvas" layout).
- **Goal:** Compare two model versions (e.g., a baseline vs. a new fine-tuned model).
- **Process:** Present a prompt and two anonymized completions. Ask a human rater: "Which is better for [Specific Goal]?"
- **Metric:** Win Rate (The percentage of time the new model beats the baseline).

### 3. Model-Graded Evals (LLM-as-a-Judge)
Best for scaling quality checks without manual labor.
- **Goal:** Use a high-reasoning model (like o1) to grade the output of a faster, cheaper model.
- **Process:** Give the "Judge" model the rubric of what a "good" response looks like and ask it to score the "Student" model on a scale of 1-5.

## Step-by-Step Process for Designing Evals

### 1. Create the "Ground Truth" Dataset
Build a spreadsheet with the following columns to define the model's target behavior:
- **Input/Prompt:** What the user says (include diverse variations).
- **Baseline Behavior:** How the current model responds.
- **Ideal Behavior:** A hand-written "Golden Response" showing exactly what you want.
- **Rationale:** Why the ideal behavior is better (e.g., "It didn't trigger the UI when it should have stayed in chat").

### 2. Define Decision Boundaries
For agentic features (like Canvas or Task execution), define the "Trigger Boundary":
- **Trigger Scenarios:** Prompt: "Write a 5-page essay." Result: Model opens the document editor.
- **Non-Trigger Scenarios:** Prompt: "Who is the President?" Result: Model stays in the standard chat interface.

### 3. Identify Performance Regressions
When you optimize for one skill (e.g., "Being more concise"), you may accidentally "brain damage" another skill (e.g., "Formatting code correctly").
- Always run your new feature evals alongside a "General Intelligence" eval set to ensure core reasoning hasn't dropped.

## Examples

**Example 1: Deterministic Eval for a "Tasks" Tool**
- **Context:** An AI assistant that sets reminders.
- **Input:** "Remind me to call Mom in two hours." (Sent at 10:00 AM).
- **Expected Output:** `{ "action": "set_reminder", "content": "Call Mom", "time": "12:00" }`.
- **Application:** Run 100 variations of time-based language ("tonight," "in a bit," "next Tuesday") to ensure the extraction logic holds.

**Example 2: Preference Eval for Writing Style**
- **Context:** Improving the "friendly" tone of a document editor.
- **Input:** "Rewrite this paragraph to be more encouraging."
- **Model A:** "You did a good job on the report."
- **Model B:** "This report is a fantastic start! Your analysis of the data is really sharp."
- **Evaluation:** Human rater chooses Model B because it uses specific positive reinforcement instead of generic praise.

## Common Pitfalls

- **Measuring the Wrong Baseline:** Using a weak model as your baseline makes your new model look better than it actually is. Always test against the "state of the art" (SOTA).
- **Neglecting Diversity:** Training or testing only on "happy path" prompts. Include edge cases, slang, and non-English inputs to ensure the model doesn't fail in the wild.
- **The "Over-Refusal" Trap:** Teaching a model to be too safe or helpful can cause it to start refusing valid requests (e.g., the "body paradox" where a model refuses to set an alarm because it "doesn't have a physical body").
- **Ignoring Latency:** A model that is 5% more accurate but 10x slower is often a net-negative for the user experience. Always include "Time to First Token" as an eval metric.