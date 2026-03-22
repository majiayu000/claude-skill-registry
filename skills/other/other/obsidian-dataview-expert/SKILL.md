---
name: obsidian-dataview-expert
description: Dataview plugin expertise for dynamic queries and dashboards
category: Session Knowledge
---

# Skill: obsidian-dataview-expert

## What I do

I provide definitive expertise in writing Dataview queries (DQL) and JavaScript-based views (DataviewJS) within Obsidian. I enable agents to transform static knowledge bases into dynamic, self-organising databases by treating the vault as a queryable data source.

## When to use me

- When creating or updating Obsidian Knowledge Base (KB) pages.
- When dynamic indexing of notes, skills, agents, or tasks is required.
- When building dashboards that must reflect the current state of the vault.
- When replacing static markdown tables with dynamic data views.
- **CRITICAL RULE**: Use me for ANY KB index page. NEVER use static markdown tables or manual lists in Obsidian KB pages. ALWAYS use DataviewJS queries that dynamically pull from vault metadata.

## Core principles

1. **Metadata-First Architecture**: Treat frontmatter and tags as query fuel. No metadata means no visibility.
2. **Defensive Programming**: ALWAYS wrap DataviewJS in `try/catch` blocks with user-friendly error messages to prevent dashboard crashes.
3. **Progressive Complexity**: Use DQL for simple lists/tables; escalate to DataviewJS for complex logic, multi-step filtering, or custom CSS-styled rendering.
4. **Path-Based Scoping**: Narrow query scope using folder paths (e.g., `startsWith("3. Resources/KB")`) to ensure performance and accuracy.
5. **British English**: All labels, headers, and documentation within queries must use British English spelling.

## DQL vs DataviewJS

| Feature | DQL (Dataview Query Language) | DataviewJS |
|:---|:---|:---|
| **Complexity** | Simple filtering, sorting, and display. | Full JavaScript power, logic, and loops. |
| **Rendering** | Standard List, Table, Task, Calendar. | Custom HTML, CSS grids, dynamic elements. |
| **Logic** | Basic logical operators (AND, OR, NOT). | Conditionals, complex math, external calls. |
| **Error Handling** | Silent failure or basic error message. | Comprehensive `try/catch` blocks. |
| **Use Case** | Quick indexes, simple task lists. | Dashboards, statistics, skill cards, grids. |

## DataviewJS fundamentals

### Querying and Filtering
```javascript
// Scoped query by path and tag
const base = "3. Resources/Knowledge Base/AI Development System";
const pages = dv.pages().where(p => p.file.path.startsWith(base));

// Tag matching (handling both single strings and arrays)
const skills = pages.where(p => 
    p.file.tags.values.some(t => t.startsWith("#skill/"))
);
```

### Rendering Components
```javascript
dv.header(2, "Active Skills");
dv.table(["Skill", "Category"], 
    skills.map(p => [p.file.link, p.category])
);
```

## Common patterns

### The Quick Stats Counter
Used for high-level dashboard summaries.
```javascript
try {
    const pages = dv.pages("#type/note");
    const count = pages.length;
    dv.table(["Metric", "Count"], [
        ["Total Knowledge Assets", count]
    ]);
} catch (e) {
    dv.paragraph("⚠️ Error loading stats.");
}
```

### The CSS Grid Skill Card
For visually engaging resource indexes (requires `dashboard` cssclass in frontmatter).
```javascript
const groups = skills.groupBy(p => p.category);
for (const group of groups) {
    dv.header(3, group.key);
    dv.list(group.rows.file.link);
}
```

## Error handling

**MANDATORY TEMPLATE**: Never write naked DataviewJS. Always use this wrapper:
```javascript
try {
    // 1. Gather Data
    const data = dv.pages("#tag").where(condition);
    // 2. Process Data
    if (data.length === 0) {
        dv.paragraph("No matching resources found.");
        return;
    }
    // 3. Render Data
    dv.list(data.file.link);
} catch (e) {
    console.error("Dataview Error:", e);
    dv.paragraph("⚠️ Error rendering view. Check console for details.");
}
```

## Anti-patterns to avoid

- ❌ **Static Tables**: Manual markdown tables in index pages. These go out of date instantly.
- ❌ **Naked JS**: DataviewJS without `try/catch`. This causes the entire page to break if a single note has malformed metadata.
- ❌ **Vault-Wide Scoping**: Using `dv.pages()` without `where` or `FROM` filters. This is slow and pulls irrelevant data.
- ❌ **Hardcoded Values**: Hardcoding dates or counts that should be derived from note metadata.
- ❌ **American English**: Using `color` instead of `colour` or `initialize` instead of `initialise` in labels.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Session-Knowledge/Obsidian Dataview Expert.md`

## Related skills

- `obsidian-frontmatter`: Source of truth for all Dataview queries.
- `obsidian-structure`: Defines the PARA paths used for scoped queries.
- `british-english`: Ensures consistency in all rendered dashboard text.
- `obsidian-customjs-expert`: For offloading complex logic to shared scripts.
