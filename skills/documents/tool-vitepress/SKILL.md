---
version: 1.0.0
name: tool-vitepress
description: >
  Set up and manage VitePress documentation site with Mermaid diagram support.
  Use when the user says "render the docs", "start the docs site", "build documentation",
  "preview docs", or "set up VitePress".
disable-model-invocation: false
user-invocable: true
argument-hint: "[init|dev|build|preview]"
---

# VitePress Documentation Site

## Commands

### `init` — First-time setup

1. Check if `package.json` exists in the project root
2. If not, initialize with:
   ```bash
   npm init -y
   npm install -D vitepress vitepress-plugin-mermaid mermaid
   ```
3. Create `.vitepress/config.mts` if it doesn't exist (see Config section below)
4. Add scripts to `package.json`:
   ```json
   {
     "scripts": {
       "docs:dev": "vitepress dev docs",
       "docs:build": "vitepress build docs",
       "docs:preview": "vitepress preview docs"
     }
   }
   ```
5. Create `docs/index.md` as the landing page if it doesn't exist

### `dev` — Start development server

```bash
npm run docs:dev
```

Opens at `http://localhost:5173`. Hot-reloads on file changes.

### `build` — Build static site

```bash
npm run docs:build
```

Output goes to `docs/.vitepress/dist/`.

### `preview` — Preview built site

```bash
npm run docs:build && npm run docs:preview
```

## Config

The VitePress config at `docs/.vitepress/config.mts` should include:

```typescript
import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

export default withMermaid(
  defineConfig({
    title: 'Project Documentation',
    description: 'Architecture, decisions, and operational docs',
    themeConfig: {
      nav: [
        { text: 'PRDs', link: '/prd/' },
        { text: 'RFCs', link: '/rfc/' },
        { text: 'ADRs', link: '/adr/' },
        { text: 'Design', link: '/design/' },
        { text: 'Architecture', link: '/architecture/' },
        { text: 'Runbooks', link: '/runbooks/' },
      ],
      sidebar: 'auto',
      search: { provider: 'local' },
    },
    mermaid: {},
  })
)
```

## Directory Structure

VitePress serves from `docs/` by default. The skill expects this structure:

```
docs/
├── .vitepress/
│   └── config.mts
├── index.md              # Landing page
├── prd/                  # Product requirements
├── rfc/                  # Request for comments
├── adr/                  # Architecture decision records
├── design/               # Design documents
├── architecture/         # C4 diagrams and architecture docs
├── runbooks/             # Operational runbooks
├── postmortems/          # Incident post-mortems
└── spikes/               # Research spikes
```

## Tips

- Mermaid diagrams render automatically in fenced code blocks with `mermaid` language tag
- C4 diagrams (C4Context, C4Container, C4Component) are supported via the Mermaid plugin
- Use `[[toc]]` in any markdown file to generate a table of contents
- VitePress auto-generates sidebar from file structure when `sidebar: 'auto'`
- Add frontmatter to any doc for custom titles: `---\ntitle: My Custom Title\n---`
