---
name: docs-creator
description: Create and organize public documentation pages using Fumadocs. Use when building new documentation pages or organizing existing ones.
---

# Documentation Creator Skill

This skill helps you build public-facing documentation in `src/content/docs`. The system is powered by [Fumadocs](https://fumadocs.dev) and supports MDX, automatic routing, and Lucide icons.

## Core Concepts

### 1. File Structure
-   **Root**: `src/content/docs/`
-   **Pages**: `.mdx` files become pages (e.g., `getting-started.mdx` -> `/docs/getting-started`).
-   **Nested**: Folders create URL segments (e.g., `api/auth.mdx` -> `/docs/api/auth`).
-   **Images**: Automatic OG image generation is enabled.

### 2. Frontmatter
Every `.mdx` file should have frontmatter:

```yaml
---
title: Page Title
description: A short description for SEO and search
icon: Box # Lucide icon name
---
```

### 3. Folder Organization (`meta.json`)
Control sidebar order, group titles, and icons by placing a `meta.json` in any directory.

```json
{
  "title": "Section Name",
  "icon": "Settings",
  "pages": [
    "index",           // Matches index.mdx
    "getting-started", // Matches getting-started.mdx
    "---Separator---", // Adds a visual separator
    "advanced"         // Matches advanced/ folder or file
  ],
  "defaultOpen": true
}
```

## Features

-   **Lucide Icons**: Use any [Lucide icon name](https://lucide.dev/icons) in frontmatter `icon: Name`.
-   **Components**: All standard MDX components + Fumadocs UI components (Callout, Cards, Tabs) are available.
-   **Relative Links**: `[Link](./other-page)` works correctly.
-   **Sitemap**: Automatically generated.

## Examples

### Basic Page (`src/content/docs/introduction.mdx`)
```mdx
---
title: Introduction
description: Getting started with our platform
icon: BookOpen
---

# Welcome

This is the introduction page.

## Next Steps
- [Installation](./installation)
- [Configuration](./config)
```

### Folder Metadata (`src/content/docs/api/meta.json`)
```json
{
  "title": "API Reference",
  "icon": "Webhook",
  "root": true, 
  "pages": ["introduction", "endpoints", "authentication"]
}
```
*Note: `"root": true` makes this folder a separate tab in the sidebar if using root-level folders.*

