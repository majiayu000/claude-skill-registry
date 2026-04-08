---
name: user-model-builder
description: "Build complete userModels for people Claude Code collaborates with. Creates core persona files, social dossiers with voice analysis, content archives, and INDEX registration. Use when asked to create a user model, build a persona, or document someone's voice and identity."
argument-hint: [person-name]
---

# User Model Builder

Build a complete userModel for **$ARGUMENTS** following the 7-phase workflow below. Each phase must complete before moving to the next. The output is a folder at `~/.claude/userModels/{name}/` containing a core persona, platform-specific dossiers, a content archive, and INDEX registration.

## Phase 1: Discovery

Gather available information about the subject before creating any files.

**Determine:**
- Relationship to the user (collaborator, partner, observed figure)
- Publishing platforms (Substack, Twitter, blog, LinkedIn)
- Scrapeable content availability — dead domains require Wayback Machine CDX API
- Basic identity: full name, email (`~` if unknown), phone (`~` if unknown), location, primary roles

**Ask clarifying questions** if the relationship or scope is ambiguous. Proceed autonomously once direction is clear.

## Phase 2: Folder & Core Persona

Create the userModel directory and core persona file.

1. Create `~/.claude/userModels/{name}/`
2. Write `{name}Model.md` following `references/persona-model-template.md`
3. Frontmatter per `references/frontmatter-schema.md` — `type: user-model`, `category: persona`
4. Required sections: Persona, Education (if known), Career Timeline, Worldview, Writing Voice (brief), Personal, Online Presence
5. Adapt to subject — omit sections that don't apply, add domain-specific sections as needed

## Phase 3: Content Scraping & Archive

Scrape all discoverable published content into `archive/`.

**Per platform:**

| Platform | Tool | Archive path |
|----------|------|-------------|
| Substack | Firecrawl | `archive/substack/YYYY-MM-DD-slug.md` |
| Twitter | Jina (Firecrawl blocks Twitter) | `archive/tweets/` |
| Dead domains | Wayback CDX API → Firecrawl | `archive/{platform}/` |
| LinkedIn | GDPR export via `linkedin-export` skill | `archive/linkedin/` |

**Wayback discovery:**
```
https://web.archive.org/cdx/search/cdx?url=DOMAIN&output=json&fl=timestamp,original&collapse=urlkey
```

**Each archived file gets frontmatter:**
```yaml
---
title: "Post Title"
date: YYYY-MM-DD
source_url: "https://..."
archived_from: "{platform}"
archive_date: YYYY-MM-DD
---
```

**Naming convention:** `YYYY-MM-DD-slug.md` (kebab-case slug from title).

Write `archive/INDEX.md` — table of all files with dates, titles, approximate word counts.

## Phase 4: Voice Analysis & Dossiers

Read the entire archived corpus before beginning analysis. Analyze each platform's content for voice, worldview, and biographical signals.

For each platform, create a social dossier following `references/social-dossier-template.md`.

**Frontmatter:** `type: social-dossier`, `category: {platform}-analysis`, include `corpus` field.

**Required dossier sections:**
- **Source** — URLs, scraping method, verification date
- **Platform Profile** — Handle, legal entity, tagline, cadence, engagement metrics
- **Post/Content Index** — Table: date, title, type, themes
- **Voice Analysis** — Registers, tonal range, sentence mechanics, characteristic phrases. Follow `references/voice-analysis-guide.md`
- **Worldview Markers** — Minimum 5 recurring themes with evidence
- **Biographical Signals** — Per-post table of facts revealed. Separate distinct events.
- **Calibration Quotes** — 10-15 verbatim quotes. Copy directly from archive files. Verify character-by-character: opening words, punctuation, emphasis, quote mark style. Never paraphrase.

Include a Voice Evolution section when the corpus spans 3+ years or crosses a major life transition.

Name dossiers descriptively: `{platform}-{publication-name}.md`.

## Phase 5: Cross-References & Registration

Wire everything together.

1. Add a "Supplementary Dossiers" section to `{name}Model.md` listing all dossiers and archive
2. Update `~/.claude/userModels/INDEX.md`:
   - Add/update the subject's section with a Files table
   - Add Data Collections subsection for archive directories
   - Add Related links (Substack, LinkedIn, etc.)

## Phase 6: Review

Launch a `code-reviewer` subagent to audit all files against `references/review-checklist.md`.

**Priority checks:**
1. Calibration quotes are verbatim (opening words, punctuation, quote style)
2. Author bios are verbatim (not paraphrased)
3. Biographical facts match source (names, dates, locations — distinct events not merged)
4. Frontmatter schema compliance
5. INDEX.md consistency with files on disk
6. Cross-references resolve to real files

Fix all critical and moderate findings before declaring complete.

**Automated validation:**
```bash
uv run ~/.claude/skills/user-model-builder/scripts/validate_usermodel.py ~/.claude/userModels/{name}/
```

## Phase 7: Summary

Report what was built:
- Files created (with paths)
- Corpus stats (post count, word count, date range)
- Key findings (voice registers, worldview themes, biographical discoveries)
- Suggested next steps (RLAMA collection, voice model for composition, etc.)

## Reference Files

| File | Purpose |
|------|---------|
| `references/persona-model-template.md` | Core persona section skeleton |
| `references/social-dossier-template.md` | Social dossier section skeleton |
| `references/frontmatter-schema.md` | YAML frontmatter spec for all file types |
| `references/voice-analysis-guide.md` | Open Souls voice analysis methodology |
| `references/review-checklist.md` | Post-build verification checklist |
| `scripts/validate_usermodel.py` | Structural + quote accuracy validation |
