---
name: book-analyzer
description: >-
  Analyze a book (EPUB/PDF) and generate detailed chapter-by-chapter notes
  with extracted key concepts. Use when given a book file path to process.
disable-model-invocation: true
argument-hint: "[path/to/book.epub or book.pdf]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent, TodoWrite
---

<Purpose>
Full autonomous analysis of book files (EPUB/PDF) into structured notes.
Extracts text, detects chapters, analyzes each chapter via parallel agents,
synthesizes across chapters, and optionally integrates into an Obsidian vault
with wikilinks and extracted Term notes.
</Purpose>

<Use_When>
- User provides a path to an EPUB or PDF book file
- User says "analyze this book", "process this book", "read this book"
- User wants structured notes from a book-length document (20+ pages)
</Use_When>

<Do_Not_Use_When>
- Short documents under 20 pages — use /paper or /process instead
- User wants to read or search specific sections — just use Read tool directly
- User wants EPUB output from markdown — wrong direction
- URL-only input with no file on disk — use /research instead
</Do_Not_Use_When>

<Why_This_Exists>
Book notes that merely transcribe content are useless — the value is in synthesis.
Most book notes in a vault end up sparse because processing a full book manually is
exhausting. This skill automates the mechanical work (extraction, splitting, formatting)
while delegating the intellectual work (synthesis, assessment, connections) to specialized
agents with strict quality constraints.
</Why_This_Exists>

<Execution_Policy>
- Run extraction scripts first, verify output before proceeding to analysis
- Delegate chapter analysis to parallel agents (one per chapter, all simultaneous)
- Use Sonnet for chapter analysis, Opus for cross-book synthesis
- Vault integration is conditional — detect .obsidian/ or CLAUDE.md in working directory
- Report progress via TodoWrite at each stage transition
- If extraction fails, stop and report — don't guess at content
- Total chapters capped at 50 — if more, group adjacent chapters into batches
</Execution_Policy>

<Steps>

## Stage 1: PARSE ARGUMENTS AND EXTRACT

Parse `$ARGUMENTS` to get the book file path and optional flags.

**Argument format:**
```
$ARGUMENTS = "path/to/book.epub"                    # basic
$ARGUMENTS = "path/to/book.pdf --no-terms"          # skip term extraction
$ARGUMENTS = "path/to/book.epub --output ~/Desktop/" # custom output location
```

**Parse logic:**
1. Split $ARGUMENTS by spaces, treating quoted paths as single tokens
2. First non-flag token = file path (REQUIRED — stop if missing)
3. Optional flags: `--no-terms` (skip concept extraction), `--output <dir>` (custom output)
4. Detect format from file extension: `.epub`, `.pdf`, `.mobi`

**Run extraction based on format:**

For EPUB:
```bash
SKILL_DIR="$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")")"
# Find skill directory — check common locations
for dir in .claude/skills/book-analyzer ~/.claude/skills/book-analyzer; do
  if [ -f "$dir/scripts/extract_epub.py" ]; then SKILL_DIR="$dir"; break; fi
done
WORK_DIR=".book-work-$(date +%s)"
python3 "$SKILL_DIR/scripts/extract_epub.py" "INPUT_PATH" "$WORK_DIR"
```

For PDF:
```bash
WORK_DIR=".book-work-$(date +%s)"
"$SKILL_DIR/scripts/extract_pdf.sh" "INPUT_PATH" "$WORK_DIR"
```

For MOBI: Convert to EPUB first with `ebook-convert` (calibre), then run EPUB extraction.

The work directory is created inside the vault root (e.g., `.book-work-1709398200/`).
Clean it up after the pipeline completes.

**After extraction:** Read `$WORK_DIR/metadata.json` to verify success.

**PDF fallback:** If metadata shows `"needs_fallback": true`, use the Claude Read tool instead:
- Read the PDF 20 pages at a time: `Read(file_path="INPUT_PATH", pages="1-20")`, then `pages="21-40"`, etc.
- Write each batch to `$WORK_DIR/pages/page_batch_NNN.txt`
- Update metadata with actual content

## Stage 2: STRUCTURE

Read `metadata.json` from the extraction output.

**For EPUBs:** Chapter structure comes directly from extraction (H1/H2 splitting). Proceed to Stage 3.

**For PDFs:** Chapter detection depends on extraction quality.
- If pages have clear chapter headings, group pages into chapters
- If no clear structure: Launch a single agent to read the first 5 pages and detect chapter boundaries:

```
Agent(
  subagent_type="general-purpose",
  model="haiku",
  prompt="Read the following text from the first 5 pages of a book. Identify chapter
  boundaries and return a JSON array of {title, start_page, end_page} objects.
  If no chapters are detectable, return [{title: 'Full Text', start_page: 1, end_page: LAST}].

  TEXT:
  [first 5 pages content]"
)
```

- Update metadata with detected chapter list
- Group page files into chapter files by concatenation

**Result:** A `chapters/` directory with one file per chapter, and updated `metadata.json`.

## Stage 3: ANALYZE (parallel, file-based)

Read the agent definition from `agents/chapter-analyst.md` in the skill directory.

**Create analyses directory:**
```bash
mkdir -p "$WORK_DIR/analyses"
```

For EACH chapter, launch a parallel agent that WRITES ITS OUTPUT TO A FILE:

```
Agent(
  subagent_type="general-purpose",
  model="sonnet",
  run_in_background=true,
  prompt="You are Chapter Analyst. Follow these instructions exactly:

  [INSERT FULL CONTENT OF agents/chapter-analyst.md HERE]

  BOOK CONTEXT:
  - Title: {title}
  - Author: {author}
  - This is Chapter {N} of {total_chapters}
  - Table of Contents: {chapter_list summary}

  CHAPTER FILE TO READ: {path to chapter .md file}
  OUTPUT_FILE: $WORK_DIR/analyses/ch{NN}_analysis.md

  CRITICAL: Read the chapter file, produce your analysis, then WRITE it to OUTPUT_FILE using the Write tool. Be detailed — include all interesting quotes, concrete examples, and anecdotes. The master agent will read your file later."
)
```

**Parallel execution:** Launch ALL chapter agents simultaneously with `run_in_background=true`.
Wait for all to complete. Verify all analysis files exist in `$WORK_DIR/analyses/`.

**Why file-based:** Agent return messages get truncated by context compression. Writing to files preserves full detail — every quote, every example, every nuance. The master agent reads these files directly.

**Chapter cap:** If more than 50 chapters, batch adjacent chapters (2-3 per agent) to stay within limits.

**Result:** One analysis file per chapter in `$WORK_DIR/analyses/`, each containing detailed notes with quotes.

## Stage 4: SYNTHESIZE + SECTION WRITE (parallel)

This stage runs the cross-book synthesizer AND section writers ALL IN PARALLEL.

**Batching formula:** Divide chapters into batches of ~5 chapters each.
`M = min(max(ceil(N/5), 1), 10)` where N = total number of chapters.

**Create sections directory:**
```bash
mkdir -p "$WORK_DIR/sections"
```

Read agent definitions from `agents/book-synthesizer.md` and `agents/section-writer.md`.

**Launch ALL of the following simultaneously (one message, all with `run_in_background=true`):**

### 4a. Book Synthesizer (Opus)

```
Agent(
  subagent_type="general-purpose",
  model="opus",
  run_in_background=true,
  prompt="You are Book Synthesizer. Follow these instructions exactly:

  [INSERT FULL CONTENT OF agents/book-synthesizer.md HERE]

  BOOK METADATA:
  - Title: {title}
  - Author: {author}
  - Total chapters: {N}

  ANALYSIS FILES DIRECTORY: $WORK_DIR/analyses/
  Read ALL .md files in this directory.

  OUTPUT_FILE: $WORK_DIR/synthesis.md
  Write your synthesis to this file.

  IMPORTANT: Per-chapter detail is handled by section writer agents.
  Your job is ONLY cross-chapter patterns: Core Thesis, Deepest Insights,
  Chapter Map, Critical Assessment, Cross-Domain Connections."
)
```

### 4b. Section Writers (Sonnet, one per batch)

For each batch of ~5 chapters:

```
Agent(
  subagent_type="general-purpose",
  model="sonnet",
  run_in_background=true,
  prompt="You are Section Writer. Follow these instructions exactly:

  [INSERT FULL CONTENT OF agents/section-writer.md HERE]

  BOOK CONTEXT:
  - Title: {title}
  - Author: {author}

  YOUR ASSIGNED CHAPTER ANALYSES (read ALL of these):
  - $WORK_DIR/analyses/ch{NN}_analysis.md
  - $WORK_DIR/analyses/ch{NN}_analysis.md
  - ... (list all files in this batch)

  OUTPUT_FILE: $WORK_DIR/sections/part_{MM}.md

  CRITICAL: Read each chapter analysis file. Format ALL their content into
  vault-ready markdown preserving every key idea, every quote (in > blockquote
  format), every example, and every anecdote. Your job is FORMATTING, not
  summarizing. Write output to OUTPUT_FILE."
)
```

**Example for a 20-chapter book (4 section writers):**
- Section Writer 1: ch01-ch05 → sections/part_01.md
- Section Writer 2: ch06-ch10 → sections/part_02.md
- Section Writer 3: ch11-ch15 → sections/part_03.md
- Section Writer 4: ch16-ch20 + postscript → sections/part_04.md

**Result:** `synthesis.md` + `sections/part_01.md` through `sections/part_MM.md`, all written in parallel.

## Stage 4.5: ASSEMBLE FINAL NOTE (lightweight concatenation)

The master agent reads all section files and the synthesis, then assembles the final note.

**This step is mostly CONCATENATION, not generation.** The section writers already produced vault-ready markdown. The master agent's job is:

1. Read `$WORK_DIR/synthesis.md`
2. Read ALL `$WORK_DIR/sections/part_*.md` files in order
3. Assemble the final note structure:
   - Core Thesis (from synthesis)
   - Deepest Insights (from synthesis)
   - How the Argument Builds / Chapter Map (from synthesis)
   - `---`
   - Chapter Notes: **COPY section files VERBATIM** — do NOT summarize or compress
   - `---`
   - Critical Assessment (from synthesis)
   - Cross-Domain Connections (from synthesis)
   - Questions: extract from `<!-- QUESTIONS: ... -->` HTML comments in section files, deduplicate, add synthesis questions
   - Related Links: wikilinks to related vault notes
4. Extract key terms from `<!-- TERMS: ... -->` HTML comments for Stage 5 concept extraction

**CRITICAL RULE:** Chapter note content from section files must be copied VERBATIM into the final note. The assembly agent must NOT summarize, compress, or reduce the section content. If a section file has 15 bullets for a chapter, the final note has 15 bullets for that chapter.

## Stage 4.6: VERIFY FINAL NOTE (quality gate)

Before proceeding to integration or cleanup, verify the assembled note:

1. **Completeness check:** Every chapter should have a `### Ch` heading in the final note. Count the headings and compare to total chapters from metadata.
2. **Quote format check:** All quotes should use `>` blockquote syntax. Look for `"` patterns that aren't inside blockquotes.
3. **Detail preservation:** The Chapter Notes section should be substantially longer than the synthesis sections. If the chapter notes are shorter than the synthesis, something went wrong — the section content was compressed.
4. **Section presence:** Verify these sections exist: Core Thesis, Deepest Insights, Chapter Notes, Critical Assessment, Cross-Domain Connections, Questions.
5. **Length sanity:** Expect ~300-500 words per chapter analyzed. A 20-chapter book should produce ~6,000-10,000 words of chapter notes.

If any check fails, fix the issue using Edit before proceeding. Do NOT delete the work directory until verification passes.

## Stage 5: INTEGRATE

**Detect vault context:** Check if `.obsidian/` directory or `CLAUDE.md` file exists in the current working directory.

### If in vault context (Obsidian):

1. **Create book note** via `create-note.py`:
   ```bash
   python3 .claude/scripts/create-note.py book "{Title}" author="{Author}" year={YEAR}
   ```
   Script outputs the created file path. The template handles frontmatter (id, dates, type) automatically.

2. **Fill the book note body** using Edit tool on the created file:
   - Add `processing_status: inbox` to frontmatter
   - Compose body sections: Core Thesis → Key Themes → Chapter Notes → Critical Assessment → Cross-Domain Connections → Questions
   - Add topic tags to the `🏷️Tags` line (e.g., `#psychology`, `#startup`)
   - Use `[[short-form wikilinks]]` for all internal references

3. **Extract concepts** (unless `--no-terms` flag):
   Read agent definition from `agents/concept-extractor.md`, then:

   ```
   Agent(
     subagent_type="general-purpose",
     model="sonnet",
     prompt="You are Concept Extractor. Follow these instructions exactly:

     [INSERT FULL CONTENT OF agents/concept-extractor.md HERE]

     VAULT ROOT: [current working directory]
     BOOK NOTE TITLE: {Title}

     ALL KEY TERMS FROM CHAPTER ANALYSES:
     [INSERT COLLECTED KEY TERMS HERE]

     Use create-note.py to create new Term notes:
       python3 .claude/scripts/create-note.py term 'Term Name' processing_status=processed
     Then Edit the created file to fill in definition, example, tags, and links.

     Search the vault for existing terms using Grep and Glob.
     Report what was found, created, and skipped."
   )
   ```

4. **Report results:**
   - Book note wikilink: `[[{Title}]]`
   - Number of chapters analyzed
   - Number of terms extracted (existing vs new)
   - Any issues encountered

### If NOT in vault context (plain markdown):

1. **Assemble markdown file** using the format from `references/note-templates.md` (Section 2)
2. **Write** to `./book-analysis-{slug}.md` (or `--output` dir if specified)
3. **Skip term extraction** (no vault to search)
4. **Report** output file location

</Steps>

<Tool_Usage>
- **Bash**: Run extraction scripts, run `create-note.py`, check tool availability
- **Read**: Read extracted chapters, metadata.json, agent definitions, PDF pages (fallback)
- **Edit/Write**: Fill note body after `create-note.py` creates the skeleton
- **Agent**: Delegate to chapter-analyst (sonnet, parallel), book-synthesizer (opus, parallel), section-writer (sonnet, parallel), concept-extractor (sonnet)
- **Grep/Glob**: Search vault for existing terms (used by concept-extractor agent)
- **TodoWrite**: Report progress at each stage

**Agent delegation pattern:**
1. Read the agent .md file from `agents/` directory
2. Include agent instructions verbatim in the prompt
3. Append book-specific context (metadata, chapter text, etc.)
4. For chapter analysis: `run_in_background=true` (parallel)
5. For synthesis + section writers: `run_in_background=true` (ALL launched in parallel in one message)
6. For concept extraction: `run_in_background=false` (sequential, after assembly)

**Work directory cleanup:** Do NOT delete `$WORK_DIR` until Stage 4.6 verification passes. If verification fails, the work directory is needed for debugging and fixing.

**Finding the skill directory:**
The skill lives at `.claude/skills/book-analyzer/` (project-level). To find it reliably:
```bash
SKILL_DIR=".claude/skills/book-analyzer"
```
Read agent definitions with: `Read(file_path="$SKILL_DIR/agents/chapter-analyst.md")`
</Tool_Usage>

<Examples>
<Good>
User: "/book-analyzer ~/Books/thinking-fast-and-slow.epub"
- Detects EPUB format, runs extract_epub.py
- Finds 38 chapters via H1 splitting
- Launches 38 parallel chapter-analyst agents (sonnet)
- Collects all analyses, launches book-synthesizer (opus)
- Detects .obsidian/ → vault mode
- Creates book note at notes/books/(Book) Thinking, Fast and Slow.md
- Extracts 12 concepts, finds 4 existing in vault, creates 8 new Term notes
- Reports: "Created book note with 38 chapters, 8 new terms, 4 linked existing terms"
</Good>

<Good>
User: "/book-analyzer paper.pdf --no-terms"
- Detects PDF, runs extract_pdf.sh
- Quality OK (no fallback needed), 45 pages detected
- No clear chapters → structure agent groups into 6 logical sections
- 6 chapter-analyst agents + 1 book-synthesizer
- --no-terms flag → skip concept extraction
- Creates book note, reports results
</Good>

<Bad>
User: "/book-analyzer notes/short-article.pdf"
- PDF is only 8 pages — this is not a book
- Should suggest: "This document is only 8 pages. Consider using /paper for academic papers or /process for existing notes instead."
</Bad>

<Bad>
User: "/book-analyzer https://example.com/book.pdf"
- URL, not a file path — no file on disk
- Should suggest: "Please provide a path to a local file. Download the PDF first, then run /book-analyzer on the downloaded file."
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- **Missing file**: If the input path doesn't exist, stop immediately and report
- **Missing pandoc/pdftotext**: If required tool isn't installed, stop and provide install instructions
- **Extraction failure**: If extraction script fails, report the error — don't proceed with empty content
- **PDF fallback too large**: If PDF is >500 pages and needs fallback (Read tool), warn user it will take a while and ask to proceed
- **No chapters detected**: If structure detection fails completely, proceed with full text as single chapter (degraded but functional)
- **Agent failure**: If a chapter-analyst agent fails, report which chapter failed and continue with others — partial results are still valuable
- **Too short**: If extracted text is under ~5000 words, suggest /paper or /process instead
</Escalation_And_Stop_Conditions>

<Final_Checklist>
- [ ] Input file exists and format detected correctly
- [ ] Extraction completed successfully (metadata.json present)
- [ ] All chapters analyzed (no silent failures)
- [ ] All section writers completed (sections/part_*.md files present)
- [ ] Synthesis covers core thesis, insights, chapter map, assessment, connections
- [ ] Section content copied VERBATIM into final note (not compressed)
- [ ] ALL quotes use `>` blockquote markdown syntax
- [ ] Stage 4.6 verification passed (completeness, formatting, length)
- [ ] Book note follows correct template (vault or generic)
- [ ] If vault: frontmatter schema matches vault conventions
- [ ] If vault: wikilinks used for internal references
- [ ] If vault: term extraction ran (unless --no-terms)
- [ ] Work directory NOT deleted until verification passes
- [ ] No hardcoded paths — all paths derived from arguments and detection
- [ ] User informed of results with file paths
</Final_Checklist>

$ARGUMENTS
