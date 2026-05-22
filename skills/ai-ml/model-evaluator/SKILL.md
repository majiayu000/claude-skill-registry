---
name: Model Evaluator
slug: model-evaluator
description: Evaluate and compare ML model performance with rigorous testing methodologies
category: ai-ml
complexity: advanced
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "evaluate model"
  - "compare models"
  - "model performance"
  - "benchmark ML"
  - "model metrics"
tags:
  - evaluation
  - benchmarking
  - metrics
  - machine-learning
  - testing
---

# Model Evaluator

The Model Evaluator skill helps you rigorously assess and compare machine learning model performance across multiple dimensions. It guides you through selecting appropriate metrics, designing evaluation protocols, avoiding common statistical pitfalls, and making data-driven decisions about model selection.

Proper model evaluation goes beyond accuracy scores. This skill covers evaluation across the full spectrum: predictive performance, computational efficiency, robustness, fairness, calibration, and production readiness. It helps you answer not just "which model is best?" but "which model is best for my specific use case and constraints?"

Whether you are comparing LLMs, classifiers, or custom models, this skill ensures your evaluation methodology is sound and your conclusions are reliable.

## Core Workflows

### Workflow 1: Design Evaluation Protocol
1. **Define** evaluation objectives:
   - Primary goal (accuracy, speed, cost, etc.)
   - Secondary constraints
   - Failure modes to test
   - Real-world conditions to simulate
2. **Select** appropriate metrics:
   | Task Type | Primary Metrics | Secondary Metrics |
   |-----------|-----------------|-------------------|
   | Classification | Accuracy, F1, AUC-ROC | Precision, Recall, Confusion Matrix |
   | Regression | RMSE, MAE, R-squared | Residual analysis, prediction intervals |
   | Ranking | NDCG, MRR, MAP | Precision@k, Recall@k |
   | Generation | BLEU, ROUGE, BERTScore | Human eval, Faithfulness |
   | LLM | Task-specific accuracy | Latency, cost, consistency |
3. **Design** test sets:
   - Held-out test data
   - Edge case collections
   - Adversarial examples
   - Distribution shift tests
4. **Plan** statistical methodology:
   - Sample sizes for significance
   - Confidence intervals
   - Multiple comparison corrections

### Workflow 2: Execute Comparative Evaluation
1. **Prepare** evaluation infrastructure:
   ```python
   class ModelEvaluator:
       def __init__(self, test_data, metrics):
           self.test_data = test_data
           self.metrics = metrics
           self.results = {}

       def evaluate(self, model, model_name):
           predictions = model.predict(self.test_data.inputs)
           scores = {}
           for metric in self.metrics:
               scores[metric.name] = metric.compute(
                   predictions,
                   self.test_data.labels
               )
           self.results[model_name] = scores
           return scores

       def compare(self):
           return statistical_comparison(self.results)
   ```
2. **Run** evaluations consistently across models
3. **Compute** confidence intervals
4. **Test** for statistical significance
5. **Generate** comparison report

### Workflow 3: LLM-Specific Evaluation
1. **Define** evaluation dimensions:
   - Task accuracy (factual, reasoning, coding)
   - Response quality (coherence, relevance, style)
   - Safety and alignment
   - Efficiency (tokens, latency, cost)
2. **Create** evaluation datasets:
   - Representative prompts
   - Ground truth answers (where applicable)
   - Human preference data
3. **Implement** LLM evaluation:
   - Automated metrics (exact match, semantic similarity)
   - LLM-as-judge evaluations
   - Human evaluation protocols
4. **Analyze** results across dimensions
5. **Make** recommendations with tradeoffs

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Design evaluation | "How should I evaluate [model type]" |
| Choose metrics | "What metrics for [task type]" |
| Compare models | "Compare these models: [list]" |
| LLM evaluation | "Evaluate LLM performance" |
| Statistical testing | "Is this difference significant" |
| Bias evaluation | "Check model for bias" |

## Best Practices

- **Use Multiple Metrics**: No single metric tells the whole story
  - Include both aggregate and granular metrics
  - Report confidence intervals, not just point estimates
  - Show performance across subgroups

- **Test on Realistic Data**: Evaluation data should match production
  - Same distribution as real inputs
  - Include edge cases and hard examples
  - Test on data the model hasn't seen

- **Account for Variance**: Models and data have randomness
  - Run multiple seeds for training-based evaluations
  - Bootstrap confidence intervals
  - Use proper statistical tests for comparison

- **Consider All Costs**: Performance isn't just accuracy
  - Inference latency and throughput
  - Memory and compute requirements
  - API costs for hosted models
  - Maintenance and update burden

- **Test Robustness**: How does the model handle adversity?
  - Input perturbations and noise
  - Distribution shift
  - Adversarial examples
  - Missing or malformed inputs

- **Evaluate Fairly**: Ensure fair comparison across models
  - Same test data for all models
  - Consistent preprocessing
  - Equivalent hyperparameter tuning effort
  - Document any advantages/disadvantages

## Advanced Techniques

### Multi-Dimensional Evaluation
Score models across multiple axes:
```python
def multi_dim_evaluate(model, test_data):
    return {
        "accuracy": compute_accuracy(model, test_data),
        "latency_p50": measure_latency(model, test_data, percentile=50),
        "latency_p99": measure_latency(model, test_data, percentile=99),
        "memory_mb": measure_memory(model),
        "cost_per_1k": compute_cost(model, n=1000),
        "robustness": adversarial_accuracy(model, test_data),
        "fairness": demographic_parity(model, test_data)
    }
```

### LLM-as-Judge Protocol
Use LLMs to evaluate LLM outputs:
```
Prompt template:
"Rate the following response on a scale of 1-5 for:
- Accuracy: Is the information correct?
- Helpfulness: Does it address the user's need?
- Clarity: Is it easy to understand?

Question: {question}
Response: {response}
Ground truth (if available): {ground_truth}

Provide scores and brief justification."
```

### A/B Testing Framework
For production evaluation:
```python
class ABTest:
    def __init__(self, model_a, model_b, traffic_split=0.5):
        self.models = {"A": model_a, "B": model_b}
        self.split = traffic_split
        self.results = {"A": [], "B": []}

    def serve(self, request):
        variant = "A" if random.random() < self.split else "B"
        response = self.models[variant].predict(request)
        return response, variant

    def record_outcome(self, variant, success):
        self.results[variant].append(success)

    def compute_significance(self):
        return statistical_test(self.results["A"], self.results["B"])
```

### Calibration Analysis
Ensure predicted probabilities are meaningful:
```
- Expected Calibration Error (ECE)
- Reliability diagrams
- Brier score decomposition
- Temperature scaling for recalibration
```

## Common Pitfalls to Avoid

- Overfitting to the test set through repeated evaluation
- Ignoring statistical significance in model comparisons
- Using inappropriate metrics for the task (accuracy for imbalanced classes)
- Evaluating on data too similar to training data
- Ignoring computational costs in model selection
- Not testing robustness to distribution shift
- Conflating correlation with causation in A/B tests
- Failing to account for multiple comparisons in statistical tests
