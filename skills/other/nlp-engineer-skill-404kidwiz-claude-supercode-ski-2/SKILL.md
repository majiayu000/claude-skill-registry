---
name: nlp-engineer
description: Expert in Natural Language Processing, designing systems for text classification, NER, translation, and LLM integration using Hugging Face, spaCy, and LangChain. Use when building NLP pipelines, text analysis, or LLM-powered features. Triggers include "NLP", "text classification", "NER", "named entity", "sentiment analysis", "spaCy", "Hugging Face", "transformers".
---

# NLP Engineer

## Purpose
Provides expertise in Natural Language Processing systems design and implementation. Specializes in text classification, named entity recognition, sentiment analysis, and integrating modern LLMs using frameworks like Hugging Face, spaCy, and LangChain.

## When to Use
- Building text classification systems
- Implementing named entity recognition (NER)
- Creating sentiment analysis pipelines
- Fine-tuning transformer models
- Designing LLM-powered features
- Implementing text preprocessing pipelines
- Building search and retrieval systems
- Creating text generation applications

## Quick Start
**Invoke this skill when:**
- Building NLP pipelines (classification, NER, sentiment)
- Fine-tuning transformer models
- Implementing text preprocessing
- Integrating LLMs for text tasks
- Designing semantic search systems

**Do NOT invoke when:**
- RAG architecture design → use `/ai-engineer`
- LLM prompt optimization → use `/prompt-engineer`
- ML model deployment → use `/mlops-engineer`
- General data processing → use `/data-engineer`

## Decision Framework
```
NLP Task Type?
├── Classification
│   ├── Simple → Fine-tuned BERT/DistilBERT
│   └── Zero-shot → LLM with prompting
├── NER
│   ├── Standard entities → spaCy
│   └── Custom entities → Fine-tuned model
├── Generation
│   └── LLM (GPT, Claude, Llama)
└── Semantic Search
    └── Embeddings + Vector store
```

## Core Workflows

### 1. Text Classification Pipeline
1. Collect and label training data
2. Preprocess text (tokenization, cleaning)
3. Select base model (BERT, RoBERTa)
4. Fine-tune on labeled dataset
5. Evaluate with appropriate metrics
6. Deploy with inference optimization

### 2. NER System
1. Define entity types for domain
2. Create labeled training data
3. Choose framework (spaCy, Hugging Face)
4. Train custom NER model
5. Evaluate precision, recall, F1
6. Integrate with post-processing rules

### 3. Embedding-Based Search
1. Select embedding model (sentence-transformers)
2. Generate embeddings for corpus
3. Index in vector database
4. Implement query embedding
5. Add hybrid search (keyword + semantic)
6. Tune similarity thresholds

## Best Practices
- Start with pretrained models, fine-tune as needed
- Use domain-specific preprocessing
- Evaluate with task-appropriate metrics
- Consider inference latency for production
- Implement proper text cleaning pipelines
- Use batching for efficient inference

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Training from scratch | Wastes data and compute | Fine-tune pretrained |
| No preprocessing | Noisy inputs hurt performance | Clean and normalize text |
| Wrong metrics | Misleading evaluation | Task-appropriate metrics |
| Ignoring class imbalance | Biased predictions | Balance or weight classes |
| Overfitting to eval set | Poor generalization | Proper train/val/test splits |
