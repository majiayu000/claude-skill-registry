---
description: Comprehensive guide for creating content on ayokoding-web Hugo site using Hextra theme. Covers bilingual content strategy (default English), level-based weight ordering system, by-example tutorial annotation standards (1-2.25 comments per code line), absolute path linking requirements, and ayokoding-web specific frontmatter patterns. Essential for content creation tasks on ayokoding-web
---

# Hugo ayokoding-web Development Skill

## Purpose

This Skill provides comprehensive knowledge for creating and managing content on the **ayokoding-web** Hugo site, which uses the Hextra theme and serves as a bilingual educational platform for Indonesian developers.

**When to use this Skill:**

- Creating educational content on ayokoding-web
- Setting up programming language tutorials
- Managing bilingual content (English/Indonesian)
- Configuring navigation and weight systems
- Writing by-example tutorials with proper annotation density
- Ensuring proper frontmatter configuration
- Following ayokoding-web specific conventions

## Core Concepts

### Site Overview

**ayokoding-web** (`apps/ayokoding-web/`):

- **Site**: ayokoding.com
- **Theme**: Hextra (modern documentation theme)
- **Purpose**: Bilingual educational platform
- **Languages**: Indonesian (id) and English (en)
- **Content Types**: Learning content, personal essays (celoteh/rants), video content

### Bilingual Strategy

**Default Language**: English (`en`)

**Critical Rule**: Content does NOT have to be mirrored between languages

- ✅ Content can exist in English only (`/en/`)
- ✅ Content can exist in Indonesian only (`/id/`)
- ✅ Content can exist in both (if explicitly created)
- ❌ Do NOT automatically create mirror content in other language

**Workflow**: Create English content first → Review → Decide if Indonesian version needed → Create Indonesian as separate task

### Content Structure

```
apps/ayokoding-web/content/
├── id/                          # Indonesian content
│   ├── _index.md
│   ├── belajar/                 # Learning (Indonesian)
│   ├── celoteh/                 # Personal essays
│   └── konten-video/            # Video content
└── en/                          # English content
    ├── _index.md
    ├── learn/                   # Learning (English)
    ├── rants/                   # Personal essays
    └── video-content/           # Video content
```

### No H1 Headings in Content

**CRITICAL**: ayokoding-web content MUST NOT include ANY H1 headings (`# ...`) in markdown content.

**Rationale**: Hextra theme automatically renders frontmatter `title` as the page H1. Each page should have exactly ONE H1 (from frontmatter).

**Rule**: Content should start with introduction text or H2 headings (`## ...`).

## Weight System - Level-Based Ordering

### Powers of 10 Ranges

ayokoding-web uses a **level-based weight system** with powers of 10 ranges that reset for each parent folder:

- **Level 1**: 0-9 (language roots `/en/`, `/id/`)
- **Level 2**: 10-99 (children of language roots)
- **Level 3**: 100-999 (children of level 2 folders)
- **Level 4**: 1000-9999 (children of level 3 folders)
- **Level 5**: 10000-99999 (children of level 4 folders)
- **Level 6**: 100000-999999 (children of level 5 folders)

### Critical Rules

**Folder Representation**: `_index.md` represents the folder itself at level N → uses level N weight

**Content Inside**: Content INSIDE folder is one level deeper → uses level N+1 base weight

**Weights Reset Per Parent**: Each parent's children reset to base range independently

### Weight Calculation Example

```
Path: /en/ (1) → /learn/ (2) → /swe/ (3) → /prog-lang/ (4) → /golang/ (5) → /tutorials/ (6)

tutorials/ is level 6 folder:
  - tutorials/_index.md: weight: 100002 (level 6 - represents folder)
  - Content INSIDE tutorials/ uses level 7 (1000000, 1000001...)

by-concept/ is level 7 folder (child of tutorials/):
  - by-concept/_index.md: weight: 1000000 (level 7 - first child)
  - Content INSIDE by-concept/ uses level 8 (10000000, 10000001...)

by-example/ is level 7 folder (sibling of by-concept/):
  - by-example/_index.md: weight: 1000001 (level 7 - second child)
  - Content INSIDE by-example/ uses level 8 (10000000 - RESET, different parent)
```

## By-Example Tutorial Standards

### Annotation Density Requirement

**CRITICAL**: All code examples MUST meet annotation density standards

**Target**: 1.0-2.25 comment lines per code line **PER EXAMPLE**

- **Minimum**: 1.0 (examples below need enhancement)
- **Optimal**: 1-2.25 (target range)
- **Upper bound**: 2.5 (examples exceeding need reduction)

### Annotation Pattern

Use `// =>` or `# =>` notation to document:

```java
int x = 10;                      // => x is 10 (type: int)
String result = transform(x);    // => Calls transform with 10
                                 // => result is "10-transformed" (type: String)
System.out.println(result);      // => Output: 10-transformed
```

**Simple lines get 1 annotation, complex lines get 2 annotations**

## Internal Link Requirements

**CRITICAL**: ALL internal links MUST use absolute paths with language prefix

**Format**: `/[language]/[section]/[path]/[filename]`

**Examples**:

```markdown
✅ Correct:

- [Python](/en/learn/swe/prog-lang/python)
- [Golang Overview](/en/learn/swe/prog-lang/golang/overview)
- [Ikhtisar](/id/belajar/swe/prog-lang/ikhtisar)

❌ Wrong:

- [Python](swe/prog-lang/python) # Relative path
- [Overview](./overview) # Relative path
- [Python](/learn/swe/prog-lang/python) # Missing language prefix
```

**Why**: Hugo resolves links based on current page context. Relative paths break when content rendered in different locations.

## Frontmatter Patterns

### Required Fields

```yaml
---
title: "Page Title"
date: 2025-12-07T10:00:00+07:00
draft: false
description: "Brief description"
weight: 100000 # Level-based weight
tags: ["tag1", "tag2"] # JSON array format
---
```

### Critical Rules

- **No categories field**: Causes raw text leak in Hextra theme
- **No author field**: Uses site-level config (except rants/celoteh directories)
- **Date format**: UTC+7 with ISO 8601 format
- **Weight field**: MANDATORY - uses level-based system
- **Tags**: JSON array format `["tag1", "tag2"]` (NOT dash-based YAML)

### Author Field Rules

**FORBIDDEN** in these directories (uses site-level author):

- `apps/ayokoding-web/content/en/learn/`
- `apps/ayokoding-web/content/id/belajar/`
- `apps/ayokoding-web/content/en/video-content/`
- `apps/ayokoding-web/content/id/konten-video/`

**ALLOWED** in these directories only:

- `apps/ayokoding-web/content/en/rants/` - Guest contributors possible
- `apps/ayokoding-web/content/id/celoteh/` - Guest contributors possible

## Overview/Ikhtisar Requirements

### Required Files

**CRITICAL**: EVERY content folder MUST have an intro content file

- **English folders** (`/en/learn/` and subfolders): MUST have `overview.md`
- **Indonesian folders** (`/id/belajar/` and subfolders): MUST have `ikhtisar.md`

### Overview/Ikhtisar Link Requirement

**CRITICAL**: ALL `_index.md` files (except language roots) MUST include overview/ikhtisar link as FIRST item in navigation list

**Examples**:

```markdown
<!-- File: /en/learn/_index.md -->

- [Overview](/en/learn/overview) # ← FIRST ITEM
- [Software Engineering](/en/learn/swe)
- [AI Engineering](/en/learn/ai)

<!-- File: /id/belajar/swe/_index.md -->

- [Ikhtisar](/id/belajar/swe/ikhtisar) # ← FIRST ITEM
- [Programming Languages](/id/belajar/swe/prog-lang)
```

### Title Format

- **`overview.md` files**: Title MUST be "Overview" (simple, generic)
- **`ikhtisar.md` files**: Title MUST be "Ikhtisar" (simple, generic)

Context provided by directory structure, not title.

## Navigation Depth (2 Layers)

**CRITICAL**: `_index.md` files MUST display navigation links 2 layers deep with complete coverage

**Layer Definition**:

- **Layer 1**: Parent section/category (current level)
- **Layer 2**: ALL immediate children (subdirectories and direct content files)

**Completeness Requirement**: Show ALL children (every subdirectory and direct content file)

**Terminal Directory Exemption**: Folders containing ONLY content files (no subdirectories) are exempt from 2-layer requirement

## Programming Language Structure

### Dual-Path Organization

**By Concept Path** (mandatory):

- Narrative-driven tutorials
- Deep explanations
- Progressive examples
- 0-95% coverage (beginner, intermediate, advanced)

**By Example Path** (optional):

- Code-first approach
- 75-90 heavily annotated examples
- Five-part structure per example
- 95% coverage efficiently

**Foundational Tutorials** (at root level, NOT nested):

- `initial-setup.md` - 0-5% coverage
- `quick-start.md` - 5-30% coverage

### Standard Tutorial Folder Arrangement

All topics with tutorials follow 5-item arrangement:

1. **overview** (weight: 100000)
2. **initial-setup** (weight: 100001)
3. **quick-start** (weight: 100002)
4. **by-example** (weight: 100003) - if exists
5. **by-concept** (weight: 100004) - optional

## Common Mistakes

### ❌ Mistake 1: Content using same level as folder

```yaml
# WRONG! Content should be one level deeper
# File: /en/learn/overview.md (inside level 2 folder)
weight: 10 # Should use level 3, not level 2
```

### ❌ Mistake 2: Not resetting weights for different parents

```yaml
# WRONG! Continuing numbers across different parents
/en/learn/swe/_index.md → weight: 102
/en/learn/ai/_index.md → weight: 103
/en/rants/2024/_index.md → weight: 104 # Should reset to 102
```

### ❌ Mistake 3: Using relative paths

```markdown
<!-- WRONG! -->

- [Python](swe/prog-lang/python)

<!-- RIGHT! -->

- [Python](/en/learn/swe/prog-lang/python)
```

### ❌ Mistake 4: Missing weight field

```yaml
# WRONG!
---
title: "Initial Setup"
# No weight field - Hugo sorts alphabetically
---
```

### ❌ Mistake 5: H1 in content

```markdown
---
title: "Software Engineering"
---

# Introduction # ← WRONG! No H1 in content

## What You'll Learn # ← CORRECT! Start with H2
```

## Best Practices

### Content Creation Workflow

1. **Determine language**: Default to English (`/en/`)
2. **Calculate weight**: Use level-based system (folder level + 1 for content)
3. **Create frontmatter**: Required fields with JSON array tags
4. **Write content**: Start with H2, use absolute paths
5. **Add overview file**: Create overview.md or ikhtisar.md for folder
6. **Update navigation**: Add to parent `_index.md` with overview link first
7. **Validate**: Check no H1 headings, absolute paths, proper weights

### By-Example Tutorial Creation

1. **Plan examples**: 75-90 examples achieving 95% coverage
2. **Write code first**: Self-contained, runnable examples
3. **Add annotations**: 1-2.25 comments per code line PER EXAMPLE
4. **Use `// =>` notation**: Document values, states, outputs
5. **Add diagrams**: Mermaid diagrams when appropriate (use accessible colors)
6. **Verify density**: Measure per-example annotation ratio

### Weight Calculation Strategy

1. **Identify path**: `/en/` (1) → `/learn/` (2) → `/swe/` (3) → ...
2. **Determine folder level**: Count from language root
3. **Apply rules**:
   - Folder's `_index.md` uses folder's level weight
   - Content inside folder uses next level deeper (base + position)
   - Weights reset for different parents

## Deployment Workflow

Deploy ayokoding-web to production using Vercel integration.

### Production Branch

**Branch**: `prod-ayokoding-web`
**Purpose**: Deployment-only branch that Vercel monitors
**Build System**: Vercel (Hugo SSG with Hextra theme)

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
git push origin main:prod-ayokoding-web --force
```

**Step 3: Vercel Auto-Build**

Vercel automatically:

- Detects push to prod-ayokoding-web branch
- Pulls latest content
- Builds Hugo site with Hextra theme
- Deploys to production URL

### Why Force Push

**Safe for deployment branches**:

- prod-ayokoding-web is deployment-only (no direct commits)
- Always want exact copy of main branch
- Trunk-based development: main is source of truth

### Deployment Safety

**Pre-deployment checks**:

- ✅ On main branch
- ✅ No uncommitted changes
- ✅ Latest from remote

**No local build**: Vercel handles all build operations

## References

**Primary Convention**: [Hugo Content Convention - ayokoding-web](../../../../governance/conventions/hugo/ayokoding.md)

**Related Conventions**:

- [Programming Language Tutorial Structure](../../../../governance/conventions/tutorial/programming-language-structure.md) - Dual-path organization
- [By Example Tutorial Convention](../../../../governance/conventions/tutorial/by-example.md) - Annotation standards
- [Hugo Content Shared](../../../../governance/conventions/hugo/shared.md) - Shared Hugo patterns
- [Content Quality Principles](../../../../governance/conventions/content/quality.md) - Universal quality standards

**Related Skills**:

- `docs__creating-by-example-tutorials` - Detailed by-example tutorial guidance
- `docs__creating-accessible-diagrams` - Accessible diagram creation for tutorials

---

This Skill packages critical ayokoding-web development knowledge for progressive disclosure. For comprehensive details, consult the primary convention document.
