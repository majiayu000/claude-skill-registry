---
name: agent-parser
description: End-to-end resume parsing (detect format → extract fields). Uses a combination of format detection, text extraction, and LLM parsing to normalize resume data.
---

# Parser Agent

## Overview

The Parser Agent handles the ingestion of resume files. It follows a multi-step workflow:
1.  Detects file format (`detect-resume-format`)
2.  Extracts raw text (`extract-text-pdf`, `extract-text-docx`)
3.  Sanitizes text (`sanitize-text`)
4.  Parses identifying fields (`llm-parse-resume`)

## Workflow Definition

1.  **Input**: Resume file path.
2.  **Detection**: Call `detect-resume-format` script.
3.  **Extraction**:
    *   If PDF: Call `extract-text-pdf`
    *   If DOCX: Call `extract-text-docx`
    *   If Unknown/Txt: Read file directly
4.  **Sanitization**: Call `sanitize-text`.
5.  **Parsing**: Call `llm-parse-resume`.
6.  **Validation**: Call `schema-validate-resume`.
7.  **Output**: Validated JSON object.
