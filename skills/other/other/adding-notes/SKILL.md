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
| URL ending in `.pdf` | article (PDF) | `references/content-types/article.md` (use PDF extraction) |
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
| `get-youtube-transcript.py URL [--format FORMAT]` | Video transcript (see formats below) |
| `get-podcast-transcript.py [opts]` | Podcast transcript |
| `get-reddit-thread.py URL --comments N` | Thread + comments |
| `get-goodreads-metadata.sh URL` | Book metadata |
| `get-manga-metadata.sh URL` | Manga series data |
| `get-github-metadata.sh URL` | Repo stats |
| `get-pdf-text.sh URL [output-file]` | Download PDF and extract text (requires `pdftotext`) |

### Transcript Format Options

```bash
get-youtube-transcript.py URL                      # plain (default) - single blob
get-youtube-transcript.py URL --format sentences   # one sentence per line (grep-friendly)
get-youtube-transcript.py URL --format timestamped # [MM:SS] per segment
get-youtube-transcript.py URL --format json        # full metadata with timestamps
```

**Recommended:** Use `--format sentences` for large transcripts—enables grep/search and chunked reading.

**Do NOT use scripts for trivial operations** — do them inline:
- Author check: `Glob` with `content/authors/*{lastname}*.md`
- Frontmatter: Write YAML directly
- Tag lookup: `Grep` or knowledge from prior notes

---

## Workflow Phases

```text
Phase 0: Load SOUL.md → Read SOUL.md for voice, perspective, and anti-patterns
Phase 1: Type Detection → Route to content-type file
Phase 2: Parallel Metadata Collection → Per-type agents
Phase 2.5: Large Transcript Handling → Subagent for >10K token transcripts
Phase 3: Author Creation → See references/author-creation.md
Phase 4: Content Generation → Apply writing-style + SOUL.md voice, generate body
Phase 4.25: Diagram Evaluation → REQUIRED visual assessment with logged outcome
Phase 4.5: Connection Discovery → Find genuine wiki-link candidates (if any exist)
Phase 5: Quality Validation → Parallel validators
Phase 6: Save Note → Write to content/{slug}.md with link density report
Phase 7: MOC Placement → Suggest placements + check MOC threshold
Phase 8: Quality Check → Run pnpm lint:fix && pnpm typecheck
```

### Phase 0: Load Soul (REQUIRED)

Read `SOUL.md` from the project root. This defines Alexander's voice, what he values in notes, anti-patterns to avoid, and how to add his perspective. Every note must reflect this identity — not just summarize a source.

Key things SOUL.md controls:
- **Voice:** Direct, opinionated, no filler — not polished AI prose
- **Perspective:** Always contextualize why Alexander cares about this content
- **Author preservation:** Don't flatten unique voices into generic summaries
- **Anti-patterns:** No sycophancy, no rigid same-template-for-everything, no generic summaries

### Phase 1: Type Detection & Dispatch

1. **Detect type from URL** using the Content Type Routing table above (no script needed)
2. **Load the content-type reference file** for detailed handling
3. Detect `isTechnical` flag (see content-type file for criteria)

### Phase 2: Metadata Collection

Spawn parallel agents as specified in the content-type file. Each file lists:
- Required scripts to run
- Agent configuration
- Special handling notes

**If URL ends in `.pdf`:** WebFetch cannot parse PDFs. Use `get-pdf-text.sh URL` to download and extract text, then read the output file. For large PDFs (>50KB extracted text), use a subagent per Phase 2.5 pattern.

**If `isTechnical: true`:** Also spawn code extraction agent (see `references/code-extraction.md`).

### Phase 2.5: Large Transcript Handling

For podcasts/videos with transcripts >10K tokens, use a dedicated subagent instead of reading directly.

**Detection:** If transcript file exceeds 50KB or initial read fails with token limit error.

**Option A: Transcript Analysis Subagent (Recommended)**

Spawn a Task with `subagent_type: general-purpose`:

```text
Analyze this transcript and extract structured content for a knowledge base note.

**Instructions:**
1. Read the transcript file at: {transcript_path}
2. Extract and return:

## Timestamps
| Time | Topic |
|------|-------|
(Major topic shifts with approximate times)

## Key Arguments
(3-5 main claims with supporting reasoning, 2-3 sentences each)

## Notable Quotes
(4-6 verbatim quotes that capture core ideas, with speaker attribution)

## Named Frameworks
(Any models, principles, or processes given specific names)

## Diagram Candidates
(Any process, system, or framework worth visualizing)

**Output:** Structured markdown, max 1500 words.
```

**Option B: Chunked Extraction (Fallback)**

If subagent unavailable, use `--format sentences` and manual chunking:

1. Fetch with sentences format: `get-youtube-transcript.py URL --format sentences > transcript.txt`
2. Read first 100 lines (intro, episode overview)
3. Read last 100 lines (conclusion, wrap-up)
4. Grep for key terms mentioned in intro
5. Extract quotes around grep matches with `-C 3` context

**Benefits of Subagent Approach:**
| Aspect | Direct Read | Subagent |
|--------|-------------|----------|
| Context usage | Fills main context with raw text | Returns only structured output |
| Parallelism | Sequential processing | Runs alongside other agents |
| Semantic analysis | Manual grep for terms | Agent identifies themes |
| Output quality | May miss connections | Comprehensive extraction |

### Phase 3: Author Creation

For external content, check if author exists:

```text
Glob: content/authors/*{lastname}*.md
```

- **Match found:** Use existing slug
- **Partial match:** Use AskUserQuestion to confirm identity
- **No match:** Create new author per `references/author-creation.md`

### Phase 4: Content Generation

1. **Verify SOUL.md loaded** (REQUIRED): Must have been read in Phase 0. If not, `Read SOUL.md` now
2. **Load writing-style skill** (REQUIRED): `Read .claude/skills/writing-style/SKILL.md`
3. **Load linking philosophy** (REQUIRED): `Read .claude/skills/adding-notes/references/linking-philosophy.md`
4. If `isTechnical`: collect code snippets from Phase 2
5. **Compile frontmatter** using template from content-type file
6. **Generate body** applying SOUL.md voice — add Alexander's perspective, preserve author's unique voice, no generic summaries (see Phase 4.5 for connection discovery)

**Tags:** 3-5 relevant tags. Use tags you've seen in prior notes or `Grep` for similar content to find existing tags.

**Summary:** Frame as a core argument, not a description. What claim does this content make?

### Phase 4.25: Diagram Evaluation (REQUIRED — Visual-First)

Alexander is a visual learner. **Default to adding a diagram.** Only skip when the content is genuinely too brief or structureless (short quotes, link lists).

1. Load `references/diagrams-guide.md` — apply the decision tree (all 7 triggers) with visual-first bias
2. **If diagram needed** (expected for most notes), delegate to the mermaid skill:
   a. Load mermaid skill: `Read .agents/skills/mermaid/skill.md`
   b. Choose the best diagram type — prefer `mindmap` for concept overviews, `flowchart` for processes
   c. Write diagram source to `{slug}.mmd` in project root
   d. Validate: `.agents/skills/mermaid/tools/validate.sh {slug}.mmd`
   e. If validation fails, fix syntax errors and re-validate
   f. Show ASCII preview output to user
   g. Copy validated mermaid block into note wrapped with MDC syntax:
      ```markdown
      ::mermaid
      <pre>
      {validated mermaid source}
      </pre>
      ::
      ```
   h. Delete the `.mmd` file: `command rm {slug}.mmd` (use `command` to bypass shell aliases)
   i. For rich content (books, talks, long articles): consider a second diagram if there's both a concept overview AND a distinct process/framework
3. Log outcome (REQUIRED):
   - Adding: `✓ Diagram added: [mermaid-type] - [description]`
   - Skipping: `✓ No diagram needed: [specific reason]` (should be rare)

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
| Transcript too large (>10K tokens) | Use Phase 2.5 subagent or chunked extraction |
| PDF extraction fails (no `pdftotext`) | Install with `brew install poppler`, then retry |
| Author not found online | Create minimal profile (name only) |
| Reddit 429 | Wait 60s and retry |
| Semantic analysis timeout | Proceed without wiki-link suggestions |
| Validation crash | Warn user, recommend manual check |

---

## Reference Files

| File | Purpose |
|------|---------|
| `SOUL.md` (project root) | Alexander's voice, perspective, and anti-patterns — **load first** |
| `references/author-creation.md` | Author profile workflow |
| `references/diagrams-guide.md` | Decision tree for when to add diagrams |
| `.agents/skills/mermaid/skill.md` | Full mermaid syntax reference + validation (loaded in Phase 4.25) |
| `references/linking-philosophy.md` | Connection quality standards |
| `references/moc-placement.md` | MOC suggestion and creation |
| `references/code-extraction.md` | Technical content code snippets |
| `references/podcast-profile-creation.md` | Podcast show profiles |
| `references/newsletter-profile-creation.md` | Newsletter publication profiles |
| `references/content-types/*.md` | Type-specific templates |
