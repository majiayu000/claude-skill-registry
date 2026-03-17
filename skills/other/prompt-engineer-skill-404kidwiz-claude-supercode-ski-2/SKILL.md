---
name: prompt-engineer
description: Expert in designing, optimizing, and evaluating prompts for Large Language Models. Specializes in Chain-of-Thought, ReAct, few-shot learning, and production prompt management. Use when crafting prompts, optimizing LLM outputs, or building prompt systems. Triggers include "prompt engineering", "prompt optimization", "chain of thought", "few-shot", "prompt template", "LLM prompting".
---

# Prompt Engineer

## Purpose
Provides expertise in designing, optimizing, and evaluating prompts for Large Language Models. Specializes in prompting techniques like Chain-of-Thought, ReAct, and few-shot learning, as well as production prompt management and evaluation.

## When to Use
- Designing prompts for LLM applications
- Optimizing prompt performance
- Implementing Chain-of-Thought reasoning
- Creating few-shot examples
- Building prompt templates
- Evaluating prompt effectiveness
- Managing prompts in production
- Reducing hallucinations through prompting

## Quick Start
**Invoke this skill when:**
- Crafting prompts for LLM applications
- Optimizing existing prompts
- Implementing advanced prompting techniques
- Building prompt management systems
- Evaluating prompt quality

**Do NOT invoke when:**
- LLM system architecture → use `/llm-architect`
- RAG implementation → use `/ai-engineer`
- NLP model training → use `/nlp-engineer`
- Agent performance monitoring → use `/performance-monitor`

## Decision Framework
```
Prompting Technique?
├── Reasoning Tasks
│   ├── Step-by-step → Chain-of-Thought
│   └── Tool use → ReAct
├── Classification/Extraction
│   ├── Clear categories → Zero-shot + examples
│   └── Complex → Few-shot with edge cases
├── Generation
│   └── Structured output → JSON mode + schema
└── Consistency
    └── System prompt + temperature tuning
```

## Core Workflows

### 1. Prompt Design
1. Define task clearly
2. Choose prompting technique
3. Write system prompt with context
4. Add examples if few-shot
5. Specify output format
6. Test with diverse inputs

### 2. Chain-of-Thought Implementation
1. Identify reasoning requirements
2. Add "Let's think step by step" or equivalent
3. Provide reasoning examples
4. Structure expected reasoning steps
5. Test reasoning quality
6. Iterate on step guidance

### 3. Prompt Optimization
1. Establish baseline metrics
2. Identify failure patterns
3. Adjust instructions for clarity
4. Add/modify examples
5. Tune output constraints
6. Measure improvement

## Best Practices
- Be specific and explicit in instructions
- Use structured output formats (JSON, XML)
- Include examples for complex tasks
- Test with edge cases and adversarial inputs
- Version control prompts
- Measure and track prompt performance

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Vague instructions | Inconsistent output | Be specific and explicit |
| No examples | Poor performance on complex tasks | Add few-shot examples |
| Unstructured output | Hard to parse | Specify format clearly |
| No testing | Unknown failure modes | Test diverse inputs |
| Prompt in code | Hard to iterate | Separate prompt management |
