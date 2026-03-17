---
name: nuxt-sanity
description: >-
  @nuxtjs/sanity module integration best practices for Nuxt 3 apps connected
  to Sanity CMS. Covers useSanityQuery, useLazySanityQuery, useSanity,
  SanityImage, SanityContent (Portable Text), visual editing / live preview
  with stega, TypeScript typegen, named clients, and Nitro server routes.
  Use when the user mentions @nuxtjs/sanity, nuxt-sanity, useSanityQuery,
  SanityImage in Nuxt, or is building a Nuxt app that fetches data from Sanity.
---

# Nuxt + Sanity Integration Best Practices

Best-practices guide for the `@nuxtjs/sanity` module (Nuxt 3). Covers module
setup, composables, SSR data fetching, image handling, Portable Text, visual
editing, TypeScript, and Nitro server routes.

> Also load the `nuxt` skill for Nuxt core patterns and `sanity-best-practices`
> for GROQ query optimization and schema design. This skill covers the
> integration layer only.

## ROUTING: Which rule file to load

**IF setting up the module or configuring nuxt.config.ts:**
→ Read `rules/core-module-setup.md`

**IF using useSanityQuery, useLazySanityQuery, or useSanity composables:**
→ Read `rules/core-composables.md`

**IF writing Nitro server routes that query Sanity:**
→ Read `rules/core-server-routes.md`

**IF working with the SanityImage component or useSanityImage():**
→ Read `rules/features-sanity-image.md`

**IF rendering Portable Text with SanityContent:**
→ Read `rules/features-sanity-content.md`

**IF implementing visual editing, live preview, stega, or the Presentation tool:**
→ Read `rules/features-visual-editing.md`

**IF experiencing stale data, cache misses, or reactive query bugs:**
→ Read `rules/perf-query-keys-and-caching.md`

**IF debugging CORS errors, auth token issues, or hydration mismatches:**
→ Read `rules/debug-common-errors.md`

**IF generating a dynamic sitemap from Sanity routes (works, case studies, etc.):**
→ Read `rules/features-sitemap.md`

## Rule index

| Topic | Description | File |
|-------|-------------|------|
| Sections overview | Categories and reading order | [rules/_sections.md](rules/_sections.md) |
| Module setup | Installation, nuxt.config.ts options, env vars | [rules/core-module-setup.md](rules/core-module-setup.md) |
| Composables | useSanityQuery, useLazySanityQuery, useSanity usage | [rules/core-composables.md](rules/core-composables.md) |
| Server routes | Nitro server routes with useSanity, validateSanityQuery | [rules/core-server-routes.md](rules/core-server-routes.md) |
| SanityImage | SanityImage component, useSanityImage(), @nuxt/image integration | [rules/features-sanity-image.md](rules/features-sanity-image.md) |
| SanityContent | Portable Text rendering, custom components | [rules/features-sanity-content.md](rules/features-sanity-content.md) |
| Visual editing | Stega, live preview, Presentation tool, draft mode | [rules/features-visual-editing.md](rules/features-visual-editing.md) |
| Caching | Query key stability, reactive params, cache invalidation | [rules/perf-query-keys-and-caching.md](rules/perf-query-keys-and-caching.md) |
| Debug | CORS, auth tokens, hydration errors, common pitfalls | [rules/debug-common-errors.md](rules/debug-common-errors.md) |
| Sitemap | Dynamic sitemap sources, defineSitemapEventHandler, stegaClean on slugs | [rules/features-sitemap.md](rules/features-sitemap.md) |

## Rule categories by priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Module setup & composables | CRITICAL | `core-` |
| 2 | Server routes | HIGH | `core-` |
| 3 | Visual editing | HIGH | `features-` |
| 4 | Image & Portable Text | HIGH | `features-` |
| 5 | Caching & performance | MEDIUM-HIGH | `perf-` |
| 6 | Debug | MEDIUM | `debug-` |

## Coverage and maintenance

- Coverage map: `rules/_coverage-map.md`
- Module source: https://github.com/nuxt-modules/sanity
- Update when `@nuxtjs/sanity` releases a new major version or visual editing APIs change.
