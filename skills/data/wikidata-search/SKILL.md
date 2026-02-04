---
name: wikidata-search
description: Search for items and properties on Wikidata and retrieve entity details, claims, and external identifiers. Supports both keyword search (Wikidata Action API) and semantic/hybrid search (Wikidata Vector Database), plus direct entity retrieval (Special:EntityData) and structured querying (WDQS SPARQL).
---

# Wikidata Search Skill

Search and retrieve data from Wikidata, the free knowledge base.

## Choosing An Access Method

Use the method that matches the task to reduce load and improve accuracy:

- Keyword search by label/alias/description: Action API `wbsearchentities`
- Semantic exploration / fuzzy concept search: Wikidata Vector Database (hybrid vector + keyword via RRF)
- Fetch a known entity's current JSON quickly: Special:EntityData
- Complex graph relations / reporting: Wikidata Query Service (WDQS) SPARQL

## API Endpoints

Base URL: `https://www.wikidata.org/w/api.php`

Entity JSON (often faster for current state): `https://www.wikidata.org/wiki/Special:EntityData/{ID}.json`

SPARQL endpoint: `https://query.wikidata.org/sparql`

Vector DB API: `https://wd-vectordb.wmcloud.org`

## Core Functions

### 1. Search Items (wbsearchentities)

Search for entities by label or alias.

```bash
curl 'https://www.wikidata.org/w/api.php?action=wbsearchentities&search=QUERY&language=en&format=json&type=item&limit=10'
```

Parameters:
- `search`: Search term (required)
- `language`: Language code (default: en)
- `type`: `item` (Q-entities) or `property` (P-entities)
- `limit`: Max results (1-50, default: 7)
- `continue`: Offset for pagination

Response fields per result:
- `id`: Entity ID (e.g., Q42)
- `label`: Primary label
- `description`: Short description
- `aliases`: Alternative names
- `url`: Wikidata page URL

### 2. Get Entity Details (wbgetentities)

Retrieve full entity data including claims/identifiers.

```bash
curl 'https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q42&format=json&props=labels|descriptions|aliases|claims'
```

Parameters:
- `ids`: Pipe-separated entity IDs (max 50)
- `props`: `labels|descriptions|aliases|claims|sitelinks|info`
- `languages`: Filter languages (e.g., `en|fr|de`)

### 3. Get Claims Only (wbgetclaims)

Retrieve claims for specific entity/property.

```bash
curl 'https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=Q42&property=P31&format=json'
```

### 4. Semantic / Hybrid Search (Wikidata Vector Database)

When you don't know the exact label, or want "things like this" discovery, use the Vector DB.

Item search:
```bash
curl 'https://wd-vectordb.wmcloud.org/item/query/?query=QUERY&lang=all&K=20'
```

Property search:
```bash
curl 'https://wd-vectordb.wmcloud.org/property/query/?query=QUERY&lang=all&K=20&exclude_external_ids=false'
```

Optional parameters:
- `lang`: language code, or `all` for cross-language
- `K`: number of results
- `instanceof`: comma-separated QIDs to filter items by "instance of"
- `rerank`: `true|false` (slower)

Response fields:
- `QID` / `PID`
- `similarity_score`
- `rrf_score`
- `source`

### 5. Direct Entity JSON (Special:EntityData)

```bash
curl 'https://www.wikidata.org/wiki/Special:EntityData/Q42.json?flavor=simple'
```

`flavor`:
- `simple`: truthy statements + sitelinks/version
- `full`: full data

### 6. Structured Queries (WDQS SPARQL)

```bash
curl -G 'https://query.wikidata.org/sparql' --data-urlencode 'query=SELECT * WHERE { wd:Q42 ?p ?o } LIMIT 5' -H 'Accept: application/sparql-results+json'
```

## Extracting External Identifiers

External identifiers are stored as claims with datatype `external-id`. Common identifier properties:

| Property | Name                   | Example                |
| -------- | ---------------------- | ---------------------- |
| P214     | VIAF ID                | 75121530               |
| P227     | GND ID                 | 119033364              |
| P244     | Library of Congress ID | n79023811              |
| P213     | ISNI                   | 0000 0001 2144 9326    |
| P345     | IMDb ID                | nm0001354              |
| P646     | Freebase ID            | /m/0282x               |
| P349     | NDL ID                 | 00621256               |
| P268     | BnF ID                 | 11888092r              |
| P269     | IdRef ID               | 026927608              |
| P906     | SELIBR ID              | 182099                 |
| P396     | SBN author ID          | IT\\ICCU\\CFIV\\000163 |

To extract identifiers from `wbgetentities` response:
```python
# claims = response['entities']['Q42']['claims']
# For each property P:
#   claims[P][0]['mainsnak']['datavalue']['value'] -> identifier string
```

## Python Script Usage

Use `scripts/wikidata_api.py` for programmatic access:

```python
from scripts.wikidata_api import WikidataAPI

wd = WikidataAPI()

# Search for items
results = wd.search("Albert Einstein", language="en", limit=5)

# Get entity with identifiers
entity = wd.get_entity("Q937", props=["labels", "descriptions", "claims"])

# Get external identifiers only (all values by default)
identifiers = wd.get_identifiers("Q937")
# Returns: {'P214': ['75121530', ...], 'P227': '118529579', ...}

# Semantic search (Vector DB)
candidates = wd.vector_search_items("a famous science fiction writer", lang="en", k=5)

# SPARQL
raw = wd.execute_sparql("SELECT * WHERE { wd:Q42 ?p ?o } LIMIT 5")
```

## Response Handling

### Search Response Structure
```json
{
  "searchinfo": {"search": "query"},
  "search": [
    {
      "id": "Q42",
      "label": "Douglas Adams",
      "description": "English writer and humorist",
      "aliases": ["Douglas Noël Adams"],
      "url": "//www.wikidata.org/wiki/Q42"
    }
  ]
}
```

### Entity Response Structure
```json
{
  "entities": {
    "Q42": {
      "type": "item",
      "id": "Q42",
      "labels": {"en": {"language": "en", "value": "Douglas Adams"}},
      "descriptions": {"en": {"language": "en", "value": "..."}},
      "claims": {
        "P31": [...],  // instance of
        "P214": [{"mainsnak": {"datavalue": {"value": "113230702"}}}]  // VIAF
      }
    }
  }
}
```

## Best Practices

1. **Choose the right access method**: search vs vector search vs entity fetch vs SPARQL
2. **Rate limiting**: add 500ms-1s delay between requests
3. **Batch requests**: use pipe-separated IDs (max 50 per `wbgetentities` call)
4. **Set User-Agent**: include contact info in headers
5. **Handle 429**: respect `Retry-After` and back off
6. **Action API etiquette**: use `maxlag` and request only needed `props`
