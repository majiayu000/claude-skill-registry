---
name: google-seo
version: 1.0.0
author: Claude (sourced from Google SEO Starter Guide)
created: 2026-01-22
last_updated: 2026-01-22
status: active
complexity: moderate
category: content-optimization
tags: [seo, content-quality, web-optimization, google-search, metadata]
source: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
---

# Google SEO Best Practices

## Description
This skill provides comprehensive guidance for optimizing web content and documentation for search engine discoverability based on Google's official SEO Starter Guide. Use this skill when creating new web content, reviewing existing pages for SEO compliance, or documenting best practices for web-based projects. The skill ensures content follows Google's people-first approach while implementing technical optimizations that improve search visibility.

## When to Use This Skill
- When creating new web pages, documentation sites, or online content
- When reviewing existing web content for search optimization
- When generating HTML documentation that needs to be discoverable
- When implementing metadata (titles, descriptions, alt text) for web content
- When structuring URLs, navigation, or site architecture
- When providing guidance on content quality and organization

## When NOT to Use This Skill
- For content not intended for search engines (internal tools, private documentation)
- For API-only services without web interfaces
- When SEO considerations conflict with user experience (prioritize UX)
- For content behind authentication walls where search indexing is inappropriate

## Prerequisites
- Access to web content, documentation, or HTML files
- Understanding of basic HTML structure (`<title>`, `<meta>`, `<img>` tags)
- Familiarity with web architecture (URLs, directories, linking)
- Context about target audience and search vocabulary

## Workflow

### Phase 1: Content Discovery & Indexability
**Purpose**: Ensure Google can find and access your content

#### Step 1.1: Verify Indexing
Check if Google has already indexed your content:
```bash
# Use site: search operator in Google
site:example.com/your-page
```

**Expected Output**: Verification of whether page is indexed

#### Step 1.2: Enable Crawl Access
Ensure Google can access critical resources:
- [ ] CSS files are accessible (not blocked by robots.txt)
- [ ] JavaScript files are accessible
- [ ] Images are accessible
- [ ] Page renders properly in URL Inspection Tool

**Decision Point**:
- IF content is new → Submit sitemap (optional but helpful)
- IF content is established → Monitor via Search Console
- IF critical resources blocked → Update robots.txt

**Expected Output**: Confirmation that Googlebot can fully render page

#### Step 1.3: Establish Link Structure
Enable natural discovery through links:
- Ensure new pages are linked from existing indexed pages
- Create logical navigation hierarchy
- Implement breadcrumb navigation for deep content

**Expected Output**: Clear path for crawlers to discover content

### Phase 2: URL Structure Optimization
**Purpose**: Create descriptive, organized URLs that enhance search results

#### Step 2.1: Design Descriptive URLs
**Best Practices**:
✅ Use meaningful words: `example.com/pets/cats.html`
❌ Avoid random IDs: `example.com/2/6772756D707920636174`

**Implementation**:
```
# Good URL structure
https://example.com/docs/api/authentication
https://example.com/products/laptops/gaming

# Poor URL structure
https://example.com/page?id=12345
https://example.com/p/a/b/c/xyz
```

**Validation**:
- [ ] URLs contain meaningful words
- [ ] URL segments reflect content hierarchy
- [ ] URLs are concise but descriptive

#### Step 2.2: Organize Directory Structure
Group similar content logically:

```
/policies/          # Infrequently updated content
/blog/              # Frequently updated content
/docs/getting-started/
/docs/api-reference/
/products/category/
```

**Expected Output**: Hierarchical URL structure that communicates update frequency and content grouping

#### Step 2.3: Manage Duplicate Content
Implement canonicalization:

```html
<!-- In <head> of duplicate/alternate pages -->
<link rel="canonical" href="https://example.com/preferred-url" />
```

**Or use 301 redirects**:
```
# .htaccess example
Redirect 301 /old-page.html https://example.com/new-page.html
```

**Expected Output**: Each content piece accessible via one primary URL

### Phase 3: Metadata Optimization
**Purpose**: Create compelling titles and descriptions that appear in search results

#### Step 3.1: Craft Unique Titles
Write clear, concise `<title>` elements:

```html
<!-- Good examples -->
<title>API Authentication Guide | Example Docs</title>
<title>Gaming Laptops - High Performance | Example Store</title>

<!-- Poor examples -->
<title>Page 1</title>
<title>Home - Home - Home - Example</title>
<title>Buy cheap laptops gaming computers best deals discount sale</title>
```

**Guidelines**:
- Keep unique per page
- Include business name or key identifier
- Accurately describe page content
- Avoid keyword stuffing

**Expected Output**: Unique, descriptive titles for each page

#### Step 3.2: Write Meta Descriptions
Create 1-2 sentence summaries:

```html
<!-- Good example -->
<meta name="description" content="Learn how to implement OAuth 2.0 authentication in our API with step-by-step code examples for Node.js, Python, and Ruby." />

<!-- Poor example -->
<meta name="description" content="API docs page authentication login security OAuth token password credential user access." />
```

**Guidelines**:
- One unique description per page
- Highlight most relevant information
- Keep succinct (1-2 sentences)
- Write naturally, not keyword-stuffed

**Expected Output**: Unique meta descriptions that accurately summarize page content

### Phase 4: Image Optimization
**Purpose**: Make images discoverable and accessible

#### Step 4.1: Use High-Quality Images
**Best Practices**:
- Use sharp, clear images
- Place images near relevant text
- Ensure surrounding text explains image content

#### Step 4.2: Write Descriptive Alt Text
Implement proper `alt` attributes:

```html
<!-- Good examples -->
<img src="golden-retriever-playing-fetch.jpg"
     alt="Golden retriever catching red frisbee in park" />

<img src="api-authentication-flow.png"
     alt="Diagram showing OAuth 2.0 authentication flow from client to server" />

<!-- Poor examples -->
<img src="img123.jpg" alt="image" />
<img src="photo.jpg" alt="" />
<img src="product.jpg" alt="buy now click here cheap discount sale" />
```

**Guidelines**:
- Keep short but descriptive
- Explain image-content relationship
- Avoid keyword stuffing
- Provide context for accessibility

**Expected Output**: All images have meaningful alt text

### Phase 5: Content Quality & Link Strategy
**Purpose**: Create people-first content with proper link practices

#### Step 5.1: Ensure Content Quality
**Core Attributes Checklist**:
- [ ] Text is easy-to-read and well organized
- [ ] Content is unique (not copied from other sources)
- [ ] Information is current and updated
- [ ] Content is helpful, reliable, and people-first
- [ ] Expertise/authority is demonstrated
- [ ] No keyword stuffing (write naturally)

**Organization**:
- Break long content into paragraphs
- Use clear section headings
- Create logical navigation structure

**Expected Output**: High-quality, original, well-organized content

#### Step 5.2: Implement Link Best Practices
**Anchor Text**:
```html
<!-- Good examples -->
<a href="/api/authentication">Learn about API authentication</a>
<a href="/products/gaming-laptops">Browse gaming laptops</a>

<!-- Poor examples -->
<a href="/page">click here</a>
<a href="/info">read more</a>
```

**Outbound Links**:
- Link to trusted resources that corroborate content
- Add `rel="nofollow"` to untrusted sources

```html
<!-- Trusted resource -->
<a href="https://oauth.net/2/">OAuth 2.0 specification</a>

<!-- User-generated or untrusted content -->
<a href="https://unknown-site.com" rel="nofollow">User submitted link</a>
```

**Expected Output**: Descriptive anchor text and properly qualified outbound links

### Phase 6: Technical Implementation & Structured Data
**Purpose**: Implement technical SEO features

#### Step 6.1: Implement Structured Data
Add schema.org markup for rich results:

```html
<!-- Breadcrumb example -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [{
    "@type": "ListItem",
    "position": 1,
    "name": "Docs",
    "item": "https://example.com/docs"
  },{
    "@type": "ListItem",
    "position": 2,
    "name": "API Reference",
    "item": "https://example.com/docs/api"
  }]
}
</script>
```

#### Step 6.2: Create and Submit Sitemap
Generate XML sitemap for content management:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/docs/getting-started</loc>
    <lastmod>2026-01-22</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

**Expected Output**: Sitemap submitted to Search Console

#### Step 6.3: Configure Robots Meta Tags
Control crawl/index behavior when needed:

```html
<!-- Prevent indexing of test pages -->
<meta name="robots" content="noindex, nofollow" />

<!-- Allow indexing, prevent link following -->
<meta name="robots" content="index, nofollow" />
```

**Expected Output**: Appropriate robots directives on all pages

## Examples

### Example 1: Optimizing Documentation Site
**Context**: Creating new API documentation site with 50+ pages

**Input:**
```
Project: API Documentation
Pages: Authentication, Endpoints, Examples, Guides
Current state: Basic HTML with generic titles
```

**Execution Flow:**
1. **Phase 1**: Verify localhost isn't blocking CSS/JS → Create sitemap
2. **Phase 2**: Restructure URLs from `/page1.html` to `/docs/authentication`
3. **Phase 3**: Write unique titles:
   - `<title>API Authentication - OAuth 2.0 Guide | Example API</title>`
   - `<title>POST /users Endpoint Reference | Example API</title>`
4. **Phase 4**: Add alt text to all code diagram images
5. **Phase 5**: Add descriptive anchor text to cross-references
6. **Phase 6**: Implement breadcrumb structured data

**Expected Output:**
- 50 pages with unique, descriptive titles and meta descriptions
- Logical URL hierarchy (`/docs/authentication`, `/docs/endpoints/users`)
- All images with proper alt text
- Breadcrumb navigation with schema.org markup
- Sitemap submitted to Search Console

**Rationale**: Documentation sites benefit greatly from SEO as users primarily discover APIs through search

### Example 2: Content Quality Review
**Context**: Existing blog with poor search performance

**Input:**
```markdown
Current issues:
- Generic titles ("Blog Post 1", "Blog Post 2")
- No meta descriptions
- Short, thin content (<200 words)
- Heavy keyword stuffing
- No internal linking structure
```

**Execution Flow:**
1. **Quality Audit**: Identify thin content for expansion or deletion
2. **Title Rewrite**: "Blog Post 1" → "How to Implement OAuth 2.0 in Node.js"
3. **Meta Description**: Add unique 1-2 sentence summary per post
4. **Content Enhancement**: Expand thin posts with unique insights
5. **Link Structure**: Add descriptive internal links between related posts
6. **Keyword Review**: Remove keyword stuffing, write naturally

**Expected Output:**
```html
<!-- Before -->
<title>Blog Post 1</title>
<!-- No meta description -->
<p>OAuth security authentication login API security token...</p>

<!-- After -->
<title>How to Implement OAuth 2.0 in Node.js | Example Blog</title>
<meta name="description" content="Learn how to add OAuth 2.0 authentication to your Node.js application with this step-by-step tutorial including code examples." />
<p>OAuth 2.0 provides a secure authentication framework for web applications. This guide walks through implementing OAuth in a Node.js Express application...</p>
```

**Rationale**: Demonstrates transformation from SEO anti-patterns to best practices

### Example 3: E-commerce Product Pages
**Context**: 500 product pages with duplicate content issues

**Input:**
```
Problem: Multiple URLs for same product
- example.com/products/laptop-123
- example.com/products/laptop-123?color=black
- example.com/products/laptop-123?utm_source=email

All have identical content, causing duplicate content issues
```

**Execution Flow:**
1. **Canonicalization**: Add canonical link to all variants
   ```html
   <link rel="canonical" href="https://example.com/products/laptop-123" />
   ```
2. **Image Optimization**: Add product-specific alt text
   ```html
   <img src="laptop.jpg" alt="15-inch gaming laptop with RGB keyboard and GeForce RTX 4080" />
   ```
3. **Unique Descriptions**: Write unique meta description per product
4. **Structured Data**: Add Product schema for rich results
   ```json
   {
     "@type": "Product",
     "name": "Gaming Laptop XZ-500",
     "description": "High-performance 15-inch gaming laptop",
     "offers": {
       "@type": "Offer",
       "price": "1299.99",
       "priceCurrency": "USD"
     }
   }
   ```

**Expected Output:**
- All product variants canonicalize to primary URL
- Each product has unique, descriptive title and meta description
- Product images have descriptive alt text (not just "product image")
- Structured data enables rich search results (price, reviews, availability)

**Rationale**: E-commerce sites particularly benefit from structured data and canonical URLs

## Quality Standards

### Output Requirements
- All pages must have unique `<title>` elements (100% compliance)
- All images must have descriptive `alt` attributes (100% compliance)
- URLs must contain meaningful words, not random IDs (100% compliance)
- Meta descriptions should be present on priority pages (90%+ coverage)
- No keyword stuffing in any content (zero tolerance)

### Performance Requirements
- Content quality audit: Complete within 2-3 hours for 50-page sites
- Metadata generation: <2 minutes per page
- Sitemap generation: <5 minutes for 1000-page sites

### Integration Requirements
- Works with static site generators (Jekyll, Hugo, Gatsby)
- Compatible with CMS platforms (WordPress, Drupal, custom systems)
- Integrates with Search Console API for automated monitoring

## Common Pitfalls

### Pitfall 1: Keyword Stuffing
**Issue**: Repeating keywords unnaturally to manipulate rankings
**Why it happens**: Misunderstanding of how modern search algorithms work
**Solution**:
- Write naturally for humans, not search engines
- Google's systems automatically handle keyword variations
- Keyword stuffing violates spam policies and harms rankings
- Focus on comprehensive, helpful content instead

### Pitfall 2: Duplicate Titles Across Pages
**Issue**: Using same title on multiple pages (e.g., "Welcome to Example.com")
**Why it happens**: Copy-paste during development, template issues
**Solution**:
```bash
# Audit for duplicate titles
grep -r "<title>" . | sort | uniq -d

# Each page needs unique title reflecting its specific content
# Bad: All pages use "<title>Example Docs</title>"
# Good: Each page has specific title like "Authentication | Example Docs"
```

### Pitfall 3: Missing or Generic Alt Text
**Issue**: Images without alt text or generic placeholders ("image", "photo")
**Why it happens**: Alt text seen as optional, not understanding its importance
**Solution**:
- Alt text improves accessibility (screen readers)
- Helps Google understand image context
- Contributes to image search rankings
- Write short, descriptive alt text for every meaningful image
- Decorative images can use empty alt (`alt=""`) but content images need description

### Pitfall 4: Blocking CSS/JS from Crawlers
**Issue**: robots.txt blocks stylesheets or JavaScript, preventing proper page rendering
**Why it happens**: Overcautious robots.txt configuration
**Solution**:
```
# Bad - blocks critical rendering resources
User-agent: *
Disallow: /css/
Disallow: /js/

# Good - allows CSS/JS, blocks actual private content
User-agent: *
Disallow: /admin/
Disallow: /private/
Allow: /css/
Allow: /js/
```

### Pitfall 5: Neglecting Mobile Experience
**Issue**: Poor mobile rendering affects rankings (mobile-first indexing)
**Why it happens**: Desktop-only testing, responsive design issues
**Solution**:
- Test with Mobile-Friendly Test tool
- Use responsive design
- Avoid intrusive interstitials on mobile
- Ensure text is readable without zooming

## Integration with Command & Control

### Related Agents
- **Scribe Agent**: Collaborates on documentation generation, applying SEO best practices to all generated content
- **Builder Agent**: Consults during web application development to ensure SEO-friendly architecture from start
- **Validator Agent**: Reviews HTML output for SEO compliance before deployment

### Related Commands
- `/docs`: Use SEO skill when generating documentation to ensure search discoverability
- `/prepare-pr`: Include SEO validation in pre-merge checklist for web content changes
- `/create-skill`: Reference as example of comprehensive skill documentation

### MCP Dependencies
None required for basic functionality. Optional integrations:
- **Search Console MCP**: Programmatic access to indexing status and search analytics
- **Sitemap Generator MCP**: Automated sitemap creation and submission

### Orchestration Notes
- **Chained with**: documentation-skill, content-writing-skill, accessibility-skill
- **Invoked by**: scribe-agent, builder-agent
- **Invokes**: None (leaf skill)

## Troubleshooting

### Issue: Pages Not Appearing in Search Results
**Symptoms**: Content exists but doesn't show in `site:` search
**Diagnosis**:
1. Check robots.txt isn't blocking crawlers
2. Verify robots meta tags aren't set to `noindex`
3. Check if page is linked from other indexed pages
4. Use URL Inspection Tool in Search Console
**Solution**:
- Ensure robots.txt allows crawling: `Allow: /`
- Remove/fix `noindex` directives if inappropriate
- Create internal links from homepage or sitemap
- Submit URL via Search Console for expedited indexing

### Issue: Title/Description Not Matching What Appears in Search
**Symptoms**: Google shows different title or description than your HTML
**Diagnosis**: Google may override titles/descriptions deemed unhelpful
**Solution**:
- Review title for keyword stuffing or manipulation
- Ensure title accurately describes page content
- Make titles unique and concise (under 60 characters)
- Write descriptive meta descriptions (under 160 characters)
- Google uses page content for snippets when meta description is missing/poor

### Issue: Duplicate Content Warnings
**Symptoms**: Search Console reports duplicate content issues
**Diagnosis**: Same content accessible via multiple URLs
**Solution**:
```html
<!-- Add canonical link to all duplicate versions -->
<link rel="canonical" href="https://example.com/preferred-url" />

<!-- Or implement 301 redirects -->
```
- Choose one canonical URL per content piece
- Use rel="canonical" on all variants
- Consider parameter handling in Search Console
- Implement 301 redirects when possible

### Issue: Images Not Appearing in Image Search
**Symptoms**: Images exist but don't show in Google Image Search
**Diagnosis**: Missing alt text, poor image quality, or blocked images
**Solution**:
- Add descriptive alt text to all images
- Use high-quality, sharp images (not blurry/pixelated)
- Place images near relevant text
- Ensure robots.txt doesn't block image files
- Submit image sitemap for large image collections

## Debunked SEO Myths

The following practices are **ineffective** or **harmful**:

### ❌ Keyword Meta Tags
- `<meta name="keywords">` is ignored by Google
- Has no ranking influence
- Remove or don't bother adding

### ❌ Domain Keywords
- Having keywords in domain name has minimal impact
- Content quality matters far more
- Don't rebrand for keyword-rich domain

### ❌ Content Length Alone
- Long content doesn't automatically rank higher
- Quality and usefulness matter more than word count
- Short, comprehensive content can outrank long, thin content

### ❌ Exact Match Keywords
- Google handles synonyms and variations automatically
- Writing naturally is better than forcing exact phrases
- Keyword stemming and semantic understanding are sophisticated

### ✅ Focus Instead On:
- People-first content
- Natural, helpful writing
- Technical best practices (this skill)
- User experience
- Expertise and authority

## Version History
- 1.0.0 (2026-01-22): Initial release
  - Comprehensive SEO guidance from Google's official starter guide
  - URL structure, metadata, content quality workflows
  - Image optimization and link best practices
  - Technical implementation examples
  - Common pitfalls and troubleshooting
  - Integration with Command & Control system
