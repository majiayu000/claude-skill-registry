---
name: text-analyzer
description: Advanced text analysis and summarization skill for Claude
version: 1.0.0
author: claude-team
tags: [text, analysis, nlp]
---

# Text Analyzer Skill

A comprehensive skill for analyzing, processing, and summarizing text documents with support for multiple formats and output types.

## Overview

Text Analyzer provides intelligent text processing capabilities including:
- Document summarization with multiple summary lengths
- Sentiment analysis and emotion detection
- Keyword extraction and topic modeling
- Reading level assessment
- Text statistics and metrics

## Installation

```bash
curl -s https://claude.ai/skills/text-analyzer | bash
```

Or manually:
1. Copy `text-analyzer.md` to `~/.claude/skills/`
2. Restart Claude Code
3. Access via `/text-analyzer` command

## Quick Start

### Basic Summarization

```bash
/text-analyzer summarize --file document.txt --length short
```

### Sentiment Analysis

```bash
/text-analyzer sentiment --text "This is amazing!"
```

### Extract Keywords

```bash
/text-analyzer keywords --file article.md --count 10
```

## Configuration

Create `~/.config/text-analyzer.yaml`:

```yaml
summarization:
  default_length: medium
  preserve_structure: true

sentiment:
  model: bert-base
  confidence_threshold: 0.7

keywords:
  algorithm: tfidf
  min_frequency: 2
```

## Commands

### summarize

Generates summaries of text documents with configurable length.

**Usage:**
```
/text-analyzer summarize [OPTIONS]
```

**Options:**
- `--file PATH` - Input file path (required)
- `--length {short|medium|long}` - Summary length (default: medium)
- `--format {text|json|markdown}` - Output format (default: text)
- `--preserve-structure` - Keep original document structure
- `--ignore-stopwords` - Remove common words from summary

**Example:**
```bash
/text-analyzer summarize --file research.pdf --length long --format json
```

### sentiment

Analyzes text sentiment and emotional tone.

**Usage:**
```
/text-analyzer sentiment [OPTIONS]
```

**Options:**
- `--text STRING` - Input text (required if no --file)
- `--file PATH` - Input file path (required if no --text)
- `--detailed` - Show detailed emotion breakdown
- `--comparative` - Compare sentiment across sections

**Example:**
```bash
/text-analyzer sentiment --file feedback.txt --detailed
```

### keywords

Extracts key terms and topics from text.

**Usage:**
```
/text-analyzer keywords [OPTIONS]
```

**Options:**
- `--file PATH` - Input file path (required)
- `--count N` - Number of keywords to extract (default: 5)
- `--min-frequency N` - Minimum occurrence frequency (default: 1)
- `--include-phrases` - Include multi-word phrases
- `--exclude-pos TAGS` - Exclude parts of speech

**Example:**
```bash
/text-analyzer keywords --file document.md --count 15 --include-phrases
```

## Use Cases

### Document Summarization Workflow

Process large documentation automatically:

1. Store documents in a library
2. Generate summaries for quick review
3. Extract keywords for indexing
4. Assess reading difficulty

### Sentiment Monitoring

Track sentiment across customer feedback:

```bash
/text-analyzer sentiment --file feedback.csv --detailed
/text-analyzer sentiment --file support_tickets.json --comparative
```

### Content Analysis Pipeline

Build AI-powered content analysis workflows:

```bash
# Extract summary and keywords
/text-analyzer summarize --file article.md > summary.txt
/text-analyzer keywords --file article.md --count 20 > keywords.txt

# Analyze sentiment
/text-analyzer sentiment --file comments.txt --detailed > sentiment.json
```

## Output Formats

### Text Format (default)

Plain text output with clear sections.

```
Summary:
[summarized content]

Statistics:
- Original Length: 5,234 words
- Summary Length: 1,045 words
- Compression Ratio: 80%
```

### JSON Format

Structured output for integration:

```json
{
  "summary": "...",
  "statistics": {
    "original_words": 5234,
    "summary_words": 1045
  },
  "metadata": {
    "processed_at": "2026-02-03T10:30:00Z",
    "version": "1.0.0"
  }
}
```

### Markdown Format

Enhanced markdown with formatting:

```markdown
# Summary

## Key Points
- Point 1
- Point 2
- Point 3

## Metadata
**Original:** 5,234 words | **Summary:** 1,045 words
```

## Advanced Features

### Batch Processing

Process multiple files at once:

```bash
/text-analyzer batch --input-dir ./documents --output-dir ./summaries --length short
```

### Custom Models

Use custom language models:

```bash
/text-analyzer summarize --file doc.txt --model gpt-4 --temperature 0.3
```

### Stream Processing

Handle large files with streaming:

```bash
/text-analyzer stream --input-pipe < large_file.txt --chunk-size 10000
```

## Performance Tips

1. **For Large Files:** Use `--stream` option to avoid memory issues
2. **For Speed:** Use shorter summary length settings
3. **For Accuracy:** Use `--detailed` flag with sentiment analysis
4. **For Batch Jobs:** Use `--parallel` to process multiple files

## Troubleshooting

### Command Not Found

Ensure skill is installed:
```bash
ls ~/.claude/skills/ | grep text-analyzer
```

### Memory Issues with Large Files

Use streaming mode:
```bash
/text-analyzer summarize --file huge.txt --stream
```

### Inconsistent Results

Clear cache and retry:
```bash
/text-analyzer clear-cache
/text-analyzer summarize --file document.txt
```

## API Reference

### Python Integration

```python
from text_analyzer import TextAnalyzer

analyzer = TextAnalyzer()
summary = analyzer.summarize("path/to/file.txt", length="medium")
keywords = analyzer.extract_keywords("path/to/file.txt", count=10)
sentiment = analyzer.analyze_sentiment("This is great!")
```

### REST API

```bash
curl -X POST http://localhost:8080/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "length": "short"}'
```

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

- GitHub Issues: https://github.com/claude-team/text-analyzer/issues
- Documentation: https://claude.ai/skills/text-analyzer
- Community: https://discourse.claude.ai/c/skills/text-analyzer

---

*Last Updated: 2026-02-03*
*Maintained by: Claude Team*
