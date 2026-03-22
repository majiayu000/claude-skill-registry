---
name: deduplicate-articles
version: 2.0.0
description: 'DEPRECATED: This skill has been replaced by memory/check_seen and memory/mark_seen
  tools. Use fetch-rss-feeds or other collection skills which handle deduplication
  automatically through the Memory MCP server.

  '
license: MIT
deprecated: true
deprecated_by: memory/check_seen, memory/mark_seen
deprecated_reason: Deduplication is now built into collection skills using Memory
  MCP
metadata:
  domain: news
  category: collection
  requires-approval: false
  confidence: 0.0
  mcp-servers: []
  status: deprecated
---

# Deduplicate Articles (DEPRECATED)

> **⚠️ DEPRECATED**: This skill has been deprecated as of v2.0.0.
>
> Deduplication is now handled automatically by collection skills using the Memory MCP server's `check_seen` and `mark_seen` tools.

## Migration Guide

### Before (v1.0)
Collection and deduplication were separate skills:
1. `fetch-rss-feeds` - Collect articles
2. `deduplicate-articles` - Remove duplicates

### After (v2.0)
Deduplication is built into collection skills:
1. `fetch-rss-feeds` - Collects AND deduplicates using memory/check_seen

### How to Migrate

If you were using `deduplicate-articles`, update your workflow to use the v2.0 collection skills which handle deduplication automatically.

**The new approach:**
1. Before storing an article, call `memory/check_seen` with the article URL as key
2. If not seen, store the article with `memory/add`
3. Mark as seen with `memory/mark_seen`

This is now handled automatically by all collection skills.

## Replacement Tools

| Old Approach | New Approach |
|--------------|--------------|
| `deduplicate-articles` skill | `memory/check_seen` + `memory/mark_seen` |
| In-memory URL set | Redis-backed deduplication with TTL |
| Per-run dedup only | Cross-run persistent deduplication |

## Why Deprecated

1. **Redundant**: Deduplication is now built into collection skills
2. **Better persistence**: Memory MCP provides persistent deduplication with TTL
3. **Simpler workflows**: One fewer skill to coordinate
4. **Consistency**: All collection skills use the same deduplication mechanism

## See Also

- [fetch-rss-feeds](../fetch-rss-feeds/SKILL.md) - v2.0 with built-in dedup
- [fetch-arxiv-papers](../fetch-arxiv-papers/SKILL.md) - v2.0 with built-in dedup
- [fetch-github-trending](../fetch-github-trending/SKILL.md) - v2.0 with built-in dedup
