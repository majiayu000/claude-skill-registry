---
name: Slipbot
description: Used to capture and organize notes, ideas, quotes, and journal entries with automatic tagging, linking, and knowledge graph maintenance.
---

# Configuration

Run `pwd` and get the `{curDir}`

- **Notes directory:** `{curDir}/slipbox/`
- **Graph index:** `{curDir}/slipbox/.graph/graph.json`
- **Timezone:** User's local timezone (check USER.md or system)

# Note Patterns & Types

### Prefixes
- `> {content}` → quote, contains attributed text.
- `! {content}` → idea, for speculative or creative thinking
- `* {content}` → journal, for personal reflection and logs
- `- {content}` → note, for information about subject

### Delimiters
- `~ {content}` → source (appended after prefix+content combination)
    - Example note with source: `- Content here ~ Source Type, Source Title by Source Author`
    - Example quote with source: `> Content here ~ Source Type, Source Author`

# Workflow

## 1. Capture

When a note is recognized:

1. **Extract content and metadata**
    - Note content
    - Type (quote/idea/journal/note)
    - Source information (if provided)

2. **Generate filename**
    - Format: `YYYYMMDD-HHMMSS-slug.md`
    - Slug: lowercase, hyphenated, from content passed in (max 4-5 words)
    - Example: `20260131-143022-compound-interest.md`

3. **Check for existing source**
    - If source is not provided set `source: null`.
    - If source provided, search existing notes for matching source title (case insensitive)
        - Use existing source if found
        - Otherwise, use provided source as-is
        - **No external API calls** - trust user input

4. **Generate tags**
    - Extract specific objects concepts (nouns)
    - Focus on: people, tools, techniques, systems, specific topics
    - **Avoid broad categories** like "productivity" or "ideas"
    - **Consistency:** Check existing tags before creating new ones
    - 2 or 3 tags per note
    - Examples: `[pomodoro-technique, Cal-Newport, deep-work]`

5. **Create markdown file**

```yaml
---
title: "Generated Note Title from Content"
date: 2026-01-31T14:30:22-05:00
type: note
tags: [specific, object, based, tags]
source:
  title: "Source Title"
  type: "book"
  author: "Author Name"
links: []
---

Note content here in markdown.
```
### Note Titles
- **Descriptive but concise:** 3-8 words
- **Avoid generic:** Not "Thoughts" or "Notes", be specific
- **Question format works:** "Why does X happen?" or "How to Y?"

## 2. Link

After creating a note, find connections:

1. **Search existing notes**
   - Look for related concepts, people, topics
   - Check for overlapping tags

2. **Determine connection type**
   - **related** - Similar topic or theme
   - **extends** - Builds on or expands another note
   - **contradicts** - Opposing viewpoint
   - **references** - Mentions same person/book/concept
   - **supports** - Provides evidence for another note

3. **Add bidirectional links**
   - Update both notes' frontmatter
   - Include reason for connection

**Quality over quantity:** Only link when genuinely related

```yaml
links:
  - id: "20260120-093045-compound-interest"
    type: related
    reason: "Both discuss exponential growth concepts"
```

## 3. Note Validations

3.1: **Validate frontmatter** - Ensure the note has the required fields
    - title
    - date
    - type
    - tags

3.2: **Remove broken links**
    - Check if notes that the new note links to still exist
    - If any files are missing save them to `{curDir}/slipbox/missing.md`

## 4. Update Graph

After capture and linking:

4.1: **Load graph index**
    - Read `{curDir}/slipbox/.graph/graph.json`

4.2: **Add/update note entry**

```json
{
  "notes": {
    "20260131-143022-note-title.md": {
      "title": "Your Note Title",
      "source": {
        "title": "Source Title",
        "type": "book",
        "author": "Author Name"
      },
      "type": "note",
      "tags": ["tag1", "tag2"],
      "links": [
          "20260120-093045-other-note.md",
      ]
    }
  },
  "last_updated": "2026-01-31T14:35:00-05:00"
}
```
4.3: **Remove any entries from graph**
    - Read `{curDir}/slipbox/missing.md`
    - If any notes are found missing remove the entry from the graph.
    - Then remove them from `{curDir}/slipbox/missing.md`

4.4: **Rebuild graph**
    - If corrupted beyond simple note removals, rebuild from the current note files.

4.5: **Write updated graph**
    - Save back to `{curDir}/slipbox/.graph/graph.json`

## Querying

Respond to natural queries like: "Show me notes about X"

**Approach:**
1. Search graph index first (fast); only fall back to file search if needed.
2. Present results with titles, dates, snippets
3. Offer to show full content if relevant

## User Feedback

Keep responses minimal:
- ❌ Don't narrate every step unless debugging

### Example Interaction

**User:** "- The Feynman Technique is about teaching concepts to identify gaps in understanding"

**You:**
1. Create `20260131-163500-feynman-technique.md`
2. Tag: `[Feynman-technique, learning, teaching]`
3. Search for related notes (study techniques, learning methods)
4. Link to any relevant note about learning
5. Update graph index
6. Reply: "Note captured: Feynman Technique"

---

**When to apply this skill:** Whenever user shares content that starts with the defined prefixes the content which follows should be captured for later reference.
