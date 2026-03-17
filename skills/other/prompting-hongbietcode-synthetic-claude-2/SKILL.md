---
name: prompting
description: "PROACTIVE: This skill SHOULD BE USED AUTOMATICALLY when writing prompts, system prompts, crafting instructions for LLMs, or optimizing AI interactions. Triggers on: write prompt, system prompt, prompt engineering, optimize prompt, better prompt, prompt template, instruction design, context engineering, SKILL.md description, agent instructions. Use for CRAFTING LLM PROMPTS. Model-agnostic best practices for coding agents."
---

# Prompting - Model-Agnostic Best Practices (Late 2025)

Optimal prompt standards for coding agents. Applies to all models (Claude, GPT, Gemini, Grok).

**Paradigm**: Context Engineering > Prompt Engineering. Focus on designing information systems, not "perfect wording". API-level configs (effort, reasoning_effort, thinking_level) are separate from prompt text.

## Quick Reference (Use First)

Before writing/reviewing any prompt, verify:

```
[ ] Structure: Clear XML/Markdown sections (context → task → constraints → output)
[ ] Order: Long context BEFORE query (+30% quality)
[ ] Task: ONE atomic, explicit action
[ ] Output: Format defined (JSON schema, structure)
[ ] Positive: "Do X" instead of "Don't Y"
[ ] Reasoning: Zero-shot for reasoning models (no manual CoT)
[ ] Examples: Few-shot ONLY for format, not logic
[ ] Caching: Static content first, dynamic last
[ ] Simplicity: Start simple, add complexity only if needed (Stanford 8-word)
```

## Decision Flow

```
Task Type?
│
├─ Simple (1 step) ────────────► Direct instruction, no CoT
│
├─ Complex reasoning
│   ├─ Reasoning model (o3/o4/GPT-5/Claude thinking)
│   │   └─► Zero-shot + explicit goal only
│   └─ Standard model
│       └─► Structured prompt + optional CoT
│
├─ Code generation ────────────► Define: language, framework, style
│                                Provide: context files, dependencies
│                                Specify: output format, tests
│
└─ Multi-step workflow ────────► Break into atomic tasks
                                 Use Orchestrator-Worker pattern
                                 Include verification steps
```

## Core Structure Template

```xml
<context>
  [Background, project details - place LONG documents here]
</context>
<task>
  [ONE specific action required]
</task>
<constraints>
  [Boundaries, limitations]
</constraints>
<output_format>
  [Exact format: JSON schema, markdown structure]
</output_format>
```

For **system prompts** (coding agents):

```xml
<role>[Expert domain]</role>
<capabilities>[Tools, what agent CAN do]</capabilities>
<constraints>[Security rules, boundaries]</constraints>
<workflow>[Step-by-step process]</workflow>
<output_standards>[Code style, testing requirements]</output_standards>
```

## Key Principles

| Principle | Do This | Avoid This |
|-----------|---------|------------|
| **Structure** | XML/Markdown sections | Wall of text |
| **Context** | Long docs BEFORE query | Query before context (-30%) |
| **Specificity** | "Dashboard with filtering, export, real-time" | "Create dashboard" |
| **Instructions** | "Return only JSON" | "Don't add explanations" |
| **Reasoning models** | Zero-shot, explicit goal | Manual "think step-by-step" |
| **Examples** | Few-shot for FORMAT only | Few-shot for logic (hurts reasoning) |
| **Caching** | Static first, dynamic last | Dynamic content first |

## Technique Selection

| Technique | Use When | Avoid When |
|-----------|----------|------------|
| **Extended Thinking** | Complex math, multi-step planning | Pattern recognition, simple tasks (can HURT -36%) |
| **Atom of Thoughts** | Parallelizable problems | Creative writing |
| **Tree of Thoughts** | Multiple valid paths | Simple queries |
| **ReAct** | Tool use, external data | Pure reasoning |
| **Self-Consistency** | High-stakes decisions | Speed-critical |
| **Role Reversal** | Need +40% accuracy | Quick drafts |

See details: `references/techniques.md`

## Context Stack (Priority Order)

1. System Instructions (role, rules) - **cached**
2. Long-Term Memory (preferences)
3. Retrieved Documents (RAG)
4. Tool Definitions - **cached**
5. Conversation History
6. Current Task - **last for recency**

## Security

- Separate system/user content with XML tags
- Validate user inputs before embedding
- Validate OUTPUT, not reasoning (CoT hijackable 94-99%)
- Mark sensitive context with explicit boundaries

## References

Load as needed for detailed guidance:

- `references/techniques.md` - AoT, ToT, ReAct, Self-Consistency, Role Reversal, Extended Thinking
- `references/anti-patterns.md` - Full list of what to avoid with explanations
- `references/agentic-patterns.md` - Orchestrator-Worker, Reflexion, Plan-Execute, Tool Orchestration
- `references/memory-patterns.md` - CoALA Framework: Procedural, Semantic, Episodic memory
- `references/meta-prompting.md` - LLM self-optimization workflow
