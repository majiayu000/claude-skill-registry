---
name: nlp-processing
description: "Process and analyze natural language using modern NLP techniques. Use for text classification, named entity recognition, sentiment analysis, tokenization, embeddings, transformers (BERT, GPT), and language understanding tasks."
---

# NLP Processing

Process and analyze natural language using modern techniques and transformer models.

## Overview

Natural Language Processing enables computers to understand, interpret, and generate human language. This skill covers fundamental techniques through state-of-the-art transformer models.

## Quick Reference

| Scenario | Recommended Approach | Reference File |
|----------|---------------------|----------------|
| Text preprocessing and tokenization | Cleaning, normalization, tokenization | `/references/preprocessing.md` |
| Text classification and sentiment analysis | Fine-tuned transformers or classical ML | `/references/classification.md` |
| Named entities, POS tagging, parsing | Sequence labeling with transformers | `/references/sequence-labeling.md` |
| Embeddings and semantic similarity | Sentence transformers, BERT embeddings | `/references/embeddings.md` |

## Core Principles

1. **Tokenization** - Split text into meaningful units
2. **Representation** - Convert text to numerical vectors
3. **Context** - Capture word meaning from surrounding words
4. **Transfer Learning** - Leverage pre-trained models
5. **Fine-Tuning** - Adapt models to specific tasks

## NLP Pipeline

### 1. Preprocessing
- Lowercasing, removing special characters
- Tokenization (word, subword, character)
- Stopword removal (task-dependent)
- Lemmatization or stemming

### 2. Representation
- Word embeddings (Word2Vec, GloVe)
- Contextual embeddings (BERT, RoBERTa)
- Sentence embeddings (Sentence-BERT)

### 3. Modeling
- Classical: Naive Bayes, SVM, Random Forest
- Deep Learning: RNNs, LSTMs, Transformers
- Pre-trained: BERT, GPT, T5

### 4. Post-processing
- Decoding, formatting
- Confidence scoring
- Error handling

## Key Tasks

**Text Classification:**
- Sentiment analysis
- Topic classification
- Intent detection
- Spam detection

**Sequence Labeling:**
- Named Entity Recognition (NER)
- Part-of-Speech (POS) tagging
- Chunking

**Text Generation:**
- Summarization
- Translation
- Question answering
- Dialogue systems

## Using the Reference Files

**`/references/preprocessing.md`** — Text cleaning, tokenization methods (word, subword, BPE), normalization, and handling special cases.

**`/references/classification.md`** — Text classification approaches, sentiment analysis, fine-tuning BERT/RoBERTa, evaluation metrics.

**`/references/sequence-labeling.md`** — NER, POS tagging, chunking, CRF layers, and sequence labeling with transformers.

**`/references/embeddings.md`** — Word2Vec, GloVe, BERT embeddings, Sentence-BERT, semantic similarity, and embedding fine-tuning.

## Best Practices

- Use pre-trained transformers when possible
- Fine-tune on domain-specific data
- Handle class imbalance appropriately
- Use appropriate tokenization for your model
- Validate on diverse test sets
- Monitor for bias in predictions
- Consider computational constraints
- Document preprocessing steps

## Common Pitfalls to Avoid

- Over-preprocessing (removing useful information)
- Not handling out-of-vocabulary words
- Ignoring class imbalance
- Using wrong tokenizer for model
- Not validating on diverse data
- Overfitting to small datasets
- Ignoring computational costs
- Not considering model bias

