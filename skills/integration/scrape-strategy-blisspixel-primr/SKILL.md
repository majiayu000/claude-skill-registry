---
name: scrape-strategy
version: "1.0.0"
description: "Web scraping strategy and troubleshooting. Use when scraping fails, site protection is encountered, or the user asks about scraping tier behavior."

tools:
  - estimate_run
  - research_company
  - check_jobs

resources:
  - file://references/tiers

metadata:
  openclaw:
    requires:
      bins:
        - primr-mcp
      env:
        - GEMINI_API_KEY
---

# Scrape Strategy

Primr uses an 8-tier fallback system for web scraping. See `references/tiers.md` for the full tier table and selection heuristics.

## Key Features

- **Sticky Tier**: Once a tier works for a host, it's tried first for subsequent pages
- **Circuit Breaker**: After 3 consecutive failures of the same tier for a host, that tier is skipped
- **Cookie Handoff**: Cookies obtained by browser tiers are reused by faster HTTP tiers
- **Content Validation**: Checks actual content, not just HTTP status -- catches "200 OK" responses that are actually block pages

## Error Handling

### Content Validation Indicators
- Content length < 1000 bytes
- Contains "access denied", "blocked", "captcha"
- Missing expected content markers
- Redirect to login/challenge page

### Tier Escalation
On failure: log reason, check circuit breaker, try next tier. Stops after 3 consecutive same-error failures.

### Recovery Strategies

| Failure Type | Strategy |
|--------------|----------|
| Timeout | Increase timeout, try slower tier |
| 403 Forbidden | Try stealth tier (4-5) |
| 429 Rate Limit | Exponential backoff, reduce concurrency |
| SSL Error | Try TLS compatibility tier (3) |
| Empty Content | Try aggressive tier (2) |
| CAPTCHA | Skip page, note in results |

## Interpreting Results

```
+ 34/46 pages scraped
34 = successfully scraped, 46 = total selected, 12 = failed
```

- 70%+ success rate: Good coverage
- 50-70%: Acceptable for protected sites
- <50%: Consider deep mode instead

## Example Workflow

```
User: "The site seems heavily protected"

1. Check prior scrape results:
   - Success rate: 35%
   - Most pages blocked at tier 4

2. Recommend strategy:
   "This site has strong protection. I recommend:
    - Use deep mode for external research
    - Or accept partial scrape results

    Deep mode gathers information from external sources
    without needing to access the protected site directly."

3. If user chooses deep mode:
   estimate_run(company, url, "deep")
   -> Cost: $0.80, Time: ~12 minutes
```

## Constraints

- **Patient Timeout**: 90s max per page (allows multiple tier attempts)
- **Concurrency**: 3 concurrent pages default
- **Circuit Breaker**: 3 failures before tier skip
- **Smart Escalation**: Stops after 3 consecutive same-error failures
