---
name: keyword-extractor
description: Extract keywords and key phrases from text using TF-IDF, RAKE, and frequency analysis. Generate word clouds and export to various formats.
---

# Keyword Extractor

Extract important keywords and key phrases from text documents using multiple algorithms. Supports TF-IDF, RAKE, and simple frequency analysis with word cloud visualization.

## Quick Start

```python
from scripts.keyword_extractor import KeywordExtractor

# Extract keywords
extractor = KeywordExtractor()
keywords = extractor.extract("Your long text document here...")
print(keywords[:10])  # Top 10 keywords

# From file
keywords = extractor.extract_from_file("document.txt")
extractor.to_wordcloud("keywords.png")
```

## Features

- **Multiple Algorithms**: TF-IDF, RAKE, frequency-based
- **Key Phrases**: Extract multi-word phrases, not just single words
- **Scoring**: Relevance scores for ranking
- **Stopword Filtering**: Built-in + custom stopwords
- **N-gram Support**: Unigrams, bigrams, trigrams
- **Word Cloud**: Visualize keyword importance
- **Batch Processing**: Process multiple documents

## API Reference

### Initialization

```python
extractor = KeywordExtractor(
    method="tfidf",      # tfidf, rake, frequency
    max_keywords=20,     # Maximum keywords to return
    min_word_length=3,   # Minimum word length
    ngram_range=(1, 3)   # Unigrams to trigrams
)
```

### Extraction Methods

```python
# TF-IDF (best for comparing documents)
keywords = extractor.extract(text, method="tfidf")

# RAKE (best for key phrases)
keywords = extractor.extract(text, method="rake")

# Frequency (simple word counts)
keywords = extractor.extract(text, method="frequency")
```

### Results Format

```python
keywords = extractor.extract(text)
# Returns list of tuples: [(keyword, score), ...]
# [('machine learning', 0.85), ('data science', 0.72), ...]

# Get just keywords
keyword_list = extractor.get_keywords(text)
# ['machine learning', 'data science', ...]
```

### Customization

```python
# Add custom stopwords
extractor.add_stopwords(['company', 'product', 'service'])

# Set minimum frequency
extractor.min_frequency = 2

# Filter by part of speech (nouns only)
extractor.pos_filter = ['NN', 'NNS', 'NNP']
```

### Visualization

```python
# Generate word cloud
extractor.to_wordcloud("wordcloud.png", colormap="viridis")

# Bar chart of top keywords
extractor.plot_keywords("keywords.png", top_n=15)
```

### Export

```python
# To JSON
extractor.to_json("keywords.json")

# To CSV
extractor.to_csv("keywords.csv")

# To plain text
extractor.to_text("keywords.txt")
```

## CLI Usage

```bash
# Extract from text
python keyword_extractor.py --text "Your text here" --top 10

# Extract from file
python keyword_extractor.py --input document.txt --method tfidf --output keywords.json

# Generate word cloud
python keyword_extractor.py --input document.txt --wordcloud cloud.png

# Batch process directory
python keyword_extractor.py --input-dir ./docs --output keywords_all.csv
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--text` | Text to analyze | - |
| `--input` | Input file path | - |
| `--input-dir` | Directory of files | - |
| `--output` | Output file | - |
| `--method` | Algorithm (tfidf, rake, frequency) | `tfidf` |
| `--top` | Number of keywords | 20 |
| `--ngrams` | N-gram range (e.g., "1,2") | `1,3` |
| `--wordcloud` | Generate word cloud | - |
| `--stopwords` | Custom stopwords file | - |

## Examples

### Article Keyword Extraction

```python
extractor = KeywordExtractor(method="tfidf")

article = """
Machine learning is transforming data science. Deep learning models
are achieving state-of-the-art results in natural language processing
and computer vision. Neural networks continue to advance...
"""

keywords = extractor.extract(article, top_n=10)
for keyword, score in keywords:
    print(f"{score:.3f}: {keyword}")
```

### Compare Multiple Documents

```python
extractor = KeywordExtractor(method="tfidf")

docs = [
    open("doc1.txt").read(),
    open("doc2.txt").read(),
    open("doc3.txt").read()
]

# Extract keywords from each
for i, doc in enumerate(docs):
    keywords = extractor.extract(doc, top_n=5)
    print(f"\nDocument {i+1}:")
    for kw, score in keywords:
        print(f"  {kw}: {score:.3f}")
```

### SEO Keyword Research

```python
extractor = KeywordExtractor(
    method="rake",
    ngram_range=(2, 4),  # Focus on phrases
    max_keywords=30
)

webpage_content = open("page.html").read()
keywords = extractor.extract(webpage_content)

# Filter by score threshold
high_value = [(kw, s) for kw, s in keywords if s > 0.5]
print("High-value keywords for SEO:")
for kw, score in high_value:
    print(f"  {kw}")
```

## Algorithm Comparison

| Algorithm | Best For | Strengths |
|-----------|----------|-----------|
| **TF-IDF** | Document comparison | Finds unique terms, good for search |
| **RAKE** | Key phrases | Extracts multi-word concepts |
| **Frequency** | Quick overview | Simple, fast, interpretable |

## Dependencies

```
scikit-learn>=1.2.0
nltk>=3.8.0
pandas>=2.0.0
matplotlib>=3.7.0
wordcloud>=1.9.0
```

## Limitations

- English optimized (other languages need language-specific stopwords)
- Very short texts may not have enough data for TF-IDF
- Domain-specific jargon may need custom stopword handling
