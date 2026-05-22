---
name: llm-pipeline
description: Pydantic-AI agents, RAG, embeddings for Pulse Radar knowledge extraction.
---

# LLM Pipeline Skill

<overview>
Pulse Radar uses LLM pipeline to transform raw Telegram messages into structured knowledge.
Core philosophy: Messages individually are noise; batched extraction reveals patterns.
</overview>

<entity-hierarchy>
```
TOPICS (categories)
  └─ ATOMS (knowledge units: problem/solution/decision/insight...)
       └─ MESSAGES (raw data, hidden layer)
```
</entity-hierarchy>

<extraction-flow>
```python
# 1. Message arrives via Telegram webhook
await save_telegram_message(message)  # triggers TaskIQ

# 2. Scoring (AI Judge, not heuristics - ADR-003)
score = await importance_scorer.score(message)
# classification: SIGNAL (>0.6) / NOISE (<0.3)

# 3. Auto-trigger extraction when threshold met
if unprocessed_count >= 10:  # ai_config.message_threshold
    await extract_knowledge_from_messages_task.kiq()

# 4. KnowledgeOrchestrator runs Pydantic AI agent
agent = Agent(
    model=model,
    system_prompt=get_extraction_prompt("uk"),
    output_type=KnowledgeExtractionOutput,  # CRITICAL: structured output
    output_retries=5,
)
result = await agent.run(messages_content)

# 5. Save to DB + embed
await save_topics_and_atoms(result.output)
await embed_atoms_batch_task.kiq(atom_ids)
```
</extraction-flow>

<agent-creation>
```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel

# Provider-specific model creation
if provider.type == "ollama":
    model = OpenAIChatModel(
        model_name=agent_config.model_name,
        provider=OllamaProvider(base_url=provider.base_url),
    )
elif provider.type == "openai":
    model = OpenAIChatModel(
        model_name=agent_config.model_name,
        provider=OpenAIProvider(api_key=api_key),
    )

# Agent with structured output
agent = Agent(
    model=model,
    output_type=MyPydanticModel,  # Forces JSON schema
    system_prompt="...",
    output_retries=5,
)
```
</agent-creation>

<prompt-guidelines>
1. **JSON-only output** — explicitly state "respond with ONLY JSON"
2. **Schema in prompt** — include exact JSON structure expected
3. **Language enforcement** — "ALL fields MUST be in Ukrainian"
4. **Retry on language mismatch** — use `get_strengthened_prompt()`
5. **No markdown** — models often wrap JSON in ```json blocks
</prompt-guidelines>

<embedding-service>
```python
# OpenAI: 1536 dimensions (text-embedding-3-small)
# Ollama: 1024 dimensions (mxbai-embed-large) → padded to 1536

await embedding_service.generate_embedding(text)
await embedding_service.embed_messages_batch(session, ids, batch_size=10)
```
</embedding-service>

<rag-context>
```python
# SemanticSearchService uses pgvector cosine similarity
similar_atoms = await search_service.search_atoms(
    query_embedding=embedding,
    limit=5,
    threshold=0.65,  # ai_config.semantic_search
)

# RAGContextBuilder assembles context for LLM
context = await rag_builder.build_context(
    query=user_query,
    similar_atoms=similar_atoms,
    related_messages=messages,
)
```
</rag-context>

<context-strategies>
## RAG vs CAG

| Strategy | Data Type | Pulse Radar Use |
|----------|-----------|-----------------|
| **RAG** | Dynamic (messages, atoms) | Semantic search, history retrieval |
| **CAG** | Static (project config) | Keywords, glossary, components preloaded |

**Hybrid:** Project context (CAG) + similar atoms (RAG) = best extraction quality.
See: @references/rag.md for detailed comparison.
</context-strategies>

<adrs>
- **ADR-003:** AI Importance Scoring — LLM Judge vs Heuristics (LLM chosen)
- **ADR-006:** Pydantic AI vs LangChain — Hexagonal architecture (Pydantic AI chosen)
</adrs>

<references>
- @references/architecture.md — Hexagonal LLM domain structure
- @references/pydantic-ai.md — Agent configuration, streaming
- @references/rag.md — RAG & CAG context strategies
</references>
