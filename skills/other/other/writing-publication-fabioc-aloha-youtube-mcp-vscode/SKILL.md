---
name: "Writing & Publication Skill"
description: "Patterns for technical writing, academic publication, content strategy, and Word-compatible research formatting."
---

# Writing & Publication Skill

> Patterns for technical writing, academic publication, and content strategy.

## Writing Formats

| Format | Audience | Length | Review |
| ------ | -------- | ------ | ------ |
| Academic Paper | Researchers | 4-10K words | Peer (2-6 mo) |
| Workshop Paper | Researchers | 2-4K words | Light (1-2 mo) |
| Trade Publication | Practitioners | 1-2K words | Editorial (2-4 wk) |
| Blog Post | Developers | 500-1.5K words | Self |
| Documentation | Users | Variable | Internal |

## Academic Paper Structure

1. **Abstract** — Problem, approach, results, implications (150-300 words)
2. **Introduction** — Motivation, problem, contributions, outline
3. **Related Work** — Position within existing research
4. **Methodology** — How you did it (reproducible)
5. **Implementation** — Technical details (if applicable)
6. **Evaluation** — Evidence for claims
7. **Discussion** — Interpretation, limitations
8. **Conclusion** — Summary, future work
9. **References** — Venue-specific format

## Writing Principles

- Precision over flair
- Evidence for claims (data or citations)
- Acknowledge limitations
- Active voice preferred
- Define terms on first use
- Break sentences at 25-30 words

## Pitfalls to Avoid

| Bad | Fix |
| --- | --- |
| "might possibly perhaps" | "may" |
| "revolutionary" | "novel approach" |
| "was performed" | "we performed" |
| Jargon without definition | Define on first use |
| Buried contributions | State explicitly in intro |

## Structuring Arguments

**CARS Model (Introductions):**

1. Establish territory (topic importance)
2. Establish niche (gap in knowledge)
3. Occupy niche (your contribution)

**Heilmeier Catechism (Motivation):**

- What are you trying to do?
- How is it done today? Limits?
- What's new in your approach?
- Who cares? What difference?
- What are the risks?

## Audience Adaptation

| Audience | Adjust |
| -------- | ------ |
| Researchers | Add theoretical framing, citations |
| Practitioners | Add code examples |
| Executives | Add business value |
| General tech | Remove jargon |

## Publication Strategy

**Venue sequencing:**

1. Trade publication → immediate visibility
2. arXiv pre-print → establish priority
3. Workshop paper → academic credibility
4. Journal/conference → peer-reviewed validation

**First-time author:**

- Start with lower-barrier venues
- Collaborate with established authors
- Target workshops first
- Conduct user studies (empirical data strengthens)

## Responding to Reviews

| Feedback | Response |
| -------- | -------- |
| "Missing related work" | Add citations, explain positioning |
| "Claims not supported" | Add evidence or soften claims |
| "Unclear methodology" | Expand description |
| "Limited evaluation" | Add studies or acknowledge |

**Response letter**: Thank → Summarize changes → Address each point → Highlight extras

## Pre-Submission Checklist

- [ ] Abstract stands alone
- [ ] Contributions stated in intro
- [ ] Claims supported by evidence
- [ ] Limitations acknowledged
- [ ] References complete
- [ ] Figures/tables readable
- [ ] Page limit respected
- [ ] Code available (if applicable)

## Word-Compatible Research Writing Style

Conventions for research documents authored in Markdown and converted to Word via Pandoc or md-to-word.

### Punctuation Rules

| Instead of | Use | When |
| ---------- | --- | ---- |
| Em-dash (—) | Colon (:) | Elaboration or definition: "The framework provides: integration across domains" |
| Em-dash (—) | Comma (,) | Parenthetical aside: "The model, originally designed for therapy, applies broadly" |
| Em-dash (—) | Semicolon (;) | Related independent clauses: "The theory is sound; the implementation follows" |
| Em-dash (—) | Period (.) | Full sentence break: "This completes Phase 1. The next phase begins" |
| Double-hyphen (--) | Same as above | Never use -- as a substitute; apply proper punctuation directly |

### Definition List Formatting

Use bold term followed by colon, no dash separators:

```markdown
<!-- Bad -->
**Term** — description
**Term** -- description

<!-- Good -->
**Term**: description
```

### Formal Tone

| Avoid | Use |
| ----- | --- |
| Contractions (isn't, it's, don't) | Full forms (is not, it is, do not) |
| Em-dashes for drama | Colons for precision |
| First person plural ("we find") | Active voice with subject ("the analysis reveals") |

### Markdown Elements to Avoid for Word

| Element | Problem | Alternative |
| ------- | ------- | ----------- |
| `---` horizontal rules | Renders as full-width line in Word | Use headings or blank lines for separation |
| `\n` in Mermaid labels | Not rendered; breaks labels | Use `<br/>` for line breaks |
| Nested blockquotes | Inconsistent Word rendering | Use single-level blockquotes only |
| HTML tags in body text | May not convert | Use pure Markdown |

### APA 7 Conventions for Markdown

- **In-text citations**: parenthetical `(Author, Year)` or narrative `Author (Year)`
- **References**: alphabetical by last name, hanging indent, sentence-case titles
- **Title page**: title, authors, date, abstract paragraph (no page numbers in Markdown)
- **Headings**: H1 for title, H2 for major sections, H3 for subsections (maps to APA levels)
- **Tables**: include descriptive captions above, notes below
- **Figures**: Mermaid diagrams count as figures; caption with "Figure N." prefix

### Mermaid Diagram Conventions for Research

- Use `%%{init: {'theme': 'base', 'themeVariables': {...}}}%%` for consistent styling
- Line breaks: `<br/>` only; never `\n`
- Keep node text concise; move detail to surrounding prose
- GitHub Pastel v2 palette for professional appearance
- Export as PNG before Word conversion if diagram fidelity is critical

## Tools

| Tool | Purpose |
| ---- | ------- |
| Overleaf | LaTeX collaboration |
| Grammarly | Grammar/style |
| Zotero | References |
| Connected Papers | Literature discovery |
| Pandoc | Markdown to Word conversion |
| md-to-word skill | Markdown + Mermaid to Word pipeline |

## Synapses

See [synapses.json](synapses.json) for connections.
