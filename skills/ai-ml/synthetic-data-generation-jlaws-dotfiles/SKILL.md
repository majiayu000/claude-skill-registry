---
name: synthetic-data-generation
description: LLM-generated training data, augmentation strategies, distillation datasets, self-instruct and Evol-Instruct patterns, quality filtering pipelines.
---

# Synthetic Data Generation

## When to Use

Generate synthetic training data when real data is scarce, expensive to label, or restricted by privacy/licensing. Also applies to distillation pipelines where a larger model generates training signal for a smaller one.

## Strategy Selection

### Decision Table: Synthetic Data Strategy by Use Case

| Use Case | Strategy | Quality Bar | Volume Needed | Key Risk |
|----------|----------|-------------|---------------|----------|
| Instruction tuning (general) | Self-Instruct | Medium-High | 10K-100K | Diversity collapse |
| Instruction tuning (complex) | Evol-Instruct | High | 5K-50K | Over-complexity drift |
| Domain adaptation | Paraphrasing + seeding | Medium | 50K-500K | Distribution shift |
| Low-resource language | Back-translation | Medium | 10K-100K | Translationese artifacts |
| Distillation | Teacher rationale generation | High | 10K-1M | Capacity gap noise |
| Classification augmentation | Label-conditioned generation | Medium | 10K-100K | Label leakage |
| Safety/alignment | Red-teaming + refusal pairs | High | 1K-10K | Reward hacking patterns |

### Decision Table: Quality vs Quantity Tradeoff

| Data Budget | Filtering Strategy | Expected Yield | Notes |
|-------------|-------------------|----------------|-------|
| < 5K samples | Manual review + LLM-as-judge | 60-80% pass | Worth human verification |
| 5K-50K | LLM-as-judge + heuristic filters | 40-70% pass | Two-stage filtering |
| 50K-500K | Heuristic filters + sampling QA | 30-60% pass | Spot-check batches |
| > 500K | Deduplication + basic heuristics | 50-80% pass | Diversity matters more than per-sample quality |

## Self-Instruct Pipeline

### Core Loop

```python
import openai
import json
import random
from collections import Counter

SEED_TASKS = [
    {"instruction": "Summarize the key points of this article.", "input": "", "output": "..."},
    {"instruction": "Convert this Python function to use list comprehension.", "input": "def f(xs): ...", "output": "..."},
    # 50-175 seed tasks for diversity
]

def generate_instructions(client, seed_pool, n=5, model="gpt-4o"):
    """Generate new instructions from seed examples."""
    sampled = random.sample(seed_pool, min(8, len(seed_pool)))
    prompt = f"Generate {n} diverse task instructions. Each must be distinct from these examples:\n\n"
    for i, task in enumerate(sampled, 1):
        prompt += f"{i}. {task['instruction']}\n"
    prompt += f"\nReturn {n} new instructions as a JSON array of strings."

    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        response_format={"type": "json_object"},
    )
    return json.loads(resp.choices[0].message.content)["instructions"]


def generate_instance(client, instruction, model="gpt-4o"):
    """Generate input-output pair for an instruction."""
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Generate a training example for this task."},
            {"role": "user", "content": f"Instruction: {instruction}\n\nProvide a JSON with 'input' and 'output' fields."},
        ],
        temperature=0.7,
        response_format={"type": "json_object"},
    )
    return json.loads(resp.choices[0].message.content)


def self_instruct_loop(client, seeds, target_count=10000):
    """Main self-instruct generation loop."""
    pool = list(seeds)
    generated = []
    seen_instructions = set(t["instruction"].lower().strip() for t in seeds)

    while len(generated) < target_count:
        new_instructions = generate_instructions(client, pool)
        for instr in new_instructions:
            normalized = instr.lower().strip()
            if normalized in seen_instructions:
                continue
            seen_instructions.add(normalized)
            instance = generate_instance(client, instr)
            task = {"instruction": instr, **instance}
            generated.append(task)
            pool.append(task)

    return generated
```

### Evol-Instruct Enhancement

```python
EVOLUTION_STRATEGIES = [
    "Add constraints: make the task harder by adding specific requirements.",
    "Deepen: require multi-step reasoning instead of a single step.",
    "Concretize: replace generic references with specific domain examples.",
    "Broaden: generalize the task to cover more scenarios.",
    "Increase reasoning: require the response to explain its logic step by step.",
]

def evolve_instruction(client, instruction, strategy, model="gpt-4o"):
    """Evolve an instruction using a specific strategy."""
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"Rewrite this instruction to make it more challenging. Strategy: {strategy}"},
            {"role": "user", "content": instruction},
        ],
        temperature=0.8,
    )
    return resp.choices[0].message.content
```

## Quality Filtering

### LLM-as-Judge

```python
JUDGE_PROMPT = """Rate this training example on a 1-5 scale for each criterion:
- Instruction clarity (is the task unambiguous?)
- Output correctness (does the output correctly fulfill the instruction?)
- Output completeness (is anything missing?)
- Difficulty (1=trivial, 5=expert-level)

Instruction: {instruction}
Input: {input}
Output: {output}

Return JSON: {{"clarity": int, "correctness": int, "completeness": int, "difficulty": int, "reject_reason": str|null}}"""

def filter_with_judge(client, examples, min_score=3.5, model="gpt-4o-mini"):
    """Filter examples using LLM-as-judge scoring."""
    passed = []
    for ex in examples:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": JUDGE_PROMPT.format(**ex)}],
            response_format={"type": "json_object"},
        )
        scores = json.loads(resp.choices[0].message.content)
        avg = (scores["clarity"] + scores["correctness"] + scores["completeness"]) / 3
        if avg >= min_score and scores["correctness"] >= 4:
            ex["judge_scores"] = scores
            passed.append(ex)
    return passed
```

### Diversity Sampling

```python
from sentence_transformers import SentenceTransformer
from sklearn.cluster import MiniBatchKMeans
import numpy as np

def diversity_sample(examples, target_n, model_name="all-MiniLM-L6-v2"):
    """Select diverse subset via embedding clustering."""
    model = SentenceTransformer(model_name)
    texts = [ex["instruction"] for ex in examples]
    embeddings = model.encode(texts, show_progress_bar=True)

    n_clusters = min(target_n, len(examples))
    kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(embeddings)

    # Pick the example closest to each cluster center
    selected = []
    for cluster_id in range(n_clusters):
        mask = kmeans.labels_ == cluster_id
        cluster_embeds = embeddings[mask]
        cluster_indices = np.where(mask)[0]
        center = kmeans.cluster_centers_[cluster_id]
        distances = np.linalg.norm(cluster_embeds - center, axis=1)
        best_idx = cluster_indices[np.argmin(distances)]
        selected.append(examples[best_idx])

    return selected
```

### Back-Translation Augmentation

```python
from transformers import MarianMTModel, MarianTokenizer

def back_translate(texts, pivot_lang="de", batch_size=32):
    """Augment text via round-trip translation (en -> pivot -> en)."""
    fwd_name = f"Helsinki-NLP/opus-mt-en-{pivot_lang}"
    bwd_name = f"Helsinki-NLP/opus-mt-{pivot_lang}-en"

    fwd_tok = MarianTokenizer.from_pretrained(fwd_name)
    fwd_model = MarianMTModel.from_pretrained(fwd_name)
    bwd_tok = MarianTokenizer.from_pretrained(bwd_name)
    bwd_model = MarianMTModel.from_pretrained(bwd_name)

    augmented = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        # Forward: en -> pivot
        encoded = fwd_tok(batch, return_tensors="pt", padding=True, truncation=True)
        translated = fwd_model.generate(**encoded)
        pivot_texts = fwd_tok.batch_decode(translated, skip_special_tokens=True)
        # Backward: pivot -> en
        encoded = bwd_tok(pivot_texts, return_tensors="pt", padding=True, truncation=True)
        back = bwd_model.generate(**encoded)
        augmented.extend(bwd_tok.batch_decode(back, skip_special_tokens=True))

    return augmented
```

## Gotchas and Anti-Patterns

### Model Collapse from Synthetic Data Loops
Training model B on synthetic data from model A, then generating data from B to train C causes progressive quality degradation. Each generation loses tail distribution diversity. **Mitigation**: always mix real data (>10-20% of final mix), track distributional metrics across generations.

### Diversity Collapse
Self-instruct tends toward repetitive instruction patterns. The model gravitates to templates it finds easy. **Mitigation**: enforce topic/category diversity constraints, use embedding-based dedup with a similarity threshold of ~0.85, rotate seed examples.

### License Contamination
Synthetic data generated by a model trained on copyrighted content may reproduce that content. **Mitigation**: run near-duplicate detection against known datasets (The Pile, RedPajama), filter outputs with n-gram overlap checks, document provenance chain.

### Quality-Quantity Inversion
More synthetic data is not always better. Past a threshold, adding low-quality synthetic data degrades model performance. **Mitigation**: plot validation loss vs. synthetic data ratio, typically optimal at 30-70% synthetic depending on domain.

### Evaluation Contamination
If synthetic data inadvertently includes benchmark questions or answers, eval metrics become meaningless. **Mitigation**: filter against known benchmark datasets before training, use held-out evals the generating model never saw.

### Reward Hacking in Judge Pipelines
LLM judges tend to prefer longer, more verbose outputs regardless of correctness. **Mitigation**: include length-penalizing criteria, use pairwise comparison instead of absolute scoring, calibrate with human-annotated anchors.
