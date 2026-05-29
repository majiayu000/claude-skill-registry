---
name: web-scraping
description: This skill activates for web scraping and Actor development. It proactively discovers sitemaps/APIs, recommends optimal strategy (sitemap/API/Playwright/hybrid), and implements iteratively. For production, it guides TypeScript Actor creation via Apify CLI.
license: MIT
---

# Web Scraping with Intelligent Strategy Selection

## When This Skill Activates

Activate automatically when user requests:
- "Scrape [website]"
- "Extract data from [site]"
- "Get product information from [URL]"
- "Find all links/pages on [site]"
- "I'm getting blocked" or "Getting 403 errors" (loads `strategies/anti-blocking.md`)
- "Make this an Apify Actor" (loads `apify/` subdirectory)
- "Productionize this scraper"

## Proactive Workflow

This skill follows a systematic 5-phase approach to web scraping, always starting with interactive reconnaissance and ending with production-ready code.

### Phase 1: INTERACTIVE RECONNAISSANCE (Critical First Step)

When user says "scrape X", **immediately start with hands-on reconnaissance** using MCP tools:

**DO NOT jump to automated checks or implementation** - reconnaissance prevents wasted effort and discovers hidden APIs.

#### Use Playwright MCP & Chrome DevTools MCP:

**1. Open site in real browser** (Playwright MCP)
   - Navigate like a real user
   - Observe page loading behavior (SSR? SPA? Loading states?)
   - Take screenshots for reference
   - Test basic interactions

**2. Monitor network traffic** (Chrome DevTools via Playwright)
   - Watch XHR/Fetch requests in real-time
   - **Find API endpoints** returning JSON (10-100x faster than HTML scraping!)
   - Analyze request/response patterns
   - Document headers, cookies, authentication tokens
   - Extract pagination parameters

**3. Test site interactions**
   - **Pagination**: URL-based? API? Infinite scroll?
   - **Filtering and search**: How do they work?
   - **Dynamic content loading**: Triggers and patterns
   - **Authentication flows**: Required? Optional?

**4. Assess protection mechanisms**
   - Cloudflare/bot detection
   - CAPTCHA requirements
   - Rate limiting behavior (test with multiple requests)
   - Fingerprinting scripts

**5. Generate Intelligence Report**
   - Site architecture (framework, rendering method)
   - **Discovered APIs/endpoints** with full specs
   - Protection mechanisms and required countermeasures
   - **Optimal extraction strategy** (API > Sitemap > HTML)
   - Time/complexity estimates

**See**: `workflows/reconnaissance.md` for complete reconnaissance guide with MCP examples

**Why this matters**: Reconnaissance discovers hidden APIs (eliminating need for HTML scraping), identifies blockers before coding, and provides intelligence for optimal strategy selection. **Never skip this step.**

### Phase 2: AUTOMATIC DISCOVERY (Validate Reconnaissance)

After Phase 1 reconnaissance, **validate findings with automated checks**:

#### 1. Check for Sitemaps

```bash
# Automatically check these locations
curl -s https://[site]/robots.txt | grep -i Sitemap
curl -I https://[site]/sitemap.xml
curl -I https://[site]/sitemap_index.xml
```

**Log findings clearly**:
- ✓ "Found sitemap at /sitemap.xml with ~1,234 URLs"
- ✓ "Found sitemap index with 5 sub-sitemaps"
- ✗ "No sitemap detected at common locations"

**Why this matters**: Sitemaps provide instant URL discovery (60x faster than crawling)

#### 2. Investigate APIs

**Prompt user**:
```
Should I check for JSON APIs first? (Highly recommended)

Benefits of APIs vs HTML scraping:
• 10-100x faster execution
• More reliable (structured JSON vs fragile HTML)
• Less bandwidth usage
• Easier to maintain

Check for APIs? [Y/n]
```

**If yes**, guide user:
1. Open browser DevTools → Network tab
2. Navigate the target website
3. Look for XHR/Fetch requests
4. Check for endpoints: `/api/`, `/v1/`, `/v2/`, `/graphql`, `/_next/data/`
5. Analyze request/response format (JSON, GraphQL, REST)

**Log findings**:
- ✓ "Found API: GET /api/products/{id} (returns JSON)"
- ✓ "Found GraphQL endpoint: /graphql"
- ✗ "No obvious public APIs detected"

#### 3. Analyze Site Structure

**Automatically assess**:
- JavaScript-heavy? (Look for React, Vue, Angular indicators)
- Authentication required? (Login walls, auth tokens)
- Page count estimate (from sitemap or site exploration)
- Rate limiting indicators (robots.txt directives)

### Phase 3: STRATEGY RECOMMENDATION

Based on Phases 1-2 findings, present 2-3 options with clear reasoning:

#### Example Output Template:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Analysis of example.com
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1 Intelligence (Reconnaissance):
✓ API discovered via DevTools: GET /api/products?page=N&limit=100
✓ Framework: Next.js (SSR + CSR hybrid)
✓ Protection: Cloudflare detected, rate limit ~60/min
✗ No authentication required

Phase 2 Validation:
✓ Sitemap found: 1,234 product URLs (validates API total)
✓ Static HTML fallback available if needed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommended Approaches:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⭐ Option 1: Hybrid (Sitemap + API) [RECOMMENDED]
   ✓ Use sitemap to get all 1,234 product URLs instantly
   ✓ Extract product IDs from URLs
   ✓ Fetch data via API (fast, reliable JSON)

   Estimated time: 8-12 minutes
   Complexity: Low-Medium
   Data quality: Excellent
   Speed: Very Fast

⚡ Option 2: Sitemap + Playwright
   ✓ Use sitemap for URLs
   ✓ Scrape HTML with Playwright

   Estimated time: 15-20 minutes
   Complexity: Medium
   Data quality: Good
   Speed: Fast

🔧 Option 3: Pure API (if sitemap fails)
   ✓ Discover product IDs through API exploration
   ✓ Fetch all data via API

   Estimated time: 10-15 minutes
   Complexity: Medium
   Data quality: Excellent
   Speed: Fast

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
My Recommendation: Option 1 (Hybrid)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reasoning:
• Sitemap gives us complete URL list (instant discovery)
• API provides clean, structured data (no HTML parsing)
• Combines speed of sitemap with reliability of API
• Best of both worlds

Proceed with Option 1? [Y/n]
```

**Key principles**:
- Always recommend the SIMPLEST approach that works
- Sitemap > API > Playwright (in terms of simplicity)
- Show time estimates and complexity
- Explain reasoning clearly

### Phase 4: ITERATIVE IMPLEMENTATION

Implement scraper incrementally, starting simple and adding complexity only as needed.

**Core Pattern**:
1. Implement recommended approach (minimal code)
2. Test with small batch (5-10 items)
3. Validate data quality
4. Scale to full dataset or fallback
5. Handle blocking if encountered
6. Add robustness (error handling, retries, logging)

**See**: `workflows/implementation.md` for complete implementation patterns and code examples

### Phase 5: PRODUCTIONIZATION (On Request)

Convert scraper to production-ready Apify Actor.

**Activation triggers**:
- "Make this an Apify Actor"
- "Productionize this scraper"
- "Deploy to Apify"
- "Create an actor from this"

**Core Pattern**:
1. Confirm TypeScript preference (STRONGLY RECOMMENDED)
2. Initialize with `apify create` command (CRITICAL)
3. Port scraping logic to Actor format
4. Test locally and deploy

**See**: `workflows/productionization.md` for complete productionization workflow and `apify/` directory for all Actor development guides

## Quick Reference

| Task | Pattern/Command | Documentation |
|------|----------------|---------------|
| **Reconnaissance** | **Playwright + DevTools MCP** | **`workflows/reconnaissance.md`** |
| Find sitemaps | `RobotsFile.find(url)` | `strategies/sitemap-discovery.md` |
| Filter sitemap URLs | `RequestList + regex` | `reference/regex-patterns.md` |
| Discover APIs | DevTools → Network tab | `strategies/api-discovery.md` |
| Playwright scraping | `PlaywrightCrawler` | `strategies/playwright-scraping.md` |
| HTTP scraping | `CheerioCrawler` | `strategies/cheerio-scraping.md` |
| Hybrid approach | Sitemap + API | `strategies/hybrid-approaches.md` |
| Handle blocking | fingerprint-suite + proxies | `strategies/anti-blocking.md` |
| Fingerprint configs | Quick patterns | `reference/fingerprint-patterns.md` |
| Create Apify Actor | `apify create` | `apify/cli-workflow.md` |
| Template selection | Cheerio vs Playwright | `workflows/productionization.md` |
| Input schema | `.actor/input_schema.json` | `apify/input-schemas.md` |
| Deploy actor | `apify push` | `apify/deployment.md` |

## Common Patterns

### Pattern 1: Sitemap-Based Scraping

```javascript
import { RobotsFile, PlaywrightCrawler, Dataset } from 'crawlee';

// Auto-discover and parse sitemaps
const robots = await RobotsFile.find('https://example.com');
const urls = await robots.parseUrlsFromSitemaps();

const crawler = new PlaywrightCrawler({
    async requestHandler({ page, request }) {
        const data = await page.evaluate(() => ({
            title: document.title,
            // ... extract data
        }));
        await Dataset.pushData(data);
    },
});

await crawler.addRequests(urls);
await crawler.run();
```

See `examples/sitemap-basic.js` for complete example.

### Pattern 2: API-Based Scraping

```javascript
import { gotScraping } from 'got-scraping';

const productIds = [123, 456, 789];

for (const id of productIds) {
    const response = await gotScraping({
        url: `https://api.example.com/products/${id}`,
        responseType: 'json',
    });

    console.log(response.body);
}
```

See `examples/api-scraper.js` for complete example.

### Pattern 3: Hybrid (Sitemap + API)

```javascript
// Get URLs from sitemap
const robots = await RobotsFile.find('https://shop.com');
const urls = await robots.parseUrlsFromSitemaps();

// Extract IDs from URLs
const productIds = urls
    .map(url => url.match(/\/products\/(\d+)/)?.[1])
    .filter(Boolean);

// Fetch data via API
for (const id of productIds) {
    const data = await gotScraping({
        url: `https://api.shop.com/v1/products/${id}`,
        responseType: 'json',
    });
    // Process data
}
```

See `examples/hybrid-sitemap-api.js` for complete example.

## Directory Navigation

This skill uses **progressive disclosure** - detailed information is organized in subdirectories and loaded only when needed.

### Workflows (Implementation Patterns)
**For**: Step-by-step workflow guides for each phase

- `workflows/reconnaissance.md` - **Phase 1 interactive reconnaissance (CRITICAL)**
- `workflows/implementation.md` - Phase 4 iterative implementation patterns
- `workflows/productionization.md` - Phase 5 Apify Actor creation workflow

### Strategies (Deep Dives)
**For**: Detailed guides on specific scraping approaches

- `strategies/sitemap-discovery.md` - Complete sitemap guide (4 patterns)
- `strategies/api-discovery.md` - Finding and using APIs
- `strategies/playwright-scraping.md` - Browser-based scraping
- `strategies/cheerio-scraping.md` - HTTP-only scraping
- `strategies/hybrid-approaches.md` - Combining strategies
- `strategies/anti-blocking.md` - Fingerprinting & proxies for blocked sites

### Examples (Runnable Code)
**For**: Working code to reference or execute

**JavaScript Learning Examples** (Simple standalone scripts):
- `examples/sitemap-basic.js` - Simple sitemap scraper
- `examples/api-scraper.js` - Pure API approach
- `examples/playwright-basic.js` - Basic Playwright scraper
- `examples/hybrid-sitemap-api.js` - Combined approach
- `examples/iterative-fallback.js` - Try sitemap→API→Playwright

**TypeScript Production Examples** (Complete Actors):
- `apify/examples/basic-scraper/` - Sitemap + Playwright
- `apify/examples/anti-blocking/` - Fingerprinting + proxies
- `apify/examples/hybrid-api/` - Sitemap + API (optimal)

### Reference (Quick Lookup)
**For**: Quick patterns and troubleshooting

- `reference/regex-patterns.md` - Common URL regex patterns
- `reference/selector-guide.md` - Playwright selector strategies
- `reference/fingerprint-patterns.md` - Common fingerprint configurations
- `reference/anti-patterns.md` - What NOT to do

### Apify (Production Deployment)
**For**: Creating production Apify Actors

- `apify/README.md` - When and how to use Apify
- `apify/typescript-first.md` - **Why TypeScript for actors**
- `apify/cli-workflow.md` - **apify create workflow (CRITICAL)**
- `apify/initialization.md` - Complete setup guide
- `apify/input-schemas.md` - Input validation patterns
- `apify/configuration.md` - actor.json setup
- `apify/deployment.md` - Testing and deployment
- `apify/templates/` - TypeScript boilerplate

**Note**: Each file is self-contained and can be read independently. Claude will navigate to specific files as needed.

## Core Principles

### 1. Progressive Enhancement
Start with the simplest approach that works:
- Sitemap > API > Playwright
- Static > Dynamic
- HTTP > Browser

### 2. Proactive Discovery
Always investigate before implementing:
- Check for sitemaps automatically
- Look for APIs (ask user to check DevTools)
- Analyze site structure

### 3. Iterative Implementation
Build incrementally:
- Small test batch first (5-10 items)
- Validate quality
- Scale or fallback
- Add robustness last

### 4. Production-Ready Code
When productionizing:
- Use TypeScript (strongly recommended)
- Use `apify create` (never manual setup)
- Add proper error handling
- Include logging and monitoring

---

**Remember**: Sitemaps first, APIs second, scraping last!

For detailed guidance on any topic, navigate to the relevant subdirectory file listed above.
