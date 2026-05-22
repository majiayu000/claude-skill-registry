---
name: rspress-frontmatter
description: Configure RSPress frontmatter for documentation pages. Use when setting up page metadata, controlling layout options, or configuring home page hero/features sections.
allowed-tools: Read, Write, Edit, Glob
agent: rspress-doc-agent
---

# RSPress Frontmatter Configuration

Configure YAML frontmatter in RSPress markdown/mdx files to control page
metadata, layout, and special page types.

## Core Metadata Fields

| Field | Type | Description |
| ----- | ---- | ----------- |
| `title` | string | Page title (overrides H1 heading) |
| `description` | string | Page description for SEO meta tags |
| `titleSuffix` | string | Custom suffix for page title |

## Page Layout Control

| Field | Type | Description |
| --------- | ------- | ----------- |
| `pageType` | string | Page type: `doc`, `home`, `blank`, `custom` |
| `sidebar` | boolean | Show/hide sidebar (default: true) |
| `outline` | boolean | Show/hide table of contents outline (default: true) |
| `footer` | boolean | Show/hide footer (default: true) |
| `navbar` | boolean | Show/hide navigation bar (default: true) |

## Overview Page Configuration

Configure automatic overview pages that list child pages:

```yaml
---
pageType: overview
overview: true
overviewHeaders:
  - 2
  - 3
---
```

## Home Page Configuration

Configure hero sections and feature cards:

```yaml
---
pageType: home
hero:
  name: Project Name
  text: Tagline text
  tagline: Subtitle description
  actions:
    - text: Get Started
      link: /guide/getting-started
      theme: brand
    - text: View on GitHub
      link: https://github.com/user/repo
      theme: alt
features:
  - title: Feature One
    details: Description of first feature
    icon: 🚀
  - title: Feature Two
    details: Description of second feature
    icon: ⚡
---
```

## Common Examples

**Standard documentation page:**

```yaml
---
title: Getting Started
description: Learn how to install and configure the project
sidebar: true
outline: true
---
```

**Home page:**

```yaml
---
pageType: home
title: Welcome
navbar: true
sidebar: false
hero:
  name: My Project
  text: Build amazing things
  tagline: Fast, flexible, and powerful
---
```

**API reference page:**

```yaml
---
title: API Reference
description: Complete API documentation
outline: true
pageType: doc
---
```

**Blank page (custom layout):**

```yaml
---
pageType: blank
navbar: false
sidebar: false
footer: false
---
```

**Overview page:**

```yaml
---
title: Guides
pageType: overview
overview: true
---
```

## Notes

* Frontmatter must be at the very top of the file
* All frontmatter blocks must use triple-dash (`---`) delimiters
* Use YAML syntax for all field values
* Boolean values should be lowercase: `true`, `false`
* The `title` field overrides the first H1 heading in the document
