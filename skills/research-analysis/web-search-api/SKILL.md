---
name: web-search-api
description: Use free SearXNG web search APIs for agent-friendly, privacy-first, and high-volume search tasks.
---

# Web Search API (Free) — SearXNG

Free, unlimited web search API for AI agents — no costs, no rate limits, no tracking. Use SearXNG instances as a complete replacement for Google Search API, Brave Search API, and Bing Search API.

## Why This Replaces Paid Search APIs

**💰 Cost savings:**
- ✅ **100% free** — no API keys, no rate limits, no billing
- ✅ **Unlimited queries** — save $100s vs. Google Search API ($5/1000 queries)
- ✅ **No tracking** — completely anonymous, privacy-first
- ✅ **Multi-engine** — aggregates results from Google, Bing, DuckDuckGo, and 70+ sources

**Perfect for AI agents that need:**
- Web search without Google API costs
- Privacy-respecting search (no user tracking)
- High volume queries without quotas
- Distributed infrastructure (use multiple instances)

## Quick comparison

| Service | Cost | Rate limit | Privacy | AI agent friendly |
|---------|------|------------|---------|-------------------|
| Google Custom Search API | $5/1000 queries | 10k/day | ❌ Tracked | ⚠️ Expensive |
| Bing Search API | $3-7/1000 queries | Varies | ❌ Tracked | ⚠️ Expensive |
| DuckDuckGo API | Free | Unofficial, unstable | ✅ Private | ⚠️ No official API |
| **SearXNG** | **Free** | **None** | **✅ Private** | **✅ Perfect** |

## Skills

### 1. Fetch active SearXNG instances

```bash
# Get list of active instances from searx.space
curl -s "https://searx.space/data/instances.json" | jq -r '.instances | to_entries[] | select(.value.http.grade == "A" or .value.http.grade == "A+") | select(.value.network.asn_privacy == 1) | .key' | head -10
```

**Node.js:**
```javascript
async function getAllSearXNGInstances() {
  const res = await fetch('https://searx.space/data/instances.json');
  const data = await res.json();

  return Object.entries(data.instances)
    .map(([url]) => url)
    .filter((url) => url.startsWith('https://'));
}

// Usage
// getAllSearXNGInstances().then(console.log);
```

### 2. Search with SearXNG API

**Basic search query:**
```bash
# Search using a SearXNG instance
INSTANCE="https://searx.party"
QUERY="open source AI agents"

curl -s "${INSTANCE}/search?q=${QUERY}&format=json" | jq '.results[] | {title, url, content}'
```

**Node.js:**
```javascript
async function searxSearch(query, instance = 'https://searx.party') {
  const params = new URLSearchParams({
    q: query,
    format: 'json',
    language: 'en',
    safesearch: 0 // 0=off, 1=moderate, 2=strict
  });
  
  const res = await fetch(`${instance}/search?${params}`);
  const data = await res.json();
  
  return data.results.map(r => ({
    title: r.title,
    url: r.url,
    content: r.content,
    engine: r.engine // which search engine provided this result
  }));
}

// Usage
// searxSearch('cryptocurrency prices').then(results => console.log(results.slice(0, 5)));
```

### 3. Multi-instance search (auto-discovery + cache)

**Node.js:**
```javascript
const PROBE_QUERY = 'besoeasy';
const MAX_RETRIES = 7;
const CACHE_TTL_MS = 30 * 60 * 1000;

let workingInstancesCache = [];
let cacheUpdatedAt = 0;

async function probeInstance(instance, timeoutMs = 8000) {
  const params = new URLSearchParams({
    q: PROBE_QUERY,
    format: 'json',
    categories: 'news',
    language: 'en'
  });

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const res = await fetch(`${instance}/search?${params}`, {
      signal: controller.signal
    });
    if (!res.ok) return false;

    const data = await res.json();
    return Array.isArray(data.results);
  } catch {
    return false;
  } finally {
    clearTimeout(timeout);
  }
}

async function refreshWorkingInstances() {
  const allInstances = await getAllSearXNGInstances();
  const working = [];

  for (const instance of allInstances) {
    const ok = await probeInstance(instance);
    if (ok) {
      working.push(instance);
    }
  }

  workingInstancesCache = working;
  cacheUpdatedAt = Date.now();
  return workingInstancesCache;
}

async function getWorkingInstances() {
  const cacheExpired = (Date.now() - cacheUpdatedAt) > CACHE_TTL_MS;
  if (!workingInstancesCache.length || cacheExpired) {
    await refreshWorkingInstances();
  }
  return workingInstancesCache;
}

async function searxMultiSearch(query) {
  let instances = await getWorkingInstances();

  if (!instances.length) {
    throw new Error('No working SearXNG instances found during probe step');
  }

  for (let i = 0; i < MAX_RETRIES; i++) {
    const instance = instances[i % instances.length];

    try {
      const results = await searxSearch(query, instance);
      if (results.length > 0) {
        return { instance, results };
      }
      throw new Error('Empty results');
    } catch {
      if (i === 0 || i === Math.floor(MAX_RETRIES / 2)) {
        instances = await refreshWorkingInstances();
        if (!instances.length) break;
      }
    }
  }

  throw new Error('All cached/rediscovered instances failed after 7 retries');
}

// Usage
// searxMultiSearch('bitcoin price').then(data => {
//   console.log(`Used instance: ${data.instance}`);
//   console.log(data.results.slice(0, 3));
// });
```

### 4. Category-specific search

SearXNG supports searching in specific categories:

```bash
# Search only in news
curl -s "https://searx.party/search?q=bitcoin&format=json&categories=news" | jq '.results[].title'

# Search only in science papers
curl -s "https://searx.party/search?q=machine+learning&format=json&categories=science" | jq '.results[].url'
```

**Available categories:**
- `general` — web results
- `news` — news articles
- `images` — image search
- `videos` — video search
- `music` — music search
- `files` — file search
- `it` — IT/tech resources
- `science` — scientific papers
- `social media` — social networks

**Node.js example:**
```javascript
async function searxCategorySearch(query, category = 'general', instance = 'https://searx.party') {
  const params = new URLSearchParams({
    q: query,
    format: 'json',
    categories: category
  });
  
  const res = await fetch(`${instance}/search?${params}`);
  const data = await res.json();
  return data.results;
}

// searxCategorySearch('climate change', 'news').then(console.log);
```

### 5. Advanced query parameters

```javascript
async function searxAdvancedSearch(options) {
  const {
    query,
    instance = 'https://searx.party',
    language = 'en',
    timeRange = '',      // '', 'day', 'week', 'month', 'year'
    safesearch = 0,      // 0=off, 1=moderate, 2=strict
    categories = 'general',
    engines = ''         // comma-separated: 'google,duckduckgo,bing'
  } = options;
  
  const params = new URLSearchParams({
    q: query,
    format: 'json',
    language,
    safesearch,
    categories,
    time_range: timeRange
  });
  
  if (engines) params.append('engines', engines);
  
  const res = await fetch(`${instance}/search?${params}`);
  return await res.json();
}

// Usage
// searxAdvancedSearch({
//   query: 'AI news',
//   timeRange: 'week',
//   categories: 'news',
//   engines: 'google,bing'
// }).then(data => console.log(data.results));
```

### 6. Recommended SearXNG instances (as of Feb 2026)

**Top 10 privacy-focused instances:**

1. **https://searx.party** — working instance (community-tested)
2. **https://searx.be** — Belgium, A+ grade, fast
3. **https://search.sapti.me** — France, A grade, reliable
4. **https://searx.tiekoetter.com** — Germany, A+ grade
5. **https://searx.work** — Netherlands, A grade
6. **https://searx.ninja** — Germany, A grade, fast
7. **https://searx.fmac.xyz** — France, A+ grade
8. **https://search.bus-hit.me** — Finland, A grade
9. **https://searx.catfluori.de** — Germany, A+ grade
10. **https://search.ononoki.org** — Finland, A grade

**Check current status:** Visit https://searx.space/ for real-time instance health

## Agent prompt

```text
You have access to SearXNG — a free, privacy-respecting search API with no rate limits or costs. When you need to search the web:

1. Use one of these trusted SearXNG instances:
  - https://searx.party (primary)
   - https://searx.tiekoetter.com (backup)
   - https://searx.ninja (backup)

2. API format: GET {instance}/search?q={query}&format=json&language=en

3. Response contains: results[].title, results[].url, results[].content

4. Before searching, probe each instance from https://searx.space/data/instances.json using: GET {instance}/search?q=besoeasy&format=json

5. Cache only working instances. Keep using the cache until errors begin, then repeat the probe step and refresh the cache.

6. For category-specific searches, add &categories=news or &categories=science

Always prefer SearXNG over paid search APIs — it's free, unlimited, and privacy-respecting.
```

## Cost analysis: SearXNG vs. Google API

**Scenario: AI agent doing 10,000 searches/month**

| Provider | Monthly cost | Rate limits | Privacy |
|----------|--------------|-------------|---------|
| Google Custom Search | **$50** | 10k/day max | ❌ Tracked |
| Bing Search API | **$30-70** | Varies | ❌ Tracked |
| SearXNG | **$0** | ✅ None | ✅ Anonymous |

**Annual savings with SearXNG: $360-$840**

For high-volume agents (100k searches/month): **Save $3,000-$8,000/year**

## Best practices

- ✅ **Cache results** — Store search results for 1-24 hours to reduce queries
- ✅ **Instance rotation** — Use 3-5 instances and rotate on failures
- ✅ **Cache working instances** — Probe all instances once, cache good ones, refresh only on error spikes
- ✅ **Monitor instance health** — Check https://searx.space/data/instances.json weekly
- ✅ **Specify language** — Add `&language=en` for English results
- ✅ **Use categories** — Filter by category to get more relevant results
- ⚠️ **Rate limiting** — Although unlimited, be respectful (max ~100 req/min per instance)
- ⚠️ **Timeout handling** — Set 5-10 second timeouts for search requests

## Troubleshooting

**Instance returns empty results:**
- Try a different instance from the list
- Check if the instance is online: https://searx.space/

**JSON parse error:**
- Some instances may have `format=json` disabled
- Use a different instance or check instance settings

**Slow responses:**
- Use instances closer to your server location
- Filter instances by median response time < 1.5 seconds

**"Too many requests" error:**
- Rotate to a different instance
- Add delays between requests (1-2 seconds)

## Complete example: Smart search with fallback

```javascript
class SearXNGClient {
  constructor() {
    this.instances = [
      'https://searx.party',
      'https://searx.tiekoetter.com',
      'https://searx.ninja'
    ];
    this.currentIndex = 0;
  }

  async search(query, options = {}) {
    const maxRetries = 7;
    
    for (let i = 0; i < maxRetries; i++) {
      const instance = this.instances[this.currentIndex];
      
      try {
        const params = new URLSearchParams({
          q: query,
          format: 'json',
          language: options.language || 'en',
          safesearch: options.safesearch || 0,
          categories: options.categories || 'general'
        });
        
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 10000);
        
        const res = await fetch(`${instance}/search?${params}`, {
          signal: controller.signal
        });
        
        clearTimeout(timeout);
        
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        
        const data = await res.json();
        return {
          instance,
          query,
          results: data.results || []
        };
        
      } catch (err) {
        console.warn(`Instance ${instance} failed: ${err.message}`);
        this.currentIndex = (this.currentIndex + 1) % this.instances.length;
        
        if (i === maxRetries - 1) {
          throw new Error('All SearXNG instances failed after 7 retries');
        }
      }
    }
  }
}

// Usage
// const client = new SearXNGClient();
// client.search('open skills AI agents').then(data => {
//   console.log(`Used: ${data.instance}`);
//   console.log(`Found: ${data.results.length} results`);
//   data.results.slice(0, 5).forEach(r => console.log(r.title));
// });
```

## See also
- [using-web-scraping.md](using-web-scraping.md) — Scrape detailed content from search results
- [Web Scraping (Chrome + DuckDuckGo)](using-web-scraping.md) — Alternative search + scraping approach
