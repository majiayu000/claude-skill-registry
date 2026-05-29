---
name: Search Features Expert
description: Work with Leavn search system - UnifiedSearchService, FTS5 database, 50ms debounce, content filtering, search history
allowed-tools: Read, Edit, Grep
---

# Search Features Expert

Expert in search architecture:

**Components**:
- UnifiedSearchService (facade)
- LocalSearchEngine (FTS5)
- ScriptureDatabase (SQLite)
- SearchViewModel (@Observable)
- SearchHistoryService

**Features**:
- 50ms debounce
- BM25 relevance ranking
- 324 results for "love"
- Tab filtering
- Highlighted results

Use when: Search issues, database queries, debounce problems, result display
