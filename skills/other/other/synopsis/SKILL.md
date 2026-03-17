---
name: synopsis
description: Generate a synopsis of your manuscript at various lengths. Great for pitches, query letters, or back cover copy.
argument-hint: "[book N]"
---

Generate a synopsis of your story using the synopsis agent.

## What This Does

1. Asks what length synopsis you want (long, medium, or short)
2. Reads the manuscript (or available chapters)
3. Produces a synopsis at your chosen length
4. Focuses on story summary, not evaluation

## Length Options

- **Long** — Detailed 800-1200 word synopsis covering full plot arc, subplots, and character journeys
- **Medium** — Standard 300-500 word synopsis for query letters and submissions
- **Short** — Punchy 100-150 word hook/blurb suitable for back cover or elevator pitch

## Usage

```
/synopsis                  # Synopsis of current project
/synopsis book 2           # Synopsis of specific book in series
```

If arguments provided: $ARGUMENTS

## Output

Synopses are saved to `synopses/synopsis-YYYY-MM-DD-{length}.md` and tracked in `progress.md`.

A plot-focused summary including:
- Story premise and hook
- Main character arc
- Key plot points and turning points
- Resolution (for long/medium; short may tease rather than spoil)

## When to Use

- Preparing query letters
- Writing back cover copy
- Creating marketing materials
- Summarizing for collaborators or editors
- Refreshing your memory on a shelved project

## Important Note

Unlike critique, synopsis doesn't require a complete manuscript. It will work with whatever chapters are available, noting if the story is incomplete.
