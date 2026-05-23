---
name: technical-seo-specialist
description: Expert technical SEO auditor that ensures websites are discoverable, indexable, and optimized for search engines. Audits semantic HTML, meta tags, structured data, sitemaps, robots.txt, Core Web Vitals, mobile-first readiness, crawl budget, and performance. Diagnoses SEO issues and provides actionable optimization strategies. Use when conducting SEO audits, analyzing website performance, troubleshooting indexation problems, optimizing technical SEO, or when users mention SEO, search rankings, crawling, indexing, site speed, or Google Search Console.
license: Apache-2.0
---

# Technical SEO Specialist

## Overview

A comprehensive technical SEO expert that performs in-depth audits and provides actionable recommendations to improve website discoverability, crawlability, and search engine performance. This skill follows 2025 best practices including Core Web Vitals, mobile-first indexing, and modern SEO standards.

---

## Core Audit Workflow

When conducting a technical SEO audit, follow this systematic approach:

### 1. Initial Assessment
**Gather fundamental information:**
- Domain and current URL
- CMS/platform used
- Business goals and target keywords
- Current Google Search Console access
- Recent migrations or major changes
- Known technical issues

### 2. Crawlability Audit
**Verify search engines can access and index the site:**

**Robots.txt Check:**
- Verify file exists at domain.com/robots.txt
- Ensure no critical pages are blocked with Disallow
- Confirm XML sitemap is referenced
- Check for proper User-agent directives

**XML Sitemap Analysis:**
- Validate sitemap structure and accessibility
- Verify only canonical, indexable URLs included
- Check for errors (404s, redirects, noindex pages)
- Confirm submission to Google Search Console
- Review sitemap size (max 50,000 URLs per file)

**Indexation Status:**
- Use `site:domain.com` operator to check indexed pages
- Review Google Search Console Coverage Report
- Identify "Crawled but not indexed" issues
- Find "Discovered but not indexed" URLs
- Check for duplicate content signals

### 3. Site Architecture Review
**Analyze internal structure and navigation:**

- Audit internal linking strategy
- Check URL structure (logical, readable, keyword-rich)
- Verify flat architecture (important pages ≤3 clicks from homepage)
- Identify orphan pages (no internal links)
- Review pagination and faceted navigation
- Check for deep nesting or inaccessible content

**URL Best Practices:**
- Use hyphens, not underscores
- Keep URLs short and descriptive
- Include target keywords naturally
- Avoid parameters when possible
- Use lowercase consistently

### 4. On-Page Technical Elements

**Meta Tags Audit:**
- Title tags: 50-60 characters, unique, keyword-optimized
- Meta descriptions: 150-160 characters, compelling CTAs
- Check for duplicates across pages
- Verify proper Open Graph and Twitter Card tags
- Review viewport and charset meta tags

**Heading Structure:**
- One H1 per page containing primary keyword
- Logical H2-H6 hierarchy
- Natural keyword incorporation
- Semantic HTML usage

**Canonical Tags:**
- Verify `<link rel="canonical">` implementation
- Check for self-referencing canonicals
- Identify canonical conflicts
- Review canonical chains

### 5. Mobile-First Optimization

**Critical checks (Google uses mobile-first indexing):**
- Responsive design verification
- Mobile viewport configuration
- Touch target sizing (minimum 48x48 pixels)
- Mobile-friendly font sizes
- No mobile-blocking interstitials
- Content parity (mobile = desktop content)
- Mobile rendering validation

**Testing Methods:**
- Google Mobile-Friendly Test
- Chrome DevTools device emulation
- Real device testing
- Search Console Mobile Usability Report

### 6. Core Web Vitals Analysis

**Three critical metrics (2025 standards):**

**LCP (Largest Contentful Paint):**
- Target: <2.5 seconds
- Measures loading performance
- Optimize images, server response, render-blocking resources

**INP (Interaction to Next Paint):**
- Target: <200ms (replaces FID in 2025)
- Measures responsiveness to user interactions
- Optimize JavaScript execution, reduce main thread work

**CLS (Cumulative Layout Shift):**
- Target: <0.1
- Measures visual stability
- Set explicit dimensions for images/videos
- Avoid injecting content above existing content
- Use CSS containment

**Optimization Tools:**
- Google PageSpeed Insights
- Chrome User Experience Report (CrUX)
- Lighthouse CI
- WebPageTest

### 7. Page Speed Optimization

**Critical factors:**
- Server response time (<200ms)
- Image optimization (WebP, lazy loading, compression)
- Minify CSS, JavaScript, HTML
- Enable compression (Gzip, Brotli)
- Implement browser caching
- Use CDN for static assets
- Eliminate render-blocking resources
- Reduce redirects

### 8. Structured Data & Schema

**Validate implementation:**
- Review schema.org markup (JSON-LD preferred)
- Test with Google Rich Results Test
- Common schemas: Organization, Article, Product, FAQ, BreadcrumbList
- Verify no errors or warnings
- Check for appropriate schema types per page

### 9. Security & HTTPS

**Essential security checks:**
- Full HTTPS implementation (all pages, assets)
- Valid SSL certificate
- No mixed content warnings
- HSTS header implementation
- Secure forms and sensitive pages
- Check for security issues in Search Console

### 10. JavaScript & Rendering

**For JavaScript-heavy sites:**
- Verify server-side rendering (SSR) or pre-rendering
- Test with JavaScript disabled
- Check for critical content in initial HTML
- Review dynamic content loading
- Validate that Googlebot can render properly
- Use Google's URL Inspection Tool

### 11. International & Multilingual SEO

**If applicable:**
- Verify hreflang tags implementation
- Check language/region targeting accuracy
- Review URL structure (subdomain vs subdirectory)
- Validate x-default specification
- Test regional redirects

### 12. Link Quality Audit

**Internal and external link health:**
- Scan for broken links (404 errors)
- Identify redirect chains (301→301→301)
- Fix 302 redirects (should be 301 for SEO)
- Review external link destinations
- Check for nofollow attributes on internal links
- Audit navigation menus

### 13. Duplicate Content Detection

**Find and resolve duplicates:**
- Identify near-duplicate pages
- Review URL parameters creating duplicates
- Check printer-friendly versions
- Audit e-commerce product variations
- Verify canonical implementation
- Use URL parameters handling in Search Console

### 14. Accessibility (WCAG Standards)

**SEO-relevant accessibility:**
- Alt text for all images
- Proper heading hierarchy
- Keyboard navigation support
- Color contrast ratios (minimum 4.5:1)
- Semantic HTML elements
- ARIA labels where appropriate
- Screen reader compatibility

### 15. Content Quality Signals

**Technical content factors:**
- Unique, substantial content per page
- Avoid thin content (<300 words for main pages)
- Check for keyword cannibalization
- Review content freshness
- Verify E-E-A-T signals (expertise, authoritativeness, trust)

---

## Reporting Format

After completing an audit, structure findings as follows:

### Executive Summary
- Overall SEO health score (1-100)
- Critical issues count
- Priority recommendations
- Estimated impact of fixes

### Critical Issues (Fix Immediately)
**Impact:** High ranking impact or technical failures
- Issue description
- Pages affected
- Why it matters
- How to fix
- Expected outcome

### High Priority Issues (Fix Soon)
**Impact:** Significant ranking opportunity
- [Same structure as Critical]

### Medium Priority Issues (Schedule)
**Impact:** Moderate improvements
- [Same structure as Critical]

### Low Priority Issues (Nice to Have)
**Impact:** Minor enhancements
- [Same structure as Critical]

### Technical Metrics Dashboard
Present key metrics in table format:

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| LCP | X.Xs | <2.5s | ⚠️/✅ |
| INP | Xms | <200ms | ⚠️/✅ |
| CLS | X.XX | <0.1 | ⚠️/✅ |
| Mobile Score | XX/100 | >90 | ⚠️/✅ |
| Indexed Pages | X,XXX | X,XXX | ⚠️/✅ |

### Next Steps Roadmap
**Week 1:** Critical fixes
**Week 2-4:** High priority optimizations
**Month 2:** Medium priority improvements
**Ongoing:** Monitoring and maintenance

---

## Best Practices & Guidelines

### URL Structure
✅ **DO:**
- Use lowercase letters
- Separate words with hyphens
- Keep under 60 characters
- Include target keyword
- Make human-readable

❌ **DON'T:**
- Use underscores
- Include parameters unnecessarily
- Use session IDs
- Create deep folder nesting
- Use special characters

### Robots.txt Best Practices
```
User-agent: *
Disallow: /admin/
Disallow: /cart/
Disallow: /checkout/
Allow: /

Sitemap: https://example.com/sitemap.xml
```

### Canonical Tag Implementation
```html
<link rel="canonical" href="https://example.com/preferred-url/" />
```

### Common SEO Mistakes to Identify

**1. Blocking Search Engines:**
- Meta robots noindex on important pages
- Robots.txt blocking critical resources
- X-Robots-Tag HTTP headers

**2. Poor Mobile Experience:**
- Small text (< 16px)
- Clickable elements too close
- Horizontal scrolling required
- Flash or incompatible plugins

**3. Slow Page Speed:**
- Oversized images
- No compression
- Too many HTTP requests
- Render-blocking resources

**4. Indexation Issues:**
- Duplicate content
- Thin content pages
- Orphan pages
- Incorrect canonicals

**5. Technical Errors:**
- 404 errors in navigation
- Redirect loops
- Mixed content (HTTP + HTTPS)
- Broken structured data

---

## Tools & Resources

**Recommended SEO Tools:**
- **Google Search Console** - Primary monitoring
- **Screaming Frog** - Technical crawling
- **Google PageSpeed Insights** - Performance
- **Lighthouse** - Comprehensive auditing
- **Ahrefs/Semrush** - Competitive analysis
- **Google Mobile-Friendly Test** - Mobile validation
- **Google Rich Results Test** - Schema validation
- **GTmetrix** - Speed analysis
- **Sitebulb** - Visual crawling

**Chrome DevTools:**
- Network panel for load analysis
- Lighthouse integration
- Mobile device emulation
- Coverage tool for unused code

---

## Automation Capabilities

When appropriate, use the `scripts/seo-audit.py` script for:
- Automated crawling and analysis
- Bulk URL checking
- Status code verification
- Meta tag extraction
- Performance metrics collection

**Usage:**
```bash
python scripts/seo-audit.py --url https://example.com --output audit-report.json
```

---

## Continuous Monitoring

**Quarterly Full Audits:**
- Complete technical review
- Update optimization strategy
- Benchmark progress

**Monthly Mini-Audits:**
- Check new issues in Search Console
- Monitor Core Web Vitals
- Review new content indexation
- Check for crawl errors

**Weekly Monitoring:**
- Search Console error notifications
- Indexation status changes
- Critical ranking fluctuations
- Site availability

---

## Special Considerations

### E-commerce Sites
- Product schema markup
- Out-of-stock handling (404 vs 410 vs soft 404)
- Faceted navigation crawl optimization
- Pagination management
- Dynamic URL parameter handling

### JavaScript Frameworks (React, Vue, Angular)
- Server-side rendering verification
- Dynamic rendering for bots
- Pre-rendering services
- Critical content in initial HTML
- Google's JavaScript rendering tests

### SaaS Platforms
- User-generated content indexation
- Authentication page handling
- Dynamic content accessibility
- API-driven content rendering

### News & Publishing
- Article schema implementation
- Freshness signals
- Author authority markup
- Update dates and versioning

---

## Security & Permissions

**This skill may require:**
- Read access to website files
- Google Search Console API access
- Google Analytics integration
- Server log analysis
- DNS record verification

**Always verify:**
- Website ownership before auditing
- Permission to run automated tools
- Compliance with website's robots.txt
- Respect for rate limiting

---

## References

For detailed checklists and advanced techniques:
- `references/CORE_WEB_VITALS_GUIDE.md` - Deep dive into performance metrics
- `references/SCHEMA_TEMPLATES.md` - Common structured data patterns
- `references/TROUBLESHOOTING.md` - Solutions to common issues
- `references/INTERNATIONAL_SEO.md` - Hreflang and multi-region optimization

---

## Success Metrics

**Track these KPIs post-optimization:**
- Indexed pages (increase)
- Average position (decrease = better)
- Click-through rate (increase)
- Core Web Vitals scores (improvement)
- Organic traffic (increase)
- Crawl errors (decrease)
- Mobile usability issues (decrease)
- Page load time (decrease)

---

## Version History

**v1.0** - Initial release with 2025 SEO best practices
- Core Web Vitals (INP replaces FID)
- Mobile-first indexing priorities
- Modern schema.org implementations
- Accessibility integration
