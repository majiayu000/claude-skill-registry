---
name: perplexity-web-research
description: Leverage Perplexity CLI for web research, deep reasoning, and independent validation. Use when you need current/external knowledge, want a second opinion before decisions, or want to delegate complex analytical thinking to specialized reasoning models. Complements (not replaces) standard web tools. Can be invoked directly or spawned as a subagent.
license: MIT
compatibility: Requires llm CLI with llm-perplexity plugin and Perplexity API key
metadata:
  author: Pietro Di Bello
  version: "1.0.0"
allowed-tools: Bash(llm:*)
---

# Perplexity Web Research

Use the `llm` CLI with Perplexity plugin for web research, deep reasoning, and independent validation.

## Quick Start

```bash
llm -m sonar 'your question here'
```

## Model Selection

Choose the appropriate model based on query complexity:

| Model | Use Case | Context | Web Search |
|-------|----------|---------|------------|
| `sonar` | Quick lookups, general questions | 128k | ✓ |
| `sonar-pro` | Thorough answers, detailed research (flagship) | 200k | ✓ |
| `sonar-deep-research` | Complex multi-faceted research | 128k | ✓ |
| `sonar-reasoning` | Step-by-step reasoning questions | 128k | ✓ |
| `sonar-reasoning-pro` | Advanced reasoning with more detail | 128k | ✓ |
| `r1-1776` | Specialized model without web search | 128k | ✗ |

**Default choice**: `sonar` for most queries.

**Use `sonar-pro`** when:
- Query requires comprehensive coverage
- Need detailed explanations
- Research involves multiple aspects
- Largest context window needed (200k)

**Use `sonar-deep-research`** when:
- Topic is complex and multi-faceted
- Need synthesis across many sources
- Research question has no simple answer

**Use `sonar-reasoning`** when:
- Question requires logical deduction
- Need step-by-step problem solving
- Math or algorithmic reasoning involved

**Use `sonar-reasoning-pro`** when:
- Advanced reasoning with more comprehensive analysis needed
- Complex multi-step logical problems
- Need most thorough step-by-step explanations
- Reasoning task benefits from deeper exploration

**Use `r1-1776`** when:
- Need specialized reasoning without web search
- Pure analytical or logical tasks
- Information is already known, just need reasoning applied
- Want to avoid web search overhead

**Note**: Most models include real-time web search. Only `r1-1776` omits web search for pure reasoning tasks.

## When to Use

Use this skill in three primary scenarios:

### 1. Current or External Knowledge

When you need up-to-date information and intentionally want to use Perplexity instead of standard web fetch tools:

- **Documentation lookups**: Current API docs, library references, framework guides
- **Library versions**: "What's the latest version of X?"
- **Recent changes**: "What changed in Y version 2.0?"
- **Error research**: Unfamiliar error messages or stack traces
- **Technology verification**: "Does X support Y feature?"
- **Current events**: Recent news, announcements, releases
- **Fact checking**: Information that may have changed since training cutoff

### 2. Second Opinions

When you want an independent perspective before committing to a decision or approach:

- **Architecture decisions**: "What are the trade-offs between approach A and B?"
- **Technology choices**: "Should I use X or Y for this use case?"
- **Design validation**: "Is this approach considered best practice?"
- **Problem verification**: "Am I thinking about this problem correctly?"
- **Alternative perspectives**: "What other ways could this be solved?"

### 3. Deep Reasoning Delegation

When you want to offload complex analytical thinking to specialized reasoning models (even when information doesn't need to be current):

- **Complex problem solving**: Multi-step reasoning requiring systematic analysis
- **Algorithmic thinking**: "How should I optimize this algorithm?"
- **System design**: "How should I architect this system?"
- **Trade-off analysis**: Comparing multiple options with many variables
- **Mathematical reasoning**: Calculations, proofs, or quantitative analysis

## When NOT to Use

Do NOT use for:

- **Local codebase questions**: Use grep/read tools instead
- **Information already in context**: Use existing conversation context
- **Simple factual questions**: Use your training data when sufficient
- **Tasks requiring file operations**: Code analysis, refactoring, editing

This skill complements, not replaces, standard web tools (WebFetch, WebSearch). Choose based on whether you want Perplexity's specific capabilities (reasoning models, synthesis, alternative perspective).

## Usage Examples

### Current Knowledge: Documentation Lookup
```bash
llm -m sonar 'Next.js App Router documentation 2026'
```

### Current Knowledge: Error Research
```bash
llm -m sonar 'ECONNREFUSED error when connecting to PostgreSQL'
```

### Current Knowledge: Library Version
```bash
llm -m sonar 'latest stable version of React 2026'
```

### Current Knowledge: Complex Research
```bash
llm -m sonar-deep-research 'comparison of WebSocket vs Server-Sent Events for real-time updates in 2026'
```

### Second Opinion: Architecture Decision
```bash
llm -m sonar-pro 'trade-offs between microservices and monolith for a team of 5 engineers'
```

### Second Opinion: Technology Choice
```bash
llm -m sonar 'should I use PostgreSQL or MongoDB for a social media analytics platform'
```

### Deep Reasoning: Algorithm Design
```bash
llm -m sonar-reasoning 'how to design an efficient caching strategy for a rate-limited API with bursty traffic patterns'
```

### Deep Reasoning: System Architecture
```bash
llm -m sonar-reasoning-pro 'design a scalable job queue system that handles both immediate and scheduled tasks with priority levels'
```

## Using as a Subagent

This skill can be invoked directly within the conversation or spawned as a subagent for focused research:

**Direct invocation**: Use the Bash tool to run `llm` commands inline when the query is straightforward and the result can be immediately incorporated.

**Subagent invocation**: Spawn a subagent when:
- Research requires multiple iterations or follow-up queries
- You want the subagent to synthesize findings before reporting back
- The reasoning task is complex enough to benefit from dedicated focus
- You want to continue other work while research happens in parallel

## Context Marker

When using this skill, add 🔍 as a start-of-message marker.

```
🔍 I will research Next.js App Router on Perplexity...
```

## Setup

If the `llm` CLI or Perplexity plugin is not installed, see [references/setup.md](references/setup.md) for installation instructions.

## Relationship with Other Tools

This skill **complements** standard web tools (WebFetch, WebSearch), not replaces them.

**Use Perplexity** when you want:
- Specialized reasoning models for complex analysis
- Synthesis and perspective from multiple sources
- Independent validation or second opinions
- Specific Perplexity model capabilities

**Use standard web tools** when you want:
- Direct access to specific URLs or pages
- Raw content from known sources
- General web search without specialized reasoning
