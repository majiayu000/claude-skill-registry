---
name: spacy
description: spaCy NLP library with pipelines. Use for text processing.
---

# spaCy

spaCy is "Industrial Strength" NLP. Unlike NLTK (academic), spaCy focuses on providing the **best** single algorithm for a task. v3.8 supports Python 3.13.

## When to Use

- **NER (Named Entity Recognition)**: Extracting person names, dates, orgs.
- **Parsing**: Dependency parsing to understand sentence structure.
- **Speed**: Cython-optimized pipelines.

## Core Concepts

### Pipeline

Tokenizer -> Tagger -> Parser -> NER.

### Doc / Token / Span

The core data structures. Efficient memory usage.

### Prodigy

The annotation tool (paid) from the same creators, tightly integrated.

## Best Practices (2025)

**Do**:

- **Use Transformer pipelines**: `en_core_web_trf` (Roberta-based) for high accuracy.
- **Use `nlp.pipe()`**: For batch processing huge texts.

**Don't**:

- **Don't use for GenAI**: spaCy is for structure extraction, not text generation (LLMs).

## References

- [spaCy Documentation](https://spacy.io/)
