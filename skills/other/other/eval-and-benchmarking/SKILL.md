---
name: eval-and-benchmarking
description: LLM and ML model evaluation with lm-evaluation-harness, HELM, and custom benchmarks. Covers metric selection, contamination detection, statistical significance, and leaderboard methodology.
---

# Eval and Benchmarking

## Metric Selection by Task Type

| Task | Primary Metric | Secondary | Avoid |
|------|---------------|-----------|-------|
| Classification | F1 (macro) | Precision, Recall, AUC-ROC | Accuracy (misleading on imbalanced) |
| Text generation | Human eval, LLM-as-judge | BLEU, ROUGE-L | BLEU alone (poor correlation) |
| Summarization | ROUGE-L, BERTScore | Faithfulness (NLI-based) | ROUGE-1 alone |
| QA (extractive) | Exact Match, F1 (token) | Has-answer accuracy | Accuracy without normalization |
| QA (generative) | LLM-as-judge, semantic sim | ROUGE-L | Exact match (too strict) |
| Code generation | pass@k | Functional correctness | BLEU (meaningless for code) |
| Translation | COMET, BLEURT | chrF, BLEU | BLEU without normalization |
| Reasoning | Accuracy (MCQ) | Chain-of-thought analysis | Single-benchmark conclusions |

**Decision rule**: If human eval is feasible, do it. If not, LLM-as-judge + at least one automatic metric. Never rely on a single metric.

## lm-evaluation-harness

### Running Standard Benchmarks

```bash
# Install
pip install lm-eval

# Run MMLU (5-shot) on a local model
lm_eval --model hf \
    --model_args pretrained=meta-llama/Llama-3.1-8B-Instruct,dtype=bfloat16 \
    --tasks mmlu \
    --num_fewshot 5 \
    --batch_size auto \
    --output_path ./results/

# Run multiple benchmarks
lm_eval --model hf \
    --model_args pretrained=./my_model \
    --tasks mmlu,hellaswag,arc_challenge,truthfulqa_mc2,winogrande,gsm8k \
    --batch_size auto \
    --output_path ./results/

# Evaluate a vLLM server
lm_eval --model local-completions \
    --model_args model=meta-llama/Llama-3.1-8B-Instruct,base_url=http://localhost:8000/v1 \
    --tasks mmlu \
    --num_fewshot 5
```

### Custom Eval Task

```yaml
# tasks/my_task/my_task.yaml
task: my_custom_qa
dataset_path: json
dataset_name: null
dataset_kwargs:
  data_files: "./data/eval.jsonl"
output_type: generate_until
training_split: null
test_split: train
doc_to_text: "Question: {{question}}\nAnswer:"
doc_to_target: "{{answer}}"
generation_kwargs:
  until: ["\n", "Question:"]
  max_gen_toks: 64
  temperature: 0
  do_sample: false
metric_list:
  - metric: exact_match
    aggregation: mean
    higher_is_better: true
  - metric: f1
    aggregation: mean
    higher_is_better: true
metadata:
  version: 1.0
```

```bash
# Run custom task
lm_eval --model hf \
    --model_args pretrained=./my_model \
    --tasks my_custom_qa \
    --include_path ./tasks/ \
    --output_path ./results/
```

### Custom Metric in Python

```python
# tasks/my_task/utils.py
import re

def normalize_answer(s):
    """Lowercase, strip articles/punctuation/whitespace."""
    s = s.lower().strip()
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    s = re.sub(r"[^\w\s]", "", s)
    return " ".join(s.split())

def custom_exact_match(references, predictions, **kwargs):
    correct = sum(
        normalize_answer(pred) == normalize_answer(ref)
        for pred, ref in zip(predictions, references)
    )
    return correct / len(predictions)
```

## Statistical Significance Testing

### Bootstrap Confidence Intervals

```python
import numpy as np

def bootstrap_ci(scores, n_bootstrap=10000, confidence=0.95):
    """Bootstrap confidence interval for a metric."""
    rng = np.random.default_rng(42)
    bootstrapped = np.array([
        np.mean(rng.choice(scores, size=len(scores), replace=True))
        for _ in range(n_bootstrap)
    ])
    alpha = (1 - confidence) / 2
    return np.percentile(bootstrapped, [100 * alpha, 100 * (1 - alpha)])

def paired_bootstrap_test(scores_a, scores_b, n_bootstrap=10000):
    """Test if model A is significantly better than model B."""
    rng = np.random.default_rng(42)
    diff = np.array(scores_a) - np.array(scores_b)
    observed_diff = np.mean(diff)

    count = 0
    for _ in range(n_bootstrap):
        sample = rng.choice(diff, size=len(diff), replace=True)
        if np.mean(sample) <= 0:
            count += 1

    p_value = count / n_bootstrap
    return {"observed_diff": observed_diff, "p_value": p_value,
            "significant": p_value < 0.05}
```

```python
# Usage
model_a_scores = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1]  # per-example correctness
model_b_scores = [1, 0, 0, 1, 0, 1, 0, 1, 0, 1]

ci = bootstrap_ci(model_a_scores)
print(f"Model A: {np.mean(model_a_scores):.3f} [{ci[0]:.3f}, {ci[1]:.3f}]")

result = paired_bootstrap_test(model_a_scores, model_b_scores)
print(f"Diff: {result['observed_diff']:.3f}, p={result['p_value']:.3f}")
```

## LLM-as-Judge

```python
JUDGE_PROMPT = """Rate the following response on a scale of 1-5.

Criteria:
- Accuracy: Does the response correctly answer the question?
- Completeness: Does it cover all relevant aspects?
- Conciseness: Is it free of unnecessary information?

Question: {question}
Reference Answer: {reference}
Model Response: {response}

Output ONLY a JSON object: {{"score": <1-5>, "reasoning": "<brief explanation>"}}"""

def llm_judge(client, question, reference, response):
    result = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": JUDGE_PROMPT.format(
            question=question, reference=reference, response=response
        )}],
        temperature=0,
    )
    return json.loads(result.choices[0].message.content)
```

**Gotcha**: LLM judges have position bias (prefer the first response in pairwise eval). Always run comparisons in both orders and average.

## Contamination Detection

### N-gram Overlap Check

```python
def check_contamination(train_texts, eval_texts, n=13):
    """Check for n-gram overlap between training and eval data."""
    def get_ngrams(text, n):
        words = text.lower().split()
        return set(tuple(words[i:i+n]) for i in range(len(words) - n + 1))

    train_ngrams = set()
    for text in train_texts:
        train_ngrams.update(get_ngrams(text, n))

    contaminated = []
    for i, text in enumerate(eval_texts):
        eval_ngrams = get_ngrams(text, n)
        overlap = eval_ngrams & train_ngrams
        if overlap:
            contaminated.append({
                "index": i, "overlap_ratio": len(overlap) / max(len(eval_ngrams), 1),
                "sample_overlap": list(overlap)[:3],
            })
    return contaminated
```

### Canary String Method

```python
# Insert unique canaries into training data, check if model memorizes them
CANARY = "The quick brown fox benchmark canary 7f3a9b2e"

def test_memorization(model, tokenizer, canary_prefix, full_canary):
    """If model completes the canary, training data leaked into eval."""
    inputs = tokenizer(canary_prefix, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_new_tokens=50, temperature=0)
    generated = tokenizer.decode(output[0], skip_special_tokens=True)
    return full_canary in generated
```

## Gotchas and Anti-Patterns

### Benchmark Gaming
- **Prompt format sensitivity**: A model scoring 70% on MMLU with one prompt can score 60% with another. Always report the exact prompt template.
- **Few-shot vs zero-shot**: Not comparable. A 5-shot result is not better than a 0-shot result from a different model. Always compare like-for-like.
- **Subset selection**: Reporting results on "selected" benchmarks is cherry-picking. Use standard suites (Open LLM Leaderboard tasks).

### Lost-in-the-Middle
For long-context eval, models perform best on information at the beginning and end of the context, worst in the middle. Eval must test retrieval at all positions.

### Common Mistakes
- Comparing models evaluated with different tokenizers (affects token-level metrics)
- Using `temperature > 0` during eval (introduces variance between runs)
- Not normalizing answers before exact match (whitespace, articles, casing)
- Reporting mean without confidence intervals on small eval sets
- Evaluating instruction-tuned models with base-model prompts (or vice versa)
- Running benchmarks on data the model was trained on (contamination)
