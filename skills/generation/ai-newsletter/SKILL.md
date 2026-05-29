---
name: ai-newsletter
description: Curate weekly newsletter from checked stories in daily AI digests. Extracts [x] marked items, groups into narrative themes, generates editorial newsletter.
argument-hint: "[--week YYYY-WNN] [--dry-run] [--force]"
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: true
---

# AI Weekly Newsletter Skill

Generate curated weekly newsletter from stories marked `[x]` in daily AI digests.

**Prerequisite:** User must check `- [x]` on desired stories in daily digest files (Notion renders these as clickable checkboxes).

## Arguments

Parse from `$ARGUMENTS`:

- `--week YYYY-WNN` — Target week (e.g., `2026-W06`). Default: current week
- `--dry-run` — Show extraction results without saving
- `--force` — Allow re-publishing a week already in `.published-issues`

## State Files

### Published Issues

Track published newsletters in:

```text
./findings/ai-newsletter/.published-issues
```

Format: `YYYY-WNN|YYYY-MM-DD` (one line per issue)

Example:

```text
2026-W05|2026-02-02
2026-W06|2026-02-09
```

## Workflow

### Phase 1: Setup

1. Parse arguments for `--week`, `--dry-run`, `--force`
2. Determine target week:
   - If `--week` provided: use that week
   - Default: current ISO week
3. Calculate date range (Monday to Sunday of target week)
4. Read `.published-issues` file:
   - If target week already published AND no `--force` flag → error with message: `"Week {YYYY-WNN} already published on {date}. Use --force to regenerate."`
   - If missing: create empty file
5. Read `output-template.md` for newsletter format

### Phase 2: Extract Checked Stories

1. Glob digest files in date range:

```text
./findings/ai-daily-digest/ai-digest-{YYYY-MM-DD}.md
```

Match files where date falls within Mon-Sun of target week.

2. For each digest file:
   - Read file content
   - Extract all lines matching `- [x] **` (checked story items)
   - For each matched line, capture:
     - **title** — text between `**` markers
     - **summary** — text after `**` and before `[[Source]` or `[Source`
     - **url** — source URL
     - **section** — nearest `##` or `###` header above the line
     - **date** — from filename

3. If zero checked stories found:
   - Error: `"No stories marked [x] found in digests for week {YYYY-WNN} ({date_range}). Check stories in Notion first."`
   - Abort

4. Store extracted stories with metadata.

### Phase 3: Categorize into Themes

Group stories into narrative themes based on content similarity:

**Rules:**

- **1-2 stories total:** Skip theming, use simple list format
- **3-7 stories:** Group into 2 themes
- **8-15 stories:** Group into 2-4 themes + Quick Hits overflow
- **16+ stories:** 3-4 themes + generous Quick Hits

**Theme generation:**

- Analyze story titles, summaries, and sections
- Create narrative theme titles (NOT mechanical section names)
- Pick appropriate emoji for each theme
- Select lead story for each theme (most impactful)
- Overflow stories (don't fit themes cleanly) → Quick Hits

**Good theme names:**

- "The Open Source Surge" (not "Open Source AI")
- "Agents Are Everywhere" (not "AI Tools")
- "The Infrastructure Race" (not "Hardware & Infra")
- "When AI Meets Science" (not "Research Papers")

**Bad theme names:**

- Direct copies of digest section names
- Single-word themes
- Generic "AI News" / "Updates"

### Phase 4: Generate Newsletter

1. Load `output-template.md`
2. Generate content:

**Editorial opening (This Week in AI):**
- 2-3 sentences capturing the week's narrative
- Reference the biggest story
- Set the tone (exciting, concerning, transformative, etc.)

**Themed sections:**
- 1-2 sentence context for the theme
- Each story: enhanced summary (expand beyond original 1-liner)
- Append `| *{Mon DD}*` date to each story
- "Why this matters" analysis after each theme's stories

**Quick Hits:**
- 1-line per story (title + brief summary + source)
- For overflow that didn't fit themes

**Looking Ahead:**
- 2-3 bullet points on trends to watch based on this week's stories
- Forward-looking, not summary

3. If `--dry-run`: output to console, skip Phase 5

### Phase 5: Save Newsletter

**Step 1:** Create directory if needed

```bash
mkdir -p ./findings/ai-newsletter
```

**Step 2:** Write newsletter to Notion workspace

Use Notion MCP to create page in workspace with title `AI Newsletter {YYYY-WNN}` and content formatted per template.

**Step 3:** Write archive copy

```text
./findings/ai-newsletter/ai-newsletter-{YYYY-WNN}.md
```

**Step 4:** Update `.published-issues`

Append line: `{YYYY-WNN}|{today's date YYYY-MM-DD}`

**Verification:** Confirm Notion page created + 1 archive file + 1 state file updated.

## Output Requirements

- Use emojis in section headers
- Bullet points over paragraphs
- Every story must have source URL
- Include story count and digest count in header
- Wikilinks to vault notes where relevant
- Tags: `#ai-newsletter #weekly #YYYY-WNN`

## Error Handling

- Zero marked stories → clear error message, abort
- Missing digest files for date range → warn, continue with available files
- Already published week → blocked unless `--force`
- Single digest file in range → proceed normally (partial week OK)

## Example Invocations

```bash
# Current week newsletter
/ai-newsletter

# Specific week
/ai-newsletter --week 2026-W06

# Preview without saving
/ai-newsletter --dry-run

# Regenerate already-published week
/ai-newsletter --week 2026-W05 --force
```
