---
name: rag-accuracy
version: 1.0
last_updated: 2025-12-04
description: RAG evaluation metrics - faithfulness, relevance, answer quality measurement
license: MIT
priority: critical
triggers:
  - "accuracy", "evaluation", "faithfulness", "relevance", "metrics"
  - Evaluation tasks
  - Quality assessment
dependencies:
  - langsmith-testing-SKILL.md
compatibility:
  - ragas: ">=0.1.0"
  - langchain: ">=0.1.0"
changelog:
  - version: 1.0
    date: 2025-12-04
    changes:
      - Initial release for RAG evaluation
      - RAGAS framework integration
      - Custom metric implementations
---

# 📈 RAG Accuracy SKILL

## Purpose

Measure RAG answer quality through three core metrics: **Faithfulness** (accuracy to context), **Relevance** (retrieval quality), and **Answer Quality** (overall usefulness).

---

## Auto-Trigger Conditions

**Activate when:**
- User mentions: "accuracy", "evaluation", "faithfulness", "relevance", "metrics"
- Evaluation tasks
- Quality assessment
- A/B testing RAG variants

---

## Core Metrics (3 Metrics)

### 1. Faithfulness (0-1 scale)

**Definition:** How accurate is the generated answer to the retrieved context?

**Why Critical:** Detects hallucinations (LLM making up facts not in context)

**Calculation:**
```python
from ragas import faithfulness
from ragas.metrics import Faithfulness

metric = Faithfulness()

score = metric.score({
    "question": "What is RAG?",
    "answer": "RAG is Retrieval Augmented Generation, a technique...",
    "contexts": ["RAG combines retrieval with generation..."]
})

print(f"Faithfulness: {score}")  # 0.0-1.0
```

**Interpretation:**
- **0.9-1.0:** Excellent (no hallucinations)
- **0.7-0.9:** Good (minor inaccuracies)
- **0.5-0.7:** Fair (some hallucinations)
- **< 0.5:** Bad (significant hallucinations)

**Example:**
```python
# Good faithfulness (0.95)
question = "What is the capital of France?"
answer = "The capital of France is Paris."
contexts = ["Paris is the capital and largest city of France."]

# Bad faithfulness (0.3)
question = "What is the capital of France?"
answer = "The capital of France is London and it has 10 million people."
contexts = ["Paris is the capital and largest city of France."]
# Hallucination: London (wrong), 10 million (not in context)
```

---

### 2. Context Relevance (0-1 scale)

**Definition:** How relevant are the retrieved documents to the question?

**Why Critical:** Bad retrieval = bad answers (even perfect LLM can't fix)

**Calculation:**
```python
from ragas.metrics import ContextRelevance

metric = ContextRelevance()

score = metric.score({
    "question": "How does vector search work?",
    "contexts": [
        "Vector search uses embeddings to find similar documents.",
        "Embeddings are numerical representations of text."
    ]
})

print(f"Context Relevance: {score}")  # 0.0-1.0
```

**Interpretation:**
- **0.9-1.0:** Excellent (all docs highly relevant)
- **0.7-0.9:** Good (most docs relevant)
- **0.5-0.7:** Fair (some docs off-topic)
- **< 0.5:** Bad (retrieval failed)

**Example:**
```python
# Good relevance (0.92)
question = "How do I make a cake?"
contexts = [
    "Mix flour, eggs, and sugar. Bake at 350°F for 30 minutes.",
    "Cake baking requires preheating the oven first."
]

# Bad relevance (0.2)
question = "How do I make a cake?"
contexts = [
    "The history of bread dates back to ancient Egypt.",
    "Different types of pasta include spaghetti and penne."
]
```

---

### 3. Answer Relevance (0-1 scale)

**Definition:** How well does the answer address the original question?

**Why Critical:** Ensures answer is on-topic (not tangential)

**Calculation:**
```python
from ragas.metrics import AnswerRelevance

metric = AnswerRelevance()

score = metric.score({
    "question": "What is machine learning?",
    "answer": "Machine learning is a subset of AI that enables systems to learn from data."
})

print(f"Answer Relevance: {score}")  # 0.0-1.0
```

**Interpretation:**
- **0.9-1.0:** Excellent (directly answers question)
- **0.7-0.9:** Good (mostly on-topic)
- **0.5-0.7:** Fair (some tangential info)
- **< 0.5:** Bad (doesn't answer question)

---

## RAGAS Framework Integration

### 1. Installation

```bash
pip install ragas
```

### 2. Batch Evaluation

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevance,
    context_relevance,
    context_recall,
    context_precision
)

# Prepare dataset
dataset = {
    "question": [
        "What is RAG?",
        "How does retrieval work?"
    ],
    "answer": [
        "RAG is Retrieval Augmented Generation...",
        "Retrieval uses vector embeddings..."
    ],
    "contexts": [
        ["RAG combines retrieval with generation..."],
        ["Vector embeddings enable semantic search..."]
    ],
    "ground_truths": [
        ["RAG is a technique that..."],
        ["Retrieval finds relevant documents..."]
    ]
}

# Evaluate
results = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevance,
        context_relevance,
        context_recall,
        context_precision
    ]
)

print(results)
```

**Output:**
```
{
    'faithfulness': 0.85,
    'answer_relevance': 0.92,
    'context_relevance': 0.88,
    'context_recall': 0.90,
    'context_precision': 0.87
}
```

---

## Custom Metric Implementations

### 1. Faithfulness (Manual)

```python
from langchain_openai import ChatOpenAI

def calculate_faithfulness(answer: str, contexts: list[str]) -> float:
    """
    Check if answer claims are supported by context.
    """
    llm = ChatOpenAI(model="gpt-4", temperature=0)

    prompt = f"""
    Given the following context and answer, rate how faithful the answer is to the context.
    Return a score from 0.0 to 1.0.

    Context:
    {' '.join(contexts)}

    Answer:
    {answer}

    Faithfulness score (0.0-1.0):
    """

    response = llm.invoke(prompt)
    score = float(response.content.strip())

    return score
```

### 2. Relevance (Manual)

```python
from langchain_openai import ChatOpenAI

def calculate_relevance(question: str, contexts: list[str]) -> float:
    """
    Check if retrieved contexts are relevant to question.
    """
    llm = ChatOpenAI(model="gpt-4", temperature=0)

    prompt = f"""
    Given the following question and retrieved documents, rate how relevant the documents are.
    Return a score from 0.0 to 1.0.

    Question:
    {question}

    Retrieved Documents:
    {' | '.join(contexts)}

    Relevance score (0.0-1.0):
    """

    response = llm.invoke(prompt)
    score = float(response.content.strip())

    return score
```

---

## LangSmith Integration

### 1. Add Metrics as Feedback

```python
from langsmith import Client
from ragas.metrics import Faithfulness, ContextRelevance

client = Client()
faithfulness_metric = Faithfulness()
relevance_metric = ContextRelevance()

# After RAG query
result = rag_chain.invoke(query)

# Calculate metrics
faithfulness_score = faithfulness_metric.score({
    "question": query,
    "answer": result["answer"],
    "contexts": [doc.page_content for doc in result["source_documents"]]
})

relevance_score = relevance_metric.score({
    "question": query,
    "contexts": [doc.page_content for doc in result["source_documents"]]
})

# Send to LangSmith
client.create_feedback(
    run_id=run_id,
    key="faithfulness",
    score=faithfulness_score
)

client.create_feedback(
    run_id=run_id,
    key="context_relevance",
    score=relevance_score
)
```

**See:** `langsmith-testing-SKILL.md` for trace collection

---

## Quality Thresholds

### Production Standards

| Metric | Minimum | Good | Excellent |
|--------|---------|------|-----------|
| Faithfulness | 0.7 | 0.85 | 0.95 |
| Context Relevance | 0.7 | 0.85 | 0.95 |
| Answer Relevance | 0.7 | 0.85 | 0.95 |
| Latency (ms) | < 2000 | < 1000 | < 500 |

**Action on failure:**
- **Faithfulness < 0.7:** Check prompt engineering, reduce temperature
- **Context Relevance < 0.7:** Improve retrieval (hybrid search, reranking)
- **Answer Relevance < 0.7:** Refine prompt, add few-shot examples

---

## A/B Testing with Metrics

### Compare Retrieval Strategies

```python
from ragas import evaluate

# Strategy A: Semantic only
results_a = evaluate(
    dataset_a,
    metrics=[faithfulness, context_relevance]
)

# Strategy B: Hybrid (BM25 + Semantic)
results_b = evaluate(
    dataset_b,
    metrics=[faithfulness, context_relevance]
)

# Compare
print(f"Semantic only: {results_a}")
print(f"Hybrid search: {results_b}")

# Decision: Choose strategy with higher context_relevance
```

### Compare Prompt Templates

```python
# Template A: Simple
prompt_a = "Answer: {question}\nContext: {context}"

# Template B: Few-shot
prompt_b = """
Examples:
Q: What is X?
A: X is...

Now answer:
Q: {question}
Context: {context}
"""

# Evaluate both
results_a = evaluate(dataset_a, metrics=[faithfulness, answer_relevance])
results_b = evaluate(dataset_b, metrics=[faithfulness, answer_relevance])

# Decision: Choose template with higher faithfulness
```

---

## Automated Quality Monitoring

### Daily Checks

```python
from langsmith import Client
from datetime import datetime, timedelta

client = Client()

# Get today's runs
runs = client.list_runs(
    project_name="rag-production",
    start_time=datetime.now() - timedelta(days=1)
)

# Calculate avg metrics
faithfulness_scores = []
relevance_scores = []

for run in runs:
    feedbacks = client.list_feedback(run_id=run.id)
    for fb in feedbacks:
        if fb.key == "faithfulness":
            faithfulness_scores.append(fb.score)
        elif fb.key == "context_relevance":
            relevance_scores.append(fb.score)

avg_faithfulness = sum(faithfulness_scores) / len(faithfulness_scores)
avg_relevance = sum(relevance_scores) / len(relevance_scores)

print(f"Avg Faithfulness: {avg_faithfulness:.2f}")
print(f"Avg Relevance: {avg_relevance:.2f}")

# Alert if below threshold
if avg_faithfulness < 0.7:
    print("WARNING: Faithfulness below threshold!")
if avg_relevance < 0.7:
    print("WARNING: Relevance below threshold!")
```

---

## Best Practices

### 1. Evaluate on Representative Dataset

```python
# Bad: Only simple questions
dataset = [
    "What is X?",
    "What is Y?"
]

# Good: Mix of simple, complex, edge cases
dataset = [
    "What is X?",                          # Simple
    "Compare X and Y",                     # Complex
    "What is the capital of Atlantis?",    # No answer in knowledge base
    ""                                     # Empty query
]
```

### 2. Track Metrics Over Time

```python
import pandas as pd
from datetime import datetime

# Log daily metrics
metrics_log = []

def log_metrics(date, faithfulness, relevance):
    metrics_log.append({
        "date": date,
        "faithfulness": faithfulness,
        "relevance": relevance
    })

# Visualize trends
df = pd.DataFrame(metrics_log)
df.plot(x="date", y=["faithfulness", "relevance"])
```

### 3. Use Ground Truth for Validation

```python
# Include expected answers in dataset
dataset = {
    "question": ["What is RAG?"],
    "ground_truths": [["RAG is Retrieval Augmented Generation..."]],
    # ... rest of dataset
}

# Evaluate with context_recall (how much of ground truth is retrieved)
from ragas.metrics import context_recall

results = evaluate(dataset, metrics=[context_recall])
```

---

## Troubleshooting

### Issue: Low faithfulness despite good context

**Cause:** LLM hallucinating or temperature too high

**Solution:**
```python
# Reduce temperature
llm = ChatOpenAI(model="gpt-4", temperature=0)  # 0 = deterministic

# Add "stick to context" instruction
prompt = """
Use ONLY the provided context to answer. Do not use external knowledge.
If the answer is not in the context, say "I don't know based on the provided context."

Context: {context}
Question: {question}
"""
```

### Issue: Low relevance despite good embeddings

**Cause:** Retrieval strategy not optimal

**Solution:**
```python
# Use hybrid search (BM25 + Semantic)
from langchain.retrievers import EnsembleRetriever

retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, semantic_retriever],
    weights=[0.5, 0.5]
)

# Or add reranking
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker

compressor = CrossEncoderReranker()
retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)
```

**See:** `retrieval-patterns-SKILL.md`

---

## Integration with Other Skills

### Workflow

```
RAG Query
   ↓
LangSmith Trace (langsmith-testing-SKILL.md)
   ↓
Get Result
   ↓
Calculate Metrics (THIS SKILL)
   ↓
Send Feedback to LangSmith
   ↓
Monitor Quality Thresholds
```

### Related Files

| Skill | Purpose |
|-------|---------|
| `langsmith-testing-SKILL.md` | Trace collection, feedback API |
| `retrieval-patterns-SKILL.md` | Improve context relevance |
| `prompt-engineering-SKILL.md` | Improve faithfulness |
| `e2e-testing-SKILL.md` | E2E tests with metric assertions |

---

**Last Updated:** 2025-12-04
**Version:** 1.0
**Priority:** CRITICAL (Core RAG quality measurement)
