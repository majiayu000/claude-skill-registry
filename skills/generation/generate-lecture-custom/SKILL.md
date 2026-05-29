---
name: generate-lecture-custom
description: Generate a single lecture using the custom pipeline (bypasses VectorShift)
user_invocable: true
arguments: "<outline_path> --target <lecture> [--output PATH] [--dossier PATH] [--materials FOLDER]"
allowed-tools: Read, Bash, Glob, Grep, Write
---

# Custom Lecture Generator

Generate a single lecture using direct API calls to Gemini, Claude, Perplexity, and VectorShift KB. This bypasses the VectorShift pipeline orchestration and uses the custom pipeline at `lib/lecture_pipeline/`.

## Slash Command Usage

```
/generate-lecture-custom <outline_path> --target "Lecture 1 - Title"
```

**Examples:**
- `/generate-lecture-custom outline.md --target "Lecture 1"`
- `/generate-lecture-custom "course materials/outline.md" --target "GLP-1 Agonists"`
- `/generate-lecture-custom outline.md --target "Lecture 3" --output ./my-outputs/`

## When to Use This Skill

Use this skill when:
- You want to generate a single lecture from an outline
- You're experiencing issues with VectorShift polling
- You want more control over the generation process
- You need detailed progress logging

## Architecture

This skill uses the custom pipeline at `lib/lecture_pipeline/` which orchestrates:

| Step | Provider | Model | Purpose |
|------|----------|-------|---------|
| 1 | Gemini | gemini-2.5-pro-preview | Extract lecture context |
| 2 | Claude | claude-haiku-4.5 | Generate KB queries |
| 3 | VectorShift | KB API | Search knowledge base |
| 4 | Perplexity | sonar-deep-research | Deep web research |
| 5 | Gemini | gemini-2.5-pro-preview | Create blueprint |
| 6 | Claude | claude-opus-4.5 | Generate HTML/SVG slides |
| 7 | Gemini | gemini-2.5-pro-preview | Generate voiceover |
| 8 | Perplexity | sonar-reasoning-pro | Find references |

## Required Environment Variables

```bash
export GOOGLE_API_KEY="..."        # Gemini API
export ANTHROPIC_API_KEY="..."     # Claude API
export PERPLEXITY_API_KEY="..."    # Perplexity API
export VECTORSHIFT_API_KEY="..."   # VectorShift KB
export UNSTRUCTURED_API_KEY="..."  # Unstructured.io (PDF parsing)
```

## Execution Instructions

When this skill is invoked:

### Step 1: Verify Environment

First, check that API keys are configured:

```bash
python -m lib.lecture_pipeline.cli check
```

If any keys are missing, inform the user which environment variables need to be set.

### Step 2: Parse Arguments

Extract from the skill invocation:
- `outline_path`: Path to course outline markdown
- `--target`: Which lecture to generate (required)
- `--output`: Output directory (optional, default: `./outputs`)
- `--dossier`: Path to research dossier (optional)

### Step 3: Run the Generator

```bash
cd "/Users/anantvinjamoori/NGM Site NextJS V1/ngm-website-official"

python -m lib.lecture_pipeline.cli generate \
    --outline "{outline_path}" \
    --target "{target_lecture}" \
    --output "{output_path}"
```

Add `--dossier "{dossier_path}"` if a dossier was provided.

### Step 4: Report Results

After completion, show the user:
- List of generated files
- Location of output directory
- Any errors that occurred

## Output Files

For each lecture, the following files are saved:

| File | Content |
|------|---------|
| `{lecture}_slides.json` | JSON slides with SVG diagrams |
| `{lecture}_transcript.md` | TTS-ready voiceover script |
| `{lecture}_blueprint.md` | Slide-by-slide plan |
| `{lecture}_research.md` | Deep research dossier |
| `{lecture}_context.md` | Extracted lecture context |
| `{lecture}_kb_queries.json` | KB search queries |
| `{lecture}_references.json` | Authoritative citations |

## Example Workflow

```
User: /generate-lecture-custom outline.md --target "Lecture 2 - Metabolic Health"

Claude:
1. Checks API keys with `python -m lib.lecture_pipeline.cli check`
2. Runs the custom pipeline
3. Reports generated files

Output:
  - lecture_2_-_metabolic_health_slides.json
  - lecture_2_-_metabolic_health_transcript.md
  - lecture_2_-_metabolic_health_blueprint.md
  - ...
```

## Comparison to VectorShift Pipeline

| Aspect | VectorShift | Custom Pipeline |
|--------|-------------|-----------------|
| Orchestration | VectorShift cloud | Local Python |
| Polling | Async with 5s intervals | Direct API calls |
| Debugging | Limited visibility | Full logging |
| Reliability | Inconsistent results delivery | Synchronous, predictable |
| Cost | Markup on API calls | Direct API pricing |

## Troubleshooting

**Missing API keys:**
```bash
export GOOGLE_API_KEY="your_key"
export PERPLEXITY_API_KEY="your_key"
```

**Import errors:**
```bash
pip install google-generativeai httpx tenacity click
```

**Timeout on long lectures:**
The pipeline has built-in timeouts. For very long content, consider breaking into smaller lectures.
