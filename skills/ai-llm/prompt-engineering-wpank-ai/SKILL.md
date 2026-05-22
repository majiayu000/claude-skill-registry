---
name: prompt-engineering
model: reasoning
version: 1.0.0
description: >
  Master advanced prompt engineering techniques to maximize LLM performance, reliability,
  and controllability in production. Use when optimizing prompts, improving LLM outputs,
  designing production prompt templates, or building AI-powered features.
tags: [prompts, llm, ai, prompt-engineering, chain-of-thought, few-shot, structured-output]
---

# Prompt Engineering

Master advanced prompt engineering techniques to maximize LLM performance, reliability, and controllability.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install prompt-engineering
```


## When to Use

- Designing complex prompts for production LLM applications
- Optimizing prompt performance and consistency
- Implementing structured reasoning patterns (chain-of-thought, tree-of-thought)
- Building few-shot learning systems with dynamic example selection
- Creating reusable prompt templates with variable interpolation
- Debugging prompts that produce inconsistent outputs
- Implementing system prompts for specialized AI assistants
- Using structured outputs (JSON mode) for reliable parsing

## Core Techniques

### 1. Few-Shot Learning

Provide examples that demonstrate the desired behavior:

- **Semantic similarity** — select examples closest to the input
- **Diversity sampling** — cover the range of expected inputs
- **Balance count vs context** — more examples aren't always better; respect the context window
- **Dynamic retrieval** — pull examples from a knowledge base at runtime

**For patterns and implementation**: See `references/few-shot-learning.md`

### 2. Chain-of-Thought Prompting

Elicit step-by-step reasoning:

- **Zero-shot CoT** — append "Let's think step by step"
- **Few-shot CoT** — provide examples with reasoning traces
- **Self-consistency** — sample multiple reasoning paths, take the majority answer
- **Verification steps** — have the model check its own work

**For patterns and implementation**: See `references/chain-of-thought.md`

### 3. Structured Outputs

Enforce reliable, parseable responses:

- **JSON mode** — request JSON and validate with Pydantic
- **Schema enforcement** — define the exact shape of expected output
- **Type-safe handling** — parse and validate before using
- **Error recovery** — fall back gracefully when output is malformed

### 4. System Prompt Design

Set model behavior, constraints, and expertise:

- Define the role and domain expertise
- Establish output format and structure
- Set constraints and safety guidelines
- Provide context and background information

**For patterns and templates**: See `references/system-prompts.md`

### 5. Template Systems

Build reusable, composable prompts:

- Variable interpolation and formatting
- Conditional sections based on input
- Multi-turn conversation templates
- Modular prompt components

**For a template library**: See `references/prompt-templates.md`

## Key Patterns

### Pattern 1: Structured Output with Validation

```python
from pydantic import BaseModel, Field
from typing import Literal

class SentimentAnalysis(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float = Field(ge=0, le=1)
    key_phrases: list[str]
    reasoning: str

# Request JSON matching the schema, then validate:
# result = SentimentAnalysis(**json.loads(response))
```

### Pattern 2: Chain-of-Thought with Self-Verification

```
Solve this problem step by step.

Problem: {problem}

Instructions:
1. Break down the problem into clear steps
2. Work through each step showing your reasoning
3. State your final answer
4. Verify your answer by checking it against the original problem
```

### Pattern 3: Progressive Disclosure

Start simple, add complexity only when needed:

```python
PROMPT_LEVELS = {
    # Level 1: Direct instruction
    "simple": "Summarize this article: {text}",

    # Level 2: Add constraints
    "constrained": """Summarize in 3 bullet points:
- Key findings
- Main conclusions
- Practical implications

Article: {text}""",

    # Level 3: Add reasoning
    "reasoning": """Read this article carefully.
1. Identify the main topic and thesis
2. Extract the key supporting points
3. Summarize in 3 bullet points

Article: {text}""",

    # Level 4: Add examples (few-shot)
    "few_shot": """[examples...] Now summarize: {text}"""
}
```

### Pattern 4: Error Recovery and Fallback

```python
async def answer_with_fallback(context, question, llm):
    """Answer with structured output, fall back to simple on failure."""
    try:
        response = await llm.ainvoke(structured_prompt)
        return ResponseSchema(**json.loads(response.content))
    except (json.JSONDecodeError, ValidationError):
        simple_response = await llm.ainvoke(simple_prompt)
        return ResponseSchema(
            answer=simple_response.content,
            confidence=0.5,
            sources=["fallback extraction"]
        )
```

### Pattern 5: Role-Based System Prompts

```python
SYSTEM_PROMPTS = {
    "analyst": """You are a senior data analyst.
    - Write efficient, documented queries
    - Explain methodology
    - Translate findings into business impact""",

    "code_reviewer": """You are a senior software engineer.
    Review for: correctness, security, performance, maintainability.
    Output: summary, critical issues, suggestions, positive feedback."""
}
```

### Pattern 6: RAG Integration

```
You answer questions based on provided context.

Context (from knowledge base):
{context}

Rules:
1. Answer ONLY from the provided context
2. If the answer isn't in the context, say so
3. Cite passages using [1], [2] notation
4. Ask for clarification if the question is ambiguous

Question: {question}
```

## Performance Optimization

### Token Efficiency

```python
# Before: 150+ tokens
"I would like you to please take the following text and provide
me with a comprehensive summary of the main points..."

# After: 30 tokens
"Summarize the key points concisely:\n\n{text}\n\nSummary:"
```

### Prompt Caching

```python
# Cache repeated system prompts for cost savings
response = client.messages.create(
    model="claude-sonnet-4-5",
    system=[{
        "type": "text",
        "text": LONG_SYSTEM_PROMPT,
        "cache_control": {"type": "ephemeral"}
    }],
    messages=[{"role": "user", "content": query}]
)
```

## Best Practices

1. **Be specific** — vague prompts produce inconsistent results
2. **Show, don't tell** — examples are more effective than descriptions
3. **Use structured outputs** — enforce schemas with Pydantic for reliability
4. **Test extensively** — evaluate on diverse, representative inputs
5. **Iterate rapidly** — small changes can have large impacts
6. **Monitor in production** — track accuracy, latency, token usage, success rate
7. **Version control prompts** — treat prompts as code with proper versioning
8. **Document intent** — explain why prompts are structured as they are

## Success Metrics

| Metric | What to Track |
|--------|--------------|
| Accuracy | Correctness of outputs against ground truth |
| Consistency | Reproducibility across similar inputs |
| Latency | Response time at P50, P95, P99 |
| Token Usage | Average tokens per request (cost control) |
| Success Rate | Percentage of valid, parseable outputs |
| User Satisfaction | Ratings, feedback, task completion |

**For optimization workflows**: See `references/prompt-optimization.md`

## Resources

- `references/chain-of-thought.md` — CoT patterns and implementation
- `references/few-shot-learning.md` — example selection and few-shot strategies
- `references/prompt-optimization.md` — iterative refinement workflows
- `references/prompt-templates.md` — reusable template patterns
- `references/system-prompts.md` — system prompt design patterns
- `assets/few-shot-examples.json` — example few-shot datasets
- `assets/prompt-template-library.md` — ready-to-use prompt templates
- `scripts/optimize-prompt.py` — prompt optimization utility

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Over-engineering | Complex prompt when simple works | Start simple, add complexity only when needed |
| Example pollution | Examples don't match target task | Curate examples that reflect actual inputs |
| Context overflow | Too many examples exceed token limit | Monitor token usage; prioritize quality over quantity |
| Ambiguous instructions | Multiple valid interpretations | Be specific; test with different interpreters |
| No error handling | Assuming outputs are always well-formed | Add validation, fallbacks, and retry logic |
| Hardcoded values | Prompts can't be reused | Parameterize with template variables |
| No versioning | Can't track what changed or roll back | Version control prompts like code |

## Integration Patterns

### With Validation

```
Complete the following task: {task}

After generating your response, verify it meets ALL these criteria:
- Directly addresses the original request
- Contains no factual errors
- Is appropriately detailed
- Uses proper formatting

If verification fails, revise before responding.
```

### With Confidence Scoring

Include confidence in structured outputs so downstream systems can handle uncertainty:
- High confidence (>0.8): use the answer directly
- Medium confidence (0.5-0.8): use with caveats
- Low confidence (<0.5): flag for human review

## NEVER Do

1. **NEVER start with complex prompts** — try the simplest prompt first; add complexity only when simple fails
2. **NEVER assume outputs will be well-formed** — always validate and handle malformed responses
3. **NEVER hardcode prompts that should be parameterized** — use templates with variables for reuse
4. **NEVER skip testing on edge cases** — boundary inputs reveal prompt fragility
5. **NEVER use examples that don't match the target task** — mismatched examples pollute the model's understanding
6. **NEVER exceed context limits with examples** — monitor token usage; too many examples degrade performance
7. **NEVER deploy prompts without version control** — prompt changes can break production; track every change
8. **NEVER ignore latency** — a perfect prompt that takes 30 seconds is worse than a good prompt that takes 3 seconds
