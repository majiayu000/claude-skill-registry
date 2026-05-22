---
name: langfuse-observability
description: LLM observability platform for tracing, evaluation, prompt management, and cost tracking. Use when setting up Langfuse, monitoring LLM costs, tracking token usage, or implementing prompt versioning.
context: fork
agent: metrics-architect
version: 1.0.0
author: SkillForge AI Agent Hub
tags: [langfuse, llm, observability, tracing, evaluation, prompts, 2025]
user-invocable: false
---

# Langfuse Observability

## Overview

**Langfuse** is the open-source LLM observability platform that SkillForge uses for tracing, monitoring, evaluation, and prompt management. Unlike LangSmith (deprecated), Langfuse is self-hosted, free, and designed for production LLM applications.

**When to use this skill:**
- Setting up LLM observability from scratch
- Debugging slow or incorrect LLM responses
- Tracking token usage and costs
- Managing prompts in production
- Evaluating LLM output quality
- Migrating from LangSmith to Langfuse

**SkillForge Integration:**
- **Status**: Migrated from LangSmith (Dec 2025)
- **Location**: `backend/app/shared/services/langfuse/`
- **MCP Server**: `skillforge-langfuse` (optional)

---

## Quick Start

### Setup

```python
# backend/app/shared/services/langfuse/client.py
from langfuse import Langfuse
from app.core.config import settings

langfuse_client = Langfuse(
    public_key=settings.LANGFUSE_PUBLIC_KEY,
    secret_key=settings.LANGFUSE_SECRET_KEY,
    host=settings.LANGFUSE_HOST  # Self-hosted or cloud
)
```

### Basic Tracing with @observe

```python
from langfuse.decorators import observe, langfuse_context

@observe()  # Automatic tracing
async def analyze_content(content: str):
    langfuse_context.update_current_observation(
        metadata={"content_length": len(content)}
    )
    return await llm.generate(content)
```

### Session & User Tracking

```python
langfuse.trace(
    name="analysis",
    user_id="user_123",
    session_id="session_abc",
    metadata={"content_type": "article", "agent_count": 8},
    tags=["production", "skillforge"]
)
```

---

## Core Features Summary

| Feature | Description | Reference |
|---------|-------------|-----------|
| Distributed Tracing | Track LLM calls with parent-child spans | `references/tracing-setup.md` |
| Cost Tracking | Automatic token & cost calculation | `references/cost-tracking.md` |
| Prompt Management | Version control for prompts | `references/prompt-management.md` |
| LLM Evaluation | Custom scoring with G-Eval | `references/evaluation-scores.md` |
| Session Tracking | Group related traces | `references/session-tracking.md` |
| Experiments API | A/B testing & benchmarks | `references/experiments-api.md` |
| Multi-Judge Eval | Ensemble LLM evaluation | `references/multi-judge-evaluation.md` |

---

## References

### Tracing Setup
**See: `references/tracing-setup.md`**

Key topics covered:
- Initializing Langfuse client with @observe decorator
- Creating nested traces and spans
- Tracking LLM generations with metadata
- LangChain/LangGraph CallbackHandler integration
- Workflow integration patterns

### Cost Tracking
**See: `references/cost-tracking.md`**

Key topics covered:
- Automatic cost calculation from token usage
- Custom model pricing configuration
- Monitoring dashboard SQL queries
- Cost tracking per analysis/user
- Daily cost trend analysis

### Prompt Management
**See: `references/prompt-management.md`**

Key topics covered:
- Prompt versioning and labels (production/staging/draft)
- Template variables with Jinja2 syntax
- A/B testing prompt versions
- SkillForge 4-level caching architecture (L1-L4)
- Linking prompts to generation spans

### LLM Evaluation
**See: `references/evaluation-scores.md`**

Key topics covered:
- Custom scoring with numeric/categorical values
- G-Eval automated quality assessment
- Score trends and comparisons
- Filtering traces by score thresholds

### Session Tracking
**See: `references/session-tracking.md`**

Key topics covered:
- Grouping traces by session_id
- Multi-turn conversation tracking
- User and metadata analytics

### Experiments API
**See: `references/experiments-api.md`**

Key topics covered:
- Creating test datasets in Langfuse
- Running automated evaluations
- Regression testing for LLMs
- Benchmarking prompt versions

### Multi-Judge Evaluation
**See: `references/multi-judge-evaluation.md`**

Key topics covered:
- Multiple LLM judges for quality assessment
- Weighted scoring across judges
- SkillForge langfuse_evaluators.py integration

---

## Best Practices

1. **Always use @observe decorator** for automatic tracing
2. **Set user_id and session_id** for better analytics
3. **Add meaningful metadata** (content_type, analysis_id, etc.)
4. **Score all production traces** for quality monitoring
5. **Use prompt management** instead of hardcoded prompts
6. **Monitor costs daily** to catch spikes early
7. **Create datasets** for regression testing
8. **Tag production vs staging** traces

---

## LangSmith Migration Notes

**Key Differences:**
| Aspect | Langfuse | LangSmith |
|--------|----------|-----------|
| Hosting | Self-hosted, open-source | Cloud-only, proprietary |
| Cost | Free | Paid |
| Prompts | Built-in management | External storage needed |
| Decorator | `@observe` | `@traceable` |

---

## External References

- [Langfuse Docs](https://langfuse.com/docs)
- [Python SDK](https://langfuse.com/docs/sdk/python)
- [Decorators Guide](https://langfuse.com/docs/sdk/python/decorators)
- [Prompt Management](https://langfuse.com/docs/prompts)
- [Self-Hosting](https://langfuse.com/docs/deployment/self-host)

---

## Capability Details

### distributed-tracing
**Keywords:** trace, tracing, observability, span, nested, parent-child, observe
**Solves:**
- How do I trace LLM calls across my application?
- How to debug slow LLM responses?
- Track execution flow in multi-agent workflows
- Create nested trace spans

### cost-tracking
**Keywords:** cost, token usage, pricing, budget, spend, expense
**Solves:**
- How do I track LLM costs?
- Calculate token usage and pricing
- Monitor AI budget and spending
- Track cost per user or session

### prompt-management
**Keywords:** prompt version, prompt template, prompt control, prompt registry
**Solves:**
- How do I version control prompts?
- Manage prompts in production
- A/B test different prompt versions
- Link prompts to traces

### llm-evaluation
**Keywords:** score, quality, evaluation, rating, assessment, g-eval
**Solves:**
- How do I evaluate LLM output quality?
- Score responses with custom metrics
- Track quality trends over time
- Compare prompt versions by quality

### session-tracking
**Keywords:** session, user tracking, conversation, group traces
**Solves:**
- How do I group related traces?
- Track multi-turn conversations
- Monitor per-user performance
- Organize traces by session

### langchain-integration
**Keywords:** langchain, callback, handler, langgraph integration
**Solves:**
- How do I integrate Langfuse with LangChain?
- Use CallbackHandler for tracing
- Automatic LangGraph workflow tracing
- LangChain observability setup

### datasets-evaluation
**Keywords:** dataset, test set, evaluation dataset, benchmark
**Solves:**
- How do I create test datasets in Langfuse?
- Run automated evaluations
- Regression testing for LLMs
- Benchmark prompt versions

### ab-testing
**Keywords:** a/b test, experiment, compare prompts, variant testing
**Solves:**
- How do I A/B test prompts?
- Compare two prompt versions
- Experimental prompt evaluation
- Statistical prompt testing

### monitoring-dashboard
**Keywords:** dashboard, analytics, metrics, monitoring, queries
**Solves:**
- What are the most expensive traces?
- Average cost by agent type
- Quality score trends
- Custom monitoring queries

### skillforge-integration
**Keywords:** skillforge, migration, setup, workflow integration
**Solves:**
- How does SkillForge use Langfuse?
- Migrate from LangSmith to Langfuse
- SkillForge workflow tracing patterns
- Cost tracking per analysis

### multi-judge-evaluation
**Keywords:** multi judge, g-eval, multiple evaluators, ensemble evaluation, weighted scoring
**Solves:**
- How do I use multiple LLM judges to evaluate quality?
- Set up G-Eval criteria evaluation
- Configure weighted scoring across judges
- Wire SkillForge's existing langfuse_evaluators.py

### experiments-api
**Keywords:** experiment, dataset, benchmark, regression test, prompt testing
**Solves:**
- How do I run experiments across datasets?
- A/B test models and prompts systematically
- Track quality regression over time
- Compare experiment results