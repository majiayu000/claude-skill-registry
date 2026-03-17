---
name: sitemap-audit
description: Audit website sitemaps for AEO optimization opportunities. Use when analyzing site structure, checking indexed URLs, planning content migrations, or when user mentions "sitemap", "site structure", "URL audit", "page inventory", or "content migration".
allowed-tools: Read, Grep, Glob, WebFetch
---

# Sitemap Audit for AEO

This skill provides methodology for auditing website sitemaps to identify AEO optimization opportunities, content gaps, and migration planning.

## Why Sitemaps Matter for AEO

1. **Crawl Discovery** - LLMs/crawlers use sitemaps to find content
2. **Content Inventory** - Reveals what pages exist vs. what's missing
3. **URL Structure** - Poor slugs hurt LLM understanding
4. **Junk Detection** - Test pages, drafts pollute index
5. **Migration Planning** - Required for language/structure changes

## Sitemap Audit Process

### Step 1: Find All Sitemaps

Check these locations:
```
/sitemap.xml
/sitemap_index.xml
/sitemap-index.xml
/wp-sitemap.xml (WordPress default)
/page-sitemap.xml
/post-sitemap.xml
/robots.txt (often lists sitemap URL)
```

### Step 2: Fetch & Parse Each Sitemap

For sitemap index, extract all child sitemaps:
```xml
<sitemap>
  <loc>https://example.com/page-sitemap.xml</loc>
</sitemap>
```

For regular sitemaps, extract all URLs:
```xml
<url>
  <loc>https://example.com/page/</loc>
  <lastmod>2024-01-01</lastmod>
</url>
```

### Step 3: Categorize URLs

| Category | Examples | AEO Priority |
|----------|----------|--------------|
| **Core Pages** | /, /about/, /services/ | 🔴 Critical |
| **Service Pages** | /service-name/ | 🔴 Critical |
| **Comparison Pages** | /vs/competitor/ | 🔴 Critical |
| **Results/Portfolio** | /results/, /case-studies/ | 🟠 High |
| **Blog Posts** | /blog/post-name/ | 🟡 Medium |
| **Category Pages** | /category/name/ | 🟡 Medium |
| **Legal Pages** | /privacy/, /terms/ | ⚪ Low |
| **Junk Pages** | /test/, /draft/, /elementor-123/ | 🗑️ Delete |

### Step 4: Identify Issues

**Junk Pages (Delete/Noindex):**
- `/test/`, `/test-page/`, `/test123/`
- `/draft-*`, `/preview-*`
- `/elementor-*`, `/et_pb_*` (page builder artifacts)
- `/page/2/`, `/page/3/` (pagination without content)
- `/?p=123` (parameter URLs)

**Slug Issues:**
- Non-English slugs for international audience
- Overly long slugs
- Keyword-stuffed slugs
- Inconsistent patterns

**Missing Critical Pages:**
- No pricing/investment page
- No comparison pages (`/vs/*`)
- No dedicated founder/expert page
- No FAQ page
- No `llms.txt`

**Stale Content:**
- `lastmod` older than 2 years
- Blog posts from 3+ years ago
- Outdated statistics pages

### Step 5: URL Audit Checklist

For each important URL, check:

- [ ] **Slug is English** (for international brands)
- [ ] **Slug is descriptive** (not `/page-123/`)
- [ ] **Slug matches content** (not misleading)
- [ ] **No duplicate content** (same page, different URLs)
- [ ] **Proper hierarchy** (`/services/service-name/` not `/service-name/`)
- [ ] **Mobile version same URL** (no `/m/` or `m.` versions)

## Migration Planning Template

When changing site structure:

```markdown
## URL Migration Map

### Redirects Required

| Old URL | New URL | Type | Priority |
|---------|---------|------|----------|
| /old-page/ | /new-page/ | 301 | High |

### New Pages to Create

| URL | Purpose | Template |
|-----|---------|----------|
| /vs/competitor/ | Comparison | Use comparison template |

### Pages to Delete

| URL | Reason |
|-----|--------|
| /test/ | Junk |

### Redirect Implementation

For WordPress (.htaccess):
\`\`\`apache
RedirectPermanent /old-page/ /new-page/
\`\`\`

For WordPress (plugin):
- Use Redirection plugin
- Or RankMath/Yoast redirect manager
```

## Multilingual Sitemap Considerations

For translated sites:

1. **Check hreflang** - Each URL should have alternates
2. **Separate sitemaps per language** - `/en/sitemap.xml`, `/nl/sitemap.xml`
3. **Consistent slugs** - `/about/` (EN) ↔ `/over-ons/` (NL) properly linked
4. **No mixed content** - Dutch slug with English content = confusion

## Output Format

```markdown
# Sitemap Audit: [Domain]

## Summary
- **Total URLs:** X
- **Core Pages:** X
- **Blog Posts:** X
- **Junk Pages:** X (to delete)

## Sitemaps Found
- [URL 1] (X URLs)
- [URL 2] (X URLs)

## Issues Found

### 🗑️ Junk Pages (Delete)
| URL | Reason |
|-----|--------|
| /test/ | Test page |

### ⚠️ Slug Issues
| URL | Issue | Suggested |
|-----|-------|-----------|
| /haartransplantatie/ | Dutch | /hair-transplant/ |

### ❌ Missing Pages
| Page | Why Needed |
|------|------------|
| /vs/competitor/ | Comparison for AEO |

### 📅 Stale Content
| URL | Last Modified |
|-----|---------------|
| /old-post/ | 2020-01-01 |

## Recommendations
1. [Priority action 1]
2. [Priority action 2]
```

## Quick Reference

**Common Sitemap Generators:**
- WordPress: Yoast, RankMath, default wp-sitemap
- Shopify: Auto-generated
- Next.js: next-sitemap package
- Manual: xml-sitemaps.com

**Sitemap Size Limits:**
- Max 50,000 URLs per sitemap
- Max 50MB uncompressed
- Use sitemap index for larger sites

**Submission Points:**
- Google Search Console
- Bing Webmaster Tools
- Ping: `https://www.google.com/ping?sitemap=URL`
