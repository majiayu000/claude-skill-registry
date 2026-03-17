---
name: language-detector
description: Detect language of text with confidence scores, support for 50+ languages, and batch text classification.
---

# Language Detector

Identify the language of text with confidence scoring.

## Features

- **50+ Languages**: Wide language support
- **Confidence Scores**: Probability estimates
- **Batch Detection**: Process multiple texts
- **CSV Support**: Analyze text columns
- **Multiple Algorithms**: Character n-gram analysis

## CLI Usage

```bash
python language_detector.py --text "Hello world" --output result.json
python language_detector.py --file texts.csv --column text --output languages.csv
```

## Dependencies

- langdetect>=1.0.9
- pandas>=2.0.0
