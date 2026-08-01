---
name: notion-workflows
description: Provides Notion workspace organization patterns, layout preferences,
  and workflow automation for personal productivity systems. Includes structure guidelines,
  content reuse patterns, and integration w
---

---
name: notion-workflows
description: Provides Notion workspace organization patterns, layout preferences, and workflow automation for personal productivity systems. Includes structure guidelines, content reuse patterns, and integration with external tools. MANDATORY: Claude must read this skill file before using any Notion MCP tools.
---

# Notion Workflows & Organization

## Overview

This skill provides guidance for organizing and working with Notion workspaces, including personal preferences, workflow patterns, and best practices for productivity systems integration.

**CRITICAL REQUIREMENT**: Before using ANY Notion MCP tools, Claude MUST read this entire skill file to understand proper workflow patterns, cost-effective strategies, and organizational preferences. This prevents expensive API calls and ensures proper workspace organization.

**Keywords**: notion, productivity, workspace organization, synced blocks, database management, content organization, workflow automation

## Personal Preferences

### Layout Preferences
- **Triple-column layouts**: Preferred for organizing information and tasks in Notion
- Organize content in logical columns for better visual hierarchy
- Use consistent spacing and alignment across pages

### Content Reuse
- **Synced blocks**: Strongly prefer synced blocks whenever reusing text makes sense, especially for to-do list tasks
- Create reusable templates for common content patterns
- Maintain consistency across related pages through synced content

## Workflow Patterns

### Change Validation Protocol
Before making any reorganization changes (tasks, views, content), present a natural language diff summary:

**Standard validation format**:
```
**Before**: [what currently exists/state]
**Completed/Removed**: [items being completed or removed]
**Moving/Keeping**: [items staying but changing location/category]
**New/Added**: [new items being added] → [where they're going]
**After**: [final organized state]
```

**When to use**: Task rollovers, view reorganization, content restructuring, database cleanup, any bulk changes

### Notion-Specific Workflows

#### Daily Task Rollover
- Preserve exact wording and synced block references
- Organize new items into priority categories (🔥→💪→🎯→🧹→🔬)
- Use change validation protocol before executing

#### Content Reorganization
- Maintain page hierarchies and relationships
- Preserve important links and references
- Use change validation protocol before executing

### Database Organization
- Structure databases with clear property schemas
- Use consistent naming conventions for properties
- Implement proper filtering and sorting for different views
- Reference personal taxonomy from `private-prefs/personal-taxonomy.json`

### Content Management
- Prefer editing existing content over creating new files
- Use page templates for consistent structure
- Implement proper tagging and categorization systems
- Maintain clean page hierarchies

### Integration Considerations
- Design workflows that complement Things3 task management
- Use Notion for documentation and detailed planning
- Leverage database relationships for cross-referencing
- Consider API limitations when planning automation

## MCP Tools Integration

This skill works with the available MCP tools:
- `migrate_inbox_to_notion`: Transfer Things3 inbox items to Notion blocks
- `consolidate_twitter_pages`: Organize Twitter content in structured layouts
- Standard Notion API tools for page and database management

## Cost-Effective Operations

### Database Query Strategy
When working with large databases:
1. **Warn user about expensive operations** requiring many API calls
2. Suggest creating filtered views in Notion first
3. Use specific page IDs/URLs for targeted operations
4. Only use database-wide operations when explicitly confirmed

### Temp Folder Usage
For complex operations exceeding ~10k characters:
1. Use `temp/` folder for caching large responses
2. Break operations into incremental steps
3. Cache database schemas and search results
4. Track page IDs/URLs safely

## Personal Context Integration

This skill automatically references:
- Personal work areas and tags from `private-prefs/personal-taxonomy.json`
- Organizational patterns and preferences
- Integration points with Things3 workflows
- Custom workflow automation patterns

Always consider personal context when suggesting Notion organization or automation approaches.