---
name: graphrag-patterns
description: GraphRAG implementation patterns for hybrid search, Text2Cypher, and agentic retrieval. Use when implementing RAG workflows with Neo4j.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# GraphRAG Patterns

## Hybrid Search (Vector + Keyword)

Combine vector similarity with full-text search for better recall:

```python
from langchain_neo4j import Neo4jVector

def create_hybrid_retriever(driver, embeddings):
    return Neo4jVector.from_existing_graph(
        embeddings,
        driver=driver,
        index_name="article_embeddings",
        keyword_index_name="article_fulltext",
        search_type="hybrid",  # Combines vector + keyword
        node_label="Article",
        text_node_properties=["content", "summary"],
        embedding_node_property="embedding",
    )
```

## Text2Cypher with Few-Shot Examples

Always provide examples for better query generation:

```python
FEW_SHOT_EXAMPLES = [
    {
        "question": "What articles discuss requirements traceability?",
        "cypher": '''
            MATCH (a:Article)
            WHERE a.content CONTAINS 'traceability'
            RETURN a.title, a.summary
            LIMIT 10
        '''
    },
    {
        "question": "Which chapters have the most articles?",
        "cypher": '''
            MATCH (c:Chapter)-[:CONTAINS]->(a:Article)
            RETURN c.title, count(a) as article_count
            ORDER BY article_count DESC
        '''
    },
]

from langchain_neo4j import GraphCypherQAChain

chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    cypher_prompt=CYPHER_PROMPT,
    example_selector=SemanticSimilarityExampleSelector.from_examples(
        FEW_SHOT_EXAMPLES,
        embeddings,
        k=3,
    ),
    validate_cypher=True,
)
```

## Agentic Router Pattern

Route queries to the best retrieval strategy:

```python
from langchain_core.prompts import ChatPromptTemplate

ROUTER_PROMPT = ChatPromptTemplate.from_template('''
Classify the query into one of these retrieval strategies:

- VECTOR: Semantic similarity search (concepts, topics, "similar to")
- CYPHER: Structured queries (counts, relationships, specific filters)
- HYBRID: Complex queries needing both approaches

Query: {query}

Strategy:''')

async def route_query(query: str, llm) -> str:
    response = await llm.ainvoke(ROUTER_PROMPT.format(query=query))
    return response.content.strip().upper()
```

## Graph-Enriched Retrieval

Augment vector results with graph context:

```python
async def graph_enriched_search(driver, query: str, embeddings) -> list[dict]:
    # Step 1: Vector search for relevant articles
    vector_results = await vector_search(driver, query, embeddings, limit=5)

    # Step 2: Expand with graph traversal
    article_ids = [r["id"] for r in vector_results]

    enrichment_query = '''
        MATCH (a:Article) WHERE a.id IN $ids
        OPTIONAL MATCH (a)<-[:CONTAINS]-(c:Chapter)
        OPTIONAL MATCH (a)-[:RELATED_TO]->(related:Article)
        RETURN a, c.title as chapter, collect(DISTINCT related.title) as related_articles
    '''

    enriched = await execute_read_query(driver, enrichment_query, {"ids": article_ids})
    return enriched
```

## RAGAS Evaluation Metrics

Evaluate retrieval quality:

```python
from ragas.metrics import (
    context_precision,
    context_recall,
    faithfulness,
    answer_relevancy,
)
from ragas import evaluate

def evaluate_retrieval(questions, ground_truths, contexts, answers):
    dataset = Dataset.from_dict({
        "question": questions,
        "ground_truth": ground_truths,
        "contexts": contexts,
        "answer": answers,
    })

    results = evaluate(
        dataset,
        metrics=[
            context_precision,
            context_recall,
            faithfulness,
            answer_relevancy,
        ],
    )
    return results
```

## Stepback Prompting

For complex queries, generate a broader question first:

```python
STEPBACK_PROMPT = '''
Given a specific question, generate a more general "stepback" question
that would help gather broader context before answering the specific question.

Specific question: {question}
Stepback question:'''

async def stepback_retrieval(query: str, retriever, llm):
    # Generate stepback question
    stepback_q = await llm.ainvoke(STEPBACK_PROMPT.format(question=query))

    # Retrieve for both questions
    specific_docs = await retriever.ainvoke(query)
    stepback_docs = await retriever.ainvoke(stepback_q.content)

    # Combine and deduplicate
    all_docs = {doc.page_content: doc for doc in specific_docs + stepback_docs}
    return list(all_docs.values())
```
