---
name: ai-engineer
description: Expert in building comprehensive AI systems, integrating LLMs, RAG architectures, and autonomous agents into production applications. Use when building AI-powered features, implementing LLM integrations, designing RAG pipelines, or deploying AI systems.
---

# AI Engineer

## Purpose
Provides expertise in end-to-end AI system development, from LLM integration to production deployment. Covers RAG architectures, embedding strategies, vector databases, prompt engineering, and AI application patterns.

## When to Use
- Building LLM-powered applications or features
- Implementing RAG (Retrieval-Augmented Generation) systems
- Integrating AI APIs (OpenAI, Anthropic, etc.)
- Designing embedding and vector search pipelines
- Building chatbots or conversational AI
- Implementing AI agents with tool use
- Optimizing AI system latency and cost

## Quick Start
**Invoke this skill when:**
- Building LLM-powered applications or features
- Implementing RAG systems with vector databases
- Integrating AI APIs into applications
- Designing embedding and retrieval pipelines
- Building conversational AI or agents

**Do NOT invoke when:**
- Training custom ML models from scratch (use ml-engineer)
- Deploying ML models to production infrastructure (use mlops-engineer)
- Managing multi-agent coordination (use agent-organizer)
- Optimizing LLM serving infrastructure (use llm-architect)

## Decision Framework
```
AI Feature Type:
├── Simple Q&A → Direct LLM API call
├── Knowledge-based answers → RAG pipeline
├── Multi-step reasoning → Chain-of-thought or agents
├── External actions needed → Tool-use agents
├── Real-time data → Streaming + function calling
└── Complex workflows → Multi-agent orchestration
```

## Core Workflows

### 1. RAG Pipeline Implementation
1. Chunk documents with appropriate strategy
2. Generate embeddings using suitable model
3. Store in vector database with metadata
4. Implement semantic search with reranking
5. Construct prompts with retrieved context
6. Add evaluation and monitoring

### 2. LLM Integration
1. Select appropriate model for use case
2. Design prompt templates with versioning
3. Implement structured output parsing
4. Add retry logic and fallbacks
5. Monitor token usage and costs
6. Cache responses where appropriate

### 3. AI Agent Development
1. Define agent capabilities and tools
2. Implement tool interfaces with validation
3. Design agent loop with termination conditions
4. Add guardrails and safety checks
5. Implement logging and tracing
6. Test edge cases and failure modes

## Best Practices
- Version prompts alongside application code
- Use structured outputs (JSON mode) for reliability
- Implement semantic caching for common queries
- Add human-in-the-loop for critical decisions
- Monitor hallucination rates and retrieval quality
- Design for graceful degradation when AI fails

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Prompt in code | Hard to iterate and test | Use prompt templates with versioning |
| No evaluation | Unknown quality in production | Implement eval pipelines |
| Synchronous LLM calls | Slow user experience | Use streaming responses |
| Unbounded context | Token limits and cost | Implement context windowing |
| No fallbacks | System fails on API errors | Add retry logic and alternatives |
