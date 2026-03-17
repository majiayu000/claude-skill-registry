---
name: dewey-docs
description: Generate AI-agent-ready documentation using Dewey. Use when asked to "set up docs", "create documentation", "make docs agent-friendly", "generate AGENTS.md", or "add llms.txt".
---

# Dewey Documentation Toolkit

Dewey generates AI-agent-ready documentation for software projects. It creates AGENTS.md, llms.txt, docs.json, and install.md files that AI coding agents can consume effectively.

## When to Use

Activate this skill when the user asks to:
- "Set up documentation for my project"
- "Make my docs AI-friendly"
- "Generate AGENTS.md"
- "Create an llms.txt file"
- "Add agent-ready docs"
- "Set up Dewey"

## Installation

```bash
pnpm add @arach/dewey
# or
npm install @arach/dewey
```

## CLI Commands

| Command | Purpose |
|---------|---------|
| `dewey init` | Create docs/ folder and dewey.config.ts |
| `dewey audit` | Check documentation completeness |
| `dewey generate` | Create AGENTS.md, llms.txt, docs.json, install.md |
| `dewey agent` | Score agent-readiness (0-100 scale) |

## Quick Setup

```bash
# 1. Install
pnpm add @arach/dewey

# 2. Initialize
npx dewey init

# 3. Generate agent files
npx dewey generate
```

This creates:
```
docs/
├── overview.md
├── quickstart.md
├── AGENTS.md        # Combined agent context
└── llms.txt         # Plain text summary
dewey.config.ts      # Configuration
```

## Configuration (dewey.config.ts)

```typescript
import { defineConfig } from '@arach/dewey'

export default defineConfig({
  project: {
    name: 'my-project',
    tagline: 'A brief description',
    type: 'npm-package', // or 'cli-tool', 'macos-app', 'react-library', 'monorepo', 'generic'
  },

  agent: {
    // Critical rules agents MUST follow
    criticalContext: [
      'Always use TypeScript',
      'Run tests before committing',
    ],

    // Key directories for navigation
    entryPoints: {
      'Source': 'src/',
      'Tests': 'tests/',
      'Config': 'config/',
    },

    // Pattern-based instructions
    rules: [
      { pattern: '*.test.ts', instruction: 'Use vitest for testing' },
      { pattern: 'src/api/*', instruction: 'Follow REST conventions' },
    ],

    // Docs to include in AGENTS.md
    sections: ['overview', 'quickstart', 'api'],
  },

  docs: {
    path: './docs',
    output: './',
    required: ['overview.md', 'quickstart.md'],
  },

  // For install.md generation (installmd.org standard)
  install: {
    objective: 'Set up the development environment',
    doneWhen: {
      command: 'npm test',
      expectedOutput: 'All tests passed',
    },
    prerequisites: ['Node.js 18+', 'pnpm'],
    steps: [
      { description: 'Install dependencies', command: 'pnpm install' },
      { description: 'Run tests', command: 'pnpm test' },
    ],
  },
})
```

## Project Types

| Type | Best For |
|------|----------|
| `npm-package` | Published npm packages |
| `cli-tool` | Command-line tools |
| `macos-app` | macOS applications |
| `react-library` | React component libraries |
| `monorepo` | Multi-package workspaces |
| `generic` | Other projects |

## Generated Files

### AGENTS.md
Combined documentation with critical context for AI agents:
- Project overview and structure
- Critical rules and conventions
- Entry points for navigation
- API reference

### llms.txt
Plain text summary optimized for LLM context windows:
- Concise project description
- Key commands
- Installation steps
- Links to full docs

### docs.json
Structured JSON for programmatic access:
- Full documentation tree
- Metadata and navigation
- Searchable content

### install.md
LLM-executable installation instructions following [installmd.org](https://installmd.org):
- Step-by-step setup
- Verification commands
- Can be piped to AI: `curl url/install.md | claude`

## Agent Content Pattern

Each doc page should have two versions:

```
docs/
├── overview.md           # Human-readable (prose, examples)
├── agent/
│   └── overview.agent.md # Agent-optimized (dense, structured)
```

**Agent versions should be:**
- Dense (no prose, just facts)
- Structured (tables, explicit values)
- Self-contained (no URL fetching needed)
- Cross-referenced against source code

## React Components

Dewey provides 22 components for building documentation sites:

### Layout
- `DocsApp` - Complete docs site with routing
- `DocsLayout` - Main layout (sidebar, TOC, navigation)
- `Header` - Sticky header with theme toggle
- `Sidebar` - Left navigation panel
- `TableOfContents` - Right minimap with scroll-spy

### Content
- `MarkdownContent` - Renders markdown with syntax highlighting
- `CodeBlock` - Code with copy button
- `Callout` - Alert boxes (info, warning, tip, danger)
- `Tabs` - Tabbed content
- `Steps` - Numbered instructions
- `Card`, `CardGrid` - Content cards
- `FileTree` - Directory visualizer
- `ApiTable` - Props/params table
- `Badge` - Status indicators

### Agent-Friendly
- `AgentContext` - Collapsible agent content block
- `PromptSlideout` - Interactive prompt editor
- `CopyButtons` - "Copy for AI" button

### Provider
- `DeweyProvider` - Theme and component context

## Theme Presets

```typescript
import { DeweyProvider } from '@arach/dewey'

<DeweyProvider theme="neutral">
  {/* Your docs */}
</DeweyProvider>
```

**Available themes:**
`neutral` | `ocean` | `emerald` | `purple` | `dusk` | `rose` | `github` | `warm`

## Built-in Skills

Dewey includes LLM prompt templates for documentation workflows:

### docsReviewAgent
Reviews documentation quality, catches drift from codebase:
```typescript
import { docsReviewAgent } from '@arach/dewey'

const prompt = docsReviewAgent.reviewPage
  .replace('{DOC_FILE}', 'docs/api.md')
  .replace('{SOURCE_FILES}', 'src/types/index.ts')
  .replace('{OUTPUT_FILE}', '.dewey/reviews/api.md')
```

### installMdGenerator
Generates install.md files following installmd.org standard.

### promptSlideoutGenerator
Creates interactive prompt configs for PromptSlideout components.

## Workflow: Agent-Ready Docs

1. **Initialize**: `npx dewey init`
2. **Write docs**: Create human-readable markdown in `docs/`
3. **Add agent versions**: Create `docs/agent/*.agent.md` with structured content
4. **Configure**: Set critical context and rules in `dewey.config.ts`
5. **Generate**: `npx dewey generate` creates AGENTS.md, llms.txt, etc.
6. **Audit**: `npx dewey audit` checks completeness
7. **Score**: `npx dewey agent` rates agent-readiness (target: 80+)

## Example: API Documentation

Human version (`docs/api.md`):
```markdown
# API Reference

The API provides methods for managing users...

## createUser(options)

Creates a new user with the specified options.

### Parameters

- `name` - The user's display name
- `email` - Email address (must be unique)
```

Agent version (`docs/agent/api.agent.md`):
```markdown
# API Reference

## createUser

| Param | Type | Required | Default |
|-------|------|----------|---------|
| name | string | yes | - |
| email | string | yes | - |
| role | 'admin' \| 'user' | no | 'user' |

Returns: `Promise<User>`

Throws: `DuplicateEmailError` if email exists
```

## Output

When setting up Dewey for a project:
1. Create `dewey.config.ts` with appropriate project type
2. Run `dewey init` to scaffold docs structure
3. Add critical context relevant to the project
4. Generate agent files with `dewey generate`
5. Verify with `dewey agent` (target score: 80+)
