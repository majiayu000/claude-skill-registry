---
name: nuxt-seo
description: |
  Comprehensive guide for all 8 Nuxt SEO modules plus Pro modules: @nuxtjs/seo, nuxt-robots, nuxt-sitemap, nuxt-og-image, nuxt-schema-org, nuxt-link-checker, nuxt-seo-utils, nuxt-site-config, and Pro modules (AI Ready, Skew Protection, SEO Pro MCP). Use when building SEO-optimized Nuxt applications, implementing robots.txt and sitemaps, generating Open Graph images, adding Schema.org structured data, managing meta tags, checking links, configuring site-wide SEO settings, or implementing advanced SEO features like rendering modes, canonical URLs, Twitter Cards, and IndexNow.

  Keywords: nuxt-seo, nuxt, seo, nuxt 3, nuxt 4, nuxt seo, vue, vue 3, search engine optimization, @nuxtjs/seo, nuxt-robots, nuxt-sitemap, nuxt-og-image, nuxt-schema-org, nuxt-link-checker, nuxt-seo-utils, nuxt-site-config, robots.txt, sitemap, sitemap.xml, og image, open graph, social sharing, meta tags, schema.org, structured data, json-ld, canonical urls, breadcrumbs, bot detection, crawling, indexing, noindex, nofollow, xml sitemap, multiple sitemaps, sitemap index, dynamic sitemap, og image generation, satori, chromium rendering, vue templates, seo setup, seo configuration, meta management, social media preview, search optimization, link checking, broken links, site config, multi-language seo, i18n seo, sitemap not generated, robots.txt missing, og image not rendering, schema validation errors, duplicate meta tags, canonical url issues, sitemap index errors, twitter cards, indexnow, ssr, ssg, isr, rendering modes, rich results, useSeoMeta, useSchemaOrg, defineOgImage, url structure, meta robots, ai ready, llms.txt, skew protection, i18n multilanguage, hreflang, _i18nTransform, _sitemap, route rules, routeRules, enhanced titles, title template, fallback title, link checker rules, prerendering spa, hydration mismatch, crawler protection, getBotDetection, useBotDetection, 404 page, seo-friendly 404, inspection rules, absolute-site-urls, link-text, missing-hash, no-error-response, defineSitemapEventHandler, nitro hooks, sitemap:input, sitemap:resolved, nuxt-og-image:context, asSeoCollection, asSitemapCollection, asSchemaOrgCollection, nuxt content v3, content collections, nuxt ai ready, mcp server, content signals, og image templates, multi-sitemaps, chunked sitemap, image sitemap, video sitemap, zero runtime
license: MIT
metadata:
  version: 2.2.0
  last_updated: 2025-12-28
  module_versions:
    nuxtjs_seo: 3.3.0
    nuxt_robots: 5.6.7
    nuxt_sitemap: 7.5.0
    nuxt_og_image: 5.1.13
    nuxt_schema_org: 5.0.10
    nuxt_link_checker: 4.3.9
    nuxt_seo_utils: 7.0.19
    nuxt_site_config: 3.2.14
  nuxt_compatibility: ">=3.0.0"
  auto_trigger_scenarios:
    - Setting up SEO in Nuxt project
    - Configuring robots.txt or sitemap
    - Generating Open Graph images
    - Adding Schema.org structured data
    - Managing meta tags and social sharing
    - Checking and fixing broken links
    - Implementing site-wide SEO configuration
    - Implementing Twitter Cards or Open Graph
    - Setting up canonical URLs
    - Configuring rendering modes (SSR/SSG/ISR)
    - Using IndexNow for instant indexing
    - Implementing rich results with JSON-LD
    - Setting up multilanguage/i18n SEO
    - Configuring SEO route rules
    - Debugging hydration mismatches
    - Creating SEO-friendly 404 pages
    - Protecting from malicious crawlers
---

# Nuxt SEO - Complete Guide to All 8 SEO Modules + Pro Features

**Status**: Production Ready
**Last Updated**: 2025-12-28
**Dependencies**: Nuxt >=3.0.0
**Latest Versions**: See module versions table below

Use this skill when building SEO-optimized Nuxt applications with any combination of the 8 official Nuxt SEO modules plus advanced Pro modules. This skill covers the complete Nuxt SEO ecosystem maintained by Harlan Wilton, including comprehensive guides for rendering modes, JSON-LD, Twitter Cards, IndexNow, and more.

---

## Nuxt SEO Ecosystem Overview

Nuxt SEO consists of **8 core modules** plus **3 Pro modules** that work together seamlessly:

### Core Modules

| Module | Version | Purpose |
|--------|---------|---------|
| **@nuxtjs/seo** | v3.3.0 | Primary SEO module (installs all 8 modules as bundle) |
| **nuxt-robots** | v5.6.7 | Manages robots.txt and bot detection |
| **nuxt-sitemap** | v7.5.0 | Generates XML sitemaps with advanced features |
| **nuxt-og-image** | v5.1.13 | Creates Open Graph images via Vue templates |
| **nuxt-schema-org** | v5.0.10 | Builds Schema.org structured data graphs |
| **nuxt-link-checker** | v4.3.9 | Finds and fixes broken links |
| **nuxt-seo-utils** | v7.0.19 | SEO utilities for discoverability & shareability |
| **nuxt-site-config** | v3.2.14 | Centralized site configuration management |

### Pro Modules

| Module | Purpose |
|--------|---------|
| **nuxt-ai-ready** | Generate llms.txt for AI crawlers and LLM optimization |
| **nuxt-skew-protection** | Prevent version mismatches during deployments |
| **Nuxt SEO Pro MCP** | AI-powered SEO tools via Model Context Protocol |

**Requirements**: Nuxt v3 or v4

---

## Quick Start (5 Minutes)

### 1. Install Complete SEO Bundle

Install all 8 modules at once:

```bash
# Using Bun (primary)
bunx nuxi module add @nuxtjs/seo

# Using npm (backup)
npx nuxi module add @nuxtjs/seo

# Using pnpm (backup)
pnpm dlx nuxi module add @nuxtjs/seo
```

**Why this matters:**
- Installs all 8 modules with a single command
- Ensures compatible versions across modules
- Provides best-practice defaults automatically

### 2. Configure Site Settings

Add to `nuxt.config.ts`:

```typescript
export default defineNuxtConfig({
  modules: ['@nuxtjs/seo'],

  site: {
    url: 'https://example.com',
    name: 'My Awesome Site',
    description: 'Building amazing web experiences',
    defaultLocale: 'en'
  }
})
```

**CRITICAL:**
- Set `site.url` to production URL (required for sitemaps and canonical URLs)
- Use environment variable for multi-environment setups
- Set `defaultLocale` if using i18n

### 3. Restart and Verify

```bash
bun run dev
# or
npm run dev
```

Visit these URLs to verify:
- `http://localhost:3000/robots.txt` - Robots file
- `http://localhost:3000/sitemap.xml` - Sitemap

---

## Installation Options

### Option 1: Complete Bundle (Recommended)

```bash
bunx nuxi module add @nuxtjs/seo
# or: npx nuxi module add @nuxtjs/seo
```

Configuration:

```typescript
export default defineNuxtConfig({
  modules: ['@nuxtjs/seo']
})
```

### Option 2: Individual Modules

Install only what's needed:

```bash
# Bun
bunx nuxi module add nuxt-robots
bunx nuxi module add nuxt-sitemap
bunx nuxi module add nuxt-og-image

# npm
npx nuxi module add nuxt-robots
npx nuxi module add nuxt-sitemap
npx nuxi module add nuxt-og-image

# pnpm (backup)
pnpm dlx nuxi module add nuxt-robots
pnpm dlx nuxi module add nuxt-sitemap
pnpm dlx nuxi module add nuxt-og-image
```

Configuration:

```typescript
export default defineNuxtConfig({
  modules: [
    'nuxt-robots',
    'nuxt-sitemap',
    'nuxt-og-image'
  ]
})
```

---

## Module Overview (Brief)

The Nuxt SEO ecosystem consists of **8 specialized modules** that work together seamlessly. Each module serves a specific purpose and can be installed individually or as a complete bundle.

### Module 1: @nuxtjs/seo
Primary SEO module that installs all 8 modules as a bundle. Provides unified configuration through the `site` object and integrates with Nuxt Content for automatic SEO.

### Module 2: nuxt-robots
Manages robots.txt and bot detection. Controls which pages search engines can crawl with site-wide and page-level rules. Includes server-side and client-side bot detection.

### Module 3: nuxt-sitemap
Generates XML sitemaps automatically from routes with support for dynamic URLs, multiple sitemaps, media, and advanced optimization. Perfect for large sites with thousands of pages.

### Module 4: nuxt-og-image
Creates Open Graph images dynamically using Vue templates. Zero runtime overhead with Satori renderer or full CSS support with Chromium renderer.

### Module 5: nuxt-schema-org
Builds Schema.org structured data for enhanced search results with rich snippets, knowledge panels, and better SEO.

### Module 6: nuxt-link-checker
Finds and fixes links that may negatively affect SEO. Detects broken links, redirects, and issues during development and build.

### Module 7: nuxt-seo-utils
SEO utilities for discoverability and shareability including canonical URLs, breadcrumbs, app icons, and Open Graph automation.

### Module 8: nuxt-site-config
Centralized site configuration management for all SEO modules. Single source of truth for site-wide settings like URL, name, and locale.

**For complete module documentation with configurations, APIs, and examples:**  
Load `references/module-details.md` when you need:
- Detailed configuration options for a specific module
- Complete API documentation
- Code examples and usage patterns
- Module-specific troubleshooting
---

## Integration Patterns

### Basic Example

```typescript
// nuxt.config.ts - Complete SEO setup
export default defineNuxtConfig({
  modules: ['@nuxtjs/seo'],

  site: {
    url: 'https://example.com',
    name: 'My Awesome Site',
    defaultLocale: 'en'
  },

  robots: {
    disallow: ['/admin']
  },

  sitemap: {
    sitemaps: {
      blog: { sources: ['/api/__sitemap__/blog'] }
    }
  }
})
```

**For complete integration examples:**  
Load `references/common-patterns.md` when you need:
- Blog page SEO implementation
- E-commerce product page examples
- Multi-language SEO patterns
- Integration with Nuxt Content
## Critical Rules

### Always Do

✅ Set `site.url` in nuxt.config.ts (required for sitemaps and canonical URLs)
✅ Use environment variables for multi-environment setups
✅ Configure robots.txt to block admin/private pages
✅ Add Schema.org structured data to all important pages
✅ Generate OG images for social sharing
✅ Test all SEO features before deploying to production
✅ Submit sitemap to Google Search Console after deployment
✅ Enable link checker during development

### Never Do

❌ Forget to set `site.url` (breaks sitemaps and canonical URLs)
❌ Allow crawling of staging environments
❌ Skip Schema.org for key pages (products, articles, events)
❌ Deploy without testing OG images
❌ Use outdated module versions
❌ Ignore broken links found by link checker
❌ Forget to exclude admin/private routes from sitemap
❌ Use wrong rendering engine for OG images (Chromium vs Satori)

---

## Known Issues Prevention

This skill prevents **10** documented common SEO mistakes:

### Issue #1: Sitemap Not Generating

**Error**: `/sitemap.xml` returns 404
**Why It Happens**: Missing `site.url` configuration
**Prevention**: Always set `site.url` in nuxt.config.ts

### Issue #2: robots.txt Missing

**Error**: `/robots.txt` not accessible
**Why It Happens**: Module not installed or misconfigured
**Prevention**: Install `nuxt-robots` and set `site.url`

### Issue #3: OG Images Not Rendering

**Error**: `/__og-image__/og.png` returns error
**Why It Happens**: Incompatible CSS with Satori renderer
**Prevention**: Use Satori-compatible CSS or switch to Chromium renderer

### Issue #4: Schema Validation Errors

**Error**: Invalid JSON-LD in page source
**Why It Happens**: Incorrect Schema.org structure
**Prevention**: Follow official Schema.org types and validate with Google's Rich Results Test

### Issue #5: Broken Internal Links

**Error**: 404 errors on internal links
**Why It Happens**: Links not updated after route changes
**Prevention**: Enable `nuxt-link-checker` during development

### Issue #6: Duplicate Meta Tags

**Error**: Multiple meta tags with same property
**Why It Happens**: Conflicting manual meta tags and module automation
**Prevention**: Let modules handle meta tags automatically

### Issue #7: Canonical URL Issues

**Error**: Wrong canonical URL in meta tags
**Why It Happens**: Incorrect `site.url` or missing trailing slash config
**Prevention**: Configure `site.url` and `trailingSlash` correctly

### Issue #8: Sitemap Index Errors

**Error**: Sitemap index XML malformed
**Why It Happens**: Too many URLs in single sitemap
**Prevention**: Use `chunksSize` option to split large sitemaps

### Issue #9: Crawling Staging Environment

**Error**: Staging site indexed by Google
**Why It Happens**: No robots.txt blocking
**Prevention**: Configure robots to block staging: `disallow: process.env.NUXT_PUBLIC_ENV === 'staging' ? ['/'] : []`

### Issue #10: Missing Social Sharing Images

**Error**: No preview image when sharing on social media
**Why It Happens**: OG image not defined or not accessible
**Prevention**: Use `defineOgImage()` on all important pages

---

## Configuration Example

### Basic Production Config

```typescript
export default defineNuxtConfig({
  modules: ['@nuxtjs/seo'],

  site: {
    url: process.env.NUXT_PUBLIC_SITE_URL,
    name: 'My Site',
    defaultLocale: 'en'
  },

  robots: {
    disallow: process.env.NUXT_PUBLIC_ENV === 'staging' ? ['/'] : []
  },

  sitemap: {
    sitemaps: {
      blog: { sources: ['/api/__sitemap__/blog'] }
    }
  }
})
```

**For complete configuration examples:**  
Load `references/advanced-configuration.md` when you need:
- Production-ready multi-environment setup
- Development and staging configurations
- Advanced sitemap patterns
- Dynamic route rules
- Multi-language configuration
## Using Bundled Resources

### Scripts (scripts/)

**`init-nuxt-seo.sh`** - Quick setup script for new projects

```bash
./scripts/init-nuxt-seo.sh
```

Automatically:
- Installs @nuxtjs/seo module
- Creates basic nuxt.config.ts configuration
- Sets up example OG image component
- Creates sitemap API endpoint example

### References (references/)

#### When to Load References

Load the appropriate reference file based on the user's specific needs:

**Load `references/seo-guides.md` when:**
- User asks about rendering modes (SSR, SSG, ISR, Hybrid)
- Need JSON-LD structured data implementation
- Setting up canonical URLs
- Implementing Twitter Cards or Open Graph
- Configuring meta robots tags
- Using IndexNow for instant indexing
- URL structure best practices
- Debugging SEO issues
- Rich results implementation

**Load `references/pro-modules.md` when:**
- User asks about AI optimization (llms.txt)
- Need deployment version skew protection
- Setting up MCP tools for AI-assisted SEO
- Advanced Pro module features

**Load `references/advanced-seo-guides.md` when:**
- User asks about I18n/multilanguage SEO
- Need hreflang or locale-specific sitemaps
- Configuring SEO route rules (routeRules)
- Enhanced title configuration (templates, fallbacks)
- Deep dive into nuxt-seo-utils features
- Link checker inspection rules
- Prerendering Vue SPA for SEO
- Hydration mismatch debugging
- Protecting from malicious crawlers/bots
- Creating SEO-friendly 404 pages

**Load `references/modules-overview.md` when:**
- User asks "what modules are available?" or "which module should I use?"
- Need overview of module capabilities and use cases
- Comparing modules to choose the right one
- Understanding how modules work together

**Load `references/installation-guide.md` when:**
- User is setting up Nuxt SEO for the first time
- Package manager specific questions (Bun vs npm vs pnpm)
- Installation troubleshooting or dependency conflicts
- Need step-by-step installation instructions

**Load `references/api-reference.md` when:**
- User asks about specific composable APIs (e.g., "how to use useSchemaOrg?")
- Need complete parameter lists or return types
- Troubleshooting API method signatures
- Looking for specific configuration options

**Load `references/common-patterns.md` when:**
- User wants real-world implementation examples
- Need blog, e-commerce, or multi-language SEO patterns
- Integrating with Nuxt Content or other modules
- Production-ready configuration examples

**Load `references/module-details.md` when:**
- User asks about specific module configuration
- Need detailed documentation for one of the 8 modules
- Troubleshooting module-specific issues

**Load `references/best-practices.md` when:**
- Setting up production SEO configuration
- Need SEO optimization guidelines
- Following Nuxt SEO best practices

**Load `references/troubleshooting.md` when:**
- User experiencing specific errors
- Sitemap, robots.txt, or OG image issues
- Build problems or module conflicts

**Load `references/advanced-configuration.md` when:**
- Need production-ready configurations
- Multi-environment setup (dev/staging/production)
- Advanced features (multiple sitemaps, custom OG templates)

**Load `references/og-image-guide.md` when:**
- User asks about OG image generation, Satori vs Chromium
- Need custom OG image templates or Vue components
- Configuring fonts, emojis, or caching for OG images
- Troubleshooting OG image rendering issues
- Implementing custom props or dynamic OG images

**Load `references/nuxt-content-integration.md` when:**
- User is using @nuxt/content with SEO modules
- Need asSeoCollection, asSitemapCollection, asSchemaOrgCollection patterns
- Content v2 vs v3 integration differences
- Module load order issues with content
- Automatic SEO from content frontmatter

**Load `references/sitemap-advanced.md` when:**
- User needs dynamic sitemap URLs from API/database
- Implementing multi-sitemaps with chunking
- Image or video sitemaps
- I18n sitemap with _i18nTransform
- Performance optimization (caching, zero runtime)
- defineSitemapEventHandler patterns

**Load `references/nitro-api-reference.md` when:**
- User needs server-side SEO hooks
- Implementing sitemap:input, sitemap:resolved, sitemap:output hooks
- OG image hooks (nuxt-og-image:context, nuxt-og-image:satori:vnodes)
- Robots composables (getSiteRobotConfig, getPathRobotConfig)
- Nitro plugin integration for SEO

**Load `references/ai-seo-tools.md` when:**
- User asks about llms.txt or AI discoverability
- Implementing Nuxt AI Ready module
- MCP server for AI-powered SEO
- Content signals for AI crawlers
- LLM optimization techniques

**Available references:**
- `references/seo-guides.md` - Comprehensive SEO implementation guides (rendering, JSON-LD, canonical URLs, IndexNow, Twitter Cards, Open Graph, meta robots, URL structure)
- `references/pro-modules.md` - Pro modules (AI Ready, Skew Protection, SEO Pro MCP)
- `references/advanced-seo-guides.md` - Advanced SEO topics (I18n multilanguage, route rules, enhanced titles, link checker rules, SPA prerendering, hydration, crawler protection, 404 pages)
- `references/og-image-guide.md` - OG image generation (Satori/Chromium, fonts, emojis, caching, custom templates)
- `references/nuxt-content-integration.md` - Nuxt Content v2/v3 integration (asSeoCollection, module order, auto-SEO)
- `references/sitemap-advanced.md` - Advanced sitemap patterns (dynamic URLs, multi-sitemaps, chunking, i18n, performance)
- `references/nitro-api-reference.md` - Server-side SEO hooks and composables (Nitro plugins, sitemap hooks, robots composables)
- `references/ai-seo-tools.md` - AI SEO tools (llms.txt, Nuxt AI Ready, MCP, content signals)
- `references/modules-overview.md` - Detailed overview of all 8 core modules
- `references/installation-guide.md` - Step-by-step installation patterns
- `references/api-reference.md` - Complete API documentation for all composables
- `references/common-patterns.md` - Real-world usage patterns and examples
- `references/module-details.md` - Detailed module configurations
- `references/best-practices.md` - Production SEO best practices
- `references/troubleshooting.md` - Error resolution guides
- `references/advanced-configuration.md` - Advanced configuration patterns

### Assets (assets/)

- `assets/package-versions.json` - Current module versions for verification

### Agents (agents/)

Autonomous agents for complex SEO tasks:

| Agent | Purpose |
|-------|---------|
| `seo-auditor.md` | Comprehensive SEO audit of Nuxt projects |
| `schema-generator.md` | Generate Schema.org structured data |
| `og-image-generator.md` | Create custom OG image Vue templates |
| `link-checker.md` | Analyze internal/external links |
| `sitemap-builder.md` | Design optimal sitemap strategies |

### Commands (commands/)

Slash commands for quick SEO tasks:

| Command | Purpose |
|---------|---------|
| `/seo-audit` | Run comprehensive SEO audit |
| `/seo-setup` | Quick Nuxt SEO project setup |
| `/og-preview` | Preview OG image generation |
| `/check-links` | Run link checker analysis |
| `/validate-sitemap` | Validate sitemap configuration |
| `/check-schema` | Validate Schema.org implementation |

### Hooks (hooks/)

SEO validation hooks that run automatically:

| Hook | Event | Purpose |
|------|-------|---------|
| SEO Config Validator | PreToolUse | Validates SEO configuration in file edits |
| Post-Write Checker | PostToolUse | Checks SEO config after file writes |
| Completion Validator | Stop | Ensures SEO validation before task completion |
| Project Detector | SessionStart | Detects Nuxt SEO modules on session start |

---

## Best Practices

### Top 3 Critical Practices

**1. Always Set Site Config**
```typescript
site: {
  url: process.env.NUXT_PUBLIC_SITE_URL,
  name: 'Your Site Name'
}
```

**2. Block Staging from Search Engines**
```typescript
robots: {
  disallow: process.env.NUXT_PUBLIC_ENV === 'staging' ? ['/'] : []
}
```

**3. Add Schema.org to All Pages**
Every page should have appropriate structured data (Organization, BlogPosting, Product, etc.).

**For complete best practices guide:**  
Load `references/best-practices.md` when you need:
- All 8 SEO best practices
- Environment variable configuration
- Dynamic sitemap generation
- OG image optimization
- Multi-language SEO setup
## Troubleshooting

### Top 3 Common Issues

**1. Sitemap Not Generating**
- Ensure `nuxt-sitemap` is installed
- Set `site.url` in config  
- Restart dev server and visit `/sitemap.xml`

**2. OG Images Not Rendering**
- Check if `nuxt-og-image` is installed
- Verify fonts are accessible
- For complex layouts, switch to Chromium renderer

**3. Build Errors**
- Update all modules to latest versions
- Clear `.nuxt` and `node_modules/.cache`
- Reinstall: `rm -rf node_modules && bun install`

**For complete troubleshooting guide:**  
Load `references/troubleshooting.md` when you need:
- Detailed solutions for all 5 common problems
- Advanced debugging techniques
- Module-specific error resolution
- Build and deployment issues
## Package Versions (Verified 2025-12-28)

```json
{
  "dependencies": {
    "@nuxtjs/seo": "^3.3.0",
    "nuxt-robots": "^5.6.7",
    "nuxt-sitemap": "^7.5.0",
    "nuxt-og-image": "^5.1.13",
    "nuxt-schema-org": "^5.0.10",
    "nuxt-link-checker": "^4.3.9",
    "nuxt-seo-utils": "^7.0.19",
    "nuxt-site-config": "^3.2.14"
  }
}
```

---

## Complete Setup Checklist

Use this checklist to verify setup:

- [ ] Installed @nuxtjs/seo or individual modules
- [ ] Set `site.url` in nuxt.config.ts
- [ ] Configured `site.name` and `site.description`
- [ ] Set `defaultLocale` if using i18n
- [ ] Configured robots.txt to block admin/private pages
- [ ] Configured staging environment to block all crawling
- [ ] Created dynamic sitemap endpoints for content
- [ ] Added OG image to important pages
- [ ] Added Schema.org structured data to key pages
- [ ] Enabled link checker in development
- [ ] Tested `/robots.txt` endpoint
- [ ] Tested `/sitemap.xml` endpoint
- [ ] Verified OG images render correctly
- [ ] Submitted sitemap to Google Search Console
- [ ] Production build succeeds without errors

---

## Official Documentation

- **Nuxt SEO**: https://nuxtseo.com
- **@nuxtjs/seo**: https://nuxtseo.com/nuxt-seo/getting-started/installation
- **nuxt-robots**: https://nuxtseo.com/robots/getting-started/installation
- **nuxt-sitemap**: https://nuxtseo.com/sitemap/getting-started/installation
- **nuxt-og-image**: https://nuxtseo.com/og-image/getting-started/installation
- **nuxt-schema-org**: https://nuxtseo.com/schema-org/getting-started/installation
- **nuxt-link-checker**: https://nuxtseo.com/link-checker/getting-started/installation
- **GitHub**: https://github.com/harlan-zw

---

**Production Ready**: All patterns based on official documentation from https://nuxtseo.com/llms.txt | Last verified: 2025-12-28

---

## Version History

**v2.2.0** (2025-12-28)
- Full expansion with comprehensive coverage of all topics from nuxtseo.com/llms.txt
- Added 5 new reference files:
  - `references/og-image-guide.md` - Complete OG image guide (Satori/Chromium, fonts, emojis, caching)
  - `references/nuxt-content-integration.md` - Nuxt Content v2/v3 integration patterns
  - `references/sitemap-advanced.md` - Advanced sitemap patterns (dynamic URLs, multi-sitemaps, chunking)
  - `references/nitro-api-reference.md` - Server-side SEO hooks and composables
  - `references/ai-seo-tools.md` - Nuxt AI Ready, llms.txt, MCP server, content signals
- Added 3 new agents:
  - `agents/og-image-generator.md` - Creates custom OG image Vue templates
  - `agents/link-checker.md` - Analyzes internal/external links
  - `agents/sitemap-builder.md` - Designs optimal sitemap strategies
- Added 4 new commands:
  - `/og-preview` - Preview OG image generation
  - `/check-links` - Run link checker analysis
  - `/validate-sitemap` - Validate sitemap configuration
  - `/check-schema` - Validate Schema.org implementation
- Added SEO validation hooks:
  - PreToolUse hook for SEO config validation
  - PostToolUse hook for post-write checks
  - Stop hook for completion validation
  - SessionStart hook for project detection
- Enhanced keywords with 20+ new terms for better discoverability
- Total: 16 reference files, 5 agents, 6 commands, 4 hooks

**v2.1.0** (2025-12-28)
- Added `references/advanced-seo-guides.md` with 9 advanced topics:
  - I18n Multilanguage SEO (robots + sitemap integration)
  - SEO Route Rules (routeRules configuration)
  - Enhanced Titles (templates, fallbacks)
  - Nuxt SEO Utils Deep Dive
  - Nuxt Link Checker Rules (14 inspection rules)
  - Prerendering Vue SPA for SEO
  - Hydration Mismatches (causes, fixes, SEO impact)
  - Protecting from Malicious Crawlers
  - SEO-Friendly 404 Pages
- Added 5 new auto-trigger scenarios
- Enhanced keywords with 25+ new terms

**v2.0.0** (2025-12-28)
- Major update with comprehensive SEO guides and Pro modules
- Added `references/seo-guides.md` - Complete SEO implementation guides:
  - Rendering modes (SSR, SSG, ISR, Hybrid)
  - JSON-LD Structured Data
  - Canonical URLs
  - IndexNow & Indexing APIs
  - Twitter Cards
  - Social Sharing & Open Graph
  - Meta Robots Tags
  - URL Structure Best Practices
  - Rich Results
  - Debugging Vue SEO Issues
- Added `references/pro-modules.md` - Pro module documentation:
  - Nuxt AI Ready (llms.txt generation)
  - Nuxt Skew Protection (deployment version safety)
  - Nuxt SEO Pro MCP (AI-powered SEO tools)
- Created `agents/seo-auditor.md` - Autonomous SEO audit agent
- Created `agents/schema-generator.md` - Schema.org code generator
- Created `commands/seo-audit.md` - SEO audit slash command
- Created `commands/seo-setup.md` - Quick SEO setup command
- Updated all package versions to latest (2025-12-28)
- Enhanced keywords for better skill discovery
- Added 5 new auto-trigger scenarios

**v1.1.0** (2025-11-27)
- Refactored SKILL.md from 1505 to 628 lines (58% reduction)
- Extracted module details to references/module-details.md
- Extracted best practices to references/best-practices.md
- Extracted troubleshooting to references/troubleshooting.md
- Extracted advanced config to references/advanced-configuration.md
- Added "When to Load References" section for progressive disclosure
- Added TOCs to all 8 reference files
- All content preserved, just reorganized for optimal token efficiency
- Phases 6-7, 13-14 complete per skill-review process

**v1.0.0** (2025-11-10)
- Initial release
- Complete documentation for all 8 Nuxt SEO modules
- 10 documented error patterns
- Production-tested patterns
