---
name: keyword-based-llm-eval
description: "Use when evaluating LLM-generated structured output against expected results using keyword matching and F1 metrics."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-10"
---

# Keyword-Based LLM Output Evaluation

**Extracted:** 2026-02-10
**Context:** Evaluating structured LLM output (cards, summaries, extractions) against expected results without exact match or expensive semantic similarity.

## Problem

LLM generates structured output (e.g., Anki cards with front/back text, card types, tags). Need to measure prompt quality quantitatively — but:
- Exact match is too strict (LLM wording varies)
- Semantic similarity (embeddings) is expensive and adds dependency
- Manual review doesn't scale

## Solution

Keyword presence-based lightweight matching with greedy best-match:

### 1. Define Expected Output as Keywords

```python
@dataclass(frozen=True, slots=True)
class ExpectedCard:
    front_keywords: list[str]  # must appear in generated front
    back_keywords: list[str]   # must appear in generated back
    card_type: CardType | None = None  # optional type constraint
```

### 2. Keyword Similarity Score

```python
def _keyword_similarity(keywords: list[str], text: str) -> float:
    if not keywords:
        return 0.0
    found = sum(1 for kw in keywords if kw in text)
    return found / len(keywords)
```

### 3. Weighted Pair Scoring

```python
def _score_pair(expected, card) -> float:
    front_sim = _keyword_similarity(expected.front_keywords, card.front)
    back_sim = _keyword_similarity(expected.back_keywords, card.back)
    # Optional type bonus (20% weight when type specified)
    if expected.card_type is not None:
        type_bonus = 1.0 if card.card_type == expected.card_type else 0.0
        return front_sim * 0.4 + back_sim * 0.4 + type_bonus * 0.2
    return front_sim * 0.5 + back_sim * 0.5
```

### 4. Greedy Best-Match Algorithm

```python
def match_cards(expected, generated, threshold=0.3) -> CaseResult:
    used_indices: set[int] = set()
    for ec in expected:
        # Find highest-scoring unused generated card
        best_score, best_idx = 0.0, -1
        for i, card in enumerate(generated):
            if i in used_indices:
                continue
            score = _score_pair(ec, card)
            if score > best_score:
                best_score, best_idx = score, i
        if best_idx >= 0 and best_score >= threshold:
            used_indices.add(best_idx)
            # Record match
    # Remaining generated cards = unmatched (extra output)
```

### 5. Aggregate Metrics

- **Recall** = matched / total_expected (coverage)
- **Precision** = matched / total_generated (relevance)
- **F1** = harmonic mean
- **Avg Similarity** = mean similarity of matched pairs

### 6. YAML Dataset Format

```yaml
name: "eval-dataset"
version: "1.0"
cases:
  - id: "case-01"
    text: "Input text for LLM..."
    expected_cards:
      - front_keywords: ["key concept"]
        back_keywords: ["expected answer part"]
        card_type: qa
```

## Architecture

4-module separation (each independently testable):

```
dataset.py  → ExpectedCard/EvalCase/EvalDataset + YAML loader
matcher.py  → _keyword_similarity + _score_pair + match_cards (greedy)
metrics.py  → EvalMetrics (Recall/Precision/F1) + calculate_metrics
report.py   → Rich table + JSON report + comparison report
```

## When to Use

- Building eval harness for LLM-generated structured output
- Measuring prompt quality changes (A/B comparison)
- CI integration for prompt regression detection
- Any scenario where output has identifiable keywords but not exact text

## Trade-offs

- **Pro:** Zero additional dependencies, fast (~ms), language-agnostic keywords
- **Pro:** Easy to maintain YAML datasets, human-readable
- **Con:** Keyword presence != semantic understanding (false positives possible)
- **Con:** Order-insensitive (can't verify sequence constraints)
- **Future:** Add semantic similarity tier using embeddings for higher precision
