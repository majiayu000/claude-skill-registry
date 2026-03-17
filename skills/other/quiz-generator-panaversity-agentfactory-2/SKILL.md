---
name: quiz-generator
description: Generate 50-question interactive quizzes using the Quiz component with randomized batching. Use when creating end-of-chapter assessments. Displays 15-20 questions per session with immediate feedback. NOT for static markdown quizzes.
allowed-tools: Bash, Read, Write
---

# Quiz Generator

## Quick Start

```bash
# 1. Generate 50 questions for chapter
# Focus on conceptual (75%+ Apply level), not recall

# 2. Redistribute answers evenly
python scripts/redistribute_answers_v2.py quiz.md A

# 3. Validate option lengths (±3 words per question)
# Manually count words for ALL 50 questions
```

## Persona

You generate college-level conceptual quizzes that test understanding, not memorization. Your goal is 50 comprehensive questions covering all chapter concepts with immediate feedback per answer.

## Fixed Constraints

```yaml
question_count: 50  # Comprehensive bank
questions_per_batch: 15-20  # Displayed per session
options_per_question: 4  # Always exactly 4
correct_answer_distribution: ~12-13 per index (0-3)
feedback_timing: immediate  # After each answer
passing_score: NONE  # No threshold
file_naming: ##_chapter_##_quiz.md
```

## Analysis Questions

### 1. Is this conceptual (not recall)?

| Type | Example | Valid? |
|------|---------|--------|
| Recall | "What is a Python list?" | ❌ |
| Conceptual | "Which operation reveals a mutability issue?" | ✅ |

**Target**: 75%+ at Apply level or higher

### 2. Are options equal length (±3 words)?

| Options | Words | Valid? |
|---------|-------|--------|
| A: "Yes" / B: "It processes async" | 2 vs 4 | ✅ |
| A: "Yes" / B: "The framework processes requests asynchronously" | 2 vs 6 | ❌ |

**Rule**: ALL options within ±3 words to prevent pattern-guessing

### 3. Are answers evenly distributed?

| Index | Count | Valid? |
|-------|-------|--------|
| 0 | 12-13 | ✅ |
| 1 | 12-13 | ✅ |
| 2 | 12-13 | ✅ |
| 3 | 12-13 | ✅ |

**Rule**: No 3+ consecutive same index, no obvious patterns

## Principles

### Principle 1: 50 Questions Required

- Comprehensive coverage (all chapter concepts)
- Spaced repetition (different questions each retake)
- Component shuffles and displays 15-20 per session

### Principle 2: Immediate Feedback

Show after EACH answer (not at end):
- ✅ Correct option highlighted (green)
- ❌ Why wrong (if incorrect)
- Explanation (100-150 words)

### Principle 3: Address All Options

Every explanation must cover:
1. Why correct is correct (2-3 sentences)
2. Why each distractor is wrong (1-2 sentences × 3)
3. Real-world connection (1-2 sentences)

### Principle 4: Source Attribution

```javascript
source: "Lesson 1: Understanding Mutability"
```

Links each question to specific lesson for review.

## Quiz Component Format

```markdown
---
sidebar_position: 5
title: "Chapter X: [Topic] Quiz"
---

# Chapter X Quiz

Brief intro (1-2 sentences).

<Quiz
  title="Chapter X Assessment"
  questions={[
    {
      question: "Conceptual question here?",
      options: [
        "Option A (4-6 words)",
        "Option B (4-6 words)",
        "Option C (4-6 words) ← CORRECT",
        "Option D (4-6 words)"
      ],
      correctOption: 2,  // Index 0-3, NOT 1-4!
      explanation: "Why C is correct (2-3 sentences). Why A is wrong (1-2 sentences). Why B is wrong. Why D is wrong. Real-world connection.",
      source: "Lesson 1: Topic Title"
    },
    // ... 49 more questions (total: 50)
  ]}
  questionsPerBatch={18}
/>
```

## Answer Redistribution

LLMs struggle with even distribution. Use the script after generation:

```bash
python scripts/redistribute_answers_v2.py quiz.md A
```

**Sequences A-H** provide different distributions (~12-13 per index).

**What it does**:
1. Parses quiz questions
2. Swaps option positions to match sequence
3. Updates explanations to reference new positions
4. Validates all explanations match correct answers

## Option Length Validation (CRITICAL)

**Problem**: Unequal lengths let students guess by picking longest/shortest.

**Solution**: Manually count words for EVERY option in EVERY question.

```
✅ PASS: 4, 5, 4, 5 words (all within ±3)
❌ FAIL: 2, 4, 11, 3 words (2 to 11 = 9-word spread)
```

**Also verify**:
- Longest option correct in ~25% (not biased)
- Shortest option correct in ~25% (not biased)

## Common Pitfalls

| Pitfall | Wrong | Right |
|---------|-------|-------|
| Question count | <50 questions | Exactly 50 |
| Index values | `correctOption: 4` | `correctOption: 3` (0-3) |
| Missing source | No source field | `source: "Lesson N: Title"` |
| Passing score | `passingScore={70}` | No prop (removed) |
| Recall questions | "What is X?" | "Which reveals X issue?" |
| Weak explanations | Only explains correct | Addresses all 4 options |
| Answer patterns | 0,1,2,3,0,1,2,3... | Random, ~12-13 per index |
| Option lengths | 2 vs 11 words | All within ±3 words |

## File Naming

**Pattern**: `##_chapter_##_quiz.md`

| Chapter | Lessons | Filename |
|---------|---------|----------|
| 2 | 4 | `05_chapter_02_quiz.md` |
| 5 | 6 | `07_chapter_05_quiz.md` |
| 14 | 5 | `06_chapter_14_quiz.md` |

## Handoff Checklist

**Content**:
- [ ] 50 questions (not fewer)
- [ ] 75%+ Apply level or higher
- [ ] All major topics covered
- [ ] No recall questions

**Distribution**:
- [ ] correctOption uses 0-3 (not 1-4)
- [ ] ~12-13 per index
- [ ] No 3+ consecutive same index

**Option Lengths**:
- [ ] ALL options counted (all 50 questions)
- [ ] ALL within ±3 words
- [ ] Longest not biased toward correct
- [ ] Shortest not biased toward correct

**Explanations**:
- [ ] 100-150 words each
- [ ] Explains why correct
- [ ] Addresses each distractor
- [ ] Real-world connection

**Format**:
- [ ] Valid JSX syntax
- [ ] Exactly 4 options per question
- [ ] `source` field on all 50
- [ ] NO `passingScore` prop
- [ ] File named correctly

## If Verification Fails

1. Run redistribution script: `python scripts/redistribute_answers_v2.py quiz.md A`
2. Re-count option lengths manually
3. Check explanation references match correctOption
4. **Stop and report** if issues persist after 2 attempts
