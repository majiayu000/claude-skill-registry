---
name: data-extraction-patterns
description: |
  Common patterns for extracting and combining analytics data from GA4, GSC, and SE Ranking.
  Includes API patterns, rate limiting, caching, and error handling.
---

# Data Extraction Patterns

## When to Use

- Setting up analytics data pipelines
- Combining data from multiple sources
- Handling API rate limits and errors
- Caching frequently accessed data
- Building data collection workflows

## API Reference

### Google Analytics 4 (GA4)

**MCP Server**: `mcp-server-google-analytics`

**Key Operations**:
```
get_report({
  propertyId: "properties/123456789",
  dateRange: { startDate: "30daysAgo", endDate: "today" },
  dimensions: ["pagePath", "date"],
  metrics: ["screenPageViews", "averageSessionDuration", "bounceRate"]
})
```

**Useful Metrics**:
| Metric | Description | Use Case |
|--------|-------------|----------|
| screenPageViews | Total page views | Traffic volume |
| sessions | User sessions | Visitor count |
| averageSessionDuration | Avg time in session | Engagement |
| bounceRate | Single-page visits | Content quality |
| engagementRate | Engaged sessions % | True engagement |
| scrolledUsers | Users who scrolled | Content consumption |

**Useful Dimensions**:
| Dimension | Description |
|-----------|-------------|
| pagePath | URL path |
| date | Date (for trending) |
| sessionSource | Traffic source |
| deviceCategory | Desktop/mobile/tablet |

### Google Search Console (GSC)

**MCP Server**: `mcp-server-gsc`

**Key Operations**:
```
search_analytics({
  siteUrl: "https://example.com",
  startDate: "2025-11-27",
  endDate: "2025-12-27",
  dimensions: ["query", "page"],
  rowLimit: 1000
})

get_url_inspection({
  siteUrl: "https://example.com",
  inspectionUrl: "https://example.com/page"
})
```

**Available Metrics**:
| Metric | Description | Use Case |
|--------|-------------|----------|
| clicks | Total clicks from search | Traffic from Google |
| impressions | Times shown in results | Visibility |
| ctr | Click-through rate | Snippet effectiveness |
| position | Average ranking | SEO success |

**Dimensions**:
| Dimension | Description |
|-----------|-------------|
| query | Search query |
| page | Landing page URL |
| country | User country |
| device | Desktop/mobile/tablet |
| date | Date (for trending) |

### SE Ranking (Official MCP Server)

**MCP Server**: `seo-data-api-mcp` (official SE Ranking MCP)

**Repository**: https://github.com/seranking/seo-data-api-mcp-server

**Installation** (via claudeup TUI - recommended):
```bash
npx claudeup
# Navigate to: MCP Server Setup → SEO & Analytics → se-ranking
```

**Manual Installation**:
```bash
git clone https://github.com/seranking/seo-data-api-mcp-server.git
cd seo-data-api-mcp-server
docker compose build
```

**Environment Variable**: `SERANKING_API_TOKEN`

**Available MCP Tools**:

| Tool | Description | Use Case |
|------|-------------|----------|
| `domainOverview` | Domain performance metrics | Overall domain health |
| `domainKeywords` | Keyword rankings for domain | Track ranking positions |
| `domainCompetitors` | Identify competitors | Competitive analysis |
| `domainKeywordsComparison` | Compare keywords across domains | Gap analysis |
| `backlinksAll` | Retrieve backlink data | Link profile audit |
| `relatedKeywords` | Related keyword discovery | Content expansion |
| `similarKeywords` | Similar keyword suggestions | Keyword clustering |

**Example MCP Calls**:
```
MCP: seo-data-api-mcp.domainOverview({ domain: "example.com" })
MCP: seo-data-api-mcp.domainKeywords({ domain: "example.com", limit: 100 })
MCP: seo-data-api-mcp.backlinksAll({ domain: "example.com" })
```

## Parallel Execution Pattern

### Optimal Data Fetch (All Sources)

```markdown
## Parallel Data Fetch Pattern

When fetching from multiple sources, issue all requests in a SINGLE message
for parallel execution:

┌─────────────────────────────────────────────────────────────────┐
│  MESSAGE 1: Parallel Data Requests                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [MCP Call 1]: google-analytics.get_report(...)                 │
│  [MCP Call 2]: google-search-console.search_analytics(...)      │
│  [WebFetch 3]: SE Ranking API endpoint                          │
│                                                                  │
│  → All execute simultaneously                                    │
│  → Results return when all complete                              │
│  → ~3x faster than sequential                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Sequential (When Needed)

Some operations require sequential execution:

```markdown
## Sequential Pattern (Dependencies)

When one request depends on another's result:

┌─────────────────────────────────────────────────────────────────┐
│  MESSAGE 1: Get list of pages                                   │
│  → Returns: ["/page1", "/page2", "/page3"]                      │
├─────────────────────────────────────────────────────────────────┤
│  MESSAGE 2: Get details for each page                           │
│  → Uses page list from Message 1                                │
│  → Can parallelize within this message                          │
└─────────────────────────────────────────────────────────────────┘
```

## Rate Limiting

### API Rate Limits

| API | Limit | Strategy |
|-----|-------|----------|
| GA4 | 10 QPS per property | Batch dimensions |
| GSC | 1,200 requests/min | Paginate large exports |
| SE Ranking | 100 requests/min | Queue long operations |

### Retry Pattern

```bash
#!/bin/bash
# Retry with exponential backoff

MAX_RETRIES=3
RETRY_DELAY=5

fetch_with_retry() {
    local url="$1"
    local attempt=1

    while [ $attempt -le $MAX_RETRIES ]; do
        response=$(curl -s -w "%{http_code}" -o /tmp/response.json "$url")
        http_code="${response: -3}"

        if [ "$http_code" = "200" ]; then
            cat /tmp/response.json
            return 0
        elif [ "$http_code" = "429" ]; then
            echo "Rate limited, waiting ${RETRY_DELAY}s..." >&2
            sleep $RETRY_DELAY
            RETRY_DELAY=$((RETRY_DELAY * 2))
        else
            echo "Error: HTTP $http_code" >&2
            return 1
        fi

        attempt=$((attempt + 1))
    done

    echo "Max retries exceeded" >&2
    return 1
}
```

## Caching Pattern

### Session-Based Cache

```bash
# Cache structure
SESSION_PATH="/tmp/seo-performance-20251227-143000-example"
CACHE_DIR="${SESSION_PATH}/cache"
CACHE_TTL=3600  # 1 hour in seconds

mkdir -p "$CACHE_DIR"

# Cache key generation
cache_key() {
    echo "$1" | md5sum | cut -d' ' -f1
}

# Check cache
get_cached() {
    local key=$(cache_key "$1")
    local cache_file="${CACHE_DIR}/${key}.json"

    if [ -f "$cache_file" ]; then
        local age=$(($(date +%s) - $(stat -f%m "$cache_file" 2>/dev/null || stat -c%Y "$cache_file")))
        if [ $age -lt $CACHE_TTL ]; then
            cat "$cache_file"
            return 0
        fi
    fi
    return 1
}

# Save to cache
save_cache() {
    local key=$(cache_key "$1")
    local cache_file="${CACHE_DIR}/${key}.json"
    cat > "$cache_file"
}

# Usage
CACHE_KEY="ga4_${URL}_${DATE_RANGE}"
if ! RESULT=$(get_cached "$CACHE_KEY"); then
    RESULT=$(fetch_from_api)
    echo "$RESULT" | save_cache "$CACHE_KEY"
fi
```

## Date Range Standardization

### Common Date Ranges

```bash
# Standard date range calculations
TODAY=$(date +%Y-%m-%d)

case "$RANGE" in
    "7d")
        START_DATE=$(date -v-7d +%Y-%m-%d 2>/dev/null || date -d "7 days ago" +%Y-%m-%d)
        ;;
    "30d")
        START_DATE=$(date -v-30d +%Y-%m-%d 2>/dev/null || date -d "30 days ago" +%Y-%m-%d)
        ;;
    "90d")
        START_DATE=$(date -v-90d +%Y-%m-%d 2>/dev/null || date -d "90 days ago" +%Y-%m-%d)
        ;;
    "mtd")
        START_DATE=$(date +%Y-%m-01)
        ;;
    "ytd")
        START_DATE=$(date +%Y-01-01)
        ;;
esac

END_DATE="$TODAY"
```

### API-Specific Formats

| API | Format | Example |
|-----|--------|---------|
| GA4 | Relative or ISO | "30daysAgo", "2025-12-01" |
| GSC | ISO 8601 | "2025-12-01" |
| SE Ranking | ISO 8601 or Unix | "2025-12-01", 1735689600 |

## Graceful Degradation

### Data Source Fallback

```markdown
## Fallback Strategy

When a data source is unavailable:

┌─────────────────────────────────────────────────────────────────┐
│  PRIMARY SOURCE      │  FALLBACK           │  LAST RESORT       │
├──────────────────────┼─────────────────────┼────────────────────┤
│  GA4 traffic data    │  GSC clicks         │  Estimate from GSC │
│  GSC search perf     │  SE Ranking queries │  WebSearch SERP    │
│  SE Ranking ranks    │  GSC avg position   │  Manual SERP check │
│  CWV (CrUX)          │  PageSpeed API      │  Lighthouse CLI    │
└──────────────────────┴─────────────────────┴────────────────────┘
```

### Partial Data Output

```markdown
## Analysis Report (Partial Data)

### Data Availability

| Source | Status | Impact |
|--------|--------|--------|
| GA4 | NOT CONFIGURED | Missing engagement metrics |
| GSC | AVAILABLE | Full search data |
| SE Ranking | ERROR (rate limit) | Using cached rankings |

### Analysis Notes

This analysis is based on limited data sources:
- Search performance metrics are complete (GSC)
- Engagement metrics unavailable (no GA4)
- Ranking data may be 24h stale (cached)

**Recommendation**: Configure GA4 for complete analysis.
Run `/setup-analytics` to add Google Analytics.
```

## Unified Data Model

### Combined Output Structure

```json
{
  "metadata": {
    "url": "https://example.com/page",
    "fetchedAt": "2025-12-27T14:30:00Z",
    "dateRange": {
      "start": "2025-11-27",
      "end": "2025-12-27"
    }
  },
  "sources": {
    "ga4": {
      "available": true,
      "metrics": {
        "pageViews": 2450,
        "avgTimeOnPage": 222,
        "bounceRate": 38.2,
        "engagementRate": 64.5
      }
    },
    "gsc": {
      "available": true,
      "metrics": {
        "impressions": 15200,
        "clicks": 428,
        "ctr": 2.82,
        "avgPosition": 4.2
      },
      "topQueries": [
        {"query": "seo guide", "clicks": 156, "position": 4}
      ]
    },
    "seRanking": {
      "available": true,
      "rankings": [
        {"keyword": "seo guide", "position": 4, "volume": 12100}
      ],
      "visibility": 42
    }
  },
  "computed": {
    "healthScore": 72,
    "status": "GOOD"
  }
}
```

## Error Handling

### Common Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| 401 Unauthorized | Invalid/expired credentials | Re-run /setup-analytics |
| 403 Forbidden | Missing permissions | Check API access in console |
| 429 Too Many Requests | Rate limit | Wait and retry with backoff |
| 404 Not Found | Invalid property/site | Verify IDs in configuration |
| 500 Server Error | API issue | Retry later, check status page |

### Error Output Pattern

```markdown
## Data Fetch Error

**Source**: Google Analytics 4
**Error**: 403 Forbidden
**Message**: "User does not have sufficient permissions for this property"

### Troubleshooting Steps

1. Verify Service Account email in GA4 Admin
2. Ensure "Viewer" role is granted
3. Check Analytics Data API is enabled
4. Wait 5 minutes for permission propagation

### Workaround

Proceeding with available data sources (GSC, SE Ranking).
GA4 engagement metrics will not be included in this analysis.
```
