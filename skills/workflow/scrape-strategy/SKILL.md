---
name: scrape-strategy
version: "2.0.0"
description: "Tier selection heuristics and error handling for web scraping"

metadata:
  openclaw:
    requires:
      bins:
        - primr-mcp
      env:
        - GEMINI_API_KEY

mcp_server: primr
tools:
  - estimate_run
  - research_company
  - check_jobs
resources:
  - primr://research/status
  - primr://output/artifacts
---

# Scrape Strategy Skill (v2.0)

You are an expert at web scraping strategy, understanding when and how to extract content from protected websites.

## 8-Tier Scraping System

Primr uses an 8-tier fallback system for web scraping:

| Tier | Method | Speed | Use Case |
|------|--------|-------|----------|
| 1 | Playwright | Medium | JS-rendered content (default) |
| 2 | Playwright Aggressive | Medium | Accordions, lazy load, expandable content |
| 3 | curl_cffi | Fast | TLS fingerprint impersonation |
| 4 | DrissionPage Stealth | Slow | Challenge waiting, anti-bot bypass |
| 5 | DrissionPage | Slow | Driverless CDP browser |
| 6 | httpx | Fast | HTTP/2 sites |
| 7 | requests | Fast | Simple sites, no JS |
| 8 | Vision | Slow | AI-based extraction (opt-in) |

## Key Features

### Sticky Tier
Once a tier works for a host, it's tried first for subsequent pages from that host.

### Circuit Breaker
After 3 consecutive failures of the same tier for a host, that tier is skipped.

### Cookie Handoff
Cookies obtained by browser tiers are reused by faster HTTP tiers.

### Soft Block Detection
Checks actual content, not just HTTP status. Catches "200 OK" traps where the response is a block page.

## Tier Selection Heuristics

### When to Expect Tier 1-2 (Playwright)
- Modern SPA sites (React, Vue, Angular)
- Sites with dynamic content loading
- Sites with accordions or expandable sections

### When to Expect Tier 3 (curl_cffi)
- Sites with TLS fingerprint detection
- Cloudflare-protected sites (some)
- Sites that block Python user agents

### When to Expect Tier 4-5 (DrissionPage)
- Sites with aggressive bot detection
- Sites requiring JavaScript challenges
- Sites with CAPTCHA (limited success)

### When to Expect Tier 6-7 (HTTP)
- Simple static sites
- API endpoints
- Sites without JavaScript requirements

### When to Expect Tier 8 (Vision)
- Sites with complex layouts
- PDF-heavy content
- Sites where text extraction fails

## Error Handling Patterns

### Soft Block Detection
```
Indicators of soft blocks:
- Content length < 1000 bytes
- Contains "access denied", "blocked", "captcha"
- Missing expected content markers
- Redirect to login/challenge page
```

### Tier Escalation
```
On failure:
1. Log failure reason
2. Check circuit breaker status
3. Try next tier if available
4. After 3 consecutive same-error failures, stop escalation
```

### Recovery Strategies

| Failure Type | Strategy |
|--------------|----------|
| Timeout | Increase timeout, try slower tier |
| 403 Forbidden | Try stealth tier (4-5) |
| 429 Rate Limit | Exponential backoff, reduce concurrency |
| SSL Error | Try curl_cffi (tier 3) |
| Empty Content | Try aggressive tier (2) |
| CAPTCHA | Skip page, note in results |

## Interpreting Scrape Results

### Success Metrics
```
+ 34/46 pages scraped

34 = pages successfully scraped
46 = total pages selected
12 = pages that failed (blocked, timeout, etc.)
```

### Quality Assessment
- 70%+ success rate: Good coverage
- 50-70% success rate: Acceptable for protected sites
- <50% success rate: Consider deep mode instead

### Tier Statistics
```yaml
tier_stats:
  playwright: 20
  playwright_aggressive: 8
  curl_cffi: 4
  drissionpage_stealth: 2
```

Higher numbers in lower tiers = more protected site.

## Mode Selection Guidance

### Use Scrape Mode When:
- Target is company's own website
- Need first-party content
- Budget is limited
- Time is limited

### Use Deep Mode When:
- Site is heavily protected (>50% failure rate)
- Need external sources
- Company website is sparse
- Need market/competitive context

### Use Full Mode When:
- Comprehensive report needed
- Budget allows (~$1.50)
- Time allows (~30 min)
- Both first-party and external sources valuable

## Example Workflow

```
User: "The site seems heavily protected"

Agent:
1. Check prior scrape results:
   - Success rate: 35%
   - Most pages blocked at tier 4
   
2. Recommend strategy:
   "This site has aggressive bot protection. I recommend:
    - Use deep mode for external research
    - Or accept partial scrape results
    
    Deep mode will gather information from external sources
    without hitting the protected site directly."

3. If user chooses deep mode:
   estimate_run(company, url, "deep")
   → Cost: $0.80, Time: ~12 minutes
```

## Constraints

- **Patient Timeout**: 90s max per page (allows multiple tier attempts)
- **Concurrency**: 3 concurrent pages default
- **Circuit Breaker**: 3 failures before tier skip
- **Smart Escalation**: Stops after 3 consecutive same-error failures
