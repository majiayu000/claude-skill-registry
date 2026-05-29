---
name: error-recovery
version: 1.0
triggers: ["error", "retry", "fallback"]
---

# Error Recovery SKILL

## Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def query_with_retry(query):
    return rag_chain.invoke(query)
```

## Fallback Chain

```python
try:
    result = primary_retriever.get_relevant_documents(query)
except Exception:
    result = fallback_retriever.get_relevant_documents(query)
```
