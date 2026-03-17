---
name: similar-code
description: Find semantically similar code across the codebase using vector search (armyknife searchx). Use when looking for similar implementations, duplicate code, or existing patterns. Requires symbols.db.
keywords: similar-code, 類似コード, 似た実装, 重複コード
---

* Always use actual code as query input, not natural language descriptions
* Prerequisite: `symbols.db` must exist at project root (built via `armyknife searchx index`)

## Workflow

1. User provides code as argument (e.g., `/similar-code <pasted code>`)
2. Run the search command:

```bash
armyknife searchx query '<code>' --limit 10 --database symbols.db
```

3. Present results as a table (symbol, kind, file, line, similarity)
4. Read top matches to show code context

## Interpreting Results

| Similarity | Meaning |
|------------|---------|
| 0.8+ | Very similar (likely same pattern or implementation) |
| 0.6-0.8 | Related (similar structure or purpose) |
| <0.6 | Weak match |

## Limitations

| Input Type | Result Quality |
|------------|----------------|
| Actual code | Good (designed for code-to-code similarity) |
| Natural language | Poor (embedding model is code-focused) |

Code is embedded using `embeddinggemma:300m` (768-dim) via Ollama.
