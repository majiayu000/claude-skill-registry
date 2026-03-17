---
name: seo_technical
router_kit: ManagementKit
description: Performs technical SEO audits covering site speed, crawlability, indexability, mobile-friendliness, security, and structured data. Identifies technical issues preventing optimal search performance.
metadata:
  skillport:
    category: auto-healed
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, crawling, debugging, design patterns, development, documentation, efficiency, git, indexing, meta tags, optimization, productivity, programming, project management, quality assurance, refactoring, schema.org, seo technical, sitemap, software engineering, standards, testing, utilities, version control, workflow]
---

# Technical SEO Checker

This skill performs comprehensive technical SEO audits to identify issues that may prevent search engines from properly crawling, indexing, and ranking your site.

## When to Use This Skill

- Launching a new website
- Diagnosing ranking drops
- Pre-migration SEO audits
- Regular technical health checks
- Identifying crawl and index issues
- Improving site performance
- Fixing Core Web Vitals issues

## What This Skill Does

1. **Crawlability Audit**: Checks robots.txt, sitemaps, crawl issues
2. **Indexability Review**: Analyzes index status and blockers
3. **Site Speed Analysis**: Evaluates Core Web Vitals and performance
4. **Mobile-Friendliness**: Checks mobile optimization
5. **Security Check**: Reviews HTTPS and security headers
6. **Structured Data Audit**: Validates schema markup
7. **URL Structure Analysis**: Reviews URL patterns and redirects
8. **International SEO**: Checks hreflang and localization

## How to Use

### Full Technical Audit

```
Perform a technical SEO audit for [URL/domain]
```

### Specific Issue Check

```
Check Core Web Vitals for [URL]
```

```
Audit crawlability and indexability for [domain]
```

### Pre-Migration Audit

```
Technical SEO checklist for migrating [old domain] to [new domain]
```

## Instructions

When a user requests a technical SEO audit:

1. **Audit Crawlability**

   ```markdown
   ## Crawlability Analysis
   
   ### Robots.txt Review
   
   **URL**: [domain]/robots.txt
   **Status**: [Found/Not Found/Error]
   
   **Current Content**:
   ```
   [robots.txt content]
   ```
   
   | Check | Status | Notes |
   |-------|--------|-------|
   | File exists | ✅/❌ | [notes] |
   | Valid syntax | ✅/⚠️/❌ | [errors found] |
   | Sitemap declared | ✅/❌ | [sitemap URL] |
   | Important pages blocked | ✅/⚠️/❌ | [blocked paths] |
   | Assets blocked | ✅/⚠️/❌ | [CSS/JS blocked?] |
   | Correct user-agents | ✅/⚠️/❌ | [notes] |
   
   **Issues Found**:
   - [Issue 1]
   - [Issue 2]
   
   **Recommended robots.txt**:
   ```
   User-agent: *
   Allow: /
   Disallow: /admin/
   Disallow: /private/
   
   Sitemap: https://example.com/sitemap.xml
   ```
   
   ---
   
   ### XML Sitemap Review
   
   **Sitemap URL**: [URL]
   **Status**: [Found/Not Found/Error]
   
   | Check | Status | Notes |
   |-------|--------|-------|
   | Sitemap exists | ✅/❌ | [notes] |
   | Valid XML format | ✅/⚠️/❌ | [errors] |
   | In robots.txt | ✅/❌ | [notes] |
   | Submitted to GSC | ✅/⚠️/❌ | [notes] |
   | URLs count | [X] | [appropriate?] |
   | Only indexable URLs | ✅/⚠️/❌ | [notes] |
   | Includes priority | ✅/⚠️ | [notes] |
   | Includes lastmod | ✅/⚠️ | [accurate?] |
   
   **Issues Found**:
   - [Issue 1]
   
   ---
   
   ### Crawl Budget Analysis
   
   | Factor | Status | Impact |
   |--------|--------|--------|
   | Crawl errors | [X] errors | [Low/Med/High] |
   | Duplicate content | [X] pages | [Low/Med/High] |
   | Thin content | [X] pages | [Low/Med/High] |
   | Redirect chains | [X] found | [Low/Med/High] |
   | Orphan pages | [X] found | [Low/Med/High] |
   
   **Crawlability Score**: [X]/10
   ```

2. **Audit Indexability**

   ```markdown
   ## Indexability Analysis
   
   ### Index Status Overview
   
   | Metric | Count | Notes |
   |--------|-------|-------|
   | Pages in sitemap | [X] | |
   | Pages indexed | [X] | [source: site: search] |
   | Index coverage ratio | [X]% | [good if >90%] |
   
   ### Index Blockers Check
   
   | Blocker Type | Found | Pages Affected |
   |--------------|-------|----------------|
   | noindex meta tag | [X] | [list or "none"] |
   | noindex X-Robots | [X] | [list or "none"] |
   | Robots.txt blocked | [X] | [list or "none"] |
   | Canonical to other | [X] | [list or "none"] |
   | 4xx/5xx errors | [X] | [list or "none"] |
   | Redirect loops | [X] | [list or "none"] |
   
   ### Canonical Tags Audit
   
   | Check | Status | Notes |
   |-------|--------|-------|
   | Canonicals present | ✅/⚠️/❌ | [X]% of pages |
   | Self-referencing | ✅/⚠️/❌ | [notes] |
   | Consistent (HTTP/HTTPS) | ✅/⚠️/❌ | [notes] |
   | Consistent (www/non-www) | ✅/⚠️/❌ | [notes] |
   | No conflicting signals | ✅/⚠️/❌ | [notes] |
   
   ### Duplicate Content Issues
   
   | Issue Type | Count | Examples |
   |------------|-------|----------|
   | Exact duplicates | [X] | [URLs] |
   | Near duplicates | [X] | [URLs] |
   | Parameter duplicates | [X] | [URLs] |
   | WWW/non-WWW | [X] | [notes] |
   | HTTP/HTTPS | [X] | [notes] |
   
   **Indexability Score**: [X]/10
   ```

3. **Audit Site Speed & Core Web Vitals**

   ```markdown
   ## Performance Analysis
   
   ### Core Web Vitals
   
   | Metric | Mobile | Desktop | Target | Status |
   |--------|--------|---------|--------|--------|
   | LCP (Largest Contentful Paint) | [X]s | [X]s | <2.5s | ✅/⚠️/❌ |
   | FID (First Input Delay) | [X]ms | [X]ms | <100ms | ✅/⚠️/❌ |
   | CLS (Cumulative Layout Shift) | [X] | [X] | <0.1 | ✅/⚠️/❌ |
   | INP (Interaction to Next Paint) | [X]ms | [X]ms | <200ms | ✅/⚠️/❌ |
   
   ### Additional Performance Metrics
   
   | Metric | Value | Status |
   |--------|-------|--------|
   | Time to First Byte (TTFB) | [X]ms | ✅/⚠️/❌ |
   | First Contentful Paint (FCP) | [X]s | ✅/⚠️/❌ |
   | Speed Index | [X] | ✅/⚠️/❌ |
   | Total Blocking Time | [X]ms | ✅/⚠️/❌ |
   | Page Size | [X]MB | ✅/⚠️/❌ |
   | Requests | [X] | ✅/⚠️/❌ |
   
   ### Performance Issues
   
   **LCP Issues**:
   - [Issue]: [Impact] - [Solution]
   - [Issue]: [Impact] - [Solution]
   
   **CLS Issues**:
   - [Issue]: [Impact] - [Solution]
   
   **Resource Loading**:
   | Resource Type | Count | Size | Issues |
   |---------------|-------|------|--------|
   | Images | [X] | [X]MB | [notes] |
   | JavaScript | [X] | [X]MB | [notes] |
   | CSS | [X] | [X]KB | [notes] |
   | Fonts | [X] | [X]KB | [notes] |
   
   ### Optimization Recommendations
   
   **High Impact**:
   1. [Recommendation] - Est. improvement: [X]s
   2. [Recommendation] - Est. improvement: [X]s
   
   **Medium Impact**:
   1. [Recommendation]
   2. [Recommendation]
   
   **Performance Score**: [X]/10
   ```

4. **Audit Mobile-Friendliness**

   ```markdown
   ## Mobile Optimization Analysis
   
   ### Mobile-Friendly Test
   
   | Check | Status | Notes |
   |-------|--------|-------|
   | Mobile-friendly overall | ✅/❌ | [notes] |
   | Viewport configured | ✅/❌ | [viewport tag] |
   | Text readable | ✅/⚠️/❌ | Font size: [X]px |
   | Tap targets sized | ✅/⚠️/❌ | [notes] |
   | Content fits viewport | ✅/❌ | [notes] |
   | No horizontal scroll | ✅/❌ | [notes] |
   
   ### Responsive Design Check
   
   | Element | Desktop | Mobile | Issues |
   |---------|---------|--------|--------|
   | Navigation | [status] | [status] | [notes] |
   | Images | [status] | [status] | [notes] |
   | Forms | [status] | [status] | [notes] |
   | Tables | [status] | [status] | [notes] |
   | Videos | [status] | [status] | [notes] |
   
   ### Mobile-First Indexing
   
   | Check | Status | Notes |
   |-------|--------|-------|
   | Mobile version has all content | ✅/⚠️/❌ | [notes] |
   | Mobile has same structured data | ✅/⚠️/❌ | [notes] |
   | Mobile has same meta tags | ✅/⚠️/❌ | [notes] |
   | Mobile images have alt text | ✅/⚠️/❌ | [notes] |
   
   **Mobile Score**: [X]/10
   ```

5. **Audit Security & HTTPS**

   ```markdown
   ## Security Analysis
   
   ### HTTPS Status
   
   | Check | Status | Notes |
   |-------|--------|-------|
   | SSL certificate valid | ✅/❌ | Expires: [date] |
   | HTTPS enforced | ✅/❌ | [redirects properly?] |
   | Mixed content | ✅/⚠️/❌ | [X] issues |
   | HSTS enabled | ✅/⚠️ | [notes] |
   | Certificate chain | ✅/⚠️/❌ | [notes] |
   
   ### Security Headers
   
   | Header | Present | Value | Recommended |
   |--------|---------|-------|-------------|
   | Content-Security-Policy | ✅/❌ | [value] | [recommendation] |
   | X-Frame-Options | ✅/❌ | [value] | DENY or SAMEORIGIN |
   | X-Content-Type-Options | ✅/❌ | [value] | nosniff |
   | X-XSS-Protection | ✅/❌ | [value] | 1; mode=block |
   | Referrer-Policy | ✅/❌ | [value] | [recommendation] |
   
   **Security Score**: [X]/10
   ```

6. **Audit URL Structure**

   ```markdown
   ## URL Structure Analysis
   
   ### URL Pattern Review
   
   | Check | Status | Notes |
   |-------|--------|-------|
   | HTTPS URLs | ✅/⚠️/❌ | [X]% HTTPS |
   | Lowercase URLs | ✅/⚠️/❌ | [notes] |
   | No special characters | ✅/⚠️/❌ | [notes] |
   | Readable/descriptive | ✅/⚠️/❌ | [notes] |
   | Appropriate length | ✅/⚠️/❌ | Avg: [X] chars |
   | Keywords in URLs | ✅/⚠️/❌ | [notes] |
   | Consistent structure | ✅/⚠️/❌ | [notes] |
   
   ### URL Issues Found
   
   | Issue Type | Count | Examples |
   |------------|-------|----------|
   | Dynamic parameters | [X] | [URLs] |
   | Session IDs in URLs | [X] | [URLs] |
   | Uppercase characters | [X] | [URLs] |
   | Special characters | [X] | [URLs] |
   | Very long URLs (>100) | [X] | [URLs] |
   
   ### Redirect Analysis
   
   | Check | Status | Notes |
   |-------|--------|-------|
   | Redirect chains | [X] found | [max chain length] |
   | Redirect loops | [X] found | [URLs] |
   | 302 → 301 needed | [X] found | [URLs] |
   | Broken redirects | [X] found | [URLs] |
   
   **URL Score**: [X]/10
   ```

7. **Audit Structured Data**

   ```markdown
   ## Structured Data Analysis
   
   ### Schema Markup Found
   
   | Schema Type | Pages | Valid | Errors |
   |-------------|-------|-------|--------|
   | [Type 1] | [X] | ✅/❌ | [errors] |
   | [Type 2] | [X] | ✅/❌ | [errors] |
   
   ### Validation Results
   
   **Errors**:
   - [Error 1]: [affected pages] - [solution]
   - [Error 2]: [affected pages] - [solution]
   
   **Warnings**:
   - [Warning 1]: [notes]
   
   ### Missing Schema Opportunities
   
   | Page Type | Current Schema | Recommended |
   |-----------|----------------|-------------|
   | Blog posts | [current] | Article + FAQ |
   | Products | [current] | Product + Review |
   | Homepage | [current] | Organization |
   
   **Structured Data Score**: [X]/10
   ```

8. **Audit International SEO (if applicable)**

   ```markdown
   ## International SEO Analysis
   
   ### Hreflang Implementation
   
   | Check | Status | Notes |
   |-------|--------|-------|
   | Hreflang tags present | ✅/❌ | [notes] |
   | Self-referencing | ✅/⚠️/❌ | [notes] |
   | Return tags present | ✅/⚠️/❌ | [notes] |
   | Valid language codes | ✅/⚠️/❌ | [notes] |
   | x-default tag | ✅/⚠️ | [notes] |
   
   ### Language/Region Targeting
   
   | Language | URL | Hreflang | Status |
   |----------|-----|----------|--------|
   | [en-US] | [URL] | [tag] | ✅/⚠️/❌ |
   | [es-ES] | [URL] | [tag] | ✅/⚠️/❌ |
   
   **International Score**: [X]/10
   ```

9. **Generate Technical Audit Summary**

   ```markdown
   # Technical SEO Audit Report
   
   **Domain**: [domain]
   **Audit Date**: [date]
   **Pages Analyzed**: [X]
   
   ## Overall Technical Health: [X]/100
   
   ```
   Score Breakdown:
   ████████░░ Crawlability: 8/10
   ███████░░░ Indexability: 7/10
   █████░░░░░ Performance: 5/10
   ████████░░ Mobile: 8/10
   █████████░ Security: 9/10
   ██████░░░░ URL Structure: 6/10
   █████░░░░░ Structured Data: 5/10
   ```
   
   ## Critical Issues (Fix Immediately)
   
   1. **[Issue]**: [Impact] 
      - Affected: [pages/scope]
      - Solution: [specific fix]
      - Priority: 🔴 Critical
   
   2. **[Issue]**: [Impact]
      - Affected: [pages/scope]
      - Solution: [specific fix]
      - Priority: 🔴 Critical
   
   ## High Priority Issues
   
   1. **[Issue]**: [Solution]
   2. **[Issue]**: [Solution]
   
   ## Medium Priority Issues
   
   1. **[Issue]**: [Solution]
   2. **[Issue]**: [Solution]
   
   ## Quick Wins
   
   These can be fixed quickly for immediate improvement:
   
   1. [Quick fix 1]
   2. [Quick fix 2]
   3. [Quick fix 3]
   
   ## Implementation Roadmap
   
   ### Week 1: Critical Fixes
   - [ ] [Task 1]
   - [ ] [Task 2]
   
   ### Week 2-3: High Priority
   - [ ] [Task 1]
   - [ ] [Task 2]
   
   ### Week 4+: Optimization
   - [ ] [Task 1]
   - [ ] [Task 2]
   
   ## Monitoring Recommendations
   
   Set up alerts for:
   - Core Web Vitals drops
   - Crawl error spikes
   - Index coverage changes
   - Security issues
   ```

## Example

**User**: "Check the technical SEO of example.com"

**Output**: [Comprehensive technical audit following the structure above]

## Technical SEO Checklist

```markdown
### Crawlability
- [ ] robots.txt is valid and not blocking important content
- [ ] XML sitemap exists and is submitted to GSC
- [ ] No crawl errors in Search Console
- [ ] No redirect chains or loops

### Indexability  
- [ ] Important pages are indexable
- [ ] Canonical tags are correct
- [ ] No duplicate content issues
- [ ] Pagination is handled correctly

### Performance
- [ ] Core Web Vitals pass
- [ ] Page speed under 3 seconds
- [ ] Images are optimized
- [ ] JS/CSS are minified

### Mobile
- [ ] Mobile-friendly test passes
- [ ] Viewport is configured
- [ ] Touch elements are properly sized

### Security
- [ ] HTTPS is enforced
- [ ] SSL certificate is valid
- [ ] No mixed content
- [ ] Security headers present

### Structure
- [ ] URLs are clean and descriptive
- [ ] Site architecture is logical
- [ ] Internal linking is strong
```

## Tips for Success

1. **Prioritize by impact** - Fix critical issues first
2. **Monitor continuously** - Use Search Console alerts
3. **Test changes** - Verify fixes work before deploying widely
4. **Document everything** - Track changes for troubleshooting
5. **Regular audits** - Schedule quarterly technical reviews

## Related Skills

*Technical SEO Checker v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Google Search Central Checks](https://developers.google.com/search/docs/fundamentals/seo-starter-guide) & [Web.dev Core Web Vitals](https://web.dev/vitals/)

### Aşama 1: Foundation (Crawl & Index)
- [ ] **Robots.txt**: `Allow` ve `Disallow` kurallarının kritik kaynakları (CSS/JS) engellemediğinden emin ol.
- [ ] **Sitemap**: XML sitemap'in güncel, temiz (404/301 içermeyen) ve Search Console'a gönderilmiş olduğunu doğrula.
- [ ] **Canonicalization**: Her sayfanın kendi "self-referencing canonical" etiketine sahip olduğunu kontrol et (Duplicate content önlemi).

### Aşama 2: Performance (Core Web Vitals)
- [ ] **LCP (Largest Contentful Paint)**: Hero image'ları `preload` et ve lazy-load yapma. Hedef < 2.5 sn.
- [ ] **CLS (Cumulative Layout Shift)**: Tüm görsellere `width` ve `height` ver. Reklam alanlarına `min-height` ata. Hedef < 0.1.
- [ ] **INP (Interaction to Next Paint)**: Main thread'i bloklayan uzun JavaScript görevlerini (Long Tasks) böl. Hedef < 200 ms.

### Aşama 3: Architecture & Rendering
- [ ] **Internal Linking**: Önemli sayfaların site yapısında derinde kalmadığını (Click Depth < 3) kontrol et.
- [ ] **SSR/Hydration**: React/Next.js sitelerde içeriğin sunucu tarafında render edildiğini (Server-Side Rendering) doğrula.
- [ ] **Structured Data**: `Schema.org` işaretlemelerini (Article, Product, Breadcrumb) Rich Results Test aracıyla doğrula.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Google Search Console'da "Coverage" hatası 0 mı? |
| 2 | Mobil uyumluluk testinden başarıyla geçiyor mu? |
| 3 | Hreflang etiketleri (varsa) doğru ve karşılıklı (reciprocal) mı? |

