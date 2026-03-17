---
name: using-llm-specialist
description: LLM specialist router to prompt engineering, fine-tuning, RAG, evaluation, and safety skills.
---

# Using LLM Specialist

**You are an LLM engineering specialist.** This skill routes you to the right specialized skill based on the user's LLM-related task.

## When to Use This Skill

Use this skill when the user needs help with:
- Prompt engineering and optimization
- Fine-tuning LLMs (full, LoRA, QLoRA)
- Building RAG systems
- Evaluating LLM outputs
- Managing context windows
- Optimizing LLM inference
- LLM safety and alignment

## How to Access Reference Sheets

**IMPORTANT**: All reference sheets are located in the SAME DIRECTORY as this SKILL.md file.

When this skill is loaded from:
  `skills/using-llm-specialist/SKILL.md`

Reference sheets like `prompt-engineering-patterns.md` are at:
  `skills/using-llm-specialist/prompt-engineering-patterns.md`

NOT at:
  `skills/prompt-engineering-patterns.md` ← WRONG PATH

When you see a link like `[prompt-engineering-patterns.md](prompt-engineering-patterns.md)`, read the file from the same directory as this SKILL.md.

---

## Routing Decision Tree

### Step 1: Identify the task category

**Prompt Engineering** → See [prompt-engineering-patterns.md](prompt-engineering-patterns.md)
- Writing effective prompts
- Few-shot learning
- Chain-of-thought prompting
- System message design
- Output formatting
- Prompt optimization

**Fine-tuning** → See [llm-finetuning-strategies.md](llm-finetuning-strategies.md)
- When to fine-tune vs prompt engineering
- Full fine-tuning vs LoRA vs QLoRA
- Dataset preparation
- Hyperparameter selection
- Evaluation and validation
- Catastrophic forgetting prevention

**RAG (Retrieval-Augmented Generation)** → See [rag-architecture-patterns.md](rag-architecture-patterns.md)
- RAG system architecture
- Retrieval strategies (dense, sparse, hybrid)
- Chunking strategies
- Re-ranking
- Context injection
- RAG evaluation

**Evaluation** → See [llm-evaluation-metrics.md](llm-evaluation-metrics.md)
- Task-specific metrics (classification, generation, summarization)
- Human evaluation
- LLM-as-judge
- Benchmark selection
- A/B testing
- Quality assurance

**Context Management** → See [context-window-management.md](context-window-management.md)
- Context window limits (4k, 8k, 32k, 128k tokens)
- Summarization strategies
- Sliding window
- Hierarchical context
- Token counting
- Context pruning

**Inference Optimization** → See [llm-inference-optimization.md](llm-inference-optimization.md)
- Reducing latency
- Increasing throughput
- Batching strategies
- KV cache optimization
- Quantization (INT8, INT4)
- Speculative decoding

**Safety & Alignment** → See [llm-safety-alignment.md](llm-safety-alignment.md)
- Prompt injection prevention
- Jailbreak detection
- Content filtering
- Bias mitigation
- Hallucination reduction
- Guardrails

## Routing Examples

### Example 1: User asks about prompts
**User:** "My LLM isn't following instructions consistently. How can I improve my prompts?"

**Route to:** [prompt-engineering-patterns.md](prompt-engineering-patterns.md)
- Covers instruction clarity, few-shot examples, format specification

### Example 2: User asks about fine-tuning
**User:** "I have 10,000 examples of customer support conversations. Should I fine-tune a model or use prompts?"

**Route to:** [llm-finetuning-strategies.md](llm-finetuning-strategies.md)
- Covers when to fine-tune vs prompt engineering
- Dataset preparation
- LoRA vs full fine-tuning

### Example 3: User asks about RAG
**User:** "I want to build a Q&A system over my company's documentation. How do I give the LLM access to this information?"

**Route to:** [rag-architecture-patterns.md](rag-architecture-patterns.md)
- Covers RAG architecture
- Chunking strategies
- Retrieval methods

### Example 4: User asks about evaluation
**User:** "How do I measure if my LLM's summaries are good quality?"

**Route to:** [llm-evaluation-metrics.md](llm-evaluation-metrics.md)
- Covers summarization metrics (ROUGE, BERTScore)
- Human evaluation
- LLM-as-judge

### Example 5: User asks about context limits
**User:** "My documents are 50,000 tokens but my model only supports 8k context. What do I do?"

**Route to:** [context-window-management.md](context-window-management.md)
- Covers summarization, chunking, hierarchical context

### Example 6: User asks about speed
**User:** "My LLM inference is too slow (500ms per request). How can I make it faster?"

**Route to:** [llm-inference-optimization.md](llm-inference-optimization.md)
- Covers quantization, batching, KV cache, speculative decoding

### Example 7: User asks about safety
**User:** "Users are trying to jailbreak my LLM to bypass content filters. How do I prevent this?"

**Route to:** [llm-safety-alignment.md](llm-safety-alignment.md)
- Covers prompt injection prevention, jailbreak detection, guardrails

## Multiple Skills May Apply

Sometimes multiple skills are relevant:

**Example:** "I'm building a RAG system and need to evaluate retrieval quality."
- Primary: [rag-architecture-patterns.md](rag-architecture-patterns.md) (RAG architecture)
- Secondary: [llm-evaluation-metrics.md](llm-evaluation-metrics.md) (retrieval metrics: MRR, NDCG)

**Example:** "I'm fine-tuning an LLM but context exceeds 4k tokens."
- Primary: [llm-finetuning-strategies.md](llm-finetuning-strategies.md) (fine-tuning process)
- Secondary: [context-window-management.md](context-window-management.md) (handling long contexts)

**Example:** "My RAG system is slow and I need better prompts for the generation step."
- Primary: [rag-architecture-patterns.md](rag-architecture-patterns.md) (RAG architecture)
- Secondary: [llm-inference-optimization.md](llm-inference-optimization.md) (speed optimization)
- Tertiary: [prompt-engineering-patterns.md](prompt-engineering-patterns.md) (generation prompts)

**Approach:** Start with the primary skill, then reference secondary skills as needed.

## Common Task Patterns

### Pattern 1: Building an LLM application
1. Start with [prompt-engineering-patterns.md](prompt-engineering-patterns.md) (get prompt right first)
2. If prompts insufficient → [llm-finetuning-strategies.md](llm-finetuning-strategies.md) (customize model)
3. If need external knowledge → [rag-architecture-patterns.md](rag-architecture-patterns.md) (add retrieval)
4. Validate quality → [llm-evaluation-metrics.md](llm-evaluation-metrics.md) (measure performance)
5. Optimize speed → [llm-inference-optimization.md](llm-inference-optimization.md) (reduce latency)
6. Add safety → [llm-safety-alignment.md](llm-safety-alignment.md) (guardrails)

### Pattern 2: Improving existing LLM system
1. Identify bottleneck:
   - Quality issue → [prompt-engineering-patterns.md](prompt-engineering-patterns.md) or [llm-finetuning-strategies.md](llm-finetuning-strategies.md)
   - Knowledge gap → [rag-architecture-patterns.md](rag-architecture-patterns.md)
   - Context overflow → [context-window-management.md](context-window-management.md)
   - Slow inference → [llm-inference-optimization.md](llm-inference-optimization.md)
   - Safety concern → [llm-safety-alignment.md](llm-safety-alignment.md)
2. Apply specialized skill
3. Measure improvement → [llm-evaluation-metrics.md](llm-evaluation-metrics.md)

### Pattern 3: LLM research/experimentation
1. Design evaluation → [llm-evaluation-metrics.md](llm-evaluation-metrics.md) (metrics first!)
2. Baseline: prompt engineering → [prompt-engineering-patterns.md](prompt-engineering-patterns.md)
3. If insufficient: fine-tuning → [llm-finetuning-strategies.md](llm-finetuning-strategies.md)
4. Compare: RAG vs fine-tuning → Both skills
5. Optimize best approach → [llm-inference-optimization.md](llm-inference-optimization.md)

## Quick Reference

| Task | Primary Skill | Common Secondary Skills |
|------|---------------|------------------------|
| Better outputs | [prompt-engineering-patterns.md](prompt-engineering-patterns.md) | [llm-evaluation-metrics.md](llm-evaluation-metrics.md) |
| Customize behavior | [llm-finetuning-strategies.md](llm-finetuning-strategies.md) | [prompt-engineering-patterns.md](prompt-engineering-patterns.md) |
| External knowledge | [rag-architecture-patterns.md](rag-architecture-patterns.md) | [context-window-management.md](context-window-management.md) |
| Quality measurement | [llm-evaluation-metrics.md](llm-evaluation-metrics.md) | - |
| Long documents | [context-window-management.md](context-window-management.md) | [rag-architecture-patterns.md](rag-architecture-patterns.md) |
| Faster inference | [llm-inference-optimization.md](llm-inference-optimization.md) | - |
| Safety/security | [llm-safety-alignment.md](llm-safety-alignment.md) | [prompt-engineering-patterns.md](prompt-engineering-patterns.md) |

## Default Routing Logic

If task is unclear, ask clarifying questions:
1. "What are you trying to achieve with the LLM?" (goal)
2. "What problem are you facing?" (bottleneck)
3. "Have you tried prompt engineering?" (start simple)

Then route to the most relevant skill.

## Summary

**This is a meta-skill that routes to specialized LLM engineering skills.**

## LLM Specialist Skills Catalog

After routing, load the appropriate specialist skill for detailed guidance:

1. [prompt-engineering-patterns.md](prompt-engineering-patterns.md) - Instruction clarity, few-shot learning, chain-of-thought, system messages, output formatting, prompt optimization
2. [llm-finetuning-strategies.md](llm-finetuning-strategies.md) - Full fine-tuning vs LoRA vs QLoRA, dataset preparation, hyperparameter selection, catastrophic forgetting prevention
3. [rag-architecture-patterns.md](rag-architecture-patterns.md) - RAG system architecture, retrieval strategies (dense/sparse/hybrid), chunking, re-ranking, context injection
4. [llm-evaluation-metrics.md](llm-evaluation-metrics.md) - Task-specific metrics, human evaluation, LLM-as-judge, benchmarks, A/B testing, quality assurance
5. [context-window-management.md](context-window-management.md) - Context limits (4k-128k tokens), summarization strategies, sliding window, hierarchical context, token counting
6. [llm-inference-optimization.md](llm-inference-optimization.md) - Latency reduction, throughput optimization, batching, KV cache, quantization (INT8/INT4), speculative decoding
7. [llm-safety-alignment.md](llm-safety-alignment.md) - Prompt injection prevention, jailbreak detection, content filtering, bias mitigation, hallucination reduction, guardrails

**When multiple skills apply:** Start with the primary skill, reference others as needed.

**Default approach:** Start simple (prompts), add complexity only when needed (fine-tuning, RAG, optimization).
