---
name: craft-content-modeling
description: "Craft CMS 5 content modeling — sections, entry types, fields, Matrix, relations, project config, and content architecture strategy. Covers everything editors and developers need to structure content in Craft. Triggers on: section types (single, channel, structure), entry types, field types, field layout, Matrix configuration, nested entries, relatedTo, eager loading, .with(), .eagerly(), categories, tags, globals, global sets, preloadSingles, propagation, multi-site content, URI format, project config, YAML, content architecture, content strategy, taxonomy, asset volumes, filesystems, image transforms, user groups, permissions, entries-as-taxonomy, entrify. Always use when planning content architecture, creating sections/fields, configuring Matrix, setting up relations, or making content modeling decisions."
---

# Craft CMS 5 — Content Modeling

How to structure content in Craft CMS 5. Sections, entry types, fields, Matrix,
relations, asset management, and strategic patterns for real projects.

This skill covers **content architecture** — what goes in the CP, how it's
organized, and how templates access it. For extending Craft with PHP
(plugins, modules, custom element types), see the `craftcms` skill. For Twig
template patterns, see `craft-site` and `craft-twig-guidelines`.

## Documentation

- Entries: https://craftcms.com/docs/5.x/reference/element-types/entries.html
- Sections: https://craftcms.com/docs/5.x/reference/element-types/entries.html#sections
- Fields: https://craftcms.com/docs/5.x/system/fields.html
- Field types: https://craftcms.com/docs/5.x/reference/field-types/
- Matrix: https://craftcms.com/docs/5.x/reference/field-types/matrix.html
- Relations: https://craftcms.com/docs/5.x/system/relations.html
- Eager loading: https://craftcms.com/docs/5.x/development/eager-loading.html
- Project config: https://craftcms.com/docs/5.x/system/project-config.html

Use `web_fetch` on specific doc pages when a reference file doesn't cover enough detail.

## The Craft 5 Mental Model

**Everything is an entry.** Entry types are global (shared across sections and
Matrix fields). Fields come from a global pool. Categories, tags, and globals
are being phased out — use entries instead.

Three decisions define your content architecture:

1. **Which section type** organizes the content (Single, Channel, Structure)
2. **Which entry types** define its shape (global, reusable across contexts)
3. **Which relation strategy** connects content together (Entries fields, Matrix, or both)

## Section Type Decision

| Need | Section Type | URI Example |
|------|-------------|-------------|
| One-off page (homepage, about, contact) | **Single** | `__home__`, `about` |
| Site-wide settings (footer, header config) | **Single** (no URI, `preloadSingles`) | — |
| Flat collection (blog, news, events) | **Channel** | `blog/{slug}` |
| Hierarchical pages (docs, services) | **Structure** | `{parent.uri}/{slug}` |
| Taxonomy (topics, categories) | **Structure** (replaces categories) | `topics/{slug}` |
| Flat tags | **Channel** (replaces tags) | — |

### Singles replace globals

Set `preloadSingles => true` in `config/general.php` to access singles as global
Twig variables by handle — identical to the old globals behavior but with drafts,
revisions, live preview, and scheduling.

```twig
{# With preloadSingles enabled #}
{{ siteSettings.footerText }}
{{ siteSettings.socialLinks.all() }}
```

**Caveat:** Singles always propagate to all sites. This is hard-coded.

### Structure queries for navigation

```twig
{% set topLevel = craft.entries.section('pages').level(1).all() %}
{% set children = craft.entries.descendantOf(entry).descendantDist(1).all() %}
{% set breadcrumbs = craft.entries.ancestorOf(entry).all() %}
{% set siblings = craft.entries.siblingOf(entry).all() %}
```

## Entry Types in Craft 5

Entry types are defined globally (Settings → Entry Types), then attached to
sections and Matrix fields. One entry type can serve multiple contexts.

Key implications:
- Changing an entry type's field layout affects **every** section and Matrix field using it
- Fields come from the global pool — same field definition reused everywhere
- Local name/handle overrides per context available (5.6.0+)
- The global pool demands careful field naming — use specific handles

### Reserved handles (will collide with native attributes)

`title`, `slug`, `id`, `uid`, `dateCreated`, `dateUpdated`, `status`, `url`,
`uri`, `enabled`, `archived`, `siteId`, `level`, `lft`, `rgt`, `root`,
`postDate`, `expiryDate`

## Common Pitfalls

- **Over-using Matrix** — if content needs its own URL, independent querying, or permissions, it should be a separate section with an Entries relation field, not a Matrix block.
- **Vague field handles** — `image`, `text`, `link` collide fast in the global pool. Use `blogFeaturedImage`, `serviceDescription`, `ctaLink`.
- **Not planning multi-site from the start** — propagation method, field translation methods, and site settings must be configured before content exists. Changing propagation later resaves all entries.
- **Using categories/tags in new projects** — they're deprecated. Use Structure sections (hierarchical taxonomy) and Channel sections (flat taxonomy) with Entries fields.
- **Forgetting `preloadSingles`** — without it, singles aren't available as global variables and you need explicit queries.
- **Matrix for everything** — 15+ entry types in one Matrix field is a red flag. Deeply nested Matrix hits `max_input_vars` limits and degrades CP performance.
- **Not using `.eagerly()`** — every relational field access inside a loop should use `.eagerly()` to prevent N+1 queries.
- **Editing project config YAML manually** — let Craft manage `config/project/`. Use `php craft project-config/rebuild` to regenerate from DB if needed.
- **Using database IDs in URI formats** — IDs differ across environments. Use `{slug}`, `{canonicalUid}`, or custom fields.
- **Not setting `allowAdminChanges => false` in production** — without this, production schema changes won't sync back to dev.

## Reference Files

Read the relevant reference file(s) for your task.

**Task examples:**
- "Plan a blog content architecture" → read `content-patterns.md`
- "Which field type should I use for X?" → read `field-types.md`
- "Set up relatedTo queries" → read `relations-and-eager-loading.md`
- "Configure Matrix with nested entries" → read `field-types.md` (Matrix section)
- "Plan a multi-site content model" → read `content-patterns.md` + propagation in SKILL.md
- "Understand project config workflow" → this SKILL.md covers the essentials

| Reference | Scope |
|-----------|-------|
| `references/field-types.md` | All 26 built-in field types: settings, Twig access patterns, query syntax, gotchas. Matrix configuration, view modes, nesting. |
| `references/relations-and-eager-loading.md` | relatedTo() shapes (4 forms), .with() eager loading, .eagerly() lazy eager loading, nested eager loading, native eager-loadable attributes. |
| `references/content-patterns.md` | Strategic patterns for blog, portfolio, multi-site corporate, e-commerce. Section/field/relation architecture per pattern. Categories-to-entries migration. |

## Propagation Methods (Multi-Site)

Available for channels and structures. Singles always propagate to all sites.

| Method | Behavior |
|--------|----------|
| Only save to site created in | Entries exist in one site only |
| Same site group | Entries propagate within the same site group |
| Same language | Entries propagate to sites sharing the same language |
| All enabled sites | Entries exist in all enabled sites (default) |
| Let each entry choose | Per-entry control via Status sidebar |

Matrix fields have their **own** propagation method, independent of the section's.

### Field Translation Methods

Per-field setting controlling how values behave across sites:

| Method | Behavior |
|--------|----------|
| Not translatable | Same value across all sites |
| Per site | Independent value per site |
| Per site group | Shared within site group, independent across groups |
| Per language | Shared across sites with same language |
| Custom | User-defined grouping key |

Configure translation methods **before** populating content.

## Project Config Essentials

All schema changes (sections, entry types, fields, volumes, transforms, sites,
plugins, permissions) are stored as YAML in `config/project/`.

### Workflow

1. Make CP changes in **development** environment
2. YAML auto-updates in `config/project/`
3. Commit to Git
4. Deploy to staging/production
5. Run `ddev craft up` (applies migrations + project config)

### Rules

- Never manually edit YAML — let Craft manage it
- Always set `allowAdminChanges => false` in production
- Use UIDs (not IDs) — they're stable across environments
- After resolving Git merge conflicts in YAML: `ddev craft project-config/touch` then `ddev craft project-config/apply`
- Use `$ENV_VAR` syntax in YAML for environment-specific values

## Asset Volumes and Transforms

Volumes define content organization. Filesystems define storage (local, S3,
Google Cloud, Azure). Multiple volumes can share one filesystem.

### Image Transforms

```twig
{# Named transform (defined in Settings → Assets → Image Transforms) #}
<img src="{{ asset.getUrl('thumb') }}" alt="{{ asset.alt }}">

{# Ad-hoc transform #}
{% set transform = { width: 300, height: 200, mode: 'crop', format: 'webp' } %}
<img src="{{ asset.getUrl(transform) }}" alt="{{ asset.alt }}">

{# Srcset #}
{{ asset.getImg({ width: 300 }, ['1.5x', '2x', '3x']) }}
```

Always add the **Alternative Text** field layout element to asset volumes for
accessibility.
