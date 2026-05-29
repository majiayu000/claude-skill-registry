---
name: repo-rag
description: Perform high-recall codebase retrieval using semantic search and symbol indexing. Use when you need to find specific code, understand project structure, or verify architectural patterns before editing.
context:fork: true
allowed-tools: search, symbols, codebase_search, read, grep
version: 2.0
best_practices:
  - Use clear, specific queries (avoid vague terms)
  - Provide context about what you're looking for
  - Review multiple results to understand patterns
  - Use follow-up queries to refine results
  - Verify file paths before proposing edits
error_handling: graceful
streaming: supported
---

<identity>
Repo RAG (Retrieval Augmented Generation) - Provides advanced codebase search capabilities beyond simple grep.
</identity>

<capabilities>
- High-recall codebase retrieval using semantic search
- Symbol indexing for finding classes, functions, and types
- Understanding project structure
- Verifying architectural patterns before editing
</capabilities>

<instructions>
<execution_process>
1. **Symbol Search First**: Use `symbols` to find classes, functions, and types. This is more accurate than text search for code structures.
2. **Semantic Search**: Use `search` for concepts, comments, or broader patterns.
3. **Verification**: Always verify the file path and context returned before proposing edits.
</execution_process>

<usage_patterns>

- **Architecture Review**: Run symbol searches on key interfaces to understand the dependency graph.
- **Plan Mode**: Use this skill to populate the "Context" section of a Plan Mode artifact.
- **Refactoring**: Identify all usages of a symbol before renaming or modifying it.
  </usage_patterns>
  </instructions>

<examples>
<code_example>
**Symbol Search**:

```
symbols "UserAuthentication"
```

**Semantic Search**:

```
search "authentication middleware logic"
```

</code_example>
</examples>

## RAG Evaluation

### Overview

Systematic evaluation of RAG quality using retrieval and end-to-end metrics. Based on Claude Cookbooks patterns.

### Evaluation Metrics

**Retrieval Metrics** (from `.claude/evaluation/retrieval_metrics.py`):

- **Precision**: Proportion of retrieved chunks that are actually relevant
  - Formula: `Precision = True Positives / Total Retrieved`
  - High precision (0.8-1.0): System retrieves mostly relevant items
- **Recall**: Completeness of retrieval - how many relevant items were found
  - Formula: `Recall = True Positives / Total Correct`
  - High recall (0.8-1.0): System finds most relevant items
- **F1 Score**: Harmonic mean of precision and recall
  - Formula: `F1 = 2 × (Precision × Recall) / (Precision + Recall)`
  - Balanced measure when both precision and recall matter
- **MRR (Mean Reciprocal Rank)**: Measures ranking quality
  - Formula: `MRR = 1 / rank of first correct item`
  - High MRR (0.8-1.0): Correct items ranked first

**End-to-End Metrics** (from `.claude/evaluation/end_to_end_eval.py`):

- **Accuracy (LLM-as-Judge)**: Overall correctness using Claude evaluation
  - Compares generated answer to correct answer
  - Focuses on substance and meaning, not exact wording
  - Checks for completeness and absence of contradictions

### Evaluation Process

1. **Create Evaluation Dataset**:

   ```json
   {
     "query": "How is user authentication implemented?",
     "correct_chunks": ["src/auth/middleware.ts", "src/auth/types.ts"],
     "correct_answer": "User authentication uses JWT tokens...",
     "category": "authentication"
   }
   ```

2. **Run Retrieval Evaluation**:

   ```bash
   # Using Promptfoo
   npx promptfoo@latest eval -c .claude/evaluation/promptfoo_configs/rag_config.yaml

   # Or using Python directly
   from .claude.evaluation.retrieval_metrics import evaluate_retrieval
   metrics = evaluate_retrieval(retrieved_chunks, correct_chunks)
   print(f"Precision: {metrics['precision']}, Recall: {metrics['recall']}, F1: {metrics['f1']}, MRR: {metrics['mrr']}")
   ```

3. **Run End-to-End Evaluation**:

   ```bash
   # Using Promptfoo
   npx promptfoo@latest eval -c .claude/evaluation/promptfoo_configs/rag_config.yaml

   # Or using Python directly
   from .claude.evaluation.end_to_end_eval import evaluate_end_to_end
   result = evaluate_end_to_end(query, generated_answer, correct_answer)
   print(f"Correct: {result['is_correct']}, Explanation: {result['explanation']}")
   ```

### Expected Performance

Based on Claude Cookbooks results:

- **Basic RAG**: Precision 0.43, Recall 0.66, F1 0.52, MRR 0.74, Accuracy 71%
- **With Re-ranking**: Precision 0.44, Recall 0.69, F1 0.54, MRR 0.87, Accuracy 81%

### Best Practices

1. **Separate Evaluation**: Evaluate retrieval and end-to-end separately
2. **Create Comprehensive Datasets**: Cover common and edge cases
3. **Evaluate Regularly**: Run evaluations after codebase changes
4. **Track Metrics Over Time**: Monitor improvements
5. **Use Both Metrics**: Precision/Recall for retrieval, Accuracy for end-to-end

### References

- [RAG Patterns Guide](../docs/RAG_PATTERNS.md) - Implementation patterns
- [Retrieval Metrics](../evaluation/retrieval_metrics.py) - Metric calculations
- [End-to-End Evaluation](../evaluation/end_to_end_eval.py) - LLM-as-judge
- [Evaluation Guide](../docs/EVALUATION_GUIDE.md) - Comprehensive evaluation guide
