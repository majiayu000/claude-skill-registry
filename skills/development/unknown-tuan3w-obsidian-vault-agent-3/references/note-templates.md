# Note Templates — book-analyzer output formats

**Note creation:** Use `python3 .claude/scripts/create-note.py <type> "Title" [key=value]`
to create notes with correct frontmatter and template structure. The script reads
Obsidian core templates from `templates/` and resolves `{{date:FORMAT}}` / `{{title}}`
placeholders. After creation, use Edit to fill the body.

These templates document the **body structure** each agent should produce.
The frontmatter is handled by `create-note.py` — agents only need to fill content.

---

## 1. Obsidian Book Note (default)

Created via: `python3 .claude/scripts/create-note.py book "{Title}" author="{Author}" year={YEAR}`

After creation, Edit the note to add `processing_status: inbox` to frontmatter and fill body:

```markdown
🏷️Tags: #book #{TOPIC} #{MM-YYYY}

> **Core Thesis:** {CORE_THESIS}
<!-- 2-3 sentences from book-synthesizer "Core Thesis" section -->

## Key Themes
{THEMES}
<!-- 3-5 bullets: - **Theme Name** — explanation referencing specific chapters -->

## Chapter Notes
{CHAPTER_NOTES}
<!-- Each chapter as H3 (### Ch N: Title) with Key Ideas bullets (as many as the
     chapter earns — no artificial cap), quotes in > blockquote format, and an
     Examples & Anecdotes subsection for concrete stories/case studies.
     Bold key terms. Use [[wikilinks]] for vault terms. -->

## Critical Assessment
{ASSESSMENT}
<!-- Strengths, Weaknesses, Missing sub-sections -->

## Cross-Domain Connections
{CONNECTIONS}
<!-- Use [[wikilinks]] to link to existing vault notes -->

## Questions
{QUESTIONS}
<!-- Merged from chapter-analyst + book-synthesizer. Deduplicate. -->

## Related Links
- {LINKS}
<!-- Wikilinks to related vault notes, extracted terms, source URL -->
```

---

## 2. Markdown Template (generic, no vault)

For standalone output when not in an Obsidian vault. No frontmatter, no wikilinks.

```markdown
# {TITLE}

**Author:** {AUTHOR} | **Analyzed:** {DATE}

## Core Thesis
{CORE_THESIS}

## Key Themes
{THEMES}
<!-- Same content, plain text references instead of wikilinks -->

## Chapter Notes
{CHAPTER_NOTES}

## Critical Assessment
{ASSESSMENT}

## Questions
{QUESTIONS}
```

---

## 3. Term Note Body

Created via: `python3 .claude/scripts/create-note.py term "{Term Name}" processing_status=processed`

After creation, Edit the note to fill body content:

```markdown
- **{TERM_NAME}** — {DEFINITION}
<!-- One-sentence definition in your own words. Must stand alone without book context. -->
- {CONTEXT_BULLET}
<!-- Concrete example or "why it matters" bullet. Vivid > abstract. -->

## Links
- Extracted from: [[{BOOK_TITLE}]]
<!-- Short-form wikilink — Obsidian resolves [[Title]] automatically -->
- Related: {RELATED_WIKILINKS}
<!-- [[wikilinks]] to vault notes. Prefer cross-domain links. -->
```

The script handles: frontmatter (id, dates, type: term), `[ ](#anki-card)` anchor,
`🏷️Tags` line with `#all-anki` and `#MM-YYYY`. Agent only fills definition + links.
