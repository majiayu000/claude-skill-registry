---
name: holydocs-migrate
description: Migrate documentation from Mintlify, GitBook, Docusaurus, ReadMe, or VuePress to HolyDocs. Use when the user wants to migrate, convert, switch, or move their docs from another platform. Also trigger when you see mint.json (Mintlify), docusaurus.config.js (Docusaurus), .gitbook.yaml (GitBook), or readme.yaml (ReadMe) in the project, or when the user mentions any of these platforms in the context of documentation.
---

# HolyDocs Migration Skill

## Overview

HolyDocs provides CLI-based migration via `holydocs migrate --from <platform>` that handles the bulk of conversion automatically. This skill provides the knowledge to:

- Guide users through the full migration workflow
- Handle migrations manually when the CLI misses edge cases
- Fix post-migration issues (broken links, unconverted components, missing assets)
- Map configuration and components between platforms accurately

Supported source platforms: **Mintlify**, **Docusaurus**, **GitBook**, **ReadMe**, **VuePress**.

## Migration Decision Flow

### Step 1: Detect the Source Platform

Look for these marker files in the project root:

| File | Platform |
|---|---|
| `mint.json` | Mintlify |
| `docusaurus.config.js` or `docusaurus.config.ts` | Docusaurus |
| `.gitbook.yaml` | GitBook |
| `readme.yaml` | ReadMe |
| `.vuepress/config.js` or `.vuepress/config.ts` | VuePress |

If multiple markers exist, ask the user which platform they are migrating from. If none are found, ask the user to confirm the source platform or point to the correct project directory.

### Step 2: Preview the Migration (Dry Run)

Always run a dry run first to surface issues before making changes:

```bash
holydocs migrate --from <platform> --dry-run
```

This outputs:
- Files that will be created, modified, or moved
- Components that will be converted
- Configuration fields that will be mapped
- Warnings for anything that cannot be auto-converted

Review the dry run output with the user before proceeding.

### Step 3: Run the Migration

```bash
holydocs migrate --from <platform>
```

For migrations into an existing HolyDocs project, add `--merge` to avoid overwriting:

```bash
holydocs migrate --from <platform> --merge
```

### Step 4: Verify

```bash
holydocs check
```

Use `--strict` for production readiness:

```bash
holydocs check --strict
```

### Step 5: Preview

```bash
holydocs dev
```

Open the local dev server and walk through every page. Pay attention to:
- Navigation structure and ordering
- Component rendering (callouts, tabs, code groups)
- Image loading
- Internal link resolution
- OpenAPI reference pages (if applicable)

### Step 6: Fix Issues

Use the platform-specific references and the common fixes section below to resolve any remaining problems.

## Quick Migration Commands

```bash
# Mintlify
holydocs migrate --from mintlify
holydocs migrate --from mintlify --dry-run

# Docusaurus
holydocs migrate --from docusaurus
holydocs migrate --from docusaurus --dry-run

# GitBook
holydocs migrate --from gitbook
holydocs migrate --from gitbook --dry-run

# ReadMe
holydocs migrate --from readme
holydocs migrate --from readme --dry-run

# VuePress
holydocs migrate --from vuepress
holydocs migrate --from vuepress --dry-run

# Merge into existing HolyDocs project
holydocs migrate --from <platform> --merge

# Specify a custom source directory
holydocs migrate --from <platform> --source ./path/to/docs
```

## Component Mapping (Universal)

This table maps components across all major platforms to their HolyDocs equivalents:

| Mintlify | Docusaurus | GitBook | HolyDocs |
|---|---|---|---|
| `<Note>` | `:::note` | `{% hint style="info" %}` | `<Callout type="note">` |
| `<Warning>` | `:::warning` | `{% hint style="warning" %}` | `<Callout type="warning">` |
| `<Tip>` | `:::tip` | `{% hint style="success" %}` | `<Callout type="tip">` |
| `<Info>` | `:::info` | `{% hint style="info" %}` | `<Callout type="info">` |
| `<Check>` | N/A | N/A | `<Callout type="check">` |
| `<Caution>` | `:::caution` or `:::danger` | `{% hint style="danger" %}` | `<Callout type="caution">` |
| `<Card>` | N/A | N/A | `<Card>` (compatible) |
| `<CardGroup>` | N/A | N/A | `<CardGroup>` (compatible) |
| `<Tabs>` / `<Tab>` | `<Tabs>` / `<TabItem>` | `{% tabs %}` / `{% tab %}` | `<Tabs>` / `<Tab>` |
| `<Steps>` | N/A | N/A | `<Steps>` (compatible) |
| `<Accordion>` | `<details>` | N/A | `<Accordion>` |
| `<AccordionGroup>` | N/A | N/A | `<AccordionGroup>` (compatible) |
| `<CodeGroup>` | N/A | N/A | `<CodeGroup>` (compatible) |
| `<Expandable>` | N/A | `{% expandable %}` | `<Expandable>` (compatible) |

### Conversion Rules

**Callouts** are the most common conversion. The pattern is:

- Mintlify: `<Note>content</Note>` becomes `<Callout type="note">content</Callout>`
- Docusaurus: `:::note\ncontent\n:::` becomes `<Callout type="note">content</Callout>`
- GitBook: `{% hint style="info" %}\ncontent\n{% endhint %}` becomes `<Callout type="note">content</Callout>`

**Tabs** require renaming the child component:

- Docusaurus: `<TabItem value="js" label="JavaScript">` becomes `<Tab title="JavaScript">`
- GitBook: `{% tab title="JavaScript" %}` becomes `<Tab title="JavaScript">`

## Configuration Mapping (Quick Reference)

### Mintlify `mint.json` to HolyDocs `docs.json`

```
name              -> name
logo              -> logo
favicon           -> favicon
colors.primary    -> theme.colors.primary
colors.light      -> theme.colors.light
colors.dark       -> theme.colors.dark
navigation        -> navigation.sidebar
topbarLinks       -> navigation.topbar.links
topbarCta         -> navigation.topbar.cta
anchors           -> navigation.anchors
tabs              -> navigation.tabs
footerSocials     -> footer.socials
modeToggle        -> appearance.modeToggle
api               -> api
openapi           -> openapi
```

### Docusaurus `docusaurus.config.js` to HolyDocs `docs.json`

```
title             -> name
favicon           -> favicon
themeConfig.navbar -> navigation.topbar
sidebars          -> navigation.sidebar
themeConfig.colorMode -> appearance.modeToggle
url               -> hosting.url
baseUrl           -> hosting.basePath
```

### GitBook `.gitbook.yaml` to HolyDocs `docs.json`

```
root              -> content.root (default ".")
structure.readme  -> content.index
structure.summary -> (parsed into navigation.sidebar)
```

## Post-Migration Checklist

After every migration, walk through this checklist:

- [ ] Run `holydocs check --strict` and resolve all errors
- [ ] Preview with `holydocs dev` and visually inspect every page
- [ ] Verify navigation structure matches the original site
- [ ] Check all internal links resolve correctly
- [ ] Verify all images and assets load (check browser console for 404s)
- [ ] Test OpenAPI/Swagger integration if applicable
- [ ] Confirm search works across migrated content
- [ ] Verify code blocks render with correct syntax highlighting
- [ ] Check that custom components converted properly
- [ ] Test light and dark mode rendering
- [ ] Update custom domain DNS if transferring from another platform
- [ ] Remove leftover source platform config files (mint.json, etc.)

## Common Post-Migration Fixes

### Broken Internal Links

**Symptom**: Links return 404 or point to wrong pages.

**Cause**: Different platforms use different path conventions:
- Mintlify: paths match file structure, no `/docs` prefix
- Docusaurus: `/docs/` prefix by default, category index pages
- GitBook: paths derived from SUMMARY.md, may include group prefixes

**Fix**: Run `holydocs check --links` to find all broken links. Common patterns:
```bash
# Docusaurus paths that need /docs/ prefix removed
/docs/getting-started -> /getting-started

# GitBook paths with group prefixes
/group-name/page -> /page

# File extension removal
/getting-started.md -> /getting-started
```

### Missing Images

**Symptom**: Images show as broken on the rendered site.

**Cause**: Asset directory structure differs:
- Mintlify: images in root or `/images`
- Docusaurus: images in `/static/img`
- GitBook: images in `.gitbook/assets`

**Fix**: Move all images to the HolyDocs assets directory and update references:
```bash
# Check for broken image references
holydocs check --assets
```

### Unconverted Components

**Symptom**: Raw HTML/MDX tags visible on rendered pages.

**Cause**: Platform-specific components not recognized by the auto-migrator.

**Fix**: Search for leftover platform-specific syntax:
```bash
# Mintlify leftovers
grep -r "<Note>" docs/
grep -r "<Warning>" docs/
grep -r "<ResponseField" docs/

# Docusaurus leftovers
grep -r ":::" docs/
grep -r "<TabItem" docs/
grep -r "import.*from.*@docusaurus" docs/

# GitBook leftovers
grep -r "{% hint" docs/
grep -r "{% tabs" docs/
grep -r "{% embed" docs/
```

### OpenAPI Spec Issues

**Symptom**: API reference pages don't render or show incorrect endpoints.

**Cause**: OpenAPI spec URL or path changed during migration.

**Fix**: Verify the `openapi` field in `docs.json` points to a valid spec:
```json
{
  "openapi": "https://api.example.com/openapi.json"
}
```

Or for a local file:
```json
{
  "openapi": "./openapi.yaml"
}
```

### Custom CSS Not Applied

**Symptom**: Styling differences from the original site.

**Cause**: Platform-specific CSS is not migrated automatically.

**Fix**: Move custom styles to `styles/custom.css` in your HolyDocs project. Note that class names and CSS variable names differ between platforms. Use HolyDocs theme configuration in `docs.json` for colors, fonts, and spacing before resorting to custom CSS.

## Platform-Specific References

For deep dives into each platform's migration details, component mappings, and edge cases:

- For detailed Mintlify migration, read `references/mintlify.md`
- For detailed GitBook migration, read `references/gitbook.md`
- For detailed Docusaurus migration, read `references/docusaurus.md`

## Troubleshooting

### Migration command fails to run

```bash
# Ensure HolyDocs CLI is installed and up to date
npm install -g holydocs@latest

# Check you're in the correct directory
ls mint.json  # or docusaurus.config.js, .gitbook.yaml, etc.

# Try with verbose logging
holydocs migrate --from <platform> --verbose
```

### Migration runs but output is empty

The source directory may not match expectations. Specify it explicitly:

```bash
holydocs migrate --from docusaurus --source ./docs
```

### `holydocs check` reports many warnings

Warnings are non-blocking. Focus on errors first. Common warnings include:
- Missing page descriptions (add frontmatter `description` field)
- Long page titles (keep under 60 characters)
- Missing alt text on images

These can be fixed incrementally after the core migration is verified.
