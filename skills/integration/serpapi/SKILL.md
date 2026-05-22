---
name: serpapi
description: SerpApi search engine results API via curl. Use this skill to scrape Google, Bing, YouTube, and other search engines.
vm0_secrets:
  - SERPAPI_API_KEY
---

# SerpApi

Use SerpApi via direct `curl` calls to **scrape search engine results** from Google, Bing, YouTube, and more.

> Official docs: `https://serpapi.com/search-api`

---

## When to Use

Use this skill when you need to:

- **Scrape Google search results** (organic, ads, knowledge graph)
- **Search Google Images, News, Videos, Shopping**
- **Get local business results** from Google Maps
- **Scrape other search engines** (Bing, YouTube, DuckDuckGo, etc.)
- **Monitor SERP rankings** for SEO analysis

---

## Prerequisites

1. Sign up at [SerpApi](https://serpapi.com/)
2. Go to Dashboard and copy your API key
3. Store it in the environment variable `SERPAPI_API_KEY`

```bash
export SERPAPI_API_KEY="your-api-key"
```

### Pricing

- Free tier: 100 searches/month
- API key is passed as a query parameter `api_key`

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

All examples below assume you have `SERPAPI_API_KEY` set.

Base URL: `https://serpapi.com/search`

---

### 1. Basic Google Search

Search Google and get structured JSON results:

```bash
bash -c 'curl -s "https://serpapi.com/search?engine=google&q=artificial+intelligence&api_key=${SERPAPI_API_KEY}"' | jq '.organic_results[:3] | .[] | {title, link, snippet}
```

---

### 2. Search with Location

Search from a specific location:

```bash
bash -c 'curl -s "https://serpapi.com/search?engine=google&q=best+coffee+shops&location=San+Francisco,+California&gl=us&hl=en&api_key=${SERPAPI_API_KEY}"' | jq '.organic_results[:3]'
```

**Parameters:**
- `location`: City, state, or address
- `gl`: Country code (us, uk, de, etc.)
- `hl`: Language code (en, de, fr, etc.)

---

### 3. Google Image Search

Search for images:

```bash
bash -c 'curl -s "https://serpapi.com/search?engine=google_images&q=sunset+beach&api_key=${SERPAPI_API_KEY}"' | jq '.images_results[:3] | .[] | {title, original, thumbnail}
```

---

### 4. Google News Search

Search news articles:

```bash
bash -c 'curl -s "https://serpapi.com/search?engine=google_news&q=technology&api_key=${SERPAPI_API_KEY}"' | jq '.news_results[:3] | .[] | {title, link, source, date}
```

---

### 5. Google Shopping Search

Search products:

```bash
bash -c 'curl -s "https://serpapi.com/search?engine=google_shopping&q=wireless+headphones&api_key=${SERPAPI_API_KEY}"' | jq '.shopping_results[:3] | .[] | {title, price, source}
```

---

### 6. YouTube Search

Search YouTube videos:

```bash
bash -c 'curl -s "https://serpapi.com/search?engine=youtube&search_query=python+tutorial&api_key=${SERPAPI_API_KEY}"' | jq '.video_results[:3] | .[] | {title, link, channel, views}
```

---

### 7. Google Maps / Local Results

Search local businesses:

```bash
bash -c 'curl -s "https://serpapi.com/search?engine=google_maps&q=restaurants&ll=@40.7128,-74.0060,15z&api_key=${SERPAPI_API_KEY}"' | jq '.local_results[:3] | .[] | {title, rating, address}
```

**Parameters:**
- `ll`: Latitude, longitude, and zoom level (e.g., `@40.7128,-74.0060,15z`)

---

### 8. Pagination

Get more results using the `start` parameter:

```bash
# First page (results 1-10)
bash -c 'curl -s "https://serpapi.com/search?engine=google&q=machine+learning&start=0&api_key=${SERPAPI_API_KEY}"' | jq '.organic_results | length'

# Second page (results 11-20)
bash -c 'curl -s "https://serpapi.com/search?engine=google&q=machine+learning&start=10&api_key=${SERPAPI_API_KEY}"' | jq '.organic_results | length'
```

---

### 9. Check Account Info

Check your API usage and credits:

```bash
bash -c 'curl -s "https://serpapi.com/account?api_key=${SERPAPI_API_KEY}"' | jq '{plan_name, searches_per_month, this_month_usage}
```

---

## Supported Engines

| Engine | Parameter | Description |
|--------|-----------|-------------|
| Google Search | `engine=google` | Web search results |
| Google Images | `engine=google_images` | Image search |
| Google News | `engine=google_news` | News articles |
| Google Shopping | `engine=google_shopping` | Product search |
| Google Maps | `engine=google_maps` | Local businesses |
| YouTube | `engine=youtube` | Video search |
| Bing | `engine=bing` | Bing web search |
| DuckDuckGo | `engine=duckduckgo` | Privacy-focused search |

---

## Common Parameters

| Parameter | Description |
|-----------|-------------|
| `q` | Search query (required) |
| `engine` | Search engine to use |
| `location` | Geographic location for search |
| `gl` | Country code (e.g., us, uk) |
| `hl` | Language code (e.g., en, de) |
| `start` | Pagination offset (0, 10, 20...) |
| `num` | Number of results (max 100) |
| `safe` | Safe search (`active` or `off`) |
| `device` | Device type (`desktop`, `mobile`, `tablet`) |

---

## Guidelines

1. **Use specific engines**: Use `google_images`, `google_news` etc. instead of `tbm` parameter for cleaner results
2. **Add location for local searches**: Use `location` and `gl` for geo-targeted results
3. **Cache results**: SerpApi caches results by default; use `no_cache=true` for fresh data
4. **Monitor usage**: Check `/account` endpoint to track API credits
5. **Use jq filters**: Filter large JSON responses to extract only needed data
