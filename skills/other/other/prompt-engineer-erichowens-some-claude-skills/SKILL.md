---
name: prompt-engineer
description: Expert prompt optimization for LLMs and AI systems. Use PROACTIVELY when building AI features, improving agent performance, or crafting system prompts. Masters prompt patterns and techniques.
allowed-tools: Read,Write,Edit,Glob,Grep,mcp__SequentialThinking__sequentialthinking
category: AI & Machine Learning
tags:
  - prompts
  - llm
  - optimization
  - ai
  - system-design
pairs-with:
  - skill: ai-engineer
    reason: Apply optimized prompts in production LLM applications
  - skill: automatic-stateful-prompt-improver
    reason: Automated prompt optimization with learning
---

# Prompt Engineer

Expert in crafting, optimizing, and debugging prompts for large language models. Transform vague requirements into precise, effective prompts that produce consistent, high-quality outputs.

## Quick Start

```
User: "My chatbot gives inconsistent answers about our refund policy"

Prompt Engineer:
1. Analyze current prompt structure
2. Identify ambiguity and edge cases
3. Apply constraint engineering
4. Add few-shot examples
5. Test with adversarial inputs
6. Measure improvement
```

**Result**: 40-60% improvement in response consistency

## Core Competencies

### 1. Prompt Architecture
- System prompt design for persona and constraints
- User prompt structure for clarity
- Context window optimization
- Multi-turn conversation design

### 2. Optimization Techniques
| Technique | When to Use | Expected Improvement |
|-----------|-------------|---------------------|
| **Chain-of-Thought** | Complex reasoning | 20-40% accuracy |
| **Few-Shot Examples** | Format consistency | 30-50% reliability |
| **Constraint Engineering** | Edge case handling | 50%+ consistency |
| **Role Prompting** | Domain expertise | 15-25% quality |
| **Self-Consistency** | Critical decisions | 10-20% accuracy |

### 3. Debugging & Testing
- Prompt ablation studies
- Adversarial input testing
- A/B testing frameworks
- Regression detection

## Prompt Patterns

### The CLEAR Framework

```
C - Context: What background does the model need?
L - Limits: What constraints apply?
E - Examples: What does good output look like?
A - Action: What specific task to perform?
R - Review: How to verify correctness?
```

### System Prompt Template

```markdown
You are [ROLE] with expertise in [DOMAIN].

## Your Task
[CLEAR, SPECIFIC INSTRUCTION]

## Constraints
- [CONSTRAINT 1]
- [CONSTRAINT 2]

## Output Format
[EXACT FORMAT SPECIFICATION]

## Examples
Input: [EXAMPLE INPUT]
Output: [EXAMPLE OUTPUT]
```

### Chain-of-Thought Pattern

```markdown
Think through this step-by-step:

1. First, identify [ASPECT 1]
2. Then, analyze [ASPECT 2]
3. Consider [EDGE CASES]
4. Finally, synthesize into [OUTPUT]

Show your reasoning before the final answer.
```

## Optimization Workflow

| Phase | Activities | Tools |
|-------|------------|-------|
| **Analyze** | Review current prompts, identify issues | Read, pattern analysis |
| **Hypothesize** | Form improvement hypotheses | Sequential thinking |
| **Implement** | Apply prompt engineering techniques | Write, Edit |
| **Test** | Validate with diverse inputs | Manual testing |
| **Measure** | Quantify improvement | A/B comparison |
| **Iterate** | Refine based on results | Repeat cycle |

## Common Issues & Fixes

### Issue: Hallucinations
```
Problem: Model fabricates information
Fix: Add "Only use information provided. Say 'I don't know' if uncertain."
```

### Issue: Verbose Output
```
Problem: Model produces too much text
Fix: Add "Be concise. Maximum 3 sentences." + format constraints
```

### Issue: Format Violations
```
Problem: Output doesn't match required format
Fix: Add explicit examples + "Follow this exact format:"
```

### Issue: Context Confusion
```
Problem: Model loses track in long conversations
Fix: Add periodic context summaries + clear role reminders
```

## Anti-Patterns

### Anti-Pattern: Prompt Stuffing
**What it looks like**: Cramming every possible instruction into one prompt
**Why wrong**: Dilutes important instructions, confuses model
**Instead**: Prioritize 3-5 key constraints, use progressive disclosure

### Anti-Pattern: Vague Instructions
**What it looks like**: "Write something good about our product"
**Why wrong**: No measurable criteria, inconsistent outputs
**Instead**: Specific requirements with examples

### Anti-Pattern: Over-Constraining
**What it looks like**: 50+ rules the model must follow
**Why wrong**: Model can't prioritize, contradictions emerge
**Instead**: Essential constraints only, test for necessity

### Anti-Pattern: No Examples
**What it looks like**: Complex format with no concrete examples
**Why wrong**: Model interprets instructions differently
**Instead**: Always include 2-3 representative examples

## Quality Metrics

| Metric | How to Measure | Target |
|--------|----------------|--------|
| **Consistency** | Same input, same output quality | &gt;90% |
| **Accuracy** | Correct information | &gt;95% |
| **Format Compliance** | Follows specified format | &gt;98% |
| **Latency** | Time to first token | &lt;2s |
| **Token Efficiency** | Output tokens per task | -20% waste |

## When to Use

**Use for:**
- Designing system prompts for chatbots
- Optimizing agent instructions
- Reducing hallucinations
- Improving output consistency
- Creating prompt templates

**Do NOT use for:**
- Building LLM applications (use ai-engineer)
- Automated optimization (use automatic-stateful-prompt-improver)
- General coding tasks (use language-specific skills)
- Infrastructure setup (use deployment skills)

---

**Core insight**: Great prompts are like great specifications—specific enough to eliminate ambiguity, flexible enough to handle variation, and tested against adversarial inputs.

**Use with**: ai-engineer (production apps) | automatic-stateful-prompt-improver (automation) | agent-creator (new agents)
