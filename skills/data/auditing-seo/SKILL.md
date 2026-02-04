---
name: auditing-seo
description: Use this skill when auditing websites for SEO, analyzing search performance, checking technical SEO issues, or optimizing sites for search engines. Performs comprehensive SEO audits covering technical, on-page, and off-page factors. Invoke for SEO analysis, search optimization, keyword research, or improving search rankings.
---

# SEO Audit System

Comprehensive SEO auditing for client websites and Support Forge properties.

## Client Sites to Audit

| Site | Type | Priority |
|------|------|----------|
| support-forge.com | Business/SaaS | High |
| vineyardvalais.com | E-commerce | High |
| witchsbroomcleaning.com | Local Service | High |
| sweetmeadow-bakery.com | Local Business | High |
| homebasevet.com | Local Service | Medium |
| jpbailes.com / me.jbailes.com | Personal | Low |

## Quick Audit Checklist

### Technical SEO (15 min)
```
□ Site loads in under 3 seconds
□ Mobile-friendly (passes Google test)
□ HTTPS enabled (valid SSL)
□ No mixed content warnings
□ XML sitemap exists and submitted
□ Robots.txt properly configured
□ No broken links (404s)
□ Proper redirects (no chains)
□ Clean URL structure
□ Schema markup implemented
```

### On-Page SEO (15 min)
```
□ Unique title tags (50-60 chars)
□ Meta descriptions (150-160 chars)
□ H1 tag on each page (only one)
□ Proper heading hierarchy (H1→H2→H3)
□ Image alt text on all images
□ Internal linking structure
□ Keyword usage (natural, not stuffed)
□ Content length adequate
□ Readable URLs with keywords
□ Open Graph tags for social
```

### Local SEO (10 min)
```
□ Google Business Profile claimed
□ NAP consistent (Name, Address, Phone)
□ Local keywords in content
□ Location pages (if multiple)
□ Local schema markup
□ Reviews being collected
□ Listed in local directories
□ Geo meta tags present
```

## Free SEO Tools

### Google Tools (Essential)
- **Google Search Console**: https://search.google.com/search-console
  - Index status, search performance, errors
- **Google Analytics**: https://analytics.google.com
  - Traffic sources, user behavior
- **PageSpeed Insights**: https://pagespeed.web.dev
  - Core Web Vitals, performance
- **Mobile-Friendly Test**: https://search.google.com/test/mobile-friendly
- **Rich Results Test**: https://search.google.com/test/rich-results

### Technical Analysis
- **GTmetrix**: https://gtmetrix.com - Performance analysis
- **SSL Labs**: https://www.ssllabs.com/ssltest/ - SSL certificate check
- **XML Sitemap Validator**: https://www.xml-sitemaps.com/validate-xml-sitemap.html
- **Robots.txt Tester**: In Google Search Console

### On-Page Analysis
- **Screaming Frog** (free up to 500 URLs): https://www.screamingfrog.co.uk
- **SEO Meta in 1 Click** (Chrome extension)
- **Detailed SEO Extension** (Chrome extension)

### Backlink Analysis
- **Ahrefs Backlink Checker** (free limited): https://ahrefs.com/backlink-checker
- **Moz Link Explorer** (free limited): https://moz.com/link-explorer

### Keyword Research
- **Google Keyword Planner**: https://ads.google.com/keywordplanner
- **Ubersuggest** (free limited): https://neilpatel.com/ubersuggest/
- **AnswerThePublic**: https://answerthepublic.com
- **Google Trends**: https://trends.google.com

## Full SEO Audit Template

### 1. Technical SEO Audit

#### Site Crawlability
```bash
# Check robots.txt
curl https://[domain]/robots.txt

# Check sitemap
curl https://[domain]/sitemap.xml

# Check for noindex tags
curl -s https://[domain] | grep -i "noindex"
```

**Checklist:**
- [ ] Robots.txt allows important pages
- [ ] XML sitemap exists and is valid
- [ ] Sitemap submitted to Search Console
- [ ] No accidental noindex tags
- [ ] Canonical tags implemented correctly

#### Site Speed & Core Web Vitals
```
Run PageSpeed Insights for:
- Homepage
- Key service/product pages
- Blog posts (if applicable)

Target Scores:
- Performance: 90+
- Accessibility: 90+
- Best Practices: 90+
- SEO: 90+

Core Web Vitals Targets:
- LCP (Largest Contentful Paint): < 2.5s
- INP (Interaction to Next Paint): < 200ms
- CLS (Cumulative Layout Shift): < 0.1
```

#### Mobile Optimization
- [ ] Passes Google Mobile-Friendly Test
- [ ] Text readable without zooming
- [ ] Tap targets properly sized
- [ ] No horizontal scrolling
- [ ] Viewport configured correctly

#### Security
- [ ] HTTPS enabled site-wide
- [ ] Valid SSL certificate
- [ ] No mixed content
- [ ] Security headers implemented

### 2. On-Page SEO Audit

#### Title Tags
```
For each key page, document:
| Page | Current Title | Length | Recommendation |
|------|---------------|--------|----------------|
| Home | | /60 | |
| About | | /60 | |
| Services | | /60 | |
| Contact | | /60 | |
```

**Best Practices:**
- 50-60 characters
- Primary keyword near beginning
- Brand name at end
- Unique for each page
- Compelling for clicks

#### Meta Descriptions
```
| Page | Current Description | Length | Recommendation |
|------|---------------------|--------|----------------|
| Home | | /160 | |
| About | | /160 | |
```

**Best Practices:**
- 150-160 characters
- Include primary keyword
- Compelling call-to-action
- Unique for each page

#### Heading Structure
```
Check each page for:
- [ ] One H1 tag (includes keyword)
- [ ] Logical H2-H6 hierarchy
- [ ] Keywords in subheadings
- [ ] Headings describe content
```

#### Content Quality
- [ ] Adequate word count (300+ for basic, 1000+ for cornerstone)
- [ ] Original content (not duplicated)
- [ ] Answers user intent
- [ ] Keywords used naturally
- [ ] Updated/fresh content

#### Images
- [ ] All images have alt text
- [ ] Alt text is descriptive
- [ ] Images are compressed
- [ ] Proper file names (not IMG_1234.jpg)
- [ ] Lazy loading implemented

### 3. Local SEO Audit (For Local Businesses)

#### Google Business Profile
- [ ] Profile claimed and verified
- [ ] Business name matches website
- [ ] Address is accurate
- [ ] Phone number is correct
- [ ] Hours are current
- [ ] Categories are appropriate
- [ ] Description is optimized
- [ ] Photos uploaded (10+ recommended)
- [ ] Posts being published
- [ ] Q&A monitored
- [ ] Reviews being responded to

#### NAP Consistency
```
Check NAP across:
- Website
- Google Business Profile
- Facebook
- Yelp
- Industry directories
- Local directories

Any inconsistencies? Document and fix.
```

#### Local Schema Markup
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "City",
    "addressRegion": "MA",
    "postalCode": "01234"
  },
  "telephone": "978-XXX-XXXX",
  "url": "https://website.com"
}
```

### 4. Off-Page SEO Audit

#### Backlink Profile
- Total backlinks: ___
- Referring domains: ___
- Domain authority: ___
- Toxic backlinks: ___

#### Competitor Comparison
```
| Metric | Your Site | Competitor 1 | Competitor 2 |
|--------|-----------|--------------|--------------|
| Domain Authority | | | |
| Backlinks | | | |
| Keywords Ranking | | | |
```

### 5. Content Audit

#### Existing Content Inventory
```
| URL | Title | Word Count | Traffic | Action |
|-----|-------|------------|---------|--------|
| | | | | Keep/Update/Delete/Merge |
```

#### Content Gaps
- What topics are competitors covering that you're not?
- What questions are customers asking?
- What keywords have opportunity?

## SEO Audit Report Template

```
SEO AUDIT REPORT
================
Website: [URL]
Date: [Date]
Audited by: Support Forge

EXECUTIVE SUMMARY
-----------------
Overall SEO Health: [Good/Needs Work/Critical Issues]

Key Findings:
✓ [Positive finding]
✓ [Positive finding]
✗ [Issue found]
✗ [Issue found]

Priority Actions:
1. [Highest priority fix]
2. [Second priority]
3. [Third priority]

DETAILED FINDINGS
-----------------

Technical SEO: [Score/10]
[Details...]

On-Page SEO: [Score/10]
[Details...]

Local SEO: [Score/10] (if applicable)
[Details...]

Content: [Score/10]
[Details...]

RECOMMENDATIONS
---------------

Immediate (This Week):
1. [Action item]
2. [Action item]

Short-term (This Month):
1. [Action item]
2. [Action item]

Long-term (Ongoing):
1. [Action item]
2. [Action item]

NEXT STEPS
----------
[Recommended next steps and timeline]
```

## Quick Commands

**"SEO audit [domain]"**
→ Run comprehensive audit

**"Check speed for [domain]"**
→ PageSpeed analysis

**"Local SEO check for [business]"**
→ Local SEO specific audit

**"Keyword research for [topic/business]"**
→ Keyword opportunity analysis

**"Compare SEO [domain1] vs [domain2]"**
→ Competitive analysis
