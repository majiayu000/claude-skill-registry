---
description: Guide for creating content on ose-platform-web Hugo site using PaperMod theme. Covers English-only landing page structure, update posts with date-prefixed filenames, PaperMod frontmatter (cover images, table of contents, author field), simple flat organization, and ose-platform-web specific conventions. Essential for ose-platform-web content creation tasks
---

# Hugo OSE Platform Development Skill

## Purpose

This Skill provides guidance for creating and managing content on the **ose-platform-web** Hugo site, which uses the PaperMod theme and serves as an English-only project landing page.

**When to use this Skill:**

- Creating platform updates on ose-platform-web
- Writing about page content
- Managing landing page structure
- Configuring PaperMod frontmatter
- Understanding ose-platform-web specific patterns

## Core Concepts

### Site Overview

**ose-platform-web** (`apps/ose-platform-web/`):

- **Site**: oseplatform.com
- **Theme**: PaperMod v7.0+ (compatible with v8.0)
- **Purpose**: English-only project landing page
- **Content Types**: Platform updates, about page
- **Structure**: Flat, simple organization

### English-Only Content

**NO Multi-Language Structure**:

- All content in English
- No language subdirectories
- Simple, flat content organization
- No bilingual content management

**Contrast with ayokoding-web**:

- ayokoding-web: Bilingual (`/en/`, `/id/`) with complex structure
- ose-platform-web: English-only with flat structure

## Content Structure

```
apps/ose-platform-web/content/
├── updates/                               # Platform updates
│   ├── _index.md
│   ├── 2025-12-07-initial-release.md    # Date-prefixed
│   └── 2025-11-20-announcement.md        # Date-prefixed
└── about.md                               # About page
```

**Simplicity principle**: No deep hierarchies, no complex organization.

## Date-Prefixed Filenames

### Update Post Naming

**CRITICAL**: All update posts use date prefix for automatic chronological sorting

**Format**: `YYYY-MM-DD-title.md`

**Examples**:

- `2025-12-07-beta-release.md`
- `2025-11-20-platform-announcement.md`
- `2025-10-15-architecture-overview.md`

**Rationale**:

- Automatic chronological ordering (no weight management needed)
- Clear publication date from filename
- Easy sorting in file system

### About Page Naming

**Format**: Simple slug without date prefix

**Example**: `about.md`

## PaperMod Frontmatter

### Required Fields

```yaml
---
title: "Post Title"
date: 2025-12-07T14:30:00+07:00
draft: false
---
```

**Minimal frontmatter** - PaperMod has fewer required fields than Hextra.

### Recommended Fields

```yaml
---
title: "OSE Platform Beta Release"
date: 2025-12-07T14:30:00+07:00
draft: false
description: "Brief description for meta tags and summaries"
summary: "Summary text for list pages"
tags: ["release", "beta", "announcement"]
categories: ["updates"]
showtoc: true # Enable table of contents
cover:
  image: "/images/beta-release.png"
  alt: "OSE Platform Dashboard Screenshot"
  caption: "New dashboard interface"
---
```

### PaperMod-Specific Fields

**Table of Contents**:

```yaml
showtoc: true # Show ToC
tocopen: false # ToC collapsed by default
```

**Metadata Display**:

```yaml
hidemeta: false # Show post metadata (date, reading time)
comments: true # Show comments section (if enabled)
```

**Search & SEO**:

```yaml
searchHidden: false # Include in site search
hideSummary: false # Show in list pages
robotsNoIndex: false # Allow search engine indexing
```

**Cover Image**:

```yaml
cover:
  image: "/images/cover.png" # Path to image
  alt: "Image description" # REQUIRED for accessibility
  caption: "Optional caption" # Displayed under image
  relative: false # Use absolute paths from /static/
  responsiveImages: true # Generate responsive variants
  hidden: false # Show on current page
```

### Author Field Rules

**FLEXIBLE** (unlike ayokoding-web):

- `author:` field allowed per-post
- Can be single author or multiple authors
- No site-level default restriction

**Examples**:

```yaml
# Single author
author: "OSE Platform Team"

# Multiple authors
author: ["John Doe", "Jane Smith"]
```

**Contrast with ayokoding-web**: ayokoding-web restricts `author` field to rants/celoteh only. ose-platform-web has no such restriction.

## Content Types

### Update Posts

**Location**: `content/updates/`

**Purpose**: Platform progress, feature releases, announcements

**Frontmatter example**:

```yaml
---
title: "OSE Platform Beta Release"
date: 2025-12-07T14:30:00+07:00
draft: false
tags: ["release", "beta", "announcement"]
categories: ["updates"]
summary: "Introducing the beta version of Open Sharia Enterprise Platform"
showtoc: true
cover:
  image: "/images/beta-release.png"
  alt: "OSE Platform Dashboard Screenshot"
---
```

### About Page

**Location**: `content/about.md`

**Purpose**: Project information, team details, contact info

**Frontmatter example**:

```yaml
---
title: "About OSE Platform"
url: "/about/"
summary: "Learn about Open Sharia Enterprise Platform"
showtoc: false
---
```

## Internal Links

**Format**: Absolute paths without `.md` extension

**Hugo shortcodes available**:

```markdown
# Using ref shortcode for content references

Check out our [getting started guide]({{< ref "/updates/getting-started" >}})

# Direct absolute paths

[Beta Release](/updates/2025-12-07-beta-release)
```

**Contrast with ayokoding-web**:

- ayokoding-web: MUST use absolute paths with language prefix (`/en/`, `/id/`)
- ose-platform-web: Absolute paths without language prefix (English-only)

## Asset Organization

**Location**: `apps/ose-platform-web/static/`

**Structure**:

```
static/
├── images/
│   ├── updates/
│   └── about/
└── casts/                    # Asciinema recordings
```

**Image References**:

```markdown
# Markdown image

![OSE Platform Dashboard](/images/updates/dashboard.png)

# Hugo figure shortcode

{{< figure src="/images/updates/architecture.png" alt="System Architecture" caption="OSE Platform Architecture" >}}
```

**Paths from `/static/`**:

- `static/images/dashboard.png` → `/images/dashboard.png`
- `static/casts/demo.cast` → `/casts/demo.cast`

## PaperMod Features

### Navigation

PaperMod provides:

- **Breadcrumbs**: Automatic breadcrumb navigation
- **Archive**: Chronological post listing
- **Smooth scrolling**: Anchor link behavior
- **Table of contents**: Per-page ToC (configurable)

### Theme Toggle

```yaml
# Site config (hugo.yaml)
params:
  defaultTheme: auto # Options: light, dark, auto
```

**User preference**: Stored in localStorage, persists across sessions.

### Social Sharing

```yaml
# Site config (hugo.yaml)
params:
  ShareButtons:
    - twitter
    - linkedin
    - reddit
```

**Per-page control**:

```yaml
---
ShowShareButtons: true # Enable share buttons for this post
---
```

### Home Page Configuration

```yaml
# Site config (hugo.yaml)
params:
  homeInfoParams:
    Title: "Welcome to OSE Platform"
    Content: "Open Sharia Enterprise Platform documentation and updates"

  socialIcons:
    - name: github
      url: "https://github.com/wahidyankf/open-sharia-enterprise"
    - name: twitter
      url: "https://twitter.com/oseplatform"
```

## Comparison with ayokoding-web

| Aspect               | ose-platform-web                 | ayokoding-web                                     |
| -------------------- | -------------------------------- | ------------------------------------------------- |
| **Theme**            | PaperMod                         | Hextra                                            |
| **Languages**        | English only                     | Bilingual (Indonesian/English)                    |
| **Structure**        | Flat (updates/, about.md)        | Deep hierarchy (learn/archived/crash-courses/...) |
| **Archetypes**       | 1 (default)                      | 5 (learn, celoteh, konten-video, etc.)            |
| **Weight Ordering**  | Optional (date-prefix for posts) | Strict level-based system (mandatory)             |
| **Navigation**       | Breadcrumbs, archive             | Auto-sidebar, 3-layer nav                         |
| **Author Field**     | Per-post (flexible)              | Site-level default (exceptions for rants/celoteh) |
| **Complexity**       | Simple, minimal                  | Feature-rich, complex                             |
| **Content Types**    | Updates, about                   | Tutorials, essays, videos                         |
| **Overview Files**   | Not required                     | Required (overview.md, ikhtisar.md)               |
| **Internal Links**   | Absolute paths                   | Absolute paths with language prefix               |
| **Primary Purpose**  | Landing page & updates           | Educational platform                              |
| **Target Audience**  | Enterprise users                 | Indonesian developers (bilingual)                 |
| **Tutorial Content** | No                               | Yes (detailed programming tutorials)              |

**Key Takeaway**: ose-platform-web is MUCH simpler than ayokoding-web.

## Common Patterns

### Creating Update Post

```bash
# 1. Create file with date prefix
hugo new content/updates/2025-12-07-feature-release.md

# 2. Edit frontmatter
# (add title, date, tags, cover image)

# 3. Write content
# (markdown content)

# 4. Set draft: false when ready to publish
```

### Creating About Page

```bash
# 1. Create file
hugo new content/about.md

# 2. Edit frontmatter
# (add title, url, summary)

# 3. Write content
# (project info, team details)

# 4. Set draft: false to publish
```

## Content Validation Checklist

Before publishing:

- [ ] Frontmatter uses YAML format (2-space indentation)
- [ ] Date format is `YYYY-MM-DDTHH:MM:SS+07:00`
- [ ] Description length is 150-160 characters (if present)
- [ ] Internal links use absolute paths without `.md`
- [ ] All images have descriptive alt text
- [ ] Update posts use date-prefixed filenames (`YYYY-MM-DD-title.md`)
- [ ] Cover images have alt text
- [ ] Summary field provided for list pages
- [ ] Draft status set correctly (`draft: true/false`)
- [ ] Tags and categories are arrays (if present)

## Common Mistakes

### ❌ Mistake 1: Using language prefixes

**Wrong**: `/en/updates/post` (ose-platform-web is English-only)

**Right**: `/updates/post`

### ❌ Mistake 2: Forgetting date prefix for updates

**Wrong**: `feature-release.md` (no chronological ordering)

**Right**: `2025-12-07-feature-release.md`

### ❌ Mistake 3: Missing cover image alt text

```yaml
# Wrong
cover:
  image: "/images/cover.png"
  # No alt text - accessibility violation

# Right
cover:
  image: "/images/cover.png"
  alt: "OSE Platform Dashboard showing metrics"
```

### ❌ Mistake 4: Using Hextra conventions

**Wrong**: Applying ayokoding-web conventions (weight system, ikhtisar files)

**Right**: Use simple PaperMod conventions (optional weight, no overview files)

## Best Practices

### Update Post Workflow

1. **Plan content**: Outline key points
2. **Create file**: Use date-prefixed filename
3. **Write frontmatter**: Title, date, tags, cover image
4. **Write content**: Clear, concise updates
5. **Add visuals**: Cover image, diagrams if needed
6. **Validate**: Check frontmatter, links, alt text
7. **Publish**: Set `draft: false`

### About Page Maintenance

1. **Keep current**: Update as project evolves
2. **Clear structure**: Sections for vision, team, contact
3. **No date needed**: About page is timeless
4. **Link to updates**: Reference update posts for news

## Reference Documentation

**Primary Convention**: [Hugo Content Convention - ose-platform-web](../../../../governance/conventions/hugo/ose-platform.md)

**Related Conventions**:

- [Hugo Content Shared](../../../../governance/conventions/hugo/shared.md) - Shared Hugo patterns
- [Content Quality Principles](../../../../governance/conventions/content/quality.md) - Universal quality standards

**Related Skills**:

- `hugo-ayokoding-development` - Comparison with ayokoding-web patterns
- `color-accessibility-diagrams` - Accessible diagrams for technical content

**Related Agents**:

- `apps__ose-platform-web__content-maker` - Creates ose-platform-web content
- `apps__ose-platform-web__content-checker` - Validates ose-platform-web content
- `apps__ose-platform-web__deployer` - Deploys ose-platform-web

**External Resources**:

- [PaperMod Official Documentation](https://adityatelange.github.io/hugo-PaperMod/)
- [PaperMod GitHub Repository](https://github.com/adityatelange/hugo-PaperMod)

---

This Skill packages essential ose-platform-web development knowledge for creating simple, effective landing page content. For comprehensive details, consult the primary convention document.

## Deployment Workflow

Deploy ose-platform-web to production using Vercel integration.

### Production Branch

**Branch**: `prod-ose-platform-web`  
**Purpose**: Deployment-only branch that Vercel monitors  
**Build System**: Vercel (Hugo SSG with PaperMod theme)

### Deployment Process

**Step 1: Validate Current State**

```bash
# Ensure on main branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "❌ Must be on main branch"
  exit 1
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
  echo "❌ Uncommitted changes detected"
  exit 1
fi
```

**Step 2: Force Push to Production**

```bash
# Deploy to production
git push origin main:prod-ose-platform-web --force
```

**Step 3: Vercel Auto-Build**

Vercel automatically:

- Detects push to prod-ose-platform-web branch
- Pulls latest content
- Builds Hugo site with PaperMod theme
- Deploys to production URL

### Why Force Push

**Safe for deployment branches**:

- prod-ose-platform-web is deployment-only (no direct commits)
- Always want exact copy of main branch
- Trunk-based development: main is source of truth

### Deployment Safety

**Pre-deployment checks**:

- ✅ On main branch
- ✅ No uncommitted changes
- ✅ Latest from remote

**No local build**: Vercel handles all build operations

## References

**Primary Convention**: [Hugo Content Convention - ose-platform-web](../../../../governance/conventions/hugo/ose-platform.md)

**Related Conventions**:

- [Hugo Content Shared](../../../../governance/conventions/hugo/shared.md) - Shared Hugo patterns
- [Content Quality Principles](../../../../governance/conventions/content/quality.md) - Universal quality standards

**Related Skills**:

- `apps__ayokoding-web__developing-content` - Comparison with ayokoding-web patterns
- `docs__creating-accessible-diagrams` - Accessible diagrams for technical content
