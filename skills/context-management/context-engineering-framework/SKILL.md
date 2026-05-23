---
name: context-engineering-framework
description: Optimize context windows, manage token budgets, compress context, and create effective handoff documents for long-running multi-agent workflows
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash, WebFetch]
---

# Context Engineering Framework

## Purpose

Context engineering is critical for managing the finite resource of LLM context windows. This skill provides systematic approaches to:
- **Measure** token usage and identify optimization opportunities
- **Compress** context without losing critical information
- **Optimize** token budget allocation across workflow stages
- **Handoff** work between agents with complete state preservation

Token costs scale linearly with context size - a 100k token context costs 10x more than 10k. Poor context management leads to:
- Failed completions when context overflows
- Degraded quality from truncated information
- Increased costs from redundant context
- Lost work when sessions can't resume properly

## Quick Start: 4-Step Process

### Step 1: Measure Current Context
```python
# Count tokens in your context
from tiktoken import encoding_for_model
enc = encoding_for_model("gpt-4")
tokens = len(enc.encode(context_text))
print(f"Current context: {tokens:,} tokens")
```

### Step 2: Compress Context
```python
# Apply compression techniques
compressed = apply_compression(context_text, {
    'remove_whitespace': True,
    'deduplicate': True,
    'summarize_verbose': True,
    'extract_references': True
})
print(f"Compressed to: {len(enc.encode(compressed)):,} tokens")
```

### Step 3: Optimize Budget Allocation
```python
# Allocate tokens across workflow stages
budget = TokenBudget(total=100_000)
budget.allocate('system_prompt', 2_000)
budget.allocate('working_memory', 30_000)
budget.allocate('reference_docs', 40_000)
budget.allocate('conversation', 28_000)
```

### Step 4: Create Handoff Document
```python
# Generate handoff for next agent/session
handoff = create_handoff({
    'completed': ['task1', 'task2'],
    'current_state': working_memory,
    'next_steps': ['task3', 'task4'],
    'constraints': ['must_preserve_X', 'avoid_Y'],
    'context_summary': compressed_context
})
```

## Core Patterns Overview

### Pattern 1: Token Budget Management
Track token usage across all context components. Set alerts before limits. Enforce hard boundaries to prevent overflow.

### Pattern 2: Context Compression (Lossless & Lossy)
Remove redundancy without information loss. Apply semantic compression when acceptable. Preserve critical details while reducing verbosity.

### Pattern 3: Semantic Chunking
Split context along natural boundaries. Maintain semantic coherence within chunks. Enable selective retrieval of relevant sections.

### Pattern 4: Progressive Summarization
Create multi-level summaries for different detail needs. Drill down when specifics required. Maintain high-level overview for navigation.

### Pattern 5: Handoff Document Generation
Capture complete state for work continuation. Include decision history and rationale. Provide clear next steps and constraints.

### Pattern 6: Context Window Optimization
Balance detail vs breadth based on task needs. Use RAG for large reference sets. Implement sliding windows for long conversations.

## Detailed Documentation

- **[PATTERNS.md](PATTERNS.md)** - Full implementation details for all 6 patterns
- **[KNOWLEDGE.md](KNOWLEDGE.md)** - Theory, research, and advanced techniques
- **[EXAMPLES.md](EXAMPLES.md)** - Working code for common scenarios
- **[GOTCHAS.md](GOTCHAS.md)** - Common pitfalls and debugging strategies
- **[REFERENCE.md](REFERENCE.md)** - API documentation and performance data

## Top 3 Gotchas

### 1. Information Loss During Compression
**Problem**: Aggressive compression removes critical details
**Solution**: Always validate compressed output preserves key information. Use tiered compression with fallback to less aggressive methods.

### 2. Token Counting Mismatches
**Problem**: Different models use different tokenizers, counts vary
**Solution**: Always use model-specific tokenizer. Add 10% safety margin to budgets.

### 3. Handoff Document Incompleteness
**Problem**: Missing context causes next agent/session to fail or repeat work
**Solution**: Use structured handoff templates. Validate all required fields present.

## Quick Reference Card

### Token Budget Allocation Guide
```
System Prompt:      2-5% (2-5k tokens)
Working Memory:    20-30% (20-30k tokens)
Reference Docs:    30-50% (30-50k tokens)
Conversation:      20-40% (20-40k tokens)
Safety Buffer:     10% (10k tokens)
```

### Compression Ratios by Technique
```
Whitespace removal:        5-10% reduction
Deduplication:           10-30% reduction
Reference extraction:     20-40% reduction
Semantic compression:     40-60% reduction
Aggressive summarization: 70-90% reduction
```

### Context Window Sizes (2024)
```
GPT-4 Turbo:     128k tokens
Claude 3:        200k tokens
Gemini 1.5 Pro:  2M tokens
GPT-3.5:         16k tokens
Most OSS models: 4-32k tokens
```

### Quick Diagnostic Commands
```python
# Check current token usage
print(f"Tokens used: {count_tokens(context)}")

# Find redundancy opportunities
find_duplicates(context)

# Test compression ratio
test_compression(context, method='semantic')

# Validate handoff document
validate_handoff(handoff_doc)
```

## When to Use This Skill

- Managing projects with 50k+ tokens of context
- Coordinating multi-agent workflows requiring state transfer
- Optimizing costs for high-volume LLM usage
- Debugging context overflow errors
- Implementing long-running conversational agents
- Creating checkpoint/resume capabilities
- Building RAG systems with large document sets

## Related Skills

- `reverse-engineering-toolkit` - Analyze existing context usage patterns
- `work-forecasting-parallelization` - Estimate token requirements for workflows
- `agent-builder-framework` - Design agents with efficient context usage
- `workflow-builder-framework` - Orchestrate context across workflow stages

## Integration with Agents

### Primary User: context-manager
The `context-manager` agent should be refactored to use this skill instead of embedding context engineering logic directly.

```python
# Before: Embedded in agent
class ContextManager:
    def compress_context(self, text):
        # 500+ lines of compression logic...

# After: Delegate to skill
class ContextManager:
    def compress_context(self, text):
        return skill('context-engineering-framework').compress(text)
```

### Other Agent Integrations
- `agent-orchestrator` - Manage context budgets across agent pods
- `prompt-engineer` - Optimize prompts for token efficiency
- `long-running-assistant` - Handle session continuity
- `document-processor` - Chunk and compress large documents

## Best Practices

### DO
- ✅ Measure before optimizing - profile actual token usage
- ✅ Preserve information architecture during compression
- ✅ Test compression with real workloads
- ✅ Version handoff document schemas
- ✅ Monitor token usage in production

### DON'T
- ❌ Compress without validating information preservation
- ❌ Assume token counts are consistent across models
- ❌ Hard-code context window limits
- ❌ Skip handoff validation before agent switches
- ❌ Ignore compression impact on downstream tasks

## Validation Checklist

Before using compressed context:
- [ ] Key information preserved?
- [ ] Semantic coherence maintained?
- [ ] References still resolvable?
- [ ] Compression ratio acceptable?
- [ ] Handoff document complete?

## Performance Benchmarks

| Technique | Compression Ratio | Info Retention | Speed |
|-----------|------------------|----------------|-------|
| Whitespace removal | 5-10% | 100% | <1ms |
| Deduplication | 10-30% | 100% | <10ms |
| Reference extraction | 20-40% | 95% | <50ms |
| Semantic compression | 40-60% | 85% | <200ms |
| Aggressive summary | 70-90% | 60% | <500ms |

## Getting Started

1. **Install dependencies**:
```bash
pip install tiktoken langchain openai anthropic
```

2. **Run token analysis**:
```python
from context_engineering import analyze_context
report = analyze_context("your_context.txt")
print(report.summary())
```

3. **Apply compression**:
```python
from context_engineering import compress
compressed = compress(context, target_ratio=0.5)
```

4. **Create handoff**:
```python
from context_engineering import create_handoff
handoff = create_handoff(state, next_agent='reviewer')
```

## Conclusion

Effective context engineering is the difference between LLM applications that scale and those that fail under load. This framework provides battle-tested patterns for managing context windows, reducing token costs, and ensuring work continuity across agent boundaries.

Master these patterns to build robust, cost-effective, and scalable LLM systems.

---

*For implementation details, see [PATTERNS.md](PATTERNS.md). For theory and research, see [KNOWLEDGE.md](KNOWLEDGE.md).*