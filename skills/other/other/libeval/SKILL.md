---
name: libeval
description: >
  libeval - RAG evaluation system. Evaluator orchestrates quality assessment
  using LLM-as-judge patterns. CriteriaEvaluator scores responses against
  rubrics. RecallEvaluator measures retrieval performance. TraceEvaluator
  analyzes execution traces. EvalStore persists results. Use for automated
  quality testing, RAG pipeline evaluation, and agent performance testing
---

# libeval Skill

## When to Use

- Evaluating RAG agent response quality
- Measuring retrieval recall and precision
- Running automated quality assessments
- Benchmarking agent performance over time

## Key Concepts

**Evaluator**: Main orchestrator that runs test cases through the agent and
collects metrics.

**CriteriaEvaluator**: Uses LLM-as-judge to score responses against defined
criteria and rubrics.

**RecallEvaluator**: Measures how well the retrieval system returns relevant
documents.

**TraceEvaluator**: Analyzes execution traces for performance and correctness.

## Usage Patterns

### Pattern 1: Run evaluation suite

```javascript
import { Evaluator } from "@copilot-ld/libeval";

const evaluator = new Evaluator(config);
const results = await evaluator.run(testCases);
console.log(results.summary);
```

### Pattern 2: Criteria-based evaluation

```javascript
import { CriteriaEvaluator } from "@copilot-ld/libeval";

const criteria = new CriteriaEvaluator(llmClient);
const score = await criteria.evaluate(response, rubric);
```

## Integration

Configured via config/eval.yml. Run via `make eval`. Uses libllm for
LLM-as-judge.
