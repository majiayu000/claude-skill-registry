---
name: topic-modeler
description: Extract topics from text collections using LDA (Latent Dirichlet Allocation) with keyword extraction and topic visualization.
---

# Topic Modeler

Extract topics from text collections using LDA.

## Features

- **LDA Topic Modeling**: Latent Dirichlet Allocation
- **Topic Keywords**: Extract representative keywords per topic
- **Document Classification**: Assign documents to topics
- **Visualization**: Topic word clouds and distributions
- **Coherence Scores**: Evaluate topic quality

## CLI Usage

```bash
python topic_modeler.py --input documents.csv --column text --topics 5 --output topics.json
```

## Dependencies

- gensim>=4.3.0
- nltk>=3.8.0
- pandas>=2.0.0
- matplotlib>=3.7.0
- wordcloud>=1.9.0
