---
name: dspy-output-refinement-constraints
version: "1.0.0"
dspy-compatibility: "3.1.2"
description: This skill should be used when the user asks to "refine DSPy outputs", "enforce constraints", "use dspy.Refine", "select best output", "use dspy.BestOfN", mentions "output validation", "constraint checking", "multi-attempt generation", "reward function", or needs to improve output quality through iterative refinement or best-of-N selection with custom constraints.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# DSPy Output Refinement & Constraints

## Goal

Improve output quality using iterative refinement (dspy.Refine) and best-of-N selection (dspy.BestOfN) with custom constraint validation.

## When to Use

- Outputs need format validation (JSON, specific structure)
- Length constraints (max tokens, word count)
- Content requirements (must include X, avoid Y)
- Quality improvement through multiple attempts
- Replacing deprecated Assert/Suggest patterns

## Related Skills

- Design signatures: [dspy-signature-designer](../dspy-signature-designer/SKILL.md)
- Optimize programs: [dspy-miprov2-optimizer](../dspy-miprov2-optimizer/SKILL.md)
- Evaluate quality: [dspy-evaluation-suite](../dspy-evaluation-suite/SKILL.md)

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| `module` | `dspy.Module` | Module to refine |
| `reward_fn` | `callable` | Constraint validation function |
| `N` | `int` | Number of attempts |
| `threshold` | `float` | Minimum reward to accept |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `refined_output` | `dspy.Prediction` | Validated, refined result |

## Workflow

### Phase 1: dspy.Refine for Iterative Improvement

Refine iteratively improves outputs across multiple attempts:

```python
import dspy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

# Base module
summarizer = dspy.ChainOfThought("document -> summary: str")

# Reward function: checks constraints
def summary_reward(args, pred):
    summary = pred.summary
    word_count = len(summary.split())

    if word_count > 100 or len(summary) < 50:
        return 0.0
    if "important" not in summary.lower():
        return 0.5
    return 1.0

# Refine module
refined_summarizer = dspy.Refine(
    module=summarizer,
    reward_fn=summary_reward,
    N=3,
    threshold=1.0
)

# Use it
result = refined_summarizer(document="Long document text here...")
print(result.summary)
```

### Phase 2: dspy.BestOfN for Selection

Generate N outputs and pick the best:

```python
import dspy

def json_reward(args, pred):
    """Validate JSON format and fields."""
    import json
    try:
        data = json.loads(pred.output)
        if not {'name', 'age', 'email'}.issubset(data.keys()):
            return 0.3
        if '@' not in data.get('email', ''):
            return 0.5
        return 1.0
    except json.JSONDecodeError:
        return 0.0

# BestOfN: try 5 times, pick best
extractor = dspy.Predict("text -> output: str")
best_extractor = dspy.BestOfN(module=extractor, reward_fn=json_reward, N=5, threshold=1.0)

result = best_extractor(text="John Doe, 30 years old, john@example.com")
print(result.output)  # Best valid JSON
```

### Phase 3: Multi-Constraint Reward Functions

Complex validation with scoring:

```python
import dspy
import re

def comprehensive_reward(args, pred):
    """Validate format, length, and content."""
    text = pred.answer
    score = 0.0

    # Length: 50-150 words (33%)
    word_count = len(text.split())
    if 50 <= word_count <= 150:
        score += 0.33

    # Format: capitalized, ends with period (33%)
    if re.match(r'^[A-Z]', text) and text.endswith('.'):
        score += 0.33

    # Content: required terms present (34%)
    if all(term in text.lower() for term in ['data', 'analysis']):
        score += 0.34

    return score

# Use with Refine
qa = dspy.ChainOfThought("question -> answer: str")
refined_qa = dspy.Refine(module=qa, reward_fn=comprehensive_reward, N=4, threshold=0.9)

result = refined_qa(question="What is data science?")
```

## Production Example

```python
import dspy
import json
import logging

logger = logging.getLogger(__name__)

class StructuredExtractor(dspy.Module):
    """Extract structured data with validation."""

    def __init__(self):
        self.extractor = dspy.Predict(
            "text -> json_output: str"
        )
        self.refined = dspy.Refine(
            module=self.extractor,
            reward_fn=self.validation_reward,
            N=3,
            threshold=0.9
        )

    def validation_reward(self, args, pred):
        """Validate JSON structure and business logic."""
        try:
            data = json.loads(pred.json_output)
            score = 0.0

            # Required fields
            if {'product', 'price', 'quantity'}.issubset(data.keys()):
                score += 0.4

            # Type validation
            if isinstance(data.get('price'), (int, float)) and data['price'] > 0:
                score += 0.3
            if isinstance(data.get('quantity'), int) and data['quantity'] > 0:
                score += 0.3

            return score
        except (json.JSONDecodeError, TypeError) as e:
            logger.warning(f"Validation failed: {e}")
            return 0.0

    def forward(self, text: str):
        try:
            return self.refined(text=text)
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            return dspy.Prediction(json_output='{}')

# Usage
extractor = StructuredExtractor()
result = extractor(text="iPhone 15, $999, quantity: 50")
print(result.json_output)
```

## Migration from Assert/Suggest

DSPy 2.6+ deprecates `dspy.Assert`/`dspy.Suggest`. Use Refine with reward functions:

```python
# Old: dspy.Assert(len(output) < 100, "Too long")
# New:
def reward(args, pred):
    return 1.0 if len(pred.output) < 100 else 0.0

refined = dspy.Refine(module=module, reward_fn=reward, N=3, threshold=1.0)
```

## Best Practices

1. **Score gradually** - Use 0.0-1.0 range, not binary pass/fail
2. **Multiple constraints** - Weight each constraint (e.g., 25% each for 4 checks)
3. **Handle exceptions** - Reward functions should never raise, return 0.0 on error
4. **Limit attempts** - 3-5 attempts for Refine, 5-10 for BestOfN
5. **Log failures** - Track which constraints fail most often

## Limitations

- Each attempt costs an additional LLM call
- Reward functions don't receive feedback prompts (unlike GEPA)
- BestOfN is expensive (N × cost)
- No automatic constraint learning (manual reward design)
- Refine may not improve if base module is fundamentally wrong

## Official Documentation

- **DSPy Documentation**: https://dspy.ai/
- **DSPy GitHub**: https://github.com/stanfordnlp/dspy
- **Refine Module**: https://dspy.ai/api/modules/Refine/
