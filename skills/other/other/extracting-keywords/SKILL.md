---
name: extracting-keywords
description: Extract keywords from documents using YAKE algorithm with support for 34 languages (Arabic to Chinese). Use when users request keyword extraction, key terms, topic identification, content summarization, or document analysis. Includes domain-specific stopwords for AI/ML and life sciences. Optional deeper extraction mode (n=2+n=3 combined) for comprehensive coverage.
metadata:
  version: 0.2.1
---

# Extracting Keywords

Extract keywords from text using YAKE (Yet Another Keyword Extractor), an unsupervised statistical keyword extraction algorithm.

## Installation

**First time only:** Install YAKE with optimized dependencies to avoid unnecessary downloads.

```bash
cd /home/claude
uv venv yake-venv --system-site-packages
uv pip install yake --python yake-venv/bin/python --no-deps
uv pip install jellyfish segtok regex --python yake-venv/bin/python
```

This reuses system packages (numpy, networkx) instead of downloading them (~0.08s vs ~5s).

## Stopwords Configuration

**Built-in YAKE stopwords (34 languages):** Use `lan="<code>"` parameter
- See Parameters section below for all 34 supported language codes
- English (`lan="en"`) is the default

**Custom domain stopwords (bundled in `assets/`):**

**AI/ML:** `stopwords_ai.txt`
- English stopwords + 783 AI/ML domain-specific terms (1357 total)
- Filters AI/ML methodology noise (model, training, network, algorithm, parameter)
- Filters ML boilerplate (dataset, baseline, benchmark, experiment, evaluation)
- Filters technical terms (transformer, embedding, attention, optimization, inference)
- Includes full lemmatization (train/trains/trained/training/trainer)
- Use for AI/ML papers, technical reports, machine learning literature
- **Performance impact:** +4-5% runtime vs English stopwords

**Life Sciences:** `stopwords_ls.txt`
- English stopwords + 719 life sciences domain-specific terms (1293 total)
- Filters research methodology noise (study, results, analysis, significant, observed)
- Filters academic boilerplate (paper, manuscript, publication, review, editing)
- Filters statistical terms (correlation, distribution, deviation, variance)
- Filters clinical terms (patient, treatment, diagnosis, symptom, therapy)
- Filters biology/medicine (cell, tissue, protein, gene, organism)
- Includes full lemmatization (analyze/analyzes/analyzed/analyzing/analysis)
- Use for biomedical papers, clinical studies, research articles, scientific literature
- **Performance impact:** +4-5% runtime vs English stopwords

## Basic Usage

```python
import yake

# Read text
with open('document.txt', 'r') as f:
    text = f.read()

# Extract with English stopwords (default)
kw_extractor = yake.KeywordExtractor(
    lan="en",           # Language code
    n=3,                # Max n-gram size (1-3 word phrases)
    dedupLim=0.9,       # Deduplication threshold (0-1)
    top=20              # Number of keywords to return
)

keywords = kw_extractor.extract_keywords(text)

# Display results (lower score = more important)
for kw, score in keywords:
    print(f"{score:.4f}  {kw}")
```

## Domain-Specific Extraction

### Using Life Sciences Stopwords

**Option 1: Install custom stopwords file**

```bash
# Copy life sciences stopwords to YAKE package
cp assets/stopwords_ls.txt /home/claude/yake-venv/lib/python3.12/site-packages/yake/core/StopwordsList/stopwords_ls.txt

# Use with lan="ls"
kw_extractor = yake.KeywordExtractor(lan="ls", n=3, top=20)
```

**Option 2: Load custom stopwords directly**

```python
# Load stopwords from file
with open('assets/stopwords_ls.txt', 'r') as f:
    custom_stops = set(line.strip().lower() for line in f)

# Pass to extractor
kw_extractor = yake.KeywordExtractor(
    stopwords=custom_stops,
    n=3,
    top=20
)
```

### Using AI/ML Stopwords

```python
# Load AI/ML stopwords
with open('/mnt/skills/user/extracting-keywords/assets/stopwords_ai.txt', 'r') as f:
    ai_stops = set(line.strip().lower() for line in f)

# Extract with AI stopwords
kw_extractor = yake.KeywordExtractor(
    stopwords=ai_stops,
    n=3,
    top=20
)
keywords = kw_extractor.extract_keywords(text)
```

## Deeper Extraction (n=2 + n=3 Combined)

For more comprehensive extraction, run both n=2 and n=3 and consolidate results. This captures both focused phrases and broader context with ~100% time overhead (still <2s for large documents).

```python
import yake

# Load domain stopwords
with open('/mnt/skills/user/extracting-keywords/assets/stopwords_ai.txt', 'r') as f:
    stops = set(line.strip().lower() for line in f)

# Extract with n=2 (captures focused phrases)
kw_n2 = yake.KeywordExtractor(stopwords=stops, n=2, dedupLim=0.9, top=50)
results_n2 = kw_n2.extract_keywords(text)

# Extract with n=3 (captures broader context)
kw_n3 = yake.KeywordExtractor(stopwords=stops, n=3, dedupLim=0.9, top=50)
results_n3 = kw_n3.extract_keywords(text)

# Consolidate: union with score averaging for overlaps
combined = {}
for kw, score in results_n2:
    combined[kw] = score
for kw, score in results_n3:
    if kw in combined:
        combined[kw] = (combined[kw] + score) / 2
    else:
        combined[kw] = score

# Sort by score (lower = more important)
consolidated = sorted(combined.items(), key=lambda x: x[1])

# Display top 30
for kw, score in consolidated[:30]:
    print(f"{score:.4f}  {kw}")
```

**Benefits:**
- n=2 extracts cleaner domain-specific phrases ("disk move", "error rate")
- n=3 captures contextual combinations ("Move disk 1", "per-step error rate")
- Consolidation provides richer keyword set for topic modeling or search indexing

**Performance:**
- Combined approach: ~2x runtime of single extraction
- Typical timing: 0.4s (small doc) to 1.0s (large doc)
- Use when quality matters more than speed

## Parameters

**lan** (str): Language code for built-in stopwords
- `"en"` - English (default)
- `"ai"` - AI/ML (if stopwords_ai.txt installed in YAKE)
- `"ls"` - Life sciences (if stopwords_ls.txt installed in YAKE)

**Built-in YAKE languages (34 total):**
- `"ar"` - Arabic
- `"bg"` - Bulgarian  
- `"br"` - Breton
- `"cz"` - Czech
- `"da"` - Danish
- `"de"` - German
- `"el"` - Greek
- `"es"` - Spanish
- `"et"` - Estonian
- `"fa"` - Farsi/Persian
- `"fi"` - Finnish
- `"fr"` - French
- `"hi"` - Hindi
- `"hr"` - Croatian
- `"hu"` - Hungarian
- `"hy"` - Armenian
- `"id"` - Indonesian
- `"it"` - Italian
- `"ja"` - Japanese
- `"lt"` - Lithuanian
- `"lv"` - Latvian
- `"nl"` - Dutch
- `"no"` - Norwegian
- `"pl"` - Polish
- `"pt"` - Portuguese
- `"ro"` - Romanian
- `"ru"` - Russian
- `"sk"` - Slovak
- `"sl"` - Slovenian
- `"sv"` - Swedish
- `"tr"` - Turkish
- `"uk"` - Ukrainian
- `"zh"` - Chinese

**n** (int): Maximum n-gram size (default: 3)
- `1` - Single words only
- `2` - Up to 2-word phrases
- `3` - Up to 3-word phrases (recommended)
- `4-5` - May produce suboptimal results with YAKE's algorithm

**dedupLim** (float): Deduplication threshold (default: 0.9)
- Range: 0.0 to 1.0
- Higher values = more aggressive deduplication
- Controls handling of similar terms (e.g., "cancer cell" vs "cancer cells")

**top** (int): Number of keywords to return (default: 20)

**stopwords** (set): Custom stopwords set (overrides lan parameter)

## Workflow Patterns

### Single Document Analysis

```python
import yake

# Read document
with open('/mnt/user-data/uploads/article.txt', 'r') as f:
    text = f.read()

# Extract keywords
kw_extractor = yake.KeywordExtractor(lan="en", n=3, top=30)
keywords = kw_extractor.extract_keywords(text)

# Format results
results = []
for kw, score in keywords:
    results.append(f"{score:.4f}  {kw}")

print("\n".join(results))
```

### Comparing Stopwords Strategies

```python
import yake

# Load life sciences stopwords
with open('assets/stopwords_ls.txt', 'r') as f:
    ls_stops = set(line.strip().lower() for line in f)

# Extract with English stopwords
kw_en = yake.KeywordExtractor(lan="en", n=3, top=20)
keywords_en = kw_en.extract_keywords(text)

# Extract with life sciences stopwords
kw_ls = yake.KeywordExtractor(stopwords=ls_stops, n=3, top=20)
keywords_ls = kw_ls.extract_keywords(text)

# Compare results
print("English stopwords:")
for kw, score in keywords_en:
    print(f"  {score:.4f}  {kw}")

print("\nLife sciences stopwords:")
for kw, score in keywords_ls:
    print(f"  {score:.4f}  {kw}")
```

### Batch Processing

```python
import yake
import os

# Initialize extractor
kw_extractor = yake.KeywordExtractor(lan="en", n=3, top=15)

# Process multiple files
results = {}
for filename in os.listdir('/mnt/user-data/uploads'):
    if filename.endswith('.txt'):
        with open(f'/mnt/user-data/uploads/{filename}', 'r') as f:
            text = f.read()
        
        keywords = kw_extractor.extract_keywords(text)
        results[filename] = keywords

# Output results
for filename, keywords in results.items():
    print(f"\n{filename}:")
    for kw, score in keywords[:10]:  # Top 10
        print(f"  {score:.4f}  {kw}")
```

### Multilingual Extraction

```python
import yake

# French document
with open('/mnt/user-data/uploads/article_fr.txt', 'r') as f:
    french_text = f.read()

# Extract with French stopwords
kw_fr = yake.KeywordExtractor(lan="fr", n=3, top=20)
keywords_fr = kw_fr.extract_keywords(french_text)

print("Mots-clés (French):")
for kw, score in keywords_fr:
    print(f"  {score:.4f}  {kw}")

# German document
with open('/mnt/user-data/uploads/artikel_de.txt', 'r') as f:
    german_text = f.read()

# Extract with German stopwords
kw_de = yake.KeywordExtractor(lan="de", n=3, top=20)
keywords_de = kw_de.extract_keywords(german_text)

print("\nSchlüsselwörter (German):")
for kw, score in keywords_de:
    print(f"  {score:.4f}  {kw}")
```

## Output Formats

### Plain Text
```python
for kw, score in keywords:
    print(f"{kw}: {score:.4f}")
```

### CSV
```python
import csv

with open('/mnt/user-data/outputs/keywords.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Keyword', 'Score'])
    writer.writerows(keywords)
```

### JSON
```python
import json

output = [{"keyword": kw, "score": score} for kw, score in keywords]
with open('/mnt/user-data/outputs/keywords.json', 'w') as f:
    json.dump(output, f, indent=2)
```

## Notes

- Lower scores indicate more important keywords
- YAKE is unsupervised - no training data required
- **Supports 34 languages** - built-in stopwords for Arabic, Bulgarian, Chinese, Czech, Danish, Dutch, English, Estonian, Farsi, Finnish, French, German, Greek, Hindi, Croatian, Hungarian, Armenian, Indonesian, Italian, Japanese, Lithuanian, Latvian, Norwegian, Polish, Portuguese, Romanian, Russian, Slovak, Slovenian, Spanish, Swedish, Turkish, Ukrainian, and more
- Optimal n-gram size is 2 or 3 for most use cases
- For longer technical phrases (4+ words), consider post-processing or ontology matching
- Always specify full venv path: `/home/claude/yake-venv/bin/python`

## Troubleshooting

**Import errors:** Verify venv installation
```bash
/home/claude/yake-venv/bin/python -c "import yake; print(yake.__version__)"
```

**Empty results:** Check text length (YAKE needs sufficient content, typically 100+ words)

**Poor quality keywords:** Adjust parameters:
- Increase `dedupLim` for more aggressive deduplication
- Try domain-specific stopwords
- Increase `top` to see more candidates

**Generic terms appearing:** Add custom stopwords for your domain:
```python
with open('assets/stopwords_ls.txt', 'r') as f:
    stops = set(line.strip().lower() for line in f)

# Add domain-specific terms
stops.update(['term1', 'term2', 'term3'])

kw_extractor = yake.KeywordExtractor(stopwords=stops, n=3, top=20)
```
