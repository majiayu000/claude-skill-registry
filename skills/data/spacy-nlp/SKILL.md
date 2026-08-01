---
name: spacy-nlp
description: 'Industrial-strength NLP with spaCy 3.x for text processing and custom
  classifier training. Use when: installing spaCy, selecting models (en_core_web_sm/md/lg/trf),
  tokenization, POS tagging, named ent'
---

---
name: spacy-nlp
description: Industrial-strength NLP with spaCy 3.x for text processing and custom classifier training. Use when: installing spaCy, selecting models (en_core_web_sm/md/lg/trf), tokenization, POS tagging, named entity recognition, dependency parsing, training TextCategorizer models, troubleshooting errors (E050/E941 model errors, E927 version mismatch, memory issues), batch processing with nlp.pipe, or deploying models to production. Includes data preparation scripts, config templates, and FastAPI serving examples.
---

# spaCy NLP

Production-ready NLP with spaCy 3.x. This skill covers installation through deployment.

## Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Text Processing](#text-processing)
- [Training Classifiers](#training-classifiers)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)

---

## Scope

**In Scope:**
- spaCy 3.x installation and text processing
- TextCategorizer training for document classification
- Production deployment and optimization patterns

**Out of Scope (use other tools/skills):**
- Training custom NER models (different workflow)
- spaCy 2.x (deprecated, incompatible with 3.x)
- Rule-based matching (EntityRuler, Matcher, PhraseMatcher)
- Custom tokenizers or language models

---

## Quick Start

```python
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion.")

# Entities
for ent in doc.ents:
    print(ent.text, ent.label_)

# Tokens with attributes
for token in doc:
    print(token.text, token.pos_, token.dep_)
```

---

## Installation

### Standard Setup

```bash
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
```

### Model Selection

| Model | Size | Speed | Use Case |
|-------|------|-------|----------|
| `en_core_web_sm` | 12 MB | Fastest | Prototyping, speed-critical |
| `en_core_web_md` | 40 MB | Fast | General use with word vectors |
| `en_core_web_lg` | 560 MB | Fast | Semantic similarity tasks |
| `en_core_web_trf` | 438 MB | Slow | Maximum accuracy (GPU) |

### Verify Installation

```python
import spacy
print(spacy.__version__)
nlp = spacy.load("en_core_web_sm")
doc = nlp("Test sentence.")
print(f"Tokens: {len(doc)}")
```

**For detailed installation options** (conda, GPU, transformers): See [references/installation.md](references/installation.md)

---

## Text Processing

### Basic Pipeline

```python
nlp = spacy.load("en_core_web_sm")
doc = nlp("The striped bats are hanging on their feet.")

# Tokenization + attributes
for token in doc:
    print(f"{token.text:10} | {token.lemma_:10} | {token.pos_:6} | {token.dep_}")
```

### Named Entity Recognition

```python
for ent in doc.ents:
    print(ent.text, ent.label_)  # "Apple Inc." ORG, "Steve Jobs" PERSON
```

**For entity types, filtering, and span details**: See [references/basic-usage.md](references/basic-usage.md#named-entity-recognition)

### Batch Processing (Critical for Production)

```python
# WRONG - slow
for text in texts:
    doc = nlp(text)  # Don't do this

# CORRECT - fast
for doc in nlp.pipe(texts, batch_size=50):
    process(doc)

# With multiprocessing
docs = list(nlp.pipe(texts, n_process=4))
```

### Disable Unused Components

```python
# Only need NER - disable the rest for 2x speed
nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger", "lemmatizer"])
```

**For Doc/Token/Span details, noun chunks, similarity**: See [references/basic-usage.md](references/basic-usage.md)

---

## Training Classifiers

Train custom text classifiers with TextCategorizer.

### Workflow Overview

1. **Prepare data** → Run `scripts/prepare_training_data.py`
2. **Generate config** → Run `scripts/generate_config.py` or use `assets/config_textcat.cfg`
3. **Validate** → `python -m spacy debug data config.cfg` (catches issues before training)
4. **Train** → `python -m spacy train config.cfg --output ./output`
5. **Evaluate** → Run `scripts/evaluate_model.py`
6. **Use** → `nlp = spacy.load("./output/model-best")`

### Data Format

Training data uses spaCy's DocBin format. Example input (JSON):

```json
[
  {"text": "Quarterly revenue exceeded expectations", "label": "Business"},
  {"text": "Fixed null pointer exception in parser", "label": "Programming"},
  {"text": "Kubernetes deployment manifest updated", "label": "DevOps"}
]
```

Convert with script:

```bash
python scripts/prepare_training_data.py \
  --input data.json \
  --output-train train.spacy \
  --output-dev dev.spacy \
  --split 0.8
```

### Training Command

```bash
# Generate optimized config
python scripts/generate_config.py --categories "Business,Technology,Programming,DevOps"

# Or use template
cp assets/config_textcat.cfg config.cfg

# Train
python -m spacy train config.cfg --output ./output

# With GPU
python -m spacy train config.cfg --output ./output --gpu-id 0
```

### Using Trained Model

```python
nlp = spacy.load("./output/model-best")
doc = nlp("Deploy the application to Kubernetes cluster")
predicted = max(doc.cats, key=doc.cats.get)
confidence = doc.cats[predicted]
print(f"{predicted}: {confidence:.1%}")  # DevOps: 94.2%
```

**For detailed training guide**: See [references/text-classification.md](references/text-classification.md)

---

## Troubleshooting

### Model Not Found (E050)

```
OSError: [E050] Can't find model 'en_core_web_sm'
```

**Fix:**
```bash
python -m spacy download en_core_web_sm
```

**Alternative (avoids path issues):**
```python
import en_core_web_sm
nlp = en_core_web_sm.load()
```

### Memory Issues

**Symptoms:** OOM errors, slow processing

**Fixes:**
```python
# 1. Disable unused components
nlp = spacy.load("en_core_web_sm", exclude=["parser", "ner"])

# 2. Process in chunks
for chunk in chunk_text(large_text, max_length=100000):
    doc = nlp(chunk)

# 3. Use memory zones (spaCy 3.8+)
with nlp.memory_zone():
    for doc in nlp.pipe(batch):
        process(doc)
```

### GPU Not Working

```python
import spacy

# Must call BEFORE loading model
if spacy.prefer_gpu():
    print("Using GPU")
else:
    print("GPU not available")

nlp = spacy.load("en_core_web_trf")  # Now loads on GPU
```

### Version Compatibility

spaCy 2.x models **do not work** with spaCy 3.x. Check compatibility:

```bash
python -m spacy validate
```

**For more troubleshooting**: See [references/troubleshooting.md](references/troubleshooting.md)

---

## Production Deployment

### Package Model

```bash
python -m spacy package ./output/model-best ./packages \
  --name my_classifier \
  --version 1.0.0

pip install ./packages/en_my_classifier-1.0.0/
```

### FastAPI Server

Use the production template:

```bash
python scripts/serve_model.py --model ./output/model-best --port 8000
```

Or customize from template:

```python
from fastapi import FastAPI
import spacy

app = FastAPI()
nlp = spacy.load("en_my_classifier")

@app.post("/classify")
async def classify(text: str):
    with nlp.memory_zone():
        doc = nlp(text)
        return {
            "category": max(doc.cats, key=doc.cats.get),
            "scores": doc.cats
        }
```

### Performance Optimization

| Technique | Speedup | When to Use |
|-----------|---------|-------------|
| Disable components | 2-3x | Don't need all annotations |
| `nlp.pipe()` | 5-10x | Processing multiple texts |
| Multiprocessing | 2-4x | CPU-bound, many cores |
| GPU | 2-5x | Transformer models |

**For evaluation metrics and hyperparameter tuning**: See [references/production.md](references/production.md)

---

## Scripts Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `prepare_training_data.py` | Convert JSON to DocBin | `python scripts/prepare_training_data.py --input data.json` |
| `generate_config.py` | Create training config | `python scripts/generate_config.py --categories "A,B,C"` |
| `evaluate_model.py` | Detailed metrics | `python scripts/evaluate_model.py --model ./output/model-best` |
| `serve_model.py` | FastAPI server | `python scripts/serve_model.py --model ./model --port 8000` |

---

## Assets Reference

| Asset | Purpose | Usage |
|-------|---------|-------|
| `config_textcat.cfg` | Base training config | Copy and customize for your labels |
| `training_data_template.json` | Data format example | Reference for preparing your data |
