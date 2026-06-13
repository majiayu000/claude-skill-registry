---
name: producthunt-launches
description: "Scrape Product Hunt daily/weekly/monthly/yearly leaderboard launches with full product details, maker profiles, and website contact info. Use when user mentions Product Hunt, producthunt, PH scraper, product hunt launches, product hunt leaderboard, scrape product hunt, product hunt data, PH daily launches, product hunt upvotes, product hunt maker info, extract product hunt, product hunt today, top products product hunt, product hunt archive, PH products, product hunt email extraction, product hunt contact info, producthunt.com scraping, get product hunt launches, product hunt API alternative. Also applies to: startup launch monitoring, new product discovery, maker/founder contact enrichment, product hunt lead generation, daily product hunt digest, competitive product tracking."
---

# Product Hunt — Launch Data Extraction

> Input: date/period parameters → Output: structured product launch data with maker profiles and website contact info

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract complete product launch data from Product Hunt leaderboard pages, enriched with maker profile information and product website contact details.

## Prerequisites

- Browser session is open and can access producthunt.com
- Cloudflare challenge may appear on first visit; use `solve-captcha` or wait for auto-pass

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Cloudflare Verification

Product Hunt uses Cloudflare protection. On first navigation:
1. Navigate to target URL
2. If page title shows "Just a moment..." → `wait stable --timeout 15000` then check title again
3. If still blocked → `solve-captcha`
4. Verify page loaded: title should contain "Product Hunt" or "Best of Product Hunt"

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py)"`. `$(...)` is bash syntax; use the bash tool for execution.

### DOM: Extract product list from leaderboard page

Navigate to the target leaderboard URL first, then extract:

`eval "$(python scripts/extract-leaderboard.py)"`

URL patterns (navigate to the appropriate one before extraction):
- Daily: `https://www.producthunt.com/leaderboard/daily/{YYYY}/{M}/{DD}/all`
- Weekly: `https://www.producthunt.com/leaderboard/weekly/{YYYY}/{week-number}/all`
- Monthly: `https://www.producthunt.com/leaderboard/monthly/{YYYY}/{M}/all`
- Yearly: `https://www.producthunt.com/leaderboard/yearly/{YYYY}/all`

Replace `all` with `featured` for featured-only products.

Output example:
```json
[
  {
    "rank": 1,
    "name": "Product Name",
    "tagline": "Short product description",
    "categories": ["Productivity", "AI"],
    "thumbnail": "https://ph-files.imgix.net/...",
    "upvotes": 135,
    "comments": 42,
    "url": "https://www.producthunt.com/products/product-slug",
    "slug": "product-slug"
  }
]
```

### DOM: Extract launch detail page

Navigate to the launch page URL first (`https://www.producthunt.com/products/{slug}/launches/{launch-slug}`), then extract:

`eval "$(python scripts/extract-launch-detail.py)"`

To find the launch URL from a product page: navigate to `https://www.producthunt.com/products/{slug}` and look for links matching `/products/{slug}/launches/{launch-slug}`.

Output example:
```json
{
  "name": "Product Name",
  "tagline": "Short product tagline",
  "description": "Full product description from OG meta",
  "categories": ["Productivity", "Social Media"],
  "images": ["https://ph-files.imgix.net/gallery1.png", "https://ph-files.imgix.net/gallery2.png"],
  "websiteUrl": "https://product-website.com/?ref=producthunt",
  "upvotes": 135,
  "launchDate": "2025-05-27T07:26:33-07:00",
  "makers": [{"href": "/@username", "name": "Maker Name"}],
  "ogImage": "https://ph-files.imgix.net/og-image.png"
}
```

### DOM: Extract maker profile

Navigate to maker profile URL (`https://www.producthunt.com/@{username}`), then extract:

`eval "$(python scripts/extract-maker-profile.py)"`

Output example:
```json
{
  "name": "Maker Name",
  "slug": "@username",
  "headline": "Creating SaaS Products",
  "aboutText": "Bio text about the maker",
  "links": ["https://twitter.com/username", "https://linkedin.com/in/username"],
  "followers": 22,
  "url": "https://www.producthunt.com/@username"
}
```

### DOM: Extract website email and content

Navigate to the product website URL, wait for load, then extract:

`eval "$(python scripts/extract-website-content.py)"`

Alternatively, use `stealth-extract` for faster extraction without a browser session:
`stealth-extract {website-url} --content-type markdown` then parse the markdown for email patterns.

Output example:
```json
{
  "title": "Product Website Title",
  "url": "https://product-website.com",
  "email": "contact@product-website.com",
  "allEmails": ["contact@product-website.com", "support@product-website.com"],
  "websiteRawText": "Full visible text content of the website..."
}
```

### Composite: Full product extraction (leaderboard + detail + maker + website)

Complete pipeline replicating the full Product Hunt scraper workflow:

1. Navigate to leaderboard page → `wait stable` → `eval "$(python scripts/extract-leaderboard.py)"`
2. For each product from step 1:
   a. Navigate to `https://www.producthunt.com/products/{slug}` → find launch link → navigate to launch page
   b. `wait stable` → `eval "$(python scripts/extract-launch-detail.py)"` → get full details + maker links + website URL
3. (Optional, if `scrapeMakers` is enabled) For each unique maker from step 2:
   a. Navigate to `https://www.producthunt.com/{maker.href}` → `wait stable` → `eval "$(python scripts/extract-maker-profile.py)"`
4. (Optional, if `scrapeWebsite` is enabled) For each product website URL from step 2:
   a. Navigate to website URL → `wait stable` → `eval "$(python scripts/extract-website-content.py)"`
5. Merge all data by product slug

Final output example per product:
```json
{
  "date": "2026-06-10T00:00:00Z",
  "launchDate": "2026-06-10T07:01:04Z",
  "url": "https://www.producthunt.com/products/product-slug",
  "name": "Product Name",
  "shortDescription": "Short tagline",
  "description": "Full description text",
  "categories": ["Productivity", "AI"],
  "maker": {
    "makerHref": "https://www.producthunt.com/@username",
    "name": "Maker Name",
    "slug": "@username",
    "url": "https://www.producthunt.com/@username",
    "links": ["https://twitter.com/maker", "https://linkedin.com/in/maker"],
    "aboutText": "Maker bio text"
  },
  "websiteUrl": "https://product-website.com",
  "images": ["https://ph-files.imgix.net/image1.png"],
  "upvotes": 135,
  "website": {
    "title": "Product Website",
    "url": "https://product-website.com",
    "email": "hello@product-website.com",
    "websiteRawText": "Full page text content..."
  }
}
```

## Pagination

**No pagination required for daily/weekly leaderboard**: All products for a given day load on a single page (typically 15-50 products per day). No infinite scroll or "load more" button exists.

**Yearly leaderboard**: May contain many products. Apply `topNProducts` filter to limit. All visible products are rendered on the single page.

## Success Criteria

- `result count >= 1` (at least one product extracted from leaderboard)
- Core fields non-null: `name`, `tagline`, `upvotes`, `url` present for every product
- Data consistency: extracted product names match what is displayed on the page
- When detail enrichment is performed: `websiteUrl` or `maker` present for enriched items

## Known Limitations

- Cloudflare protection requires initial challenge pass; may need `solve-captcha` on first visit
- No public API available; Product Hunt only accepts persisted GraphQL queries. All data must be extracted via DOM
- Rate limiting: rapid sequential page navigations may trigger Cloudflare blocks. Add 2-3 second delays between product detail page visits
- The `/all` URL path (used by older scrapers) now returns 404; use `/leaderboard/daily/` path instead
- Product detail pages may vary in structure for older launches vs newer ones
- Website email extraction depends on email being visible in page text or HTML; mailto links and contact forms with obfuscated emails will not be captured

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through the command templates serially within a single session; do not parallelize within one browser. Add 2-3 second delays between navigations to avoid Cloudflare blocks. To increase throughput, open multiple stealth browser sessions and distribute work across them
- **Test before batch execution**: After writing a batch script, first test with 1-2 items to verify the script runs correctly; only then run the full batch
- **Reduce redundant pre-operations**: The leaderboard extraction gives all basic data in one pass; only visit detail pages when full description, images, or maker info are needed
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over
- **Skip website extraction when not needed**: Website content extraction is the slowest step (external site navigation). Only enable when email/content data is specifically required

## Experience Notes

Path: `browser-act-skill-forge-memories/producthunt-scraper-producthunt-launches.memory.md` (working directory is determined by the Agent running the Skill)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file.
