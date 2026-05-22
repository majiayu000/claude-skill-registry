---
name: agentic-rag-patterns
description: Advanced RAG with Self-RAG, Corrective-RAG, and knowledge graphs. Use when building agentic RAG pipelines, adaptive retrieval, or query rewriting.
version: 1.0.0
tags: [rag, self-rag, crag, knowledge-graph, langgraph, agentic, 2026]
context: fork
agent: data-pipeline-engineer
author: SkillForge
user-invocable: false
---

# Agentic RAG Patterns

Build self-correcting retrieval systems with LLM-driven decision making.

> **LangGraph 1.0.6** (Jan 2026): langgraph-checkpoint 4.0.0, compile-time checkpointer validation, namespace sanitization.

## Architecture Overview

```
Query → [Retrieve] → [Grade] → [Generate/Rewrite/Web Search] → Response
              ↓           ↓
         Documents    Quality Check
                          ↓
                   Route Decision:
                   - Good docs → Generate
                   - Poor docs → Rewrite query
                   - No docs → Web fallback
```

## Self-RAG State Definition

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Annotated
from langchain_core.documents import Document
import operator

class RAGState(TypedDict):
    """State for agentic RAG workflows."""
    question: str
    documents: Annotated[List[Document], operator.add]
    generation: str
    web_search_needed: bool
    retry_count: int
    relevance_scores: dict[str, float]
```

## Core Retrieval Node

```python
def retrieve(state: RAGState) -> dict:
    """Retrieve documents from vector store."""
    question = state["question"]
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}
```

## Document Grading (Self-RAG Core)

```python
from pydantic import BaseModel, Field

class GradeDocuments(BaseModel):
    """Binary score for document relevance."""
    binary_score: str = Field(
        description="Relevance score 'yes' or 'no'"
    )

def grade_documents(state: RAGState) -> dict:
    """Grade documents for relevance - core Self-RAG pattern."""
    question = state["question"]
    documents = state["documents"]

    filtered_docs = []
    relevance_scores = {}

    for doc in documents:
        score = retrieval_grader.invoke({
            "question": question,
            "document": doc.page_content
        })
        doc_id = doc.metadata.get("id", hash(doc.page_content))
        relevance_scores[doc_id] = 1.0 if score.binary_score == "yes" else 0.0

        if score.binary_score == "yes":
            filtered_docs.append(doc)

    # Trigger web search if too many docs filtered out
    web_search_needed = len(filtered_docs) < len(documents) // 2

    return {
        "documents": filtered_docs,
        "web_search_needed": web_search_needed,
        "relevance_scores": relevance_scores
    }
```

## Query Transformation

```python
def transform_query(state: RAGState) -> dict:
    """Transform query for better retrieval."""
    question = state["question"]

    better_question = question_rewriter.invoke({
        "question": question,
        "feedback": "Rephrase to improve retrieval. Be specific."
    })

    return {
        "question": better_question,
        "retry_count": state.get("retry_count", 0) + 1
    }
```

## Web Search Fallback (CRAG)

```python
def web_search(state: RAGState) -> dict:
    """Fallback to web search when documents insufficient."""
    question = state["question"]

    web_results = tavily_client.search(
        question,
        max_results=5,
        search_depth="advanced"
    )

    web_docs = [
        Document(
            page_content=r["content"],
            metadata={"source": r["url"], "type": "web"}
        )
        for r in web_results
    ]

    return {"documents": web_docs, "web_search_needed": False}
```

## Generation Node

```python
def generate(state: RAGState) -> dict:
    """Generate answer from documents."""
    question = state["question"]
    documents = state["documents"]

    context = "\n\n".join([
        f"[{i+1}] {doc.page_content}"
        for i, doc in enumerate(documents)
    ])

    generation = rag_chain.invoke({
        "context": context,
        "question": question
    })

    return {"generation": generation}
```

## Conditional Routing

```python
def route_after_grading(state: RAGState) -> str:
    """Route based on document quality."""
    if state["web_search_needed"]:
        if state.get("retry_count", 0) < 2:
            return "transform_query"  # Try rewriting first
        return "web_search"  # Fallback to web
    return "generate"  # Documents are good

workflow.add_conditional_edges(
    "grade",
    route_after_grading,
    {
        "generate": "generate",
        "transform_query": "transform_query",
        "web_search": "web_search"
    }
)
```

## Complete CRAG Workflow

```python
def build_crag_workflow() -> StateGraph:
    """Build Corrective-RAG workflow with web fallback."""
    workflow = StateGraph(RAGState)

    # Add nodes
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade", grade_documents)
    workflow.add_node("generate", generate)
    workflow.add_node("web_search", web_search)
    workflow.add_node("transform_query", transform_query)

    # Define edges
    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "grade")

    # Conditional routing based on document quality
    workflow.add_conditional_edges(
        "grade",
        route_after_grading,
        {
            "generate": "generate",
            "transform_query": "transform_query",
            "web_search": "web_search"
        }
    )

    # After query transform, retry retrieval
    workflow.add_edge("transform_query", "retrieve")

    # Web search leads to generation
    workflow.add_edge("web_search", "generate")

    workflow.add_edge("generate", END)

    return workflow.compile()
```

## Pattern Comparison

| Pattern | When to Use | Key Feature |
|---------|-------------|-------------|
| Self-RAG | Need adaptive retrieval | LLM decides when to retrieve |
| CRAG | Need quality assurance | Document grading + web fallback |
| GraphRAG | Entity-rich domains | Knowledge graph + vector hybrid |
| Agentic | Complex multi-step | Full plan-route-act-verify loop |

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Grading threshold | Binary (yes/no) simpler than scores |
| Max retries | 2-3 for query rewriting |
| Web search | Use as last resort (latency, cost) |
| Fallback order | Rewrite → Web → Abstain |

## Common Mistakes

- No fallback path (hangs on bad queries)
- Infinite rewrite loops (no retry limit)
- Web search on every query (expensive)
- Not tracking relevance scores (can't debug)

## Related Skills

- `rag-retrieval` - Basic RAG patterns this enhances
- `langgraph-routing` - Conditional edge patterns
- `langgraph-state` - State design with reducers
- `contextual-retrieval` - Anthropic's context-prepending
- `reranking-patterns` - Post-retrieval reranking

## Capability Details

### self-rag
**Keywords:** self-rag, adaptive retrieval, reflection tokens
**Solves:**
- Build self-correcting RAG systems
- Implement adaptive retrieval logic
- Add reflection tokens for quality

### corrective-rag
**Keywords:** crag, document grading, web fallback
**Solves:**
- Implement CRAG workflows
- Grade document relevance
- Add web search fallback

### knowledge-graph-rag
**Keywords:** graphrag, neo4j, entity extraction
**Solves:**
- Combine KG with vector search
- Entity-based retrieval
- Multi-hop reasoning

### adaptive-retrieval
**Keywords:** query routing, multi-source, orchestration
**Solves:**
- Route queries to optimal sources
- Multi-retriever orchestration
- Dynamic retrieval strategies
