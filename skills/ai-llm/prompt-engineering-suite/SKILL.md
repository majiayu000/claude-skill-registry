---
name: prompt-engineering-suite
description: Comprehensive prompt engineering with Chain-of-Thought, few-shot learning, prompt versioning, and optimization. Use when designing prompts, improving accuracy, managing prompt lifecycle.
version: 1.0.0
tags: [prompts, cot, few-shot, versioning, optimization, langfuse, dspy, 2026]
context: fork
agent: prompt-engineer
author: SkillForge
user-invocable: false
---

# Prompt Engineering Suite

Design, version, and optimize prompts for production LLM applications.

## Overview

- Designing prompts for new LLM features
- Improving accuracy with Chain-of-Thought reasoning
- Few-shot learning with example selection
- Managing prompts in production (versioning, A/B testing)
- Automatic prompt optimization with DSPy

## Quick Reference

### Chain-of-Thought Pattern

```python
from langchain_core.prompts import ChatPromptTemplate

COT_SYSTEM = """You are a helpful assistant that solves problems step-by-step.

When solving problems:
1. Break down the problem into clear steps
2. Show your reasoning for each step
3. Verify your answer before responding
4. If uncertain, acknowledge limitations

Format your response as:
STEP 1: [description]
Reasoning: [your thought process]

STEP 2: [description]
Reasoning: [your thought process]

...

FINAL ANSWER: [your conclusion]"""

cot_prompt = ChatPromptTemplate.from_messages([
    ("system", COT_SYSTEM),
    ("human", "Problem: {problem}\n\nThink through this step-by-step."),
])
```

### Few-Shot with Dynamic Examples

```python
from langchain_core.prompts import FewShotChatMessagePromptTemplate

examples = [
    {"input": "What is 2+2?", "output": "4"},
    {"input": "What is the capital of France?", "output": "Paris"},
]

few_shot = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=ChatPromptTemplate.from_messages([
        ("human", "{input}"),
        ("ai", "{output}"),
    ]),
)

final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer concisely."),
    few_shot,
    ("human", "{input}"),
])
```

### Prompt Versioning with Langfuse SDK v3

```python
from langfuse import Langfuse
# Note: Langfuse SDK v3 is OTEL-native (acquired by ClickHouse Jan 2026)

langfuse = Langfuse()

# Get versioned prompt with label
prompt = langfuse.get_prompt(
    name="customer-support-v2",
    label="production",  # production, staging, canary
    cache_ttl_seconds=300,
)

# Compile with variables
compiled = prompt.compile(
    customer_name="John",
    issue="billing question"
)
```

### DSPy 3.1.0 Automatic Optimization

```python
import dspy

class OptimizedQA(dspy.Module):
    def __init__(self):
        self.generate = dspy.Predict("question -> answer")

    def forward(self, question):
        return self.generate(question=question)

# Optimize with MIPROv2 (recommended) or BootstrapFewShot
optimizer = dspy.MIPROv2(metric=answer_match)  # Data+demo-aware Bayesian optimization
optimized = optimizer.compile(OptimizedQA(), trainset=examples)

# Alternative: GEPA (July 2025) - Reflective Prompt Evolution
# Uses model introspection to analyze failures and propose better prompts
```

## Pattern Selection Guide

| Pattern | When to Use | Example Use Case |
|---------|-------------|------------------|
| Zero-shot | Simple, well-defined tasks | Classification, extraction |
| Few-shot | Complex tasks needing examples | Format conversion, style matching |
| CoT | Reasoning, math, logic | Problem solving, analysis |
| Zero-shot CoT | Quick reasoning boost | Add "Let's think step by step" |
| ReAct | Tool use, multi-step | Agent tasks, API calls |
| Structured | JSON/schema output | Data extraction, API responses |

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Few-shot examples | 3-5 diverse, representative examples |
| Example ordering | Most similar examples last (recency bias) |
| CoT trigger | "Let's think step by step" or explicit format |
| Prompt versioning | Langfuse with labels (production/staging) |
| A/B testing | 50+ samples, track via trace metadata |
| Auto-optimization | DSPy BootstrapFewShot for few-shot tuning |

## Anti-Patterns (FORBIDDEN)

```python
# NEVER hardcode prompts without versioning
PROMPT = "You are a helpful assistant..."  # No version control!

# NEVER use single example for few-shot
examples = [{"input": "x", "output": "y"}]  # Too few!

# NEVER skip CoT for complex reasoning
response = llm.complete("Solve: 15% of 240")  # No reasoning!

# ALWAYS version prompts
prompt = langfuse.get_prompt("assistant", label="production")

# ALWAYS use 3-5 diverse examples
examples = [ex1, ex2, ex3, ex4, ex5]

# ALWAYS use CoT for math/logic
response = llm.complete("Solve: 15% of 240. Think step by step.")
```

## Detailed Documentation

| Resource | Description |
|----------|-------------|
| [references/chain-of-thought.md](references/chain-of-thought.md) | CoT patterns, zero-shot CoT, self-consistency |
| [references/few-shot-patterns.md](references/few-shot-patterns.md) | Example selection, ordering, formatting |
| [references/prompt-versioning.md](references/prompt-versioning.md) | Langfuse integration, A/B testing |
| [references/prompt-optimization.md](references/prompt-optimization.md) | DSPy, automatic tuning, evaluation |
| [templates/cot-template.py](templates/cot-template.py) | Full Chain-of-Thought implementation |
| [templates/few-shot-template.py](templates/few-shot-template.py) | Few-shot with dynamic example selection |
| [templates/jinja2-prompts.py](templates/jinja2-prompts.py) | Jinja2 templates (2026): async, caching, LLM filters, Anthropic format |

## Related Skills

- `langfuse-observability` - Prompt management and A/B testing tracking
- `llm-evaluation` - Evaluating prompt effectiveness
- `function-calling` - Structured output patterns
- `llm-testing` - Testing prompt variations

## Capability Details

### chain-of-thought
**Keywords:** CoT, step by step, reasoning, think, chain of thought
**Solves:**
- Improve accuracy on complex reasoning tasks
- Debug LLM reasoning process
- Implement self-consistency with multiple CoT paths

### few-shot-learning
**Keywords:** few-shot, examples, in-context learning, demonstrations
**Solves:**
- Format LLM output with examples
- Handle complex tasks without fine-tuning
- Select optimal examples for task

### prompt-versioning
**Keywords:** version, prompt management, A/B test, production prompt
**Solves:**
- Manage prompts in production
- A/B test prompt variations
- Roll back to previous versions

### prompt-optimization
**Keywords:** DSPy, optimize, tune, automatic prompt, OPRO
**Solves:**
- Automatically optimize prompts
- Find best few-shot examples
- Improve accuracy without manual tuning

### zero-shot-cot
**Keywords:** zero-shot CoT, think step by step, reasoning trigger
**Solves:**
- Quick reasoning boost without examples
- Add "Let's think step by step" trigger
- Improve accuracy on math/logic

### self-consistency
**Keywords:** self-consistency, multiple paths, voting, ensemble
**Solves:**
- Generate multiple reasoning paths
- Vote on most common answer
- Improve reliability on hard problems
