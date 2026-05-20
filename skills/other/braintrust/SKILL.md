---
name: braintrust
description: >-
  You are an expert in Braintrust, the evaluation and observability platform
  for AI applications. You help developers run systematic evaluations, compare
  model versions, track experiments, log production traces, and measure
  quality metrics — with a focus on making AI development as rigorous as
  traditional software testing.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: AI & Machine Learning
  tags:
    - evaluation
    - llm
    - testing
    - observability
    - experiments
    - logging
---

# Braintrust — AI Evaluation and Observability

You are an expert in Braintrust, the evaluation and observability platform for AI applications. You help developers run systematic evaluations, compare model versions, track experiments, log production traces, and measure quality metrics — with a focus on making AI development as rigorous as traditional software testing.

## Core Capabilities

```typescript
import { Eval, init } from "braintrust";

init({ apiKey: process.env.BRAINTRUST_API_KEY });

// Run evaluation
await Eval("support-chatbot", {
  data: () => [
    { input: "How do I reset my password?", expected: "Go to Settings > Security > Reset Password" },
    { input: "What's the pricing?", expected: "Plans start at $29/month" },
    { input: "I need a refund", expected: "Contact support at help@example.com" },
  ],
  task: async (input) => {
    const response = await callChatbot(input);
    return response.text;
  },
  scores: [
    // Built-in scorers
    Factuality,                            // Does output match expected facts?
    ClosedQA,                              // Is the answer correct given context?
    // Custom scorer
    (output, expected) => {
      const containsKey = expected.toLowerCase().split(" ")
        .some(word => output.toLowerCase().includes(word));
      return { name: "keyword_match", score: containsKey ? 1 : 0 };
    },
  ],
});
// Results visible in Braintrust dashboard with diffs, regressions, improvements
```

```python
# Python
from braintrust import Eval

Eval(
    "rag-pipeline",
    data=lambda: [{"input": q, "expected": a} for q, a in test_pairs],
    task=lambda input: rag_pipeline.query(input),
    scores=[Factuality, Relevance],
)
```

## Installation

```bash
npm install braintrust autoevals
# or
pip install braintrust autoevals
```

## Best Practices

1. **Eval-driven development** — Write evals first, then iterate on prompts/models; measure before optimizing
2. **Built-in scorers** — Use Factuality, ClosedQA, Relevance from `autoevals`; LLM-based quality scoring
3. **Custom scorers** — Add domain-specific metrics; combine with built-in for comprehensive evaluation
4. **Experiments** — Each eval run is an experiment; compare side-by-side in dashboard
5. **Production logging** — Use `braintrust.traced()` for production observability; same dashboard as evals
6. **CI integration** — Run evals in CI; fail builds on quality regressions
7. **Dataset management** — Store test datasets in Braintrust; version and share across team
8. **A/B comparison** — Compare two model versions on the same dataset; statistical significance reported
