---
name: docusaurus
description: Docusaurus 3.x documentation framework - MDX authoring, theming, versioning, i18n. Use for documentation sites or spec-weave.com.
---

# Docusaurus Expert Skill

Expert in Docusaurus 3.x documentation framework - the modern static site generator for technical documentation, blogs, and landing pages.

## Core Competencies

### 1. Site Setup & Configuration
- **Installation**: Quick start with templates
- **Configuration**: `docusaurus.config.ts` best practices
- **Plugins**: Content, search, analytics, sitemap
- **Themes**: Classic, Material, custom themes
- **Deployment**: GitHub Pages, Netlify, Vercel, AWS

### 2. Content Authoring
- **Markdown**: Standard Markdown with Docusaurus extensions
- **MDX**: React components in Markdown
- **Code Blocks**: Syntax highlighting, live code editors
- **Admonitions**: Notes, tips, warnings, danger alerts
- **Tabs**: Multi-language examples, platform-specific content

### 3. Advanced Features
- **Versioning**: Multi-version documentation management
- **i18n**: Internationalization and localization
- **Search**: Algolia DocSearch, local search plugins
- **Mermaid**: Diagram support with @docusaurus/theme-mermaid
- **OpenAPI**: API documentation with docusaurus-plugin-openapi-docs

### 4. Customization
- **Custom Components**: React components for docs
- **Styling**: CSS modules, Tailwind CSS integration
- **Swizzling**: Customize theme components
- **Plugins**: Custom plugin development

## Quick Start

### Installation

```bash
npx create-docusaurus@latest my-website classic --typescript
cd my-website
npm start
```

### Project Structure

```
my-website/
├── docs/                  # Documentation pages
│   ├── intro.md
│   └── tutorial/
├── blog/                  # Blog posts (optional)
│   └── 2024-01-01-post.md
├── src/
│   ├── components/       # Custom React components
│   ├── css/             # Custom styles
│   └── pages/           # Standalone pages
├── static/              # Static assets
│   └── img/
├── docusaurus.config.ts # Main configuration
├── sidebars.ts          # Sidebar configuration
└── package.json
```

## Configuration

### Basic Configuration

```typescript
// docusaurus.config.ts
import {Config} from '@docusaurus/types';

const config: Config = {
  title: 'My Project',
  tagline: 'Documentation made easy',
  url: 'https://myproject.com',
  baseUrl: '/',

  // GitHub Pages deployment config
  organizationName: 'facebook',
  projectName: 'docusaurus',

  // Theme config
  themeConfig: {
    navbar: {
      title: 'My Project',
      logo: {
        alt: 'My Project Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'doc',
          docId: 'intro',
          position: 'left',
          label: 'Docs',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        {
          href: 'https://github.com/facebook/docusaurus',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Tutorial',
              to: '/docs/intro',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} My Project`,
    },
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/facebook/docusaurus/tree/main/',
        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/facebook/docusaurus/tree/main/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],
};

export default config;
```

## MDX Content Features

### Admonitions

```markdown
:::note
This is a note
:::

:::tip
This is a tip
:::

:::warning
This is a warning
:::

:::danger
This is a danger alert
:::

:::info Custom Title
This is an info box with a custom title
:::
```

### Code Blocks with Features

```markdown
\```typescript title="src/components/HelloWorld.tsx" showLineNumbers {1,3-5}
import React from 'react';

export function HelloWorld() {
  return <h1>Hello World!</h1>;
}
\```
```

### Tabs

```markdown
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="js" label="JavaScript">
    \```js
    const greeting = 'Hello';
    \```
  </TabItem>
  <TabItem value="ts" label="TypeScript">
    \```ts
    const greeting: string = 'Hello';
    \```
  </TabItem>
</Tabs>
```

### Interactive Code Editors

```markdown
\```jsx live
function Clock() {
  const [date, setDate] = useState(new Date());
  useEffect(() => {
    const timerID = setInterval(() => setDate(new Date()), 1000);
    return () => clearInterval(timerID);
  }, []);
  return <div>{date.toLocaleTimeString()}</div>;
}
\```
```

## Plugins

### Essential Plugins

```typescript
// docusaurus.config.ts
plugins: [
  // Multiple docs instances
  [
    '@docusaurus/plugin-content-docs',
    {
      id: 'api',
      path: 'api',
      routeBasePath: 'api',
      sidebarPath: './sidebarsApi.ts',
    },
  ],

  // Sitemap
  [
    '@docusaurus/plugin-sitemap',
    {
      changefreq: 'weekly',
      priority: 0.5,
    },
  ],

  // Google Analytics
  [
    '@docusaurus/plugin-google-gtag',
    {
      trackingID: 'G-XXXXXXXXXX',
      anonymizeIP: true,
    },
  ],
],
```

### Mermaid Diagrams

```bash
npm install @docusaurus/theme-mermaid
```

```typescript
// docusaurus.config.ts
themes: ['@docusaurus/theme-mermaid'],
markdown: {
  mermaid: true,
},
```

```markdown
\```mermaid
graph TD
  A[Start] -->|Process| B[End]
\```
```

### Search

#### Algolia DocSearch

```typescript
themeConfig: {
  algolia: {
    appId: 'YOUR_APP_ID',
    apiKey: 'YOUR_SEARCH_API_KEY',
    indexName: 'YOUR_INDEX_NAME',
  },
},
```

#### Local Search

```bash
npm install @easyops-cn/docusaurus-search-local
```

```typescript
themes: [
  [
    require.resolve('@easyops-cn/docusaurus-search-local'),
    {
      hashed: true,
      language: ['en', 'zh'],
    },
  ],
],
```

## Versioning

### Enable Versioning

```bash
npm run docusaurus docs:version 1.0.0
```

### Version Structure

```
website/
├── docs/               # Current version (Next)
├── versioned_docs/
│   ├── version-1.0.0/  # Version 1.0.0
│   └── version-2.0.0/  # Version 2.0.0
├── versioned_sidebars/
│   ├── version-1.0.0-sidebars.json
│   └── version-2.0.0-sidebars.json
└── versions.json       # List of versions
```

### Version Configuration

```typescript
themeConfig: {
  navbar: {
    items: [
      {
        type: 'docsVersionDropdown',
        position: 'right',
      },
    ],
  },
},
```

## Internationalization (i18n)

### Configuration

```typescript
// docusaurus.config.ts
i18n: {
  defaultLocale: 'en',
  locales: ['en', 'fr', 'es'],
  localeConfigs: {
    en: {
      label: 'English',
    },
    fr: {
      label: 'Français',
    },
    es: {
      label: 'Español',
    },
  },
},
```

### Directory Structure

```
website/
├── i18n/
│   ├── en/
│   │   ├── docusaurus-plugin-content-docs/
│   │   └── docusaurus-theme-classic/
│   ├── fr/
│   └── es/
└── docs/              # Default locale content
```

### Build for Specific Locale

```bash
npm run build -- --locale fr
```

## Custom Components

### Create Component

```tsx
// src/components/FeatureCard.tsx
import React from 'react';
import styles from './styles.module.css';

export function FeatureCard({title, description, icon}) {
  return (
    <div className={styles.featureCard}>
      <div className={styles.icon}>{icon}</div>
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
}
```

### Use in MDX

```markdown
---
title: Features
---

import {FeatureCard} from '@site/src/components/FeatureCard';

# Our Features

<FeatureCard
  title="Fast"
  description="Lightning-fast performance"
  icon="⚡"
/>
```

## Deployment

### GitHub Pages

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - name: Install dependencies
        run: npm ci
      - name: Build website
        run: npm run build
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
```

### Netlify

```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Vercel

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "build"
}
```

## Best Practices

### 1. Organize Content Logically

```
docs/
├── getting-started/
│   ├── installation.md
│   └── quick-start.md
├── guides/
│   ├── beginner/
│   ├── intermediate/
│   └── advanced/
└── reference/
    ├── api/
    └── cli/
```

### 2. Use Frontmatter

```markdown
---
id: my-doc
title: My Document
sidebar_label: Short Label
sidebar_position: 1
description: Document description for SEO
keywords: [docusaurus, documentation, seo]
---
```

### 3. Leverage MDX

```markdown
import MyComponent from '@site/src/components/MyComponent';

<MyComponent prop="value" />
```

### 4. Optimize Images

```markdown
![Alt text](./img/photo.jpg)

<!-- Or with sizing -->
<img src={require('./img/photo.jpg').default} width="600" />
```

### 5. Add Edit Links

```typescript
docs: {
  editUrl: 'https://github.com/org/repo/edit/main/',
},
```

## Troubleshooting

### Build Errors

```bash
# Clear cache
npm run clear
npm run build
```

### Broken Links

```bash
# Check for broken links during build
npm run build -- --debug
```

### Port Already in Use

```bash
PORT=3001 npm start
```

## Resources

- [Official Docs](https://docusaurus.io/)
- [Showcase](https://docusaurus.io/showcase)
- [Discord Community](https://discord.gg/docusaurus)
- [GitHub](https://github.com/facebook/docusaurus)

## Activation Keywords

Ask me about:
- "How do I set up Docusaurus?"
- "Docusaurus configuration best practices"
- "Adding search to Docusaurus"
- "Docusaurus versioning"
- "MDX components in Docusaurus"
- "Deploy Docusaurus to GitHub Pages"
- "Internationalization in Docusaurus"
- "Custom Docusaurus themes"
