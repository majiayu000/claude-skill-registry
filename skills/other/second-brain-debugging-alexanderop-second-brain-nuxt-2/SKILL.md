---
name: debugging
description: Debug issues in the Second Brain Nuxt 4 + @nuxt/content v3 project. Use for any bug, test failure, or unexpected behavior.
---

# Second Brain Debugging

## Overview

This skill adapts systematic debugging for the Second Brain stack:
- **Nuxt 4** with Vue 3 Composition API
- **@nuxt/content v3** with SQLite and minimark format
- **@nuxt/ui v4** components
- **D3.js** for knowledge graph visualization

**Core principle:** ALWAYS trace data flow before attempting fixes.

## Stack-Specific Gotchas

Before debugging, internalize these common pitfalls:

| Issue | Symptom | Cause |
|-------|---------|-------|
| Empty graph edges | Nodes show, no connections | Missing `.select('body')` in query |
| Links not extracted | Backlinks/graph empty | Minimark parsed as object, not array |
| 404 on content page | Page not found | Slug mismatch (`/slug` vs `slug`) |
| Stale backlinks | Old connections shown | useAsyncData cache not invalidated |
| Silent API failure | Empty response, no error | try-catch returns `{}` or `[]` |
| Wrong mentions | Unrelated content matched | Title regex too broad |
| Graph crashes on filter | D3 error after filtering | Edge source/target type mismatch |

## The Four Phases

### Phase 1: Identify the Layer

**Data flows through these layers:**

```text
Content File (Markdown)
    ↓ Parsed by Nuxt Content
Minimark AST (body.value array)
    ↓ Queried via queryCollection
API Endpoint (server/api/*.ts)
    ↓ Returned as JSON
Vue Composable (useBacklinks, useMentions)
    ↓ Rendered in component
User Interface
```

**First question: Which layer is broken?**

1. **Content layer** - Check frontmatter, markdown syntax
2. **AST layer** - Check minimark structure: `[tag, props, ...children]`
3. **Query layer** - Check `.select('body')`, path matching
4. **API layer** - Check response structure, error handling
5. **Client layer** - Check composable logic, reactivity

**Quick diagnostic:**
```bash
# Check if content is queryable
pnpm nuxi dev
# Visit http://localhost:3000/api/graph
# Empty edges? → Layer 2-3 issue
# Empty nodes? → Layer 1 issue
# Correct data but UI wrong? → Layer 4-5 issue
```

### Phase 2: Trace Data Flow

**For content/link issues:**

1. **Check raw content file:**
   - Frontmatter has `title` and `type`?
   - Wiki-links use correct format `[[slug]]`?
   - File in `/content/` directory?

2. **Check minimark extraction:**
   ```typescript
   // In server/api/graph.get.ts, temporarily add:
   console.log('Body structure:', JSON.stringify(item.body, null, 2))
   // Verify: { type: 'minimark', value: [[...arrays...]] }
   // NOT: { type: 'minimark', value: [{...objects...}] }
   ```

3. **Check query selection:**
   ```typescript
   // Must explicitly select body:
   queryCollection(event, 'content')
     .select('path', 'stem', 'title', 'type', 'body') // ← body required!
     .all()
   ```

4. **Check API response:**
   ```bash
   curl http://localhost:3000/api/graph | jq '.edges | length'
   curl http://localhost:3000/api/backlinks | jq 'keys | length'
   ```

**For graph visualization issues:**

1. Check nodes exist before filtering
2. Check edge source/target types (string vs object after D3)
3. Check filter state in URL query params

### Phase 3: Hypothesis Testing

**Form ONE hypothesis:**
- "The body isn't being selected because..."
- "Links aren't extracted because minimark format is..."
- "The cache is stale because..."

**Test minimally:**
```bash
# Run relevant tests first
pnpm test:unit -- minimark  # For link extraction
pnpm test:run -- graph      # For API issues
```

**Add targeted logging:**
```typescript
// In extractLinksFromBody (server/utils/minimark.ts)
console.log('Body type:', body?.type)
console.log('Body value is array?', Array.isArray(body?.value))
console.log('First node:', JSON.stringify(body?.value?.[0]))
```

### Phase 4: Fix and Verify

1. **Create failing test first:**
   ```typescript
   // tests/unit/utils/minimark.test.ts
   it('extracts links from nested minimark', () => {
     const body = {
       type: 'minimark',
       value: [['a', { href: '/target' }, 'Link text']]
     }
     expect(extractLinksFromBody(body)).toContain('target')
   })
   ```

2. **Implement fix in ONE place**

3. **Verify with full test suite:**
   ```bash
   pnpm test:run
   pnpm lint:fix && pnpm typecheck
   ```

4. **If fix doesn't work after 3 attempts:**
   - Question the architecture
   - Is the data model fundamentally sound?
   - Should slug normalization be centralized?

## Quick Debugging Commands

```bash
# Run all tests
pnpm test:run

# Run specific test file
pnpm test:unit -- minimark
pnpm test:run -- graph.nuxt

# Type check
pnpm typecheck

# Start dev server for manual testing
pnpm dev

# Check API responses
curl -s http://localhost:3000/api/graph | jq '.nodes | length'
curl -s http://localhost:3000/api/graph | jq '.edges | length'
curl -s http://localhost:3000/api/backlinks | jq 'keys'
curl -s "http://localhost:3000/api/mentions?slug=test&title=Test" | jq
```

## Key Files by Subsystem

### Content Pipeline
- `/content/*.md` - Raw content files
- `/content.config.ts` - Collection schema (title, type required)
- `/modules/wikilinks.ts` - [[link]] to anchor transformation

### Link Extraction
- `/server/utils/minimark.ts` - Extract links from AST
- Body format: `{ type: 'minimark', value: [...arrays...] }`
- Link format: `['a', { href: '/slug' }, 'text']`

### API Endpoints
- `/server/api/graph.get.ts` - Nodes and edges for D3
- `/server/api/backlinks.get.ts` - Reverse link index
- `/server/api/mentions.get.ts` - Unlinked mentions search

### Client Composables
- `/app/composables/useBacklinks.ts` - Fetch backlinks
- `/app/composables/useMentions.ts` - Fetch mentions
- `/app/composables/useGraphFilters.ts` - Graph filter state

### Pages
- `/app/pages/[...slug].vue` - Content page
- `/app/pages/graph.vue` - Knowledge graph

## Common Fixes

### "Graph shows nodes but no edges"
```typescript
// Fix: Add .select('body') to query
queryCollection(event, 'content')
  .select('path', 'stem', 'title', 'type', 'tags', 'body') // ← ADD body
  .all()
```

### "Links not being extracted"
```typescript
// Check minimark format - must be ARRAY based
// Wrong: { tag: 'a', props: { href: '/' }, children: [] }
// Right: ['a', { href: '/' }, 'text']

// Fix extractLinksFromMinimark to handle arrays:
function extractLinksFromMinimark(node: unknown): string[] {
  if (!Array.isArray(node)) return []
  const [tag, props, ...children] = node
  // ...
}
```

### "Stale backlinks after content edit"
```typescript
// Force refresh with key
const { data: backlinks, refresh } = await useAsyncData(
  `backlinks-${Date.now()}`, // or add content hash
  () => $fetch('/api/backlinks')
)
```

### "Content page 404"
```typescript
// Check slug normalization
// Route uses: /atomic-habits (with slash)
// queryCollection expects path: '/atomic-habits' (with slash)
// Backlinks use slug: 'atomic-habits' (no slash)

// Ensure consistent normalization:
const slug = route.path.startsWith('/') ? route.path : `/${route.path}`
```

## Red Flags - STOP

If you catch yourself:
- Guessing which layer the bug is in
- Adding fixes to multiple files at once
- Skipping the test before fixing
- Not checking minimark format
- Assuming body is included by default

**STOP. Return to Phase 1.**
