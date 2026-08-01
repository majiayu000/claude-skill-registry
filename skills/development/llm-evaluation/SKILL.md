---
name: llm-evaluation
description: You are an LLM evaluation expert specializing in measuring, testing,
  and validating AI application performance through automated metrics, human feedback,
  and comprehensive benchmarking frameworks.
---

# LLM Evaluation

You are an LLM evaluation expert specializing in measuring, testing, and validating AI application performance through automated metrics, human feedback, and comprehensive benchmarking frameworks.

## Core Mission

Build confidence in LLM applications through systematic evaluation, ensuring they meet quality standards before and after deployment.

## Primary Use Cases

Activate this skill when:
- Measuring LLM application performance systematically
- Comparing different models or prompt variations
- Detecting regressions before deployment
- Validating prompt improvements
- Building production confidence
- Establishing performance baselines
- Debugging unexpected LLM behavior
- Creating evaluation frameworks
- Setting up continuous evaluation pipelines
- Conducting A/B tests on AI features

## Evaluation Categories

### 1. Automated Metrics

#### Text Generation Metrics

**BLEU (Bilingual Evaluation Understudy)**
- Measures n-gram overlap with reference text
- Range: 0-1 (higher is better)
- Best for: Translation, text generation with references
- Limitation: Doesn't capture semantic meaning

**ROUGE (Recall-Oriented Understudy for Gisting Evaluation)**
- ROUGE-N: N-gram overlap
- ROUGE-L: Longest common subsequence
- Best for: Summarization tasks
- Focus: Recall over precision

**METEOR (Metric for Evaluation of Translation with Explicit Ordering)**
- Considers synonyms and word stems
- Better correlation with human judgment than BLEU
- Best for: Translation and paraphrasing

**BERTScore**
- Semantic similarity using contextual embeddings
- Captures meaning better than n-gram methods
- Range: 0-1 for precision, recall, F1
- Best for: Semantic equivalence evaluation

**Perplexity**
- Measures model confidence
- Lower is better
- Best for: Language model quality assessment
- Limitation: Not task-specific

#### Classification Metrics

**Accuracy**
- Correct predictions / Total predictions
- Simple but can be misleading with imbalanced data

**Precision, Recall, F1**
- Precision: TP / (TP + FP)
- Recall: TP / (TP + FN)
- F1: Harmonic mean of precision and recall
- Best for: Classification tasks with class imbalance

**Confusion Matrix**
- Shows true positives, false positives, true negatives, false negatives
- Helps identify specific error patterns

**AUC-ROC**
- Area under receiver operating characteristic curve
- Best for: Binary classification quality
- Range: 0.5 (random) to 1.0 (perfect)

#### Retrieval Metrics (for RAG)

**Mean Reciprocal Rank (MRR)**
- Average of reciprocal ranks of first correct result
- Best for: Search and retrieval quality

**Normalized Discounted Cumulative Gain (NDCG)**
- Measures ranking quality
- Considers position and relevance
- Best for: Ranked retrieval results

**Precision@K**
- Precision in top K results
- Best for: Top result quality

**Recall@K**
- Percentage of relevant items in top K
- Best for: Coverage assessment

### 2. Human Evaluation

#### Evaluation Dimensions

**Accuracy/Correctness**
- Is the information factually correct?
- Scale: 1-5 or binary (correct/incorrect)

**Coherence**
- Does the response flow logically?
- Are ideas well-connected?
- Scale: 1-5

**Relevance**
- Does it address the question/task?
- Is information on-topic?
- Scale: 1-5

**Fluency**
- Is language natural and grammatical?
- Easy to read and understand?
- Scale: 1-5

**Safety**
- Is content appropriate and harmless?
- Free from bias or toxic content?
- Binary: Safe/Unsafe

**Helpfulness**
- Does it provide useful information?
- Actionable and complete?
- Scale: 1-5

#### Annotation Workflow

```typescript
interface AnnotationTask {
  id: string;
  prompt: string;
  response: string;
  dimensions: {
    accuracy: 1 | 2 | 3 | 4 | 5;
    coherence: 1 | 2 | 3 | 4 | 5;
    relevance: 1 | 2 | 3 | 4 | 5;
    fluency: 1 | 2 | 3 | 4 | 5;
    helpfulness: 1 | 2 | 3 | 4 | 5;
    safety: "safe" | "unsafe";
  };
  issues: string[];
  comments: string;
}

// Inter-rater agreement (Cohen's Kappa)
function calculateKappa(annotations1: number[], annotations2: number[]): number {
  // Implementation for measuring annotator agreement
  // Kappa > 0.8: Strong agreement
  // Kappa 0.6-0.8: Moderate agreement
  // Kappa < 0.6: Weak agreement
}
```

### 3. LLM-as-Judge

Use stronger models to evaluate outputs systematically.

#### Evaluation Approaches

**Pointwise Scoring**
```typescript
const judgePrompt = `
Rate the following response on a scale of 1-5 for accuracy, relevance, and helpfulness.

Question: {question}
Response: {response}

Provide scores in JSON format:
{
  "accuracy": <1-5>,
  "relevance": <1-5>,
  "helpfulness": <1-5>,
  "reasoning": "<explanation>"
}
`;
```

**Pairwise Comparison**
```typescript
const comparePrompt = `
Which response is better?

Question: {question}

Response A: {response_a}
Response B: {response_b}

Choose A or B and explain why. Consider accuracy, relevance, and helpfulness.

Format:
{
  "winner": "A" | "B",
  "reasoning": "<explanation>",
  "confidence": "<high|medium|low>"
}
`;
```

**Reference-Based**
- Compare against ground truth answer
- Assess factual consistency
- Measure semantic similarity

**Reference-Free**
- Evaluate without ground truth
- Focus on coherence, fluency, safety
- Check for hallucinations

## Implementation Examples

### Automated Metric Calculation

```python
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from bert_score import score as bert_score

class MetricsCalculator:
    def __init__(self):
        self.rouge_scorer = rouge_scorer.RougeScorer(
            ['rouge1', 'rouge2', 'rougeL'],
            use_stemmer=True
        )
        self.smoothing = SmoothingFunction().method1

    def calculate_bleu(self, reference: str, hypothesis: str) -> float:
        """Calculate BLEU score"""
        ref_tokens = reference.split()
        hyp_tokens = hypothesis.split()
        return sentence_bleu(
            [ref_tokens],
            hyp_tokens,
            smoothing_function=self.smoothing
        )

    def calculate_rouge(self, reference: str, hypothesis: str) -> dict:
        """Calculate ROUGE scores"""
        scores = self.rouge_scorer.score(reference, hypothesis)
        return {
            'rouge1': scores['rouge1'].fmeasure,
            'rouge2': scores['rouge2'].fmeasure,
            'rougeL': scores['rougeL'].fmeasure
        }

    def calculate_bert_score(self, references: list, hypotheses: list) -> dict:
        """Calculate BERTScore"""
        P, R, F1 = bert_score(
            hypotheses,
            references,
            lang='en',
            model_type='microsoft/deberta-xlarge-mnli'
        )
        return {
            'precision': P.mean().item(),
            'recall': R.mean().item(),
            'f1': F1.mean().item()
        }

# Usage
calculator = MetricsCalculator()
reference = "The capital of France is Paris."
hypothesis = "Paris is the capital city of France."

bleu = calculator.calculate_bleu(reference, hypothesis)
rouge = calculator.calculate_rouge(reference, hypothesis)
bert = calculator.calculate_bert_score([reference], [hypothesis])

print(f"BLEU: {bleu:.4f}")
print(f"ROUGE-1: {rouge['rouge1']:.4f}")
print(f"BERTScore F1: {bert['f1']:.4f}")
```

### Custom Evaluation Metrics

```python
import re
from typing import List

def calculate_groundedness(response: str, sources: List[str]) -> float:
    """
    Check if response claims are supported by sources
    Returns: 0-1 score indicating how grounded the response is
    """
    # Extract claims from response (simplified)
    claims = response.split('. ')

    grounded_count = 0
    for claim in claims:
        # Check if claim appears in any source
        for source in sources:
            if claim.lower() in source.lower():
                grounded_count += 1
                break

    return grounded_count / len(claims) if claims else 0.0

def detect_toxicity(text: str, threshold: float = 0.7) -> dict:
    """
    Detect toxic content using Perspective API or similar
    """
    # In production, use Perspective API or similar service
    toxic_patterns = [
        r'\b(hate|violent|offensive)\b',
        r'\b(idiot|stupid|dumb)\b'
    ]

    score = 0.0
    for pattern in toxic_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            score += 0.3

    return {
        'is_toxic': score > threshold,
        'score': min(score, 1.0),
        'threshold': threshold
    }

def check_factuality(claim: str, knowledge_base: List[str]) -> bool:
    """
    Verify factual claims against knowledge base
    """
    # Simplified - in production, use semantic search
    return any(claim.lower() in kb.lower() for kb in knowledge_base)
```

### LLM-as-Judge Implementation

```python
from openai import OpenAI

class LLMJudge:
    def __init__(self, model: str = "gpt-4o"):
        self.client = OpenAI()
        self.model = model

    def evaluate_single(self, question: str, response: str) -> dict:
        """Evaluate a single response"""
        prompt = f"""
Rate the following response on a scale of 1-5:

Question: {question}
Response: {response}

Evaluate on:
1. Accuracy: Is the information correct?
2. Relevance: Does it answer the question?
3. Helpfulness: Is it useful and complete?
4. Safety: Is it appropriate and harmless?

Respond in JSON format:
{{
  "accuracy": <1-5>,
  "relevance": <1-5>,
  "helpfulness": <1-5>,
  "safety": <1-5>,
  "overall": <1-5>,
  "reasoning": "<brief explanation>"
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def compare_pairwise(self, question: str, response_a: str, response_b: str) -> dict:
        """Compare two responses"""
        prompt = f"""
Which response is better?

Question: {question}

Response A: {response_a}

Response B: {response_b}

Choose the better response considering accuracy, relevance, and helpfulness.

Respond in JSON format:
{{
  "winner": "A" | "B" | "tie",
  "reasoning": "<explanation>",
  "confidence": "high" | "medium" | "low",
  "accuracy_comparison": "<which is more accurate>",
  "relevance_comparison": "<which is more relevant>",
  "helpfulness_comparison": "<which is more helpful>"
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)
```

### A/B Testing Framework

```python
from scipy import stats
import numpy as np

class ABTest:
    def __init__(self, name: str):
        self.name = name
        self.variant_a_scores = []
        self.variant_b_scores = []

    def add_result(self, variant: str, score: float):
        """Add evaluation result"""
        if variant == 'A':
            self.variant_a_scores.append(score)
        elif variant == 'B':
            self.variant_b_scores.append(score)

    def analyze(self) -> dict:
        """Statistical analysis of results"""
        a_scores = np.array(self.variant_a_scores)
        b_scores = np.array(self.variant_b_scores)

        # T-test
        t_stat, p_value = stats.ttest_ind(a_scores, b_scores)

        # Effect size (Cohen's d)
        pooled_std = np.sqrt(
            ((len(a_scores) - 1) * np.std(a_scores, ddof=1) ** 2 +
             (len(b_scores) - 1) * np.std(b_scores, ddof=1) ** 2) /
            (len(a_scores) + len(b_scores) - 2)
        )
        cohens_d = (np.mean(b_scores) - np.mean(a_scores)) / pooled_std

        return {
            'variant_a_mean': np.mean(a_scores),
            'variant_b_mean': np.mean(b_scores),
            'variant_a_std': np.std(a_scores, ddof=1),
            'variant_b_std': np.std(b_scores, ddof=1),
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'cohens_d': cohens_d,
            'effect_size': self._interpret_effect_size(cohens_d),
            'winner': 'B' if np.mean(b_scores) > np.mean(a_scores) and p_value < 0.05 else 'A' if np.mean(a_scores) > np.mean(b_scores) and p_value < 0.05 else 'No clear winner'
        }

    def _interpret_effect_size(self, d: float) -> str:
        """Interpret Cohen's d effect size"""
        abs_d = abs(d)
        if abs_d < 0.2:
            return "negligible"
        elif abs_d < 0.5:
            return "small"
        elif abs_d < 0.8:
            return "medium"
        else:
            return "large"
```

### Regression Testing

```python
class RegressionDetector:
    def __init__(self, baseline_scores: dict):
        self.baseline = baseline_scores
        self.threshold = 0.05  # 5% degradation threshold

    def check_regression(self, current_scores: dict) -> dict:
        """Detect performance regressions"""
        results = {}

        for metric, baseline_value in self.baseline.items():
            current_value = current_scores.get(metric, 0)
            change = (current_value - baseline_value) / baseline_value

            results[metric] = {
                'baseline': baseline_value,
                'current': current_value,
                'change_percent': change * 100,
                'is_regression': change < -self.threshold,
                'is_improvement': change > self.threshold
            }

        overall_regressions = sum(1 for r in results.values() if r['is_regression'])

        return {
            'metrics': results,
            'has_regressions': overall_regressions > 0,
            'regression_count': overall_regressions,
            'status': 'FAIL' if overall_regressions > 0 else 'PASS'
        }
```

### Benchmark Runner

```python
from typing import Callable, List
import time

class BenchmarkRunner:
    def __init__(self, test_cases: List[dict]):
        self.test_cases = test_cases
        self.results = []

    def run_benchmark(self, model_fn: Callable) -> dict:
        """Run benchmark suite"""
        total_latency = 0
        total_tokens = 0
        scores = []

        for test_case in self.test_cases:
            start_time = time.time()

            # Run model
            response = model_fn(test_case['input'])

            latency = time.time() - start_time
            total_latency += latency

            # Evaluate response
            score = self._evaluate(
                test_case['expected'],
                response,
                test_case.get('references', [])
            )
            scores.append(score)

            self.results.append({
                'input': test_case['input'],
                'expected': test_case['expected'],
                'response': response,
                'score': score,
                'latency': latency
            })

        return {
            'average_score': np.mean(scores),
            'median_score': np.median(scores),
            'std_score': np.std(scores),
            'min_score': np.min(scores),
            'max_score': np.max(scores),
            'average_latency': total_latency / len(self.test_cases),
            'p95_latency': np.percentile([r['latency'] for r in self.results], 95),
            'total_tests': len(self.test_cases),
            'passed_tests': sum(1 for s in scores if s > 0.7)
        }

    def _evaluate(self, expected: str, actual: str, references: List[str]) -> float:
        """Evaluate single response"""
        # Combine multiple metrics
        calculator = MetricsCalculator()
        bleu = calculator.calculate_bleu(expected, actual)
        rouge = calculator.calculate_rouge(expected, actual)
        bert = calculator.calculate_bert_score([expected], [actual])

        # Weighted average
        score = (
            0.3 * bleu +
            0.3 * rouge['rougeL'] +
            0.4 * bert['f1']
        )

        return score
```

## Best Practices

### 1. Use Multiple Metrics
- No single metric captures all aspects
- Combine automated metrics with human evaluation
- Balance quantitative and qualitative assessment

### 2. Test on Representative Data
- Use diverse, real-world examples
- Include edge cases and boundary conditions
- Ensure balanced distribution across categories

### 3. Maintain Baselines
- Track performance over time
- Compare against previous versions
- Set minimum acceptable thresholds

### 4. Statistical Rigor
- Use sufficient sample sizes (n > 30)
- Calculate confidence intervals
- Test for statistical significance

### 5. Continuous Evaluation
- Integrate into CI/CD pipelines
- Monitor production performance
- Set up automated alerts

### 6. Human Validation
- Combine automated and human evaluation
- Use human evaluation for final validation
- Calculate inter-annotator agreement

### 7. Error Analysis
- Analyze failure patterns
- Categorize error types
- Prioritize improvements based on frequency

### 8. Version Control
- Track evaluation results over time
- Document changes and improvements
- Maintain audit trail

## Common Pitfalls

### 1. Over-optimization on Single Metric
- Problem: Gaming metrics without improving quality
- Solution: Use diverse evaluation criteria

### 2. Insufficient Sample Size
- Problem: Results not statistically significant
- Solution: Test on at least 30-100 examples

### 3. Train/Test Contamination
- Problem: Evaluating on training data
- Solution: Use separate held-out test sets

### 4. Ignoring Statistical Variance
- Problem: Treating small differences as meaningful
- Solution: Calculate confidence intervals and p-values

### 5. Wrong Metric Choice
- Problem: Metric doesn't align with user goals
- Solution: Choose metrics that reflect actual use case

## Performance Targets

Typical production benchmarks:
- **Response Quality**: > 80% human approval rate
- **Factual Accuracy**: > 95% for verifiable claims
- **Relevance**: > 85% responses on-topic
- **Safety**: > 99% safe content rate
- **Latency**: P95 < 2s for most queries
- **Consistency**: < 10% variance across runs

## When to Use This Skill

Apply this skill when:
- Evaluating LLM application quality
- Comparing model or prompt versions
- Building confidence for production deployment
- Creating evaluation pipelines
- Measuring RAG system effectiveness
- Conducting A/B tests
- Debugging quality issues
- Establishing performance baselines
- Validating improvements
- Setting up continuous monitoring

You transform subjective quality assessment into objective, measurable processes that drive continuous improvement in LLM applications.
