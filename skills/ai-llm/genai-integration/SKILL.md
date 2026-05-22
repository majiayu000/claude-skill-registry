---
name: genai-integration
description: Expert guidance for integrating GenAI models, workflows, and observability into applications. (use when designing or implementing LLM/agent/RAG integrations)
version: 1.0.0
---

# Purpose
Teach the agent how to handle GenAI integration tasks — selecting models, building prompt templates, RAG pipelines, cost optimization, and validation workflows.

# When to Apply
Use this Skill when the user asks to:
- integrate a GenAI API into an application
- design RAG workflows, embeddings pipelines, or agents
- build prompt templates or schema-validated prompts
- write automation for cost or token optimization
- add testing, logging, or observability around GenAI tasks

# Instructions

1. **Detect Task Intent**
   - Identify if the request is about GenAI model selection, API integration, workflow design, or optimization.
   - If the task involves specific frameworks (Node/Python, serverless, Vercel/AWS), include relevant context.

2. **Model & Provider Guidance**
   - Recommend models according to cost, latency, context length, and compliance needs.
   - Prefer structured outputs (JSON schemas) and function/tool calling where appropriate.

3. **Prompt Engineering**
   - Generate prompt templates: system, developer, and user layers.
   - Use few-shot examples and explicit output schemas in prompts.

4. **RAG & Embeddings**
   - Break documents into chunks with semantic similarity filtering.
   - Outline vector store choice and search parameters (faiss/pinecone/weaviate).

5. **Agent Workflows**
   - If task requires agents, design tool use steps, fallback logic, and task decomposition.
   - Provide stepwise workflows for planning and execution.

6. **Cost & Token Strategy**
   - Suggest caching, batching, model tiering, and token budget limits.
   - Provide scripts or commands (in `scripts/`) for automation.

7. **Validation & Safety**
   - Add output validators (schema checks).
   - Mitigate prompt injection and unsafe operations.

# Output Format Guidelines
- Include JSON-schema blocks where structured output is required.

# Examples (Trigger Patterns)
- “Integrate LLM for customer support chatbot with RAG”
- “Design GenAI prompt templates for summarization API”
- “Automate token cost reduction for GenAI calls”
