---
name: prompt-engineering
description: Optimize prompts for LLMs and AI systems with structured techniques, evaluation patterns, and synthetic test data generation. Use when building AI features, improving agent performance, or crafting system prompts.
keywords:
  - prompt engineering
  - LLM
  - system prompt
  - few-shot
  - chain-of-thought
  - synthetic data
triggers:
  - prompt engineering
  - system prompt
  - LLM optimization
  - prompt template
  - synthetic test data
---

# Prompt Engineering

Craft, test, and iterate prompts that deliver reliable outputs across LLMs. Covers prompt optimization techniques, structured prompt design, synthetic test data generation, and evaluation methodology.

## When to Use This Skill

- Building or optimizing prompts for AI-powered features
- Crafting system prompts for agents or assistants
- Improving reliability and consistency of LLM outputs
- Generating synthetic test data to validate prompt behavior
- Evaluating prompt performance across edge cases
- Designing prompt chains and pipelines

## Quick Reference

| Task | Load reference |
| --- | --- |
| Prompt techniques and patterns | `skills/prompt-engineering/references/techniques.md` |
| Synthetic test data generation | `skills/prompt-engineering/references/synthetic-data.md` |

## Workflow

1. **Research**: Gather the use case, constraints, and evaluation criteria. Audit existing prompts and model behaviors.
2. **Design**: Draft structured prompts with examples, constraints, and evaluation hooks. Plan experiments and measurement strategy.
3. **Generate test data**: Analyze prompt variables, generate diverse and realistic test cases to validate the prompt.
4. **Validate**: Run prompt trials, capture outputs, document adjustments. Iterate until quality thresholds are met.
5. **Deliver**: Hand off the final prompt with usage guidance and evaluation results.

## Core Principle

When creating prompts, always display the complete prompt text in a clearly marked section. Never describe a prompt without showing it. The prompt must be copyable and self-contained.

## Deliverables Checklist

For every prompt engineering task, produce:

- [ ] The complete prompt text (displayed in full, properly formatted)
- [ ] Explanation of design choices and techniques used
- [ ] Usage guidelines (model, temperature, parameters)
- [ ] Example expected outputs
- [ ] Test cases covering happy path, edge cases, and adversarial inputs

## Example Interactions

- "Optimize this system prompt for our code review agent"
- "Create a prompt for extracting structured data from support tickets"
- "Generate test cases to validate this classification prompt"
- "Design a prompt chain for multi-step document analysis"
- "Improve consistency of this summarization prompt"
