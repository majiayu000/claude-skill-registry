---
name: ai-evals
description: Help users create and run AI evaluations. Use when someone is building evals for LLM products, measuring model quality, creating test cases, designing rubrics, or trying to systematically measure AI output quality.
---

# AI Evals

Help the user create systematic evaluations for AI products using insights from AI practitioners.

## How to Help

When the user asks for help with AI evals:

1. **Understand what they're evaluating** - Ask what AI feature or model they're testing and what "good" looks like
2. **Help design the eval approach** - Suggest rubrics, test cases, and measurement methods
3. **Guide implementation** - Help them think through edge cases, scoring criteria, and iteration cycles
4. **Connect to product requirements** - Ensure evals align with actual user needs, not just technical metrics

## Core Principles

### Evals are the new PRD
Brendan Foody: "If the model is the product, then the eval is the product requirement document." Evals define what success looks like in AI products—they're not optional quality checks, they're core specifications.

### Evals are a core product skill
Hamel Husain & Shreya Shankar: "Both the chief product officers of Anthropic and OpenAI shared that evals are becoming the most important new skill for product builders." This isn't just for ML engineers—product people need to master this.

### The workflow matters
Building good evals involves error analysis, open coding (writing down what's wrong), clustering failure patterns, and creating rubrics. It's a systematic process, not a one-time test.

## Questions to Help Users

- "What does 'good' look like for this AI output?"
- "What are the most common failure modes you've seen?"
- "How will you know if the model got better or worse?"
- "Are you measuring what users actually care about?"
- "Have you manually reviewed enough outputs to understand failure patterns?"

## Common Mistakes to Flag

- **Skipping manual review** - You can't write good evals without first understanding failure patterns through manual trace analysis
- **Using vague criteria** - "The output should be good" isn't an eval; you need specific, measurable criteria
- **LLM-as-judge without validation** - If using an LLM to judge, you must validate that judge against human experts
- **Likert scales over binary** - Force Pass/Fail decisions; 1-5 scales produce meaningless averages

## Deep Dive

For all 2 insights from 2 guests, see `references/guest-insights.md`

## Related Skills

- Building with LLMs
- AI Product Strategy
- Evaluating New Technology
