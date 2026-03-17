---
name: eval-frameworks
description: Evaluation framework patterns for RAG and LLMs, including faithfulness metrics, synthetic dataset generation, and LLM-as-a-judge patterns. Triggers: ragas, deepeval, llm-eval, faithfulness, hallucination-check, synthetic-data.
---

# Evaluation Frameworks

## Overview
Traditional software metrics (accuracy, F1) fail to capture the quality of LLM outputs. Evaluation frameworks like Ragas and DeepEval use "LLM-as-a-judge" to quantify subjective qualities like faithfulness, relevance, and professionalism.

## When to Use
- **RAG Benchmarking**: To verify if answers are supported by retrieved context (Faithfulness).
- **Regression Testing**: Ensuring that a prompt change or model upgrade doesn't break existing behavior.
- **Synthetic Benchmarking**: Creating evaluation sets when manual gold-standard data is unavailable.

## Decision Tree
1. Do you want to check for hallucinations? 
   - YES: Run a Faithfulness metric.
2. Is the retrieved context actually useful for the question? 
   - YES: Run a Retrieval Relevance metric.
3. Do you need to scale evaluation without manual labeling? 
   - YES: Use Synthetic Data Generation.

## Workflows

### 1. Evaluating RAG Faithfulness
1. Capture the `query`, the `retrieved_context`, and the `actual_output` from the system.
2. Run a Faithfulness metric (from Ragas or LlamaIndex) which uses an LLM to verify if the output claims are supported by the context.
3. If the score is low, investigate whether the context was irrelevant or the model hallucinated.

### 2. Unit Testing LLM Outputs (DeepEval)
1. Install `deepeval` and create a test file `test_example.py`.
2. Define an `LLMTestCase` with input, actual_output, and expected_output.
3. Apply a `GEval` metric with a custom `criteria` (e.g., 'professionalism').
4. Run `deepeval test run` to assert that the score meets the defined threshold.

### 3. Automated Question Generation
1. Point the evaluation framework (e.g., LlamaIndex) at a set of source documents.
2. Use the `QuestionGeneration` module to synthetically create test cases (question-context pairs).
3. Run the RAG pipeline against these generated questions to benchmark performance across the entire dataset.

## Non-Obvious Insights
- **LLM-as-a-Judge**: A stronger model (GPT-4o) can effectively grade a smaller/faster model (Llama 3) with human-like accuracy using research-backed metrics like GEval.
- **Separation of Concerns**: Good evaluation splits into 'Response' (was the answer good?) and 'Retrieval' (did we find the right docs?). Fixing one doesn't always fix the other.
- **Synthetic Scaling**: Manual evaluation doesn't scale; using an LLM to generate 1000 edge cases from your data is the only way to reach high production confidence.

## Evidence
- "Faithfulness: Evaluates if the answer is faithful to the retrieved contexts (in other words, whether if there’s hallucination)." - [LlamaIndex](https://docs.llamaindex.ai/en/stable/module_guides/evaluating/)
- "GEval is a research-backed metric... for you to evaluate your LLM output's on any custom metric with human-like accuracy." - [DeepEval](https://docs.confident-ai.com/docs/getting-started)
- "Traditional evaluation metrics don't capture what matters for LLM applications." - [Ragas](https://docs.ragas.io/en/stable/)

## Scripts
- `scripts/eval-frameworks_tool.py`: Script defining a Faithfulness evaluation loop.
- `scripts/eval-frameworks_tool.js`: Node.js simulation for calculating relevance scores.

## Dependencies
- `ragas`
- `deepeval`
- `llama-index`

## References
- [references/README.md](references/README.md)