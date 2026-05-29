---
name: learning-translation-quality
description: Assess pedagogical equivalence of translations, check terminology consistency, validate educational accuracy in target language, and measure translation quality metrics. Use when validating translated educational content. Activates on "translation quality", "pedagogical equivalence", or "translation validation".
---

# Learning Translation Quality Assurance

Assess and validate the quality of translated educational content for pedagogical equivalence and accuracy.

## When to Use

- Validating professional translations
- Quality control for localized curriculum
- Ensuring pedagogical accuracy across languages
- Maintaining terminology consistency
- Measuring translation effectiveness

## Quality Dimensions

### 1. Pedagogical Equivalence

**Beyond Linguistic Accuracy**:
- Do learning objectives translate effectively?
- Are explanations equally clear?
- Do examples work in target culture?
- Is cognitive load equivalent?
- Are scaffolding and hints preserved?

### 2. Terminology Consistency

**Educational Vocabulary**:
- Subject-specific terms used consistently
- Pedagogical terms standardized
- Assessment terminology aligned
- Glossary compliance

### 3. Educational Accuracy

**Content Integrity**:
- Mathematical/scientific accuracy maintained
- Historical facts culturally appropriate
- Technical precision preserved
- Citations and references validated

### 4. Readability and Level

**Age-Appropriate Language**:
- Reading level matches original
- Sentence complexity equivalent
- Vocabulary difficulty calibrated

## CLI Interface

```bash
/learning.translation-quality --source "course-en.md" --translation "course-es.md" --glossary "terms.json"
```

## Output

- Quality score (0-100)
- Pedagogical equivalence report
- Terminology issues flagged
- Readability comparison
- Recommendations

## Exit Codes

- **0**: Translation quality acceptable
- **1**: Critical quality issues
- **2**: Pedagogical equivalence compromised
