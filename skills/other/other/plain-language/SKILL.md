---
name: plain-language
description: >
  Reviews project text (documentation, READMEs, marketing copy, UI strings, code
  comments, error messages) for plain language compliance and produces structured
  edit recommendations based on the U.S. federal government Plain Language Guidelines
  (https://digital.gov/guides/plain-language). Use when asked to: review language, check readability,
  audit docs, improve copy clarity, do a plain language check, make a README
  clearer, or review writing quality. Triggers on phrases like "plain language
  review", "check readability", "audit the copy", "make this clearer".
allowed-tools: Read Bash(scripts/scan-files.sh:*)
---

# Plain Language Review

Review text files against the U.S. federal government Plain Language Guidelines (~30 rules across 6 categories) and produce a structured report of findings with concrete rewrites.

**Important: This skill produces a report. Do not modify any reviewed files.**

## Review Workflow

1. **Select files** — Use the user's specified files. If none specified, run `scripts/scan-files.sh <project-directory>` to discover all `.md`, `.mdx`, `.txt`, `.rst`, and `.adoc` files. The `<project-directory>` argument is **required** — it must be the root of the user's project (the repository being reviewed), NOT the skill's own directory.
2. **Load rules** — Read `references/rules-quick-ref.md` for the full rule checklist.
3. **Review each file** — For each file, read it and apply all rules. Skip text inside code blocks/fences, inline code, and code-only files. Only review human-readable prose.
4. **Generate findings** — For each issue found, produce a finding using the output format below.
5. **Classify severity** — Use `references/severity-rubric.md` to assign high/medium/low.
6. **Verify rewrites** — For each suggested rewrite, confirm it resolves the flagged rule violation and does not introduce new violations. If a rewrite still triggers the same or a different rule, revise it before including it in the report.
7. **Assemble report** — Group findings by file, then by severity (high first).

## Output Format

Use this exact structure for each finding:

```
## [file path]

### Finding [N] — [Rule name] (severity: [high|medium|low])
- **Line [N]:** "[original text]"
- **Guideline:** [One-sentence explanation of the rule violated]
- **Suggested:** "[concrete rewrite]"
```

**Example:**

```
## docs/getting-started.md

### Finding 1 — Use simple words (severity: medium)
- **Line 14:** "In order to utilize the configuration module..."
- **Guideline:** Replace complex words with simple alternatives — "utilize" → "use", "in order to" → "to"
- **Suggested:** "To use the configuration module..."

### Finding 2 — Use active voice (severity: high)
- **Line 23:** "The database will be initialized by the setup script."
- **Guideline:** Make the actor the subject of the sentence
- **Suggested:** "The setup script initializes the database."
```

If a file has no findings, omit it from the report entirely — do not list it.

End the report with a summary:

```
## Summary
- **Files reviewed:** [N]
- **Total findings:** [N] ([N] high, [N] medium, [N] low)
- **Top issues:** [List the 2-3 most frequent rule violations]
```

## When to Load Reference Files

Load references on demand to conserve context:

| File | When to load |
|------|-------------|
| `references/rules-quick-ref.md` | Always — load at start of every review |
| `references/word-substitutions.md` | When checking word choice or when you encounter a word that might have a simpler alternative |
| `references/active-voice-guide.md` | When you detect passive voice patterns (forms of "to be" + past participle) |
| `references/before-and-after-examples.md` | When crafting suggested rewrites — use as transformation models |
| `references/severity-rubric.md` | When classifying findings — consult definitions and examples |

## Key Rules by Priority

**Critical (always flag):**
- Use simple words and phrases (check against the Dirty Dozen first)
- Avoid jargon (unnecessary complexity, not legitimate technical terms)
- Use active voice (passive voice hides responsibility)

**High (flag unless context justifies):**
- Avoid hidden verbs ("make a determination" → "determine")
- Use terms consistently (don't synonym-swap)
- Write short sentences (~20 words)
- Keep subject-verb-object close together
- Use present tense
- Use "must" not "shall" for requirements
- Address the user ("you")
- Place main idea before exceptions

**Medium (flag with lighter touch):**
- Avoid noun strings (3+ stacked nouns)
- Minimize abbreviations
- Write short paragraphs and sections
- Use lists for series
- Use positive language (avoid double negatives)
- Add useful headings
- Cut excess modifiers (really, very, basically, totally, etc.)
- Avoid doublets and triplets ("cease and desist" → "stop", "null and void" → "void")
- Use general-to-specific order (broad info first, specialized details later)
- Use chronological order for processes (steps in the sequence users follow)

**Low (note, don't belabor):**
- Use contractions where natural (context-dependent)
- Don't use slashes ("and/or")
- Minimize cross-references

## Scope Rules

- **Review:** prose in `.md`, `.mdx`, `.txt`, `.rst`, `.adoc` files; comments in source code files; UI strings; error messages
- **Skip:** code inside fences/backticks, variable names, import statements, configuration values, URLs, file paths
- **Don't rewrite files** — produce recommendations only. The human or agent decides what to apply.
- **Preserve technical terms** — flag jargon only when a simpler alternative exists without losing precision. "Brinulator valve" is fine; "utilize the brinulator valve" is not.

## Attribution

The plain language guidelines and examples referenced by this skill originate from the U.S. federal government's Plain Language initiative, maintained by the General Services Administration (GSA). All guideline content is U.S. government work in the public domain. Source: https://digital.gov/guides/plain-language
