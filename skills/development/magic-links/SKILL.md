# Magic Links System

This project uses a build-time magic link system (adapted from surfdeeper) for semantic document linking.

## Syntax

### Standard Magic Links
```markdown
[Display Text](:document-id)
[Display Text](:document-id|:fallback-id)
```

Example:
```markdown
[Read about context collapse](:context-collapse)
```

### Learning Links (optional variant)
```markdown
[[document-id]]
[[document-id|Custom Display Text]]
```

These render as auto-numbered references.

## How It Works

1. Author writes `[text](:id)` in any markdown file
2. At build time, the Remark plugin scans all content collections
3. Builds a map of `id` → `slug` from frontmatter
4. Rewrites `:id` references to actual routes like `/concept/{slug}`

## Document Frontmatter

Each content file needs an `id` in frontmatter:

```yaml
---
title: Context Collapse
id: context-collapse           # Used for magic link resolution
aliases: [context-loss]        # Optional alternative IDs
---
```

## Collections

Magic links resolve across these collections:
- `concepts` → `/concept/{slug}`
- `failure-modes` → `/failure-mode/{slug}`
- `patterns` → `/pattern/{slug}`

## Implementation Files

If implementing this system, you need:

1. **Remark plugin** (`scripts/remark-magic-links.mjs`):
   - `buildIdMap()` - scans content directories, extracts id/slug/aliases
   - Plugin function - transforms `:id` links to actual URLs

2. **Astro config** (`astro.config.mjs`):
   ```javascript
   import remarkMagicLinks from "./scripts/remark-magic-links.mjs";

   export default defineConfig({
     markdown: {
       remarkPlugins: [remarkMagicLinks],
     },
   });
   ```

3. **Validation script** (`scripts/validate-concept-ids.js`):
   - Checks for duplicate IDs
   - Validates all magic link references resolve
   - Run with `npm run lint:links`

## When Adding New Content

1. Always include a unique `id` in frontmatter
2. Use kebab-case for IDs: `context-collapse`, not `contextCollapse`
3. Add `aliases` array if the concept has common alternative names
4. Run link validation before committing

## Error Handling

- Unresolved magic links are converted to plain text (no broken links)
- Build-time validation catches broken references
- Duplicate IDs cause validation failure
