# Extraction Guide — book-analyzer pipeline reference

How the book-analyzer skill converts raw book files (EPUB, PDF) into
structured text that the analysis agents can process.

---

## 1. EPUB Extraction

**Script:** `scripts/extract_epub.py`
**Usage:** `python extract_epub.py <input.epub> <output_dir>`
**Dependency:** pandoc 3.4+ must be on PATH.

### Pipeline

1. **Pandoc conversion** — converts the EPUB to a single markdown string
   using `pandoc <file> -t markdown --wrap=none`. The `--wrap=none` flag
   prevents pandoc from inserting hard line breaks, preserving the
   original paragraph structure.

2. **Metadata extraction** — pulls title and author from the EPUB's
   internal metadata via pandoc. Uses a custom `--template` string to
   extract just the title and author fields. Falls back to parsing a
   YAML metadata dump (`--dump-metadata`) if the template approach
   returns nothing. Handles authors stored as both single strings and
   YAML lists.

3. **Chapter splitting** — splits the markdown into chapters using a
   three-level fallback:
   - **H1 first:** counts `# Heading` lines. If there are 2 or more H1
     headings and splitting on them produces 2+ chapters, use H1.
   - **H2 fallback:** if H1 splitting fails, try `## Heading` with the
     same 2+ threshold.
   - **Whole-text fallback:** if neither heading level produces usable
     splits, return the entire text as a single chapter titled
     "Full Text".

   Content before the first heading is captured as "Front Matter" only
   if it exceeds 50 characters (skips trivial preamble).

4. **Output structure** — writes to `<output_dir>/`:
   ```
   output_dir/
     full_text.md          # complete markdown, unsplit
     metadata.json         # title, author, total_chapters, chapter_list, format
     chapters/
       ch01_<slug>.md      # each chapter as a separate file
       ch02_<slug>.md
       ...
   ```
   Filenames are slugified (lowercased, non-alphanumeric stripped,
   spaces to underscores). The `metadata.json` file contains a
   `chapter_list` array where each entry has `number`, `title`, and
   `file` (relative path to the chapter markdown).

### metadata.json shape (EPUB)

```json
{
  "title": "Book Title",
  "author": "Author Name",
  "total_chapters": 12,
  "chapter_list": [
    { "number": 1, "title": "Chapter Title", "file": "chapters/ch01_chapter_title.md" }
  ],
  "format": "epub"
}
```

---

## 2. PDF Extraction

**Script:** `scripts/extract_pdf.sh`
**Usage:** `extract_pdf.sh <pdf_path> <output_dir>`
**Dependency:** pdftotext (from poppler). Optional: pdfinfo (also from
poppler, used for accurate page count).

### Pipeline

1. **Text extraction** — runs `pdftotext -layout <pdf> <output>/full_text.txt`.
   The `-layout` flag preserves the original spatial layout of the page
   (columns, indentation, tables) rather than reflowing text. This
   produces better results for books with complex formatting.

2. **Page count** — determined in two ways:
   - **Primary:** `pdfinfo` output, parsing the `Pages:` line.
   - **Fallback:** counts form-feed characters (`\f`, ASCII 12) in the
     extracted text and adds 1 (last page has no trailing form-feed).

3. **Quality detection** — computes two metrics to decide if the
   extraction is usable:
   - **Printable ratio:** `printable_chars / total_chars`. Characters
     matching `[:print:]\n\t` count as printable. A ratio below 0.5
     signals garbled or binary content (typical of scanned/image PDFs).
   - **Words per page:** `total_words / total_pages`. Fewer than 20
     words per page signals the PDF is image-based or the extraction
     failed to capture meaningful text.

   If either threshold is tripped, `needs_fallback` is set to `true`.

4. **Page splitting** — uses awk to split `full_text.txt` on form-feed
   characters into individual page files: `pages/page_001.txt`,
   `pages/page_002.txt`, etc.

5. **Title** — derived from the PDF filename (strips `.pdf` extension).
   No internal metadata extraction is attempted (unlike EPUB).

6. **Output structure:**
   ```
   output_dir/
     full_text.txt         # complete extracted text
     metadata.json         # title, format, total_pages, quality metrics, needs_fallback
     pages/
       page_001.txt        # per-page text files
       page_002.txt
       ...
   ```

### metadata.json shape (PDF)

```json
{
  "title": "filename-without-extension",
  "format": "pdf",
  "total_pages": 340,
  "words_per_page": 285,
  "printable_ratio": 0.97,
  "needs_fallback": false,
  "extraction_tool": "pdftotext"
}
```

---

## 3. PDF Fallback (Claude Read)

When `metadata.json` contains `"needs_fallback": true`, the pdftotext
output is unusable (scanned pages, image-heavy layouts, garbled text).
SKILL.md switches to using Claude's built-in Read tool to process the
PDF directly.

### Pagination pattern

The Read tool accepts a `pages` parameter for PDFs, with a maximum of
20 pages per request. SKILL.md reads the PDF in sequential 20-page
batches:

```
Read(file_path, pages="1-20")    # batch 1
Read(file_path, pages="21-40")   # batch 2
Read(file_path, pages="41-60")   # batch 3
...
```

Each batch is processed by the chapter-analyst agent before the next
batch is read. This keeps context manageable and avoids exceeding the
Read tool's per-request limit.

### How SKILL.md determines page ranges

1. Reads `metadata.json` to get `total_pages`.
2. Generates batch ranges: `1-20`, `21-40`, ..., up to `total_pages`.
3. For each batch, calls Read with the `pages` parameter.
4. Passes the returned content to chapter-analyst for analysis.
5. After all batches are processed, runs book-synthesizer across the
   collected chapter analyses.

### Differences from normal pipeline

- No `chapters/` directory is created — Claude reads the PDF directly.
- Chapter boundaries are inferred from content (headings, page breaks)
  rather than pre-split files.
- The chapter-analyst may receive content that spans chapter boundaries
  within a 20-page batch and must handle partial chapters gracefully.

---

## 4. Known Limitations

### Scanned PDFs (image-only)
PDFs containing only scanned page images (no text layer) will produce
empty or garbled pdftotext output. The fallback (Claude Read) can handle
these since it processes the PDF visually, but quality depends on scan
resolution and clarity. Handwritten annotations are generally not
captured.

### DRM-protected EPUBs
Pandoc cannot open DRM-protected EPUB files. The script will fail with
a pandoc error. The user must strip DRM before processing (the skill
does not do this automatically and should not attempt to).

### Image-heavy books (diagrams lost)
Both extraction paths lose visual content:
- EPUB: pandoc converts to markdown, which drops embedded images.
- PDF: pdftotext extracts text only; diagrams, charts, and figures
  are silently lost.
- Claude Read fallback: can see images in the PDF but cannot embed
  them in the output notes.

For books where diagrams carry significant meaning (e.g., statistics
textbooks, architecture books), the generated notes will have gaps.
Flag this to the user when the book appears image-heavy.

### Very large books (>1000 pages)
Books exceeding roughly 1000 pages may stress the pipeline:
- EPUB: the full markdown conversion can be very large, but chapter
  splitting keeps individual files manageable.
- PDF: the Read fallback requires 50+ batches of 20 pages each, which
  can hit context limits across the full analysis.
- Recommendation: for books over 1000 pages, consider processing in
  parts (e.g., Part I, Part II) rather than the full book at once.

### Encoding issues
Some older EPUBs use non-UTF-8 encodings. Pandoc handles most cases,
but occasionally produces mojibake (garbled characters). If the output
contains systematic encoding artifacts, the user may need to re-encode
the source file.

---

## 5. Dependencies

| Dependency | Version | Required for | Install |
|---|---|---|---|
| **pandoc** | 3.4+ | EPUB extraction | `brew install pandoc` (macOS) / `apt install pandoc` (Ubuntu) |
| **pdftotext** | any (via poppler) | PDF text extraction | `brew install poppler` (macOS) / `apt install poppler-utils` (Ubuntu) |
| **pdfinfo** | any (via poppler) | PDF page count (optional) | installed with poppler |
| **Python** | 3.8+ | `extract_epub.py` | system Python or `brew install python` |
| **awk** | any POSIX awk | PDF page splitting | pre-installed on macOS and Linux |

### Graceful error handling

Both scripts check for their required dependencies at startup:
- `extract_epub.py` calls `shutil.which("pandoc")` and exits with a
  clear error message if pandoc is not found.
- `extract_pdf.sh` uses `command -v pdftotext` and exits with
  platform-specific install instructions if pdftotext is missing.

The `pdfinfo` dependency is optional — if missing, the script falls back
to counting form-feed characters for the page count. This fallback is
reliable for most PDFs.

### Version notes

- **pandoc 3.4+** is recommended because earlier versions have
  inconsistent EPUB metadata extraction. The `--template` approach for
  metadata relies on template variable syntax that stabilized in 3.x.
- **Python 3.8+** is the minimum because `extract_epub.py` uses
  f-strings and `subprocess.run` with `capture_output=True` (added in
  3.7, but 3.8 is the practical floor for maintained Python versions).
