---
name: evaluating-llms
description: Evaluate LLM systems using automated metrics, LLM-as-judge, and benchmarks. Use when testing prompt quality, validating RAG pipelines, measuring safety (hallucinations, bias), or comparing models for production deployment.
---

# LLM Evaluation

Evaluate Large Language Model (LLM) systems using automated metrics, LLM-as-judge patterns, and standardized benchmarks to ensure production quality and safety.

## When to Use This Skill

Apply this skill when:

- Testing individual prompts for correctness and formatting
- Validating RAG (Retrieval-Augmented Generation) pipeline quality
- Measuring hallucinations, bias, or toxicity in LLM outputs
- Comparing different models or prompt configurations (A/B testing)
- Running benchmark tests (MMLU, HumanEval) to assess model capabilities
- Setting up production monitoring for LLM applications
- Integrating LLM quality checks into CI/CD pipelines

Common triggers:
- "How do I test if my RAG system is working correctly?"
- "How can I measure hallucinations in LLM outputs?"
- "What metrics should I use to evaluate generation quality?"
- "How do I compare GPT-4 vs Claude for my use case?"
- "How do I detect bias in LLM responses?"

## Evaluation Strategy Selection

### Decision Framework: Which Evaluation Approach?

**By Task Type:**

| Task Type | Primary Approach | Metrics | Tools |
|-----------|------------------|---------|-------|
| **Classification** (sentiment, intent) | Automated metrics | Accuracy, Precision, Recall, F1 | scikit-learn |
| **Generation** (summaries, creative text) | LLM-as-judge + automated | BLEU, ROUGE, BERTScore, Quality rubric | GPT-4/Claude for judging |
| **Question Answering** | Exact match + semantic similarity | EM, F1, Cosine similarity | Custom evaluators |
| **RAG Systems** | RAGAS framework | Faithfulness, Answer/Context relevance | RAGAS library |
| **Code Generation** | Unit tests + execution | Pass@K, Test pass rate | HumanEval, pytest |
| **Multi-step Agents** | Task completion + tool accuracy | Success rate, Efficiency | Custom evaluators |

**By Volume and Cost:**

| Samples | Speed | Cost | Recommended Approach |
|---------|-------|------|---------------------|
| 1,000+ | Immediate | $0 | Automated metrics (regex, JSON validation) |
| 100-1,000 | Minutes | $0.01-0.10 each | LLM-as-judge (GPT-4, Claude) |
| < 100 | Hours | $1-10 each | Human evaluation (pairwise comparison) |

**Layered Approach (Recommended for Production):**
1. **Layer 1:** Automated metrics for all outputs (fast, cheap)
2. **Layer 2:** LLM-as-judge for 10% sample (nuanced quality)
3. **Layer 3:** Human review for 1% edge cases (validation)

## Core Evaluation Patterns

### Unit Evaluation (Individual Prompts)

Test single prompt-response pairs for correctness.

**Methods:**
- **Exact Match:** Response exactly matches expected output
- **Regex Matching:** Response follows expected pattern
- **JSON Schema Validation:** Structured output validation
- **Keyword Presence:** Required terms appear in response
- **LLM-as-Judge:** Binary pass/fail using evaluation prompt

**Example Use Cases:**
- Email classification (spam/not spam)
- Entity extraction (dates, names, locations)
- JSON output formatting validation
- Sentiment analysis (positive/negative/neutral)

**Quick Start (Python):**
```python
import pytest
from openai import OpenAI

client = OpenAI()

def classify_sentiment(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Classify sentiment as positive, negative, or neutral. Return only the label."},
            {"role": "user", "content": text}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip().lower()

def test_positive_sentiment():
    result = classify_sentiment("I love this product!")
    assert result == "positive"
```

For complete unit evaluation examples, see `examples/python/unit_evaluation.py` and `examples/typescript/unit-evaluation.ts`.

### RAG (Retrieval-Augmented Generation) Evaluation

Evaluate RAG systems using RAGAS framework metrics.

**Critical Metrics (Priority Order):**

1. **Faithfulness** (Target: > 0.8) - **MOST CRITICAL**
   - Measures: Is the answer grounded in retrieved context?
   - Prevents hallucinations
   - If failing: Adjust prompt to emphasize grounding, require citations

2. **Answer Relevance** (Target: > 0.7)
   - Measures: How well does the answer address the query?
   - If failing: Improve prompt instructions, add few-shot examples

3. **Context Relevance** (Target: > 0.7)
   - Measures: Are retrieved chunks relevant to the query?
   - If failing: Improve retrieval (better embeddings, hybrid search)

4. **Context Precision** (Target: > 0.5)
   - Measures: Are relevant chunks ranked higher than irrelevant?
   - If failing: Add re-ranking step to retrieval pipeline

5. **Context Recall** (Target: > 0.8)
   - Measures: Are all relevant chunks retrieved?
   - If failing: Increase retrieval count, improve chunking strategy

**Quick Start (Python with RAGAS):**
```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_relevancy
from datasets import Dataset

data = {
    "question": ["What is the capital of France?"],
    "answer": ["The capital of France is Paris."],
    "contexts": [["Paris is the capital of France."]],
    "ground_truth": ["Paris"]
}

dataset = Dataset.from_dict(data)
results = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_relevancy])
print(f"Faithfulness: {results['faithfulness']:.2f}")
```

For comprehensive RAG evaluation patterns, see `references/rag-evaluation.md` and `examples/python/ragas_example.py`.

### LLM-as-Judge Evaluation

Use powerful LLMs (GPT-4, Claude Opus) to evaluate other LLM outputs.

**When to Use:**
- Generation quality assessment (summaries, creative writing)
- Nuanced evaluation criteria (tone, clarity, helpfulness)
- Custom rubrics for domain-specific tasks
- Medium-volume evaluation (100-1,000 samples)

**Correlation with Human Judgment:** 0.75-0.85 for well-designed rubrics

**Best Practices:**
- Use clear, specific rubrics (1-5 scale with detailed criteria)
- Include few-shot examples in evaluation prompt
- Average multiple evaluations to reduce variance
- Be aware of biases (position bias, verbosity bias, self-preference)

**Quick Start (Python):**
```python
from openai import OpenAI

client = OpenAI()

def evaluate_quality(prompt: str, response: str) -> tuple[int, str]:
    """Returns (score 1-5, reasoning)"""
    eval_prompt = f"""
Rate the following LLM response on relevance and helpfulness.

USER PROMPT: {prompt}
LLM RESPONSE: {response}

Provide:
Score: [1-5, where 5 is best]
Reasoning: [1-2 sentences]
"""
    result = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": eval_prompt}],
        temperature=0.3
    )
    content = result.choices[0].message.content
    lines = content.strip().split('\n')
    score = int(lines[0].split(':')[1].strip())
    reasoning = lines[1].split(':', 1)[1].strip()
    return score, reasoning
```

For detailed LLM-as-judge patterns and prompt templates, see `references/llm-as-judge.md` and `examples/python/llm_as_judge.py`.

### Safety and Alignment Evaluation

Measure hallucinations, bias, and toxicity in LLM outputs.

#### Hallucination Detection

**Methods:**

1. **Faithfulness to Context (RAG):**
   - Use RAGAS faithfulness metric
   - LLM checks if claims are supported by context
   - Score: Supported claims / Total claims

2. **Factual Accuracy (Closed-Book):**
   - LLM-as-judge with access to reliable sources
   - Fact-checking APIs (Google Fact Check)
   - Entity-level verification (dates, names, statistics)

3. **Self-Consistency:**
   - Generate multiple responses to same question
   - Measure agreement between responses
   - Low consistency suggests hallucination

#### Bias Evaluation

**Types of Bias:**
- Gender bias (stereotypical associations)
- Racial/ethnic bias (discriminatory outputs)
- Cultural bias (Western-centric assumptions)
- Age/disability bias (ableist or ageist language)

**Evaluation Methods:**

1. **Stereotype Tests:**
   - BBQ (Bias Benchmark for QA): 58,000 question-answer pairs
   - BOLD (Bias in Open-Ended Language Generation)

2. **Counterfactual Evaluation:**
   - Generate responses with demographic swaps
   - Example: "Dr. Smith (he/she) recommended..." → compare outputs
   - Measure consistency across variations

#### Toxicity Detection

**Tools:**
- **Perspective API (Google):** Toxicity, threat, insult scores
- **Detoxify (HuggingFace):** Open-source toxicity classifier
- **OpenAI Moderation API:** Hate, harassment, violence detection

For comprehensive safety evaluation patterns, see `references/safety-evaluation.md`.

### Benchmark Testing

Assess model capabilities using standardized benchmarks.

**Standard Benchmarks:**

| Benchmark | Coverage | Format | Difficulty | Use Case |
|-----------|----------|--------|------------|----------|
| **MMLU** | 57 subjects (STEM, humanities) | Multiple choice | High school - professional | General intelligence |
| **HellaSwag** | Sentence completion | Multiple choice | Common sense | Reasoning validation |
| **GPQA** | PhD-level science | Multiple choice | Very high (expert-level) | Frontier model testing |
| **HumanEval** | 164 Python problems | Code generation | Medium | Code capability |
| **MATH** | 12,500 competition problems | Math solving | High school competitions | Math reasoning |

**Domain-Specific Benchmarks:**
- **Medical:** MedQA (USMLE), PubMedQA
- **Legal:** LegalBench
- **Finance:** FinQA, ConvFinQA

**When to Use Benchmarks:**
- Comparing multiple models (GPT-4 vs Claude vs Llama)
- Model selection for specific domains
- Baseline capability assessment
- Academic research and publication

**Quick Start (lm-evaluation-harness):**
```bash
pip install lm-eval

# Evaluate GPT-4 on MMLU
lm_eval --model openai-chat --model_args model=gpt-4 --tasks mmlu --num_fewshot 5
```

For detailed benchmark testing patterns, see `references/benchmarks.md` and `scripts/benchmark_runner.py`.

### Production Evaluation

Monitor and optimize LLM quality in production environments.

#### A/B Testing

Compare two LLM configurations:
- **Variant A:** GPT-4 (expensive, high quality)
- **Variant B:** Claude Sonnet (cheaper, fast)

**Metrics:**
- User satisfaction scores (thumbs up/down)
- Task completion rates
- Response time and latency
- Cost per successful interaction

#### Online Evaluation

Real-time quality monitoring:
- **Response Quality:** LLM-as-judge scoring every Nth response
- **User Feedback:** Explicit ratings, thumbs up/down
- **Business Metrics:** Conversion rates, support ticket resolution
- **Cost Tracking:** Tokens used, inference costs

#### Human-in-the-Loop

Sample-based human evaluation:
- **Random Sampling:** Evaluate 10% of responses
- **Confidence-Based:** Evaluate low-confidence outputs
- **Error-Triggered:** Flag suspicious responses for review

For production evaluation patterns and monitoring strategies, see `references/production-evaluation.md`.

## Classification Task Evaluation

For tasks with discrete outputs (sentiment, intent, category).

**Metrics:**
- **Accuracy:** Correct predictions / Total predictions
- **Precision:** True positives / (True positives + False positives)
- **Recall:** True positives / (True positives + False negatives)
- **F1 Score:** Harmonic mean of precision and recall
- **Confusion Matrix:** Detailed breakdown of prediction errors

**Quick Start (Python):**
```python
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

y_true = ["positive", "negative", "neutral", "positive", "negative"]
y_pred = ["positive", "negative", "neutral", "neutral", "negative"]

accuracy = accuracy_score(y_true, y_pred)
precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted')

print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")
```

For complete classification evaluation examples, see `examples/python/classification_metrics.py`.

## Generation Task Evaluation

For open-ended text generation (summaries, creative writing, responses).

**Automated Metrics (Use with Caution):**
- **BLEU:** N-gram overlap with reference text (0-1 score)
- **ROUGE:** Recall-oriented overlap (ROUGE-1, ROUGE-L)
- **METEOR:** Semantic similarity with stemming
- **BERTScore:** Contextual embedding similarity (0-1 score)

**Limitation:** Automated metrics correlate weakly with human judgment for creative/subjective generation.

**Recommended Approach:**
1. **Automated metrics:** Fast feedback for objective aspects (length, format)
2. **LLM-as-judge:** Nuanced quality assessment (relevance, coherence, helpfulness)
3. **Human evaluation:** Final validation for subjective criteria (preference, creativity)

For detailed generation evaluation patterns, see `references/evaluation-types.md`.

## Quick Reference Tables

### Evaluation Framework Selection

| If Task Is... | Use This Framework | Primary Metric |
|---------------|-------------------|----------------|
| RAG system | RAGAS | Faithfulness > 0.8 |
| Classification | scikit-learn metrics | Accuracy, F1 |
| Generation quality | LLM-as-judge | Quality rubric (1-5) |
| Code generation | HumanEval | Pass@1, Test pass rate |
| Model comparison | Benchmark testing | MMLU, HellaSwag scores |
| Safety validation | Hallucination detection | Faithfulness, Fact-check |
| Production monitoring | Online evaluation | User feedback, Business KPIs |

### Python Library Recommendations

| Library | Use Case | Installation |
|---------|----------|--------------|
| **RAGAS** | RAG evaluation | `pip install ragas` |
| **DeepEval** | General LLM evaluation, pytest integration | `pip install deepeval` |
| **LangSmith** | Production monitoring, A/B testing | `pip install langsmith` |
| **lm-eval** | Benchmark testing (MMLU, HumanEval) | `pip install lm-eval` |
| **scikit-learn** | Classification metrics | `pip install scikit-learn` |

### Safety Evaluation Priority Matrix

| Application | Hallucination Risk | Bias Risk | Toxicity Risk | Evaluation Priority |
|-------------|-------------------|-----------|---------------|---------------------|
| Customer Support | High | Medium | High | 1. Faithfulness, 2. Toxicity, 3. Bias |
| Medical Diagnosis | Critical | High | Low | 1. Factual Accuracy, 2. Hallucination, 3. Bias |
| Creative Writing | Low | Medium | Medium | 1. Quality/Fluency, 2. Content Policy |
| Code Generation | Medium | Low | Low | 1. Functional Correctness, 2. Security |
| Content Moderation | Low | Critical | Critical | 1. Bias, 2. False Positives/Negatives |

## Detailed References

For comprehensive documentation on specific topics:

- **Evaluation types (classification, generation, QA, code):** `references/evaluation-types.md`
- **RAG evaluation deep dive (RAGAS framework):** `references/rag-evaluation.md`
- **Safety evaluation (hallucination, bias, toxicity):** `references/safety-evaluation.md`
- **Benchmark testing (MMLU, HumanEval, domain benchmarks):** `references/benchmarks.md`
- **LLM-as-judge best practices and prompts:** `references/llm-as-judge.md`
- **Production evaluation (A/B testing, monitoring):** `references/production-evaluation.md`
- **All metrics definitions and formulas:** `references/metrics-reference.md`

## Working Examples

**Python Examples:**
- `examples/python/unit_evaluation.py` - Basic prompt testing with pytest
- `examples/python/ragas_example.py` - RAGAS RAG evaluation
- `examples/python/deepeval_example.py` - DeepEval framework usage
- `examples/python/llm_as_judge.py` - GPT-4 as evaluator
- `examples/python/classification_metrics.py` - Accuracy, precision, recall
- `examples/python/benchmark_testing.py` - HumanEval example

**TypeScript Examples:**
- `examples/typescript/unit-evaluation.ts` - Vitest + OpenAI
- `examples/typescript/llm-as-judge.ts` - GPT-4 evaluation
- `examples/typescript/langsmith-integration.ts` - Production monitoring

## Executable Scripts

Run evaluations without loading code into context (token-free):

- `scripts/run_ragas_eval.py` - Run RAGAS evaluation on dataset
- `scripts/compare_models.py` - A/B test two models
- `scripts/benchmark_runner.py` - Run MMLU/HumanEval benchmarks
- `scripts/hallucination_checker.py` - Detect hallucinations in outputs

**Example usage:**
```bash
# Run RAGAS evaluation on custom dataset
python scripts/run_ragas_eval.py --dataset data/qa_dataset.json --output results.json

# Compare GPT-4 vs Claude on benchmark
python scripts/compare_models.py --model-a gpt-4 --model-b claude-3-opus --tasks mmlu,humaneval
```

## Integration with Other Skills

**Related Skills:**
- **`building-ai-chat`:** Evaluate AI chat applications (this skill tests what that skill builds)
- **`prompt-engineering`:** Test prompt quality and effectiveness
- **`testing-strategies`:** Apply testing pyramid to LLM evaluation (unit → integration → E2E)
- **`observability`:** Production monitoring and alerting for LLM quality
- **`building-ci-pipelines`:** Integrate LLM evaluation into CI/CD

**Workflow Integration:**
1. Write prompt (use `prompt-engineering` skill)
2. Unit test prompt (use `llm-evaluation` skill)
3. Build AI feature (use `building-ai-chat` skill)
4. Integration test RAG pipeline (use `llm-evaluation` skill)
5. Deploy to production (use `deploying-applications` skill)
6. Monitor quality (use `llm-evaluation` + `observability` skills)

## Common Pitfalls

**1. Over-reliance on Automated Metrics for Generation**
- BLEU/ROUGE correlate weakly with human judgment for creative text
- Solution: Layer LLM-as-judge or human evaluation

**2. Ignoring Faithfulness in RAG Systems**
- Hallucinations are the #1 RAG failure mode
- Solution: Prioritize faithfulness metric (target > 0.8)

**3. No Production Monitoring**
- Models can degrade over time, prompts can break with updates
- Solution: Set up continuous evaluation (LangSmith, custom monitoring)

**4. Biased LLM-as-Judge Evaluation**
- Evaluator LLMs have biases (position bias, verbosity bias)
- Solution: Average multiple evaluations, use diverse evaluation prompts

**5. Insufficient Benchmark Coverage**
- Single benchmark doesn't capture full model capability
- Solution: Use 3-5 benchmarks across different domains

**6. Missing Safety Evaluation**
- Production LLMs can generate harmful content
- Solution: Add toxicity, bias, and hallucination checks to evaluation pipeline
