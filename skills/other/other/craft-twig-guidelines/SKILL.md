---
name: craft-twig-guidelines
description: "Twig coding standards and conventions for Craft CMS 5 templates. Covers variable naming, null handling, whitespace control, include isolation, Craft Twig helpers ({% tag %}, tag(), attr(), |attr, svg()), and collect() usage. Triggers on: any Twig template creation or review, .twig files, {% include %}, {% extends %}, {% tag %}, collect(), props.get(), .implode(), attr(), |attr filter, svg(), ?? operator, whitespace control, template coding standards, Twig best practices, naming conventions for Twig, currentSite, siteUrl, craft.entries, .eagerly(), .collect. Not for Twig architecture patterns (use craft-site) or PHP code (use craft-php-guidelines). Always use when writing, editing, or reviewing any Craft CMS Twig template code."
---

# Twig Coding Standards — Craft CMS 5

Coding conventions for Twig templates in Craft CMS 5 projects. These apply to
all Twig code — atomic components, views, layouts, builders, partials.

For Twig **architecture** patterns (atomic design, routing, builders), see the
`craft-site` skill. For PHP coding standards, see `craft-php-guidelines`.

## Documentation

- Twig in Craft: https://craftcms.com/docs/5.x/development/twig.html
- Template tags: https://craftcms.com/docs/5.x/reference/twig/tags.html
- Template functions: https://craftcms.com/docs/5.x/reference/twig/functions.html
- Twig 3 docs: https://twig.symfony.com/doc/3.x/

Use `web_fetch` on specific doc pages when something isn't covered here.

## Variable Naming

Single-word, descriptive, lowercase. No camelCase in Twig unless absolutely
unavoidable.

```twig
{# Correct #}
{% set heading = entry.title %}
{% set image = entry.heroImage.one() %}
{% set items = navigation.links.all() %}
{% set element = props.get('url') ? 'a' : 'span' %}

{# Wrong #}
{% set heroHeading = entry.title %}
{% set heroImg = entry.heroImage.one() %}
{% set navItems = navigation.links.all() %}
{% set el = props.get('url') ? 'a' : 'span' %}
```

No abbreviations: `element` not `el`, `button` not `btn`, `navigation` not `nav`,
`description` not `desc`.

If you need a multi-word variable, reconsider whether you're over-specifying.
If truly unavoidable, use snake_case over camelCase: `hero_image` over `heroImage`.

## Null Handling

`??` only. Always. No exceptions.

```twig
{# Correct #}
{% set heading = entry.heading ?? '' %}
{% set image = entry.heroImage.one() ?? null %}
{{ props.get('label') ?? 'Default' }}

{# Wrong — custom Twig extension, not portable #}
{% set heading = entry.heading ??? '' %}

{# Wrong — verbose, unnecessary #}
{% if entry.heading is defined and entry.heading is not null %}
{% if entry.heading is not defined %}
```

Twig 3.21.x (Craft 5) does not have the nullsafe operator (`?.`). That requires
Twig 3.23+. Use `??` and ternaries instead:

```twig
{# Can't do this yet #}
{{ entry?.author?.fullName }}

{# Do this instead #}
{{ entry.author.fullName ?? '' }}
```

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

## `collect()` Conventions

`collect()` wraps a Twig hash into a Collection object. Primary use cases:

### Props collection

```twig
{%- set props = collect({
    heading: heading ?? null,
    content: content ?? null,
    utilities: utilities ?? null,
}) -%}

{# Access with get() #}
{{ props.get('heading') }}
{{ props.get('size', 'text-base') }}

{# Merge additional props #}
{%- set props = props.merge({ icon: icon ?? null }) -%}
```

### Class collection (named keys)

```twig
{%- set classes = collect({
    layout: 'flex items-center gap-2',
    color: 'bg-brand-primary text-white',
    hover: 'hover:bg-brand-accent',
    utilities: props.get('utilities'),
}) -%}

class="{{ classes.implode(' ') }}"
```

Null values in `collect()` produce harmless extra spaces when joined — browsers
normalize whitespace in class attributes. Use `classes.filter(v => v).implode(' ')`
if you want pristine output for devMode inspection, but plain `implode(' ')`
is fine for production.

### Entry queries as Collections

```twig
{# .collect instead of .all() when you need Collection methods #}
{%- set entries = craft.entries.section('blog').eagerly().collect -%}
{%- set featured = entries.filter(e => e.featured).first -%}
```

## Common Pitfalls

1. **`???` operator** — custom Twig extension from older projects. Not portable. Use `??`.
2. **camelCase variables** — `iconPosition` → just `position`. Single descriptive words.
3. **Missing `only`** — silent variable leaking, invisible coupling.
4. **`{%- minify -%}`** — deprecated. Use `{%-` whitespace control.
5. **Abbreviations** — `el`, `btn`, `nav`, `desc`, `ctr` → spell it out.
6. **`is not defined`** — verbose null checking. `??` handles it.
7. **Macros as components** — wrong scoping, no extends/block support.
8. **Hardcoded colors in class strings** — `bg-yellow-600` → `bg-brand-accent`.
9. **String concatenation for classes** — `'flex ' ~ extraClass` → use `collect({})` with named keys.
10. **`options.x` pattern** — old macro convention. Use direct variable names.