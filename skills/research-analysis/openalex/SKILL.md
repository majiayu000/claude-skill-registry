---
name: openalex
description: >
  Search and retrieve scholarly metadata from the OpenAlex API — a free, open catalog of 270M+ works,
  90M+ authors, and 100K+ sources. Use this skill whenever the user wants to query OpenAlex for works,
  authors, institutions, sources, topics, publishers, or funders. Trigger on phrases like "search OpenAlex
  for X", "find papers in OpenAlex", "OpenAlex works by author Y", "get institution metadata from OpenAlex",
  "look up this DOI in OpenAlex", "how many works does institution X have in OpenAlex", or any request that
  specifically involves the OpenAlex API or database. Also trigger when the user pastes an OpenAlex ID
  (like W1234567890 or A5023888391) or mentions OpenAlex by name in any research context. This skill
  complements the semantic-scholar skill — use OpenAlex when the user asks for it specifically, when they
  need institution/funder/topic data that Semantic Scholar doesn't cover, or when they want open-access
  filtering and aggregation features unique to OpenAlex.
---

# OpenAlex API Skill

Query the [OpenAlex](https://openalex.org) open scholarly metadata catalog via its REST API using curl.

**Base URL:** `https://api.openalex.org`
**Auth:** API key required (free at https://openalex.org/settings/api). Pass as `?api_key=KEY`.
Store in env var `OPENALEX_API_KEY` and use `api_key=$OPENALEX_API_KEY` in queries.

---

## Entity Endpoints

| Endpoint | Description |
|----------|-------------|
| `/works` | Scholarly documents (articles, books, datasets) |
| `/authors` | Researcher profiles with disambiguated identities |
| `/sources` | Journals, repositories, conferences |
| `/institutions` | Universities, research organizations |
| `/topics` | Subject classifications (3-level hierarchy) |
| `/publishers` | Publishing organizations |
| `/funders` | Funding agencies |
| `content.openalex.org/works/{id}.pdf` | PDF download ($0.01 each) |

Singleton lookups are free (e.g., `/works/W2741809807`). List/filter queries cost $0.0001; search queries cost $0.001.

---

## Critical: Two-Step ID Resolution

Names are ambiguous — never filter by display name directly. Resolve to an OpenAlex ID first, then use that ID in filters.

```bash
# WRONG
/works?filter=author_name:Einstein

# CORRECT — two steps
# 1. Search for author → get ID
curl "https://api.openalex.org/authors?search=Einstein&api_key=$OPENALEX_API_KEY"
# Response includes: id = "A5012345678"

# 2. Filter works by that ID
curl "https://api.openalex.org/works?filter=authorships.author.id:A5012345678&api_key=$OPENALEX_API_KEY"
```

This applies to all entities: authors, institutions, sources, topics, publishers, funders.

---

## Query Parameters

```
api_key=        Required. Free key from openalex.org/settings/api
filter=         Filter results (see syntax below)
search=         Full-text search across title/abstract/fulltext
sort=           Sort results (e.g., cited_by_count:desc)
per_page=       Results per page (default 25, max 100)
page=           Page number
sample=         Random sample size (max 10,000)
seed=           Reproducible sampling seed
select=         Limit returned fields (e.g., select=id,title,publication_year)
group_by=       Aggregate results by a field
```

All parameters use **snake_case**.

---

## Filter Syntax

```bash
# Single filter
?filter=publication_year:2024

# Multiple filters (AND) — comma-separated
?filter=publication_year:2024,is_oa:true

# Multiple values (OR) — pipe-separated, up to 100 values
?filter=type:article|book|dataset

# Negation
?filter=type:!paratext

# Comparison operators
?filter=cited_by_count:>100
?filter=publication_year:<2020
?filter=publication_year:2020-2024
```

---

## Common Filter Fields

### Works

```
authorships.author.id         Author's OpenAlex ID
authorships.institutions.id   Institution's OpenAlex ID
primary_location.source.id    Journal/source OpenAlex ID
topics.id                     Topic ID
publication_year              Year (integer)
cited_by_count                Citation count (integer)
is_oa                         Open access (boolean)
type                          article, book, dataset, etc.
has_fulltext                  Has searchable fulltext (boolean)
```

### Authors

```
last_known_institutions.id    Current institution
works_count                   Number of works
cited_by_count                Total citations
```

---

## Common Patterns with curl Examples

### Find works by author (two-step)

```bash
# 1. Find the author
curl -s "https://api.openalex.org/authors?search=Heather+Piwowar&api_key=$OPENALEX_API_KEY" | jq '.results[0] | {id, display_name, works_count}'

# 2. Get their works
curl -s "https://api.openalex.org/works?filter=authorships.author.id:A5023888391&per_page=10&select=id,title,publication_year,cited_by_count&api_key=$OPENALEX_API_KEY" | jq '.results[] | "\(.publication_year) [\(.cited_by_count)] \(.title)"'
```

### Find works from an institution

```bash
# 1. Find the institution
curl -s "https://api.openalex.org/institutions?search=MIT&api_key=$OPENALEX_API_KEY" | jq '.results[0] | {id, display_name}'

# 2. Get highly-cited works
curl -s "https://api.openalex.org/works?filter=authorships.institutions.id:I63966007,cited_by_count:>100&sort=cited_by_count:desc&per_page=10&select=id,title,publication_year,cited_by_count&api_key=$OPENALEX_API_KEY" | jq '.results[]'
```

### Bulk DOI lookup (up to 100)

```bash
curl -s "https://api.openalex.org/works?filter=doi:10.1234/a|10.1234/b|10.1234/c&per_page=100&api_key=$OPENALEX_API_KEY"
```

### Random sample with seed

```bash
curl -s "https://api.openalex.org/works?sample=100&seed=42&select=id,title,publication_year&api_key=$OPENALEX_API_KEY"
```

### Aggregate by field

```bash
curl -s "https://api.openalex.org/works?filter=publication_year:2024&group_by=topics.id&api_key=$OPENALEX_API_KEY"
```

### Single work by OpenAlex ID

```bash
curl -s "https://api.openalex.org/works/W2741809807?api_key=$OPENALEX_API_KEY" | jq '{title, publication_year, cited_by_count, type}'
```

---

## Limits

| Limit | Value |
|-------|-------|
| OR values per filter | 100 |
| `per_page` max | 100 |
| `sample` max | 10,000 |
| Basic paging limit | 10,000 results |

For larger result sets, use cursor-based pagination (pass `cursor=*` on the first request, then use the returned `next_cursor` value).

---

## Error Handling

Implement exponential backoff for 429 (rate limit) and 500 (server error) responses. A simple retry pattern:

```bash
# In practice, just retry the curl command after a brief pause if you get a non-200 response.
# For scripting, use the Python pattern:
# response = requests.get(url, timeout=30)
# if response.status_code in [429, 500]: time.sleep(2 ** attempt)
```

---

## Deprecated Features (Avoid)

| Old | Replacement |
|-----|-------------|
| Concepts | Topics |
| `/text` endpoint | Do not use |
| `host_venue` | `primary_location` |
| `grants` | `funders` and `awards` |

---

## Choosing Between OpenAlex and Semantic Scholar

Both are academic metadata APIs. Choose based on what the user needs:

| Need | Best choice |
|------|-------------|
| Institution/funder/topic metadata | **OpenAlex** (S2 doesn't have these) |
| Open access filtering (`is_oa`) | **OpenAlex** |
| Aggregation (`group_by`) | **OpenAlex** |
| Citation graphs (who cites whom) | **Semantic Scholar** (dedicated endpoints) |
| Abstract text in results | **Semantic Scholar** (richer abstract coverage) |
| Boolean search (AND/OR/NOT in query) | **Semantic Scholar** bulk search |
| Author h-index | **Semantic Scholar** |
| User says "OpenAlex" | **OpenAlex** |
| User says "Semantic Scholar" or "S2" | **Semantic Scholar** |

When in doubt and the user doesn't specify, prefer Semantic Scholar for paper search and OpenAlex for institutional/funder/topic analytics.

---

## Workflow Tips

- Use `select=` to request only the fields you need — smaller responses, lower cost.
- Set `per_page=100` when you need more than the default 25 results.
- For "papers about X" queries, combine `search=` with `filter=cited_by_count:>50` to surface impactful work.
- When displaying results, format as a table with title, year, and citation count.
- Batch DOI lookups with the pipe operator instead of making one request per DOI.
