---
name: e2e-testing
version: 1.0
last_updated: 2025-12-04
description: End-to-end RAG pipeline testing (query → retrieval → generation → answer)
license: MIT
priority: high
triggers:
  - "E2E", "pipeline test", "integration test", "end-to-end"
dependencies:
  - langsmith-testing-SKILL.md
  - rag-accuracy-SKILL.md
---

# 🧪 E2E Testing SKILL

## Purpose

Test complete RAG pipeline: query → embedding → retrieval → reranking → generation → answer validation.

---

## Pipeline Test Structure

### Python (pytest)

```python
import pytest
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

@pytest.fixture
def rag_chain():
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.load_local("./test_index", embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    llm = ChatOpenAI(model="gpt-4", temperature=0)
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return chain

def test_rag_pipeline_happy_path(rag_chain):
    """Test: Normal query returns valid answer"""
    query = "What is retrieval augmented generation?"
    result = rag_chain.invoke(query)

    # Assertions
    assert "answer" in result
    assert len(result["answer"]) > 0
    assert len(result["source_documents"]) > 0

    # Quality checks
    from ragas.metrics import Faithfulness
    metric = Faithfulness()
    score = metric.score({
        "question": query,
        "answer": result["answer"],
        "contexts": [doc.page_content for doc in result["source_documents"]]
    })
    assert score > 0.7, f"Faithfulness too low: {score}"
```

### Next.js (Playwright)

```typescript
import { test, expect } from '@playwright/test';

test('RAG pipeline returns answer', async ({ request }) => {
  const response = await request.post('/api/rag/query', {
    data: { query: 'What is RAG?' }
  });

  expect(response.ok()).toBeTruthy();
  const data = await response.json();

  expect(data.answer).toBeDefined();
  expect(data.answer.length).toBeGreaterThan(0);
  expect(data.sourceDocuments.length).toBeGreaterThan(0);
  expect(data.faithfulness).toBeGreaterThan(0.7);
});
```

---

## Test Categories

### 1. Happy Path Tests

```python
def test_simple_question(rag_chain):
    """Test: Simple factual question"""
    result = rag_chain.invoke("What is machine learning?")
    assert "machine learning" in result["answer"].lower()

def test_retrieval_returns_relevant_docs(rag_chain):
    """Test: Retrieved docs are relevant"""
    result = rag_chain.invoke("Explain neural networks")

    for doc in result["source_documents"]:
        assert any(keyword in doc.page_content.lower()
                   for keyword in ["neural", "network", "layer"])
```

### 2. Sad Path Tests (Error Handling)

```python
def test_empty_query(rag_chain):
    """Test: Empty query handled gracefully"""
    with pytest.raises(ValueError, match="Query cannot be empty"):
        rag_chain.invoke("")

def test_no_relevant_docs(rag_chain):
    """Test: Query with no relevant documents"""
    result = rag_chain.invoke("Quantum computing in 1850")

    assert "answer" in result
    assert "don't know" in result["answer"].lower() or \
           "no information" in result["answer"].lower()
```

### 3. Edge Case Tests

```python
def test_very_long_query(rag_chain):
    """Test: Handle long queries (>1000 chars)"""
    long_query = "What is " + "machine learning " * 100
    result = rag_chain.invoke(long_query[:1000])  # Truncate

    assert len(result["answer"]) > 0

def test_special_characters(rag_chain):
    """Test: Handle special characters"""
    query = "What is @#$% <script>alert('xss')</script>?"
    result = rag_chain.invoke(query)

    assert "script" not in result["answer"]  # XSS protection
```

---

## Latency Testing

```python
import time

def test_query_latency(rag_chain):
    """Test: Query completes within 2 seconds"""
    query = "What is RAG?"

    start = time.time()
    result = rag_chain.invoke(query)
    latency = (time.time() - start) * 1000  # ms

    assert latency < 2000, f"Query too slow: {latency}ms"

def test_batch_queries_parallel(rag_chain):
    """Test: Multiple queries in parallel"""
    import concurrent.futures

    queries = [
        "What is RAG?",
        "How does retrieval work?",
        "What are embeddings?"
    ]

    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(rag_chain.invoke, queries))
    total_time = time.time() - start

    assert all(len(r["answer"]) > 0 for r in results)
    assert total_time < 5.0, "Batch queries too slow"
```

---

## LangSmith Integration

```python
import os
from langchain_core.tracers.context import tracing_v2_enabled

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "rag-e2e-tests"

def test_with_langsmith_trace(rag_chain):
    """Test: Query traced in LangSmith"""
    query = "What is RAG?"

    with tracing_v2_enabled(project_name="rag-e2e-tests") as cb:
        result = rag_chain.invoke(query)
        run_id = cb.run_id

    # Validate trace exists
    from langsmith import Client
    client = Client()
    run = client.read_run(run_id)

    assert run is not None
    assert run.error is None
    assert run.latency_ms < 2000
```

**See:** `langsmith-testing-SKILL.md`

---

## Metric Assertions

```python
from ragas.metrics import Faithfulness, ContextRelevance

def test_faithfulness_threshold(rag_chain):
    """Test: Answer faithfulness > 0.7"""
    query = "What is machine learning?"
    result = rag_chain.invoke(query)

    metric = Faithfulness()
    score = metric.score({
        "question": query,
        "answer": result["answer"],
        "contexts": [doc.page_content for doc in result["source_documents"]]
    })

    assert score > 0.7, f"Faithfulness: {score:.2f}"

def test_relevance_threshold(rag_chain):
    """Test: Context relevance > 0.7"""
    query = "Explain neural networks"
    result = rag_chain.invoke(query)

    metric = ContextRelevance()
    score = metric.score({
        "question": query,
        "contexts": [doc.page_content for doc in result["source_documents"]]
    })

    assert score > 0.7, f"Relevance: {score:.2f}"
```

**See:** `rag-accuracy-SKILL.md`

---

## CI/CD Integration

### GitHub Actions

```yaml
name: RAG E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest ragas

      - name: Run E2E tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          LANGSMITH_API_KEY: ${{ secrets.LANGSMITH_API_KEY }}
        run: pytest tests/e2e/ -v

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: pytest-results
          path: pytest-report.xml
```

---

## Test Data Management

```python
import pytest

@pytest.fixture(scope="session")
def test_documents():
    """Load test documents once per session"""
    return [
        "RAG is Retrieval Augmented Generation...",
        "Vector embeddings enable semantic search...",
        "LangChain is a framework for LLMs..."
    ]

@pytest.fixture(scope="session")
def test_vector_store(test_documents):
    """Create test vector store"""
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain.schema import Document

    docs = [Document(page_content=text) for text in test_documents]
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(docs, embeddings)

    return vector_store
```

---

**Last Updated:** 2025-12-04
**Version:** 1.0
**Adapted from:** WHRESUME testing-checklist-SKILL.md
