---
name: prompt-engineering
version: 1.0
triggers: ["prompt", "template", "context injection"]
---

# Prompt Engineering SKILL

## RAG Prompt Template

```python
template = """
Use the following context to answer the question.
If you don't know, say "I don't know based on the provided context."

Context:
{context}

Question: {question}

Answer:
"""
```

## Few-Shot Template

```python
template = """
Context: {context}

Examples:
Q: What is X?
A: X is...

Q: {question}
A:
"""
```
