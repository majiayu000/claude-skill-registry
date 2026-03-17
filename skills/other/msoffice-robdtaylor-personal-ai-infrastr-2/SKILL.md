---
name: MSOffice
description: |
  Create MS Word and PowerPoint documents on any topic.

  USE WHEN user wants: documents, reports, word docs, presentations, slides, powerpoint, decks.

allowed-tools:
  - Bash(~/.claude/Skills/MSOffice/venv/bin/python:*)
---

# MS Office Document Generator

Creates professional Word (.docx) and PowerPoint (.pptx) documents.

## Workflow Selection

| User Intent | Workflow | Output |
|-------------|----------|--------|
| "document", "report", "word", "write up" | Templates/Word.md | .docx |
| "presentation", "slides", "powerpoint", "deck" | Templates/PowerPoint.md | .pptx |

## Quick Reference

**Tool Location**: `~/.claude/Skills/MSOffice/Tools/generate.py`
**Python Interpreter**: `~/.claude/Skills/MSOffice/venv/bin/python`
**Output Directory**: `~/Downloads/` (for review before delivery)

## Usage Pattern

1. **Understand** the user's topic and document requirements
2. **Research** the topic if needed (use Research skill for comprehensive content)
3. **Structure** content into the appropriate JSON format
4. **Generate** document using the CLI tool
5. **Inform** user of file location

## Document Delivery

Files are saved to `~/Downloads/` by default. User can:
- Access locally on Mac
- Download via Kai Mobile App (browse to ~/Downloads/, tap file, download)

## CLI Usage

```bash
# Word document
~/.claude/Skills/MSOffice/venv/bin/python ~/.claude/Skills/MSOffice/Tools/generate.py \
  --type word \
  --title "Document Title" \
  --content '{"sections": [...]}' \
  --output ~/Downloads/filename.docx

# PowerPoint
~/.claude/Skills/MSOffice/venv/bin/python ~/.claude/Skills/MSOffice/Tools/generate.py \
  --type powerpoint \
  --title "Presentation Title" \
  --content '{"slides": [...]}' \
  --output ~/Downloads/filename.pptx
```
