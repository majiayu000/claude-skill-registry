---
name: text-summarizer
description: 'Advanced text summarization and translation service with async processing
  capabilities. Use when users need to: (1) Summarize large text datasets from CSV/DataFrame,
  (2) Batch process text documents w'
---

---
name: text-summarizer
description: Advanced text summarization and translation service with async processing capabilities. Use when users need to: (1) Summarize large text datasets from CSV/DataFrame, (2) Batch process text documents with length-based intelligent routing, (3) Translate shorter text content, (4) Configure custom processing parameters for text analysis workflows, (5) Handle text processing tasks requiring async operations for performance.
---

# Text Summarizer

Intelligent text processing service that automatically determines whether to summarize or translate content based on configurable length thresholds, with async batch processing capabilities.

## Core Functionality

Use `scripts/text_summarizer.py` for bulk text processing operations:

- **Smart routing**: Texts above length threshold ? summarization; texts below ? translation
- **Async processing**: Efficient batch operations with concurrent API calls
- **Flexible input**: Process pandas DataFrames or CSV files
- **Configurable**: Adjustable length thresholds, model selection, temperature settings

## Quick Start

Process a DataFrame with default settings:

```python
uv run scripts/text_summarizer.py --input data.csv --text-column content --output results.csv
```

## Advanced Configuration

**Custom length threshold** (default: 500 words):
```bash
uv run scripts/text_summarizer.py --input data.csv --length 1000 --text-column review
```

**Model selection** (default: gpt-4.1):
```bash
uv run scripts/text_summarizer.py --input data.csv --model gpt-4o-mini --temperature 0.3
```

## API Reference

For programmatic usage and advanced customization, see [API_REFERENCE.md](references/API_REFERENCE.md) for complete NotesSummarizer class documentation.

## Error Handling

- **Missing dependencies**: Ensure LangChain, pandas, and OpenAI libraries are installed
- **API limits**: Script handles retries automatically with exponential backoff
- **File access**: Verify input file paths and write permissions for output files
- **Column names**: Specify correct text column name with `--text-column` parameter

## Environment Requirements

- Python 3.11+
- OpenAI API key configured
- Required packages: `langchain`, `pandas`, `tqdm`, `numpy`
