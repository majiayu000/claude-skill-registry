---
name: rspress-page
description: Scaffold new RSPress documentation pages with proper structure and templates. Use when creating new docs pages, adding package documentation, writing guides, or setting up API reference pages.
allowed-tools: Read, Write, Edit, Glob, Grep
context: fork
agent: rspress-doc-agent
---

# RSPress Page Scaffolding

You are a specialized skill for scaffolding new RSPress documentation pages in the Savvy Web Workflow documentation site.

## Documentation Root

All documentation content lives in:

```text
docs/src/en/
```

RSPress configuration is at `docs/rspress.config.ts` with root set to `src`.

## Directory Structure Patterns

```text
docs/src/en/
├── index.mdx                    # Homepage
├── guide/                       # Guides and tutorials
│   └── start/
│       ├── overview.mdx
│       └── quick-start.md
├── packages/                    # Package documentation
│   ├── index.md
│   └── @savvy-web/
│       └── package-name/
│           ├── index.mdx        # Package overview
│           └── api/             # API reference
│               ├── index.md
│               ├── functions/
│               └── classes/
├── actions/                     # GitHub Actions documentation
│   └── action-name/
│       ├── index.md
│       └── overview.md
└── api/                         # General API docs
    ├── index.md
    ├── components.md
    └── utils.md
```

## Page Types

### Package Overview Page

Location: `docs/src/en/packages/@savvy-web/{package-name}/index.mdx`

Required frontmatter:

* `title` - Package name in quotes (e.g., `"@savvy-web/commitlint-config"`)

Structure:

* Brief description
* Installation section with bash code block
* Usage examples
* Configuration options (if applicable)
* Links to API reference or GitHub

### Guide Page

Location: `docs/src/en/guide/{category}/{page-name}.md`

Optional frontmatter:

* `pageTitle` - Custom page title
* `overview` - Set to `false` to hide from overview

Structure:

* H1 heading matching the topic
* Introduction paragraph
* Organized sections with H2/H3 headings
* Code examples with language identifiers
* Step-by-step instructions using ordered lists

### API Reference Page

Location: `docs/src/en/packages/@savvy-web/{package}/api/{type}/{name}.md`

Types: `functions/`, `classes/`, `types/`, `interfaces/`

Structure:

* H1 heading with the item name
* Description paragraph
* Signature section with TypeScript code block
* Parameters section (table or list)
* Returns section
* Examples section
* Related links

### GitHub Actions Page

Location: `docs/src/en/actions/{action-name}/index.md`

Structure:

* H1 heading with action name
* Description of purpose
* Inputs section (table format)
* Outputs section (table format)
* Usage examples with yaml code blocks
* Related documentation links

## Creating New Pages Checklist

When scaffolding a new documentation page:

1. Determine the page type and correct directory location
1. Create the file with appropriate frontmatter
1. Add H1 heading (only one per file)
1. Write concise introduction paragraph
1. Structure content with H2/H3 sections
1. Add code blocks with language identifiers (`bash`, `typescript`, `yaml`, etc.)
1. Use `*` for unordered lists, `1.` for ordered lists
1. Ensure blank lines around headings, lists, and code blocks
1. Add navigation links to parent index pages if needed
1. Run `pnpm lint:md` to validate markdown

## Common Frontmatter Fields

* `title` - Page title (displayed in browser tab)
* `pageTitle` - Alternative page title for display
* `overview` - Boolean to control overview display
* `description` - Page description for SEO

## Code Block Languages

Use these language identifiers for code blocks:

* `bash` - Shell commands
* `typescript` - TypeScript code
* `javascript` - JavaScript code
* `json` - JSON configuration
* `yaml` - YAML configuration
* `text` - Plain text output
* `tsx` - React/TSX components
* `mdx` - MDX content

## Tips

* Keep content scannable with short paragraphs and lists
* Use tables for structured data (inputs, outputs, parameters)
* Link to related pages and external resources
* Provide working code examples
* Follow existing patterns in similar documentation files
