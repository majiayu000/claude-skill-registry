---
name: pptx-posters
description: Generate PowerPoint presentations and academic posters from paper abstracts or full paper content, with automatic layout optimization and citation formatting.
license: MIT
skill-author: AIPOCH
---
# PPTX Posters

Generate PowerPoint presentations and academic posters from paper abstracts or content.

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## When to Use

- Use this skill when converting a paper abstract or PDF into a structured academic poster or slide deck.
- Use this skill when a specific design template (academic, minimal, colorful) or output format (poster, slides) is needed.
- Do not use this skill to write original research content, fabricate figures, or produce documents for submission as original work.

## Workflow

1. Confirm the input source (abstract text or paper PDF), output format, and template preference.
2. **PDF Validation:** If the input is a PDF, check whether it can be parsed. If the PDF is encrypted, image-only, or corrupt, emit a specific error: "The provided PDF cannot be parsed (possible causes: encrypted, image-only, or corrupt file). Please convert to text or provide the abstract directly."
3. Validate that the request is for presentation generation from existing content, not original research writing.
4. Extract and structure content into appropriate layout sections.
5. Generate the PowerPoint file with layout recommendations.
6. If inputs are incomplete, state which fields are missing and request only the minimum additional information.

## Usage

```text
python scripts/main.py --abstract paper.txt --format poster --output poster.pptx
python scripts/main.py --paper paper.pdf --format slides --template academic
python scripts/main.py --abstract paper.txt --format slides --style minimal --output talk.pptx
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--abstract` | file/text | No | — | Abstract text or file path |
| `--paper` | file path | No | — | Full paper PDF |
| `--format` | string | Yes | — | Output format: `poster` or `slides` |
| `--template` | string | No | `academic` | Design template: `academic`, `minimal`, or `colorful` |
| `--output` | file path | No | stdout | Output `.pptx` file path |

## Output

- PowerPoint file (`.pptx`)
- Layout recommendations
- Design guidelines for manual refinement

## Scope Boundaries

- This skill generates layout and structure from provided content; it does not write original research.
- Figure placeholders are inserted; actual figures must be added manually.
- Citation formatting follows standard academic style but should be verified before submission.

## Stress-Case Rules

For complex multi-constraint requests, always include these explicit blocks:

1. Assumptions
2. Content Source Used
3. Layout Output
4. Design Notes
5. Risks and Manual Checks

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate research content, figures, or citations.

## Input Validation

This skill accepts: a paper abstract or PDF as source content, with a target output format (poster or slides) and optional template preference.

If the request does not involve generating a presentation from existing paper content — for example, asking to write original research, create figures from data, or produce submission-ready manuscripts — do not proceed with the workflow. Instead respond:
> "pptx-posters is designed to generate PowerPoint presentations and academic posters from existing paper content. Your request appears to be outside this scope. For figure generation, use a data visualization tool with your actual data. For original research writing, use a manuscript drafting skill. Please provide an abstract or paper file, or use a more appropriate tool."

## Response Template

Use the following fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

If the request is simple, you may compress the structure, but still keep assumptions and limits explicit when they affect correctness.
