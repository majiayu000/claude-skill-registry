---
name: craft-twig-guidelines
description: "Twig coding standards and conventions for Craft CMS 5 templates. ALWAYS load this skill when writing, editing, or reviewing any .twig file in a Craft CMS project — even for small edits. Covers: variable naming (camelCase, no abbreviations), null handling (?? operator, ??? with empty-coalesce plugin), whitespace control ({%- trimming, NOT {%- minify -%}), include isolation (always use 'only'), Craft Twig helpers ({% tag %}, tag(), attr(), |attr filter, |parseAttr, |append, svg()), collect() for props and class collections, .implode(), comment headers with ========= separators on component files, and common pitfalls (snake_case, macros as components, hardcoded colors). Triggers on: Twig template creation, editing, or review; .twig files; {% include %} with 'only'; {% tag %} and polymorphic elements; collect() and props.get(); class string building; attr() and |attr filter; svg() with styling and aria; ?? and ??? null coalescing; whitespace control and blank lines in output; minify alternatives; Twig file headers and comment blocks; variable naming conventions in Twig; currentSite, siteUrl, craft.entries, .eagerly(), .collect in template context. NOT for Twig architecture patterns, atomic design structure, or template routing (use craft-site). NOT for PHP code (use craft-php-guidelines). NOT for content modeling or field configuration (use craft-content-modeling)."
---

# Twig Coding Standards — Craft CMS 5

Coding conventions for Twig templates in Craft CMS 5 projects. These apply to
all Twig code — atomic components, views, layouts, builders, partials.

## Companion Skills — Always Load Together

When this skill triggers, also load:

- **`craft-site`** — Template architecture and component patterns. Required when creating or editing components, layouts, views, or builders.
- **`craft-content-modeling`** — Content architecture. Required when template code involves element queries, field access, or section decisions.

For Twig **architecture** patterns (atomic design, routing, builders), see the
`craft-site` skill. For PHP coding standards, see `craft-php-guidelines`.

## Documentation

- Twig in Craft: https://craftcms.com/docs/5.x/development/twig.html
- Template tags: https://craftcms.com/docs/5.x/reference/twig/tags.html
- Template functions: https://craftcms.com/docs/5.x/reference/twig/functions.html
- Twig 3 docs: https://twig.symfony.com/doc/3.x/

Use `WebFetch` on specific doc pages when something isn't covered here.

## Variable Naming

Single-word, descriptive, lowercase preferred. When multi-word is needed, use
camelCase.

```twig
{# Correct #}
{% set heading = entry.title %}
{% set image = entry.heroImage.one() %}
{% set items = navigation.links.all() %}
{% set element = props.get('url') ? 'a' : 'span' %}
{% set buttonText = entry.callToAction %}
{% set containerClass = 'max-w-3xl' %}

{# Wrong — abbreviations #}
{% set el = props.get('url') ? 'a' : 'span' %}
{% set btn = entry.callToAction %}
{% set nav = navigation.links.all() %}

{# Wrong — snake_case #}
{% set button_text = entry.callToAction %}
{% set container_class = 'max-w-3xl' %}
```

No abbreviations: `element` not `el`, `button` not `btn`, `navigation` not `nav`,
`description` not `desc`.

Prefer single-word names when context makes the meaning clear (e.g. `heading`
inside a component is better than `sectionHeading`). But multi-word camelCase is
perfectly fine when needed for clarity.

## Null Handling

`??` is the default. Always safe, always portable.

`???` (empty coalesce) is acceptable if the project already has `nystudio107/craft-emptycoalesce` or `nystudio107/craft-seomatic` installed — both provide the operator. But never install a plugin just for `???`. Check `composer.json` first.

```twig
{# Always correct #}
{% set heading = entry.heading ?? '' %}
{% set image = entry.heroImage.one() ?? null %}
{{ props.get('label') ?? 'Default' }}

{# OK if empty-coalesce or SEOmatic is installed — checks empty, not just null #}
{% set heading = entry.heading ??? '' %}

{# Wrong — verbose, unnecessary #}
{% if entry.heading is defined and entry.heading is not null %}
{% if entry.heading is not defined %}
```

Craft 5 supports the nullsafe operator (`?.`). Use it for deep traversal through
chains that may have null links — it propagates `null` cleanly without the verbose
`is defined and is not null` dance:

```twig
{# Reach for ?. when any link in the chain may be null #}
{{ entry?.author?.fullName ?? 'Anonymous' }}

{# ?? alone is enough when only the leaf is in question #}
{{ entry.title ?? '' }}
```

`??` stays the right tool for simple "value or fallback" cases; `?.` is for chains
where intermediate links may be missing. Don't reach for `?.` on a single property
access — it adds noise without adding safety.

## Whitespace Control

Use `{%-` and `{{-` for whitespace trimming. Never use `{%- minify -%}`.

```twig
{# Correct — surgical whitespace control #}
{%- set heading = entry.title -%}
{%- if heading -%}
    {{- heading -}}
{%- endif -%}

{# Wrong — deprecated minification approach #}
{%- minify -%}
    {% set heading = entry.title %}
{%- endminify -%}
```

Apply whitespace control on tags that produce unwanted blank lines in output.
Not every tag needs it — use where visible output whitespace matters.

## Include Isolation

Every `{% include %}` MUST use `only`. No exceptions.

```twig
{# Correct — explicit, isolated #}
{%- include '_atoms/buttons/button--primary' with {
    text: entry.title,
    url: entry.url,
} only -%}

{# Wrong — ambient variables leak in #}
{%- include '_atoms/buttons/button--primary' with {
    text: entry.title,
    url: entry.url,
} -%}
```

Without `only`, a component can silently depend on variables from its parent
scope, creating invisible coupling.

## No Macros for Components

Never use `{% macro %}` for UI components. Macros don't support extends/block
and their scoping model differs from includes.

```twig
{# Wrong — macro for a component #}
{% macro button(text, url) %}
    <a href="{{ url }}">{{ text }}</a>
{% endmacro %}

{# Correct — include with isolation #}
{%- include '_atoms/buttons/button--primary' with {
    text: text,
    url: url,
} only -%}
```

Macros are acceptable for utility functions that return strings (e.g., formatting
helpers), not for rendering UI.

## Comment Headers

Every component file gets a section header comment:

```twig
{# =========================================================================
   Component Name
   Brief description of what this component does.
   ========================================================================= #}
```

Props files, variant files, views, layouts — all get headers. The `=========`
separator matches the PHP convention from `craft-php-guidelines`.

## Craft Twig Helpers

### `{% tag %}` — Polymorphic Elements

Primary tool for rendering elements whose tag name depends on props.

```twig
{%- set element = props.get('url') ? 'a' : 'span' -%}

{%- tag element with {
    class: classes.implode(' '),
    href: props.get('url') ?? false,
    target: props.get('target') ?? false,
    rel: props.get('rel') ?? false,
    aria: {
        label: props.get('label') ?? false,
    },
} -%}
    {{ props.get('text') }}
{%- endtag -%}
```

Rules:
- Variable name must be descriptive: `element`, `heading`, `wrapper`. Never `el`, `hd`.
- `false` omits an attribute entirely from the rendered HTML.
- `null` also omits. Use `false` when explicitly excluding, `null` when absent.
- `class` accepts arrays with automatic falsy filtering.
- `aria` and `data` accept nested hashes that expand to `aria-*` / `data-*` attributes.

### `tag()` — Inline Element Function

For simple elements without complex inner content:

```twig
{{ tag('span', { class: 'sr-only', text: '(opens in new window)' }) }}
{{ tag('img', { src: image.url, alt: image.title, loading: 'lazy' }) }}
{{ tag('i', { class: ['fa-solid', icon], aria: { hidden: 'true' } }) }}

{# Craft 5.10+: pass a string as the second arg as a text-only shortcut #}
{{ tag('span', 'Read more') }}
```

- `text:` key = HTML-encoded content.
- `html:` key = raw HTML content (trusted input only).
- Self-closing elements (`img`, `input`, `br`) handled automatically.

### `attr()` — Attribute Strings

For building attributes in non-tag contexts:

```twig
<div{{ attr({ class: ['card', active ? 'card--active'], data: { id: entry.id } }) }}>
```

Returns a space-prefixed attribute string. Same `false`-means-omit and class
array filtering as `{% tag %}`.

### `|attr` Filter

For merging attributes onto existing HTML strings:

```twig
{{ svg('@webroot/icons/check.svg')|attr({ class: 'w-4 h-4', aria: { hidden: 'true' } }) }}
```

### `|parseAttr` Filter

For extracting attributes from an HTML string into a hash for manipulation:

```twig
{% set attributes = '<div class="foo" data-id="1">'|parseAttr %}
{# attributes = { class: 'foo', data: { id: '1' } } #}
```

### `|append` Filter

For adding content to an element string:

```twig
{{ svg('@webroot/icons/logo.svg')|append('<title>Company Logo</title>', 'replace') }}
```

### `svg()` Function

```twig
{{ svg('@webroot/icons/logo.svg') }}
{{ svg(entry.svgField.one()) }}
```

Combine with `|attr` for classes and aria attributes. Use `|append` for
accessible labels inside the SVG.

### `heading()` / `h()` / `h1()`…`h6()` — Programmatic Headings (Craft 5.10+)

Build heading tags from a dynamic level without string-concatenation. Useful in
components that receive a `level` prop and need to render the matching tag
without doing `tag('h' ~ level, text)` manually.

```twig
{# heading(level, text-or-attributes) — level is an int 1-6 #}
{{ heading(2, 'Section title') }}                     {# <h2>Section title</h2> #}
{{ heading(3, { class: 'text-xl', text: 'Subsection' }) }}

{# h() is the short alias for heading() #}
{{ h(2, 'Section title') }}

{# Bound-level shortcuts — only attributes/text needed #}
{{ h1('Page title') }}
{{ h2('Section') }}
{{ h6({ class: 'sr-only', text: 'Hidden heading' }) }}
```

These are stateless tag builders — there's no auto-incrementing or current-level
tracking. Components that need to thread a level across nested contexts still
pass it as a prop. `heading()` throws `InvalidArgumentException` when level is
outside 1-6.

### Filter Additions (Craft 5.10+)

```twig
{{ price|number(locale: 'de-DE') }}                   {# locale arg #}
{{ entry.postDate|datetime('long', withTimeZone: true) }}
{{ deadline|time('short', withTimeZone: true) }}
{{ maybeNull|timestamp }}                              {# returns "now" for null/empty #}
```

### Filtering and Mapping — Default to `collect()`

For data manipulation in templates, **default to `collect()`** — one consistent, chainable API (`where`, `firstWhere`, `groupBy`, `keyBy`, `unique`, `pluck`, `map`, `filter`, `sortByDesc`) instead of mixing idioms:

```twig
{% set newsByYear = entries.collect
    .where('type', 'news')
    .sortByDesc('postDate')
    .groupBy(e => e.postDate|date('Y')) %}
```

The bare Twig/Craft array filters are fine for a **single trivial operation inline** — `{% for e in entries|filter(e => e.enabled) %}` — where a Collection adds nothing. But Twig's `|filter`/`|map` return plain arrays and Craft's `|where`/`|firstWhere`/`|group`/`|index` go through `ArrayHelper`, so they **don't chain like Collection methods**; once you need more than one step, switch to `collect()`. Don't mix both styles arbitrarily.

There is **no `|indexBy` filter** — key a list with `|index` (or `.keyBy()` on a Collection) and bucket with `|group` (or `.groupBy()`). (`|where`, `|firstWhere`, `|contains`, `|group`, `|index`, `|explodeClass`/`|explodeStyle` are all Craft-registered filters.)

### Safe Output and Inline Assets

- **`|t('category')`** — route every user-facing string through translation; never hardcode display copy.
- **`|purify`** — sanitize untrusted or rich HTML rather than reaching for `|raw`. Reserve `|raw` for trusted field output (CKEditor/Redactor); never `|raw` user-submitted or query-string-derived content.
- **`|explodeClass` / `|explodeStyle`** — normalize a class/style string to an array before merging, instead of hand-splitting on spaces.
- **`{% js %}` / `{% css %}` / `{% script %}`** — register inline assets through the View (it dedupes and positions them) instead of hand-writing `<script>`/`<style>`. (`{% js %}`/`{% css %}` go through the asset manager; `{% script %}`/`{% html %}` are verbatim.)
- **`{% dd %}` / `dump()`** — for debugging only; never ship them, and don't use `{{ x|json_encode }}` as a debug hack.

## `collect()` Conventions

When building props and class collections, these are the style rules to enforce:

- **camelCase keys** — `heroImage`, never `hero_image`.
- **One named key per concern** — a class collection gets one key per style
  concern (`layout`, `color`, `spacing`, …), never two classes fighting over the
  same element.
- **Build class strings with `.implode(' ')`** — never string concatenation
  (`'flex ' ~ extraClass`).
- **Null/empty values are harmless** — `implode(' ')` joins them as empty strings,
  producing extra spaces that browsers normalize in class attributes.

```twig
{%- set classes = collect({
    layout: 'flex items-center gap-2',
    color: 'bg-brand-primary text-brand-on-primary',
    hover: 'hover:bg-brand-accent',
    utilities: props.get('utilities'),
}) -%}

class="{{ classes.implode(' ') }}"
```

For the full `collect()` method reference and architecture patterns (props
collection, `get()`/`merge()`, entry-queries-as-Collections), see `craft-site`
(`references/twig-collections.md`); for the named-key Tailwind class pattern, see
`craft-site` (`references/tailwind-conventions.md`).

## Common Pitfalls

1. **`???` operator without the plugin** — requires `nystudio107/craft-emptycoalesce` or `nystudio107/craft-seomatic`. Check `composer.json` before using. Default to `??`.
2. **snake_case variables** — use camelCase: `heroImage` not `hero_image`.
3. **Missing `only`** — silent variable leaking, invisible coupling.
4. **`{%- minify -%}`** — deprecated. Use `{%-` whitespace control.
5. **Abbreviations** — `el`, `btn`, `nav`, `desc`, `ctr` → spell it out.
6. **`is not defined`** — verbose null checking. `??` handles it.
7. **Macros as components** — wrong scoping, no extends/block support.
8. **Hardcoded colors in class strings** — `bg-yellow-600` → `bg-brand-accent`.
9. **String concatenation for classes** — `'flex ' ~ extraClass` → use `collect({})` with named keys.
10. **`is empty` / `|default` on Craft Models (5.10+)** — any `yii\base\Model` (entries, settings, custom models) is now treated as non-empty regardless of its property values. Means `{{ user|default('Guest') }}` always renders the user object; `{% if entry is empty %}` always false. Check the specific property you care about: `{% if entry.title is empty %}`.
11. **`options.x` pattern** — old macro convention. Use direct variable names.
12. **Blocks inside conditionals** — `{% if %}{% block foo %}{% endblock %}{% endif %}` is invalid Twig. Blocks are compile-time structures and cannot be conditionally defined. Move the conditional inside the block: `{% block foo %}{% if condition %}...{% endif %}{% endblock %}`.
13. **Hardcoded `/admin` CP URL** — `cpTrigger` is configurable via `CRAFT_CP_TRIGGER` env var or `cpTrigger` in general.php. Many projects use `cp` instead of `admin`. Use `cpUrl()` function or check `.env` — never hardcode `/admin/`.