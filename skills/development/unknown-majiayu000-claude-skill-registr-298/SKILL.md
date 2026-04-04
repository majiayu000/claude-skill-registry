---
name: document-converter
description: Convert between Markdown, DOCX, and PDF formats bidirectionally. Handles text extraction from PDF/DOCX, markdown to document conversion. Use when converting document formats or extracting structured content from Word or PDF files.
allowed-tools: Bash, Read, Glob, Write
dependencies:
  - pandoc>=2.0
  - python3>=3.8
  - markitdown (optional, recommended)
  - pymupdf4llm (optional, recommended)
  - google-genai (optional, for enhanced PDF conversion)
  - pdf2docx (optional, for PDF to DOCX)
model: haiku-4.5
model-justification: Orchestrates external conversion tools with minimal AI reasoning required
fallback-model: sonnet-4.5
---

# Document Converter Skill

Convert documents bidirectionally between Markdown, DOCX, and PDF formats. This skill automatically detects optimal conversion tools, handles batch processing, and ensures quality output with appropriate fallback mechanisms.

## Core Capabilities

### Conversion Modes

The skill supports two conversion modes:

**Default Mode (API)**: When GEMINI_API_KEY is set, PDF-to-Markdown conversions use Google Gemini API for significantly improved quality (+20-30% fidelity). Other conversions use local tools.

**Offline Mode**: Use --no-api flag or set CONVERT_DOCS_OFFLINE=true to disable all API calls. All conversions use local tools only.

### Conversion Directions

**TO Markdown** (text extraction from documents):
- DOCX → Markdown (MarkItDown or Pandoc)
- PDF → Markdown (Gemini API, PyMuPDF4LLM, or MarkItDown)

**FROM Markdown** (document generation):
- Markdown → DOCX (Pandoc)
- Markdown → PDF (Pandoc with Typst or XeLaTeX)

**Direct Conversion**:
- PDF → DOCX (pdf2docx - direct conversion preserves layout)

### Features

- Automatic tool detection and selection
- Cascading fallback mechanisms
- Batch processing support
- Image extraction and embedding
- Filename sanitization (spaces to underscores)
- Quality validation and reporting
- Concurrent conversion support

## Tool Priority Matrix

The skill uses intelligent tool selection based on format and quality metrics:

### PDF → Markdown (Mode-Dependent)

**Gemini Mode** (when GEMINI_API_KEY is set):
1. **Gemini API** (primary) - 95%+ fidelity
   - Vision-based understanding of layout
   - Semantic structure preservation
   - Code block language detection
   - 60 req/min, 1000 req/day free tier
2. **PyMuPDF4LLM** (fallback) - 70-75% fidelity
3. **MarkItDown** (fallback) - 65-70% fidelity

**Offline Mode** (--no-api or no API key):
1. **PyMuPDF4LLM** (primary) - 70-75% fidelity
   - Zero configuration required
   - Perfect Unicode preservation
   - Good for simple PDFs
2. **MarkItDown** (fallback) - 65-70% fidelity
   - Consistent quality across document types
   - Easy to configure

### PDF → DOCX
1. **pdf2docx** (only option) - 80-85% fidelity
   - Direct conversion (no intermediate format)
   - Preserves images and layout better than Gemini->Pandoc
   - Fast processing

### DOCX → Markdown
1. **MarkItDown** (primary) - 75-80% fidelity
   - Perfect table preservation (pipe-style markdown)
   - Excellent Unicode/emoji support
   - Fast processing
2. **Pandoc** (fallback) - 68% fidelity
   - Reliable baseline conversion
   - Tables converted to grid format

### Markdown → DOCX
1. **Pandoc** (only option) - 95%+ quality preservation

### Markdown → PDF
1. **Pandoc + Typst** (primary) - Fast, modern PDF engine
2. **Pandoc + XeLaTeX** (fallback) - Traditional LaTeX engine

## Usage Patterns

### Basic Conversion

```bash
# Source conversion core library
source /home/benjamin/.config/.claude/lib/convert/convert-core.sh

# Detect available tools
detect_tools

# Convert DOCX/PDF to Markdown
main_conversion /path/to/documents /path/to/output

# Convert Markdown to DOCX
main_conversion /path/to/markdown /path/to/output
```

### Batch Processing

The conversion core automatically processes all files in the input directory:
- Discovers all convertible files (.docx, .pdf, or .md)
- Detects conversion direction automatically
- Processes files concurrently (default: 4 parallel conversions)
- Generates conversion.log with statistics

### Progress Streaming

The conversion script emits PROGRESS markers:
```
[PROGRESS] Converting: file1.docx → file1.md
[PROGRESS] Converting: file2.pdf → file2.md (2/10)
[SUCCESS] Converted file1.docx → file1.md
[FAILED] file3.pdf: Conversion timeout after 300s
```

## Conversion Workflow

### Phase 1: Tool Detection
- Check for MarkItDown availability (`command -v markitdown`)
- Check for Pandoc availability (`command -v pandoc`)
- Check for PyMuPDF4LLM availability (`python3 -c "import pymupdf4llm"`)
- Check for PDF engines (Typst, XeLaTeX)
- Set availability flags for tool selection

### Phase 2: File Discovery
- Scan input directory for convertible files
- Detect conversion direction (TO_MARKDOWN or FROM_MARKDOWN)
- Validate mixed-mode errors (cannot mix directions)
- Create output directory structure

### Phase 3: Conversion Execution
- Process files using optimal tool based on priority matrix
- Apply timeout limits (60s DOCX, 300s PDF, 120s MD→PDF)
- Handle collisions (overwrite or skip existing files)
- Extract/embed images appropriately
- Retry with fallback tools on failure

### Phase 4: Validation
- Verify output file exists
- Check for broken image links
- Validate document structure (headings present)
- Report any quality issues

### Phase 5: Reporting
- Generate conversion.log with statistics
- Report success/failure counts by format
- List timeout occurrences
- Summarize validation issues

## Quality Considerations

### Fidelity Expectations
- DOCX→Markdown: 75-80% with MarkItDown (best tables)
- PDF→Markdown: Varies by PDF complexity (scan quality critical)
- Markdown→DOCX: 95%+ with Pandoc (excellent preservation)
- Markdown→PDF: High quality with Typst/XeLaTeX engines

### Known Limitations
- **Scanned PDFs**: OCR quality depends on scan resolution
- **Complex layouts**: Multi-column or nested tables may degrade
- **Embedded fonts**: PDF fonts may affect text extraction accuracy
- **Images**: Large images may cause timeout issues

### Best Practices
- Use MarkItDown for DOCX/PDF when available (better quality)
- Allow longer timeouts for large PDFs (300s default)
- Review conversion.log for failure patterns
- Test output files for critical conversions

## Error Handling

### Common Errors

**Tool not available**:
```
Error: No conversion tool available for DOCX→Markdown
Required: markitdown or pandoc
```
→ Install required tools

**Conversion timeout**:
```
[FAILED] large_document.pdf: Conversion timeout after 300s
```
→ Increase TIMEOUT_PDF_TO_MD or use simpler PDF

**Validation failure**:
```
[WARNING] output.md: No headings found (possible conversion issue)
```
→ Check source document structure

### Recovery Strategies
- Failed conversions automatically retry with fallback tool
- Timeouts skip to next file (batch processing continues)
- Validation warnings don't block workflow (reported only)

## Configuration Options

Environment variables to tune conversion behavior:

```bash
# Timeout multipliers (seconds)
TIMEOUT_MULTIPLIER=1.5  # Increase all timeouts by 50%

# Disk usage limits
MAX_DISK_USAGE_GB=10  # Abort if output exceeds 10GB
MIN_FREE_SPACE_MB=500  # Require 500MB free space

# Concurrency
MAX_CONCURRENT_CONVERSIONS=4  # Parallel conversion limit
```

## Integration Examples

### From Claude Code Agents

When working within agent contexts, the skill automatically triggers when Claude detects conversion needs:

```markdown
User: "Extract text from these PDF reports"
→ Skill auto-invokes: document-converter
→ Converts PDFs to Markdown
→ Returns structured text
```

### From Slash Commands

The `/convert-docs` command delegates to this skill when available:

```bash
/convert-docs ./documents ./output
→ Checks skill availability
→ Delegates to document-converter skill
→ Falls back to script mode if skill unavailable
```

### From Other Skills

Skills can compose with document-converter:

```yaml
# research-specialist skill
dependencies:
  - document-converter  # Auto-loads for PDF analysis
```

## Script Locations

The skill relies on conversion scripts in the project:

- **Core orchestration**: `.claude/lib/convert/convert-core.sh`
- **DOCX functions**: `.claude/lib/convert/convert-docx.sh`
- **PDF functions**: `.claude/lib/convert/convert-pdf.sh`
- **Gemini wrapper**: `.claude/lib/convert/convert-gemini.sh`
- **Gemini Python**: `.claude/lib/convert/convert_gemini.py`
- **Markdown utilities**: `.claude/lib/convert/convert-markdown.sh`

Scripts are symlinked in the skill's `scripts/` directory for easy access.

## Testing

Test the skill with sample conversions:

```bash
# Test DOCX→Markdown
/convert-docs ./test/sample.docx ./output

# Test PDF→Markdown
/convert-docs ./test/report.pdf ./output

# Test Markdown→DOCX
/convert-docs ./test/document.md ./output

# Batch test
/convert-docs ./test/documents ./output
```

Verify:
- Conversion.log generated with statistics
- Output files created with correct extensions
- Image directories created when needed
- Quality meets expectations (check tables, formatting)

## Troubleshooting

### Skill Not Triggering

If the skill doesn't auto-invoke when expected:
- Check description includes trigger keywords (convert, document, PDF, DOCX, Markdown)
- Test with explicit skill invocation: "Use document-converter skill"
- Verify skill is in `.claude/skills/` directory (project-level)

### Tool Installation

**MarkItDown** (recommended):
```bash
pip install markitdown
```

**PyMuPDF4LLM** (optional):
```bash
pip install pymupdf4llm
```

**pdf2docx** (optional, for PDF to DOCX):
```bash
pip install pdf2docx
```

**google-genai** (optional, for Gemini API):
```bash
pip install google-genai

# Set API key (free tier available at https://aistudio.google.com/)
export GEMINI_API_KEY="your-api-key"
```

**Pandoc** (required):
```bash
# Ubuntu/Debian
apt install pandoc

# macOS
brew install pandoc
```

**Typst** (optional, for MD→PDF):
```bash
# Ubuntu/Debian
wget https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz
tar -xf typst-*.tar.xz && sudo mv typst-*/typst /usr/local/bin/

# macOS
brew install typst
```

### Performance Issues

If conversions are slow:
- Reduce MAX_CONCURRENT_CONVERSIONS (lower parallelism)
- Increase timeout values for large files
- Check disk I/O (slow storage may bottleneck)
- Use PyMuPDF4LLM for simple PDFs (faster than MarkItDown)

## See Also

- [reference.md](./reference.md) - Detailed tool documentation and metrics
- [examples.md](./examples.md) - Usage examples and common patterns
- [Convert-Docs Command Guide](../../docs/guides/commands/convert-docs-command-guide.md)
- [MarkItDown Documentation](https://github.com/microsoft/markitdown)
- [Pandoc Manual](https://pandoc.org/MANUAL.html)
