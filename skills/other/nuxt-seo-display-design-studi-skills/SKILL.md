---
name: nuxt-seo
description: >-
  @nuxtjs/robots module best practices for Nuxt 3 apps — robots.txt generation,
  crawl control, noindex per page, route-rule blocking, AI bot blocking, and
  environment-based indexing. Also covers llms.txt for AI-tool documentation
  access. Use when the user mentions @nuxtjs/robots, robots.txt, crawl,
  indexing, noindex, disallow, blockAiBots, or llms.txt in a Nuxt project.
---

# Nuxt SEO — @nuxtjs/robots & llms.txt

Best-practices guide for `@nuxtjs/robots` (part of the `nuxt-seo` suite) and
`llms.txt` integration in Nuxt 3.

> Also load the `nuxt` skill for Nuxt core patterns.

## ROUTING: Which rule file to load

**IF setting up @nuxtjs/robots or configuring robots.txt for the first time:**
→ Read `rules/core-robots-setup.md`

**IF controlling crawling per page, route, or dynamically at runtime:**
→ Read `rules/features-page-control.md`

**IF adding or referencing llms.txt for AI tool documentation access:**
→ Read `rules/features-llms-txt.md`

## Rule index

| Topic | Description | File |
|-------|-------------|------|
| Sections overview | Categories and reading order | [rules/_sections.md](rules/_sections.md) |
| Robots setup | Installation, nuxt.config.ts, disallow, blockNonSeoBots, blockAiBots | [rules/core-robots-setup.md](rules/core-robots-setup.md) |
| Page control | definePageMeta, route rules, useRobotsRule composable, X-Robots-Tag | [rules/features-page-control.md](rules/features-page-control.md) |
| llms.txt | Standard, manual public/ file, nuxtseo.com docs for AI tools | [rules/features-llms-txt.md](rules/features-llms-txt.md) |

## Rule categories by priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Module setup | CRITICAL | `core-` |
| 2 | Page-level crawl control | HIGH | `features-` |
| 3 | llms.txt | MEDIUM | `features-` |

## Coverage and maintenance

- Coverage map: `rules/_coverage-map.md`
- Module source: https://github.com/harlan-zw/nuxt-robots
- Docs: https://nuxtseo.com/robots
- Update when `@nuxtjs/robots` releases a new major version.
