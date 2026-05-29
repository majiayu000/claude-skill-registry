---
name: milan-jovanovic-blog
description: Search Milan Jovanovic's .NET blog for Clean Architecture, DDD, CQRS, EF Core, and ASP.NET Core patterns. Use for finding applicable patterns, code examples, and architecture guidance. Invoke when working with .NET projects that could benefit from proven architectural patterns.
allowed-tools: Read, Glob, Grep, Bash
---

# Milan Jovanovic Blog Skill

## Overview

This skill provides access to Milan Jovanovic's curated .NET blog content, filtered to November 2025+ (aligned with .NET 10 GA). It helps developers discover and apply proven patterns for Clean Architecture, Domain-Driven Design, CQRS, Entity Framework Core, and ASP.NET Core.

**Content scope:** Articles published November 2025 and later, with promotional content stripped.

## When to Use This Skill

Use this skill when:

- Working with .NET projects that could benefit from architectural patterns
- Implementing Clean Architecture, DDD, CQRS, or Vertical Slice patterns
- Configuring Entity Framework Core or ASP.NET Core
- Looking for proven .NET code patterns and examples
- Researching .NET 10/Aspire features

## Quick Start

### Search by Keywords

```bash
python scripts/core/find_articles.py search clean architecture cqrs
```

### Filter by Tag

```bash
python scripts/core/find_articles.py tag ef-core
```

### Resolve doc_id to Path

```bash
python scripts/core/find_articles.py resolve milanjovanovic-tech-blog-{slug}
```

### Natural Language Query

```bash
python scripts/core/find_articles.py query "how to implement CQRS"
```

### List Recent Articles

```bash
python scripts/core/find_articles.py list --sort date --limit 10
```

## Tag Taxonomy

| Tag | Description |
| --- | --- |
| `clean-architecture` | Clean/Onion/Hexagonal Architecture patterns |
| `ddd` | Domain-Driven Design (aggregates, value objects, domain events) |
| `cqrs` | Command Query Responsibility Segregation |
| `mediatr` | MediatR library usage patterns |
| `ef-core` | Entity Framework Core optimization and patterns |
| `aspnet-core` | ASP.NET Core patterns and Minimal APIs |
| `modular-monolith` | Modular Monolith architecture |
| `vertical-slice` | Vertical Slice Architecture |
| `dotnet-10` | .NET 10 features and patterns |
| `aspire` | .NET Aspire patterns |
| `result-pattern` | Result pattern for error handling |
| `outbox-pattern` | Transactional outbox pattern |
| `specification-pattern` | Specification pattern |
| `repository-pattern` | Repository pattern |
| `validation` | FluentValidation patterns |
| `testing` | Unit/integration testing patterns |

## Path Resolution

**Windows PowerShell users:** Avoid `cd && python` chains - use absolute paths or run from repo root to prevent path doubling issues.

**Script location:** All scripts are in `scripts/` relative to skill root.

**Canonical content:** Scraped articles are stored in `canonical/milanjovanovic-tech/blog/`.

## Index Management

### Check Index Stats

```bash
python scripts/management/manage_index.py stats
```

### Verify Index Integrity

```bash
python scripts/management/manage_index.py verify
```

### Refresh Index (After Scraping)

```bash
python scripts/management/refresh_index.py
```

## Scraping (Use /scrape-posts Command)

For scraping operations, use the `/milan-jovanovic:scrape-posts` command which handles:

- **Pre-filtering optimization** - Parses dates from listing page before scraping individual articles
- Date filtering (November 2025+)
- Content cleanup (removes promotional sections)
- Idempotent updates (skip unchanged articles via content hash comparison)

### Efficiency Optimizations

The scraping workflow uses **pre-filtering** to minimize firecrawl API calls:

| Scenario | Without Optimization | With Optimization | Savings |
| -------- | -------------------- | ----------------- | ------- |
| No new articles | 10+ requests | 1-2 requests | 80-90% |
| 1 new article | 10+ requests | 2-3 requests | 70-80% |
| Force (unchanged) | 10+ requests | 10+ requests (skips writes) | I/O savings |

**How it works:**

1. Scrape listing page only (1-2 requests)
2. Parse dates from listing markdown (no network)
3. Compare against index to identify new articles
4. Scrape ONLY articles not already indexed

### Check for New Articles (Pre-Filter)

Before scraping, check what needs updating:

```bash
# Check for new articles since November 2025
python scripts/core/check_new_articles.py .claude/temp/listing.md --json --since 2025-11-01

# Force mode - include existing articles for re-check
python scripts/core/check_new_articles.py .claude/temp/listing.md --json --force

# URLs only output
python scripts/core/check_new_articles.py .claude/temp/listing.md --urls-only
```

Output includes `to_scrape` list with `in_index` and `content_hash` for smart handling.

## Python API

For programmatic access, use the public API:

```python
from milan_jovanovic_api import (
    search_articles,
    get_by_tag,
    resolve_doc_id,
    get_article_content,
)

# Search by keywords
results = search_articles(['clean-architecture', 'cqrs'])

# Get articles by tag
ef_articles = get_by_tag('ef-core')

# Resolve doc_id to path
path = resolve_doc_id('milanjovanovic-tech-blog-some-slug')

# Get article content
content = get_article_content('milanjovanovic-tech-blog-some-slug')
```

## Content Cleanup

Scraped articles have promotional content removed:

- Sponsor sections (between title and first H2)
- Promotional footer ("Whenever you're ready, there are X ways...")
- Newsletter signup sections
- Course CTAs
- Reading time metadata

All educational content, code blocks, and internal links are preserved.

## Related Components

- **Command:** `/milan-jovanovic:scrape-posts` - Scrape new articles
- **Agent:** `blog-advisor` - Proactive project analysis and recommendations

## Troubleshooting

### No Results Found

1. Check if index exists: `python scripts/management/manage_index.py count`
2. If count is 0, run scrape: `/milan-jovanovic:scrape-posts`
3. Verify tags with: `python scripts/core/find_articles.py tag --list`

### Path Issues on Windows

Use PowerShell or prefix Git Bash with `MSYS_NO_PATHCONV=1`:

```bash
MSYS_NO_PATHCONV=1 python scripts/core/find_articles.py search cqrs
```

## Version History

- v1.1.0 (2025-12-27): Pre-filtering optimization - 80-90% reduction in firecrawl API calls
- v1.0.0 (2025-12-22): Initial release - November 2025+ articles, full tag taxonomy

---

**Last Updated:** 2025-12-27
