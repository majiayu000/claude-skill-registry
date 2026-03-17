---
name: frontend-patterns
description: "Router skill for frontend patterns - directs to paper-rules, grid-selection, page-templates, error-prevention, or resources based on need"
version: "1.0.0"
tags: ["frontend", "mui", "react", "patterns", "router"]
---

# Frontend Patterns Router

This skill routes you to the appropriate frontend pattern based on your need.

## Available Pattern Skills

### frontend-patterns:paper-rules
**When to use:** Creating Paper components, need to determine `background={1}` usage

**Provides:**
- USE background={1} when (tab containers, dashboard widgets)
- DON'T USE when (form wrappers, kanban layouts)
- Quick decision tree
- Common mistakes

**Invoke with:**
```
Skill tool with skill: "frontend-patterns:paper-rules"
```

### frontend-patterns:grid-selection
**When to use:** Creating grid layouts, card grids, list layouts

**Provides:**
- Pattern 1: MUI Grid (structured layouts)
- Pattern 2: CSS Grid (flexible auto-fill)
- Pattern 3: Stack (vertical lists)
- Decision matrix
- Common column patterns

**Invoke with:**
```
Skill tool with skill: "frontend-patterns:grid-selection"
```

### frontend-patterns:page-templates
**When to use:** Creating new pages, determining page structure

**Provides:**
- Template 1: Simple Form Page
- Template 2: Detail Page with Sidebar
- Template 3: Dashboard Grid
- Template 4: Full-Page App (Kanban/Board)
- Template 5: List View with Filters

**Invoke with:**
```
Skill tool with skill: "frontend-patterns:page-templates"
```

### frontend-patterns:error-prevention
**When to use:** Before claiming completion, verifying work

**Provides:**
- 13 common mistakes with before/after examples
- Grid/Layout mistakes
- Paper component mistakes
- Styling mistakes
- Workflow mistakes
- Quick verification checklist

**Invoke with:**
```
Skill tool with skill: "frontend-patterns:error-prevention"
```

### frontend-patterns:resources
**When to use:** Need to reference MUI docs, icons, theme tokens

**Provides:**
- mui-doc.txt usage
- MUI MCP server info
- Icon documentation location
- Theme token reference
- Resource usage workflow

**Invoke with:**
```
Skill tool with skill: "frontend-patterns:resources"
```

## Quick Decision Guide

**Question: What are you creating?**

- **Paper component?** → Use `paper-rules`
- **Grid/card layout?** → Use `grid-selection`
- **New page?** → Use `page-templates`
- **Need MUI docs/icons?** → Use `resources`
- **Verifying work?** → Use `error-prevention`

## Multiple Patterns

If you need multiple patterns, invoke multiple skills:

```
1. Determine page structure:
   Skill tool with skill: "frontend-patterns:page-templates"

2. Determine grid layout:
   Skill tool with skill: "frontend-patterns:grid-selection"

3. Determine Paper usage:
   Skill tool with skill: "frontend-patterns:paper-rules"

4. Verify before completion:
   Skill tool with skill: "frontend-patterns:error-prevention"
```

## Integration with Core Agent

The react-mui-frontend-engineer agent will invoke these skills at specific workflow points:

- Step 1: ALWAYS ASK FIRST (confirm location)
- Step 2: Search existing components
- Step 3: **INVOKE pattern skills** (page-templates, grid-selection, paper-rules)
- Step 4: Implement following skill guidance
- Step 5: **INVOKE error-prevention** before completion

## Skill Updates

All pattern skills are versioned. Current versions:
- paper-rules: v1.0.0
- grid-selection: v1.0.0
- page-templates: v1.0.0
- error-prevention: v1.0.0
- resources: v1.0.0

See CHANGELOG.md for version history and updates.
