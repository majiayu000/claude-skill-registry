---
name: api-style-guide
description: Style and formatting rules for API/SDK documentation, samples, and tutorials.
---

# API Style Guide Skill

## When to Use
- Authoring or updating API references, tutorials, and SDK docs.
- Reviewing contributions from engineers, DevRel, or partners.
- Auditing docs for consistency before releases.

## Framework
1. **Language & Tone** – audience-specific tone, terminology list, and banned phrases.
2. **Structure** – endpoint/order conventions, table layouts, code block formatting, error doc patterns.
3. **Code Samples** – naming standards, authentication handling, pagination patterns, inline comments.
4. **Metadata & Tags** – version labels, availability notes, beta flags, locale indicators.
5. **Accessibility & Localization** – heading hierarchy, alt-text, snippet annotations, translation guidance.

## Templates
- Reference entry template (description, parameters, responses, examples, notes).
- Tutorial skeleton with prerequisites, steps, troubleshooting, next steps.
- Code sample checklist ensuring env vars, comments, and error handling are included.

## Tips
- Keep examples runnable; provide curl equivalents even when primary sample is in another language.
- Link to glossary for shared terminology across teams.
- Pair with `update-api-reference` command to enforce consistent output.

---
