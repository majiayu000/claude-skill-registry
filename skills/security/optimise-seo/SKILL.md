---
name: optimise-seo
description: 'Use when asked to make a Next.js App Router app crawlable, indexable, and search-optimized for sitemaps, robots, canonicals, and Core Web Vitals. Not for security headers or remote mutations.'
---

# Optimise SEO

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Improve SEO, Next.js SEO, sitemap, robots, meta tags, structured data, canonical URL, hreflang, Core Web Vitals, crawlability, indexability. |
| Authority | Reversible local: writes only named local project source files (App Router pages and layouts, `app/sitemap.ts`, `app/robots.ts`, `app/manifest.ts`, `next.config.ts`, JSON-LD components, `public/` assets); rollback is version control or restoring recorded prior content. No remote mutation. Audit-only mode reads a deployed origin without editing files. |
| Side effect | Applies or recommends SEO and technical changes within the named scope. No visual redesigns, component styling, or layout changes; no content rewriting; no security-header configuration; llms.txt and AI-agent readability are out of scope. |
| Done | A pass or fail checklist with per-check command evidence: build, curl header and meta checks, and Lighthouse. Each item is marked pass with evidence or fail with a named blocker. Done does not require green Core Web Vitals when external gates are unreachable; those items are marked blocked. |

## Inputs

Required: the repo root of the Next.js App Router app to change (edit mode), or a deployed origin URL (audit-only mode); the canonical production host (apex or www).
Optional: the locale list (multi-locale steps are skipped without it); which routes are staging, admin, thin, or private; which findings to apply versus only recommend.

With neither a repo nor an origin URL, stop without running.

## Procedure

1. **Bound scope and route indexing policies.** Determine the mode: edit (repo root provided) or audit-only (deployed origin only). Enumerate routes and decide index intent for each: public routes default to `index, follow`; staging, admin, thin, and private routes get explicit `noindex` (`metadata.robots` for HTML routes; `X-Robots-Tag` headers for non-HTML or whole staging environments). Record the decision per route; do not touch styling or layout. A thin page is `noindex`ed and omitted from the sitemap until it carries unique content, then indexed and linked internally. Done when: every route has a recorded index intent, the mode is confirmed, and no styling or layout is touched.

2. **Configure crawl foundations.** In edit mode, write or update: `app/sitemap.ts` listing every public URL as absolute URLs with `lastModified` derived from the freshest content date (never hardcoded); above 50,000 URLs, export `generateSitemaps()` for a sitemap index. `app/robots.ts` allowing `/`, disallowing private paths, and linking the sitemap URL. Canonicals: pick one host, one casing, one trailing-slash policy; set `alternates.canonical` on every page; 308-redirect the non-canonical host unless the platform already edge-redirects. Redirects: permanent moves use 301 or 308, temporary use 302 or 307, pointing straight at the final URL, never chained. Status codes: a missing page returns a real 404 (a 200 with a friendly message is a soft 404); maintenance windows return 503 with `Retry-After`. In audit-only mode, verify these with curl against the deployed origin. Done when: sitemap, robots, canonicals, redirects, and status codes are all configured (edit) or verified (audit-only) per the above rules.

3. **Configure metadata and structured data.** In edit mode, write or update: unique title (50 to 60 chars) and unique description (150 to 160 chars) per page via static `metadata` or `generateMetadata`. OpenGraph and Twitter Card tags on every page with a 1200x630 image. Favicons: `favicon.ico`, `icon.svg`, `apple-touch-icon.png`. JSON-LD through one `JsonLd` script component: define each entity once with a stable `@id` (for example `https://<host>/#organization`, `/#website`, `/#person`) inside a single `@graph` emitted from the root layout or homepage; per-page schema references entities by `@id` instead of duplicating them inline. Homepage: `Organization` (with `logo`) and `WebSite`. Inner pages: `BreadcrumbList`. Where the content type matches: `Article` or `BlogPosting` (author is the `Person` `@id`, publisher is the `Organization` `@id`), `Product`, `FAQPage`; `ProfilePage` on identity pages. Fill recommended fields, not only required ones. In audit-only mode, verify with curl. Done when: unique titles and descriptions, OpenGraph and Twitter Card tags with favicons, and JSON-LD with stable `@id` entities are all in place (edit) or verified (audit-only).

4. **Enforce semantics, internal linking, and CWV budgets.** In edit mode: one h1 per page with a logical h2 to h6 hierarchy; descriptive alt text on all images; internal links between related pages; every indexable page reachable from navigation, footer, or the sitemap (orphans get a crawl path or are `noindex`ed and dropped from the sitemap). CWV targets: LCP below 2.5s (hero image with `priority`), INP below 200ms, CLS below 0.1 (width and height on all media), TTFB below 600ms. Recompress oversized `public/` images in place, keeping filenames and formats so references stay valid. Do not move indexable content behind a client-only render. For multi-locale sites (when the locale list is provided): pick one URL pattern for all locales (subdirectory by default), declare `hreflang` with BCP 47 codes reciprocally (every alternate lists every other alternate including itself, plus a self-reference and `x-default`), translate everything in the head and structured data per locale, and never auto-redirect locale by IP geolocation. In audit-only mode, verify with curl and Lighthouse. Done when: semantics, internal linking, CWV budgets, and hreflang (when applicable) are configured (edit) or verified (audit-only).

5. **Execute evidence-based validation.** Run each check and mark pass or fail with command output:

   | Check | Command | Expected |
   |---|---|---|
   | Production build | `pnpm run build` (or the repository build command) | exits 0 |
   | Response headers | `curl -sI <url>` | correct status, redirects, canonical host |
   | Served HTML metadata | `curl -s <url>` piped to `grep -F -e canonical -e "og:" -e "twitter:" -e "application/ld+json"` | tags present in the served source |
   | Robots | `curl -s <origin>/robots.txt` | expected allow and disallow and sitemap link |
   | Sitemap | `curl -s <origin>/sitemap.xml` | indexed routes, absolute URLs, fresh `lastmod` |
   | Lighthouse | `pnpm dlx lighthouse <url> --only-categories=seo,performance --output=json` | SEO and Performance scores, or blockers listed |

   External gates (Rich Results Test, Search Console) may be unreachable from the skill's environment. Mark those items as blocked with the exact reason; do not fabricate or estimate metrics. Done when: every check is marked pass with command evidence, fail with a named blocker, or blocked with the exact reason. Done does not require green Core Web Vitals when the Lighthouse or external gates are unreachable; those items are blocked, not failed.

## Failure and recovery

- Build failure after an edit: restore that file's recorded prior content; never leave the production build red. Rollback is restoring the recorded prior content or the VCS state of the touched files.
- Missing deployed origin for audit-only: the origin URL is required for audit-only mode. If it is missing or unreachable, mark the audit-only checks as blocked with the exact reason.
- External search gates unreachable: Rich Results Test and Search Console require browser access or post-deploy verification. Mark these as blocked with the exact reason; do not claim Done while pretending they passed.
- Findings conflict: apply the indexing policy, `noindex` plus removal from the sitemap, and record the decision; do not widen into rewriting content or redesigning pages.
- A live hreflang set is not reciprocal: fix reciprocity before shipping; search engines ignore non-mutual sets, so a partial set must not ship.
- Blockers remain: the terminal result is a blocker list with exact URLs and owner or action per item; Done is never declared with failing or missing evidence.

## Output

A completed pass or fail checklist with per-check command evidence, the list of applied file changes each with recorded prior content for rollback (edit mode), a recommendation-only list for findings not applied, and remaining blockers with exact URLs and owner or action. Done is claimed only when every checklist item is pass, fail with a named blocker, or blocked with an exact reason.
