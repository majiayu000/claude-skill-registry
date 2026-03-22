---
name: copyedit
description: Edit blog posts and book reviews. Use `/copyedit grammar` for spelling/grammar only, or `/copyedit polish` for fuller editing. Preserves the author's voice and style.
---

# Copyedit Skill

Edit drafts for alexgude.com while preserving voice and style.

## Usage

- `/copyedit grammar` --- Fix only spelling, grammar, and punctuation. Change nothing else.
- `/copyedit polish` --- Fix errors, improve clarity, reword for coherence. Preserve voice.

If no mode is specified, ask which mode to use.

## Instructions

### Grammar Mode

Fix ONLY:
- Spelling errors
- Grammar mistakes (subject-verb agreement, tense consistency)
- Punctuation errors
- Typos

### Polish Mode

Follow this prompt:
> Fix errors, make it clearer. Reword to make the arguments and sentences more
> coherent. Use the same sort of words I'm using, don't substitute fancy
> synonyms. Maintain my voice.

You may:
- Fix all grammar/spelling issues
- Restructure sentences for clarity
- Improve flow between ideas
- Cut unnecessary words

You must:
- Preserve the author's vocabulary---don't upgrade "good" to "exceptional"
- Keep the same level of formality
- Maintain opinions and judgments as written
- Preserve all Liquid tags and formatting exactly

## Output Format

### Polish Mode

**Add the edited copy to the bottom of the article, separated by a markdown HR break.** This is a first draft. After that, work with the author to iterate: propose options for specific sentences or paragraphs, discuss transitions, and refine collaboratively.

### Grammar Mode

Change in place, and also list the changes made so the author can review them.

## Voice & Style Guide

See [references/STYLE.md](references/STYLE.md) for the complete style guide.

Key points:
- **Tone**: First-person, conversational but substantive, direct and opinionated
- **Vocabulary**: Simple, direct words. "great", "fun", "loved"---not "exceptional", "delightful", "adored"
- **Hedging**: Avoid. Say "I didn't like it" not "I perhaps didn't fully appreciate it"
- **Em-dashes**: Do NOT add em-dashes. LLMs overuse them. Only keep existing ones if appropriate.
- **Contractions**: Use naturally, don't insert needlessly.
- **Oxford comma**: Yes

### Anti-patterns (never do these)

- Don't add too many em-dashes (---)
- Don't add emojis
- Don't add exclamation marks unless the original has them
- Don't use "delve", "tapestry", "nuanced", "compelling"
- Don't add hedging words ("perhaps", "somewhat", "rather")
- Don't make it sound more formal or academic
- Don't add superlatives or intensifiers
- Don't stack comma-separated adjectives ("brutal, high-stakes", "dark, gritty"). Pick one.

## Book Review Structure

See [references/BOOK-REVIEWS.md](references/BOOK-REVIEWS.md) for details on book review structure.

Key constraints:
- **First paragraph**: Uses inline plugin tags (`{% book_link page.title %}`, `{% author_link page.book_authors %}`, `{% series_text page.series %}`), but no capture variables. This paragraph is pulled out for social media previews, so it must stand alone.
- **After first paragraph**: `{% capture %}` blocks define template variables, then prose continues using those variables.
- **Paragraph 2 transition**: The challenge is prose flow---don't repeat too much of what paragraph 1 just said. Find a new angle or continue the thought. Generally the author has already tried to do this but help them a bit.
- **References to other works**: These create backlinks, so mentioning other books/authors is encouraged, but again the author will have filled in most of these. You may suggest others.

## Plugin Reference

See [references/PLUGINS.md](references/PLUGINS.md) for the full plugin reference.

Common tags you'll encounter:
- `{% book_link "Title" %}` --- link to a book
- `{% author_link "Name" %}` --- link to an author (supports `possessive`, `link_text=`)
- `{% series_link "Series" %}` --- link to a series
- `{% capture var %}...{% endcapture %}` --- define reusable variables

Do not modify these tags. Preserve them exactly as written.
