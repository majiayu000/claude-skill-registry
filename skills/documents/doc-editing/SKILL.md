---
name: doc-editing
description: 'Use when editing documentation or long-form prose where consistency, clarity, and accuracy matter. Goal: produce clean publishable text without tone drift, structural churn, or meta commentary.'
metadata:
  short-description: Edit docs
---

# Doc Editing

Edit documentation and substantial prose to be clear, accurate, and easy to scan. Write the document, not the editing process.

## Output Rules

* Optimize for clarity and correctness, then brevity.
* Preserve existing terminology and tone unless the request requires a change.
* Avoid narration, self-reference, and process notes inside the document.
* Prefer concrete statements over vague claims.

## Editing Workflow

1. Infer audience, purpose, and scope from the file and request.
2. Make the smallest structural change that improves comprehension.
3. Enforce local consistency: headings, tense, voice, terminology, formatting.
4. Remove redundancy and ambiguity; keep one idea per paragraph.
5. Keep emphasis proportional to importance; avoid a single section dominating without intent.
6. If required information is missing, proceed with safe edits and ask only the minimal questions needed for correctness.
7. Do not add change notes unless the user asks or reviewability clearly requires it.

## Markdown Guidance

* Keep headings short and parallel.
* Use short paragraphs and scannable lists.
* Avoid deep nesting.
* Use code blocks only for literal commands, snippets, or examples.

## Review Checklist

* Tone and terminology remain consistent.
* Structure changes are minimal and justified by clarity.
* No meta commentary or process narration appears in the document.
* Sections feel balanced; length matches importance.
* Markdown is scannable: short paragraphs, flat lists, and code blocks only for literals.
