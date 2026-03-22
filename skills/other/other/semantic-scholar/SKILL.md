---
name: semantic-scholar
description: >
  Search and retrieve research paper metadata using the Semantic Scholar Academic Graph API via curl.
  Use this skill whenever the user wants to find academic papers, look up citations, get paper details
  by DOI/arXiv ID/title, explore an author's publications, or fetch reference/citation lists.
  Trigger on phrases like "find papers on X", "look up this paper", "how many citations does X have",
  "papers citing X", "search for research about X", "get metadata for arxiv:...", or any request
  to explore academic literature. Always use this skill when the task involves academic paper search
  or metadata retrieval — even if the user just pastes a DOI or arXiv link and wants info about it.
---

# Semantic Scholar Paper Metadata Skill

Search and retrieve research paper metadata using the [Semantic Scholar Academic Graph API](https://api.semanticscholar.org/api-docs/).

**Base URL:** `https://api.semanticscholar.org/graph/v1`
**Auth:** No key required for basic use. For higher rate limits, get a free key at https://www.semanticscholar.org/product/api and pass it as `x-api-key` header.

---

## Choosing the Right Endpoint

| Goal | Endpoint |
|------|----------|
| Search by keywords/topic | `GET /paper/search` |
| Boolean/filtered bulk search | `GET /paper/search/bulk` |
| Match by exact/near-exact title | `GET /paper/search/match` |
| Look up a specific paper (DOI, arXiv, etc.) | `GET /paper/{paper_id}` |
| Fetch multiple papers at once | `POST /paper/batch` |
| Papers that cite a paper | `GET /paper/{paper_id}/citations` |
| Papers referenced by a paper | `GET /paper/{paper_id}/references` |
| Author's papers | `GET /author/{author_id}/papers` |

---

## Field Selection

All endpoints accept a `fields` parameter — a comma-separated list. Default response only includes `paperId` and `title`. Always request the fields you need.

**Common fields:**
```
paperId, corpusId, externalIds, title, abstract, year, venue,
publicationDate, authors, citationCount, referenceCount,
influentialCitationCount, isOpenAccess, openAccessPdf,
fieldsOfStudy, s2FieldsOfStudy, publicationTypes
```

**Nested fields** use dot notation:
```
authors.name, authors.affiliations,
citations.title, citations.year, citations.authors,
references.title, references.externalIds,
openAccessPdf.url
```

---

## Endpoint Details & curl Examples

### 1. Keyword Search — `/paper/search`

Best for: topic discovery, finding relevant papers by concept.

```bash
curl -G "https://api.semanticscholar.org/graph/v1/paper/search" \
  --data-urlencode "query=transformer attention mechanism" \
  --data-urlencode "fields=title,year,authors,citationCount,abstract" \
  --data-urlencode "limit=10"
```

**Filters** (all optional, combine freely):
```bash
--data-urlencode "year=2020-2024"               # year range
--data-urlencode "venue=NeurIPS,ICML"           # specific venues
--data-urlencode "fieldsOfStudy=Computer Science"
--data-urlencode "minCitationCount=50"
--data-urlencode "openAccessPdf="               # open access only (empty value = true)
--data-urlencode "publicationDateOrYear=2023-01-01:2023-12-31"
```

**Pagination:** Response includes `total`, `offset`, `next`. Use `offset=N` to page through results (max 1,000 total).

---

### 2. Bulk Search — `/paper/search/bulk`

Best for: large result sets, boolean queries, sorted/filtered exports.

Supports AND/OR/NOT operators and returns up to 1,000 results per call with token-based pagination (no 1,000 total cap).

```bash
curl -G "https://api.semanticscholar.org/graph/v1/paper/search/bulk" \
  --data-urlencode "query=large language models AND safety" \
  --data-urlencode "fields=title,year,citationCount,authors" \
  --data-urlencode "sort=citationCount:desc" \
  --data-urlencode "limit=100"
```

**Sort options:** `paperId`, `publicationDate`, `citationCount` (append `:asc` or `:desc`).

**Pagination:** Response includes a `token` field. Pass it as `&token=...` on the next call.

---

### 3. Title Match — `/paper/search/match`

Best for: "I have this paper title, give me its metadata."
Returns a single best match or 404. Includes a `matchScore`.

```bash
curl -G "https://api.semanticscholar.org/graph/v1/paper/search/match" \
  --data-urlencode "query=Attention Is All You Need" \
  --data-urlencode "fields=title,year,authors,citationCount,externalIds"
```

---

### 4. Paper by ID — `/paper/{paper_id}`

Best for: fetching full metadata when you already have an identifier.

**Supported ID formats** (prefix as shown):
| Format | Example |
|--------|---------|
| S2 Paper ID (bare) | `649def34f8be52c8b66281af98ae884c09aef38a` |
| Corpus ID | `CorpusId:215416146` |
| DOI | `DOI:10.18653/v1/2020.acl-main.463` |
| arXiv | `ARXIV:2005.14165` |
| PubMed | `PMID:23193287` |
| PubMed Central | `PMCID:PMC4535869` |
| ACL Anthology | `ACL:2020.acl-main.463` |
| Semantic Scholar URL | `URL:https://www.semanticscholar.org/paper/...` |

```bash
# By arXiv ID
curl "https://api.semanticscholar.org/graph/v1/paper/ARXIV:1706.03762?fields=title,abstract,year,authors,citationCount,referenceCount,isOpenAccess,openAccessPdf"

# By DOI
curl "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3292500.3330919?fields=title,year,venue,citationCount"
```

---

### 5. Batch Paper Lookup — `POST /paper/batch`

Best for: fetching metadata for a list of known paper IDs (up to 500).

```bash
curl -X POST "https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,year,citationCount" \
  -H "Content-Type: application/json" \
  -d '{"ids": ["ARXIV:1706.03762", "ARXIV:2005.14165", "DOI:10.18653/v1/2020.acl-main.463"]}'
```

---

### 6. Citations & References

```bash
# Papers that CITE this paper (incoming)
curl "https://api.semanticscholar.org/graph/v1/paper/ARXIV:1706.03762/citations?fields=title,year,authors,citationCount&limit=20"

# Papers this paper CITES (outgoing)
curl "https://api.semanticscholar.org/graph/v1/paper/ARXIV:1706.03762/references?fields=title,year,authors&limit=20"
```

Response wraps each item in a `citingPaper` or `citedPaper` key:
```json
{ "data": [{ "citingPaper": { "title": "...", "year": 2023 } }] }
```

---

### 7. Author Lookup

```bash
# Find an author's ID by name
curl -G "https://api.semanticscholar.org/graph/v1/author/search" \
  --data-urlencode "query=Yoshua Bengio" \
  --data-urlencode "fields=name,affiliations,paperCount,citationCount,hIndex"

# Get their papers
curl "https://api.semanticscholar.org/graph/v1/author/{authorId}/papers?fields=title,year,citationCount&limit=20"
```

---

## Rate Limits & API Key

- Without a key: ~100 requests/5 min (shared pool)
- With a free API key: ~1 request/sec sustained

To use an API key:
```bash
curl -H "x-api-key: YOUR_KEY" "https://api.semanticscholar.org/graph/v1/paper/..."
```

Store the key in an env var: `export S2_API_KEY=...`
Then use: `-H "x-api-key: $S2_API_KEY"`

---

## Parsing Results

Use `jq` to extract fields from responses:

```bash
# List titles and citation counts from a search
curl -s -G "https://api.semanticscholar.org/graph/v1/paper/search" \
  --data-urlencode "query=BERT language model" \
  --data-urlencode "fields=title,year,citationCount" \
  --data-urlencode "limit=5" \
| jq '.data[] | "\(.citationCount)\t\(.year)\t\(.title)"'

# Get all author names from a paper
curl -s "https://api.semanticscholar.org/graph/v1/paper/ARXIV:1706.03762?fields=authors.name" \
| jq '[.authors[].name]'

# Extract open access PDF URL
curl -s "https://api.semanticscholar.org/graph/v1/paper/ARXIV:2005.14165?fields=openAccessPdf" \
| jq '.openAccessPdf.url'
```

---

## Workflow Tips

- **Start with `/paper/search/match`** when the user provides a full title — it's faster than a keyword search.
- **Use `/paper/{id}`** when they give you a DOI, arXiv link, or PubMed ID — extract the ID and call directly.
- **For "papers about X"** questions, use `/paper/search` with `minCitationCount` and `year` filters to surface foundational work.
- **For citation counts and h-index exploration**, combine `/author/search` → `/author/{id}/papers` sorted by `citationCount:desc`.
- **Always request only the fields you need** — smaller responses, faster calls.
- **When displaying results**, format as a table with title, year, venue, and citation count for readability.
