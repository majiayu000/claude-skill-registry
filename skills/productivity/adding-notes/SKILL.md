---
name: adding-notes
description: Add new notes to the Second Brain knowledge base. Use when the user provides a resource (URL, book, podcast, article, GitHub repo, Reddit thread) and asks to "add a note", "create a note", "save this", "add to my notes", "take notes on", or "capture this".
allowed-tools: Read, Write, Bash, WebFetch, Glob, Grep, Task, TaskOutput, WebSearch, AskUserQuestion
---

# Adding Notes to Second Brain

Add content to the knowledge base with proper frontmatter, tags, summaries, and wiki-links.

## Content Type Routing

Detect type from URL, then load the appropriate reference file.

| URL Pattern | Type | Reference |
|-------------|------|-----------|
| youtube.com | See [YouTube Classification](#youtube-classification) | `references/content-types/youtube.md` or `talk.md` or `podcast.md` |
| reddit.com | reddit | `references/content-types/reddit.md` |
| github.com | github | `references/content-types/github.md` |
| imdb.com/title/, themoviedb.org/movie/ | movie | `references/content-types/movie.md` |
| goodreads.com/series/ | manga | `references/content-types/manga.md` |
| goodreads.com, amazon.com (books) | book | `references/content-types/book.md` |
| spotify.com/episode, podcasts.apple.com | podcast | `references/content-types/podcast.md` |
| udemy.com, coursera.org, skillshare.com | course | `references/content-types/course.md` |
| *.substack.com/p/*, *.beehiiv.com/p/*, buttondown.email/* | newsletter | `references/content-types/newsletter.md` |
| Other URLs | article | `references/content-types/article.md` |
| No URL | note | `references/content-types/note.md` |
| Manual: `quote` | quote | `references/content-types/quote.md` |
| Manual: `evergreen` | evergreen | `references/content-types/evergreen.md` |
| Manual: `map` | map | `references/content-types/map.md` |

### YouTube Classification

YouTube URLs require sub-classification before processing:

1. **Known podcast channel?** → `references/content-types/podcast.md`
2. **Known talk channel OR conference title?** → `references/content-types/talk.md`
3. **Tutorial signals?** → `references/content-types/youtube.md` with `isTechnical: true`
4. **Default** → `references/content-types/youtube.md`

See `references/content-types/youtube.md` for full classification logic and channel lists.

---

## Scripts Reference

Only use scripts that fetch external data or perform complex processing:

| Script | Purpose |
|--------|---------|
| `get-youtube-metadata.sh URL` | Video title, channel |
| `get-youtube-transcript.py URL` | Video transcript |
| `get-podcast-transcript.py [opts]` | Podcast transcript |
| `get-reddit-thread.py URL --comments N` | Thread + comments |
| `get-goodreads-metadata.sh URL` | Book metadata |
| `get-manga-metadata.sh URL` | Manga series data |
| `get-github-metadata.sh URL` | Repo stats |
| `find-related-notes.ts FILE [--limit N] [--min-score N]` | Semantic search using project embeddings |

**Do NOT use scripts for trivial operations** — do them inline:
- Author check: `Glob` with `content/authors/*{lastname}*.md`
- Frontmatter: Write YAML directly
- Tag lookup: `Grep` or knowledge from prior notes

---

## Workflow Phases

```text
Phase 1: Type Detection → Route to content-type file
Phase 2: Parallel Metadata Collection → Per-type agents
Phase 3: Author Creation → See references/author-creation.md
Phase 4: Content Generation → Apply writing-style, generate body
Phase 4.25: Diagram Evaluation → REQUIRED visual assessment with logged outcome
Phase 4.5: Connection Discovery → Find genuine wiki-link candidates (if any exist)
Phase 5: Quality Validation → Parallel validators
Phase 6: Save Note → Write to content/{slug}.md with link density report
Phase 7: MOC Placement → Suggest placements + check MOC threshold
Phase 8: Quality Check → Run pnpm lint:fix && pnpm typecheck
```

### Phase 1: Type Detection & Dispatch

1. **Detect type from URL** using the Content Type Routing table above (no script needed)
2. **Load the content-type reference file** for detailed handling
3. Detect `isTechnical` flag (see content-type file for criteria)

### Phase 2: Metadata Collection

Spawn parallel agents as specified in the content-type file. Each file lists:
- Required scripts to run
- Agent configuration
- Special handling notes

**If `isTechnical: true`:** Also spawn code extraction agent (see `references/code-extraction.md`).

### Phase 3: Author Creation

For external content, check if author exists:

```text
Glob: content/authors/*{lastname}*.md
```

- **Match found:** Use existing slug
- **Partial match:** Use AskUserQuestion to confirm identity
- **No match:** Create new author per `references/author-creation.md`

### Phase 4: Content Generation

1. **Load writing-style skill** (REQUIRED): `Read .claude/skills/writing-style/SKILL.md`
2. **Load linking philosophy** (REQUIRED): `Read .claude/skills/adding-notes/references/linking-philosophy.md`
3. If `isTechnical`: collect code snippets from Phase 2
4. **Compile frontmatter** using template from content-type file
5. **Generate body** with wiki-links (see Phase 4.5 for connection discovery)

**Tags:** 3-5 relevant tags. Use tags you've seen in prior notes or `Grep` for similar content to find existing tags.

**Summary:** Frame as a core argument, not a description. What claim does this content make?

### Phase 4.25: Diagram Evaluation (REQUIRED)

1. Load `references/diagrams-guide.md`
2. Apply the decision tree based on content type priority
3. Log outcome (REQUIRED):
   - Adding: `✓ Diagram added: [mermaid-type] - [description]`
   - Skipping: `✓ No diagram needed: [specific reason]`

### Phase 4.5: Connection Discovery

Load `references/linking-philosophy.md` and follow the discovery checklist:

1. **Same-author check** (highest priority): `Grep pattern: "authors:.*{author-slug}" glob: "content/*.md"`
2. **Tag-based discovery**: `Grep pattern: "tags:.*{tag}" glob: "content/*.md" limit: 5`
3. **Evaluate**: "Would I naturally reference this when discussing the topic?"

Only add genuine connections with explanatory context. Orphans are acceptable.

### Phase 5: Quality Validation

Spawn parallel validators:

| Validator | Checks |
|-----------|--------|
| Wiki-link exists | Each `[[link]]` exists in `content/` (excluding Readwise) |
| Link context | Each link has adjacent explanation (not bare "See also") |
| Duplicate | Title/URL doesn't already exist |
| Tag | Tags match or similar to existing |
| Type-specific | E.g., podcast: profile exists, guest not in hosts |

**Wiki-link note:** Readwise highlights (`content/readwise/`) are excluded from Nuxt Content and won't resolve as valid wiki-links. Use plain text or italics for books/articles that only exist in Readwise.

**If issues found:** Use AskUserQuestion to offer: Fix issues / Save anyway / Cancel.
**If no issues:** Log "✓ Validation passed" and proceed.

### Phase 6: Save Note

Generate slug inline: lowercase title, replace spaces with hyphens, remove special characters.
Example: `"Superhuman Is Built for Speed"` → `superhuman-is-built-for-speed`

Save to `content/{slug}.md`. Confirm with link density status:

```text
✓ Note saved: content/{slug}.md
  - Type: {type}
  - Authors: {author-slugs}
  - Tags: {tag-count} tags
  - Diagram: {diagram-status}
  - Wiki-links: {link-count} connections ({status})
    - [[link-1]] (why: {context})
    - [[link-2]] (why: {context})
```

**Diagram status:** `Added: [type] - [description]` or `None: [reason]`

**Link density status:**
- `{link-count} >= 3`: "well-connected"
- `{link-count} = 1-2`: "connected"
- `{link-count} = 0`: "standalone" (fine when no genuine connections exist)

### Phase 7: MOC Placement (Non-blocking)

See `references/moc-placement.md` for detailed workflow:
1. Suggest existing MOC placement via cluster script
2. Check if any tag exceeds 15-note threshold for new MOC creation

### Phase 8: Quality Check

Run linter and type check to catch any issues:

```bash
pnpm lint:fix && pnpm typecheck
```

If errors are found, fix them before completing the task.

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Metadata agent fails | Prompt for manual entry or WebFetch fallback |
| Transcript unavailable | Note "No transcript available" in body |
| Author not found online | Create minimal profile (name only) |
| Reddit 429 | Wait 60s and retry |
| Semantic analysis timeout | Proceed without wiki-link suggestions |
| Validation crash | Warn user, recommend manual check |

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/author-creation.md` | Author profile workflow |
| `references/diagrams-guide.md` | When/how to add mermaid diagrams |
| `references/linking-philosophy.md` | Connection quality standards |
| `references/moc-placement.md` | MOC suggestion and creation |
| `references/code-extraction.md` | Technical content code snippets |
| `references/podcast-profile-creation.md` | Podcast show profiles |
| `references/newsletter-profile-creation.md` | Newsletter publication profiles |
| `references/content-types/*.md` | Type-specific templates |
