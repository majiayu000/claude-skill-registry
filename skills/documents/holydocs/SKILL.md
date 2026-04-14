---
name: holydocs
description: Create and configure HolyDocs documentation projects. Use when the user wants to set up documentation, create a docs site, initialize a docs project, configure docs.json, add MDX pages, or work with HolyDocs in any way. Also trigger when seeing docs.json, holydocs.json, @holydocs/cli, or MDX documentation files in the project. This is the go-to skill for anything related to HolyDocs documentation platform.
---

# HolyDocs Documentation Skill

## Overview

HolyDocs is an AI-native documentation platform built on Cloudflare. Users write docs in MDX, configure with `docs.json`, and deploy via Git push or CLI. Sites are edge-rendered with sub-50ms page loads and include built-in AI search, an AI assistant, and an MCP server for IDE integration.

HolyDocs supports 11 visual themes, 38 MDX components, OpenAPI/AsyncAPI integration, versioning, i18n, auth-gated pages, and analytics integrations out of the box.

## Creating a New Project

Follow these steps when a user wants to create a docs site:

### Step 1: Check for Existing Docs

Look for any of these in the project root or common locations:
- `docs.json` or `holydocs.json` (HolyDocs config)
- `mint.json` (Mintlify config, can be migrated)
- `docs/` directory
- `.holydocs/` directory

If `mint.json` exists, offer to migrate: `holydocs migrate mint`.

### Step 2: Create Directory Structure

```
docs/
  docs.json
  introduction.mdx
  quickstart.mdx
  guides/
    getting-started.mdx
  api/
    overview.mdx
  images/
    logo-light.svg
    logo-dark.svg
```

### Step 3: Generate docs.json

Ask the user for:
1. Project name
2. Primary brand color (hex)
3. Logo (path or URL, light/dark variants if available)
4. Theme preference (show the 11 options)
5. Whether they have an OpenAPI spec

Then generate the config. Minimal working example:

```json
{
  "name": "My Project",
  "theme": "mint",
  "colors": {
    "primary": "#0D9373"
  },
  "logo": {
    "light": "/images/logo-light.svg",
    "dark": "/images/logo-dark.svg"
  },
  "favicon": "/images/favicon.svg",
  "navigation": {
    "tabs": [
      {
        "tab": "Documentation",
        "groups": [
          {
            "group": "Getting Started",
            "pages": ["introduction", "quickstart"]
          },
          {
            "group": "Guides",
            "pages": ["guides/getting-started"]
          }
        ]
      },
      {
        "tab": "API Reference",
        "groups": [
          {
            "group": "API",
            "pages": ["api/overview"]
          }
        ]
      }
    ]
  },
  "topbarCtaButton": {
    "name": "Dashboard",
    "url": "https://example.com/dashboard"
  },
  "footerSocials": {
    "github": "https://github.com/example",
    "twitter": "https://twitter.com/example"
  }
}
```

### Step 4: Create Starter Pages

**introduction.mdx:**
```mdx
---
title: Introduction
description: Welcome to the project documentation.
icon: book-open
---

# Welcome to [Project Name]

A brief overview of what the project does and why it exists.

<CardGroup cols={2}>
  <Card title="Quickstart" icon="rocket" href="/quickstart">
    Get up and running in under 5 minutes.
  </Card>
  <Card title="API Reference" icon="code" href="/api/overview">
    Explore the full API documentation.
  </Card>
</CardGroup>
```

**quickstart.mdx:**
```mdx
---
title: Quickstart
description: Get started in under 5 minutes.
icon: rocket
---

# Quickstart

<Steps>
  <Step title="Install">
    Install the package using your preferred package manager.
    ```bash
    npm install my-package
    ```
  </Step>
  <Step title="Configure">
    Add your configuration.
    ```ts
    import { createClient } from 'my-package';
    const client = createClient({ apiKey: 'your-key' });
    ```
  </Step>
  <Step title="Use">
    Make your first API call.
    ```ts
    const result = await client.hello();
    console.log(result);
    ```
  </Step>
</Steps>
```

### Step 5: Guide Deployment

Tell the user:
1. Push to a Git repository connected to HolyDocs (auto-deploys on push)
2. Or use the CLI: `npx @holydocs/cli deploy`
3. Or deploy from the HolyDocs dashboard

## docs.json Essentials

The `docs.json` file is the single source of configuration. Key fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Project name shown in sidebar and SEO |
| `colors.primary` | string (hex) | Yes | Primary brand color |
| `theme` | string | No | Visual theme (default: `mint`) |
| `logo` | string or object | No | Logo path/URL or `{light, dark, href}` |
| `favicon` | string or object | No | Favicon path or `{light, dark}` |
| `navigation` | object | Yes | Page navigation structure |
| `appearance` | object | No | Light/dark mode settings |
| `topbarLinks` | array | No | Links in the top navigation bar |
| `topbarCtaButton` | object | No | Primary CTA button in topbar |
| `footerSocials` | object | No | Social media links in footer |
| `api.openapi` | string or array | No | OpenAPI spec URL(s) or file path(s) |
| `assistant.enabled` | boolean | No | Enable AI assistant widget |

For the complete docs.json schema, read `references/docs-json-schema.md`.

## MDX Page Format

Every `.mdx` file starts with YAML frontmatter:

```mdx
---
title: Page Title
description: A brief description for SEO and search.
icon: lucide-icon-name
sidebarTitle: Short Title
mode: wide
openapi: GET /api/endpoint
---

Your content here in MDX (Markdown + JSX components).
```

### Frontmatter Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Page title (required) |
| `description` | string | SEO description, shown in search results |
| `icon` | string | Lucide icon name for sidebar |
| `sidebarTitle` | string | Override title shown in sidebar navigation |
| `mode` | `wide` or `default` | Use full-width layout |
| `openapi` | string | Auto-generate from OpenAPI spec (`METHOD /path`) |

## Navigation Patterns

### Flat Groups (Simple)

For small docs with no tabs:

```json
{
  "navigation": {
    "groups": [
      {
        "group": "Getting Started",
        "pages": ["introduction", "quickstart"]
      },
      {
        "group": "Guides",
        "pages": ["guides/auth", "guides/deploy"]
      }
    ]
  }
}
```

### Tabbed Navigation (Larger Sites)

For docs with distinct sections:

```json
{
  "navigation": {
    "tabs": [
      {
        "tab": "Documentation",
        "icon": "book",
        "groups": [
          {
            "group": "Getting Started",
            "pages": ["introduction", "quickstart"]
          }
        ]
      },
      {
        "tab": "API Reference",
        "icon": "code",
        "groups": [
          {
            "group": "Endpoints",
            "pages": ["api/users", "api/projects"]
          }
        ]
      }
    ]
  }
}
```

### Nested Groups

Groups can contain sub-groups for deep hierarchies:

```json
{
  "group": "Authentication",
  "pages": [
    "auth/overview",
    {
      "group": "Providers",
      "pages": ["auth/oauth", "auth/saml", "auth/api-keys"]
    }
  ]
}
```

### OpenAPI Auto-Generation

Add an OpenAPI spec and pages are generated automatically:

```json
{
  "tab": "API Reference",
  "groups": [
    {
      "group": "Users API",
      "openapi": "https://api.example.com/openapi.json"
    }
  ]
}
```

## Key Components (Quick Reference)

HolyDocs ships 38 MDX components. The most commonly used:

| Component | Description |
|-----------|-------------|
| `Callout` | Highlighted message box (note, warning, tip, info, caution, check, danger) |
| `Card` | Clickable card with icon, title, and description |
| `CardGroup` | Grid layout for cards (`cols={2}` or `cols={3}`) |
| `Tabs` / `Tab` | Tabbed content switcher |
| `Steps` / `Step` | Numbered step-by-step instructions |
| `Accordion` | Collapsible content section |
| `AccordionGroup` | Group of exclusive accordions |
| `CodeGroup` | Tabbed code blocks for multiple languages |
| `Expandable` | Show/hide content toggle |
| `Badge` | Inline status/label badge |
| `Banner` | Full-width announcement banner |
| `Tooltip` | Hover tooltip on any element |
| `Icon` | Inline Lucide icon |
| `ParamField` | API parameter documentation field |
| `ResponseField` | API response field documentation |

For all 38 components with full props and examples, read `references/components.md`.

## Theming Quick Reference

Set the theme and customize colors/fonts in `docs.json`:

```json
{
  "theme": "holy",
  "colors": {
    "primary": "#0D9373",
    "light": "#07C983",
    "dark": "#0D9373",
    "background": {
      "light": "#FFFFFF",
      "dark": "#0F1117"
    }
  },
  "fonts": {
    "heading": {
      "family": "Fraunces",
      "weight": 700,
      "source": "google"
    },
    "body": {
      "family": "Inter",
      "weight": 400,
      "source": "google"
    }
  }
}
```

### Available Themes

| Theme | Style |
|-------|-------|
| `mint` | Clean, minimal with green accents (default) |
| `maple` | Warm, editorial with serif headings |
| `palm` | Tropical, vibrant with rounded cards |
| `willow` | Soft, organic with muted tones |
| `linden` | Structured, corporate with tight spacing |
| `almond` | Warm neutrals, cozy and approachable |
| `aspen` | Light, airy with generous whitespace |
| `holy` | Sharp edges, dark sidebar, bordered cards |
| `atlas` | Map-inspired, info-dense with compact layout |
| `nova` | Futuristic, dark-first with neon accents |
| `cipher` | Hacker aesthetic, monospace-heavy |

For full theme details, read `references/themes.md`.

## Deployment

### Git Push (Recommended)

Connect your repository in the HolyDocs dashboard. Every push to the configured branch triggers an automatic build and deploy.

### CLI Deploy

```bash
npx @holydocs/cli login
npx @holydocs/cli deploy
```

### Programmatic Domain Management

Use the authenticated CLI API helper for custom domains:

```bash
npx @holydocs/cli login
npx @holydocs/cli api put /domains/proj_abc123 --json '{"customDomain":"docs.example.com"}'
npx @holydocs/cli api post /domains/proj_abc123/verify
```

To remove a domain:

```bash
npx @holydocs/cli api delete /domains/proj_abc123
```

### Dashboard Deploy

Click "Deploy" in the HolyDocs dashboard to trigger a manual build from the latest commit.

### Preview Deployments

Every pull request gets a unique preview URL automatically. Preview URLs follow the pattern: `preview-{pr-number}.{project}.holydocs.com`.

## API Documentation

### OpenAPI Integration

Add your OpenAPI spec to auto-generate API reference pages:

```json
{
  "api": {
    "openapi": "https://api.example.com/openapi.json",
    "playground": {
      "display": "interactive",
      "proxy": "https://api.example.com"
    }
  }
}
```

You can also use a local file path: `"openapi": "./openapi.yaml"`

Multiple specs are supported as an array:
```json
{
  "api": {
    "openapi": [
      "./specs/users-api.yaml",
      "./specs/billing-api.yaml"
    ]
  }
}
```

### AsyncAPI

For event-driven APIs, use AsyncAPI specs the same way:
```json
{
  "api": {
    "asyncapi": "./asyncapi.yaml"
  }
}
```

## AI Features

### AI Assistant

Enable the embedded AI assistant widget that answers questions using your docs:

```json
{
  "assistant": {
    "enabled": true,
    "name": "Docs AI",
    "greeting": "Hi! Ask me anything about our docs.",
    "suggestedQuestions": [
      "How do I get started?",
      "What authentication methods are supported?"
    ],
    "position": "bottom-right"
  }
}
```

### AI Search

Automatic on all plans. Combines keyword and semantic search across all pages, including API endpoints.

### MCP Server

Automatic for Starter plan and above. Provides a Model Context Protocol server so IDEs (Claude Code, Cursor, Windsurf) can query your docs programmatically. The MCP endpoint is:

```
https://{project}.holydocs.com/mcp
```

## Reference Pointers

- For the complete docs.json schema, read `references/docs-json-schema.md`
- For all 38 MDX components with props, read `references/components.md`
- For all 11 themes, read `references/themes.md`
- For CLI commands, read `references/cli.md`
