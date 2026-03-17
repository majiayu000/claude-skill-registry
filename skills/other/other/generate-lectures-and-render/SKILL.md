---
name: generate-lectures-and-render
description: Generate lectures from a course outline using VectorShift and automatically render them in the physician preview system
user_invocable: true
arguments: "<outline_path> [--physician ID] [--course ID] [--dry-run] [--start N] [--end N] [--materials PATH] [--no-llm-parser]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Generate Lectures and Render

Generate complete lecture packages from a course outline and automatically register them for physician preview. This skill combines the VectorShift pipeline with the physician course preview system.

## Slash Command Usage

```
/generate-lectures-and-render <outline_path> [options]
```

**Examples:**
- `/generate-lectures-and-render outline.md` - Generate all, prompt for physician/course
- `/generate-lectures-and-render outline.md --physician dr-abid-husain --course advanced-cardio`
- `/generate-lectures-and-render outline.md --dry-run` - Preview only

## Execution Flow

When this skill is invoked, execute these phases:

---

### Phase 1: Setup (Interactive)

#### Step 1.1: Parse Arguments

Extract from invocation:
- `outline_path` (required)
- `--physician ID` (optional)
- `--course ID` (optional)
- `--dry-run`, `--start N`, `--end N`, `--materials PATH`, `--no-llm-parser` (pass to generator)

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
OUTPUT: content/physician-courses/dr-john-smith/metabolic-health/

Proceed with generation? [Y/n]
```

---

### Phase 2: Generation

#### Step 2.1: Run the Generator

Execute the Python runner (same as /generate-lectures):

```bash
python3 "/Users/anantvinjamoori/Vectorshift Pipelines/cli/iterative_lecture_runner.py" \
    "{outline_path}" \
    {--dry-run if specified} \
    {--start N if specified} \
    {--end N if specified} \
    {--materials PATH if specified} \
    {--no-llm-parser if specified}
```

#### Step 2.2: Monitor Progress

The runner will:
1. Parse outline to find lectures
2. Match materials to PDFs
3. Submit async jobs to VectorShift
4. Poll for results (5-sec intervals, max 30 min per lecture)
5. Save outputs to `outputs/{course_name}/`

Output files per lecture:
- `lecture_N_slides.json` - The JSON we need
- `lecture_N_transcript.md`
- `lecture_N_blueprint.md`
- `lecture_N_research_dossier.md`
- `lecture_N_kb_context.md`

---

### Phase 3: Copy and Register

After generation completes (or for each successful lecture), perform these steps:

#### Step 3.1: Create Target Directory

```bash
mkdir -p "content/physician-courses/{physician}/{course}"
```

Example:
```bash
mkdir -p "content/physician-courses/dr-john-smith/metabolic-health"
```

#### Step 3.2: Copy and Rename JSON Files

For each generated lecture:

```bash
cp "outputs/{course_name}/lecture_N_slides.json" \
   "content/physician-courses/{physician}/{course}/lecture-N.json"
```

Example:
```bash
cp "outputs/Metabolic_Health/lecture_1_slides.json" \
   "content/physician-courses/dr-john-smith/metabolic-health/lecture-1.json"
```

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
- Extract last name from physician ID: `dr-john-smith` → `Smith`
- Shorten course ID: `metabolic-health` → `Metabolic`
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

**For EXISTING physician with NEW course**, add to their `courses` array:

```typescript
      {
        id: 'new-course-id',
        title: 'New Course Title',
        description: 'Course description.',
        status: 'preview',
        lectures: [
          { id: 'lecture-1', title: 'Lecture 1 Title', order: 1, lecture: importVar as Lecture },
        ],
      },
```

**For EXISTING course**, add to the `lectures` array:

```typescript
          {
            id: 'lecture-3',
            title: 'New Lecture Title',
            order: 3,
            lecture: drSmithMetabolicLecture3 as Lecture,
          },
```

---

### Phase 4: Render and Review

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
| `--no-llm-parser` | Use regex parser instead of LLM |

---

## Error Handling

| Error | Action |
|-------|--------|
| Outline not found | Ask for correct path |
| Generation fails for a lecture | Continue with remaining, report failures |
| Invalid JSON output | Warn but still copy (renderer handles gracefully) |
| Registry parse error | Show manual edit instructions |
| All lectures fail | Report failures, skip registry update |

## Output Retrieval Fallback

If output capture fails locally, the **task_id fallback** triggers automatically—no manual intervention required.

**VectorShift confirmed:** The `task_id` returned when submitting a job can be used directly to query results (task_id == span_id for queries).

### Automatic Recovery

The runner scripts now automatically use the stored `task_id` to retry fetching results on timeout.

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

---

## Example Session

```
User: /generate-lectures-and-render cardiovascular-outline.md

Claude: I'll help you generate lectures and set up preview URLs.

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

Proceed? [Y/n]
> Y

Running VectorShift pipeline...
[Progress updates as lectures complete]

✓ Lecture 1 generated
  → Copied to content/physician-courses/dr-abid-husain/advanced-cardio/lecture-1.json

✓ Lecture 2 generated
  → Copied to content/physician-courses/dr-abid-husain/advanced-cardio/lecture-2.json

[continues...]

✓ Registry updated with 5 lectures

Opening first lecture in browser...

Preview URLs:
━━━━━━━━━━━━━━━━
• Lecture 1: http://localhost:3000/preview/courses/dr-abid-husain/advanced-cardio-1 (opened)
• Lecture 2: http://localhost:3000/preview/courses/dr-abid-husain/advanced-cardio-2
• Lecture 3: http://localhost:3000/preview/courses/dr-abid-husain/advanced-cardio-3
• Lecture 4: http://localhost:3000/preview/courses/dr-abid-husain/advanced-cardio-4
• Lecture 5: http://localhost:3000/preview/courses/dr-abid-husain/advanced-cardio-5

Generation complete! Review the lectures and let me know if you need any adjustments.
```

---

## Related Skills

- `/generate-lectures` - Generate lectures only (no rendering)
- `/physician-course-builder` - Manually create/edit individual lectures
