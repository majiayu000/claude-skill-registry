---
name: token-efficiency
description: Maximise AI interaction value per token - techniques, patterns, integration with cost estimation
category: Session Knowledge
---

# Skill: token-efficiency

## What I do

I optimise every AI interaction for maximum value per token: being explicit about intent, structuring information clearly, removing noise, and using iteration instead of perfection in one shot. I provide efficiency techniques that reduce costs identified by token-cost-estimation.

## When to use me

- When asking complex questions or requesting implementations
- When dealing with large codebases (summarise, don't dump)
- When writing prompts that will be reused
- When you have limited token budget
- When token-cost-estimation identifies optimisation opportunities

## Core principles

1. **Explicit intent** - State what you need, why, what success looks like
2. **Structured information** - Sections, bullets, clear formatting over prose
3. **Cut noise** - Remove unnecessary words and irrelevant context
4. **Context efficiency** - One good example beats ten vague descriptions
5. **Iterate** - Expect refinement, don't demand perfection first try

## Efficiency Techniques

### Prompt Structure (saves 10-20%)
```
Bad: "I need help with the authentication system, 
     it's not working properly and I've tried a 
     few things but nothing works..."

Good:
Goal: Fix auth token validation
Error: JWT expired check failing
Tried: Updated token library (no effect)
Need: Root cause + fix
```

### Context Provision (saves 15-25%)
- Provide relevant code snippets, not entire files
- State assumptions explicitly
- Include error messages verbatim
- Reference specific line numbers

### Efficient Patterns

| Pattern | Token Savings | Example |
|---------|---------------|---------|
| Focused context | 20-30% | Snippet vs full file |
| Clear structure | 10-15% | Bullets vs prose |
| Explicit success criteria | 10-20% | "Done when X passes" |
| Example over description | 15-25% | Show, don't tell |

## Integration with token-cost-estimation

### Pre-Session
1. Review token-cost-estimation breakdown
2. Identify high-cost phases
3. Apply efficiency techniques to reduce

### During Session
- Use structured prompts throughout
- Provide focused context
- Iterate in small steps

### Post-Session
- Compare actual vs estimated
- Identify which techniques helped
- Store learnings in memory-keeper

## Quantitative Metrics

Track these to measure efficiency:
- Tokens per task completed
- First-attempt success rate
- Iteration count per task
- Context rebuild frequency

## Anti-patterns to avoid

- ❌ Dumping entire files when snippet suffices
- ❌ Vague requests ("fix this")
- ❌ Expecting perfection on first try
- ❌ Repeating context unnecessarily
- ❌ Not learning from high-cost sessions

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Workflow-Orchestration/Token Efficiency.md`

## Related skills

- `token-cost-estimation` - Quantifies costs, identifies savings
- `pre-action` - Clarify before prompting
- `parallel-execution` - Efficiency through parallelism
- `scope-management` - Scope affects token usage
- `context-efficient-tools` — Tool result filtering (complements prompt-level efficiency)
