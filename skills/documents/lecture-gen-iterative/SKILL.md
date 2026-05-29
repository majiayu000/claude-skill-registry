---
name: lecture-gen-iterative
description: Generate lectures iteratively using Ralph-style architecture with closed feedback loops, per-slide validation, and flexible research sources.
---

# Iterative Lecture Generator (Ralph-Style)

Generate high-quality medical education lectures using an iterative, segment-by-segment approach with continuous validation against source materials.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: PLANNING                                          │
│  Parse outline → Generate slide segments → Create PRD       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: ITERATIVE EXECUTION (per-slide loop)              │
│  For each slide:                                            │
│    Research → Generate → Validate → (Retry or Complete)     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 3: ASSEMBLY                                          │
│  Merge slides → Coherence pass → Script → References        │
└─────────────────────────────────────────────────────────────┘
```

## When to Use

Use this skill when:
- You need to generate a lecture aligned with specific source materials
- The clinician has provided PDFs, notes, or outlines that must be faithfully reflected
- Quality and accuracy are more important than speed
- You want iterative feedback on each slide before proceeding

## Quick Start

### Full Pipeline (All Phases)

```
/lecture-gen-iterative --outline course_outline.md --lecture 3
```

### Phase by Phase

```bash
# Phase 1: Plan the lecture
/lecture-gen-plan --outline course_outline.md --lecture 3

# Phase 2: Execute generation (can resume)
/lecture-gen-execute

# Phase 3: Assemble final output
/lecture-gen-assemble
```

## Input Requirements

### Course Outline (Required)

A markdown file with this structure:

```markdown
# Course Title

## Lecture 1: Introduction to Longevity Medicine
### Learning Objectives
- Understand the hallmarks of aging
- Define key biomarkers
### Section 1: Hallmarks of Aging
- Genomic instability
- Telomere attrition
### Section 2: Clinical Biomarkers
- NAD+ levels
- Inflammatory markers

## Lecture 2: Mitochondrial Dynamics
...
```

### Additional Materials (Optional)

- **Course Dossier**: Research context markdown
- **Materials Folder**: PDFs, notes, protocols to cross-reference
- **KB ID**: VectorShift knowledge base for semantic search

## Configuration Options

### Research Mode

Specify how research is conducted for each slide:

| Mode | Description |
|------|-------------|
| `hybrid` (default) | Use Perplexity + KB + direct files |
| `perplexity` | Web research only |
| `kb` | Knowledge base only |
| `files` | Direct file access only |

```
/lecture-gen-iterative --research-mode hybrid
```

### Validation Stringency

Control validation threshold:

```
/lecture-gen-iterative --max-retries 3  # Default: 2
```

## State Files

All state is persisted in `.lecture-gen/`:

```
.lecture-gen/
├── prd.json              # Segment definitions + status
├── progress.json         # Iteration history (JSON)
├── progress.txt          # Human-readable progress log
└── materials_index.json  # Source material index
```

### Resuming Generation

If generation is interrupted, simply run:

```
/lecture-gen-execute
```

This will:
1. Load existing state from `.lecture-gen/`
2. Continue from the last pending segment
3. Preserve all completed work

## Output Structure

### Lecture JSON

```json
{
  "id": "lecture-3-mitochondrial-dynamics",
  "title": "Mitochondrial Dynamics in Disease",
  "module": "Systems Cardiology",
  "duration": 21,
  "slides": [
    {
      "id": "slide-1",
      "title": "Learning Objectives",
      "content": [
        {"type": "bullets", "items": ["..."]},
        {"type": "keyTakeaway", "message": "..."}
      ]
    }
  ],
  "keyTakeaways": ["..."],
  "references": [...]
}
```

### Voiceover Script

Plain text optimized for TTS (ElevenLabs):
- No headers or formatting
- Natural speech patterns
- ~150 words per minute

### References

JSON array with PubMed citations and relevance notes.

## Validation Criteria

Each slide is validated against two criteria types:

### Source Fidelity
- Content matches source materials
- Correct terminology used
- Data accuracy verified
- Claims properly supported

### Structural Completeness
- Valid JSON schema
- Required content blocks present
- Word count in target range
- Diagrams where required

## Example Usage

### Generate a specific lecture

```
/lecture-gen-iterative \
  --outline /path/to/course_outline.md \
  --lecture 5 \
  --dossier /path/to/research_dossier.md \
  --materials /path/to/pdfs/
```

### Resume a stalled generation

```
/lecture-gen-execute
```

### Re-run a specific slide

```python
from lib.lecture_gen_iterative import StateManager

state = StateManager()
state.reset_segment("SEG-003")  # Reset slide 3
```

### Check progress

```python
state = StateManager()
summary = state.get_state_summary()
print(f"Completed: {summary['segments']['completed']}/{summary['segments']['total']}")
```

## Troubleshooting

### Slide blocked after retries

1. Check `.lecture-gen/progress.txt` for failure reasons
2. Review the source materials for the blocked segment
3. Reset and retry with modified criteria:

```python
from lib.lecture_gen_iterative import StateManager

state = StateManager()
state.reset_segment("SEG-003")
```

### Research timeouts

Configure longer timeouts in LectureConfig:

```python
config = LectureConfig(
    research_model="sonar-reasoning-pro",  # Faster than deep-research
)
```

### JSON parse errors

Check that your outline follows the expected markdown structure. The parser expects:
- `## Lecture N: Title` for lecture headers
- `### Section Name` for section headers
- `- Item` for bullet points

## API Reference

### StateManager

```python
from lib.lecture_gen_iterative import StateManager

state = StateManager(output_dir=".lecture-gen")

# Load/save PRD
prd = state.load_prd()
state.save_prd(prd)

# Segment operations
segment = state.get_segment("SEG-001")
state.mark_segment_completed("SEG-001")
state.reset_segment("SEG-001")

# Progress tracking
state.log_iteration(segment, status="PASSED", ...)
state.add_pattern("Clinician prefers mechanism-first explanations")
```

### Planning

```python
from lib.lecture_gen_iterative import create_prd_from_outline, StateManager

state = StateManager()
prd = await create_prd_from_outline(
    state_manager=state,
    outline_text=outline_content,
    target_lecture=3,
    config=LectureConfig(research_mode=ResearchMode.HYBRID),
)
```

### Execution

```python
from lib.lecture_gen_iterative import execute_all_segments, StateManager

state = StateManager()
results = await execute_all_segments(state)
print(f"Completed: {results['summary']['segments_completed']}")
```

### Assembly

```python
from lib.lecture_gen_iterative import assemble_lecture, StateManager

state = StateManager()
output = await assemble_lecture(
    state,
    run_coherence_pass=True,
    generate_script=True,
    find_refs=True,
)
print(f"Lecture saved to: {output['files']['lecture']}")
```

## Comparison with VectorShift Pipeline

| Feature | VectorShift Pipeline | Iterative Generator |
|---------|---------------------|---------------------|
| Research | Single global pass | Per-slide targeted |
| Validation | None | Dual validation |
| Retry mechanism | None | Up to 2 retries |
| State persistence | None | Full state files |
| Source cross-reference | None | Explicit validation |
| Resumable | No | Yes |
