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

## Dimensions

This skill has multiple configuration dimensions. See [compatibility-matrix.md](references/compatibility-matrix.md) for:

- Workflow x Voice Type
- Tone x Format (Microcopy)
- Editing Pass x Document Type
- Voice Dimension x Content Type
- Narrative Structure x Audience

Use ✓✓ combinations when possible; avoid ✗ combinations.

## Usage

1. Detect which workflow applies based on user's task
2. Check [compatibility matrix](references/compatibility-matrix.md) for dimension compatibility
3. Announce: "I'm using the writing skill for [workflow]"
4. Load the appropriate reference file
5. Execute the workflow with confirmation gates (see below)

## Confirmation Gates

Multi-step workflows pause at checkpoints to prevent wasted work when intent drifts.

**Gate Points:**

| Phase | Gate |
|-------|------|
| After voice/style analysis | ⚠️ CHECKPOINT: "Does this capture the voice you want?" |
| After outline/structure | ⚠️ CHECKPOINT: "Here's my proposed structure. Should I proceed?" |
| Before final output | ⚠️ CHECKPOINT: "Ready to generate final version. Confirm?" |

**Skip gates:** Say "proceed without confirmation" to run uninterrupted.

**In workflows:** Each reference file should pause at these points:

```
### Phase 2: Analysis

[... phase content ...]

⚠️ **CHECKPOINT**: Present findings summary. Ask: "Does this capture the voice/style? Any adjustments before I continue?"
```

## Rules

- Use Ask tool to gather input before proceeding
- Preserve author voice when editing
- Be specific about changes and rationale
- For evaluations, provide exact replacement text for fixes
