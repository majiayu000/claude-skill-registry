# book-analyzer

A Claude Code skill that autonomously analyzes EPUB and PDF books, producing structured chapter-by-chapter notes with extracted key concepts.

## What it does

Given a book file on disk, the skill runs a 5-stage pipeline:

1. **Extract** — Converts EPUB (via pandoc) or PDF (via pdftotext) to plain text, splits into chapters
2. **Structure** — Detects chapter boundaries from headings or page structure
3. **Analyze** — Launches parallel agents (one per chapter) that synthesize key ideas, terms, quotes, examples, and questions
4. **Synthesize + Section Write** — Cross-book synthesis (Opus) runs in parallel with section writers (Sonnet) that format detailed chapter notes into vault-ready markdown. All run simultaneously for speed
5. **Verify + Integrate** — Quality verification ensures completeness and formatting. Then assembles a structured book note; optionally extracts key concepts into standalone Term notes with vault wikilinks

## Requirements

- **pandoc 3.4+** — Required for EPUB extraction (`brew install pandoc`)
- **pdftotext** (poppler) — Required for PDF extraction (`brew install poppler`)
- **Python 3.8+** — For the EPUB extraction script
- **Claude Code** — With skill support enabled

## Installation

This is a **project-level skill**. Place the `book-analyzer/` directory inside your project's `.claude/skills/`:

```bash
cp -r book-analyzer/ your-project/.claude/skills/book-analyzer/
```

Claude Code will auto-discover it as a project skill.

## Usage

```
/book-analyzer path/to/book.epub
/book-analyzer path/to/book.pdf
/book-analyzer path/to/book.epub --no-terms
/book-analyzer path/to/book.pdf --output ~/Desktop/
```

**Arguments:**
- First argument: path to the book file (EPUB or PDF)
- `--no-terms`: Skip concept extraction (faster, no Term notes created)
- `--output <dir>`: Write output to a specific directory instead of the default

## Output

### In an Obsidian vault (auto-detected)

- **Book note** at `notes/books/(Book) Title.md` with:
  - YAML frontmatter (type: book, author, year, processing_status)
  - Core thesis, key themes, chapter-by-chapter notes
  - Critical assessment, cross-domain connections, questions
  - Inline `#tags` and `[[wikilinks]]`
- **Term notes** for key concepts (5-15 per book), linked back to the book note

### Outside a vault

- Single markdown file with all analysis content
- No vault-specific syntax (no wikilinks, no frontmatter)

## Architecture

```
book-analyzer/
├── SKILL.md                    # Orchestration (multi-stage pipeline)
├── agents/
│   ├── chapter-analyst.md      # Per-chapter analysis (Sonnet, parallel)
│   ├── section-writer.md       # Batch chapter formatting (Sonnet, parallel)
│   ├── book-synthesizer.md     # Cross-chapter synthesis (Opus, parallel)
│   └── concept-extractor.md    # Term extraction (Sonnet)
├── references/
│   ├── extraction-guide.md     # How the extraction pipeline works
│   └── note-templates.md       # Output templates (Obsidian/generic/term)
├── scripts/
│   ├── extract_epub.py         # EPUB → chapters via pandoc
│   └── extract_pdf.sh          # PDF → pages via pdftotext
└── examples/
    └── sample-output.md        # Example output (Thinking, Fast and Slow)
```

Follows [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) skill patterns: XML-tagged SKILL.md, separate agent definitions with `<Role>`, `<Constraints>`, `<Output_Format>`, and tiered model routing.

## Known limitations

- **Scanned PDFs** (image-only) produce empty text — the skill detects this and flags `needs_fallback: true`, falling back to Claude's native PDF reader (20 pages at a time)
- **DRM-protected EPUBs** cannot be opened by pandoc
- **Image-heavy books** — Diagrams and figures are lost in text extraction
- **Very large books** (1000+ pages) may need longer processing time due to many parallel agents

## Quality principles

The skill enforces these writing standards in all agent outputs:

- **Synthesize, don't transcribe** — Notes are in the agent's voice, not copied passages
- **Lead with insight** — Every bullet starts with the key point, not context
- **One point per bullet** — If a bullet needs "and", it becomes two bullets
- **Bold key terms** — Terms that could become standalone notes are highlighted
- **Preserve all detail** — Section writers preserve all key ideas, quotes, and examples from chapter analyses. No artificial bullet caps
- **Quotes in blockquotes** — All quotes use `>` markdown blockquote syntax with context
- **Verify before cleanup** — Final note is checked for completeness and formatting before temp files are removed
- **Honest assessment** — Critical assessment includes genuine weaknesses, not just praise
