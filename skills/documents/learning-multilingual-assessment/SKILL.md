---
name: learning-multilingual-assessment
description: Design assessments that work across languages, avoid language-dependent cultural bias, support multilingual learners, and validate assessment equivalence across translations. Use when creating fair assessments for multilingual contexts. Activates on "multilingual assessment", "language-fair testing", or "assessment translation".
---

# Learning Multilingual Assessment

Design fair, valid assessments that work effectively across languages and for multilingual learners.

## When to Use

- International testing programs
- Multilingual classroom assessments
- ELL/ESL student assessment
- Translated assessments
- Global certification exams

## Key Challenges

### Language-Dependent Bias

**Sources of Bias**:
- Complex vocabulary unnecessary for content
- Culture-specific scenarios
- Idioms and figurative language
- Text-heavy questions
- Reading speed requirements

### Assessment Translation

**Challenges**:
- Linguistic equivalence ≠ difficulty equivalence
- Some concepts harder to express in certain languages
- Test length varies by language
- Reading time differences

### Multilingual Learner Support

**Considerations**:
- Content knowledge vs. language proficiency
- Accommodations without compromising validity
- Fair comparison across language groups

## Design Principles

### 1. Reduce Language Load

**Strategies**:
- Use simple, direct language
- Short sentences and paragraphs
- Visual supports (diagrams, charts, images)
- Minimize unnecessary text
- Concrete > abstract language
- Active voice > passive voice

### 2. Avoid Cultural Bias

**Review for**:
- Cultural scenarios (unfamiliar contexts)
- Regional references (geography, events, people)
- Socioeconomic assumptions
- Holiday/calendar references
- Food, sports, leisure activities

### 3. Universal Design

**Accessibility Features**:
- Glossaries for technical terms
- Bilingual glossaries
- Extended time options
- Translation tools (for instructions, not content)
- Text-to-speech support

### 4. Multiple Modalities

**Beyond Text**:
- Visual representations
- Interactive elements
- Demonstrations
- Hands-on performance tasks
- Oral assessment options

## Translation Guidelines

### Equivalence Types

**Linguistic Equivalence**: Word-for-word accuracy
**Functional Equivalence**: Same meaning, different words
**Psychometric Equivalence**: Same difficulty across languages

### Translation Process

1. Forward translation by subject expert
2. Backward translation to verify
3. Reconciliation of differences
4. Pilot testing in target language
5. Difficulty analysis and adjustment
6. Cultural review

### Validation

**Field Testing**:
- Differential item functioning (DIF) analysis
- Compare difficulty across languages
- Identify biased items
- Adjust or remove problematic items

## Accommodations

### Linguistic Supports

**Allowed Accommodations**:
- ✓ Bilingual glossaries (mathematics terms)
- ✓ Extra time
- ✓ Simplified language instructions
- ✓ Test directions in native language
- ✓ Clarification of test directions

**Generally Not Allowed**:
- ✗ Translation of test items (depends on purpose)
- ✗ Side-by-side bilingual tests (for language assessments)

## CLI Interface

```bash
# Design language-fair assessment
/learning.multilingual-assessment --content "math-test/" --reduce-language-load --output fair-test.md

# Validate translation equivalence
/learning.multilingual-assessment --source "test-en.json" --translations "test-es.json,test-zh.json" --validate-equivalence

# Design with accommodations
/learning.multilingual-assessment --assessment "science-exam/" --accommodations "glossary,extended-time,visual-supports"

# Cultural bias review
/learning.multilingual-assessment --test "reading-test/" --bias-check --cultures "Hispanic,East Asian,Middle Eastern"
```

## Output

- Language-fair assessment design
- Translation guidelines
- Cultural bias analysis
- Accommodation recommendations
- Validation protocols
- Equivalence reports

## Composition

**Input from**: `/curriculum.assess-design`, `/learning.translation-quality`
**Works with**: `/learning.cultural-adaptation`, `/learning.language-level-calibration`
**Output to**: Fair, valid multilingual assessments

## Exit Codes

- **0**: Multilingual assessment designed
- **1**: Excessive language dependence
- **2**: Cultural bias detected
- **3**: Translation equivalence compromised
