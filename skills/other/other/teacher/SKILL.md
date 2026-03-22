---
name: teacher
description: Fast-track course setup for someone with learning targets ready. Efficient workflow, batch assessment, minimal explanation.
license: MIT
metadata:
  author: Andamio
  version: 1.0.0
---

# Pathway: Teacher

You're working with an expert who has learning targets ready or nearly ready. Be efficient and respectful. Move fast.

## Instructions

### 1. Accept SLTs

```
Ready when you are. Paste your SLTs, point me to a file, or describe
what you have.
```

If the user provides SLTs:
- Quick format check — reformat to "I can [verb] [object] by [evidence]" if needed
- Fix quietly, note what you changed

If the user provides outcomes that aren't SLTs yet:
- Convert them, show the conversion, confirm

### 2. Assess Quality

Read and follow the instructions in `skills/assess-slts/SKILL.md`. Present results concisely:

```
| # | SLT | Quality | Notes |
|---|-----|---------|-------|
| 1 | I can... | Strong | — |
| 2 | I can... | Needs refinement | Suggest: "I can... by..." |
```

Fix what the user agrees with. Move on.

### 3. Classify Lesson Types

Read and follow the instructions in `skills/classify-lesson-types/SKILL.md`. Present all classifications at once:

```
| # | SLT | Lesson Type | Confidence |
|---|-----|-------------|------------|
| 1 | I can... | Product Demo | High |
| 2 | I can... | Developer Documentation | High |
| 3 | I can... | How To Guide | Medium |

Agree? Or override any of these?
```

Apply overrides.

### 4. Assess Readiness

Read and follow the instructions in `skills/self-assess-readiness/SKILL.md`.

### 5. Hand Off

Save all artifacts:
- SLTs to `01-slts.md`
- Quality review to `02-slts-quality-review.md`
- Classification to `03-lesson-type-classification.md`
- Readiness to `04-readiness-assessment.md`

"Everything's assessed. Let's build."

Read and follow the instructions in `skills/course-workflow/SKILL.md`, starting at the `readiness-assessed` status.
