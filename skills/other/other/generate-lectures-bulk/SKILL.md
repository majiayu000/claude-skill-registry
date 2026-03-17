---
name: generate-lectures-bulk
description: Generate all lectures from a course outline in parallel using asyncio for 3-5x faster processing
user_invocable: true
arguments: "<outline_path> [--dry-run] [--start N] [--end N] [--materials PATH] [--max-concurrent N] [--no-llm-parser]"
allowed-tools: Read, Bash, Glob, Grep
---

# Parallel Lecture Generator

Generate complete lecture packages from a course outline by running the VectorShift Individual Lecture HTML pipeline for ALL lectures concurrently using asyncio.

## Performance Comparison

| Approach | 5 Lectures | 10 Lectures |
|----------|------------|-------------|
| Sequential (/generate-lectures) | ~30-50 min | ~60-100 min |
| **Parallel (this skill)** | ~10-15 min | ~15-25 min |

## Slash Command Usage

```
/generate-lectures-bulk <outline_path> [options]
```

**Examples:**
- `/generate-lectures-bulk outline.md` - Generate all lectures in parallel
- `/generate-lectures-bulk outline.md --dry-run` - Preview without API calls
- `/generate-lectures-bulk outline.md --max-concurrent 3` - Limit to 3 parallel jobs
- `/generate-lectures-bulk outline.md --start 2 --end 6` - Generate lectures 2-6 only

## Execution Instructions

When this skill is invoked, execute the following steps:

### Step 1: Parse Arguments

Extract from invocation:
- `outline_path` (required)
- `--dry-run` - Preview only
- `--start N` - Start from lecture N
- `--end N` - Stop after lecture N
- `--materials PATH` - Custom materials folder (default: Abid Husain/)
- `--max-concurrent N` - Max parallel jobs (default: 5)
- `--no-llm-parser` - Use regex parser instead of LLM

### Step 2: Run Dry-Run First

Always run dry-run first to show the execution plan:

```bash
python3 "/Users/anantvinjamoori/Vectorshift Pipelines/cli/parallel_lecture_runner.py" \
    "{outline_path}" \
    --dry-run \
    {--start N if specified} \
    {--end N if specified} \
    {--materials PATH if specified} \
    {--max-concurrent N if specified}
```

### Step 3: Confirm with User

Show the execution plan and estimated time savings. Ask for confirmation before proceeding.

### Step 4: Execute Parallel Generation

```bash
python3 "/Users/anantvinjamoori/Vectorshift Pipelines/cli/parallel_lecture_runner.py" \
    "{outline_path}" \
    {--start N if specified} \
    {--end N if specified} \
    {--materials PATH if specified} \
    {--max-concurrent N if specified} \
    {--no-llm-parser if specified}
```

### Step 5: Report Results

After completion, show the user:
- Number of successful/failed lectures
- Actual time vs sequential estimate
- Speedup achieved
- Location of output files
- Any error messages for failed lectures

## How It Works

1. **Parse Outline**: Extract all lectures from the course outline (LLM or regex parser)
2. **Match Materials**: Fuzzy-match material references to PDF files
3. **Prepare Materials**: Convert/compress PDFs for upload
4. **Concurrent Submission**: Submit ALL lecture jobs at once (with semaphore rate limiting)
5. **Parallel Polling**: Poll all task_ids concurrently every 5 seconds
6. **Real-time Progress**: Display status for each lecture as it processes
7. **Collect Results**: Save outputs as they complete

## Pipeline Information

| Property | Value |
|----------|-------|
| Pipeline ID | `69601d086fdec16163dc80fe` |
| Pipeline Name | Individual Lecture HTML v1 (SVG Diagrams) |
| Max Concurrent | Configurable (default: 5) |

## Output Files

For each lecture, the following files are saved to `outputs/{course_name}/`:

| File | Content |
|------|---------|
| `lecture_N_slides.json` | Structured JSON slides |
| `lecture_N_transcript.md` | TTS-ready speaker script |
| `lecture_N_blueprint.md` | Slide-by-slide plan |
| `lecture_N_research_dossier.md` | Deep research content |
| `lecture_N_kb_context.md` | Knowledge base results |

## Error Handling

| Scenario | Behavior |
|----------|----------|
| 1 lecture fails | Other lectures continue, failure reported at end |
| Rate limited (429) | Automatic retry with backoff |
| Network error | Retry up to 10 times per job |
| Timeout (30 min/lecture) | Mark as failed, continue others |
| All lectures fail | Exit with error, show diagnostics |

## Output Retrieval Fallback

If output capture fails locally, the **task_id fallback** triggers automatically—no manual intervention required.

**VectorShift confirmed:** The `task_id` returned when submitting a job can be used directly to query results (task_id == span_id for queries).

### Automatic Recovery

The parallel runner stores all `task_id` values and automatically retries failed fetches using them.

### Manual Recovery (if needed)

If you have a `task_id` from a previous run:

```bash
# Use task_id directly (same as span_id)
python3 "/Users/anantvinjamoori/Vectorshift Pipelines/cli/fetch_by_span_id.py" \
    69601d086fdec16163dc80fe \
    <TASK_ID> \
    --output-dir ./output
```

See [vectorshift-pipeline-deployment.md](../vectorshift-pipeline-deployment.md#output-retrieval-fallback-pattern) for details.

## Fallback to Sequential

If parallel generation has issues, fall back to sequential:

```
/generate-lectures <outline_path> [same options except --max-concurrent]
```

## When to Use This Skill

Use this skill when:
- Processing multiple lectures (3+) for significant time savings
- Need faster turnaround on course generation
- System resources can handle concurrent processing
- VectorShift API is responding normally

Use `/generate-lectures` (sequential) when:
- Processing only 1-2 lectures (minimal benefit from parallelism)
- Need detailed per-lecture progress visibility
- Troubleshooting API issues
- System resources are constrained

## Dependencies

Requires `aiohttp` for async HTTP:

```bash
pip install aiohttp
```

## Related Skills

- `/generate-lectures` - Sequential lecture generation (slower but simpler)
- `/generate-lectures-bulk-and-render` - Parallel generation + automatic preview rendering
- `/physician-course-builder` - Manual lecture creation/editing
