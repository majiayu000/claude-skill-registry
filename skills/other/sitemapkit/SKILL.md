---
name: sitemapkit
description: Discover and extract sitemaps from any website using SitemapKit. Use this skill whenever the user wants to find pages on a website, get a list of URLs from a domain, audit a site's structure, crawl a sitemap, check what pages exist on a site, or do anything involving sitemaps or site URL discovery — even if they don't explicitly say "sitemap". Requires the sitemapkit MCP server configured with a valid SITEMAPKIT_API_KEY.
---

# SitemapKit

Use the SitemapKit MCP tools to discover and extract URLs from any website's sitemaps.

## Tools available

- **discover_sitemaps** — finds all sitemap files for a domain (checks robots.txt, common paths, sitemap indexes). Use this first when you just want to know what sitemaps exist.
- **extract_sitemap** — fetches all URLs from a specific sitemap URL. Use when the user gives you a direct sitemap URL.
- **full_crawl** — discovers all sitemaps for a domain and returns every URL across all of them in one call. Use this when the user wants the complete list of pages on a site.

## When to use which tool

| User says | Use |
|-----------|-----|
| "find sitemaps for X" / "does X have a sitemap?" | `discover_sitemaps` |
| "extract URLs from X/sitemap.xml" | `extract_sitemap` |
| "get all pages on X" / "crawl X" / "list all URLs on X" | `full_crawl` |

## Usage guidelines

- Always pass a full URL including protocol: `https://example.com`
- `full_crawl` and `discover_sitemaps` only use the domain — paths are ignored
- `extract_sitemap` needs the exact sitemap URL, e.g. `https://example.com/sitemap.xml`
- Default `max_urls` is 1000. If the user wants more, pass a higher value (up to plan limit)
- If `truncated: true` appears in the result, tell the user there are more URLs and suggest increasing `max_urls`
- Check `meta.quota.remaining` in the response — if it's low, warn the user proactively

## Error handling

| Error | What to tell the user |
|-------|-----------------------|
| `Unauthorized` | API key is missing or invalid. Get one at https://app.sitemapkit.com/settings/api |
| `Monthly quota exceeded` | Plan limit reached. Upgrade at https://sitemapkit.com/pricing |
| `Rate limit exceeded` | Too many requests per minute. Wait and retry — the response includes a `retryAfter` timestamp |

## Example interactions

**"What pages does stripe.com have?"**
→ Call `full_crawl` with `url: "https://stripe.com"`, present the URL list.

**"Find all sitemaps for shopify.com"**
→ Call `discover_sitemaps` with `url: "https://shopify.com"`, list the sitemap URLs found and which sources they came from (robots.txt, common paths, etc.).

**"Extract https://example.com/sitemap-posts.xml"**
→ Call `extract_sitemap` with `url: "https://example.com/sitemap-posts.xml"`, present the URLs with lastmod dates if available.

**"How many pages does vercel.com have?"**
→ Call `full_crawl`, report `totalUrls` and whether the result was truncated.
