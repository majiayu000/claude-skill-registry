---
name: nltk
description: NLTK natural language toolkit. Use for NLP.
---

# NLTK

NLTK is the classic library for teaching and researching NLP. While slower than spaCy, it offers **comprehensive** linguistic data.

## When to Use

- **Education**: Learning how tokenizers or stemmers work from scratch.
- **Lexical Resources**: Access to WordNet, FrameNet, and huge corpora.
- **Low-level Text Processing**: Porter/Snowball stemmers.

## Core Concepts

### Corpora

`nltk.download('gutenberg')`. Access to classic texts.

### Tokenization

Splitting text into words/sentences.

## Best Practices (2025)

**Do**:

- **Use for Education**: Excellent for linguistics classes.
- **Use for Lexical Lookups**: WordNet interface is still useful.

**Don't**:

- **Don't use in Production**: Use spaCy or Hugging Face. NLTK is slow and string-based.

## References

- [NLTK Documentation](https://www.nltk.org/)
