---
name: nlp-basics
description: Process and analyze text using modern NLP techniques - preprocessing, embeddings, and transformers
version: "1.4.0"
sasmp_version: "1.4.0"
bonded_agent: 05-nlp
bond_type: PRIMARY_BOND

# Parameter Validation
parameters:
  required:
    - name: text
      type: string|list
      validation: "Non-empty text or list of texts"
  optional:
    - name: model_name
      type: string
      default: "bert-base-uncased"
    - name: max_length
      type: integer
      default: 512
      validation: "1 <= max_length <= 512"

# Retry Logic
retry_logic:
  strategy: exponential_backoff
  max_attempts: 3
  base_delay_ms: 1000

# Observability
logging:
  level: info
  metrics: [tokenization_time, embedding_dim, batch_size]
---

# NLP Basics Skill

> Transform unstructured text into structured insights.

## Quick Start

```python
from transformers import AutoTokenizer, AutoModel
import torch

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModel.from_pretrained('bert-base-uncased')

# Tokenize
text = "Machine learning is transforming industries."
inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)

# Get embeddings
with torch.no_grad():
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)  # [CLS] pooling

print(f"Embedding shape: {embeddings.shape}")
```

## Key Topics

### 1. Text Preprocessing

```python
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class TextPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def clean(self, text):
        # Lowercase
        text = text.lower()
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        # Remove special chars
        text = re.sub(r'[^\w\s]', '', text)
        # Tokenize and filter
        tokens = word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(t) for t in tokens
                  if t not in self.stop_words]
        return ' '.join(tokens)
```

### 2. Word Embeddings

| Type | Model | Use Case |
|------|-------|----------|
| **Static** | Word2Vec, GloVe | Simple, fast |
| **Contextual** | BERT, RoBERTa | SOTA accuracy |
| **Sentence** | all-MiniLM | Similarity, search |

```python
from sentence_transformers import SentenceTransformer

# Sentence embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(['Hello world', 'Hi there'])

# Similarity
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
```

### 3. Text Classification

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import Trainer, TrainingArguments

# Load pretrained model
model_name = 'bert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name, num_labels=2
)

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    evaluation_strategy='epoch',
    save_strategy='epoch',
    load_best_model_at_end=True
)

# Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)
trainer.train()
```

### 4. Named Entity Recognition

```python
from transformers import pipeline

# NER pipeline
ner = pipeline('ner', aggregation_strategy='simple')

text = "Apple Inc. was founded by Steve Jobs in Cupertino, California."
entities = ner(text)

for entity in entities:
    print(f"{entity['word']}: {entity['entity_group']} ({entity['score']:.2f})")
```

### 5. Semantic Search

```python
from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticSearch:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.corpus_embeddings = None
        self.corpus = None

    def index(self, documents):
        self.corpus = documents
        self.corpus_embeddings = self.model.encode(documents)

    def search(self, query, top_k=5):
        query_embedding = self.model.encode([query])[0]
        scores = np.dot(self.corpus_embeddings, query_embedding)
        top_indices = np.argsort(scores)[-top_k:][::-1]
        return [(self.corpus[i], scores[i]) for i in top_indices]
```

## Best Practices

### DO
- Use pretrained models
- Fine-tune on domain data
- Handle tokenization edge cases
- Batch process for efficiency
- Cache embeddings

### DON'T
- Don't ignore text preprocessing
- Don't use large models for simple tasks
- Don't fine-tune without validation
- Don't skip error analysis

## Exercises

### Exercise 1: Sentiment Analysis
```python
# TODO: Fine-tune BERT for sentiment classification
# Use the IMDB dataset
```

### Exercise 2: Semantic Search
```python
# TODO: Build a semantic search engine
# Index 1000 documents and search by query
```

## Unit Test Template

```python
import pytest

def test_preprocessing():
    """Test text preprocessing."""
    preprocessor = TextPreprocessor()
    text = "Hello World! Visit https://example.com"

    cleaned = preprocessor.clean(text)

    assert 'http' not in cleaned
    assert cleaned.islower()

def test_embeddings_shape():
    """Test embedding dimensions."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(['test'])

    assert embeddings.shape == (1, 384)
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| OOV tokens | Rare words | Use subword tokenization |
| Slow inference | Large model | Use distilled model |
| Poor accuracy | Small dataset | Data augmentation |
| Memory error | Long sequences | Reduce max_length |

## Related Resources

- **Agent**: `05-nlp`
- **Previous**: `deep-learning`
- **Next**: `computer-vision`
- **Docs**: [HuggingFace](https://huggingface.co/docs)

---

**Version**: 1.4.0 | **Status**: Production Ready
