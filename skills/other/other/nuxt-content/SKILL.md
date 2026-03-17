---
name: nuxt-content
description: Author Markdown content files for Nuxt Content using MDC syntax. Use when creating or editing .md files in content/ directories, writing documentation, blog posts, or any content that uses Vue components in Markdown. Triggers on content authoring, MDC syntax, Nuxt Content files.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Nuxt Content MDC Authoring Guide

MDC (Markdown Components) extends standard Markdown with Vue component support. Use this guide when authoring `.md` files for Nuxt Content.

## Quick Reference

| Syntax | Description |
|--------|-------------|
| `::component` | Block component |
| `:component` | Inline component |
| `{prop="value"}` | Props |
| `#slotname` | Named slot |
| `[text]{.class}` | Span with attributes |
| `{{ $doc.var }}` | Variable binding |

## Frontmatter

YAML metadata block at the top of the file:

```markdown
---
title: My Article
description: A brief description
author: John Doe
date: 2024-01-15
tags:
  - tutorial
  - nuxt
draft: false
---
```

Access frontmatter values in content using `{{ $doc.propertyName }}`.

## Block Components

Block components use `::` syntax and can contain Markdown content:

```markdown
::alert{type="warning"}
This is a warning message with **Markdown** support.
::
```

### Nested Components

```markdown
::card
  ::card-header
  Card Title
  ::

  Card body content here.

  ::card-footer
  Footer text
  ::
::
```

### Named Slots

Use `#slotname` to define named slots:

```markdown
::card
Default slot content goes here.

#header
This goes in the header slot.

#footer
This goes in the footer slot.
::
```

### Self-Closing Block Components

For components without content:

```markdown
::divider
::
```

## Inline Components

Inline components use single `:` and flow with text:

```markdown
Here is an :icon{name="heroicons:star"} icon inline.

Status: :badge[Active]{color="success"}

Click :button[Submit]{@click="handleSubmit"} to continue.
```

### Inline Component with Content

Use square brackets for default slot content:

```markdown
:badge[Premium]
:button[Click Me]{variant="outline"}
```

## Props

### Inline Props

```markdown
::alert{type="info" icon="heroicons:information-circle"}
Content here
::

:icon{name="heroicons:check" class="text-green-500" size="24"}
```

### YAML Props Block

For complex props, use a YAML block after the component declaration:

```markdown
::card
---
title: My Card
image: /images/hero.jpg
tags:
  - featured
  - new
---
Card content with complex props defined above.
::
```

### JSON Props (Arrays/Objects)

Prefix with `:` for JavaScript expressions:

```markdown
::dropdown{:items='["Option A", "Option B", "Option C"]'}
::

::chart{:data='{"labels": ["Jan", "Feb"], "values": [10, 20]}'}
::
```

### Boolean Props

```markdown
::modal{closable}       <!-- true -->
::modal{:closable="false"}  <!-- explicit false -->
```

### Dynamic Props

Bind to frontmatter variables:

```markdown
---
cardTitle: Welcome
---

::card{:title="$doc.cardTitle"}
::
```

## Slots

### Default Slot

Content directly inside the component:

```markdown
::callout
This is the default slot content.
It supports **Markdown** formatting.
::
```

### Named Slots

```markdown
::hero
#title
Welcome to Our Site

#subtitle
Build amazing things with Nuxt

#actions
:button[Get Started]{to="/docs"}
:button[Learn More]{to="/about" variant="outline"}
::
```

### Nested Slots

```markdown
::tabs
  ::tab{label="Preview"}
  Preview content here.
  ::

  ::tab{label="Code"}
  ```ts
  const example = 'code'
  ```
  ::
::
```

## Spans & Attributes

Apply attributes to inline text using `[text]{attributes}`:

```markdown
This is [highlighted text]{.text-primary}.

[Custom styled]{.font-bold .text-lg #my-id style="color: red"}

[Link with class](/about){.nav-link}
```

### Attributes on Standard Markdown

```markdown
**bold text**{.text-red-500}

*italic*{.text-sm}

`inline code`{lang="ts"}

![image alt](/path/to/image.jpg){width="300" loading="lazy"}
```

### Multiple Classes

```markdown
[styled text]{.class-one .class-two .class-three}
```

## Variable Binding

Interpolate frontmatter values in content:

```markdown
---
author: Jane Smith
publishDate: 2024-01-15
version: 2.0.0
---

# {{ $doc.title }}

Written by {{ $doc.author }} on {{ $doc.publishDate }}.

Current version: **{{ $doc.version }}**
```

## Code Blocks

### Basic Syntax Highlighting

```markdown
```typescript
const greeting: string = 'Hello, World!'
console.log(greeting)
```
```

### Filename Display

```markdown
```ts [utils/helpers.ts]
export function formatDate(date: Date): string {
  return date.toLocaleDateString()
}
```
```

### Line Highlighting

```markdown
```ts {2-4,6}
function example() {
  // Lines 2-4 highlighted
  const a = 1
  const b = 2
  // Line 5 not highlighted
  return a + b  // Line 6 highlighted
}
```
```

### Meta String

Combine filename and highlighting:

```markdown
```vue [components/Button.vue] {3-5}
<template>
  <button
    class="btn"
    :class="variant"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>
```
```

### Code Groups

```markdown
::code-group
```bash [npm]
npm install @nuxt/content
```

```bash [pnpm]
pnpm add @nuxt/content
```

```bash [yarn]
yarn add @nuxt/content
```
::
```

## Prose Components

Customize how standard Markdown elements render by creating components in `components/content/`:

| Element | Component | Description |
|---------|-----------|-------------|
| `<p>` | `ProseP` | Paragraphs |
| `<h1>` | `ProseH1` | Heading 1 |
| `<h2>` | `ProseH2` | Heading 2 |
| `<h3>` | `ProseH3` | Heading 3 |
| `<a>` | `ProseA` | Links |
| `<code>` | `ProseCode` | Inline code |
| `<pre>` | `ProsePre` | Code blocks |
| `<ul>` | `ProseUl` | Unordered lists |
| `<ol>` | `ProseOl` | Ordered lists |
| `<li>` | `ProseLi` | List items |
| `<blockquote>` | `ProseBlockquote` | Blockquotes |
| `<img>` | `ProseImg` | Images |
| `<table>` | `ProseTable` | Tables |

## Excerpts

Use `<!--more-->` to define excerpt boundaries:

```markdown
---
title: My Article
---

This is the excerpt that appears in listings.

<!--more-->

This is the full article content that only shows on the detail page.
```

## Practical Component Examples

### Alert/Callout

```markdown
::alert{type="info"}
This is an informational message.
::

::alert{type="warning" icon="heroicons:exclamation-triangle"}
**Warning:** Please read carefully before proceeding.
::

::alert{type="error"}
An error occurred. Please try again.
::

::alert{type="success"}
Operation completed successfully!
::
```

### Card with Slots

```markdown
::card{image="/images/feature.jpg"}
#header
Feature Title

#default
This card showcases a new feature with an image header and action buttons.

#footer
:button[Learn More]{to="/features" variant="link"}
::
```

### Accordion/Collapsible

```markdown
::accordion
  ::accordion-item{title="What is Nuxt Content?"}
  Nuxt Content is a file-based CMS for Nuxt applications.
  ::

  ::accordion-item{title="How do I install it?"}
  Run `npx nuxi module add content` to add it to your project.
  ::
::
```

### Tabs

```markdown
::tabs
  ::tab{label="Vue"}
  ```vue
  <template>
    <div>Hello Vue!</div>
  </template>
  ```
  ::

  ::tab{label="React"}
  ```jsx
  function Hello() {
    return <div>Hello React!</div>
  }
  ```
  ::
::
```

### Badge/Tag

```markdown
Status: :badge[Published]{color="success"} :badge[Featured]{color="primary"}

Tags: :tag[Vue] :tag[Nuxt] :tag[TypeScript]
```

### Icon

```markdown
:icon{name="heroicons:home" class="w-5 h-5"}
:icon{name="lucide:github" size="24"}
:icon{name="mdi:vuejs" class="text-green-500"}
```

### Callout with Icon

```markdown
::callout{icon="heroicons:light-bulb"}
#title
Pro Tip

#default
Use MDC syntax to create rich, interactive documentation with Vue components.
::
```

## Creating Custom Components

Create Vue components in `components/content/` to use in MDC:

```vue
<!-- components/content/Alert.vue -->
<script setup lang="ts">
defineProps<{
  type?: 'info' | 'warning' | 'error' | 'success'
  icon?: string
}>()
</script>

<template>
  <div :class="['alert', `alert-${type}`]">
    <Icon v-if="icon" :name="icon" />
    <slot />
  </div>
</template>
```

Then use in Markdown:

```markdown
::alert{type="info" icon="heroicons:information-circle"}
Custom alert component content.
::
```

## Routing Best Practices

### Avoiding Route Ambiguity with Optional Catch-All Routes
When creating a documentation section or any area using dynamic routes for content, avoid using optional catch-all routes like `[[...slug]].vue` if you also need to support the root path (e.g., `/docs`) and sub-paths (e.g., `/docs/getting-started`) reliably.

Nuxt/Vue Router can have trouble disambiguating the root path when using `[[...slug]].vue`.

**Recommended Pattern:**
Split the implementation into two explicit files:

1. `pages/docs/index.vue` - Handles the root `/docs` path
   ```vue
   <script setup>
   const { data: page } = await useAsyncData('docs-index', () => 
     queryCollection('docs').path('/docs').first()
   )
   // ... handle page not found ...
   </script>
   ```

2. `pages/docs/[...slug].vue` - Handles all nested paths (slug is required)
   ```vue
   <script setup>
   const route = useRoute()
   const slug = route.params.slug.join('/')
   const { data: page } = await useAsyncData(`docs-${slug}`, () => 
     queryCollection('docs').path(`/docs/${slug}`).first()
   )
   // ... handle page not found ...
   </script>
   ```

This ensures predictable routing behavior and prevents 404 errors on the root path.

## References

- [ContentRenderer](https://content.nuxt.com/docs/components/content-renderer) - Render parsed content in templates
- [Custom Components](https://content.nuxt.com/docs/getting-started/components) - Create MDC-compatible Vue components
- [Collections](https://content.nuxt.com/docs/getting-started/collections) - Organize and query content
- [Prose Components](https://content.nuxt.com/docs/components/prose) - Customize default HTML rendering
- [MDC Module](https://github.com/nuxt-modules/mdc) - Underlying MDC parser and syntax
- [Nuxt Content Docs](https://content.nuxt.com/) - Official documentation

