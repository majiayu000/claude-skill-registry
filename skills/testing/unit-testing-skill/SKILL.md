---
name: unit-testing
version: 1.0
last_updated: 2025-12-04
description: Component isolation and unit testing for RAG components
license: MIT
priority: medium
triggers:
  - "unit test", "component test", "mocking"
---

# 🧩 Unit Testing SKILL

## Purpose

Test individual RAG components in isolation using mocking and dependency injection.

---

## Component Isolation

### 1. Test Embedder

```python
import pytest
from unittest.mock import Mock

def test_embedder_produces_correct_dimensions(mocker):
    """Test: Embedder returns correct vector dimensions"""
    mock_llm = mocker.Mock()
    mock_llm.embed_query.return_value = [0.1] * 1536

    embedder = Embedder(mock_llm)
    result = embedder.embed("test query")

    assert len(result) == 1536
    assert isinstance(result, list)
    assert all(isinstance(x, float) for x in result)

def test_embedder_handles_empty_input(mocker):
    """Test: Embedder handles empty strings"""
    mock_llm = mocker.Mock()
    embedder = Embedder(mock_llm)

    with pytest.raises(ValueError, match="Input cannot be empty"):
        embedder.embed("")
```

### 2. Test Retriever

```python
def test_retriever_returns_top_k_documents(mocker):
    """Test: Retriever returns correct number of documents"""
    mock_vector_store = mocker.Mock()
    mock_vector_store.similarity_search.return_value = [
        Document(page_content="doc1"),
        Document(page_content="doc2"),
        Document(page_content="doc3")
    ]

    retriever = Retriever(mock_vector_store, k=3)
    results = retriever.retrieve("test query")

    assert len(results) == 3
    mock_vector_store.similarity_search.assert_called_once()

def test_retriever_filters_by_metadata(mocker):
    """Test: Retriever applies metadata filters"""
    mock_vector_store = mocker.Mock()
    retriever = Retriever(mock_vector_store)

    retriever.retrieve("query", filter={"category": "technical"})

    call_args = mock_vector_store.similarity_search.call_args
    assert call_args.kwargs["filter"] == {"category": "technical"}
```

### 3. Test Reranker

```python
def test_reranker_sorts_by_relevance(mocker):
    """Test: Reranker orders documents by score"""
    mock_model = mocker.Mock()
    mock_model.predict.return_value = [0.9, 0.3, 0.7]

    reranker = Reranker(mock_model)
    docs = [
        Document(page_content="doc1"),
        Document(page_content="doc2"),
        Document(page_content="doc3")
    ]

    reranked = reranker.rerank("query", docs)

    assert reranked[0].metadata["score"] == 0.9
    assert reranked[1].metadata["score"] == 0.7
    assert reranked[2].metadata["score"] == 0.3
```

---

## Mocking

### 1. Mock LangSmith Client

```python
@pytest.fixture
def mock_langsmith():
    """Mock LangSmith client to avoid external API calls"""
    with patch('langsmith.Client') as mock:
        mock.return_value.create_feedback.return_value = None
        yield mock

def test_feedback_sent_to_langsmith(mock_langsmith):
    """Test: Feedback is sent to LangSmith"""
    client = mock_langsmith()

    send_feedback(
        run_id="test-123",
        key="faithfulness",
        score=0.85
    )

    client.create_feedback.assert_called_once_with(
        run_id="test-123",
        key="faithfulness",
        score=0.85
    )
```

### 2. Mock LLM Calls

```python
@pytest.fixture
def mock_llm():
    """Mock LLM to avoid expensive API calls"""
    with patch('langchain_openai.ChatOpenAI') as mock:
        mock.return_value.invoke.return_value = "Mocked response"
        yield mock

def test_llm_called_with_correct_prompt(mock_llm):
    """Test: LLM receives correctly formatted prompt"""
    llm = mock_llm()

    generate_answer(
        query="What is RAG?",
        context=["RAG is..."]
    )

    call_args = llm.invoke.call_args[0][0]
    assert "What is RAG?" in call_args
    assert "RAG is..." in call_args
```

---

## Test Fixtures

### 1. Shared Test Data

```python
@pytest.fixture(scope="module")
def sample_documents():
    """Provide sample documents for testing"""
    return [
        Document(
            page_content="RAG is Retrieval Augmented Generation",
            metadata={"source": "doc1.txt"}
        ),
        Document(
            page_content="Vector embeddings enable semantic search",
            metadata={"source": "doc2.txt"}
        )
    ]

@pytest.fixture(scope="module")
def sample_embeddings():
    """Provide sample embeddings"""
    return [
        [0.1, 0.2, 0.3],  # 3-dimensional for testing
        [0.4, 0.5, 0.6]
    ]
```

### 2. Mock Vector Store

```python
@pytest.fixture
def mock_vector_store(sample_documents):
    """Create mock vector store with test data"""
    mock_store = Mock()
    mock_store.similarity_search.return_value = sample_documents
    return mock_store
```

---

## Coverage

### 1. Running Coverage

```bash
# Run tests with coverage
pytest --cov=src tests/unit/

# Generate HTML report
pytest --cov=src --cov-report=html tests/unit/

# View report
open htmlcov/index.html
```

### 2. Coverage Targets

| Component | Target Coverage | Priority |
|-----------|----------------|----------|
| Core logic | 90%+ | High |
| Utilities | 80%+ | Medium |
| Integration | 70%+ | Medium |
| UI/API | 60%+ | Low |

### 3. Coverage Configuration

```ini
# .coveragerc
[run]
source = src
omit =
    */tests/*
    */migrations/*
    */venv/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:
```

---

## Test Organization

### Directory Structure

```
tests/
├── unit/
│   ├── test_embedder.py
│   ├── test_retriever.py
│   ├── test_reranker.py
│   └── test_generator.py
├── integration/
│   └── test_rag_chain.py
├── e2e/
│   └── test_pipeline.py
└── fixtures/
    └── conftest.py
```

### Naming Conventions

```python
# Test files: test_*.py
# Test functions: test_*

# Good names (descriptive)
def test_embedder_handles_empty_input()
def test_retriever_returns_top_k_documents()
def test_reranker_filters_low_scores()

# Bad names (vague)
def test_embedder()
def test_basic()
def test_1()
```

---

## Best Practices

### 1. Fast Tests

```python
# Good: Mock external dependencies
@patch('openai.Embedding.create')
def test_fast(mock_embed):
    mock_embed.return_value = {"data": [{"embedding": [0.1]}]}
    # Test runs instantly

# Bad: Real API calls
def test_slow():
    embeddings = OpenAIEmbeddings()
    result = embeddings.embed_query("test")
    # Takes 1-2 seconds per test
```

### 2. Isolated Tests

```python
# Good: Each test is independent
def test_a():
    state = create_clean_state()
    assert state.value == 0

def test_b():
    state = create_clean_state()
    assert state.increment() == 1

# Bad: Tests depend on each other
state = None
def test_a():
    global state
    state = create_state()

def test_b():
    global state  # Depends on test_a running first
    assert state.value == 0
```

### 3. Clear Assertions

```python
# Good: Specific assertions
def test_retriever():
    results = retriever.retrieve("query")
    assert len(results) == 5
    assert all(isinstance(doc, Document) for doc in results)
    assert results[0].metadata["score"] > 0.8

# Bad: Vague assertions
def test_retriever():
    results = retriever.retrieve("query")
    assert results  # What does this check?
```

---

## Troubleshooting

### Issue: Tests too slow

**Solution:**
```python
# Use mocks instead of real dependencies
@patch('langchain_openai.ChatOpenAI')
def test_with_mock(mock_llm):
    mock_llm.return_value.invoke.return_value = "mocked"
    # Test runs instantly
```

### Issue: Flaky tests

**Solution:**
```python
# Set random seeds for reproducibility
import random
import numpy as np

@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(42)
    np.random.seed(42)
```

### Issue: Hard to test private methods

**Solution:**
```python
# Test through public interface
def test_public_method():
    obj = MyClass()
    result = obj.public_method()  # Calls private method internally
    assert result == expected

# Or make method protected (_method) and test directly
def test_protected_method():
    obj = MyClass()
    result = obj._internal_logic()  # Test implementation detail
    assert result == expected
```

---

**Last Updated:** 2025-12-04
**Version:** 1.0
**Priority:** Medium (Component-level testing)
