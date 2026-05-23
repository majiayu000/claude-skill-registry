---
name: google-style-guide
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use when writing or reviewing technical documentation to follow Google's documentation style guide - https://developers.google.com/style
---

# Google Style Guide

## Quick Start

Apply Google's documentation style guide principles to technical writing:

- Use **active voice** and **present tense**
- Write clear, concise headings
- Use numbered lists for procedures, bulleted lists for non-sequential items
- Put conditional clauses before instructions

## Core Principles

- **Clarity first**: Write for software developers and technical practitioners
- **Consistency**: Follow project-specific > Google > third-party style guides
- **Accessibility**: Use inclusive language and consider global audiences
- **Timeless**: Avoid time-specific references; use "currently" or "as of [date]"
- **Reader-focused**: Prioritize user understanding over strict grammatical rules

## Common Patterns

### Voice and Tense

Use active voice and present tense. Example: "The API returns..." not "The API will return..."

### Headings

Use sentence case for headings. Make them descriptive and actionable.

### Lists and Procedures

- Numbered lists: For sequential steps
- Bulleted lists: For non-sequential items
- Start each item with a capital letter

### Code and UI Elements

- Use `code font` for code elements, filenames, and UI elements
- Use **bold** for UI elements users interact with
- Use descriptive placeholder names like `YOUR_PROJECT_ID`

## Reference Files

For detailed documentation, see:

- [references/language-grammar.md](references/language-grammar.md) - Voice, tense, pronouns
- [references/formatting.md](references/formatting.md) - Dates, numbers, lists
- [references/inclusive-language.md](references/inclusive-language.md) - Accessibility guidelines

## Notes

- Official guide: https://developers.google.com/style
- Third-party references: Merriam-Webster (spelling), Chicago Manual of Style
- When in doubt: Choose clarity over strict rule adherence

<!--
PROGRESSIVE DISCLOSURE GUIDELINES:
- Keep this file ~50 lines total (max ~150 lines)
- Use 1-2 code blocks only (recommend 1)
- Keep description <200 chars for Level 1 efficiency
- Move detailed docs to references/ for Level 3 loading
- This is Level 2 - quick reference ONLY, not a manual

LLM WORKFLOW (when editing this file):
1. Write/edit SKILL.md
2. Format (if formatter available)
3. Run: claude-skills-cli validate <path>
4. If multi-line description warning: run claude-skills-cli doctor <path>
5. Validate again to confirm
-->
