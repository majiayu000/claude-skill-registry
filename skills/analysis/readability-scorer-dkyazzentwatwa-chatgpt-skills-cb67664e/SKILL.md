---
name: readability-scorer
description: Calculate readability scores (Flesch-Kincaid, Gunning Fog, SMOG) and grade levels for text. Analyze writing complexity and get improvement suggestions.
---

# Readability Scorer

Analyze text readability using industry-standard formulas. Get grade level estimates, complexity metrics, and suggestions for improving clarity.

## Quick Start

```python
from scripts.readability_scorer import ReadabilityScorer

# Score text
scorer = ReadabilityScorer()
scores = scorer.analyze("Your text to analyze goes here.")
print(f"Grade Level: {scores['grade_level']}")
print(f"Flesch Reading Ease: {scores['flesch_reading_ease']}")
```

## Features

- **Multiple Formulas**: Flesch-Kincaid, Gunning Fog, SMOG, Coleman-Liau, ARI
- **Grade Level**: US grade level estimate
- **Reading Ease**: 0-100 ease score
- **Text Statistics**: Words, sentences, syllables, complex words
- **Batch Analysis**: Process multiple documents
- **Comparison**: Compare readability across texts

## API Reference

### Initialization

```python
scorer = ReadabilityScorer()
```

### Analysis

```python
scores = scorer.analyze(text)
# Returns:
# {
#     'flesch_reading_ease': 65.2,
#     'flesch_kincaid_grade': 8.1,
#     'gunning_fog': 10.2,
#     'smog_index': 9.5,
#     'coleman_liau': 9.8,
#     'ari': 8.4,
#     'grade_level': 8.5,  # Average
#     'reading_time_minutes': 2.3,
#     'stats': {
#         'words': 250,
#         'sentences': 15,
#         'syllables': 380,
#         'complex_words': 25,
#         'avg_words_per_sentence': 16.7,
#         'avg_syllables_per_word': 1.52
#     }
# }
```

### Individual Scores

```python
# Get specific scores
fre = scorer.flesch_reading_ease(text)
fkg = scorer.flesch_kincaid_grade(text)
fog = scorer.gunning_fog(text)
smog = scorer.smog_index(text)
```

### Batch Analysis

```python
texts = [text1, text2, text3]
results = scorer.analyze_batch(texts)

# From files
results = scorer.analyze_files(["doc1.txt", "doc2.txt"])
```

### Comparison

```python
# Compare two texts
comparison = scorer.compare(text1, text2)
print(f"Text 1 grade: {comparison['text1']['grade_level']}")
print(f"Text 2 grade: {comparison['text2']['grade_level']}")
```

## CLI Usage

```bash
# Analyze text
python readability_scorer.py --text "Your text here"

# Analyze file
python readability_scorer.py --input document.txt

# Compare files
python readability_scorer.py --compare doc1.txt doc2.txt

# Batch analyze directory
python readability_scorer.py --input-dir ./docs --output report.csv

# Specific formula only
python readability_scorer.py --input doc.txt --formula flesch
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--text` | Text to analyze | - |
| `--input` | Input file | - |
| `--input-dir` | Directory of files | - |
| `--output` | Output file (json/csv) | - |
| `--compare` | Compare two files | - |
| `--formula` | Specific formula | all |

## Score Interpretation

### Flesch Reading Ease

| Score | Difficulty | Grade Level |
|-------|------------|-------------|
| 90-100 | Very Easy | 5th grade |
| 80-89 | Easy | 6th grade |
| 70-79 | Fairly Easy | 7th grade |
| 60-69 | Standard | 8th-9th grade |
| 50-59 | Fairly Hard | 10th-12th grade |
| 30-49 | Difficult | College |
| 0-29 | Very Difficult | College graduate |

### Grade Level Scale

| Grade | Audience |
|-------|----------|
| 1-5 | Elementary school |
| 6-8 | Middle school |
| 9-12 | High school |
| 13-16 | College |
| 17+ | Graduate level |

## Examples

### Analyze Blog Post

```python
scorer = ReadabilityScorer()

blog_post = """
Writing clear content is essential for engaging readers.
Short sentences help. Simple words work best.
Your audience will thank you for making things easy to understand.
"""

scores = scorer.analyze(blog_post)
print(f"Flesch Reading Ease: {scores['flesch_reading_ease']:.1f}")
print(f"Grade Level: {scores['grade_level']:.1f}")
print(f"Reading Time: {scores['reading_time_minutes']:.1f} minutes")

if scores['grade_level'] > 8:
    print("Consider simplifying for a wider audience.")
```

### Compare Document Versions

```python
scorer = ReadabilityScorer()

original = open("original.txt").read()
simplified = open("simplified.txt").read()

comparison = scorer.compare(original, simplified)

print("Original:")
print(f"  Grade Level: {comparison['text1']['grade_level']:.1f}")
print(f"  Flesch Ease: {comparison['text1']['flesch_reading_ease']:.1f}")

print("\nSimplified:")
print(f"  Grade Level: {comparison['text2']['grade_level']:.1f}")
print(f"  Flesch Ease: {comparison['text2']['flesch_reading_ease']:.1f}")

improvement = comparison['text1']['grade_level'] - comparison['text2']['grade_level']
print(f"\nImprovement: {improvement:.1f} grade levels easier")
```

### Batch Analyze Documentation

```python
scorer = ReadabilityScorer()
import os

results = []
for filename in os.listdir("./docs"):
    if filename.endswith(".md"):
        text = open(f"./docs/{filename}").read()
        scores = scorer.analyze(text)
        results.append({
            'file': filename,
            'grade': scores['grade_level'],
            'ease': scores['flesch_reading_ease']
        })

# Sort by difficulty
results.sort(key=lambda x: x['grade'], reverse=True)

print("Documents by Difficulty:")
for r in results:
    print(f"  {r['file']}: Grade {r['grade']:.1f}")
```

## Dependencies

```
nltk>=3.8.0
```

## Limitations

- English language only
- Formulas designed for prose (may not work well for lists, code, etc.)
- Syllable counting is estimated (may have minor inaccuracies)
- Doesn't assess comprehension, only surface-level complexity
