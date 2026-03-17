---
name: docs-style
description: Automatically applies when drafting or revising documentation to enforce repository voice, clarity, and navigation patterns.
category: documentation
---

# Documentation Style Guide

**Trigger Keywords**: documentation, doc update, README, guide, tutorial, changelog, ADR, design doc, style, tone, voice, copy edit

**Agent Integration**: Used by `spec-writer`, `technical-writer`, and `requirements-analyst` when delivering reader-facing content.

## Voice and Clarity
- Prefer concise, direct sentences; remove filler and marketing language.
- Use active voice and parallel sentence structures.
- Lead with outcomes, then supporting details.
- Keep language project-agnostic so the plugin works in any Python project.

## Structure and Navigation
- Start with a short purpose/summary before detailed sections.
- Use consistent heading levels and ordered sections; avoid nested lists where possible.
- Include quick-scannable bullets and tables for comparisons or options.
- Add cross-references to related specs, tasks, and reference docs.

## Formatting Patterns
- Use fenced code blocks with language tags for examples.
- Keep line wrapping consistent; avoid trailing whitespace.
- Use bold keywords sparingly for emphasis; prefer headings + bullets.
- For checklists, use ordered steps when sequence matters, unordered when it does not.

## Quality Checklist
- ✅ Audience and scope identified at the top.
- ✅ Clear outcomes and verification steps included.
- ✅ Terminology consistent across the document.
- ✅ Links/paths are workspace-relative (no IDE/URL schemes).
- ❌ Avoid passive voice that hides ownership or action.
- ❌ Avoid giant paragraphs; break into digestible chunks.
