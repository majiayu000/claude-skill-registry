---
name: google-official-seo-guide
description: Official Google SEO guide covering search optimization, best practices, Search Console, crawling, indexing, and improving website search visibility based on official Google documentation
---

# Google Official SEO Guide

Comprehensive assistance with Google Search optimization, SEO best practices, and search visibility improvements based on official Google documentation.

## When to Use This Skill

This skill should be triggered when users ask about:

### SEO & Search Optimization
- Improving website ranking in Google Search
- Implementing SEO best practices
- Optimizing meta tags, titles, and descriptions
- Fixing crawling or indexing issues
- Understanding how Google Search works

### Structured Data & Rich Results
- Adding VideoObject, BroadcastEvent, or Clip structured data
- Implementing schema.org markup for rich results
- Creating sitemaps and robots.txt files
- Setting up breadcrumb navigation
- Configuring hreflang for multi-language sites

### Technical SEO
- Mobile-first indexing optimization
- JavaScript SEO and rendering issues
- Managing duplicate content with canonical tags
- Configuring robots meta tags
- URL structure and internal linking

### Search Console & Monitoring
- Using Google Search Console reports
- Debugging search visibility issues
- Monitoring crawl errors and indexing status
- Analyzing search performance metrics

### Content & Links
- Writing effective anchor text
- Internal and external linking strategies
- Avoiding spam policies violations
- Managing site migrations and redirects

## Key Concepts

### The Three Stages of Google Search
1. **Crawling**: Googlebot discovers and fetches pages from the web
2. **Indexing**: Google analyzes page content and stores it in the index
3. **Serving**: Google returns relevant results for user queries

### Important SEO Principles
- **Mobile-First Indexing**: Google primarily uses the mobile version of content for indexing and ranking
- **Canonical URLs**: Specify the preferred version of duplicate or similar pages
- **Structured Data**: Use schema.org markup to help Google understand your content
- **Search Essentials**: Technical, content, and spam requirements for Google Search eligibility

### Common Structured Data Types
- **VideoObject**: For video content and features
- **BroadcastEvent**: For livestream videos (LIVE badge)
- **Clip**: For video key moments/timestamps
- **SeekToAction**: For auto-detected key moments in videos

## Quick Start Examples

### Basic VideoObject for Videos

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Video title",
  "description": "Video description",
  "thumbnailUrl": ["https://example.com/photo.jpg"],
  "uploadDate": "2024-03-31T08:00:00+08:00",
  "duration": "PT1M54S",
  "contentUrl": "https://example.com/video.mp4"
}
```

### LIVE Badge for Livestreams

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Livestream title",
  "publication": {
    "@type": "BroadcastEvent",
    "isLiveBroadcast": true,
    "startDate": "2024-10-27T14:00:00+00:00"
  }
}
```

### Crawlable Links

```html
<!-- ✅ Recommended -->
<a href="https://example.com">Link text</a>
<a href="/products/category">Link text</a>

<!-- ❌ Not recommended -->
<a routerLink="products/category">Link text</a>
<span href="https://example.com">Link text</span>
```

### Robots Meta Tags

```html
<!-- Don't index this page -->
<meta name="robots" content="noindex">

<!-- Don't follow links -->
<meta name="robots" content="nofollow">
```

**More examples**: `read references/examples.md`

## Reference Files

This skill includes comprehensive documentation organized into the following categories:

### Core Documentation

**apis.md** - Getting started with Google Search Console, monitoring tools, and APIs  
**appearance.md** - Visual elements and rich results in Google Search (58 pages)  
**crawling.md** - How Google discovers, crawls, and accesses web content  
**fundamentals.md** - Core concepts and essential SEO knowledge  
**guides.md** - Detailed how-to guides for specific SEO tasks  
**indexing.md** - How Google indexes content and troubleshooting indexing issues  
**other.md** - Additional topics, policies, and specialized information  
**specialty.md** - Structured data and specialized search features

### Usage Guides

**examples.md** - 10 detailed examples with code snippets  
**user-guide.md** - How to use this skill for different user levels  
**best-practices.md** - Common pitfalls, tips, and official tools

### When to Read Each File

- **Starting out**: fundamentals.md → guides.md → examples.md
- **Structured data**: specialty.md → examples.md
- **Technical issues**: crawling.md → indexing.md
- **Rich results**: appearance.md → specialty.md
- **Best practices**: best-practices.md

## Key Recommendations

### DO ✅
- Create unique, descriptive titles and meta descriptions
- Use meaningful heading structure (H1, H2, H3)
- Optimize images with descriptive alt text
- Submit and maintain XML sitemaps
- Use robots.txt for crawl control (not indexing)
- Implement canonical tags for duplicate content
- Test structured data with validation tools
- Monitor Search Console regularly

### DON'T ❌
- Keyword stuffing or hidden text
- Buy/sell links for ranking
- Different content on mobile vs desktop
- Block resources on mobile
- Use generic anchor text ("click here")
- Non-crawlable JavaScript-only links
- Cloaking (different content for Google vs users)

## Resources

### Official Tools
- **Google Search Console**: Monitor search presence
- **Rich Results Test**: Validate structured data
- **Mobile-Friendly Test**: Check mobile optimization
- **Page Speed Insights**: Analyze performance

### Documentation Access
All reference files preserve links to official Google resources. Use `read references/[filename].md` to access detailed documentation.

## References

**Examples & Code Snippets**: `read references/examples.md` (10 detailed examples)  
**User Guide**: `read references/user-guide.md` (for beginners, marketers, developers, advanced users)  
**Best Practices**: `read references/best-practices.md` (pitfalls, tips, tools)  

**Core Documentation**:
- `read references/apis.md` - Search Console setup
- `read references/appearance.md` - Rich results & visual elements
- `read references/crawling.md` - Googlebot & crawl optimization
- `read references/fundamentals.md` - SEO basics
- `read references/guides.md` - How-to guides
- `read references/indexing.md` - Index management
- `read references/other.md` - Policies & updates
- `read references/specialty.md` - Structured data details
