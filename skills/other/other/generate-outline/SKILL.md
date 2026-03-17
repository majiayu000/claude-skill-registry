---
name: generate-outline
description: Generate a course outline with research dossier using the VectorShift pipeline. Automatically converts and compresses files before upload.
user_invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

# Course Outline Creator (with File Conversion + Compression)

Generate a comprehensive course outline and research dossier from a topic and reference materials. Automatically converts non-PDF files (PPTX, DOCX, etc.) to PDF using LibreOffice, then compresses large PDFs (>5MB) using Ghostscript before uploading to VectorShift.

## Slash Command Usage

```
/generate-outline "<topic>" --materials <folder> [options]
```

**Examples:**
- `/generate-outline "Cardiovascular Longevity" --materials "course materials/"`
- `/generate-outline "Peptide Therapy Fundamentals" --materials "/path/to/materials/" --dry-run`
- `/generate-outline "Topic" --materials "/materials/" --outline existing_outline.md`

## Supported File Types

| Extension | Type | Processing |
|-----------|------|------------|
| `.pdf` | PDF | Compress only |
| `.pptx`, `.ppt` | PowerPoint | Convert to PDF, then compress |
| `.docx`, `.doc` | Word | Convert to PDF, then compress |
| `.xlsx`, `.xls` | Excel | Convert to PDF, then compress |
| `.odt` | OpenDocument Text | Convert to PDF, then compress |
| `.odp` | OpenDocument Presentation | Convert to PDF, then compress |
| `.ods` | OpenDocument Spreadsheet | Convert to PDF, then compress |

## Requirements

| Tool | Install Command | Purpose |
|------|-----------------|---------|
| LibreOffice | `brew install --cask libreoffice` | Convert PPTX, DOCX, etc. to PDF |
| Ghostscript | `brew install ghostscript` | Compress PDFs >5MB |

## Execution Instructions

When this skill is invoked, execute the following steps:

1. **Parse arguments** from the skill invocation
2. **Run dry-run first** (unless user explicitly skipped) to show file sizes and processing plan
3. **Confirm with user** before making API calls (especially for large uploads)
4. **Execute the generator**:

```bash
python3 "/Users/anantvinjamoori/Vectorshift Pipelines/cli/outline_creator_runner.py" \
    "{topic}" \
    --materials "{materials_folder}" \
    {--outline file if specified} \
    {--dry-run if specified} \
    {--output folder if specified}
```

## When to Use This Skill

Use this skill when the user:
- Wants to create a course outline from reference materials
- Has PowerPoint presentations, Word docs, or PDFs to process
- Has large files (>5MB) that need compression before upload
- Says "create an outline", "generate course outline", "build curriculum"
- Has a folder of research papers/protocols/presentations for a new course
- Invokes `/generate-outline`

## Pipeline Information

| Property | Value |
|----------|-------|
| Pipeline ID | `695f56da724cd19d980e4f1d` |
| Pipeline Name | Course Outline Creator v3 (Parallel Batch Processing) |
| Module | `vs_pipelines/course_outline_creator_v3.py` |
| CLI Helper | `cli/outline_creator_runner.py` |

### Architecture
```
Materials → [4 Parallel Extractors] → [Combiner] → [Perplexity] → [Outline]
```

Files are automatically split into 4 batches for parallel processing, preventing token limit issues with large material sets.

## Required Inputs

1. **Topic** - The course topic (text string)
2. **Materials folder** - Folder containing materials (PDF, PPTX, DOCX, etc.)
3. **Suggested outline** (optional) - Existing outline to revise

## Workflow

### Step 1: Gather Information

Ask the user for:
- Course topic (required)
- Path to materials folder (required)
- Existing outline file to revise (optional)
- Whether to do a dry run first (recommended for large files)

### Step 2: Run Dry Run

Always show a dry run first for large material sets:

```bash
python3 "/Users/anantvinjamoori/Vectorshift Pipelines/cli/outline_creator_runner.py" \
    "{topic}" \
    --materials "{materials_folder}" \
    --dry-run
```

This shows:
- Total number of files found
- File sizes and what will happen to each (convert, compress, or both)
- Tool availability (LibreOffice, Ghostscript)

### Step 3: Execute Pipeline

After user confirmation:

```bash
python3 "/Users/anantvinjamoori/Vectorshift Pipelines/cli/outline_creator_runner.py" \
    "{topic}" \
    --materials "{materials_folder}"
```

Options:
- `--outline <file>` - Existing outline to revise
- `--output <folder>` - Custom output folder
- `--pipeline-id <id>` - Override pipeline ID

### Step 4: Report Results

After completion, show the user:
- Location of output files
- Duration
- Any errors or warnings

## Output Files

Generated files are saved to `outputs/outlines/{topic_name}/`:

| File | Content |
|------|---------|
| `extracted_topics.md` | Research brief extracted from materials (for debugging) |
| `course_dossier.md` | Deep research dossier from Perplexity |
| `course_outline.md` | Structured 10-15 lecture curriculum |

## File Processing Pipeline

```
PPTX/DOCX/etc. ──[LibreOffice]──> PDF ──[Ghostscript]──> Compressed PDF ──> Upload
     PDF ──────────────────────────────[Ghostscript]──> Compressed PDF ──> Upload
```

### Compression Stats

| Original Size | Typical Compressed Size |
|--------------|------------------------|
| 10MB | 3-5MB |
| 50MB | 10-20MB |
| 100MB | 20-40MB |

**Compression quality:** `ebook` (150dpi) - balances quality and size

## Error Handling

| Error | Action |
|-------|--------|
| Materials folder not found | Ask user for correct path |
| No supported files found | Warn and ask if they want to proceed |
| LibreOffice not found | Warn, skip conversion for non-PDFs |
| Ghostscript not found | Warn about large uploads, proceed without compression |
| API timeout | Retry 3x with 30s delay |
| API rate limit (429) | Wait and retry with backoff |

## Output Retrieval Fallback

If output capture fails locally, the **task_id fallback** triggers automatically—no manual intervention required.

**VectorShift confirmed:** The `task_id` returned when submitting a job can be used directly to query results (task_id == span_id for queries).

### Automatic Recovery

The runner script stores the `task_id` and automatically retries fetching results on timeout.

### Manual Recovery (if needed)

If you have a `task_id` from a previous run:

```bash
# Use task_id directly (same as span_id)
python3 "/Users/anantvinjamoori/Vectorshift Pipelines/cli/fetch_by_span_id.py" \
    695f56da724cd19d980e4f1d \
    <TASK_ID> \
    --output-dir ./output
```

See [vectorshift-pipeline-deployment.md](../vectorshift-pipeline-deployment.md#output-retrieval-fallback-pattern) for details.

## Example Usage

**Via slash command:**
```
/generate-outline "Cardiovascular Longevity" --materials "course materials/"
/generate-outline "Topic" --materials "/materials/" --dry-run
/generate-outline "Topic" --materials "/materials/" --outline existing.md
```

**Via natural language:**

User: "I have a folder at 'course materials/' with PDFs and PowerPoints. Create an outline for a peptide therapy course."

Claude: First runs dry-run to show file analysis, confirms tools are available, then confirms with user before executing.

User: "Some files are over 100MB"

Claude: Shows compression/conversion analysis, confirms both LibreOffice and Ghostscript are available, proceeds with processing.

## Execution Notes

- Pipeline takes 10-20 minutes depending on material size
- Non-PDF files are converted to PDF first (may take 1-2 min per large file)
- Large PDFs are compressed before upload to avoid timeouts
- Progress is displayed during polling
- Output folder is created automatically
- Existing outline file (if provided) will be used as a guide for revision
