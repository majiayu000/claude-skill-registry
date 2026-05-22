---
name: LLM Prompt Optimizer
slug: llm-prompt-optimizer
description: Optimize prompts for better LLM outputs through systematic analysis and refinement
category: ai-ml
complexity: intermediate
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "optimize this prompt"
  - "improve LLM output"
  - "better prompt"
  - "prompt optimization"
  - "enhance prompt quality"
tags:
  - prompt-engineering
  - optimization
  - LLM
  - AI
  - performance
---

# LLM Prompt Optimizer

The LLM Prompt Optimizer skill systematically analyzes and refines prompts to maximize the quality, accuracy, and relevance of large language model outputs. It applies evidence-based optimization techniques including structural improvements, context enrichment, constraint calibration, and output format specification.

This skill goes beyond basic prompt writing by leveraging understanding of how different LLMs process instructions, their attention patterns, and their response tendencies. It helps you transform underperforming prompts into high-yield instructions that consistently produce the results you need.

Whether you are building production AI systems, conducting research, or simply want better ChatGPT responses, this skill ensures your prompts are optimized for your specific model and use case.

## Core Workflows

### Workflow 1: Analyze and Diagnose Prompt Issues
1. **Receive** the current prompt and sample outputs
2. **Identify** failure patterns:
   - Hallucination triggers
   - Ambiguity sources
   - Missing context gaps
   - Conflicting instructions
   - Over/under-constrained parameters
3. **Map** issues to specific prompt segments
4. **Prioritize** fixes by impact
5. **Explain** root causes to user

### Workflow 2: Apply Optimization Techniques
1. **Select** appropriate techniques based on diagnosis:
   - Chain-of-thought insertion
   - Few-shot example addition
   - Role/persona specification
   - Output schema definition
   - Constraint tightening/loosening
2. **Restructure** prompt for clarity
3. **Add** missing context or examples
4. **Remove** conflicting or redundant instructions
5. **Test** optimized version
6. **Iterate** based on results

### Workflow 3: Model-Specific Optimization
1. **Identify** target LLM (GPT-4, Claude, Llama, etc.)
2. **Apply** model-specific best practices:
   - Token budget optimization
   - System prompt vs user prompt split
   - Temperature/sampling guidance
   - Context window utilization
3. **Adjust** for model quirks and strengths
4. **Document** model-specific recommendations

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Diagnose prompt issues | "Why isn't this prompt working: [prompt]" |
| Optimize for accuracy | "Optimize for accuracy: [prompt]" |
| Reduce hallucinations | "Reduce hallucinations in: [prompt]" |
| Add structure | "Add better structure to: [prompt]" |
| Model-specific optimization | "Optimize this for [model]: [prompt]" |
| A/B test variants | "Create prompt variants for testing: [prompt]" |

## Best Practices

- **Start with Clear Intent**: Define exactly what success looks like before optimizing
  - Bad: "Make it work better"
  - Good: "Reduce factual errors while maintaining conversational tone"

- **Use Explicit Output Formats**: LLMs follow structure better than vague requests
  - Specify JSON schemas, markdown formats, or template structures
  - Example: "Return as JSON with keys: analysis, recommendations, confidence"

- **Calibrate Constraints**: Too many constraints cause conflicts; too few cause drift
  - Test constraint combinations systematically
  - Remove constraints that don't improve output quality

- **Leverage Positive Instructions**: Tell the model what TO do, not just what NOT to do
  - Bad: "Don't be verbose"
  - Good: "Respond in 2-3 concise sentences"

- **Position Critical Instructions Strategically**: Beginning and end get more attention
  - Put key constraints at the start
  - Repeat critical requirements at the end

- **Use Delimiters for Multi-Part Inputs**: Clear separation prevents confusion
  - Triple quotes, XML tags, or markdown headers
  - Example: `"""User Query: {query}""" """Context: {context}"""`

## Advanced Techniques

### Recursive Refinement Loop
For complex prompts, use iterative optimization:
```
1. Generate baseline outputs (n=5)
2. Score outputs against criteria
3. Identify lowest-scoring dimension
4. Adjust prompt targeting that dimension
5. Repeat until all dimensions score acceptably
```

### Prompt Decomposition
Break complex tasks into simpler sub-prompts:
```
Complex: "Analyze this code, find bugs, suggest fixes, and refactor"
Decomposed:
  Step 1: "List all potential bugs in this code"
  Step 2: "For each bug, explain the fix"
  Step 3: "Refactor the fixed code for clarity"
```

### Negative Example Injection
Show what NOT to do alongside positive examples:
```
Good output: [example]
Bad output (avoid this): [anti-example]
Key difference: [explanation]
```

### Token Budget Optimization
When context is limited:
```
1. Remove redundant phrases
2. Use abbreviations consistently
3. Compress examples to minimal effective size
4. Prioritize recent/relevant context
5. Consider summarizing long contexts
```

## Common Pitfalls to Avoid

- Over-engineering simple prompts with unnecessary complexity
- Copying prompts between models without adaptation
- Ignoring the relationship between temperature and prompt specificity
- Adding examples that introduce unwanted patterns
- Using vague terms like "good," "proper," or "appropriate" without definition
- Conflicting instructions that force the model to choose
- Forgetting to specify handling of edge cases and errors
