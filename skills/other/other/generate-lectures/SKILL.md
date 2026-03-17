---
name: generate-lectures
description: Generate all lectures from a course outline using the VectorShift pipeline
user_invocable: true
arguments: "<outline_path> [--dry-run] [--start N] [--end N] [--materials PATH] [--no-llm-parser] [--claude-api-key KEY]"
allowed-tools: Read, Bash, Glob, Grep
---

# Iterative Lecture Generator

Generate complete lecture packages from a course outline by running the VectorShift Individual Lecture HTML pipeline (with SVG diagrams) for each lecture sequentially.

## Slash Command Usage

```
/generate-lectures <outline_path> [options]
```

**Examples:**
- `/generate-lectures outline.md` - Generate all lectures
- `/generate-lectures outline.md --dry-run` - Preview without API calls
- `/generate-lectures outline.md --start 2 --end 4` - Generate lectures 2-4 only
- `/generate-lectures "Abid Husain/course_outline.md" --materials "Abid Husain/"` - Custom paths

## Execution Instructions

When this skill is invoked, execute the following steps:

1. **Parse arguments** from the skill invocation
2. **Run dry-run first** (unless user explicitly skipped it) to show the execution plan
3. **Confirm with user** before making API calls
4. **Execute the generator**:

```bash
python3 "/Users/anantvinjamoori/Vectorshift Pipelines/cli/iterative_lecture_runner.py" \
    "{outline_path}" \
    {--dry-run if specified} \
    {--start N if specified} \
    {--end N if specified} \
    {--materials PATH if specified}
```

## When to Use This Skill

Use this skill when the user:
- Has a course outline (markdown) and wants to generate all lectures
- Says "generate lectures", "create the course", "run the lecture pipeline"
- Asks to "batch process" or "iterate through" lectures
- Provides a course outline and materials folder
- Invokes `/generate-lectures`

## Pipeline Information

| Property | Value |
|----------|-------|
| Pipeline ID | `69601d086fdec16163dc80fe` |
| Pipeline Name | Individual Lecture HTML v1 (SVG Diagrams) |
| Module | `vs_pipelines/individual_lecture_html.py` |

## Required Inputs

1. **Course outline file** - Markdown file with lecture structure
2. **Materials folder** (optional) - Folder with PDF materials (default: `Abid Husain/`)

## Workflow

### Step 1: Gather Information

Ask the user for:
- Path to course outline markdown file
- Materials folder path (or confirm default: `Abid Husain/`)
- Lecture range to process (start/end numbers, optional)
- Whether to do a dry run first

### Step 2: Run the Helper Script

Execute the Python helper:

```bash
python3 "/Users/anantvinjamoori/Vectorshift Pipelines/cli/iterative_lecture_runner.py" \
    "{course_outline_path}" \
    --materials "{materials_folder}" \
    --start {start_lecture} \
    --end {end_lecture}
```

Options:
- `--dry-run` - Preview without making API calls
- `--start N` - Start from lecture N
- `--end N` - Stop after lecture N
- `--materials PATH` - Custom materials folder
- `--output PATH` - Custom output folder
- `--no-llm-parser` - Disable LLM parser and use regex instead (LLM parser is default)
- `--claude-api-key KEY` - Claude API key for LLM parser (uses env var if not provided)

### Step 3: Monitor Progress

The script will:
1. Parse the course outline to find lectures (regex or LLM parser)
2. Extract suggested materials for each lecture
3. Fuzzy-match material names to PDF files
4. Submit job to VectorShift with `background: true` (async)
5. Poll for results every 5 seconds (max 30 minutes per lecture)
6. Save outputs to `outputs/{course_name}/`

**Note:** The async API pattern eliminates HTTP timeout issues for long-running pipelines.

### Step 4: Report Results

After completion, show the user:
- Number of successful/failed lectures
- Location of output files
- Any error messages

## Output Files

For each lecture, the following files are saved to `outputs/{course_name}/`:

| File | Content |
|------|---------|
| `lecture_N_slides.json` | Structured JSON slides |
| `lecture_N_transcript.md` | TTS-ready speaker script |
| `lecture_N_blueprint.md` | Slide-by-slide plan |
| `lecture_N_research_dossier.md` | Deep research content |
| `lecture_N_kb_context.md` | Knowledge base results |

## Course Outline Format

The skill expects course outlines with this structure:

```markdown
# Course Title

## Lecture 1 - Introduction to Topic

### Where to integrate user-provided materials
- Use "BPC-157 and the Cardiovascular System" dossier
- Reference "SS-31 in Cardiovascular Medicine" protocols

### Suggested preparatory materials
- Reading: "Apolipoprotein B: Bridging the Gap"

---

## Lecture 2 - Deep Dive
...
```

## Material Matching

The skill fuzzy-matches material references to PDF files:

| Reference in Outline | Matched PDF |
|---------------------|-------------|
| "BPC-157 and the Cardiovascular System" | BPC-157-and-the-Cardiovascular-System-*.pdf |
| "SS-31 in Cardiovascular Medicine" | SS-31-Elamipretide-in-Cardiovascular-Medicine-*.pdf |
| "Cardio-Zoomer" | CARDIO-ZOOMER-A-FUNCTIONAL-CARDIOVASCULAR-PHENOTYPE-MAP.pdf |

## Available Materials (Abid Husain folder)

49 PDF files including:
- BPC-157 research papers
- SS-31/Elamipretide studies
- GLP-1 and cardiovascular effects
- Testosterone therapy research
- Peptide therapy protocols
- Cardio-Zoomer documentation
- Cardiovascular risk assessment guides

## Error Handling

| Error | Action |
|-------|--------|
| Course outline not found | Ask user for correct path |
| No lectures parsed | Check format, show example |
| Materials folder missing | Proceed without materials or ask for path |
| API timeout | Retry 3x with 30s delay |
| API rate limit (429) | Wait and retry with backoff |
| Pipeline error | Log error, continue with next lecture |

## Output Retrieval Fallback

If output capture fails locally (timeout, network issues, interrupted process), the **task_id fallback** triggers automatically—no manual intervention required.

### How It Works

**VectorShift confirmed:** The `task_id` returned when submitting a job can be used directly to query results. This eliminates the need to manually fetch span IDs from the UI.

```
task_id from job submission == span_id for status queries
```

### Automatic Recovery

The runner scripts now automatically:
1. Store the `task_id` from each job submission
2. Use the `task_id` to retry fetching results on timeout
3. Log all task IDs for manual recovery if needed

### Manual Recovery (if needed)

If you have a `task_id` from a previous run:

```bash
# Use task_id directly (same as span_id)
python3 "/Users/anantvinjamoori/Vectorshift Pipelines/cli/fetch_by_span_id.py" \
    69601d086fdec16163dc80fe \
    <TASK_ID> \
    --output-dir ./output
```

Or use Python:
```python
from vs_pipelines.config import fetch_pipeline_result_by_span_id

result = fetch_pipeline_result_by_span_id(
    pipeline_id="69601d086fdec16163dc80fe",
    span_id=task_id  # task_id works directly!
)

if result["status"] == "completed":
    slides = result["result"].get("lecture_json", "")
    transcript = result["result"].get("transcript", "")
```

See [vectorshift-pipeline-deployment.md](../vectorshift-pipeline-deployment.md#output-retrieval-fallback-pattern) for full documentation.

## Example Usage

**Via slash command:**
```
/generate-lectures outline.md
/generate-lectures outline.md --dry-run
/generate-lectures outline.md --start 2 --end 4
/generate-lectures outline.md --no-llm-parser  # Use regex instead
```

**Via natural language:**

User: "I have a course outline at `outline.md`. Generate all the lectures."

Claude: First runs dry-run to show plan, then confirms with user before executing. LLM parser (Claude Haiku 4.5) is used by default.

User: "Generate just lectures 2 through 4"

Claude: Runs with `--start 2 --end 4` flags.

User: "Use the regex parser instead"

Claude: Runs with `--no-llm-parser` flag to disable LLM parsing.

## Execution Notes

- Each lecture takes 5-10 minutes to process
- Total time for 5 lectures: ~30-50 minutes
- Progress is displayed in real-time
- Failed lectures don't stop the process
- Outputs can be resumed with `--start N`
