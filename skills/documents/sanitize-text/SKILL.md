---
name: sanitize-text
description: Normalize raw text by removing excessive whitespace, non-printable characters, and standardizing unicode. Use this to clean up text extracted from PDFs or DOCX files before processing with LLMs.
---

# Sanitize Text

## Overview

This skill cleans and normalizes raw text. It is essential for preprocessing text extracted from documents like PDFs, which often contain encoding artifacts, excessive whitespace, or weird control characters.

## Usage

### Sanitize Script

**Syntax:**

```bash
python3 .agent/skills/sanitize-text/scripts/sanitize.py <input_file> [--output <output_file>]
```

**Arguments:**

*   `input_file`: Path to the file containing raw text.
*   `--output`: (Optional) Path to write cleaned text to. If omitted, prints to stdout.

**Example:**

```bash
python3 .agent/skills/sanitize-text/scripts/sanitize.py raw_resume.txt --output clean_resume.txt
```
