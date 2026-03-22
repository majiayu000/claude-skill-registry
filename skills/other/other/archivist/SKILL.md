---
name: archivist
description: "Universal content cataloging system. Save URLs, files, snippets, or voice notes with descriptions, auto-tag everything, make it all searchable. Use when: building a personal knowledge base, saving reference material, or organizing research. NOT for: file backup, website mirroring, or large-scale web scraping."
homepage: https://pawhub.ai/archivist
metadata:
  {
    "openpaw":
      {
        "emoji": "📁",
        "requires": { "bins": ["curl", "sqlite3"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@pawhub/archivist",
              "bins": ["archivist"],
              "label": "Install Archivist (npm)",
            },
          ],
      },
  }
---

# Archivist 📁

Your personal librarian. Save anything — URLs, files, notes, screenshots — and Paw makes it searchable, tagged, and instantly retrievable.

## When to Use

✅ **USE this skill when:**

- "Save this article for later"
- Building a personal knowledge base
- Organizing research materials
- Archiving reference links
- Saving code snippets with context
- Creating a searchable bookmark library
- Capturing voice notes with transcription
- Organizing screenshots with descriptions
- Building a "second brain"

## When NOT to Use

❌ **DON'T use this skill when:**

- Full file backup/sync → use Time Machine, Backblaze, etc.
- Website mirroring → use wget, HTTrack
- Large-scale web scraping → use Scrapy, Apify
- Photo library management → use Photos, Lightroom
- Document version control → use Git, Dropbox versioning
- Collaborative wikis → use Notion, Obsidian Sync

## Setup

Install Archivist:

```bash
npm install -g @pawhub/archivist
```

Initialize your archive:

```bash
# Create archive database
archivist init

# Set storage location (default: ~/.archivist)
archivist config set storage-path ~/Documents/Archive

# Verify setup
archivist status
```

## Example Interactions

### Saving Content

**You:** Save this for later: https://example.com/great-article

**Paw:** *fetches and archives the page*

✅ **Saved:** "How to Build Better APIs"

**Captured:**
- Full HTML (for offline reading)
- Screenshot (visual reference)
- Extracted text (for search)
- Title: "How to Build Better APIs"
- Author: Jane Smith
- Published: 2026-01-15

**Auto-tags:** #api-design #programming #webdev

**Summary (AI-generated):**
> Article discusses REST vs GraphQL trade-offs, API versioning strategies, and authentication best practices. Includes code examples in Python and Node.js.

**Archive ID:** `arch_abc123`

Want to add custom tags or notes? Just say the word. 🐾

---

**You:** Add tags: must-read, reference, backend

**Paw:** *updates the entry*

✅ Tags updated:
- #api-design (auto)
- #programming (auto)
- #webdev (auto)
- #must-read (you)
- #reference (you)
- #backend (you)

Searchable immediately. Try: `archivist search "api design must-read"` 📚

---

**You:** Save this snippet:

```python
def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

**Paw:** *analyzes and archives the code*

✅ **Saved:** Code snippet

**Details:**
- Language: Python
- Type: Function definition
- Name: `retry_with_backoff`
- Lines: 9

**Auto-tags:** #python #error-handling #retry-logic

**AI Summary:**
> Implements exponential backoff retry logic. Useful for API calls and network operations.

**Archive ID:** `arch_xyz789`

**Suggested title:** "Python Retry with Exponential Backoff"

Looks good? (yes/edit)

---

**You:** Yes

**Paw:** Perfect. Archived under #python #error-handling. Search it anytime with `archivist search retry` or just ask me "find that Python retry function." 🔍

---

### Searching Your Archive

**You:** Find articles about API design

**Paw:** *searches archive*

Found **4 results** for "API design":

**1. How to Build Better APIs** (2 days ago)
   📄 Article · https://example.com/great-article
   Tags: #api-design #programming #must-read
   *REST vs GraphQL trade-offs, versioning...*

**2. REST API Best Practices 2026** (1 week ago)
   📄 Article · https://dev.to/rest-best-practices
   Tags: #api-design #rest #backend
   *Modern patterns for REST APIs including...*

**3. Designing APIs for Scale** (2 weeks ago)
   📄 Article · https://scaling.example.com
   Tags: #api-design #distributed-systems
   *Load balancing, rate limiting, caching strategies...*

**4. GraphQL Schema Design** (3 weeks ago)
   📄 Article · https://graphql-guide.example.com
   Tags: #api-design #graphql
   *Schema-first development, resolvers...*

Want me to open one? (1-4) 📖

---

**You:** Open 1

**Paw:** *opens the archived page*

Opening "How to Build Better APIs" in your browser...
(Archived version — works offline)

**Quick actions:**
- `archivist note arch_abc123 "Used this for the v2 API redesign"`
- `archivist share arch_abc123` (get shareable link)
- `archivist export arch_abc123 --format pdf`

Anything else? 🐾

---

### Voice Notes

**You:** *[voice message]* "Idea for the new feature: what if we added real-time collaboration like Figma but for code? Users could see each other's cursors and edits live. Would need WebSockets and operational transforms. Check out Yjs library."

**Paw:** *transcribes and archives*

✅ **Voice note saved**

**Transcription:**
> Idea for the new feature: what if we added real-time collaboration like Figma but for code? Users could see each other's cursors and edits live. Would need WebSockets and operational transforms. Check out Yjs library.

**Auto-tags:** #ideas #real-time #collaboration #websockets

**Extracted mentions:**
- Figma (reference)
- Yjs (library to research)
- WebSockets (tech)
- Operational transforms (concept)

**AI Summary:**
> Feature idea: real-time collaborative code editing with live cursors. Implementation notes: WebSockets + operational transforms. Research Yjs library.

**Archive ID:** `arch_voice_456`

Created follow-up todo: "Research Yjs library for operational transforms"

Want me to find similar ideas in your archive? 💡

---

### Advanced Search

**You:** Show me everything I saved last month about Python

**Paw:** *filters archive*

**Last month (Jan 2026) · Python:** 12 items

**Breakdown:**
- 🔗 Articles: 7
- 📄 Code snippets: 4
- 🎤 Voice notes: 1

**Top tags:**
- #python (12)
- #async (5)
- #fastapi (3)
- #testing (3)

**Most referenced:**
1. "Async Python Patterns" (opened 8 times)
2. "FastAPI Best Practices" (opened 5 times)

Want the full list or just the highlights? 📊

---

**You:** Just highlights

**Paw:** **Top 3 from last month:**

**1. Async Python Patterns**
   📄 Article · Saved Jan 5
   Tags: #python #async #advanced
   *Comprehensive guide to asyncio, context managers, generators*
   **Why it stood out:** You've opened this 8 times

**2. Python retry function snippet**
   📋 Code · Saved Jan 12
   Tags: #python #error-handling
   *Exponential backoff retry logic*
   **Why it stood out:** You added note "use this everywhere"

**3. Testing async code**
   📄 Article · Saved Jan 18
   Tags: #python #testing #async
   *pytest-asyncio examples and best practices*
   **Why it stood out:** Tagged as #must-read

Want to review any of these? 🐾

---

### Organization

**You:** How's my archive looking?

**Paw:** *generates statistics*

**📁 Your Archive**

**Total items:** 847
**Added this week:** 23
**Storage used:** 1.2 GB

**Breakdown by type:**
- 🔗 URLs/Articles: 512 (60%)
- 📄 Code snippets: 178 (21%)
- 📎 Files: 94 (11%)
- 🎤 Voice notes: 41 (5%)
- 📸 Screenshots: 22 (3%)

**Most common tags:**
1. #programming (234)
2. #javascript (142)
3. #reference (128)
4. #api-design (89)
5. #must-read (67)

**Recent additions:**
- Today: 3 items
- Yesterday: 7 items
- This week: 23 items

**Search hotspots:**
- You search for "api" most often (42 times)
- "async" is trending up (15 searches this month)

**Suggestions:**
- 23 items have no tags → want me to auto-tag?
- 12 broken links detected → run health check?
- 8 duplicate URLs found → merge them?

Need anything? 📚

## Commands

### Saving Content

```bash
# Save a URL
archivist save "https://example.com/article"

# Save with custom title and tags
archivist save "https://example.com" \
  --title "Great Article" \
  --tags "programming,reference"

# Save a file
archivist save-file ~/Downloads/paper.pdf \
  --tags "research,ml"

# Save a code snippet
archivist save-snippet code.py \
  --language python \
  --tags "async,example"

# Save from clipboard
archivist save-clipboard --tags "quick-save"

# Voice note (with transcription)
archivist voice-note record --tags "ideas"
```

### Searching

```bash
# Full-text search
archivist search "api design patterns"

# Search by tag
archivist search --tag python --tag async

# Search by type
archivist search --type article "REST"

# Search by date
archivist search --since "2026-01" --until "2026-02"

# Fuzzy search (typo-tolerant)
archivist search "pyton asyncio" --fuzzy

# Show recent additions
archivist recent --limit 10
```

### Organization

```bash
# List all tags
archivist tags list

# Rename a tag
archivist tags rename old-tag new-tag

# Merge tags
archivist tags merge python,python3 --into python

# Auto-tag untagged items
archivist auto-tag

# Find duplicates
archivist duplicates --action review

# Health check (broken links, etc.)
archivist health-check --fix
```

### Exporting

```bash
# Export single item
archivist export arch_abc123 --format pdf

# Export by tag
archivist export --tag must-read --format markdown

# Export search results
archivist search "api" --export --format html

# Backup entire archive
archivist backup ~/Backups/archivist-backup.zip

# Generate static site
archivist generate-site --output ~/Sites/archive
```

### Sharing

```bash
# Generate shareable link
archivist share arch_abc123

# Share with expiration
archivist share arch_abc123 --expires 7d

# Share collection by tag
archivist share-collection --tag python-resources

# Generate QR code for mobile sharing
archivist share arch_abc123 --qr
```

## Telegram Integration

Once connected, you can save from anywhere:

**You:** *[forwards article link]*

**Paw:** Want me to archive this?

**URL:** https://example.com/great-article
**Title:** "How to Build Better APIs"

React with 📚 to save, or reply with tags.

---

**You:** 📚 api-design must-read

**Paw:** ✅ Archived with tags: #api-design #must-read

Searchable via `/archive search api design` 🐾

---

**Search from Telegram:**

**You:** `/archive search python async`

**Paw:** Found **7 results**. Top 3:

1. Async Python Patterns (Jan 5)
2. Python asyncio guide (Dec 18)
3. FastAPI async examples (Jan 12)

Reply with a number to view, or `/archive search python async --all` for full list.

## Smart Features

### Auto-tagging

Archivist analyzes content and suggests tags:

```bash
# Enable auto-tagging
archivist config set auto-tag true

# Set confidence threshold (0.0-1.0)
archivist config set auto-tag-confidence 0.7

# Review auto-tag suggestions
archivist review-suggestions
```

### Summaries

AI-generated summaries for every saved item:

```bash
# Generate summary for existing item
archivist summarize arch_abc123

# Auto-summarize on save
archivist config set auto-summarize true

# Adjust summary length
archivist config set summary-length "brief" # brief, medium, detailed
```

### Related Content

Find connections between archived items:

```bash
# Show related items
archivist related arch_abc123

# Build knowledge graph
archivist graph --tag programming

# Find connections
archivist connect "api design" "authentication"
```

## Configuration

```bash
# Show config
archivist config show

# Storage location
archivist config set storage-path ~/Documents/Archive

# Database location
archivist config set db-path ~/.archivist/archive.db

# Screenshot quality
archivist config set screenshot-quality high # low, medium, high

# Full-text extraction
archivist config set extract-text true

# Offline mode (save full HTML)
archivist config set offline-mode true

# Auto-summarize
archivist config set auto-summarize true

# Language for voice transcription
archivist config set transcription-language en
```

## Storage & Performance

**Disk usage:**
- Articles: ~500KB each (HTML + screenshot)
- Code snippets: ~10KB each
- Files: original size preserved
- Voice notes: audio + text (~1MB each)

**Database:**
- SQLite (lightweight, portable)
- Full-text search via FTS5
- Typical size: ~50MB for 1000 items

**Performance:**
- Search: <100ms for 10,000 items
- Save URL: ~2-5 seconds (fetch + process)
- Voice transcription: ~3-10 seconds

## Tips from Paw

> "Tag as you go. It's way easier than bulk-tagging 500 items later. Trust me."

> "Voice notes are underrated. Capture ideas immediately, let me transcribe and tag them overnight."

> "The AI summaries are legit. Enable auto-summarize and you'll actually remember why you saved things."

> "Use the Telegram integration. Forward links directly from any app. Zero friction = more saving = better knowledge base."

> "Run `archivist health-check` monthly. Broken links pile up fast."

## Pricing

- **Free tier:** 100 items, basic search, manual tagging
- **Pro:** $8/month — unlimited items, AI tagging/summaries, voice transcription, advanced search
- **Team:** $25/month — shared archives, collaboration features, API access

Install from PawHub or [pawhub.ai/archivist](https://pawhub.ai/archivist)

## Privacy

- All data stored locally on your OpenPaw gateway
- Optional cloud sync (encrypted end-to-end)
- AI summaries use Claude API (opt-in, content is ephemeral)
- Voice transcription via Whisper API (opt-in, audio not stored by provider)
- No analytics, tracking, or third-party data sharing
- Export your entire archive anytime (open formats: JSON, Markdown, HTML)

## Notes

- Archive database is SQLite (fully portable)
- Full-text search works offline
- Screenshots use headless Chrome (requires Chromium installed)
- Voice transcription requires OpenAI API key or local Whisper model
- Supports all major file types (PDF, images, videos, code, documents)
- Archive is yours forever — no vendor lock-in

---

Built for people who read things, save them, then never find them again. Not anymore. 📁🐾
