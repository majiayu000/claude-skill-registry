---
name: content-portability
description: Export WordPress pages, posts, and custom posts to portable local packages with builder data, media, and human-readable markdown. Import to another site with smart ID remapping. Auto-backup before AI edits. Use when user says "export my site", "backup my pages", "migrate content", "download my content", or "content portability".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# Content Portability

Export WordPress content to portable local packages. Import to another site with smart ID remapping. Auto-backup before AI edits. Full builder data preservation, human-readable markdown previews, and optional media download.

## What This Skill Does

**Exports:**
- Pages, posts, and custom post types — individually or in bulk
- Full builder data (Elementor, Bricks, Divi, etc.) alongside standard content
- Allowlisted post meta (SEO fields, featured images, builder config)
- Human-readable markdown preview of every page/post
- Optional media binary download for fully offline packages
- Manifest with hashes, stats, and export metadata

**Imports:**
- Reads a local Respira Content Package and pushes to a target WordPress site
- Smart ID remapping — media IDs, post IDs, and internal links rewritten for the target site
- Bulk conflict resolution — detects slug collisions upfront, one decision for all
- Mandatory server-side snapshots before any overwrites (safety net)
- Builder JSON rewriting with full ID mapping tables
- Fidelity verification — re-reads imported content and compares hashes

**Auto-Backup:**
- Quick-backup mode before any AI edit — saves a local snapshot to `./respira-backups/`
- Timestamped, human-readable, zero-friction insurance

## Requirements

- Respira for WordPress plugin installed and activated
- MCP connection configured (site URL + API key)
- For import: write access on the target site
- For media download: sufficient local disk space

## How to Use

### Trigger Phrases
- "export my site"
- "export the homepage"
- "backup my pages before editing"
- "download my content locally"
- "migrate content to my other site"
- "content portability"
- "create a local backup"
- "export with media"

### Export Workflow

**Phase 1: Scope Selection**
1. Ask the user what to export:
   - **Single page/post**: "export the homepage", "backup the about page"
   - **Full site**: "export everything", "download all my content"
   - **By type**: "export all blog posts", "export portfolio items"
2. Ask whether to include media downloads:
   - **Without media** (default): Fast, small packages with URL references
   - **With media**: Downloads all referenced images/files locally for full offline portability

**Phase 2: Content Enumeration**
3. Call `wordpress_list_pages`, `wordpress_list_posts`, and/or `wordpress_list_custom_posts` to enumerate content in scope
4. For each item, call `wordpress_read_page` or `wordpress_read_post` with `include=builder.extracted,meta.allowlisted` to get full content with builder data
5. Report progress every 10 items: "Exported 30/120 pages..."

**Phase 3: Write Local Package**
6. Create the export directory structure:

```
respira-export/
├── manifest.json              # Package metadata, source site, export date, hashes
├── README.md                  # One-line import prompt for zero-friction migration
├── pages/
│   ├── home/
│   │   ├── content.json       # Full machine-readable export
│   │   └── content.md         # Human-readable markdown preview
│   ├── about/
│   │   ├── content.json
│   │   └── content.md
│   └── ...
├── posts/
│   ├── 2024-hello-world/
│   │   ├── content.json
│   │   └── content.md
│   └── ...
├── cpt/                       # Custom post types
│   └── {post_type}/
│       └── {slug}/
│           ├── content.json
│           └── content.md
└── media/                     # Only if --with-media
    ├── media-index.json       # URL→local-path mapping with old media IDs
    └── uploads/
        ├── hero-image.webp
        └── ...
```

7. For each page/post, write two files:

**content.json** — machine-readable, contains:
```json
{
  "export_version": "1.0",
  "source_site": "https://example.com",
  "exported_at": "2026-03-16T14:30:00Z",
  "post": {
    "id": 42,
    "post_type": "page",
    "title": "About Us",
    "slug": "about",
    "status": "publish",
    "content": "<full HTML content>",
    "excerpt": "...",
    "modified": "2026-03-10T09:00:00Z"
  },
  "builder": {
    "name": "bricks",
    "payload": {},
    "extracted": {}
  },
  "meta": {
    "_thumbnail_id": 108,
    "_yoast_wpseo_title": "About Us | Example"
  },
  "hashes": {
    "content_hash": "sha256:abc123...",
    "builder_hash": "sha256:def456...",
    "meta_hash": "sha256:ghi789..."
  }
}
```

**content.md** — human-readable markdown preview:
```markdown
# About Us

**Source:** https://example.com/about/
**Type:** page | **Status:** publish | **Builder:** Bricks
**Exported:** 2026-03-16

---

[Rendered text content extracted from HTML, preserving headings and structure]

## Section: Hero
- Heading: "Welcome to Our Company"
- Text: "We've been helping businesses..."
- Image: hero-team-photo.webp (Media ID: 108)

## Section: Team
- Heading: "Meet the Team"
...
```

8. If media download is enabled:
   - Call `wordpress_list_media` to get all media items
   - Filter to only media referenced by exported content
   - Download each file and save to `media/uploads/`
   - Write `media/media-index.json` mapping old URLs and IDs to local paths

**Phase 4: Manifest & Stats**
9. Write `manifest.json`:
```json
{
  "export_version": "1.0",
  "source_site": "https://example.com",
  "source_wordpress_version": "6.7.1",
  "source_respira_version": "4.3.1",
  "exported_at": "2026-03-16T14:30:00Z",
  "scope": "full_site",
  "content": {
    "pages": 23,
    "posts": 8,
    "custom_post_types": { "portfolio": 12, "testimonial": 5 }
  },
  "media": {
    "included": true,
    "files": 156,
    "total_bytes": 52428800
  },
  "warnings": [],
  "skipped": [],
  "hashes": {
    "manifest_hash": "sha256:..."
  }
}
```

10. Write `README.md`:
```markdown
# Respira Content Package

Exported from: https://example.com
Date: 2026-03-16
Contents: 23 pages, 8 posts, 17 custom posts, 156 media files

## To import this content to another site

Tell your AI agent:
> Import the content package from ./respira-export/

## Package format
- content.json files contain full machine-readable content with builder data
- content.md files are human-readable previews
- media/ contains downloaded media files (if included)
```

11. Show export stats summary:
```
Export Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━
Pages exported:     23
Posts exported:      8
Custom posts:       17
Media files:       156
Package size:     52.4 MB
Warnings:           0
Skipped:            0
━━━━━━━━━━━━━━━━━━━━━━━━━━
Saved to: ./respira-export/
```

### Import Workflow

**Phase 1: Read & Validate Package**
1. Read `manifest.json` from the local package
2. Validate export version compatibility
3. Report what will be imported: "Found 23 pages, 8 posts, 156 media files from example.com"

**Phase 2: Upload Media (if included)**
4. If `media/` directory exists with files:
   - For each media file, call `wordpress_upload_media` on the target site
   - Build the **media ID mapping table**: `{ old_id: 108, new_id: 342 }`
   - Log each upload; skip failures with warning
5. If media was not included in the package:
   - Media references will point to original URLs (cross-site references)
   - Warn the user about this

**Phase 3: Detect Conflicts**
6. For each content item in the package, check if a page/post with the same slug already exists on the target site
7. Present all conflicts upfront in a single table:
```
Slug Conflicts Detected (5 of 23 pages)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Slug          Source Title       Target Title
about         About Us           About Our Company
contact       Contact            Contact Us
team          Our Team           The Team
services      Services           Our Services
faq           FAQ                FAQ
```
8. Ask the user for a bulk resolution strategy:
   - **Overwrite all**: Replace target content with package content
   - **Skip conflicts**: Only import non-conflicting content
   - **Rename imports**: Add suffix to conflicting slugs (e.g., `about-imported`)

**Phase 4: Snapshot Existing Content**
9. **MANDATORY**: Before overwriting any existing content, take a server-side snapshot of each target page/post using the existing snapshot system
   - This uses the `before_edit` snapshot kind automatically via MCP write operations
   - Ensures rollback is always possible

**Phase 5: Create/Update Content**
10. For each content item:
    - If no conflict or overwrite strategy: call `wordpress_update_page` or `wordpress_update_post`
    - Set title, content, excerpt, status, and allowlisted meta
    - Build the **post ID mapping table**: `{ old_id: 42, new_id: 187 }`
11. Report progress every 10 items

**Phase 6: Rewrite & Inject Builder Data**
12. For each imported page/post that has builder data:
    - Take the builder JSON from `content.json`
    - Rewrite all media IDs using the media ID mapping table
    - Rewrite all internal post/page IDs using the post ID mapping table
    - Rewrite all internal URLs from source domain to target domain
    - Call `wordpress_inject_builder_content` to apply the rewritten builder data

**Phase 7: Verify & Report**
13. For each imported page/post:
    - Re-read via `wordpress_read_page`/`wordpress_read_post`
    - Compare content hashes to source hashes
    - Flag any mismatches
14. Show import report:
```
Import Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pages imported:     23  (5 overwrites, 18 new)
Posts imported:      8  (0 overwrites, 8 new)
Media uploaded:    156  (2 skipped — too large)
Builder data:       19  pages with builder content rewritten
ID remappings:     187  references updated
Hash verification: 46/48 match (2 minor diffs flagged)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Server-side snapshots taken for all overwrites.
```

### Auto-Backup Workflow

A lightweight mode for quick local backups before AI editing:

1. User says "backup the homepage before editing" or "save a local copy first"
2. Call `wordpress_read_page` with full includes
3. Write a single timestamped file: `./respira-backups/home-2026-03-16-1430.json`
4. Also write the markdown preview: `./respira-backups/home-2026-03-16-1430.md`
5. Confirm: "Backed up homepage to ./respira-backups/home-2026-03-16-1430.json"
6. Proceed with the requested edit

### Diff Workflow

Compare local export against current site state:

1. User says "what changed since my last export?" or "diff my backup"
2. Read the local `manifest.json` to identify exported content
3. For each exported page/post, call `wordpress_read_page`/`wordpress_read_post`
4. Compare content hashes from local `content.json` against current site hashes
5. Report differences:
```
Content Changes Since Export (2026-03-16)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Changed:
  about         Content updated (builder + text)
  homepage      Builder layout changed
  pricing       Text content changed

Unchanged:    21 pages, 8 posts
New on site:   2 pages (not in export)
Deleted:       0 pages
```

## Error Handling

The skill must handle these scenarios gracefully:

| Error | Action | User Sees |
|-------|--------|-----------|
| Site disconnected | Stop, report what was saved | "Site unreachable — 45/120 pages saved" |
| Page not found mid-export | Skip, log in manifest warnings | "Skipped: About (deleted)" |
| Malformed builder data | Export raw content without builder | Warning in manifest |
| Disk full | Stop, report progress | "Disk full after 45 pages" |
| Media download 404/403 | Skip file, log in media-index | "Skipped 3 media files" |
| Slug conflict on import | Bulk resolution (see Phase 3) | Conflict table |
| Media upload too large | Skip, log | "Skipped: hero.webp (too large)" |
| Builder version mismatch | Warn, import anyway | Warning in report |

**Key rule**: Always continue on non-fatal errors (skip the item, log it). Never silently drop content. Always produce a summary of warnings/skips at the end.

## Safety Model

- **Read-only export**: No changes to the source site during export
- **Mandatory snapshots**: Server-side snapshot taken before every import overwrite
- **Non-destructive import**: Creates new content or overwrites with snapshot safety net
- **Rollback ready**: Server-side snapshots enable one-click restoration via `wordpress_restore_snapshot`
- **No credential exposure**: Only allowlisted meta is exported — no API keys, passwords, or sensitive plugin settings

## Honest Disclaimer

**What this skill CANNOT do:**
- Export/import WordPress settings, options, or configuration
- Export/import user accounts or roles
- Export/import plugin or theme files
- Handle taxonomy/term migration (categories, tags) — future enhancement
- Guarantee pixel-perfect builder rendering across different builder versions
- Process sites with more than ~500 pages in a single session (token/context limits)

**What this skill CAN do:**
- Create complete local backups of pages, posts, and custom post types
- Preserve full builder data (Elementor, Bricks, Divi) across migrations
- Download media for fully offline packages
- Generate human-readable markdown previews of all content
- Migrate content between sites with smart ID remapping
- Auto-backup before AI edits for peace of mind
- Compare local backups against current site state

## Respira MCP Tools Used

- `wordpress_list_pages` / `wordpress_list_posts` / `wordpress_list_custom_posts` — enumerate content
- `wordpress_read_page` / `wordpress_read_post` / `wordpress_get_custom_post` — read full content with builder data
- `wordpress_list_media` / `wordpress_get_media` — media enumeration and metadata
- `wordpress_upload_media` — upload media during import
- `wordpress_update_page` / `wordpress_update_post` / `wordpress_update_custom_post` — create/update content during import
- `wordpress_inject_builder_content` — apply rewritten builder data during import
- `wordpress_get_active_site` / `wordpress_get_site_context` — verify connection and site details
- `wordpress_list_snapshots` / `wordpress_restore_snapshot` — safety net for imports

## Related Skills

- Site Onboarding — first-run primer, discovers site capabilities
- WordPress Site DNA — deep site archaeology and health scoring
- Technical Debt Audit — find orphaned content and unused plugins before migration
- WordPress AI Image Optimizer — optimize images before or after migration

---

Built by Respira for WordPress
https://respira.press
