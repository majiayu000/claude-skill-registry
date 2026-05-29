---
name: Searching AEM Documentation
description: Searches the aem.live documentation for information on AEM Edge Delivery Services features. Use this skill when you need more information about a feature, want guidance on how to implement a feature, and using existing tools you have to search the web isn't turning up relevant results.
---

# Searching AEM Documentation

## Overview

This skill helps you efficiently search the complete aem.live documentation (docs and blog posts) without wasting context on irrelevant pages. Use the provided search script to find relevant documentation pages, then use WebFetch to read the full content of the most relevant results.

## When to Use This Skill

Use this skill when:
- You need information about an aem.live feature or concept
- You've already looked at the project codebase for context
- You've tried a basic web search but didn't find relevant aem.live documentation
- You need technical guidance on implementing aem.live features
- You're looking for best practices or examples from the official docs

**Do NOT use this skill when:**
- You need reusable code snippets or block examples (use `block-collection-and-party` instead)
- You already know the specific documentation URL
- You're looking for general web development information (not aem.live specific)

## How to Use This Skill

### Step 1: Identify Keywords

Determine 1-3 specific keywords related to what you're searching for. Be specific rather than general.

**Good keywords:**
- "block decoration"
- "metadata"
- "universal editor"
- "sidekick plugin"

**Poor keywords:**
- "aem" (too generic, filtered as stop word)
- "how to build website" (too broad)
- "the" (stop word)

### Step 2: Run the Search Script

Execute the search script from the project root:

```bash
node .claude/skills/docs-search/scripts/search.js [--all] <keyword1> [keyword2] [...]
```

**Options:**
- `--all`: Return all matching results (default: limit to 10 most relevant)
- Without `--all`: Returns top 10 results

**Examples:**
```bash
# Search for block decoration info
node .claude/skills/docs-search/scripts/search.js block decoration

# Search for metadata with all results
node .claude/skills/docs-search/scripts/search.js --all metadata

# Multi-word search
node .claude/skills/docs-search/scripts/search.js universal editor blocks
```

### Step 3: Review Search Results

The script returns JSON with the following structure:

```json
[
  {
    "path": "/developer/markup-sections-blocks",
    "title": "Markup, Sections, Blocks, and Auto Blocking",
    "description": "To design websites and create functionality, developers use the markup and DOM...",
    "snippet": "Markup, Sections, Blocks, and Auto Blocking\n\nTo design websites...",
    "type": "doc",
    "deprecation": null,
    "relevanceScore": 141
  }
]
```

**Field Explanations:**
- `path`: URL path to the documentation page
- `title`: Page title
- `description`: Brief summary (usually ~150 chars) - **use this for quick context**
- `snippet`: Relevant excerpt from the page content showing keyword context
- `type`: "doc" or "blog"
- `deprecation`: Warning message if feature is deprecated (or null)
- `relevanceScore`: Relevance score (higher = more relevant)

**Important Notes:**
- Results are sorted by relevance (highest first)
- Deprecated pages have reduced relevance scores but still appear in results
- The `description` field provides the best quick summary of the page
- The `snippet` shows keyword context but may not be comprehensive

### Step 4: Use WebFetch for Full Content

The search results give you an overview. To get detailed information, use WebFetch to read the full page:

```
WebFetch: https://www.aem.live{path}
```

**Best Practice:** Start with the top 2-3 most relevant results, read them fully with WebFetch, then decide if you need more.

### Step 5: Alert User to Deprecations

If any results have a `deprecation` field with content, **inform the user** that the feature is deprecated and include the deprecation message. Suggest they look at higher-ranked (non-deprecated) alternatives.

## Search Behavior Details

### What Gets Searched

1. **Primary**: Full documentation (docpages-index.json) - 150+ pages with complete content
2. **Secondary**: Blog posts (query-index.json) - Only searched if < 5 doc results found

### Stop Words (Automatically Filtered)

These common words are ignored in searches:
- Articles: the, a, an
- Conjunctions: and, or, but
- Prepositions: in, on, at, to, for, of, with, by
- AEM-specific: aem, cms, edge, delivery, services

### Relevance Scoring

- **Title match**: 10 points per occurrence
- **Description match**: 5 points per occurrence
- **Content match**: 1 point per occurrence
- **Multi-keyword bonus**: 1.5x multiplier if multiple keywords match
- **Deprecation penalty**: 0.5x multiplier (score halved) for deprecated features

### Caching

Index files are cached locally for 24 hours in `.claude/skills/docs-search/.cache/`. This speeds up subsequent searches.

## Examples

### Example 1: Finding Block Documentation

**User Request:** "How do I decorate blocks in aem.live?"

**Good Approach:**
1. Search: `node .claude/skills/docs-search/scripts/search.js block decoration`
2. Review top 3 results
3. WebFetch the most relevant: `https://www.aem.live/developer/markup-sections-blocks`
4. Read full content and provide answer

**Poor Approach:**
- Using WebSearch instead (wastes time on irrelevant results)
- Not using the search script (might miss the best documentation page)

### Example 2: Learning About Metadata

**User Request:** "I need to add metadata to my pages"

**Good Approach:**
1. Search: `node .claude/skills/docs-search/scripts/search.js metadata`
2. Notice top result is "/docs/bulk-metadata" (score: 63)
3. Also see "/docs/metadata" (score: 30)
4. WebFetch both to understand page-level vs bulk metadata
5. Provide comprehensive answer with both approaches

**Poor Approach:**
- Only reading the first result and missing bulk metadata option
- Not using `--all` when you need comprehensive coverage

### Example 3: Deprecated Feature Warning

**User Request:** "How do I use folder mapping?"

**Search Results:**
```json
[
  {
    "path": "/developer/authoring-path-mapping",
    "title": "Path mapping for AEM authoring",
    "relevanceScore": 51,
    "deprecation": null
  },
  {
    "path": "/developer/folder-mapping",
    "title": "Folder Mapping",
    "relevanceScore": 34.5,
    "deprecation": "Please contact us if you have a use case for folder mapping..."
  }
]
```

**Good Response:**
"I found information about folder mapping, but **this feature is deprecated**. The deprecation notice says: 'Please contact us if you have a use case for folder mapping...'. The current recommended approach is **Path mapping for AEM authoring** (the top result). Let me read that documentation for you instead."

**Poor Response:**
- Ignoring the deprecation warning and implementing the deprecated feature
- Not mentioning the better alternative

## Related Skills

- **block-collection-and-party**: Use when you need reusable code examples or block implementations
- **building-blocks**: Use when creating new blocks from scratch
- **content-modeling**: Use when designing content models for blocks

## Important Reminders

1. **Always check for deprecation warnings** and alert the user
2. **Use WebFetch to read full pages** - search results are just for finding the right pages
3. **Start with top 2-3 results** before expanding search
4. **The description field is your friend** - it's usually well-written and concise
5. **Don't rely solely on snippets** - they're for context, not comprehensive information
