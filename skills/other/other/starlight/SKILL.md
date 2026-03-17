---
name: starlight
version: "1.0.0"
description: Starlight - Full-featured documentation theme built on Astro for creating beautiful, accessible, high-performance documentation websites with built-in search, i18n, and customizable components
---

# Starlight Skill

**Starlight** is a full-featured documentation theme built on top of the Astro framework. It provides everything needed to create professional documentation sites with minimal configuration - from built-in search and internationalization to customizable components and dark mode support.

**Key Value Proposition**: Build beautiful, accessible, high-performance documentation websites with Astro's speed and Starlight's comprehensive feature set. Used by 10,300+ projects with 7,700+ GitHub stars.

## When to Use This Skill

- Creating documentation websites for projects, APIs, or products
- Building technical documentation with code examples and syntax highlighting
- Setting up multilingual documentation sites with i18n support
- Developing landing pages with splash templates
- Implementing searchable documentation with Pagefind integration
- Customizing documentation themes with CSS or Tailwind
- Migrating existing docs to a modern static site generator
- Creating developer portals or knowledge bases

## When NOT to Use This Skill

- For blog-focused sites (use Astro's blog template instead)
- For e-commerce or dynamic web applications (use full-stack frameworks)
- For single-page applications requiring client-side routing (use React/Vue/Svelte)
- For sites requiring server-side rendering on every request (use Next.js/Nuxt)
- For non-documentation content-heavy sites (use general Astro templates)

---

## Core Concepts

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Starlight Site                          │
└─────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│                      Content Layer                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ Markdown │  │   MDX    │  │ Markdoc  │  │  Frontmatter  │  │
│  │  (.md)   │  │  (.mdx)  │  │ (.mdoc)  │  │    (YAML)     │  │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────┘  │
└───────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────┐
│                    Starlight Features                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ Sidebar  │  │  Search  │  │   i18n   │  │  Components   │  │
│  │Navigation│  │(Pagefind)│  │ (20+lang)│  │ (Tabs,Cards)  │  │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────┘  │
└───────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────┐
│                      Astro Build                               │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Static HTML + CSS + Optimized Assets + Sitemap + RSS    │ │
│  └──────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────┐
│                      Deployment                                │
│  Vercel | Netlify | Cloudflare Pages | GitHub Pages | Static  │
└───────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Framework** | Astro | Static site generation with island architecture |
| **Content** | Markdown/MDX/Markdoc | Documentation authoring formats |
| **Styling** | CSS/Tailwind | Custom theming and styling |
| **Search** | Pagefind | Client-side full-text search |
| **i18n** | Built-in | 20+ language translations |
| **Syntax Highlighting** | Expressive Code | Code blocks with line highlighting |
| **Components** | Astro Components | Reusable UI elements |
| **Build** | Vite | Fast development and production builds |

---

## Installation

### Prerequisites

- Node.js 18.17.1 or 20.3.0 or higher (v19 not supported)
- npm, pnpm, or Yarn package manager

### Quick Start

```bash
# Create new Starlight project (npm)
npm create astro@latest -- --template starlight

# Create new Starlight project (pnpm)
pnpm create astro --template starlight

# Create new Starlight project (Yarn)
yarn create astro --template starlight
```

### With Tailwind CSS

```bash
# Create with Tailwind pre-configured
npm create astro@latest -- --template starlight/tailwind
```

### With Markdoc

```bash
# Create with Markdoc support
npm create astro@latest -- --template starlight/markdoc
```

### Development Server

```bash
# Start development server
npm run dev

# Or with pnpm/yarn
pnpm dev
yarn dev
```

The development server starts at `http://localhost:4321` with hot reload.

### Build for Production

```bash
# Build static site
npm run build

# Preview production build
npm run preview
```

---

## Project Structure

```
my-docs/
├── public/
│   └── favicon.svg              # Static favicon
│
├── src/
│   ├── assets/
│   │   └── logo.svg             # Site logo
│   │
│   ├── components/
│   │   └── CustomCard.astro     # Custom components
│   │
│   ├── content/
│   │   ├── docs/                # Documentation pages
│   │   │   ├── index.mdx        # Homepage
│   │   │   ├── getting-started.md
│   │   │   └── guides/
│   │   │       ├── 01-installation.md
│   │   │       └── 02-configuration.md
│   │   │
│   │   ├── i18n/                # Translation files (optional)
│   │   │   ├── ar.json
│   │   │   └── zh-CN.json
│   │   │
│   │   └── content.config.ts    # Content collection config
│   │
│   └── styles/
│       └── custom.css           # Custom styles
│
├── astro.config.mjs             # Astro + Starlight configuration
├── package.json
└── tsconfig.json
```

---

## Configuration

### Basic Configuration

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: 'My Documentation',
      description: 'Learn how to use our product',

      // Logo configuration
      logo: {
        src: './src/assets/logo.svg',
        replacesTitle: true,  // Hide text title
      },

      // Social links in header
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/user/repo' },
        { icon: 'discord', label: 'Discord', href: 'https://discord.gg/...' },
      ],

      // Enable edit links
      editLink: {
        baseUrl: 'https://github.com/user/repo/edit/main/',
      },

      // Custom CSS
      customCss: ['./src/styles/custom.css'],

      // Sidebar navigation
      sidebar: [
        { slug: 'getting-started' },
        {
          label: 'Guides',
          autogenerate: { directory: 'guides' },
        },
        {
          label: 'Reference',
          items: [
            { slug: 'reference/api' },
            { label: 'External', link: 'https://example.com' },
          ],
        },
      ],
    }),
  ],
});
```

### Sidebar Configuration

```javascript
// Manual sidebar with groups
sidebar: [
  // Single page link
  { slug: 'introduction' },

  // Group with manual items
  {
    label: 'Getting Started',
    items: [
      { slug: 'installation' },
      { slug: 'configuration' },
    ],
  },

  // Auto-generated from directory
  {
    label: 'Guides',
    autogenerate: { directory: 'guides' },
    collapsed: true,  // Start collapsed
  },

  // With badge
  {
    slug: 'api-reference',
    badge: { text: 'New', variant: 'tip' },
  },

  // With translations
  {
    label: 'Resources',
    translations: { 'pt-BR': 'Recursos' },
    items: [...],
  },
]
```

### Logo Variants (Light/Dark)

```javascript
logo: {
  light: './src/assets/logo-light.svg',
  dark: './src/assets/logo-dark.svg',
  alt: 'My Project Logo',
}
```

### Table of Contents

```javascript
// Global setting
tableOfContents: {
  minHeadingLevel: 2,
  maxHeadingLevel: 3
}

// Or disable globally
tableOfContents: false
```

---

## Authoring Content

### Frontmatter Options

```yaml
---
# Required
title: Page Title

# Optional metadata
description: SEO description for the page
slug: custom-url-path

# Layout options
template: doc           # 'doc' (default) or 'splash' (landing page)
tableOfContents: false  # Disable ToC for this page

# Hero section (for splash pages)
hero:
  title: Welcome to My Docs
  tagline: Beautiful documentation made easy
  image:
    file: ../../assets/hero.png
    alt: Hero illustration
  actions:
    - text: Get Started
      link: /getting-started/
      icon: right-arrow
      variant: primary
    - text: View on GitHub
      link: https://github.com/user/repo
      variant: secondary

# Sidebar customization
sidebar:
  label: Custom Sidebar Label
  order: 1              # Sort order in autogenerated sidebar
  badge:
    text: Beta
    variant: caution    # note, tip, caution, danger, success
  hidden: false         # Hide from sidebar

# Navigation
prev: false             # Disable previous page link
next:
  link: /next-page/
  label: Continue to Next

# Content management
lastUpdated: 2026-01-12
editUrl: false          # Disable edit link for this page
draft: true             # Exclude from production
pagefind: false         # Exclude from search
---
```

### Markdown Formatting

```markdown
## Headings (H2-H6)

**Bold text** and *italic text* and ~~strikethrough~~

`inline code` for technical terms

[Internal link](/guides/setup/)
[External link](https://example.com)

> Blockquote for important notes

- Unordered list
- Another item

1. Ordered list
2. Second item
```

### Asides (Callouts)

```markdown
:::note
This is a note callout for general information.
:::

:::tip
Helpful tips and best practices go here.
:::

:::caution
Warnings about potential issues.
:::

:::danger
Critical warnings about breaking changes or security issues.
:::

:::tip[Custom Title]
You can customize the callout title.
:::
```

### Code Blocks with Expressive Code

```markdown
```javascript title="config.js"
// Basic code block with title
export const config = {
  name: 'My App',
};
```

```typescript {2-3} ins={5} del={6}
// Line highlighting and diff markers
function example() {
  const highlighted = true;
  const alsoHighlighted = true;
  const inserted = 'new line';  // Added
  const deleted = 'old line';   // Removed
}
```

```bash frame="terminal" title="Installing dependencies"
npm install @astrojs/starlight
```
```

### Details/Accordion

```html
<details>
<summary>Click to expand</summary>

This content is hidden by default.

You can include **Markdown** formatting inside.

</details>
```

---

## Built-in Components

### Importing Components

```mdx
---
title: Using Components
---

import { Tabs, TabItem, Card, CardGrid, LinkCard, Badge, Icon, Steps, FileTree } from '@astrojs/starlight/components';
```

### Tabs

```mdx
<Tabs>
  <TabItem label="npm">
    ```bash
    npm install package
    ```
  </TabItem>
  <TabItem label="pnpm">
    ```bash
    pnpm add package
    ```
  </TabItem>
  <TabItem label="yarn">
    ```bash
    yarn add package
    ```
  </TabItem>
</Tabs>
```

### Cards and Card Grids

```mdx
<CardGrid>
  <Card title="Getting Started" icon="rocket">
    Learn the basics of setting up your project.
  </Card>
  <Card title="Configuration" icon="setting">
    Customize your documentation site.
  </Card>
</CardGrid>

<LinkCard
  title="View on GitHub"
  description="Check out the source code"
  href="https://github.com/user/repo"
/>
```

### Steps

```mdx
<Steps>

1. Install the package

   ```bash
   npm install my-package
   ```

2. Configure your project

   Add the configuration to your file.

3. Start building

   You're ready to go!

</Steps>
```

### File Tree

```mdx
<FileTree>
- src/
  - components/
    - Header.astro
    - Footer.astro
  - content/
    - docs/
      - index.md
      - **getting-started.md** (highlighted)
  - styles/
    - global.css
- astro.config.mjs
- package.json
</FileTree>
```

### Badges

```mdx
<Badge text="New" variant="tip" />
<Badge text="Deprecated" variant="caution" />
<Badge text="v2.0" variant="note" />
```

### Icons

```mdx
<Icon name="star" />
<Icon name="rocket" size="1.5rem" />
<Icon name="github" />
```

---

## Internationalization (i18n)

### Configuration

```javascript
// astro.config.mjs
starlight({
  title: 'My Docs',
  defaultLocale: 'en',
  locales: {
    // Root locale (no prefix in URLs)
    root: {
      label: 'English',
      lang: 'en',
    },
    // Other locales
    'zh-cn': {
      label: '简体中文',
      lang: 'zh-CN',
    },
    ar: {
      label: 'العربية',
      dir: 'rtl',  // Right-to-left support
    },
    pt: {
      label: 'Português',
      lang: 'pt-BR',
    },
  },
})
```

### Directory Structure for i18n

```
src/content/docs/
├── index.md              # English (root locale)
├── getting-started.md
├── zh-cn/
│   ├── index.md          # Chinese
│   └── getting-started.md
├── ar/
│   ├── index.md          # Arabic
│   └── getting-started.md
└── pt/
    ├── index.md          # Portuguese
    └── getting-started.md
```

### Translating UI Strings

```typescript
// src/content/content.config.ts
import { defineCollection } from 'astro:content';
import { docsLoader, i18nLoader } from '@astrojs/starlight/loaders';
import { docsSchema, i18nSchema } from '@astrojs/starlight/schema';

export const collections = {
  docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),
  i18n: defineCollection({ loader: i18nLoader(), schema: i18nSchema() }),
};
```

```json
// src/content/i18n/zh-CN.json
{
  "search.label": "搜索",
  "tableOfContents.onThisPage": "本页目录",
  "i18n.untranslatedContent": "此内容尚未翻译。"
}
```

### Multilingual Title

```javascript
title: {
  en: 'My Documentation',
  'zh-CN': '我的文档',
  ar: 'وثائقي',
}
```

---

## Styling and Customization

### Custom CSS

```css
/* src/styles/custom.css */

/* Override CSS custom properties */
:root {
  --sl-color-accent-low: #1e1b4b;
  --sl-color-accent: #4f46e5;
  --sl-color-accent-high: #a5b4fc;

  --sl-color-text-accent: #818cf8;
  --sl-font: 'Inter', sans-serif;
  --sl-font-mono: 'Fira Code', monospace;

  /* Adjust content width */
  --sl-content-width: 50rem;
}

/* Dark mode overrides */
:root[data-theme='dark'] {
  --sl-color-accent-low: #312e81;
  --sl-color-accent: #6366f1;
}
```

### Custom Fonts

```javascript
// astro.config.mjs
customCss: [
  '@fontsource/inter/400.css',
  '@fontsource/inter/600.css',
  '@fontsource/fira-code/400.css',
  './src/styles/custom.css',
]
```

```css
/* src/styles/custom.css */
:root {
  --sl-font: 'Inter', sans-serif;
  --sl-font-mono: 'Fira Code', monospace;
}
```

### Tailwind CSS Integration

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  integrations: [
    starlight({
      title: 'Docs with Tailwind',
      customCss: ['./src/styles/tailwind.css'],
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});
```

```css
/* src/styles/tailwind.css */
@layer base, starlight, theme, components, utilities;
@import '@astrojs/starlight-tailwind';
@import 'tailwindcss/theme.css' layer(theme);
@import 'tailwindcss/utilities.css' layer(utilities);
```

---

## Overriding Components

### Replace a Component

```javascript
// astro.config.mjs
starlight({
  title: 'My Docs',
  components: {
    // Override the footer
    Footer: './src/components/CustomFooter.astro',
    // Override social icons
    SocialIcons: './src/components/MySocialLinks.astro',
  },
})
```

### Custom Component with Original

```astro
---
// src/components/CustomFooter.astro
import DefaultFooter from '@astrojs/starlight/components/Footer.astro';
---

<DefaultFooter>
  <slot />
</DefaultFooter>

<div class="custom-footer-addition">
  <p>Built with Starlight</p>
</div>
```

### Conditional Rendering

```astro
---
// src/components/ConditionalFooter.astro
import Default from '@astrojs/starlight/components/Footer.astro';
const isHomepage = Astro.locals.starlightRoute.id === '';
---

{isHomepage ? (
  <footer class="custom-homepage-footer">
    <p>Welcome to our documentation!</p>
  </footer>
) : (
  <Default><slot /></Default>
)}
```

### Available Override Points

| Component | Location |
|-----------|----------|
| `Header` | Site header with logo and navigation |
| `Footer` | Page footer |
| `Sidebar` | Sidebar navigation |
| `PageTitle` | Page title component |
| `TableOfContents` | Right sidebar table of contents |
| `SocialIcons` | Social media links |
| `Search` | Search component |
| `ThemeSelect` | Dark/light mode toggle |
| `LanguageSelect` | Language switcher |
| `PageFrame` | Overall page layout |
| `TwoColumnContent` | Main content area |

---

## Deployment

### Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod
```

### Cloudflare Pages

```bash
# Build and deploy
npm run build
wrangler pages deploy ./dist
```

### GitHub Pages

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

### Static Hosting with Base Path

```javascript
// astro.config.mjs
export default defineConfig({
  site: 'https://user.github.io',
  base: '/my-repo/',
  integrations: [starlight({ title: 'My Docs' })],
});
```

---

## Troubleshooting

### Common Issues

**Build fails with content collection error:**
```bash
# Clear Astro cache and rebuild
rm -rf .astro
npm run build
```

**Styles not updating in development:**
```bash
# Restart dev server with cache clear
npm run dev -- --force
```

**Search not working:**
```bash
# Ensure pagefind is building
npm run build
# Check dist/_pagefind/ directory exists
```

**i18n pages not found:**
- Verify directory structure matches locale configuration
- Check that `defaultLocale` matches your root content

**Components not importing:**
```javascript
// Ensure MDX is being used for component imports
// Rename .md to .mdx for component usage
```

### Updating Starlight

```bash
# Update all Astro packages
npx @astrojs/upgrade

# Or with pnpm
pnpm dlx @astrojs/upgrade
```

---

## Resources

### Official Documentation
- [Starlight Docs](https://starlight.astro.build/)
- [Astro Documentation](https://docs.astro.build/)
- [GitHub Repository](https://github.com/withastro/starlight)

### Community
- [Astro Discord](https://astro.build/chat) - #starlight channel
- [GitHub Discussions](https://github.com/withastro/starlight/discussions)

### Examples
- [Starlight Showcase](https://starlight.astro.build/resources/showcase/)
- [Community Plugins](https://starlight.astro.build/resources/plugins/)
- [Community Themes](https://starlight.astro.build/resources/themes/)

### Related Technologies
- [Expressive Code](https://expressive-code.com/) - Code block syntax highlighting
- [Pagefind](https://pagefind.app/) - Static search
- [Astro](https://astro.build/) - Web framework

---

## Version History

- **1.0.0** (2026-01-12): Initial skill release
  - Complete Starlight documentation framework coverage
  - Installation and project structure
  - Configuration options (sidebar, i18n, customization)
  - Content authoring (frontmatter, Markdown, MDX)
  - Built-in components (Tabs, Cards, Steps, FileTree)
  - Internationalization with 20+ languages
  - CSS and Tailwind styling
  - Component overriding
  - Deployment guides
  - Troubleshooting
