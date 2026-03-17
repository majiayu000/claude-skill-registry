---
name: named-entity-extractor
description: Extract named entities (people, organizations, locations, dates) from text using NLP. Use for document analysis, information extraction, or data enrichment.
---

# Named Entity Extractor

Extract named entities from text including people, organizations, locations, dates, and more.

## Features

- **Entity Types**: People, organizations, locations, dates, money, percentages
- **Multiple Models**: spaCy for accuracy, regex for speed
- **Batch Processing**: Process multiple documents
- **Entity Linking**: Group same entities across text
- **Export**: JSON, CSV output formats
- **Visualization**: Entity highlighting

## Quick Start

```python
from entity_extractor import EntityExtractor

extractor = EntityExtractor()

text = "Apple Inc. was founded by Steve Jobs in Cupertino, California in 1976."

entities = extractor.extract(text)
for entity in entities:
    print(f"{entity['text']}: {entity['type']}")

# Output:
# Apple Inc.: ORG
# Steve Jobs: PERSON
# Cupertino: GPE
# California: GPE
# 1976: DATE
```

## CLI Usage

```bash
# Extract from text
python entity_extractor.py --text "Steve Jobs founded Apple in California."

# Extract from file
python entity_extractor.py --input document.txt

# Batch process folder
python entity_extractor.py --input ./documents/ --output entities.csv

# Filter by entity type
python entity_extractor.py --input document.txt --types PERSON,ORG

# Use regex mode (faster, less accurate)
python entity_extractor.py --input document.txt --mode regex

# JSON output
python entity_extractor.py --input document.txt --json
```

## API Reference

### EntityExtractor Class

```python
class EntityExtractor:
    def __init__(self, mode: str = "spacy", model: str = "en_core_web_sm")

    # Extraction
    def extract(self, text: str) -> list
    def extract_file(self, filepath: str) -> list
    def extract_batch(self, folder: str) -> dict

    # Filtering
    def filter_entities(self, entities: list, types: list) -> list
    def get_unique_entities(self, entities: list) -> list
    def group_by_type(self, entities: list) -> dict

    # Analysis
    def entity_frequency(self, text: str) -> dict
    def find_relationships(self, text: str) -> list

    # Export
    def to_csv(self, entities: list, output: str) -> str
    def to_json(self, entities: list, output: str) -> str
    def highlight_text(self, text: str) -> str
```

## Entity Types

### Standard Entity Types (spaCy)

| Type | Description | Example |
|------|-------------|---------|
| PERSON | People, including fictional | "Steve Jobs" |
| ORG | Companies, agencies, institutions | "Apple Inc." |
| GPE | Countries, cities, states | "California" |
| LOC | Non-GPE locations, mountains, water | "Pacific Ocean" |
| DATE | Dates, periods | "January 2024" |
| TIME | Times | "3:30 PM" |
| MONEY | Monetary values | "$1.5 million" |
| PERCENT | Percentages | "20%" |
| PRODUCT | Products | "iPhone" |
| EVENT | Events | "World Cup" |
| WORK_OF_ART | Books, songs, etc. | "The Great Gatsby" |
| LAW | Laws, regulations | "GDPR" |
| LANGUAGE | Languages | "English" |
| NORP | Nationalities, groups | "American" |

### Regex Mode Entities

Faster extraction with regex patterns:

| Type | Description |
|------|-------------|
| EMAIL | Email addresses |
| PHONE | Phone numbers |
| URL | Web URLs |
| DATE | Common date formats |
| MONEY | Currency amounts |
| PERCENTAGE | Percentages |

## Output Format

### Entity Result

```python
{
    "text": "Steve Jobs",
    "type": "PERSON",
    "start": 10,
    "end": 20,
    "confidence": 0.95
}
```

### Full Extraction Result

```python
{
    "text": "Original text...",
    "entities": [
        {"text": "Steve Jobs", "type": "PERSON", "start": 10, "end": 20},
        {"text": "Apple Inc.", "type": "ORG", "start": 30, "end": 40}
    ],
    "summary": {
        "total_entities": 5,
        "unique_entities": 4,
        "by_type": {
            "PERSON": 2,
            "ORG": 1,
            "GPE": 2
        }
    }
}
```

## Filtering and Grouping

### Filter by Type

```python
entities = extractor.extract(text)

# Get only people and organizations
filtered = extractor.filter_entities(entities, ["PERSON", "ORG"])
```

### Get Unique Entities

```python
# Remove duplicates, keep first occurrence
unique = extractor.get_unique_entities(entities)
```

### Group by Type

```python
grouped = extractor.group_by_type(entities)

# Returns:
{
    "PERSON": ["Steve Jobs", "Tim Cook"],
    "ORG": ["Apple Inc."],
    "GPE": ["California", "Cupertino"]
}
```

## Entity Frequency

```python
frequency = extractor.entity_frequency(text)

# Returns:
{
    "Steve Jobs": {"count": 5, "type": "PERSON"},
    "Apple": {"count": 8, "type": "ORG"},
    "California": {"count": 2, "type": "GPE"}
}
```

## Batch Processing

### Process Folder

```python
results = extractor.extract_batch("./documents/")

# Returns:
{
    "doc1.txt": {
        "entities": [...],
        "summary": {...}
    },
    "doc2.txt": {
        "entities": [...],
        "summary": {...}
    }
}
```

### Export to CSV

```python
extractor.to_csv(results, "entities.csv")

# Creates CSV with columns:
# filename, entity_text, entity_type, start, end
```

## Text Highlighting

Generate HTML with highlighted entities:

```python
html = extractor.highlight_text(text)

# Returns HTML with colored spans for each entity type
```

## Example Workflows

### Document Analysis

```python
extractor = EntityExtractor()

# Analyze a document
text = open("article.txt").read()
result = extractor.extract(text)

# Get key people mentioned
people = extractor.filter_entities(result, ["PERSON"])
print(f"People mentioned: {len(people)}")

# Get frequency
freq = extractor.entity_frequency(text)
top_entities = sorted(freq.items(), key=lambda x: x[1]["count"], reverse=True)[:10]
```

### Contact Information Extraction

```python
extractor = EntityExtractor(mode="regex")

text = """
Contact John Smith at john.smith@example.com
or call (555) 123-4567.
"""

entities = extractor.extract(text)
# Finds: EMAIL, PHONE entities
```

### Content Tagging

```python
extractor = EntityExtractor()

articles = ["article1.txt", "article2.txt", "article3.txt"]
tags = {}

for article in articles:
    entities = extractor.extract_file(article)
    tags[article] = extractor.get_unique_entities(entities)
```

## Dependencies

- spacy>=3.7.0
- pandas>=2.0.0
- en_core_web_sm (spaCy model)

Note: Run `python -m spacy download en_core_web_sm` to install the model.
