---
name: generate-lectures-bulk-and-render
description: Generate lectures in parallel using asyncio and automatically render them in the physician preview system (3-5x faster)
user_invocable: true
arguments: "<outline_path> [--physician ID] [--course ID] [--dry-run] [--start N] [--end N] [--materials PATH] [--max-concurrent N] [--no-llm-parser]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Generate Lectures (Parallel) and Render

Generate complete lecture packages in parallel using asyncio and automatically register them for physician preview. This skill combines the VectorShift pipeline with the physician course preview system, achieving 3-5x faster throughput.

## Performance Comparison

| Approach | 5 Lectures | 10 Lectures |
|----------|------------|-------------|
| Sequential (/generate-lectures-and-render) | ~30-50 min | ~60-100 min |
| **Parallel (this skill)** | ~10-15 min | ~15-25 min |

## Slash Command Usage

```
/generate-lectures-bulk-and-render <outline_path> [options]
```

**Examples:**
- `/generate-lectures-bulk-and-render outline.md` - Generate all in parallel, prompt for physician/course
- `/generate-lectures-bulk-and-render outline.md --physician dr-abid-husain --course advanced-cardio`
- `/generate-lectures-bulk-and-render outline.md --dry-run` - Preview only
- `/generate-lectures-bulk-and-render outline.md --max-concurrent 3` - Limit parallel jobs

## Execution Flow

When this skill is invoked, execute these phases:

---

### Phase 1: Setup (Interactive)

**Same as /generate-lectures-and-render**

#### Step 1.1: Parse Arguments

Extract from invocation:
- `outline_path` (required)
- `--physician ID` (optional)
- `--course ID` (optional)
- `--dry-run`, `--start N`, `--end N`, `--materials PATH`, `--max-concurrent N`, `--no-llm-parser` (pass to generator)

#### Step 1.2: Prompt for Missing Info

If `--physician` not provided, ask:
```
What is the physician ID? (e.g., dr-john-smith)
```

If `--course` not provided, ask:
```
What is the course ID? (e.g., metabolic-health)
```

#### Step 1.3: Check Registry

Read the registry file:
```
content/physician-courses/registry.ts
```

Check if physician ID exists in `physicianRegistry`.

#### Step 1.4: Handle New vs Existing Physician

**If NEW physician**, collect metadata:
- Physician name (e.g., "Dr. John Smith")
- Credentials (e.g., "MD", "MD, PhD")
- Specialty (e.g., "Metabolic Medicine")
- Bio (optional, one sentence)

**If EXISTING physician**, check if course exists:
- If course exists: will add lectures to existing course
- If course is new: collect course title and description

#### Step 1.5: Collect Course Info (if new course)

Ask for:
- Course title (e.g., "Advanced Cardiovascular Therapies")
- Course description (one sentence)

#### Step 1.6: Show Execution Plan

Display summary:
```
PHYSICIAN: dr-john-smith (New/Existing)
COURSE: metabolic-health (New/Existing)
OUTLINE: path/to/outline.md
LECTURES: N found in outline
MAX CONCURRENT: 5
OUTPUT: content/physician-courses/dr-john-smith/metabolic-health/

Estimated time: ~X minutes (vs ~Y minutes sequential)

Proceed with parallel generation? [Y/n]
```

---

### Phase 2: Parallel Generation

**Uses parallel_lecture_runner.py instead of iterative_lecture_runner.py**

#### Step 2.1: Run the Parallel Generator

Execute the Python runner:

```bash
python3 "/Users/anantvinjamoori/Vectorshift Pipelines/cli/parallel_lecture_runner.py" \
    "{outline_path}" \
    {--dry-run if specified} \
    {--start N if specified} \
    {--end N if specified} \
    {--materials PATH if specified} \
    {--max-concurrent N if specified, default 5} \
    {--no-llm-parser if specified}
```

#### Step 2.2: Monitor Progress

The runner will show real-time progress:
```
[05:32] Pending: 0 | Submitting: 0 | Processing: 3 | Completed: 2 | Failed: 0
```

All lectures process concurrently (up to max-concurrent limit).

Output files per lecture:
- `lecture_N_slides.json` - The JSON we need
- `lecture_N_transcript.md`
- `lecture_N_blueprint.md`
- `lecture_N_research_dossier.md`
- `lecture_N_kb_context.md`

---

### Phase 3: Copy and Register

**Same as /generate-lectures-and-render**

After generation completes, perform these steps:

#### Step 3.1: Create Target Directory

```bash
mkdir -p "content/physician-courses/{physician}/{course}"
```

Example:
```bash
mkdir -p "content/physician-courses/dr-john-smith/metabolic-health"
```

#### Step 3.2: Clean and Copy JSON Files

**IMPORTANT:** VectorShift pipeline outputs JSON wrapped in markdown code fences with extra HTML content. You MUST clean the JSON before copying.

**Run this Python script to extract clean JSON:**

```python
import json
import os

source_dir = "outputs/{course_name}"  # e.g., outputs/OUTPUT_COURSE_FRAMEWORKS_SUMMARY
target_dir = "content/physician-courses/{physician}/{course}"

for i in range(1, NUM_LECTURES + 1):
    source_file = os.path.join(source_dir, f"lecture_{i}_slides.json")
    target_file = os.path.join(target_dir, f"lecture-{i}.json")

    with open(source_file, 'r') as f:
        content = f.read()

    # Remove markdown code fences if present
    content = content.strip()
    if content.startswith('```json'):
        content = content[7:]
    elif content.startswith('```'):
        content = content[3:]

    # Find the JSON object - look for balanced braces
    depth = 0
    start = None
    end = None

    for idx, char in enumerate(content):
        if char == '{':
            if start is None:
                start = idx
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0 and start is not None:
                end = idx + 1
                break

    if start is not None and end is not None:
        json_str = content[start:end]
        data = json.loads(json_str)

        # Write clean JSON
        with open(target_file, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"lecture-{i}.json: Cleaned and validated")
```

**Why this is needed:**
- VectorShift wraps JSON output in \`\`\`json ... \`\`\` code fences
- Extra HTML content (sources, references) appears after the JSON
- Next.js/Turbopack requires pure JSON for imports
- This script extracts only the valid JSON object

#### Step 3.3: Read Lecture Titles from JSON

For each copied JSON file, read the `title` field for registry entry.

#### Step 3.4: Update Registry

Edit `content/physician-courses/registry.ts`:

**A. Add Import Statements**

Insert after existing imports (after line ~10):

```typescript
import drSmithMetabolicLecture1 from './dr-john-smith/metabolic-health/lecture-1.json';
import drSmithMetabolicLecture2 from './dr-john-smith/metabolic-health/lecture-2.json';
```

Import naming convention: `dr{LastName}{CourseShort}Lecture{N}`
- Extract last name from physician ID: `dr-john-smith` -> `Smith`
- Shorten course ID: `metabolic-health` -> `Metabolic`
- Add lecture number: `Lecture1`, `Lecture2`, etc.

**B. Add/Update Physician Entry**

**For NEW physician**, add before the closing `};` of physicianRegistry:

```typescript
  'dr-john-smith': {
    physician: {
      id: 'dr-john-smith',
      name: 'Dr. John Smith',
      credentials: 'MD',
      specialty: 'Metabolic Medicine',
    },
    courses: [
      {
        id: 'metabolic-health',
        title: 'Metabolic Health Fundamentals',
        description: 'A comprehensive course on metabolic optimization.',
        status: 'preview',
        lectures: [
          {
            id: 'lecture-1',
            title: 'Introduction to Metabolic Health',
            order: 1,
            lecture: drSmithMetabolicLecture1 as Lecture,
          },
          {
            id: 'lecture-2',
            title: 'Metabolic Pathways',
            order: 2,
            lecture: drSmithMetabolicLecture2 as Lecture,
          },
        ],
      },
    ],
  },
```

**For EXISTING physician with NEW course**, add to their `courses` array.

**For EXISTING course**, add to the `lectures` array.

---

### Phase 4: Render and Review

**Same as /generate-lectures-and-render**

#### Step 4.1: Construct Preview URLs

URL pattern:
```
http://localhost:3000/preview/courses/{physician}/{course}-{N}
```

Examples:
```
http://localhost:3000/preview/courses/dr-john-smith/metabolic-health-1
http://localhost:3000/preview/courses/dr-john-smith/metabolic-health-2
```

#### Step 4.2: Open First Lecture

```bash
open "http://localhost:3000/preview/courses/{physician}/{course}-1"
```

#### Step 4.3: Print Remaining URLs

```
Lecture 1 opened in browser!

Remaining preview URLs:
- Lecture 2: http://localhost:3000/preview/courses/{physician}/{course}-2
- Lecture 3: http://localhost:3000/preview/courses/{physician}/{course}-3
...
```

---

## Options Reference

| Flag | Description |
|------|-------------|
| `<outline_path>` | Required: Path to course outline markdown |
| `--physician ID` | Pre-specify physician ID (skips prompt) |
| `--course ID` | Pre-specify course ID (skips prompt) |
| `--dry-run` | Show execution plan without running pipeline |
| `--start N` | Start from lecture N |
| `--end N` | Stop after lecture N |
| `--materials PATH` | Custom materials folder (default: Abid Husain/) |
| `--max-concurrent N` | Maximum parallel jobs (default: 5) |
| `--no-llm-parser` | Use regex parser instead of LLM |

---

## Error Handling

| Error | Action |
|-------|--------|
| Outline not found | Ask for correct path |
| Some lectures fail | Continue with successful ones, report failures |
| JSON has markdown fences | Use the cleaning script in Step 3.2 (this is expected behavior) |
| "Extra data" JSON error | JSON has trailing content - use cleaning script to extract pure JSON |
| Build fails with "invalid JSON" | Lecture files still have code fences - re-run cleaning script |
| Registry parse error | Show manual edit instructions |
| All lectures fail | Report failures, skip registry update |

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

---

## Output Summary

After successful execution:

1. **JSON files** copied to `content/physician-courses/{physician}/{course}/`
2. **Registry updated** with imports and entries
3. **First lecture** opened in browser
4. **URL list** printed for remaining lectures
5. **Performance summary** showing time savings vs sequential

---

## Example Session

```
User: /generate-lectures-bulk-and-render cardiovascular-outline.md

Claude: I'll help you generate lectures in parallel and set up preview URLs.

First, I need some information:

What is the physician ID? (e.g., dr-john-smith)
> dr-abid-husain

What is the course ID? (e.g., metabolic-health)
> advanced-cardio

Checking registry... Found existing physician: Dr. Abid Husain

This will create a new course for Dr. Abid Husain.

Course title?
> Advanced Cardiovascular Therapies

Course description?
> A deep dive into modern cardiovascular interventions and peptide therapies.

EXECUTION PLAN:
━━━━━━━━━━━━━━━━
PHYSICIAN: dr-abid-husain (existing)
COURSE: advanced-cardio (new)
OUTLINE: cardiovascular-outline.md
LECTURES: 5 found
MAX CONCURRENT: 5

Estimated time: ~12 minutes (vs ~40 minutes sequential)

Proceed? [Y/n]
> Y

Running parallel VectorShift pipeline...
[00:00] Pending: 5 | Submitting: 0 | Processing: 0 | Completed: 0 | Failed: 0
[02:15] Pending: 0 | Submitting: 0 | Processing: 5 | Completed: 0 | Failed: 0
[08:42] Pending: 0 | Submitting: 0 | Processing: 2 | Completed: 3 | Failed: 0
[11:35] Pending: 0 | Submitting: 0 | Processing: 0 | Completed: 5 | Failed: 0

All lectures completed successfully in 11.6 minutes!
(Sequential estimate: ~40 minutes - 3.4x faster)

Copying files to content/physician-courses/dr-abid-husain/advanced-cardio/
  -> lecture-1.json
  -> lecture-2.json
  -> lecture-3.json
  -> lecture-4.json
  -> lecture-5.json

Updating registry.ts with 5 lectures...

Opening first lecture in browser...

Preview URLs:
━━━━━━━━━━━━━━━━
- Lecture 1: http://localhost:3000/preview/courses/dr-abid-husain/advanced-cardio-1 (opened)
- Lecture 2: http://localhost:3000/preview/courses/dr-abid-husain/advanced-cardio-2
- Lecture 3: http://localhost:3000/preview/courses/dr-abid-husain/advanced-cardio-3
- Lecture 4: http://localhost:3000/preview/courses/dr-abid-husain/advanced-cardio-4
- Lecture 5: http://localhost:3000/preview/courses/dr-abid-husain/advanced-cardio-5

Generation complete! Review the lectures and let me know if you need any adjustments.
```

---

## SVG Diagram Rendering

The VectorShift pipeline generates lectures with inline SVG diagrams in the `diagramHtml` field of each slide. These are rendered by the `UniversalLecture` component using `dangerouslySetInnerHTML`.

**How it works:**
- Each slide can have a `diagramHtml` field containing raw SVG markup
- The UniversalLecture component at `src/components/lectures/UniversalLecture.tsx` renders this at lines 250-257
- SVG diagrams use the editorial color palette (paper, ink, gold, vermillion)

**If diagrams don't render:**
1. Check that the JSON file has `diagramHtml` field in slides (not `diagram`)
2. Verify the SVG is valid XML (no unclosed tags)
3. Check browser console for React hydration errors
4. The `diagramHtml` field should contain a complete `<svg>` element

**Diagram field formats:**
- `diagramHtml` - Inline SVG string (current pipeline output)
- `diagram` - Structured JSON diagram (legacy format, uses DiagramRenderer)

---

## Fallback to Sequential

If parallel generation has issues, fall back to:

```
/generate-lectures-and-render <outline_path> [same options except --max-concurrent]
```

---

## Related Skills

- `/generate-lectures-and-render` - Sequential generation + rendering (slower)
- `/generate-lectures-bulk` - Parallel generation only (no rendering)
- `/generate-lectures` - Sequential generation only
- `/physician-course-builder` - Manually create/edit individual lectures
