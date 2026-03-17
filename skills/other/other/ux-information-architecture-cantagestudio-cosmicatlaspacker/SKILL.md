---
name: ux-information-architecture
description: "[UI/UX] Designs Information Architecture (IA) as ASCII diagrams. Systematically organizes screen hierarchies, navigation structures, and content classification. Use when requesting 'IA design', 'information architecture', 'screen hierarchy', or 'sitemap'."
---

# UX Information Architecture

A skill that designs Information Architecture (IA) as ASCII diagrams.

## When to Use

- Designing overall screen hierarchy for apps/web
- Defining navigation structures
- Content classification and grouping
- Creating sitemaps

## IA Diagram Symbols

### Hierarchy Nodes
```
[Root]              ← Top level (app/site)
 ├─[Section]        ← Section (category)
 │  ├─[Page]        ← Page
 │  │  └─[SubPage]  ← Sub page
 │  └─[Page]
 └─[Section]
```

### Node Types
```
[Page Name]         ← Regular page
[[Core Page]]       ← Core page (emphasis)
(Modal/Overlay)     ← Modal/Overlay
{Dynamic Content}   ← Dynamic content
<External Link>     ← External link
[Page*]             ← Auth required
```

## IA Structure Patterns

### Hierarchical Tree
```
[Application]
 │
 ├─[Dashboard]
 │  ├─[Overview]
 │  └─[Statistics]
 │
 ├─[Projects]
 │  ├─[Project List]
 │  │  └─{Project Item}
 │  └─(New Project Modal)
 │
 └─[Settings]*
    ├─[Profile]
    └─[Security]
```

## IA Design Principles

- 3-click rule: Major content reachable within 3 levels
- Menu items: 7±2 recommended
- Hierarchy depth: 4 levels or less recommended