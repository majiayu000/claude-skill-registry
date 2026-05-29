---
name: aminet-mirror
description: "Selective Aminet package mirroring: single-package fetch, integrity verification, mirror state tracking, bulk download, and sync detection. Use when downloading, verifying, or managing mirrored packages."
metadata:
  extensions:
    gsd-skill-creator:
      triggers:
        intents:
          - "aminet.*fetch"
          - "aminet.*download"
          - "mirror.*state"
          - "integrity.*verif"
        files:
          - "src/aminet/package-fetcher.ts"
          - "src/aminet/mirror-state.ts"
          - "src/aminet/integrity.ts"
          - "src/aminet/bulk-downloader.ts"
          - "src/aminet/sync-detector.ts"
        contexts:
          - "aminet mirroring"
          - "package download"
        threshold: 0.7
      token_budget: "1.0%"
      version: 1
      enabled: true
      plan_origin: "242-aminet-integration"
      phase_origin: "242"
---

# Aminet Mirror

## Purpose

Manages selective mirroring of Aminet packages to the local filesystem. Handles single-package fetching with ordered mirror fallback, SHA-256 integrity verification, persistent mirror state tracking with 7-state status enum, concurrent bulk downloads with rate limiting, and sync detection comparing local state against the INDEX.

## Capabilities

- Single-package fetch with ordered mirror fallback
- Directory hierarchy preservation matching Aminet structure
- Non-fatal .readme download (best-effort alongside archive)
- User-Agent header on all HTTP requests
- SHA-256 integrity verification via node:crypto
- Size verification with +/-1 KB tolerance for Aminet metadata rounding
- Combined integrity result (hash + size) in single check
- 7-state PackageStatus enum tracking full lifecycle
- Atomic write-then-rename for mirror state persistence
- Immutable updateEntry pattern for safe concurrent access
- Bulk download with async semaphore concurrency control
- Global rate limiting gate between requests
- Resume from interruption (skips already-mirrored packages)
- Serialized state writes via Promise chain mutex
- Sync detection comparing mirror state vs INDEX by sizeKb
- O(1) Map lookup for efficient change detection
- Only change-eligible statuses compared (mirrored+)

## Key Modules

| Module | Purpose |
|--------|---------|
| `src/aminet/package-fetcher.ts` | Single-package fetch with ordered mirror fallback and .readme |
| `src/aminet/mirror-state.ts` | 7-state status enum, atomic persistence, immutable updateEntry |
| `src/aminet/integrity.ts` | SHA-256 hash and size verification with combined IntegrityResult |
| `src/aminet/bulk-downloader.ts` | Concurrent downloads with semaphore, rate limiting, resume support |
| `src/aminet/sync-detector.ts` | Detects INDEX changes against local mirror state via Map lookup |

## Usage Examples

**Fetch a single package:**
```typescript
import { fetchPackage } from './package-fetcher.js';

const result = await fetchPackage({
  entry: indexEntry,
  mirrors: ['https://aminet.net', 'https://de.aminet.net'],
  outputDir: './mirror',
});
// Downloads archive + .readme, preserves directory structure
```

**Verify integrity:**
```typescript
import { verifyIntegrity } from './integrity.js';

const result = await verifyIntegrity(filePath, { expectedSha256: hash, expectedSizeKb: 42 });
// result.valid, result.hashMatch, result.sizeMatch
```

**Bulk download with concurrency:**
```typescript
import { bulkDownload } from './bulk-downloader.js';

await bulkDownload({
  entries: selectedPackages,
  mirrors,
  outputDir: './mirror',
  concurrency: 4,
  rateLimit: 500, // ms between requests
  onProgress: (completed, total) => console.log(`${completed}/${total}`),
});
```

**Detect sync changes:**
```typescript
import { detectChanges } from './sync-detector.js';

const changes = detectChanges(mirrorState, currentIndex);
// changes: { added: [], updated: [], removed: [] }
```

## Dependencies

- Node.js `node:crypto` for SHA-256 hashing
- Node.js `node:fs` for mirror state persistence and file I/O
- HTTP client for mirror downloads
- Aminet mirror network (ordered fallback list)

## Token Budget Rationale

1.0% budget reflects the 5 modules covering fetch, state, integrity, bulk download, and sync detection. The concurrency control, rate limiting, and atomic state persistence patterns require moderate context for safe operation.
