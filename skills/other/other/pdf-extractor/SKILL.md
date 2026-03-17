---
name: pdf-extractor
description: "Extract text, tables, and images from PDFs. Use when: extracting data from reports; converting PDF tables to CSV; pulling images from presentations; processing research papers; batch converting PDFs to text"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# PDF Extractor

> Extract text, tables, and images from PDF files using pdfplumber - turn static PDFs into usable data.

## When to Use This Skill

- **Report processing** - Extract data from PDF reports
- **Table extraction** - Convert PDF tables to CSV
- **Image collection** - Pull images from presentations
- **Text mining** - Bulk convert PDFs to searchable text
- **Research** - Process academic papers and whitepapers


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures analysis frameworks | Metric definitions |
| Identifies patterns in data | Business interpretation |
| Creates visualization templates | Dashboard design |
| Suggests optimization areas | Action priorities |
| Calculates statistical measures | Decision thresholds |

## Dependencies

```bash
pip install pdfplumber pypdf click pandas
# For image extraction:
pip install Pillow
```

## Commands

### Extract Text
```bash
python scripts/main.py text document.pdf
python scripts/main.py text document.pdf --pages 1-5
```

### Extract Tables
```bash
python scripts/main.py tables report.pdf --output tables.csv
python scripts/main.py tables financial.pdf --page 3
```

### Extract Images
```bash
python scripts/main.py images presentation.pdf --output ./images/
```

### Merge PDFs
```bash
python scripts/main.py merge doc1.pdf doc2.pdf --output combined.pdf
```

### PDF Info
```bash
python scripts/main.py info document.pdf
```

## Examples

### Example 1: Extract Financial Tables
```bash
python scripts/main.py tables annual-report.pdf --output financials.csv

# Output: financials.csv with all tables found
# Also creates individual CSVs: table_page3_1.csv, table_page5_1.csv
```

### Example 2: Batch Convert to Text
```bash
python scripts/main.py batch ./pdfs/ --output ./text/

# Converts all PDFs in folder to .txt files
```

### Example 3: Extract Specific Pages
```bash
python scripts/main.py text whitepaper.pdf --pages 1,5-10,15

# Extracts only pages 1, 5-10, and 15
```

## Skill Boundaries

### What This Skill Does Well
- Structuring data analysis
- Identifying patterns and trends
- Creating visualization frameworks
- Calculating statistical measures

### What This Skill Cannot Do
- Access your actual data
- Replace statistical expertise
- Make business decisions
- Guarantee prediction accuracy

## Related Skills

- [web-scraper](../web-scraper/) - Scrape web content
- [content-repurposer](../content-repurposer/) - Repurpose extracted content

## Skill Metadata


- **Mode**: centaur
```yaml
category: automation
subcategory: document-processing
dependencies: [pdfplumber, pypdf, pandas]
difficulty: beginner
time_saved: 4+ hours/week
```
