---
name: aminet-browser
description: "Aminet search and browse: full-text search, category tree navigation, architecture filtering, package detail, and curated collections. Use when searching, browsing, or managing package collections."
metadata:
  extensions:
    gsd-skill-creator:
      triggers:
        intents:
          - "aminet.*search"
          - "aminet.*browse"
          - "aminet.*collection"
          - "package.*detail"
        files:
          - "src/aminet/search.ts"
          - "src/aminet/category-browser.ts"
          - "src/aminet/package-detail.ts"
          - "src/aminet/collection.ts"
          - "src/aminet/collection-manager.ts"
        contexts:
          - "aminet search"
          - "package browsing"
          - "aminet collections"
        threshold: 0.7
      token_budget: "1.0%"
      version: 1
      enabled: true
      plan_origin: "242-aminet-integration"
      phase_origin: "242"
---

# Aminet Browser

## Purpose

Provides search, browse, and collection management for the Aminet package archive. Supports full-text search with relevance scoring, hierarchical category tree navigation, architecture and OS version filtering, unified package detail views combining INDEX + readme + mirror state, and curated YAML-based collections with CRUD operations.

## Capabilities

- Full-text search with case-insensitive substring matching
- Relevance scoring: name=3x, description=2x, author=1x weighting
- Hierarchical category tree construction from INDEX entries
- Architecture filtering (m68k-amigaos, ppc-amigaos, etc.)
- OS version filtering for compatibility checks
- Unified package detail merging INDEX + readme + mirror state
- Collection manifest with Zod-validated YAML schema
- Import/export collections as YAML files
- 5 starter collections bundled
- Collection manager with DI-first pattern (collectionsDir param)
- Atomic write-then-rename for collection persistence
- Slugified filenames for cross-platform safety
- getCollectionPaths for bulk download integration

## Key Modules

| Module | Purpose |
|--------|---------|
| `src/aminet/search.ts` | Full-text search with relevance scoring (name=3, desc=2, author=1) |
| `src/aminet/category-browser.ts` | Category tree construction, architecture and OS version filtering |
| `src/aminet/package-detail.ts` | Unified package detail merging INDEX + readme + mirror state |
| `src/aminet/collection.ts` | Collection manifest Zod schema, YAML import/export, starter collections |
| `src/aminet/collection-manager.ts` | CRUD operations with atomic persistence, slugified filenames |

## Usage Examples

**Search packages:**
```typescript
import { searchPackages } from './search.js';

const results = searchPackages(indexEntries, 'deluxe paint');
// Sorted by relevance score, name matches weighted 3x
```

**Browse by category:**
```typescript
import { buildCategoryTree, listPackages } from './category-browser.js';

const tree = buildCategoryTree(indexEntries);
const gfxPackages = listPackages(indexEntries, 'gfx/edit');
```

**Get package detail:**
```typescript
import { buildPackageDetail } from './package-detail.js';

const detail = buildPackageDetail(indexEntry, readmeData, mirrorState);
// Unified view with all metadata sources
```

**Manage collections:**
```typescript
import { CollectionManager } from './collection-manager.js';

const mgr = new CollectionManager({ collectionsDir: './collections' });
await mgr.create({ name: 'My Games', packages: ['game/misc/Lemmings.lha'] });
const paths = mgr.getCollectionPaths('my-games');
```

## Dependencies

- Aminet INDEX data (from aminet-index skill)
- Node.js `node:fs` for collection persistence
- Zod for schema validation
- js-yaml for YAML serialization

## Token Budget Rationale

1.0% budget reflects the 5 modules covering search, browse, detail, and collection management. The search scoring algorithm and collection YAML round-trip are well-contained and require moderate context for correct usage.
