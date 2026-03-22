---
name: skill-documentation-generator
description: Auto-generate comprehensive documentation from skills in multiple formats (PDF, HTML, EPUB, Markdown). Converts skills to static sites (Docusaurus/GitBook), generates API docs from scripts, creates video tutorials, builds searchable indexes, and exports for non-AI use. Use when publishing skills or creating external documentation.
version: 1.0.0
author: Guillaume
created: 2026-01-10
tags: [meta-skill, documentation, export, publishing, automation]
license: MIT
---

# Skill Documentation Generator

Generate comprehensive documentation from skills in multiple formats.

## Quick Start

### 1. Generate HTML Site (5 min)

```bash
# Generate static website
python3 scripts/generate-docs.py ~/Skills_librairie --format website --output docs/

# Creates:
# docs/
#   ├── index.html (catalog with search)
#   ├── vps-deployment-stack/
#   ├── docker-workflow/
#   └── assets/
```

### 2. Generate PDF (2 min)

```bash
# Create PDF documentation
python3 scripts/generate-docs.py ~/Skills_librairie --format pdf --output Complete-Skills-Guide.pdf

# Single PDF with all skills (120+ pages)
```

### 3. Deploy to GitHub Pages (10 min)

```bash
# Generate Docusaurus site
python3 scripts/generate-docs.py ~/Skills_librairie --format docusaurus --output website/

cd website/
npm install
npm run build
npm run deploy  # Publishes to https://username.github.io/skills
```

## Output Formats

### 1. Static Website
- HTML with search functionality
- Responsive design
- Syntax highlighting
- Dark mode support

### 2. PDF
- Table of contents
- Hyperlinked navigation
- Syntax highlighting
- Professional layout

### 3. EPUB
- E-reader compatible
- Reflowable text
- Embedded images
- Offline reading

### 4. Markdown
- Standalone MD files
- No Claude-specific syntax
- GitHub-compatible
- Can be imported to Notion/Obsidian

### 5. Docusaurus Site
- Full-featured documentation
- Versioning support
- Blog integration
- i18n support

## Features

### Search Index
```javascript
// Generated search.json
{
  "skills": [
    {
      "name": "vps-deployment-stack",
      "description": "...",
      "keywords": ["docker", "deployment", "vps"],
      "content": "..."
    }
  ]
}
```

### API Documentation
```bash
# Extract scripts and generate docs
python3 scripts/generate-docs.py skill-path --api-docs

# Creates:
# api/
#   ├── backup.sh.html
#   ├── upload-s3.sh.html
#   └── index.html
```

### Video Tutorials
```bash
# Generate tutorial script from workflow
python3 scripts/generate-docs.py skill-path --tutorial-script

# Creates:
# tutorials/
#   └── postgres-backup-tutorial.md
#       (Step-by-step script for screen recording)
```

## Customization

```yaml
# docs-config.yml
site:
  title: "My Skills Library"
  description: "Personal collection of skills"
  author: Guillaume
  theme: dark
  
formats:
  pdf:
    paper_size: A4
    font: Arial
    toc: true
  
  website:
    search: true
    analytics: false
    github_link: https://github.com/GuillaumeBld/Skills_librairie
```

## Batch Generation

```bash
# Generate all formats
python3 scripts/generate-docs.py ~/Skills_librairie --all-formats --output dist/

# Creates:
# dist/
#   ├── website/
#   ├── Complete-Skills-Guide.pdf
#   ├── skills-library.epub
#   └── markdown/
```

## CI/CD Auto-Publish

```yaml
# .github/workflows/publish-docs.yml
on:
  push:
    branches: [main]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate Docs
        run: python3 scripts/generate-docs.py . --format website --output public/
      
      - name: Deploy to Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

## Reference Files

- **scripts/generate-docs.py** - Main documentation generator
- **scripts/convert-to-pdf.py** - PDF converter
- **scripts/build-search-index.py** - Search index builder
- **assets/website-template/** - HTML templates
- **assets/pdf-style.css** - PDF styling

## Related Skills

- skill-library-manager
- skill-quality-auditor
