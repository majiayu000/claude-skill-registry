---
name: aminet-index
description: "Manages Aminet INDEX infrastructure: fetch, parse, cache, and incremental update of ~84,000-entry package database. Use when managing INDEX data, checking freshness, or parsing .readme files."
metadata:
  extensions:
    gsd-skill-creator:
      triggers:
        intents:
          - "aminet.*index"
          - "aminet.*update"
          - "index.*fetch"
          - "readme.*parse"
        files:
          - "src/aminet/index-fetcher.ts"
          - "src/aminet/index-parser.ts"
          - "src/aminet/index-freshness.ts"
          - "src/aminet/readme-parser.ts"
        contexts:
          - "aminet index management"
          - "package database"
        threshold: 0.7
      token_budget: "1.5%"
      version: 1
      enabled: true
      plan_origin: "242-aminet-integration"
      phase_origin: "242"
---

# Aminet Index

## Purpose

Manages the complete lifecycle of the Aminet INDEX database: fetching INDEX.gz from mirrors, parsing ~84,000 package entries into structured data, caching results for offline use, checking freshness against 24-hour thresholds, and performing incremental updates via RECENT file diffing. Also handles .readme metadata extraction for individual package detail views.

## Capabilities

- Fetch INDEX.gz from Aminet mirrors with gzip decompression
- Parse ~84,000 INDEX entries using token-based regex in ~114ms
- ISO-8859-1 decoding via TextDecoder for correct character handling
- JSON cache with INDEX + INDEX.meta.json sidecar for offline access
- K=1x and M=1000x size suffix normalization
- 24-hour freshness detection with configurable thresholds
- RECENT-based incremental merge by fullPath for efficient updates
- Parse .readme files extracting raw headers (lowercase keys, multi-value split on comma+semicolon)
- Barrel file exporting complete public API

## Key Modules

| Module | Purpose |
|--------|---------|
| `src/aminet/index-fetcher.ts` | Fetches INDEX.gz from Aminet mirrors with gzip decompression |
| `src/aminet/index-parser.ts` | Parses INDEX entries into structured PackageEntry objects |
| `src/aminet/readme-parser.ts` | Extracts metadata from .readme files with header parsing |
| `src/aminet/index-freshness.ts` | Checks INDEX age against 24h threshold, triggers RECENT-based incremental merge |

## Usage Examples

**Fetch and parse the INDEX:**
```typescript
import { fetchIndex } from './index-fetcher.js';
import { parseIndex } from './index-parser.js';

const raw = await fetchIndex({ mirrorUrl: 'https://aminet.net' });
const entries = parseIndex(raw);
// entries: PackageEntry[] with ~84,000 items
```

**Check freshness and update incrementally:**
```typescript
import { checkFreshness } from './index-freshness.js';

const result = await checkFreshness({ cacheDir: './cache', maxAgeMs: 86400000 });
if (!result.fresh) {
  // Fetch RECENT, merge new entries by fullPath
}
```

**Parse a .readme file:**
```typescript
import { parseReadme } from './readme-parser.js';

const metadata = parseReadme(readmeText);
// metadata.short, metadata.author, metadata.uploader, metadata.type, etc.
```

## Dependencies

- Node.js `node:zlib` for gzip decompression
- Node.js `node:fs` for cache persistence
- Aminet mirror network for INDEX.gz and RECENT files

## Token Budget Rationale

1.5% budget reflects the 4 modules covering INDEX fetch, parse, freshness, and readme extraction. The ~84,000-entry parsing logic with ISO-8859-1 handling, size suffix normalization, and incremental merge via RECENT requires comprehensive context for correct operation and troubleshooting.
