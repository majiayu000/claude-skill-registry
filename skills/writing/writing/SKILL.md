---
name: writing
description: Precision editing for prose and copy. Use when user says "edit this", "improve this", "review my writing", "use [name]'s voice", or provides draft text to refine. Triggers on editing, voice extraction, voice library, narrative structure, microcopy.
---

# Writing Skill

Router skill for writing and content workflows. Detects task type and routes to appropriate workflow.

## When This Skill Activates

You're working on:

- Editing prose or documentation
- Extracting or matching author voice
- Managing saved voice profiles (list, apply, delete)
- Structuring narratives or stories
- Writing UI microcopy
- Evaluating content quality

## Workflow Selection

Announce which workflow you're using:

| Task Type                                    | Workflow            | Reference                   |
| -------------------------------------------- | ------------------- | --------------------------- |
| Analyze writing style, extract voice profile | Voice Extraction    | `references/voice.md`       |
| List, apply, or delete saved voices          | Voice Library       | `/wordsmith:voices` command |
| Edit text, cut fluff, tighten prose          | Precision Editing   | `references/editing.md`     |
| Structure story, build narrative arc         | Narrative Structure | `references/narrative.md`   |
| Write UI copy, tone variations               | Microcopy Tones     | `references/copy.md`        |
| Evaluate blog/content quality, score         | Content Evaluation  | `references/eval.md`        |
| Create RFC, ADR, design doc, or blog         | Document Template   | `../template/SKILL.md`      |

## Strategic Framework

| Framework | Purpose | When to Use |
|-----------|---------|-------------|
| [Open Loop](references/open-loop.md) | Make messages memorable via Zeigarnik effect | Copy, presentations, emails that need to stick |

## Related Thinking Tools

From `hope/skills/soul/references/tools/`:

| Tool                                                                      | When to Use                                |
| ------------------------------------------------------------------------- | ------------------------------------------ |
| [Minto Pyramid](../../hope/skills/soul/references/tools/minto-pyramid.md) | Structure executive summaries, SCQA format |
| [Productive Thinking](../../hope/skills/soul/references/tools/productive-thinking.md) | Multi-perspective content review |

## Usage

1. Detect which workflow applies based on user's task
2. Announce: "I'm using the writing skill for [workflow]"
3. Load the appropriate reference file
4. Execute the workflow exactly as written

## Rules

- Use Ask tool to gather input before proceeding
- Preserve author voice when editing
- Be specific about changes and rationale
- For evaluations, provide exact replacement text for fixes
