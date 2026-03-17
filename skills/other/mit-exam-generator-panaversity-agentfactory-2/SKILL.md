---
name: mit-exam-generator
description: |
  Generate rigorous MIT PhD-level qualifying examinations from Markdown/Obsidian notes.
  This skill should be used when users request quiz creation, exam generation, assessment
  materials, practice questions, or study guides. Triggers on "create quiz", "generate exam",
  "make practice questions", "assessment", "test me on", or any request for educational
  testing materials from source content.
---

# MIT PhD Qualifying Exam Generator

Generate rigorous academic assessments from structured Markdown content.

## What This Skill Does

- Generates 200-question PhD qualifying exams from Markdown/Obsidian notes
- Scales question count proportionally for sparse content
- Auto-detects difficulty from content complexity
- Merges multiple source documents with weighted question distribution
- Validates answer distribution, difficulty spread, and source coverage

## What This Skill Does NOT Do

- Process PDFs, images, or non-Markdown formats
- Generate answer explanations with direct quotes (exam integrity)
- Create exams from external web content
- Provide answer keys without completing the full exam

---

## Required Clarifications

Before generating, clarify with user:

| Question | Options | Default |
|----------|---------|---------|
| **Multi-doc strategy** | Merge thematically / Separate sections per source | Merge thematically |
| **Difficulty emphasis** | Balanced / Favor higher levels / Favor foundational | Balanced |
| **Include timing guidance** | Yes (with per-section time) / No | Yes |

### Optional Clarifications

Ask only if relevant:
- Custom question count override?
- Specific sections to emphasize or exclude?
- Target audience adjustment (undergrad vs PhD)?

### If User Doesn't Respond

Use defaults and note assumptions in exam header:
```
**Assumptions:** Merged thematically, balanced difficulty, standard timing
```

---

## Before Implementation

| Source | Gather |
|--------|--------|
| **Source Files** | Read all specified Markdown files completely |
| **Content Depth** | Assess complexity for difficulty calibration |
| **Key Concepts** | Extract testable facts, definitions, relationships |
| **Section Structure** | Map headings for source references |

---

## Exam Specifications

| Parameter | Standard | Scaled (Sparse) |
|-----------|----------|-----------------|
| **Questions** | 200 | Min 25, proportional to content |
| **Duration** | 180 min | 15 min per 25 questions |
| **Points** | 1 per question | Same |

### Grading Scale

| Grade | % | Classification |
|-------|---|----------------|
| A+ | 95-100 | Exceptional - PhD qualifying |
| A | 90-94.99 | Strong mastery |
| B+ | 85-89.99 | Good foundation |
| B | 80-84.99 | Satisfactory |
| C | 70-79.99 | Marginal pass |
| F | <70 | Fail - Retake required |

---

## Generation Workflow

```
1. ANALYZE
   └── Read source files → Extract concepts → Map sections
   └── Calculate: content_density = concepts / sections

2. CALIBRATE
   └── question_count = min(200, concepts * 2)
   └── difficulty_profile = analyze_complexity(content)

3. DISTRIBUTE
   └── Allocate questions by type (see references/question-patterns.md)
   └── Allocate by Bloom's level (see references/bloom-taxonomy.md)
   └── Weight by source document size (multi-doc)

4. GENERATE
   └── Create questions following type patterns
   └── Ensure distractors are plausible (70-90% correct)
   └── Track source section for each question

5. VALIDATE
   └── Run all checks (see references/validation-rules.md)
   └── Fix any failures before delivery

6. OUTPUT
   └── Save to exam-[source-name].md alongside source
```

---

## Question Type Distribution

| Type | % | Purpose |
|------|---|---------|
| Precision Recall | 10 | Exact values, definitions |
| Conceptual Distinction | 15 | Paired/contrasting concepts |
| Decision Matrix | 12.5 | Multi-criteria scenarios |
| Architecture Analysis | 12.5 | System components, flows |
| Economic/Quantitative | 10 | Calculations, comparisons |
| Specification Design | 10 | Framework application |
| Critical Evaluation | 12.5 | Trade-offs, judgments |
| Strategic Synthesis | 10 | Multi-concept integration |
| Research Extension | 7.5 | Novel scenario extrapolation |

See `references/question-patterns.md` for templates and examples.

---

## Bloom's Taxonomy Distribution

| Level | % | Question Characteristics |
|-------|---|--------------------------|
| Remember/Understand | 25 | Recall facts, explain concepts |
| Apply | 20 | Use in new situations |
| Analyze | 25 | Break down, compare, contrast |
| Evaluate | 18 | Judge, critique, justify |
| Create/Synthesize | 12 | Design, propose, integrate |

See `references/bloom-taxonomy.md` for level indicators.

---

## Answer Construction Rules

1. **Option A**: Never "All/None of the above"
2. **Correct Answer**: One clearly correct option
3. **Distractors**: Plausible but fail on critical detail (70-90% correct)
4. **Distribution**: Roughly equal A:B:C:D across exam
5. **Sequences**: No more than 3 consecutive same-letter answers

---

## Multi-Document Handling

When multiple source files provided:

```
weight[doc] = word_count[doc] / total_word_count
questions[doc] = round(total_questions * weight[doc])
```

Create distinct sections per source or merge thematically (user preference).

---

## Output Format

```markdown
# [Exam Title]
## MIT PhD Qualifying Examination

**Source:** [file(s)]
**Questions:** [N]
**Duration:** [X] minutes
**Generated:** [date]

---

### PART A: [Topic] ([X] Questions)

**Q1.** [Question stem]
A) [Option]
B) [Option]
C) [Option]
D) [Option]

[Continue all questions...]

---

## ANSWER KEY

| Q# | Ans | Section | Difficulty | Bloom |
|----|-----|---------|------------|-------|
| 1 | C | Part A | Medium | Apply |

---

## EXPLANATIONS

### Q1
**Correct: C**
[Explanation with section reference - NO direct quotes]
Section: [Heading from source]
```

---

## Scaling Algorithm

```python
def calculate_questions(content):
    concepts = extract_testable_concepts(content)

    if len(concepts) >= 100:
        return 200  # Full exam
    elif len(concepts) >= 50:
        return 100  # Half exam
    elif len(concepts) >= 25:
        return 50   # Quarter exam
    else:
        return max(25, len(concepts))  # Minimum viable
```

---

## Edge Case Handling

| Situation | Action |
|-----------|--------|
| **Conflicting info in source** | Flag in exam notes; create question testing the distinction |
| **Ambiguous concepts** | Skip or ask user for clarification before generating |
| **Too few testable facts** | Scale down; warn user if <25 questions possible |
| **Highly technical jargon** | Include definition in question stem if needed |
| **Multiple valid interpretations** | Avoid or phrase as "According to [source]..." |
| **Source has errors** | Do not correct; test what source states (note discrepancy) |

---

## Validation Pipeline

Run ALL checks before delivery. See `references/validation-rules.md`.

### Quick Checklist

- [ ] Question count matches calculated target
- [ ] Each question has exactly 4 options (A-D)
- [ ] Answer distribution within 20-30% per letter
- [ ] No >3 consecutive same-letter answers
- [ ] All Bloom levels represented per distribution
- [ ] All question types represented per distribution
- [ ] Every question has section reference
- [ ] No direct quotes in explanations
- [ ] Difficulty distribution matches content complexity

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/question-patterns.md` | Templates for each question type |
| `references/bloom-taxonomy.md` | Cognitive level classification |
| `references/validation-rules.md` | Quality validation criteria |
