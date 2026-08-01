---
name: azure-devops-wiki
description: 'Azure DevOps Wiki management skill. Use when working with Azure DevOps
  wikis for: (1) Creating and organizing wiki pages - provisioned or code-as-wiki,
  (2) Markdown formatting - TOC, Mermaid diagrams,'
---

---
name: azure-devops-wiki
description: Azure DevOps Wiki management skill. Use when working with Azure DevOps wikis for: (1) Creating and organizing wiki pages - provisioned or code-as-wiki, (2) Markdown formatting - TOC, Mermaid diagrams, YAML metadata, code blocks, (3) Wiki structure - .order files, subpages, attachments, (4) Best practices - naming conventions, navigation, searchability, (5) CLI operations - az devops wiki commands, (6) Git-based wiki workflows - clone, edit offline, push changes. Supports both provisioned wikis and published code wikis.
---

# Azure DevOps Wiki Skill

Complete guide for managing Azure DevOps wikis with best practices and CLI operations.

## Wiki Types

Azure DevOps supports two wiki types:

| Type | Description | Use Case |
|------|-------------|----------|
| **Provisioned Wiki** | Built-in wiki created per project | Quick team documentation, single wiki per project |
| **Published Code Wiki** | Git repo published as wiki | SDK docs, versioned content, multiple wikis per project |

## Quick Start

### Create Provisioned Wiki

```bash
# Via Azure DevOps CLI
az devops wiki create --name "Project Wiki" --type projectwiki \
  --org https://dev.azure.com/ORG --project PROJECT
```

### Publish Code as Wiki

```bash
# Publish existing Git repo as wiki
az devops wiki create --name "API Docs" --type codewiki \
  --repository REPO_NAME --mapped-path / --version main \
  --org https://dev.azure.com/ORG --project PROJECT
```

## Repository Structure

Wiki files are stored in Git with this structure:

```
ProjectName.wiki/
├── .attachments/           # All attachments
├── .order                  # Root page sequence
├── Home.md                 # Home page
├── Getting-Started.md      # Top-level page
├── Getting-Started/        # Folder for subpages
│   ├── .order              # Subpage sequence
│   ├── Installation.md     # Subpage
│   └── Configuration.md    # Subpage
└── API-Reference.md        # Another top-level page
```

**Key conventions:**

- Wiki repo name: `<ProjectName>.wiki`
- Root branch: `wikiMain`
- Spaces in titles → hyphens in filenames: `Getting Started` → `Getting-Started.md`
- Subpages require matching folder: `Page.md` + `Page/` folder

## The .order File

Controls page sequence in table of contents:

```
Home
Getting-Started
API-Reference
Troubleshooting
```

**Rules:**

- One page name per line (without `.md` extension)
- Pages not listed appear alphabetically at the end
- Delete `.order` to restore alphabetical sorting

## Essential Markdown Features

### Table of Contents

Add auto-generated TOC to any page:

```markdown
[[_TOC_]]

## Section 1
Content here...

## Section 2
More content...
```

### Mermaid Diagrams

```markdown
::: mermaid
graph LR
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
:::
```

Supported diagram types:

- Sequence diagrams
- Flowcharts (`graph` not `flowchart`)
- Gantt charts
- Class diagrams
- State diagrams
- User journeys
- Pie charts
- Entity Relationship diagrams
- Timeline diagrams

### YAML Metadata

Add searchable metadata at page start:

```markdown
---
title: API Reference
author: Team Name
tags:
  - api
  - reference
  - v2
---

# Page Content
```

### Code Blocks with Syntax Highlighting

```markdown
```javascript
const config = {
  baseUrl: 'https://api.example.com',
  timeout: 5000
};
```

```

Supported languages: `javascript`, `typescript`, `python`, `csharp`, `bash`, `yaml`, `json`, `sql`, and [more](https://github.com/highlightjs/highlight.js/tree/stable-11/src/languages).

### Collapsible Sections

```html
<details>
<summary>Click to expand</summary>

Hidden content here...

</details>
```

### Work Item Links

```markdown
Link to work item: #123
Link with text: [User Story #123](#123)
```

### User Mentions

```markdown
@<alias> - mentions user
@<GroupName> - mentions group
```

### Images with Sizing

```markdown
![Alt text](/.attachments/image.png =500x300)
![Width only](/.attachments/image.png =500x)
```

## CLI Operations

### List Wikis

```bash
az devops wiki list --org https://dev.azure.com/ORG --project PROJECT -o table
```

### Create Page

```bash
az devops wiki page create --wiki "Project Wiki" --path "NewPage" \
  --content "# Page Title\n\nPage content here" \
  --org https://dev.azure.com/ORG --project PROJECT
```

### Update Page

```bash
az devops wiki page update --wiki "Project Wiki" --path "ExistingPage" \
  --content "Updated content" --version ETAG \
  --org https://dev.azure.com/ORG --project PROJECT
```

### Delete Page

```bash
az devops wiki page delete --wiki "Project Wiki" --path "PageToDelete" \
  --org https://dev.azure.com/ORG --project PROJECT -y
```

### Show Page

```bash
az devops wiki page show --wiki "Project Wiki" --path "PageName" \
  --org https://dev.azure.com/ORG --project PROJECT
```

## Git-Based Workflow

### Clone Wiki Locally

```bash
# Get wiki clone URL
az devops wiki show --wiki "Project Wiki" \
  --org https://dev.azure.com/ORG --project PROJECT \
  --query remoteUrl -o tsv

# Clone
git clone https://dev.azure.com/ORG/PROJECT/_git/PROJECT.wiki
cd PROJECT.wiki
```

### Edit and Push

```bash
# Create/edit pages
echo "# New Page\n\nContent" > New-Page.md

# Update .order
echo -e "Home\nNew-Page\nExisting-Page" > .order

# Commit and push
git add .
git commit -m "Add new documentation page"
git push origin wikiMain
```

## Best Practices

### Structure & Organization

| Practice | Description |
|----------|-------------|
| **Flat hierarchy** | Keep max 3 levels deep for easy navigation |
| **Consistent naming** | Use kebab-case: `api-reference`, `getting-started` |
| **Logical grouping** | Group related pages in subfolders |
| **Index pages** | Create overview pages for each section |
| **Home page** | Always have a clear entry point |

### Content Guidelines

| Practice | Description |
|----------|-------------|
| **Use TOC** | Add `[[_TOC_]]` to pages with multiple sections |
| **Descriptive titles** | Use clear, searchable page titles |
| **Cross-linking** | Link related pages for discoverability |
| **Keep updated** | Archive outdated content, don't delete |
| **Diagrams** | Use Mermaid for architecture/flow visualization |

### File Naming

| Do | Don't |
|----|-------|
| `getting-started.md` | `Getting Started.md` (spaces) |
| `api-v2-reference.md` | `api_v2_reference.md` (underscores) |
| `faq.md` | `FAQ.md` (uppercase) |

### Searchability

- Add YAML metadata with tags
- Use descriptive headings
- Include keywords in content
- Link work items for context

## Provisioned vs Code Wiki Comparison

| Feature | Provisioned | Code Wiki |
|---------|-------------|-----------|
| Multiple wikis per project | No (1 only) | Yes |
| Versioning | Git history | Git branches |
| Edit from Repos | No | Yes |
| Branch policies | Limited | Full support |
| Revert from wiki UI | Yes | No (use Git) |
| Best for | Team docs | SDK/Product docs |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Page not appearing | Check `.order` file includes page name |
| Broken links | Use relative paths: `./subpage` or `/absolute/path` |
| Images not showing | Upload to `.attachments/` folder |
| TOC not rendering | Ensure `[[_TOC_]]` is on its own line |
| Mermaid not working | Use `graph` instead of `flowchart` |
| YAML metadata broken | Check for proper `---` delimiters |

## File Restrictions

| Restriction | Limit |
|-------------|-------|
| Page file size | 18 MB max |
| Attachment size | 19 MB max |
| Path length | 235 characters max |
| Special chars in names | No `/`, `\`, `#` |
| Period in names | Not at start/end |

## Scripts

- `scripts/wiki-clone.sh <project> <wiki-name>` - Clone wiki repository
- `scripts/wiki-publish.sh <project> <repo> <path>` - Publish repo as wiki

## References

For detailed documentation:

- **[references/best-practices.md](references/best-practices.md)** - Comprehensive best practices guide
- **[references/markdown-syntax.md](references/markdown-syntax.md)** - Complete Markdown reference
- [Official Azure DevOps Wiki Docs](https://learn.microsoft.com/en-us/azure/devops/project/wiki/)
