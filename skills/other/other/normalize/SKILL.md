---
name: normalize
description: >
  Normalize text to handle PDF/Unicode encoding issues.
  Converts Windows-1252, curly quotes, em/en dashes, ligatures,
  directional formatting, zero-width chars, and more to clean ASCII.
allowed-tools: Bash, Read
triggers:
  - normalize text
  - clean text
  - normalize unicode
  - fix encoding
  - clean pdf text
  - normalize pdf
metadata:
  short-description: Clean PDF/Unicode text to ASCII
  project-path: /home/graham/workspace/experiments/pi-mono
provides:
  - text-normalization
composes: [, task-monitor]

taxonomy:
  - preprocessing
  - text
  - precision
---

# Text Normalize

Comprehensive text normalization for handling PDF and Unicode encoding issues.

## Quick Start

```bash
# Normalize text from stdin
echo "Hello\u2019world" | .pi/skills/normalize/run.sh

# Normalize a file
.pi/skills/normalize/run.sh document.txt

# Normalize with output file
.pi/skills/normalize/run.sh document.txt -o clean.txt

# Treat argument as text (not filename)
.pi/skills/normalize/run.sh -t "Hello\u201cworld\u201d"

# Show statistics
.pi/skills/normalize/run.sh document.txt --stats
```

## What It Normalizes

| Category | Examples | Normalized To |
|----------|----------|---------------|
| **Whitespace** | Non-breaking, em/en space, hair space | Regular space |
| **Hyphens** | En dash, em dash, minus sign, figure dash | ASCII hyphen `-` |
| **Quotes** | Curly quotes, guillemets, primes | Straight `'` and `"` |
| **Windows-1252** | `\x93`, `\x94`, `\x92` | `"`, `"`, `'` |
| **Ligatures** | fi, fl, ffi, ffl | Expanded letters |
| **Bullets** | Various bullet points | Hyphen `-` |
| **Zero-width** | ZWSP, ZWNJ, ZWJ, BOM | Removed |
| **Directional** | LTR/RTL marks | Removed |
| **Control chars** | C0/C1 (except newline/tab) | Removed |
| **Line breaks** | `intro-\nduction` | `introduction` |

## Pipeline Integration

This skill is based on the same normalization used in the extractor pipeline's
s02_marker_extractor.py. The code is kept in sync with text_toolz patterns.

### Python Usage

```python
from normalize import normalize_text

# Clean text for pattern matching
text = "1.\u00a0Introduction"  # Non-breaking space
clean = normalize_text(text)   # "1. Introduction"
```

## Normalization Steps

1. **Windows-1252 conversion** - Handle legacy MS Office encoding
2. **NFKC normalization** - Unicode compatibility decomposition
3. **Remove directional formatting** - LTR/RTL marks
4. **Remove control characters** - C0/C1 (preserve newlines)
5. **Normalize whitespace** - All special spaces to ASCII
6. **Normalize hyphens** - All dash variants to `-`
7. **Normalize quotes** - Curly to straight
8. **Normalize dots** - Ellipsis, leader dots
9. **Normalize bullets** - All bullet types to `-`
10. **Expand ligatures** - fi/fl/ffi/ffl
11. **Fix line-break hyphens** - Join hyphenated words
12. **Collapse whitespace** - Multiple spaces to single

## Based On

- text_toolz library patterns
- extractor pipeline s02 normalization
- NFKC Unicode standard
