---
name: learning-cefr-alignment
description: Align language learning content to CEFR framework (A1-C2), design can-do statements for each proficiency level, create language assessment rubrics, and map content progression. Use for language learning curriculum. Activates on "CEFR", "language proficiency", "A1", "B2", or "language curriculum".
---

# Learning CEFR Alignment

Align language learning curriculum to the Common European Framework of Reference (CEFR) for Languages.

## When to Use

- Designing language learning courses
- Creating proficiency-based curriculum
- Assessing language learner levels
- Aligning to European standards
- Developing can-do statements

## CEFR Framework

### Proficiency Levels

**A (Basic User)**:
- **A1 (Breakthrough)**: "I can understand and use familiar everyday expressions"
- **A2 (Waystage)**: "I can communicate in simple and routine tasks"

**B (Independent User)**:
- **B1 (Threshold)**: "I can deal with most situations while travelling"
- **B2 (Vantage)**: "I can interact with a degree of fluency and spontaneity"

**C (Proficient User)**:
- **C1 (Effective Operational Proficiency)**: "I can express ideas fluently and spontaneously"
- **C2 (Mastery)**: "I can understand with ease virtually everything"

### Skill Areas

**Receptive Skills**:
- Listening comprehension
- Reading comprehension

**Productive Skills**:
- Spoken interaction
- Spoken production
- Written production

## Can-Do Descriptors

### Examples by Level

**A1 Listening**:
- Can understand familiar words and very basic phrases
- Can follow speech that is very slow and carefully articulated

**B2 Speaking**:
- Can interact with a degree of fluency and spontaneity
- Can present clear, detailed descriptions on a wide range of subjects

**C1 Writing**:
- Can express ideas fluently in clear, well-structured text
- Can write complex letters, reports, or articles

## Curriculum Mapping

### Content Progression

**Grammar Progression**:
- A1: Present simple, basic questions, personal pronouns
- A2: Past simple, future (going to), comparatives
- B1: Present perfect, conditionals, passive voice (simple)
- B2: All tenses, reported speech, advanced conditionals
- C1: Subjunctive, advanced passive, nuanced expressions
- C2: Mastery of all grammatical structures

**Vocabulary Targets**:
- A1: ~500 words
- A2: ~1,000 words
- B1: ~2,000 words
- B2: ~3,000-4,000 words
- C1: ~5,000-6,000 words
- C2: ~8,000+ words

### Topic Progression

**A Levels**: Personal information, daily routines, family, shopping, local geography
**B Levels**: Work, education, hobbies, media, current events, travel
**C Levels**: Abstract ideas, professional topics, cultural discourse, specialized fields

## Assessment Design

### CEFR-Aligned Rubrics

**Criteria by Skill**:
- Fluency and coherence
- Grammatical range and accuracy
- Lexical resource
- Pronunciation (speaking)
- Task achievement

## CLI Interface

```bash
# Align course to CEFR
/learning.cefr-alignment --content "french-course/" --level "B1" --skills "listening,speaking,reading,writing"

# Generate can-do statements
/learning.cefr-alignment --level "A2" --skill "speaking" --generate-descriptors

# Create assessment rubric
/learning.cefr-alignment --skill "writing" --levels "B1,B2" --create-rubric

# Map curriculum progression
/learning.cefr-alignment --course "spanish-curriculum/" --map-progression "A1-B2"
```

## Output

- CEFR level alignment map
- Can-do descriptors for each level
- Assessment rubrics by skill and level
- Curriculum progression guide
- Vocabulary and grammar scope & sequence

## Composition

**Input from**: `/curriculum.design`, `/learning.language-level-calibration`
**Works with**: `/curriculum.assess-design`, `/learning.multilingual-assessment`
**Output to**: CEFR-aligned language curriculum

## Exit Codes

- **0**: CEFR alignment complete
- **1**: Content doesn't match specified level
- **2**: Insufficient language content
