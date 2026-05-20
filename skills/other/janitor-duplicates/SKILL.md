---
name: janitor-duplicates
description: "Find duplicate skills that do the same thing"
metadata:
  version: 1.0.0
---

# Duplicate Detection

Find skills with overlapping functionality using keyword similarity analysis.

## How to Run

```bash
bash ~/.claude/skills/skills-janitor/scripts/detect_dupes.sh
```

## How It Works

1. Extracts trigger keywords from each skill's description field
2. Filters common stop words (~60 words)
3. Compares all skill pairs using Jaccard similarity
4. Flags pairs with >30% keyword overlap

## Output

```
[72%] marketing-copywriting <-> marketing-copy-editing
      Scopes: user, user
      Shared keywords: copy, editing, marketing, write

[45%] seo-audit <-> marketing-seo-audit
      Scopes: project, user
      Shared keywords: audit, seo, ranking
```

## After Finding Duplicates

- Review each pair - some overlap is intentional (e.g., copywriting vs copy-editing)
- Plugin skills should NOT be edited (changes get overwritten)
- For user-scope duplicates, suggest which to keep and why
- Ask for confirmation before any removal

## Related Skills

- For full skill inventory: `/janitor-audit`
- For auto-fixing issues: `/janitor-fix`
- For a health report: `/janitor-report`
