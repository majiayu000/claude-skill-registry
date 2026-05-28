---
name: learning-glossary-management
description: Create multilingual glossaries for educational content, maintain terminology consistency across translations, build translation memory databases, and define preferred terms by domain and region. Use when managing translation terminology. Activates on "glossary", "terminology management", or "translation memory".
---

# Learning Glossary Management

Create and maintain multilingual glossaries and terminology databases for consistent educational translations.

## When to Use

- Starting translation projects
- Maintaining terminology across courses
- Ensuring consistent translations
- Building translation memory
- Domain-specific vocabulary management

## Key Functions

### 1. Glossary Creation

**Extract Key Terms**:
- Subject-specific vocabulary
- Pedagogical terminology
- Assessment terms
- Platform/UI terms
- Institution-specific terms

### 2. Multilingual Mapping

**Term Relationships**:
- One source term → multiple target terms
- Context-dependent translations
- Regional variations
- Forbidden translations

### 3. Translation Memory

**Reusable Segments**:
- Sentence-level translations
- Paragraph-level matches
- Context preservation
- Quality ratings

## CLI Interface

```bash
/learning.glossary-management --content "course/" --languages "en,es,fr,de" --domain "mathematics"
```

## Output

- Multilingual glossary database
- Translation memory (.tmx format)
- Terminology guidelines
- Consistency reports

## Exit Codes

- **0**: Glossary created successfully
- **1**: Insufficient content for extraction
- **2**: Language pair not supported
