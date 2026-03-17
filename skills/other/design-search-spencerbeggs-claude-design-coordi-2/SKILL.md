---
name: design-search
description: Full-text search across design documentation. Use when looking for specific topics, decisions, or patterns documented across design docs.
allowed-tools: Read, Grep, Glob, Bash
context: fork
agent: design-doc-agent
---

# Design Documentation Search

Searches across all design documentation to find relevant content, decisions,
and patterns.

## Overview

This skill provides full-text search across all design docs with filtering,
ranking, and contextual results. Use it to quickly locate specific topics,
architectural decisions, implementation patterns, or TODO items across
the entire design documentation system.

## Quick Start

**Simple search:**

```bash
/design-search "observability"
```

**Filtered search:**

```bash
/design-search "data flow" --category=architecture
```

**Section-specific:**

```bash
/design-search "performance" --section=Rationale
```

## Parameters

### Required

- `query` - Search query (keywords or phrase)

### Optional

- `module` - Limit to specific module
- `category` - Filter by category (architecture, performance, etc.)
- `status` - Filter by status (stub, draft, current, etc.)
- `section` - Search only in specific sections
- `context` - Lines of context to show (default: 2)

## Workflow

High-level search process:

1. **Parse query and filters** from user request
2. **Load design.config.json** to identify target modules
3. **Find documents** matching filters (module, category, status)
4. **Execute search** using Grep with appropriate context
5. **Extract metadata** from document frontmatter
6. **Rank results** by relevance, status, location, and recency
7. **Format output** with context, metadata, and navigation
8. **Suggest related docs** based on cross-references

For detailed implementation steps, see supporting documentation below.

## Supporting Documentation

When you need detailed information, load the appropriate supporting file:

### For Detailed Workflow

See [instructions.md](instructions.md) for:

- Complete step-by-step search workflow
- Frontmatter parsing and metadata extraction
- Result ranking algorithm and scoring
- Navigation path generation
- Edge case handling (no results, too many results)
- Performance optimization strategies
- Output customization options

**Load when:** Performing search or need implementation details

### For Query Syntax

See [query-syntax.md](query-syntax.md) for:

- Search strategies (keyword, multi-term, section-specific, metadata)
- Search patterns (find decisions, implementations, TODOs, trade-offs)
- Query operators (grep options, regex patterns)
- Best practices and performance tips

**Load when:** Performing complex searches or need query syntax reference

### For Filter Options

See [filter-options.md](filter-options.md) for:

- All filter parameters and their valid values
- Filtering process and frontmatter extraction
- Result ranking algorithm and factors
- Advanced features (cross-references, highlighting, grouping)
- Performance optimization techniques

**Load when:** Applying filters, ranking results, or need filtering details

### For Usage Examples

See [examples.md](examples.md) for:

- Complete search examples (simple, filtered, section-specific)
- Output format examples
- Multi-filter searches
- Special cases (no results, too many results)
- Finding decisions, implementations, and TODOs

**Load when:** User needs examples or clarification on search usage

## Error Handling

### No Results Found

```text
INFO: No matches found for "{query}"

Suggestions:
- Try broader search terms
- Remove filters
- Check spelling
- Search for related terms
```

### Too Many Results

```text
WARNING: {count} results found (showing top 20)

Suggestions:
- Add filters (module, category, status)
- Use more specific search terms
- Search in specific section
```

### Invalid Filter

```text
ERROR: Invalid {filter-name}: "{value}"
Valid values: {valid-list}
```

## Integration

Works well with:

- `/design-review` - Review docs found in search
- `/design-validate` - Validate docs found
- `/design-link` - See relationships between search results
- `/design-update` - Update docs found in search

## Success Criteria

A successful search:

- ✅ Finds all relevant matches
- ✅ Ranks results by relevance
- ✅ Provides sufficient context
- ✅ Shows document metadata
- ✅ Offers clear navigation paths
- ✅ Suggests related documents
