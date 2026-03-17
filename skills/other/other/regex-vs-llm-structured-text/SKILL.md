---
name: regex-vs-llm-structured-text
description: "Use when parsing structured text (quizzes, forms, documents). Start with regex, add LLM only for low-confidence edge cases."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-14"
---
# Skill: Regex vs LLM for Structured Text Parsing

## Pattern Recognition
When parsing structured text (e.g., quiz questions, forms, documents):

1. **Start with Regex** - For well-defined patterns, regex achieves 98%+ accuracy
2. **Add Confidence Scoring** - Identify low-confidence extractions programmatically
3. **Use LLM only for edge cases** - Reserve expensive LLM calls for <5% of data

## Proven Metrics (G検定 Quiz Parser)

| Metric | Value |
|--------|-------|
| Total Questions | 410 |
| Regex Success Rate | 98.0% |
| Low Confidence (<0.95) | 8 (2.0%) |
| LLM Required | ~5 questions |
| Test Coverage | 93% |

## Architecture Pattern

```
Source Text
    ↓
[Regex Parser] ─── 100% structure extraction
    ↓
[Text Cleaner] ─── Remove noise (markers, page numbers)
    ↓
[Confidence Scorer] ─── Flag low-confidence items
    │
    ├── High (≥0.95) → Direct output
    │
    └── Low (<0.95) → [LLM Validator] → Output
```

## Text Cleaning Rules Learned

| Pattern | Action |
|---------|--------|
| `（解 問答 題）` | Remove (section marker) |
| `第N章` in text | Remove (chapter reference) |
| `[解答Nを参照]` | Remove (footnote) |
| Stray page numbers (`心理効 17 果`) | Remove |
| `（A）（B）` etc. | Add newline before |

## Key Insights

1. **Confidence Flags**:
   - `few_choices`: Less than 4 choices extracted
   - `missing_answer`: No correct answer found
   - `short_explanation`: Explanation too brief (<50 chars)

2. **TDD Approach** worked well:
   - Write tests first (RED)
   - Implement minimal code (GREEN)
   - Achieved 90%+ coverage

3. **Immutability Pattern**:
   - Never mutate Question objects
   - Return new instances from clean_question()

## When to Apply This Skill

- Quiz/exam question parsing
- Form data extraction
- Document structure parsing
- Any structured text with repeating patterns

## Answer Validation Pattern

For verifying answer consistency between explanation and declared answer:

```python
from answer_validator import generate_inconsistency_report

report = generate_inconsistency_report(questions)
# Valid: Explanation matches answer
# Invalid: Explanation suggests different answer
# Uncertain: Cannot determine from explanation
```

**Patterns detected**:
- `正解はX` / `答えはX` (explicit answer declaration)
- `Xが正解` / `Xが正しい` (answer assertion)
- `Xが適切` (appropriate choice)

**Label normalization**: ア→A, イ→B, ウ→C, エ→D

## Files Created

```
Scripts/
├── text_cleaner.py          # Text cleaning functions
├── confidence_scorer.py     # Confidence scoring
├── llm_validator.py         # LLM validation (mock-ready)
├── hybrid_parser.py         # Integration pipeline
├── answer_validator.py      # Answer consistency checking
└── tests/
    ├── test_text_cleaner.py
    ├── test_confidence_scorer.py
    ├── test_llm_validator.py
    ├── test_hybrid_parser.py
    └── test_answer_validator.py
```

## Usage Example

```python
from question_parser import parse_questions_file
from text_cleaner import clean_question
from confidence_scorer import identify_low_confidence_questions

# Parse
result = parse_questions_file(source_path)

# Clean
cleaned = [clean_question(q) for q in result.questions]

# Identify issues
low_conf = identify_low_confidence_questions(cleaned)
print(f"Need review: {len(low_conf)} questions")
```

---

**Created**: 2026-02-05
**Project**: g-kentei-ios-hybrid
**Session**: TDD Hybrid Parser Implementation
