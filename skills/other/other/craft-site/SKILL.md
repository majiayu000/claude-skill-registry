---
name: craft-site
description: "Craft CMS 5 front-end Twig development — atomic design, template architecture, component patterns, Vite buildchain. Covers the full site template surface: atoms, molecules, organisms, props/extends/block pattern, layout chains, view routing, content builders, image presets, Tailwind named-key collections, multi-brand CSS tokens, JavaScript boundaries (Alpine/DataStar/Vue), Vite asset loading. Triggers on: {% include ... only %}, {% embed %}, _atoms/, _molecules/, _organisms/, _views/, _builders/, _boilerplate/, component--variant.twig, _component--props.twig, image presets, Tailwind class collections, collect({}), utilities prop, multi-brand theming, data-brand, hero sections, card components, content builders, Matrix block rendering, craft.vite.script, vite.php, vite.config.ts, nystudio107, buildchain, asset loading, per-page scripts. Always use when creating, editing, or reviewing any Craft CMS front-end Twig template, component, layout, view, builder, or buildchain configuration."
---

# Craft CMS 5 — Front-End Twig (Atomic Design)

Atomic design system patterns for Craft CMS 5 site templates. Vanilla Twig —
no module dependency. Works with any Craft 5 project.

This skill is scoped to **front-end template architecture** — component design,
routing, composition, theming, and buildchain. For extending Craft (plugins,
modules, PHP), see the `craftcms` skill. For Twig coding standards (naming,
null handling, whitespace, helpers), see `craft-twig-guidelines`. For PHP
standards, see `craft-php-guidelines`. For content architecture (sections,
fields, entry types), see `craft-content-modeling`.

## Documentation

- Twig in Craft: https://craftcms.com/docs/5.x/development/twig.html
- Template tags: https://craftcms.com/docs/5.x/reference/twig/tags.html
- Template functions: https://craftcms.com/docs/5.x/reference/twig/functions.html
- Twig 3 docs: https://twig.symfony.com/doc/3.x/

Use `web_fetch` on specific doc pages when a reference file doesn't cover enough detail.

## Common Pitfalls (Cross-Cutting)

- Missing `only` on `{% include %}` — ambient variables leak in silently.
- Variant logic via conditionals (`{% if variant == 'x' %}`) instead of extends/block.
- Naming atoms by parent context (`hero-button`) instead of visual treatment (`button--primary`).
- `utilities` prop used as override — it's additive. Override via named-slot merge.
- Queries inside views — views receive data, they don't fetch it.
- Missing `.eagerly()` on relation fields in views — causes N+1 queries.
- Missing `devMode` fallback in builders for unknown block types.
- Hardcoded Tailwind colors (`bg-yellow-600`) instead of brand tokens (`bg-brand-accent`).
- Mixing buttons and links — buttons are actions (resolve to `<a>`, `<button>`, or `<span>` from props), links are navigation (always `<a>`). Separate atom categories.
- Tracking/analytics inside components — decouple to data attributes at view/page level.

## Reference Files

Read the relevant reference file(s) for your task. Multiple files often apply together.

**Task examples:**
- "Build a new card component" → read `atomic-patterns.md` + `component-inventory.md` + `tailwind-conventions.md`
- "Set up a new project's template structure" → read `boilerplate-routing.md` + `component-inventory.md`
- "Add a content builder for a Matrix field" → read `boilerplate-routing.md` + `atomic-patterns.md`
- "Handle responsive images" → read `image-presets.md` + `plugins/image-optimize.md`
- "Add multi-brand theming" → read `tailwind-conventions.md`
- "Decide between Alpine and Vue for a feature" → read `javascript-boundaries.md`
- "Compose Tailwind classes without conflicts" → read `tailwind-conventions.md` + `twig-collections.md`
- "Understand atomic design methodology" → read `atomic-design.md`
- "Set up Vite + Tailwind in a new Craft project" → read `vite-buildchain.md`
- "Debug why assets aren't loading in production" → read `vite-buildchain.md`
- "Install GTM/analytics/CMP in a Craft project" → read `third-party-integration.md`
- "Configure SEOMatic for a section" → read `plugins/seomatic.md`
- "Set up Blitz caching with Cloudflare" → read `plugins/blitz.md`
- "Add a form to a page" → read `plugins/formie.md`
- "Configure CKEditor with nested entries" → read `plugins/ckeditor.md`
- "Build a navigation menu" → read `plugins/navigation.md`
- "Add a link field to a component" → read `plugins/hyper.md`
- "Set up redirects for a site" → read `plugins/retour.md`
- "Add recurring/repeating dates to entries" → read `plugins/timeloop.md`
- "Create a JSON API endpoint" → read `plugins/element-api.md`
- "Debug N+1 queries in templates" → read `plugins/elements-panel.md`
- "Run a security audit" → read `plugins/sherlock.md`
- "Embed a YouTube/Vimeo video as an asset" → read `plugins/embedded-assets.md`
- "Configure email delivery via SES" → read `plugins/amazon-ses.md` + `third-party-integration.md`

| Reference | Scope |
|-----------|-------|
| `references/atomic-design.md` | Methodology: Brad Frost's atomic design principles, 5-to-3 tier compression, composability, context-agnostic naming, classification problem, decompose-downward workflow. Technology-independent. |
| `references/atomic-patterns.md` | Craft CMS implementation: props/extends/block pattern, button/link/text/icon atoms, molecule and organism composition, structural embed pattern, include/extends/embed decision table |
| `references/component-inventory.md` | Classification methodology: decision tree, naming conventions, file naming, props design, scaffold guidelines, tier promotion, audit checklist |
| `references/boilerplate-routing.md` | Template chain: layout hierarchy, Craft section template paths, global variables, routers, views, content builders, directory structure |
| `references/tailwind-conventions.md` | Class composition: named-key collections, standard key names, `utilities` prop, variant-based dark mode, spacing preference. Assumes Tailwind CSS — adapt patterns to your CSS framework. |
| `references/vite-buildchain.md` | Craft CMS Vite setup: nystudio107 plugin bridge, `config/vite.php`, `vite.config.ts`, `craft.vite.script()`, conditional per-page loading, Tailwind v4 integration, DDEV configuration |
| `references/image-presets.md` | Image handling: single atom with presets, srcset/sizes, ImageOptimize vs Craft Cloud, hosting strategies |
| `references/javascript-boundaries.md` | JS decision tree: Twig → Alpine/DataStar → Vue, mount points, data handoff, coexistence rules |
| `references/twig-collections.md` | `collect()` method reference: creating, accessing, transforming, filtering, sorting, slicing, arrow functions |
| `references/third-party-integration.md` | Script loading order, CMP (UserCentrics/CookieBot), GTM/sGTM data layer, analytics (Fathom/Plausible), AWS SES transport, n8n webhooks, Blitz compatibility, full head template example |

### Plugin References

Detailed configuration, Twig API, and pitfalls for Craft plugins. Located in `references/plugins/`.

| Reference | Plugin | Key Surface |
|-----------|--------|-------------|
| `references/plugins/seomatic.md` | SEOMatic (nystudio107) | Meta cascade, Twig get/set API, JSON-LD, custom element SEO bundles, sitemaps, GraphQL |
| `references/plugins/blitz.md` | Blitz (putyourlightson) | Refresh modes, Twig dynamic content, driver architecture (storage/purger/deployer), Nginx rewrite, Cloudflare integration |
| `references/plugins/formie.md` | Formie (verbb) | Form rendering (one-line/granular), theme config for Tailwind, submission querying, hooks, integrations |
| `references/plugins/image-optimize.md` | ImageOptimize (nystudio107) | OptimizedImages field, `imgTag()`/`pictureTag()` builders, loading strategies, transform methods, console commands |
| `references/plugins/ckeditor.md` | CKEditor (craftcms) | Toolbar config, nested entries with chunk rendering, HTML Purifier, custom styles, Redactor migration |
| `references/plugins/colour-swatches.md` | Colour Swatches (craftpulse) | Palette config, multi-colour swatches, Tailwind class mapping, Twig model API |
| `references/plugins/password-policy.md` | Password Policy (craftpulse) | Validation rules, HIBP check, retention/expiry, console commands, recommended settings |
| `references/plugins/hyper.md` | Hyper (verbb) | Link types, `getLinkAttributes()`, `getText()`, single/multi-link, element access, button atom integration |
| `references/plugins/retour.md` | Retour (nystudio107) | Redirect types (exact/regex), 404 tracking, CSV import, auto slug-change redirects, config |
| `references/plugins/navigation.md` | Navigation (verbb) | Node querying, custom rendering, active states, custom fields on nodes, GraphQL |
| `references/plugins/typogrify.md` | Typogrify (nystudio107) | `\|typogrify`, `\|widont`, `\|truncateOnWord`, smart quotes, widow prevention |
| `references/plugins/cache-igniter.md` | Cache Igniter (putyourlightson) | GlobalPing warmer, geographic locations, refresh delay, Blitz companion |
| `references/plugins/knock-knock.md` | Knock Knock (verbb) | Staging password protection, environment-aware config, URL exclusions |
| `references/plugins/timeloop.md` | Timeloop (craftpulse) | Repeating date field, `craft.timeloop` variable API, `recurringDates()` function, GraphQL, period frequencies |
| `references/plugins/element-api.md` | Element API (craftcms) | JSON API via config file, Fractal transformers, endpoint routing, pagination, caching |
| `references/plugins/elements-panel.md` | Elements Panel (putyourlightson) | Debug toolbar panels for element population counts, duplicate detection, eager-loading opportunities |
| `references/plugins/sherlock.md` | Sherlock (putyourlightson) | Security scanning, HTTP headers, CMS config checks, scheduled scans, IP restriction, monitoring |
| `references/plugins/embedded-assets.md` | Embedded Assets (spicyweb) | oEmbed as first-class assets, `craft.embeddedAssets.get()`, iframe customization, GraphQL |
| `references/plugins/amazon-ses.md` | Amazon SES (putyourlightson) | SES mail transport adapter, AWS credential config, SNS bounce tracking |

## Component System Conventions

One canonical component system across all projects. Atoms are context-agnostic — always named by visual treatment, never by parent. HTML element type is resolved from props (`url` → `<a>`, `type` → `<button>`, fallback → `<span>`).

External link detection is derived from the URL, never passed as a prop. Components auto-apply `target="_blank"`, `rel="noopener noreferrer"`, external icon, and sr-only text when a URL is external.

FontAwesome is the universal icon system. Icons are passed as FA class strings.

Visual variants use extends/block — base template defines structure, variant overrides classes. Never use conditional logic to switch between variant styles. For structural skeletons with content slots, use `{% embed %}` — see `atomic-patterns.md`.

Image handling uses a single atom with config-driven presets, not separate variant files per context.

## CSS & Theming Conventions

This skill assumes Tailwind CSS for class composition examples. Adapt patterns
to your CSS framework — the architectural principles (named keys, additive
utilities, semantic tokens) are framework-agnostic.

Class collections use named keys per style concern — this is the primary mechanism for preventing conflicts. The `utilities` prop is additive (extending), not overriding. Override specific concerns via named-slot merge.

Multi-brand theming uses CSS custom properties activated by `data-brand="{{ currentSite.handle }}"` on `<html>`. Components reference semantic Tailwind classes (`bg-brand-accent`) resolved via CSS variables. Template-level brand overrides only exist when the HTML structure itself differs between brands — not for color/font/spacing differences.

Token naming follows three layers: primitives (`--brand-{color}-{shade}`), semantics (`--brand-{purpose}`), and framework mapping (`--color-brand-{purpose}`).

Tailwind v4 cascade layers don't fix class conflicts within the same utilities layer. Named-key collections remain necessary.

## Routing Conventions

PHP handles data, Twig handles presentation. Views receive data through includes — they never query it themselves.

`collect()` is used for both props and class building. The full Collection API is available in Twig via Craft.

The JS boundary follows a decision tree: Twig is the default → Alpine/DataStar for UI state → Vue for application state.
