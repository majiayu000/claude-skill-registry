---
name: content-hub
description: Browser-based asset gallery for managing marketing assets. Visual grid with filter/search, brand context sidebar, and actions (preview, edit, generate). R2-ready manifest for future cloud sync. Use when browsing assets, managing content library, or generating new assets with brand context.
license: MIT
allowed-tools:
  - Bash
  - Read
---

# Content Hub

Visual asset gallery for ClaudeKit Marketing.

## Quick Start

```bash
# Open gallery
node .claude/skills/content-hub/scripts/server.cjs --open

# Rescan assets
node .claude/skills/content-hub/scripts/server.cjs --scan

# Stop server
node .claude/skills/content-hub/scripts/server.cjs --stop
```

Or use command: `/write:hub`

## Features

- **Gallery Grid**: Thumbnails of assets/ folder
- **Filter/Search**: By type (banners, designs, etc.) and keywords
- **Brand Sidebar**: Displays user's colors and voice from docs/brand-guidelines.md
- **Actions**: Preview, Edit in Claude, Copy path, Generate new
- **R2 Ready**: Manifest schema supports Cloudflare R2 sync (UI disabled)

## API Routes

| Route | Purpose |
|-------|---------|
| `/hub` | Gallery HTML |
| `/api/assets` | Asset list JSON |
| `/api/brand` | Brand context JSON |
| `/api/scan` | Trigger rescan |
| `/file/*` | Serve local files |

## Manifest Schema

Assets stored in `.assets/manifest.json` with R2 fields:

```json
{
  "id": "abc123",
  "path": "banners/hero.png",
  "category": "banner",
  "r2": {
    "status": "local",  // local|pending|synced|error
    "bucket": null,
    "url": null
  }
}
```

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/server.cjs` | HTTP server entry |
| `scripts/lib/scanner.cjs` | Scan assets directory |
| `scripts/lib/router.cjs` | HTTP routing |
| `scripts/lib/brand-context.cjs` | Extract brand guidelines |

## Integration

**Command**: `/write:hub`

**Related Skills**: brand-guidelines, ai-multimodal, design

**Agents**: content-creator, ui-ux-designer
