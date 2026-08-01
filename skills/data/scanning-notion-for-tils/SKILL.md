---
name: scanning-notion-for-tils
description: '[UNDER DEVELOPMENT - DO NOT USE] Searches the Notion Writing database
  for unpublished items that could become TIL posts. This skill is not yet integrated
  with the publishing workflow.'
---

---
name: scanning-notion-for-tils
description: [UNDER DEVELOPMENT - DO NOT USE] Searches the Notion Writing database for unpublished items that could become TIL posts. This skill is not yet integrated with the publishing workflow.
---

# Scan Notion for TILs Skill

**Status: Under Development** - This skill is not ready for use. Focus on git-only workflow for now.

Finds unpublished Writing items that could become TIL blog posts.

## Writing Database

- Database ID: `eb0cbc7a-4fe4-4954-99bd-94c1bf861469`
- Data Source ID: `c296db5b-d2f1-44d4-abc6-f9a05736b143`

## Usage

### Step 1: Search for blog-destined items

Use `mcp__notion__notion-search` to find Writing items:

```
Search the Writing database for items with:
- Destination includes "blog"
- Status NOT in [Published, Paused, Archived, Migrated to content repo]
```

### Step 2: Filter out already-assessed items

Skip items that have a Writing relation pointing to a page with Status = "Claude Draft".

This means the item already has a TIL draft created for it.

### Step 3: Fetch candidate items

For each remaining item, use `mcp__notion__notion-fetch` to get:
- Full title and description
- Status and Type
- Related Research, Questions, and Topics
- Last edited date
- Page content (to assess depth)
- Writing relations (to check for Claude Draft links)

### Step 4: Score and categorize

**Ready to draft** (have enough content):
- Type = "how-to" (highest priority)
- Have linked Research or Questions (indicates depth)
- Have substantial content already
- Short/focused topics (TIL-appropriate)

**Need development help** (good topic, needs work):
- Title only or minimal content
- No Research or Questions linked yet
- Topic is clear but needs exploration

Both categories are valid suggestions - offer to draft TILs for ready items, offer to help develop items that need work.

### Step 5: Format output

Present suggestions in this format:

```
📝 TIL Opportunities from Notion Backlog:

🟢 READY TO DRAFT:

1. **"Make TS understand Array.filter by using type predicates"**
   - Status: Drafting | Type: how-to
   - Last edited: 2 months ago
   - Has: 2 Research links, 1 Question
   - Content: ~200 words already written
   - TIL angle: Type predicates let TS narrow filtered arrays
   - URL: https://www.notion.so/...

🟡 NEED DEVELOPMENT:

2. **"How to filter a JS array with async/await"**
   - Status: New | Type: how-to
   - Last edited: 1 year ago
   - Has: 1 Research link
   - Content: Title only
   - Suggestion: Research async filtering patterns, find good examples
   - URL: https://www.notion.so/...

Select a number to:
- Draft a TIL (for ready items)
- Help develop the topic (for items needing work)
```

## What to Look For

Good TIL candidates from Notion:

1. **How-to items** - Already tagged as instructional content
2. **Items with Research links** - Have supporting material to draw from
3. **Items with Questions** - Answered a real question worth sharing
4. **Recently edited** - Topic is fresh, easier to write about
5. **Partially drafted** - Already has content to build on

## TIL Angle Generation

Based on the item's content, suggest a TIL angle:

- **For code patterns**: "How to [do X] using [technique]"
- **For gotchas**: "Why [X] doesn't work and what to do instead"
- **For configuration**: "Setting up [tool] for [use case]"
- **For debugging**: "How to diagnose [problem]"

## Linking Drafts Back

**IMPORTANT: Never edit existing Writing items. Always create new pages in the Writing database.**

When working with a Notion item (drafting or developing):
1. Create a NEW page in the Writing database with Status = "Claude Draft"
2. Put all content/improvements in the new Writing page
3. Link the new draft TO the source item via Writing relation
4. This marks the source as "assessed" for future scans

The original item stays untouched - it's a reference, not something to modify. All Claude's work goes into new Writing database pages.

## Notes

- Only scans items with Destination = "blog"
- Skips items with Status in Published, Paused, Archived, Migrated
- Skips items that already have a Claude Draft linked via Writing relation
- Items needing development get help, not skipped
- TIL angles are suggestions based on title/content - refine as needed
- User may want to consolidate multiple related items into one TIL
