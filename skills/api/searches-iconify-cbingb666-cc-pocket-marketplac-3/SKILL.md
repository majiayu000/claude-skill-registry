---
name: searches iconify
description: Searches Iconify API for icons by query. Use when users need to find, search, or discover icons from Iconify collections.
user-invocable: true
---

# Iconify Icon Search

## Task Progress

```text
- [ ] Generate keywords
- [ ] Execute parallel searches (all in same response)
- [ ] Aggregate results into template
```

## Phase 1: Generate Keywords

From `{{ARGUMENTS}}`, create 3-5 keyword variations:

- Synonyms (settings → gear/cog/config)
- Split compounds (user-circle → user/circle/avatar)
- Add style suffixes (-line/-solid/-outline)

## Phase 2: Parallel Search Execution

**CRITICAL: Execute ALL curl commands in parallel. Send them all in ONE response.**

```bash
curl -s "https://api.iconify.design/search?query=keyword1&limit=20"
curl -s "https://api.iconify.design/search?query=keyword2&limit=20"
curl -s "https://api.iconify.design/search?query=keyword3&limit=20"
```

Do NOT proceed to Phase 3 until all searches complete.

## Phase 3: Aggregate and Format

**Your COMPLETE output must be ONLY this template:**

```markdown
## Search Keywords

[keyword1, keyword2, keyword3]

## Search Results

### "keyword1" (found X icons)

| Icon Name | Collection | Preview |
|-----------|------------|---------|
| icon-name | collection | ![](https://api.iconify.design/collection:icon-name.svg) |

### "keyword2" (found X icons)

| Icon Name | Collection | Preview |
|-----------|------------|---------|
| icon-name | collection | ![](https://api.iconify.design/collection:icon-name.svg) |

## Recommendations

1. **collection:icon-name** - `<iconify-icon icon="collection:icon-name" />` ![](https://api.iconify.design/collection:icon-name.svg)
2. **collection:icon-name** - `<iconify-icon icon="collection:icon-name" />` ![](https://api.iconify.design/collection:icon-name.svg)
```

**Processing rules:**

- Deduplicate across all search results
- Sort by occurrence frequency
- Mark empty as "No icons found"
- NO text outside template
