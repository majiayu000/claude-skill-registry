---
name: nlp-pipeline-builder
description: |
  Natural language processing ML pipelines for text classification, NER, sentiment analysis, text generation, and embeddings. Activates for "nlp", "text classification", "sentiment analysis", "named entity recognition", "BERT", "transformers", "text preprocessing", "tokenization", "word embeddings". Builds NLP pipelines with transformers, integrated with SpecWeave increments.
---

# NLP Pipeline Builder

## Overview

Specialized ML pipelines for natural language processing. Handles text preprocessing, tokenization, transformer models (BERT, RoBERTa, GPT), fine-tuning, and deployment for production NLP systems.

## NLP Tasks Supported

### 1. Text Classification

```python
from specweave import NLPPipeline

# Binary or multi-class text classification
pipeline = NLPPipeline(
    task="classification",
    classes=["positive", "negative", "neutral"],
    increment="0042"
)

# Automatically configures:
# - Text preprocessing (lowercase, clean)
# - Tokenization (BERT tokenizer)
# - Model (BERT, RoBERTa, DistilBERT)
# - Fine-tuning on your data
# - Inference pipeline

pipeline.fit(train_texts, train_labels)
```

### 2. Named Entity Recognition (NER)

```python
# Extract entities from text
pipeline = NLPPipeline(
    task="ner",
    entities=["PERSON", "ORG", "LOC", "DATE"],
    increment="0042"
)

# Returns: [(entity_text, entity_type, start_pos, end_pos), ...]
```

### 3. Sentiment Analysis

```python
# Sentiment classification (specialized)
pipeline = NLPPipeline(
    task="sentiment",
    increment="0042"
)

# Fine-tuned for sentiment (positive/negative/neutral)
```

### 4. Text Generation

```python
# Generate text continuations
pipeline = NLPPipeline(
    task="generation",
    model="gpt2",
    increment="0042"
)

# Fine-tune on your domain-specific text
```

## Best Practices for NLP

### Text Preprocessing

```python
from specweave import TextPreprocessor

preprocessor = TextPreprocessor(increment="0042")

# Standard preprocessing
preprocessor.add_steps([
    "lowercase",
    "remove_html",
    "remove_urls",
    "remove_emails",
    "remove_special_chars",
    "remove_extra_whitespace"
])

# Advanced preprocessing
preprocessor.add_advanced([
    "spell_correction",
    "lemmatization",
    "stopword_removal"
])
```

### Model Selection

**Text Classification**:
- Small datasets (<10K): DistilBERT (6x faster than BERT)
- Medium datasets (10K-100K): BERT-base
- Large datasets (>100K): RoBERTa-large

**NER**:
- General: BERT + CRF layer
- Domain-specific: Fine-tune BERT on domain corpus

**Sentiment**:
- Product reviews: DistilBERT fine-tuned on Amazon reviews
- Social media: RoBERTa fine-tuned on Twitter

### Transfer Learning

```python
# Start from pre-trained language models
pipeline = NLPPipeline(task="classification")

# Option 1: Use pre-trained (no fine-tuning)
pipeline.use_pretrained("distilbert-base-uncased")

# Option 2: Fine-tune on your data
pipeline.use_pretrained_and_finetune(
    model="bert-base-uncased",
    epochs=3,
    learning_rate=2e-5
)
```

### Handling Long Text

```python
# For text longer than 512 tokens
pipeline = NLPPipeline(
    task="classification",
    max_length=512,
    truncation_strategy="head_and_tail"  # Keep start + end
)

# Or use Longformer for long documents
pipeline.use_model("longformer")  # Handles 4096 tokens
```

## Integration with SpecWeave

```python
# NLP increment structure
.specweave/increments/0042-sentiment-classifier/
├── spec.md
├── data/
│   ├── train.csv
│   ├── val.csv
│   └── test.csv
├── models/
│   ├── tokenizer/
│   ├── model-epoch-1/
│   ├── model-epoch-2/
│   └── model-epoch-3/
├── experiments/
│   ├── distilbert-baseline/
│   ├── bert-base-finetuned/
│   └── roberta-large/
└── deployment/
    ├── model.onnx
    └── inference.py
```

## Commands

```bash
/ml:nlp-pipeline --task classification --model bert-base
/ml:nlp-evaluate 0042  # Evaluate on test set
/ml:nlp-deploy 0042    # Export for production
```

Quick setup for NLP projects with state-of-the-art transformer models.
