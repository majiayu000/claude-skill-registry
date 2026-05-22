---
name: ai-evaluation-suite
description: Comprehensive AI/LLM evaluation toolkit for production AI systems. Covers LLM output quality, prompt engineering, RAG evaluation, agent performance, hallucination detection, bias assessment, cost/token optimization, latency metrics, model comparison, and fine-tuning evaluation. Includes BLEU/ROUGE metrics, perplexity, F1 scores, LLM-as-judge patterns, and benchmarks like MMLU and HumanEval.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, WebFetch]
---

# AI Evaluation Suite - Quick Reference

## Purpose

Production AI systems require rigorous evaluation beyond traditional software testing. This skill provides comprehensive evaluation capabilities for LLM quality, RAG systems, agents, hallucination detection, bias assessment, cost optimization, and performance metrics.

## When to Use This Skill

- Evaluating LLM outputs for quality and correctness
- A/B testing prompt variations
- Measuring RAG system retrieval accuracy
- Detecting hallucinations in generated content
- Assessing model bias and fairness
- Optimizing token usage and costs
- Comparing multiple LLM models
- Evaluating fine-tuned models vs base models
- Running standard benchmarks (MMLU, HumanEval, etc.)
- Implementing LLM-as-judge evaluation patterns

## Core Concepts

### Evaluation Pyramid

```
        ┌─────────────┐
        │  Human Eval │  <- Gold standard but expensive
        └──────┬──────┘
               │
        ┌──────┴──────────┐
        │ LLM-as-Judge    │  <- Scalable proxy for human judgment
        └──────┬──────────┘
               │
        ┌──────┴──────────┐
        │ Reference-Based │  <- BLEU, ROUGE, F1 (needs ground truth)
        └──────┬──────────┘
               │
        ┌──────┴──────────┐
        │ Reference-Free  │  <- Perplexity, consistency, coherence
        └─────────────────┘
```

### Key Metric Categories

- **Quality**: Coherence, Relevance, Factuality, Completeness, Conciseness
- **Performance**: Latency, Throughput, Token Usage, Cost, Error Rate
- **Safety**: Hallucination Rate, Bias Scores, Toxicity, PII Leakage
- **Task-Specific**: RAG (Precision/Recall), Agents (Success Rate), Code (Pass@k)

## Documentation Structure

This skill is organized into 6 files:
1. **SKILL.md** (this file) - Quick reference and essential patterns
2. **KNOWLEDGE.md** - Evaluation theory, benchmarks, resources
3. **PATTERNS.md** - 8 evaluation patterns with complete code
4. **GOTCHAS.md** - Common pitfalls, metric limitations, edge cases
5. **EXAMPLES.md** - Complete real-world evaluation scenarios
6. **REFERENCE.md** - Comprehensive metrics reference

## Quick Start: LLM Quality Evaluation

```python
from dataclasses import dataclass
import anthropic
import numpy as np

@dataclass
class QualityMetrics:
    coherence: float
    relevance: float
    factuality: float
    completeness: float
    conciseness: float
    overall_score: float

class LLMQualityEvaluator:
    def __init__(self, model="claude-3-5-sonnet-20241022"):
        self.client = anthropic.Anthropic()
        self.evaluator_model = model

    def evaluate(self, query: str, output: str,
                ground_truth: str = None) -> QualityMetrics:
        """Score output on 5 dimensions using LLM-as-judge"""

        eval_prompt = f"""Evaluate this LLM output (score 0-10 each):
Query: {query}
Output: {output}
{f'Ground Truth: {ground_truth}' if ground_truth else ''}

Provide JSON: {{
  "coherence": X,
  "relevance": X,
  "factuality": X,
  "completeness": X,
  "conciseness": X
}}"""

        response = self.client.messages.create(
            model=self.evaluator_model,
            max_tokens=256,
            messages=[{"role": "user", "content": eval_prompt}]
        )

        import json
        scores = json.loads(response.content[0].text)

        return QualityMetrics(
            coherence=scores["coherence"] / 10.0,
            relevance=scores["relevance"] / 10.0,
            factuality=scores["factuality"] / 10.0,
            completeness=scores["completeness"] / 10.0,
            conciseness=scores["conciseness"] / 10.0,
            overall_score=np.mean(list(scores.values())) / 10.0
        )

# Usage
evaluator = LLMQualityEvaluator()
metrics = evaluator.evaluate(
    query="Explain quantum entanglement",
    output="Quantum entanglement occurs when particles..."
)
print(f"Quality Score: {metrics.overall_score:.2f}")
```

## Quick Start: Hallucination Detection

```python
class HallucinationDetector:
    def __init__(self, model="claude-3-5-sonnet-20241022"):
        self.client = anthropic.Anthropic()
        self.model = model

    def detect(self, context: str, generated_text: str) -> dict:
        """Compare output against source context"""

        prompt = f"""Is this generated text supported by context? (0-100%)
Context: {context}
Generated: {generated_text}
Response: {{"supported_percentage": X}}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        result = json.loads(response.content[0].text)
        return {
            "hallucination_rate": 1 - (result["supported_percentage"] / 100),
            "supported_percentage": result["supported_percentage"]
        }

detector = HallucinationDetector()
result = detector.detect(
    context="The Eiffel Tower is in Paris and 300m tall",
    generated_text="The Eiffel Tower in Paris is 330m tall"
)
print(f"Hallucination Rate: {result['hallucination_rate']:.1%}")
```

## Quick Start: RAG Evaluation

```python
@dataclass
class RAGMetrics:
    retrieval_precision: float
    retrieval_recall: float
    overall_score: float

class RAGEvaluator:
    def evaluate_retrieval(self, query: str, retrieved: list,
                          relevant_ids: list) -> dict:
        """Score retrieval: precision, recall, MRR"""
        retrieved_set = set(range(len(retrieved)))
        relevant_set = set(relevant_ids)

        precision = len(retrieved_set & relevant_set) / len(retrieved_set) or 0
        recall = len(retrieved_set & relevant_set) / len(relevant_set) or 0

        # Mean Reciprocal Rank
        mrr = 0
        for i, _ in enumerate(retrieved):
            if i in relevant_ids:
                mrr = 1 / (i + 1)
                break

        return {
            "precision": precision,
            "recall": recall,
            "f1": 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0,
            "mrr": mrr
        }
```

## Quick Start: Prompt Engineering A/B Test

```python
def compare_prompts(variants: list, test_cases: list) -> dict:
    """Compare prompt performance on test set"""
    results = {}

    for variant in variants:
        scores = []
        for case in test_cases:
            prompt = variant["template"].format(**case)
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            score = evaluate_output(response.content[0].text)
            scores.append(score)

        results[variant["id"]] = {
            "mean_score": np.mean(scores),
            "std": np.std(scores)
        }

    return results
```

## Quick Start: Cost Optimization

```python
PRICING = {
    "claude-3-5-sonnet-20241022": {"input": 3.0, "output": 15.0},
    "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25}
}

def calculate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    pricing = PRICING.get(model)
    return ((input_tokens / 1_000_000) * pricing["input"] +
            (output_tokens / 1_000_000) * pricing["output"])

# Compare models on single prompt
for model in ["claude-3-5-sonnet-20241022", "claude-3-haiku-20240307"]:
    response = client.messages.create(model=model, max_tokens=256, ...)
    cost = calculate_cost(response.usage.input_tokens,
                         response.usage.output_tokens, model)
    print(f"{model}: ${cost:.4f}")
```

## Best Practices

### DO's
1. Use multiple metrics - combine reference-based, reference-free, LLM-as-judge
2. Establish baselines - track metrics over time
3. Test diverse data - cover edge cases, domains, lengths
4. Automate evaluation - integrate into CI/CD
5. Calibrate judges - validate LLM judges against humans
6. Monitor production - continuous evaluation on real queries
7. Version everything - track prompts, models, datasets
8. Set thresholds - define acceptable ranges
9. Use held-out data - never evaluate on training data
10. Document methodology - for reproducibility

### DON'Ts
1. Don't trust single metrics - BLEU/ROUGE alone insufficient
2. Don't ignore edge cases - rare inputs reveal issues
3. Don't overfit to benchmarks - high MMLU ≠ production-ready
4. Don't skip human eval - periodically validate
5. Don't forget cost - quality/cost tradeoff critical
6. Don't ignore latency - response time matters for UX
7. Don't test only happy paths - test failures, adversarial inputs
8. Don't use stale benchmarks - models may have seen test data
9. Don't evaluate in isolation - consider entire system
10. Don't forget fairness - evaluate across demographic groups

## 8 Core Evaluation Patterns

See **PATTERNS.md** for complete implementations:

1. **LLM Output Quality** - Coherence, relevance, factuality, completeness, conciseness
2. **Prompt Engineering** - A/B test variants with cost/quality tradeoff
3. **RAG Systems** - Retrieval + context + generation evaluation
4. **Hallucination Detection** - Fact-checking, consistency, claim verification
5. **Bias & Fairness** - Demographic parity, sentiment disparity metrics
6. **Cost Optimization** - Token usage analysis, model comparison, optimization
7. **Performance Metrics** - Latency (p50, p95, p99), throughput, load testing
8. **Benchmarks** - MMLU, HumanEval, GSM8K benchmark implementations

## Common Pitfalls

See **GOTCHAS.md** for detailed coverage:
- Benchmark overfitting and data contamination
- Metric-human judgment mismatch
- Hallucination detection challenges
- Bias and fairness assessment pitfalls
- Evaluation dataset size limitations
- Prompt sensitivity and context window issues

## Metrics Reference

See **REFERENCE.md** for:

**Text Metrics**: BLEU, ROUGE-1/2/L, BERTScore, METEOR, perplexity, MAUVE

**Ranking Metrics**: Precision, Recall, F1, MRR, nDCG

**LLM-as-Judge**: G-Eval, Prometheus, AlpacaEval patterns

**Task-Specific**: Pass@k (code), Exact Match (QA), SacreBLEU (translation)

## Knowledge Resources

See **KNOWLEDGE.md** for:
- Evaluation frameworks (HELM, LangSmith, Ragas, OpenAI Evals)
- Benchmarks (MMLU, HumanEval, MBPP, TruthfulQA, BBH, GSM8K, BEIR)
- LLM-as-judge resources and patterns
- Bias/fairness datasets and frameworks
- Production monitoring platforms
- Tool recommendations and libraries

## Complete Examples

See **EXAMPLES.md** for:
- Building evaluation datasets from scratch
- Complete end-to-end evaluation workflows
- Production integration (CI/CD pipelines)
- Monitoring dashboards and reporting
- Cost tracking and analysis

## Related Skills

- `codebase-onboarding-analyzer` - Analyze AI-generated code quality
- `gap-analysis-framework` - Identify evaluation coverage gaps
- `evaluation-reporting-framework` - Generate detailed evaluation reports
- `orchestration-coordination-framework` - Coordinate complex evaluation workflows
- `security-scanning-suite` - Security evaluation for AI systems

## Key Concepts at a Glance

**Evaluation Approaches**
- Reference-based: BLEU, ROUGE (need ground truth)
- Reference-free: Perplexity, consistency (no ground truth)
- LLM-as-judge: Scalable, flexible, but needs calibration
- Human eval: Gold standard, expensive, slow

**Common Metrics**
- Quality: Coherence, Relevance, Factuality, Completeness, Conciseness
- Performance: Latency (p50/p95/p99), Throughput (req/sec), Token count
- Safety: Hallucination rate, Bias score, Toxicity, PII leakage

**Key Benchmarks**
- MMLU: 57 subjects of general knowledge, 15K questions
- HumanEval: 164 coding problems, Pass@k metric
- GSM8K: 8.5K grade school math problems
- TruthfulQA: 817 questions testing truthfulness
- HellaSwag: 70K commonsense reasoning examples

**Critical Pitfalls**
- Benchmark overfitting (high score ≠ production-ready)
- Metric mismatch (BLEU/ROUGE don't correlate with human judgment)
- Hallucination blindness (LLMs sound confident when wrong)
- Prompt sensitivity (tiny changes cause large variance)
- Distribution shift (eval data differs from production)

**Best Practice Workflow**
1. Define evaluation dimensions (quality, performance, safety)
2. Establish baselines on existing systems
3. Create diverse evaluation datasets
4. Use multiple complementary metrics
5. Automate evaluation in CI/CD
6. Monitor production continuously
7. Regular human eval for calibration
8. Document methodology for reproducibility
