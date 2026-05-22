---
name: langsmith-testing
version: 1.0
last_updated: 2025-12-04
description: LangSmith trace validation for RAG observability - every query must be traced
license: MIT
priority: critical
triggers:
  - "LangSmith", "trace", "evaluation", "tracking", "observability"
  - RAG query execution
  - Evaluation tasks
dependencies:
  - rag-accuracy-SKILL.md
compatibility:
  - langchain: ">=0.1.0"
  - langsmith: ">=0.1.0"
changelog:
  - version: 1.0
    date: 2025-12-04
    changes:
      - Initial release for RAG demo
      - LangSmith API integration
      - Trace collection and validation
---

# 📊 LangSmith Testing SKILL

## Purpose

**CRITICAL for RAG:** Every RAG query MUST be traced in LangSmith for observability. Silent failures (bad retrieval, hallucinations) are only detectable through tracing.

---

## Auto-Trigger Conditions

**Activate when:**
- User mentions: "LangSmith", "trace", "evaluation", "tracking"
- RAG query execution
- Evaluation tasks
- Performance debugging

---

## LangSmith Setup

### 1. Installation

```bash
# Python
pip install langsmith langchain

# Environment variables
export LANGSMITH_API_KEY="your-api-key"
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_PROJECT="rag-demo"
```

### 2. Basic Integration

```python
from langchain.callbacks import LangChainTracer
from langsmith import Client

# Initialize client
client = Client(api_key=os.environ["LANGSMITH_API_KEY"])

# Create tracer
tracer = LangChainTracer(project_name="rag-demo")

# Use in chain
chain.invoke(query, config={"callbacks": [tracer]})
```

---

## Trace Collection

### 1. Automatic Tracing (Recommended)

```python
from langchain_core.tracers.context import tracing_v2_enabled

with tracing_v2_enabled(project_name="rag-demo"):
    # All operations automatically traced
    result = rag_chain.invoke(query)
```

### 2. Manual Tracing

```python
from langchain.callbacks import LangChainTracer

tracer = LangChainTracer(
    project_name="rag-demo",
    example_id="example-123"  # Optional: link to dataset
)

result = chain.invoke(query, config={"callbacks": [tracer]})
```

### 3. Trace Metadata

```python
from langchain_core.tracers.context import tracing_v2_enabled

with tracing_v2_enabled(
    project_name="rag-demo",
    metadata={
        "user_id": "user-123",
        "session_id": "session-456",
        "environment": "production"
    }
):
    result = chain.invoke(query)
```

---

## Metrics Collection

### 1. Core RAG Metrics

**Collected automatically:**
- **Latency:** Total pipeline time (ms)
- **Token usage:** Input + output tokens
- **Steps:** Number of LLM calls
- **Errors:** Failed operations

**Example trace data:**
```json
{
  "run_id": "abc-123",
  "name": "RAGChain",
  "latency_ms": 1250,
  "total_tokens": 850,
  "prompt_tokens": 600,
  "completion_tokens": 250,
  "steps": [
    {"name": "embedder", "latency_ms": 50},
    {"name": "retriever", "latency_ms": 200},
    {"name": "generator", "latency_ms": 1000}
  ]
}
```

### 2. Custom Metrics (Faithfulness, Relevance)

```python
from langsmith import Client

client = Client()

# After getting RAG result
client.create_feedback(
    run_id=run_id,
    key="faithfulness",
    score=0.85,  # 0-1 scale
    comment="Answer is mostly accurate to context"
)

client.create_feedback(
    run_id=run_id,
    key="relevance",
    score=0.92,  # 0-1 scale
    comment="Retrieved docs are highly relevant"
)
```

**See:** `rag-accuracy-SKILL.md` for metric calculations

---

## Trace Validation

### 1. Query Trace

```python
from langsmith import Client

client = Client()

# Get specific run
run = client.read_run(run_id="abc-123")

# Validate trace
assert run.latency_ms < 2000, "Query too slow"
assert run.error is None, "Query failed"
assert len(run.child_runs) >= 3, "Missing pipeline steps"
```

### 2. Batch Validation

```python
from langsmith import Client
from datetime import datetime, timedelta

client = Client()

# Get recent runs
runs = client.list_runs(
    project_name="rag-demo",
    start_time=datetime.now() - timedelta(hours=1)
)

# Aggregate metrics
avg_latency = sum(r.latency_ms for r in runs) / len(runs)
error_rate = sum(1 for r in runs if r.error) / len(runs)

print(f"Avg latency: {avg_latency}ms")
print(f"Error rate: {error_rate:.2%}")
```

---

## Run Comparisons (A/B Testing)

### 1. Compare Prompt Variants

```python
from langsmith import Client

client = Client()

# Run A: Original prompt
with tracing_v2_enabled(
    project_name="rag-demo",
    metadata={"variant": "prompt-v1"}
):
    result_a = chain_v1.invoke(query)

# Run B: New prompt
with tracing_v2_enabled(
    project_name="rag-demo",
    metadata={"variant": "prompt-v2"}
):
    result_b = chain_v2.invoke(query)

# Compare in LangSmith UI
# Filter by metadata.variant to see performance difference
```

### 2. Automated Comparison

```python
from langsmith import Client

client = Client()

# Get runs for each variant
runs_v1 = client.list_runs(
    project_name="rag-demo",
    filter='metadata.variant == "prompt-v1"'
)

runs_v2 = client.list_runs(
    project_name="rag-demo",
    filter='metadata.variant == "prompt-v2"'
)

# Compare metrics
v1_latency = sum(r.latency_ms for r in runs_v1) / len(runs_v1)
v2_latency = sum(r.latency_ms for r in runs_v2) / len(runs_v2)

print(f"V1 avg latency: {v1_latency}ms")
print(f"V2 avg latency: {v2_latency}ms")
print(f"Improvement: {((v1_latency - v2_latency) / v1_latency) * 100:.1f}%")
```

---

## Dataset Evaluation

### 1. Create Dataset

```python
from langsmith import Client

client = Client()

# Create evaluation dataset
dataset = client.create_dataset("rag-eval-v1")

# Add examples
client.create_examples(
    dataset_id=dataset.id,
    inputs=[
        {"query": "What is RAG?"},
        {"query": "How does vector search work?"}
    ],
    outputs=[
        {"expected_answer": "RAG is Retrieval Augmented Generation..."},
        {"expected_answer": "Vector search uses embeddings..."}
    ]
)
```

### 2. Run Evaluation

```python
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

# Define evaluator
def faithfulness_evaluator(run, example):
    # Calculate faithfulness score
    score = calculate_faithfulness(
        run.outputs["answer"],
        run.outputs["source_documents"]
    )
    return {"score": score}

# Run evaluation
results = evaluate(
    lambda inputs: rag_chain.invoke(inputs["query"]),
    data="rag-eval-v1",
    evaluators=[faithfulness_evaluator],
    project_name="rag-eval-results"
)

print(f"Avg faithfulness: {results['aggregate']['faithfulness']['mean']}")
```

---

## Error Detection

### 1. Failed Retrievals

```python
from langsmith import Client

client = Client()

# Find runs with no retrieved documents
failed_runs = client.list_runs(
    project_name="rag-demo",
    filter='outputs.source_documents.length == 0'
)

for run in failed_runs:
    print(f"Query: {run.inputs['query']}")
    print(f"Reason: No relevant documents found")
```

### 2. High Latency Queries

```python
from langsmith import Client

client = Client()

# Find slow queries (>2s)
slow_runs = client.list_runs(
    project_name="rag-demo",
    filter='latency_ms > 2000'
)

for run in slow_runs:
    print(f"Query: {run.inputs['query']}")
    print(f"Latency: {run.latency_ms}ms")

    # Identify bottleneck
    for child in run.child_runs:
        if child.latency_ms > 1000:
            print(f"  Bottleneck: {child.name} ({child.latency_ms}ms)")
```

---

## Best Practices

### 1. Always Trace Production

```python
# Enable tracing in production
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "rag-production"

# Sample rate for high-volume apps (optional)
os.environ["LANGCHAIN_TRACING_SAMPLING_RATE"] = "0.1"  # 10% of requests
```

### 2. Use Meaningful Project Names

```python
# Bad: Generic names
project_name = "test"

# Good: Environment + purpose
project_name = f"rag-{environment}-{feature}"  # "rag-prod-hybrid-search"
```

### 3. Add Context with Metadata

```python
with tracing_v2_enabled(
    project_name="rag-demo",
    metadata={
        "user_tier": "premium",
        "retriever_type": "hybrid",
        "llm_model": "claude-3-sonnet",
        "chunk_size": 512
    }
):
    result = chain.invoke(query)
```

### 4. Monitor Key Metrics

**Daily checks:**
- [ ] Avg latency < 2000ms
- [ ] Error rate < 1%
- [ ] Faithfulness score > 0.7
- [ ] Relevance score > 0.7

**Weekly checks:**
- [ ] Compare A/B test variants
- [ ] Review slow queries
- [ ] Identify common failure patterns

---

## Integration with Other Skills

### Workflow

```
User Query
   ↓
LangSmith Tracing (THIS SKILL)
   ↓
RAG Pipeline Execution
   ↓
Trace Collection (automatic)
   ↓
Metrics Calculation (rag-accuracy-SKILL.md)
   ↓
Feedback to LangSmith
   ↓
Dashboard Analysis
```

### Related Files

| Skill | Purpose |
|-------|---------|
| `rag-accuracy-SKILL.md` | Calculate faithfulness, relevance scores |
| `e2e-testing-SKILL.md` | E2E tests with LangSmith assertions |
| `llm-integration-SKILL.md` | LLM provider switching (affects traces) |

---

## Troubleshooting

### Issue: Traces not appearing

**Check:**
1. `LANGCHAIN_TRACING_V2=true` set?
2. `LANGSMITH_API_KEY` valid?
3. Project name correct?

**Solution:**
```python
import os
print(os.environ.get("LANGCHAIN_TRACING_V2"))  # Should be "true"
print(os.environ.get("LANGSMITH_API_KEY"))     # Should be set
```

### Issue: High latency in traces

**Check:**
1. Which step is slow? (embedder, retriever, generator)
2. Network latency to LangSmith?

**Solution:**
```python
# Disable tracing for testing
os.environ["LANGCHAIN_TRACING_V2"] = "false"
# If latency drops → LangSmith network issue
# If latency same → RAG pipeline issue
```

---

## Example: Complete RAG with LangSmith

```python
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.tracers.context import tracing_v2_enabled
from langsmith import Client

# Setup
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "rag-demo"

# Build RAG chain
embeddings = OpenAIEmbeddings()
vector_store = FAISS.load_local("./index", embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

llm = ChatOpenAI(model="gpt-4", temperature=0)
chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# Query with tracing
query = "What is retrieval augmented generation?"

with tracing_v2_enabled(
    project_name="rag-demo",
    metadata={"environment": "demo"}
) as cb:
    result = chain.invoke(query)
    run_id = cb.run_id

# Add feedback
client = Client()
client.create_feedback(
    run_id=run_id,
    key="faithfulness",
    score=0.9,
    comment="Accurate answer"
)

print(f"Answer: {result['result']}")
print(f"Trace: https://smith.langchain.com/public/{run_id}")
```

---

**Last Updated:** 2025-12-04
**Version:** 1.0
**Priority:** CRITICAL (Auto-loads for all RAG queries)
