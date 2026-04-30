---
name: craft-content-modeling
description: "Craft CMS 5 content modeling — sections, entry types, fields, Matrix, relations, project config, and content architecture strategy. Covers everything editors and developers need to structure content in Craft: choosing section types, designing entry types and field layouts, selecting field types for specific needs, configuring Matrix and nested entries, setting up relations and eager loading, and planning multi-site propagation. Triggers on: section types (single, channel, structure), entry types, field types, field layout design, field type selection, Matrix configuration, nested entries, relatedTo, eager loading, .with(), .eagerly(), categories, tags, globals, global sets, preloadSingles, propagation, multi-site content, URI format, project config, YAML, content architecture, content strategy, taxonomy, asset volumes, filesystems, image transforms, user groups, content permissions, entries-as-taxonomy, entrify, entrification, CKEditor vs Matrix, CMS editions, site propagation, multi-language, language groups, localization, translation method, field translation, content migration, reserved handles, field instances. Always use when planning content architecture, creating sections/fields, configuring Matrix, setting up relations, choosing field types, designing field layouts, making content modeling decisions, or planning multi-site content propagation. Do NOT trigger for PHP plugin/module development, custom field type code, front-end Twig templates, or buildchain configuration."
---

# Craft CMS 5 — Content Modeling

How to structure content in Craft CMS 5. Sections, entry types, fields, Matrix,
relations, asset management, and strategic patterns for real projects.

This skill covers **content architecture** — what goes in the CP, how it's
organized, and how templates access it. For extending Craft with PHP
(plugins, modules, custom element types), see the `craftcms` skill.

## Companion Skills — Always Load Together

When this skill triggers, also load:

- **`craft-site`** — Template architecture, component patterns, routing. Required when content decisions affect how templates render data.
- **`craft-twig-guidelines`** — Twig coding standards. Required when writing any Twig examples or template code alongside content modeling.
- **`ddev`** — All commands run through DDEV. Required for running project config commands, Craft CLI, and content migrations.

## Documentation

- Entries: https://craftcms.com/docs/5.x/reference/element-types/entries.html
- Sections: https://craftcms.com/docs/5.x/reference/element-types/entries.html#sections
- Fields: https://craftcms.com/docs/5.x/system/fields.html
- Field types: https://craftcms.com/docs/5.x/reference/field-types/
- Matrix: https://craftcms.com/docs/5.x/reference/field-types/matrix.html
- Relations: https://craftcms.com/docs/5.x/system/relations.html
- Eager loading: https://craftcms.com/docs/5.x/development/eager-loading.html
- Project config: https://craftcms.com/docs/5.x/system/project-config.html

Use `WebFetch` on specific doc pages when a reference file doesn't cover enough detail.

## The Craft 5 Mental Model

**Everything is becoming an entry.** Entry types are global (shared across sections and
Matrix fields). Fields come from a global pool. This is the "entrification" of Craft — categories, tags, and globals are being unified into entries over a three-version arc:

- **Craft 4.4** — `entrify` CLI commands added to convert categories, tags, and globals to entries
- **Craft 5** — Creating new category groups, tag groups, or global sets is no longer possible in the CP. Existing ones continue to work. A unified "Content" section replaces the fragmented entries view. Custom entry index pages (5.9.0) solve the sidebar organization concern.
- **Craft 6** — Categories, tags, and global sets will be removed entirely

For **new projects**, always use entries: Structure sections for hierarchical taxonomy, Channel sections for flat taxonomy, Singles for site-wide settings. For **existing projects**, migrate at your own pace using the `entrify` commands.

Three decisions define your content architecture:

1. **Which section type** organizes the content (Single, Channel, Structure)
2. **Which entry types** define its shape (global, reusable across contexts)
3. **Which relation strategy** connects content together (Entries fields, Matrix, CKEditor nested entries, or a combination)

## CMS Editions

Craft CMS has four editions (Solo, Team, Pro, Enterprise) that affect content modeling. The key distinction: if any section needs per-group edit/view restrictions, you need **Pro or Enterprise** (user groups and permissions are Pro+ only). See `references/users-and-permissions.md` for the full editions table and permissions architecture.

Choose the edition before modeling — it determines whether you can scope content access by user group, which affects section and field architecture.

## Section Type Decision

| Need | Section Type | URI Example |
|------|-------------|-------------|
| One-off page (homepage, about, contact) | **Single** | `__home__`, `about` |
| Site-wide settings (footer, header config) | **Single** (no URI, `preloadSingles`) | — |
| Flat collection (blog, news, events) | **Channel** | `blog/{slug}` |
| Hierarchical pages (docs, services) | **Structure** | `{parent.uri}/{slug}` |
| Taxonomy (topics, categories) | **Structure** (replaces categories) | `topics/{slug}` |
| Flat tags | **Channel** (replaces tags) | — |

### Section Properties

Beyond the type, sections have settings that matter for content architecture:

- **`maxAuthors`** (default 1) — allows multiple authors per entry (new in 5.0.0). Set higher for collaborative content.
- **`enableVersioning`** (default true) — version history for entries
- **`defaultPlacement`** — `'beginning'` or `'end'` for new entries in structures
- **`previewTargets`** — array of `{label, urlFormat}` objects defining where entries can be previewed. Default: primary entry page. Add custom targets for headless frontends, staging URLs, or PDF previews.

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
- Per-context name/handle/description overrides available (5.6.0+) — useful when the same entry type serves different purposes in different sections
- The global pool demands careful field naming — use specific handles

### Entry Type Visual Identity (Craft 5 new)

Entry types have visual properties that improve the editorial experience:

- **`icon`** — custom icon identifier, shown in entry type selectors and Matrix "+" menus
- **`color`** — one of 20 options (red, orange, amber, yellow, lime, green, emerald, teal, cyan, sky, blue, indigo, violet, purple, fuchsia, pink, rose, white, gray, black)
- **`description`** (5.8.0) — help text explaining what this entry type is for
- **`group`** (5.8.0) — collapsible grouping in section/Matrix entry type assignments
- **`uiLabelFormat`** (5.9.0) — customize the label shown in element indexes (default `'{title}'`)
- **`hasTitleField`** / **`titleFormat`** — disable the title field and auto-generate from other fields
- **`showSlugField`** (5.0.0) / **`showStatusField`** (4.5.0) — hide slug or status from editors
- **`allowLineBreaksInTitles`** (5.9.0) — for long-form titles

These settings are configured in Settings → Entry Types and affect all contexts where the entry type is used.

### Reserved handles — check every proposed field handle against this list

Craft has **83+ reserved handles** across all element types via `Field::RESERVED_HANDLES`. Validation is case-insensitive. Using any of these as a custom field handle will cause a validation error or silent template collision where the native attribute shadows the custom field.

**Before proposing any field handle in a content model, check it against the lists below.** When a user asks for a field that matches a native attribute name, always use a domain-specific synonym. For example: user says "I need a title field" — the entry already has a native `title`, so use `heading`, `headline`, or `pageTitle` depending on context.

**Most commonly collided (the ones you'll actually try to use):**

| Reserved | Use Instead | Why |
|----------|-------------|-----|
| `title` | `heading`, `headline`, `label`, `pageTitle` | Native element title |
| `slug` | `urlSlug`, `handle` | Native URL slug |
| `status` | `state`, `phase`, `condition` | Native element status |
| `url` | `externalUrl`, `targetUrl`, `websiteUrl` | Native element URL |
| `link` | `targetLink`, `ctaLink`, `primaryLink` | Native `getLink()` method |
| `icon` | `entryIcon`, `menuIcon`, `featureIcon` | Native element icon (5.0.0) |
| `parent` | `parentEntry`, `parentItem`, `belongsTo` | Native structure parent |
| `children` | `childEntries`, `subItems`, `nestedItems` | Native structure children |
| `owner` | `entryOwner`, `ownerElement` | Native nested entry owner |
| `site` | `location`, `branch`, `region` | Native site object |
| `level` | `depth`, `tier`, `nestingLevel` | Native structure level |
| `ancestors` | `parentChain`, `breadcrumbEntries` | Native structure ancestors |
| `siblings` | `peerEntries`, `relatedSiblings` | Native structure siblings |
| `enabled` | `isActive`, `isPublished`, `isVisible` | Native enabled/disabled state |
| `language` | `locale`, `contentLanguage` | Native site language |
| `localized` | `translations`, `localizedVersions` | Native localized entries query |
| `next` / `prev` | `nextEntry` / `prevEntry` | Native structure navigation |
| `ref` | `reference`, `referenceCode` | Native reference tag |
| `type` | `entryType`, `category`, `variant` | Native entry type |
| `author` / `authors` | `writer`, `creator`, `contributor` | Native entry author(s) |
| `postDate` | `publishDate`, `releaseDate`, `goLiveDate` | Native entry post date |

**Full list of reserved handles shared across ALL element types** (from `Field::RESERVED_HANDLES`):

`ancestors`, `archived`, `attributes`, `behaviors`, `canonical`, `children`, `contentTable`, `dateCreated`, `dateDeleted`, `dateLastMerged`, `dateUpdated`, `descendants`, `draftId`, `enabled`, `enabledForSite`, `error`, `errors`, `fieldLayoutId`, `fieldValue`, `fieldValues`, `firstSave`, `icon`, `id`, `language`, `level`, `lft`, `link`, `localized`, `next`, `nextSibling`, `owner`, `parent`, `parents`, `prev`, `prevSibling`, `ref`, `revisionId`, `rgt`, `root`, `searchScore`, `siblings`, `site`, `siteId`, `siteSettingsId`, `slug`, `sortOrder`, `status`, `structureId`, `title`, `trashed`, `uid`, `uri`, `url`, `viewMode`

**Additional per-element-type reserved handles:**

| Element Type | Additional Reserved |
|---|---|
| **Entries** | `author`, `authorId`, `authorIds`, `authors`, `section`, `sectionId`, `type`, `postDate` |
| **Assets** | `alt`, `extension`, `filename`, `folder`, `height`, `kind`, `size`, `volume`, `width` |
| **Users** | `active`, `addresses`, `admin`, `affiliatedSiteId`, `email`, `firstName`, `friendlyName`, `fullName`, `groups`, `lastName`, `locked`, `name`, `password`, `pending`, `photo`, `suspended`, `username` |
| **Categories** | `group` |
| **Tags** | `group` |
| **Addresses** | `address`, `countryCode`, `fullName`, `latLong`, `organization`, `organizationTaxId` |

**Also globally reserved** (from `HandleValidator::$baseReservedWords`, applies to ALL handles): `attribute`, `attributeLabels`, `attributeNames`, `attributes`, `dateCreated`, `dateUpdated`, `errors`, `false`, `fields`, `handle`, `id`, `n`, `name`, `no`, `rules`, `this`, `true`, `uid`, `y`, `yes`

## Field Instances — Reuse Over Duplication

Fields are defined once globally, then **instanced** into field layouts. Each instance can override four properties without affecting the global definition:

- **Label** — different display name per context
- **Handle** — different template handle per context (5.0.0+)
- **Instructions** — context-specific help text
- **Required** — required in one layout, optional in another

This means a single `heroImage` Assets field can be placed in a Blog Post, a Service Page, and a Project entry type — each with different labels ("Hero Image", "Banner", "Cover Photo") and different required settings. The field definition, type, and settings are shared.

**The rule: reuse field definitions via instances. Only create a new field when the type or settings differ** (e.g., different allowed volumes, different source restrictions, different character limits). Don't create `blogHeroImage`, `serviceHeroImage`, `projectHeroImage` — create one `heroImage` and instance it.

### Multi-Instance vs Single-Instance Fields

A field's `isMultiInstance()` method controls whether it can appear **multiple times in the same layout** with different handles. This is determined by `dbType()` — fields that return `null` are single-instance.

| Category | Field Types | Multi-Instance | Reusable Across Layouts |
|----------|-------------|:--------------:|:-----------------------:|
| **Relational** | Entries, Assets, Categories, Tags, Users | Yes | Yes |
| **Simple** | Plain Text, Number, Email, URL, Color, Lightswitch, Money, Range, Time, Date/Time | Yes | Yes |
| **Option** | Dropdown, Checkboxes, Multi-Select, Radio Buttons, Button Group | Yes | Yes |
| **Structured** | Table, Link, Icon, Country | Yes | Yes |
| **Nested element** | Matrix, Content Block, Addresses | **No** | Yes (with caveats) |

**Single-instance caveats:** Matrix, Content Block, and Addresses fields CAN be reused across different entry types (placed in multiple field layouts), but they can only appear **once per layout** and their configuration is fully shared — changing the entry types or settings on a Matrix field affects every entry type using it. Reuse these when contexts genuinely share the same structure. Create separate fields when different contexts need different nested entry types or settings.

## Adding Fields to an Entry Type — Reuse-First Workflow

Before proposing any field in a content model change, you MUST:

1. **Enumerate the existing field pool.** Read `config/project/fields/` (or CP Settings → Fields). List every field with its type, handle, and key settings.
2. **For each proposed field, classify into one of three categories:**
   - **Reuse** — existing field with matching type and compatible settings. Instance it into the layout; optionally override label, handle, instructions, or required.
   - **Reuse with settings review** — existing field of the correct type but slightly different settings (e.g., different allowed volumes, different character limit). Propose whether settings can be unified so one definition serves both contexts. Flag this as a decision for the user.
   - **Create new** — no existing field matches by type or functional purpose. Justify why a new field is needed.
3. **For single-instance fields** (Matrix, Content Block, Addresses) — if an existing field shares the same nested structure, reuse it. If the contexts need different nested entry types or settings, creating a new field is justified — note the shared-config caveat in your reasoning.
4. **Present the plan as a table** — one row per proposed field, showing the reuse decision, the existing field being reused (if applicable), and the rationale for any new field. Do not create a new field without this table.

Creating a field that duplicates an existing field's functionality is the most common content modeling mistake — it pollutes the global pool, confuses editors, and makes future refactoring harder.

## Entrification — Migrating Legacy Content

### CLI Commands

```bash
ddev craft entrify/categories <categoryGroupHandle>   # → Structure section
ddev craft entrify/tags <tagGroupHandle>               # → Channel section
ddev craft entrify/global-set <globalSetHandle>        # → Single section
```

All three accept `--section` and `--entry-type` to target an existing section/entry type instead of creating new ones. `entrify/categories` and `entrify/tags` also accept `--author`.

As of 5.9.0, these commands are interactive — the handle argument is optional.

### What the commands do

- Convert the element type to entries
- Migrate all content and field data
- Convert Categories/Tags fields to Entries fields
- Preserve existing relations
- Assign newly created sections to appropriate entry index pages

### Entries field for hierarchical selection

When replacing a Categories field with an Entries field, enable **Maintain Hierarchy** on the Entries field. This auto-selects ancestors when a nested entry is chosen — replicating the category field behavior.

### Tags replacement caveat

For flat taxonomies where editors created terms on-the-fly, the on-the-fly creation UX is not yet available for Entries fields. This is the one area where the legacy Tags field still has a UX advantage. Use a Channel section and accept the two-step workflow (create entry separately, then relate it).

## CKEditor vs Matrix vs Content Block

Three tools for structured content within an entry — choose based on editing experience:

- **Matrix** — reorderable blocks, page builders, data grids, media galleries. Multiple view modes (blocks, cards, cards-grid, index).
- **CKEditor** with nested entries — rich text with occasional structured content inline (image blocks, code blocks, CTAs). Natural writing flow.
- **Content Block** (5.8.0) — single non-repeatable nested entry for reusable field groups (SEO metadata, banner config).

For the full decision table, nested entry type patterns, and the CKEditor chunks rendering pattern, read `references/content-patterns.md`.

## Common Pitfalls

- **Over-using Matrix** — if content needs its own URL, independent querying, or permissions, it should be a separate section with an Entries relation field, not a Matrix block.
- **Creating new fields without checking the global pool** — before adding any field, run the Reuse-First Workflow above. Enumerate existing fields via `config/project/fields/` and default to reusing via instance. The only justification for a new field is a different type or genuinely incompatible settings.
- **Vague or reserved field handles** — `image`, `text`, `link` are too generic (and `link` is actually reserved). For every field handle in a content model, follow this check: (1) is the handle in the reserved list? If yes, use a synonym from the table. (2) Is the handle too generic for the global field pool? If yes, add domain context: `featuredImage`, `bodyContent`, `primaryLink`. (3) Don't over-specify — `blogFeaturedImage` creates a new field when you could instance `featuredImage` with a label override.
- **Not planning multi-site from the start** — propagation method, field translation methods, and site settings must be configured before content exists. Changing propagation later resaves all entries.
- **Using categories/tags/globals in new projects** — new creation is disabled in Craft 5 CP and they will be removed in Craft 6. Use entries instead.
- **Forgetting `preloadSingles`** — without it, singles aren't available as global variables and you need explicit queries.
- **Matrix for everything** — 15+ entry types in one Matrix field is a red flag. Deeply nested Matrix hits `max_input_vars` limits and degrades CP performance.
- **Not using `.eagerly()`** — every relational field access inside a loop should use `.eagerly()` to prevent N+1 queries.
- **Editing project config YAML manually** — let Craft manage `config/project/`. Use `ddev craft project-config/rebuild` to regenerate from DB if needed.
- **Using database IDs in URI formats** — IDs differ across environments. Use `{slug}`, `{canonicalUid}`, or custom fields.
- **Not setting `allowAdminChanges => false` in production** — without this, production schema changes won't sync back to dev.
- **Using `@web` in filesystem URLs** — `@web` is auto-detected from the HTTP request and can be spoofed or empty in console/queue contexts. Use environment variables (`$ASSETS_URL`) for filesystem URLs. `@webroot` for paths is less risky but env vars are still preferred.
- **Ignoring entry type visual identity** — editors navigate by icon, color, and description. Investing in these settings makes the CP usable as the content model grows.
- **Not planning for CMS edition** — if you need per-group content permissions, you need Pro or Enterprise. This affects section and field architecture.

## Reference Files

Read the relevant reference file(s) for your task.

**Task examples:**
- "Add fields to an existing entry type" → Reuse-First Workflow in this SKILL.md
- "Modify an entry type's field layout" → Reuse-First Workflow in this SKILL.md
- "Plan a blog content architecture" → read `content-patterns.md`
- "Which field type should I use for X?" → read `field-types.md`
- "Set up relatedTo queries" → read `relations-and-eager-loading.md`
- "Configure Matrix with nested entries" → read `field-types.md` (Matrix section)
- "Plan a multi-site content model" → read `content-patterns.md` + `infrastructure.md` (propagation)
- "Set up users, groups, and permissions" → read `users-and-permissions.md`
- "Understand project config workflow" → read `infrastructure.md` (Project Config Essentials)
- "How does Craft store content internally?" → read `infrastructure.md` (Storage Model)
- "Set up asset volumes and filesystems" → read `infrastructure.md` (Assets section)
- "Configure URI format for a structure section" → read `object-templates.md` (Structure URI Patterns)
- "Set up dynamic asset upload subpath" → read `object-templates.md` (Asset Subpath Patterns)
- "Asset subpath broken after moving field into Matrix" → read `object-templates.md` (The Matrix Gotcha)

| Reference | Scope |
|-----------|-------|
| `references/field-types.md` | All built-in field types: settings, Twig access patterns, query syntax, gotchas. Matrix configuration, view modes, nesting. |
| `references/relations-and-eager-loading.md` | relatedTo() shapes (4 forms), .with() eager loading, .eagerly() lazy eager loading, nested eager loading, native eager-loadable attributes. |
| `references/content-patterns.md` | Strategic patterns for blog, portfolio, multi-site corporate. Section/field/relation architecture per pattern. Entrification migration. CKEditor vs Matrix decisions. |
| `references/users-and-permissions.md` | Users, user groups, CMS editions, addresses, permissions architecture, field layout UI elements. |
| `references/infrastructure.md` | Multi-site propagation methods, field translation methods, project config workflow, how Craft stores content (five-table model, JSON field values, relations, nested sets), asset volumes/filesystems/transforms. |
| `references/object-templates.md` | Object template syntax: `{attribute}` vs `{{ twig }}`, URI formats, asset subpaths, preview targets, owner/rootOwner nesting, structure patterns, the Matrix gotcha. |
