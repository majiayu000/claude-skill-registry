---
name: doc-to-markdown
description: "Read or convert any document a research workflow hands you — PDF, Word, PowerPoint, Excel, OpenDocument, RTF, EPUB, or CSV. Use whenever a document has to be read, opened, quoted, summarized, searched, extracted, or added to a source library. Decides whether to read the file directly or convert it, picks the converter from the document's actual structure, and decides whether the resulting Markdown is a tracked artifact or a scratch file to delete."
---

# Reading and Converting Documents

## Instructions

### 1. Decide whether to convert at all

Conversion is a cost, not a default. Read the file directly when the question is bounded and the runtime can open the format — direct reading preserves figures, equations, and layout that no text conversion keeps, and lets you work a page range at a time. Where the runtime cannot open PDFs directly, convert, but convert only the pages you need.

**Read directly** when the document is under ~20 pages and the task is one pass over it (summarize, answer a question, check a claim, review a draft), when the payload is visual (figures, plots, scanned tables, slides), or when you need a page number you can cite.

**Convert** when the document is longer than one read comfortably spans, when the text will be searched or quoted repeatedly, when it joins a corpus or source library, when many documents get the same treatment, or when a downstream tool (grep, a classifier, a script) needs plain text. `$citation-check` and `$fact-check` both require converted Markdown, one file per source.

State which path you took in one line. Silently converting a two-page memo wastes a step; silently reading page 1 of a 300-page book and answering as if you read it all is worse.

### 2. Route by what the document actually is, not by its extension

Probe first — the extension says nothing about structure:

```bash
pdfinfo doc.pdf | grep -E '^(Pages|Encrypted)'
pages=$(pdfinfo doc.pdf | awk '/^Pages:/{print $2}')
chars=$(pdftotext -q doc.pdf - | wc -c)
echo "$((chars / pages)) chars/page"   # < 300 means image-only, needs OCR
```

| Document | Tool | Why |
|---|---|---|
| Born-digital PDF, prose-dominant (articles, books, reports) | `opendataloader-pdf -f markdown` | Keeps paragraph boundaries and does not invent tables |
| PDF whose payload is tables (questionnaires, appendices, statistical tables) | `npx -y @firecrawl/anydoc` | Real tables come out as real columns |
| Office and e-book formats (.docx, .pptx, .xlsx, .odt, .ods, .odp, .rtf, .epub, .csv) | `npx -y @firecrawl/anydoc` | One local MIT Rust binary covers all 14 formats, sub-second, no model weights |
| Scanned or image-only PDF (< 300 chars/page) | Stop and hand off to `$vlm-ocr-pipeline` | Neither text extractor can do OCR |
| One value or one passage out of a clean PDF | `pdftotext -layout` | 30 ms, no dependencies |

Fall back to `pandoc` for .docx only when Node is unavailable; it escapes apostrophes, hard-wraps lines, and emits Pandoc-flavored rather than GitHub-flavored Markdown.

If the repo already ships a conversion script — `scripts/convert-sources.sh` and a `sources/og` + `sources/md` pair is the house layout — run that script instead of a bare converter. It encodes the project's naming and output conventions, and bypassing it produces files the rest of the pipeline cannot find.

### 3. Know each converter's failure mode

These are measured on the library's own corpus of political-science PDFs, not vendor claims:

- **`opendataloader-pdf` leaves typographic ligatures intact.** One 30-page article carried 426 raw `ﬁ`/`ﬀ`/`ﬃ` characters, so `grep significant` silently misses every hit. Normalize every conversion: `python3 -c "import sys,unicodedata; sys.stdout.write(unicodedata.normalize('NFKC', open(sys.argv[1]).read()))" in.md > out.md`. Verify with `grep -c 'ﬁ\|ﬂ\|ﬀ\|ﬃ'` — the answer must be 0.
- **`opendataloader-pdf` fails silently on scanned PDFs.** A 28-page image-only article produced 2.5 KB of noise and exit code 0. Always run the chars-per-page probe first; never trust a short output.
- **`opendataloader-pdf` under-detects section headings** on some layouts, emitting the title as the only `#`. Check the heading count before relying on the Markdown for structure-aware chunking.
- **`anydoc` invents tables out of two-column prose and footnote blocks**, shredding sentences into pipe cells. On the same article it emitted 24 table rows where the PDF has no tables at all. Grep the output for `^|` and read what it caught before trusting it on a prose document.
- **`anydoc` merges a whole page into one line**, running headers and footnotes into the middle of body paragraphs — fine for retrieval, wrong for quotation and for anything that reads paragraph structure.
- **`anydoc` errors loudly on image-only PDFs** (`OCR is required`, exit 1). That is a feature: use it as a cheap scanned-document detector.

After any conversion, spot-check the head, the tail, and one middle page against the original. Converters truncate, drop columns, and reorder without complaining.

### 4. Decide whether the Markdown persists or is thrown away

Make this call yourself, then say which way you went and where the file is.

**Persist** — write into the project and keep it — when any of these hold:

- The repo has a source-library convention (`sources/md/`, `knowledge_base/md/`, a `convert-sources.sh`). Write there, under the repo's naming scheme (`author-year-slug.md`, up to three authors, then `firstauthor-etal-year-slug`).
- The document is a cited source for a manuscript, or will be quoted, coded, or fact-checked.
- The document will be read again — a corpus, a literature review, a multi-session project.
- Conversion was expensive: OCR, a VLM run, a long book, a manual repair pass.

**Use a scratch file and delete it when done** when any of these hold:

- The document lives outside the project (Downloads, an email attachment, `/tmp`) and the task is one question about it.
- Conversion is cheap and exactly reproducible from a file that is not going anywhere.
- The request is transient — "what does this say about X", "check this number".
- The document is third-party copyrighted material and the repo does not already track converted sources. Repos that keep originals gitignored and conversions tracked have made that call deliberately; a repo with no such convention has not.

When in doubt, persist inside the project and tell the user, since a stray Markdown file is cheap and a re-run of a 40-minute OCR job is not. Two rules hold either way: never write into a git-tracked directory without saying so, and never delete or move the source document.

### 5. Record what produced the file

A converted document is derived data, and a reader six months on cannot tell a clean extraction from a mangled one. For anything persisted, note the converter and version — in the file's front matter, in `sources/README.md`, or in the conversion log the repo already keeps. When a document needed OCR, that fact travels with it; downstream text analysis has to know it is working from OCR output.

Bulk intake of many sources at once is `$research-repo`'s job, not this skill's. Cleaning OCR output is `$post-ocr-cleanup`'s.

## Quality Checks

- [ ] **Read-versus-convert decided explicitly** and stated, not defaulted to conversion
- [ ] **Structure probed before routing:** page count and chars-per-page checked, image-only documents caught before a text extractor ran
- [ ] **Repo's own conversion script used** when the project ships one
- [ ] **Ligatures normalized:** `grep -c 'ﬁ\|ﬂ\|ﬀ\|ﬃ'` returns 0
- [ ] **Output spot-checked** at head, tail, and one middle page against the original
- [ ] **Tables inspected** if the output contains any, and confirmed to correspond to tables in the source
- [ ] **Persist-or-discard decided, stated, and acted on** — scratch files actually deleted
- [ ] **Naming convention followed** for anything written into a source library
- [ ] **Provenance recorded** for persisted conversions, including whether OCR was involved
- [ ] **Source document untouched**
