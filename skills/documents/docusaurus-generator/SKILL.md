---
name: docusaurus-generator
description: Generate end-user documentation site using Docusaurus 3.x from the current project. Use this skill when the user asks to create documentation, generate docs, build a docs site, or set up Docusaurus for their project. Supports analyzing project structure, generating markdown docs, configuring Docusaurus, and creating user guides.
---

# Docusaurus Generator

This skill generates end-user documentation using Docusaurus 3.x by analyzing the current project.

## Workflow Overview

1. **Analyze** the project structure to understand what to document
2. **Initialize** a new Docusaurus 3.x project (or use existing)
3. **Generate** documentation content from project analysis
4. **Configure** Docusaurus settings and theme
5. **Build & Preview** the documentation site

## Step 1: Analyze Project

Before generating docs, analyze the project to identify:

- **Package structure**: Check `package.json`, monorepo setup
- **Existing docs**: Look for `docs/`, `README.md`, JSDoc comments
- **Features**: Identify main features from routes, components, APIs
- **Configuration**: Check for config files that reveal functionality

```bash
# Key files to examine
find . -name "README.md" -o -name "*.md" | head -20
ls -la docs/ 2>/dev/null
cat package.json | jq '.name, .description'
```

## Step 2: Initialize Docusaurus

Create a new Docusaurus 3.x project in `docs-site/` directory:

```bash
npx -y create-docusaurus@latest docs-site classic --typescript
```

Or if docs already exist, skip to configuration.

## Step 3: Generate Documentation Content

### Documentation Structure

Organize docs following this structure:

```
docs-site/docs/
├── intro.md                    # Getting started
├── installation.md             # Installation guide
├── features/
│   ├── feature-1.md
│   └── feature-2.md
├── guides/
│   ├── quick-start.md
│   └── advanced-usage.md
├── configuration/
│   └── settings.md
└── faq.md
```

### Frontmatter Template

Every doc should have proper frontmatter:

```markdown
---
sidebar_position: 1
title: Page Title
description: Brief description for SEO
---

# Page Title

Content here...
```

### Content Guidelines

- **Write for end users**, not developers
- Use simple, clear language
- Include screenshots for UI features
- Add code examples where relevant
- Link between related docs

## Step 4: Configure Docusaurus

### docusaurus.config.ts

Key configuration options:

```typescript
import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';

const config: Config = {
  title: 'Project Name',
  tagline: 'Your tagline here',
  favicon: 'img/favicon.ico',
  url: 'https://your-docs-url.com',
  baseUrl: '/',
  
  // Localization
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'vi'],
  },
  
  themeConfig: {
    navbar: {
      title: 'Project Name',
      logo: {
        alt: 'Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Docs',
        },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `Copyright © ${new Date().getFullYear()}`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  },
};

export default config;
```

### Theme Customization

Edit `src/css/custom.css` for branding:

```css
:root {
  --ifm-color-primary: #2e8555;
  --ifm-color-primary-dark: #29784c;
  --ifm-color-primary-darker: #277148;
  --ifm-color-primary-darkest: #205d3b;
  --ifm-color-primary-light: #33925d;
  --ifm-color-primary-lighter: #359962;
  --ifm-color-primary-lightest: #3cad6e;
  --ifm-code-font-size: 95%;
}

[data-theme='dark'] {
  --ifm-color-primary: #25c2a0;
}
```

## Step 5: Build & Preview

```bash
cd docs-site

# Install dependencies
npm install

# Start dev server
npm run start

# Build for production
npm run build

# Serve production build locally
npm run serve
```

## Common Plugins

### Search (Algolia or local)

For local search without Algolia:

```bash
npm install @easyops-cn/docusaurus-search-local
```

```typescript
// docusaurus.config.ts
themes: [
  [
    '@easyops-cn/docusaurus-search-local',
    {
      hashed: true,
      language: ['en', 'vi'],
    },
  ],
],
```

### Blog

Already included in classic template. Configure in `docusaurus.config.ts`:

```typescript
blog: {
  showReadingTime: true,
  blogSidebarCount: 'ALL',
},
```

### Versioning

```bash
npm run docusaurus docs:version 1.0.0
```

## Multi-language Support

### Enable i18n

1. Configure locales in `docusaurus.config.ts`
2. Create translated docs in `i18n/vi/docusaurus-plugin-content-docs/current/`
3. Add locale switcher to navbar

```typescript
navbar: {
  items: [
    {
      type: 'localeDropdown',
      position: 'right',
    },
  ],
},
```

### Translation workflow

```bash
# Generate translation files
npm run write-translations -- --locale vi

# Start dev server with locale
npm run start -- --locale vi
```

## Best Practices

1. **Keep intro short** - Users want to get started quickly
2. **Use admonitions** for tips, warnings:
   ```markdown
   :::tip
   Pro tip here
   :::
   
   :::warning
   Be careful about this
   :::
   ```
3. **Add images** to `static/img/` and reference as `/img/filename.png`
4. **Use tabs** for platform-specific content:
   ```jsx
   import Tabs from '@theme/Tabs';
   import TabItem from '@theme/TabItem';
   
   <Tabs>
     <TabItem value="npm" label="npm">npm install</TabItem>
     <TabItem value="yarn" label="Yarn">yarn add</TabItem>
   </Tabs>
   ```
5. **Auto-generate sidebar** from folder structure using `sidebars.ts`
