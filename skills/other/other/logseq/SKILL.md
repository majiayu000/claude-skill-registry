---
name: logseq
description: Provide commands for interacting with a local Logseq instance through its Plugin API. Use for creating pages, inserting blocks, querying the graph database, managing tasks, retrieving content, or automating workflows in Logseq. Only works with a locally running instance with the API enabled; default port or set path expected for [$API accessible skill].
---

# Logseq Plugin API

Interact with your local Logseq instance through its JavaScript Plugin API. This skill enables reading, writing, querying, and automating workflows in your Logseq graph.

## Prerequisites

**Logseq must be running locally** with a plugin that exposes the API. The standard way is:

1. **Install a bridge plugin** that exposes `logseq` API via HTTP (e.g., via a custom plugin or localhost endpoint)
2. **Alternative**: Use Node.js with `@logseq/libs` package to script against the running Logseq instance

The API is primarily designed for in-browser plugins, so accessing it from external scripts requires a bridge/proxy.

## Core API Namespaces

The Logseq Plugin API is organized into these main proxies:

### `logseq.App`
Application-level operations: getting app info, user configs, current graph, commands, UI state, external links.

**Key methods:**
- `getInfo()` - Get app version and info
- `getUserConfigs()` - Get user preferences (theme, format, language, etc.)
- `getCurrentGraph()` - Get current graph info (name, path, URL)
- `registerCommand(type, opts, action)` - Register custom commands
- `pushState(route, params, query)` - Navigate to routes

### `logseq.Editor`
Block and page editing operations: creating, updating, moving, querying content.

**Key methods:**
- `getBlock(uuid)` - Get block by UUID
- `getCurrentPage()` - Get current page entity
- `getCurrentPageBlocksTree()` - Get all blocks on current page
- `getPageBlocksTree(page)` - Get all blocks for a specific page
- `insertBlock(target, content, opts)` - Insert a new block
- `updateBlock(uuid, content)` - Update block content
- `createPage(pageName, properties, opts)` - Create a new page
- `deletePage(pageName)` - Delete a page
- `getPageLinkedReferences(page)` - Get backlinks to a page
- `registerSlashCommand(tag, action)` - Add custom slash commands

### `logseq.DB`
Database queries using Datalog.

**Key methods:**
- `q(query, ...inputs)` - Run Datalog query
- `datascriptQuery(query, ...inputs)` - Direct Datascript query

### `logseq.UI`
UI operations: messages, dialogs, main UI visibility.

**Key methods:**
- `showMsg(content, status)` - Show toast notification
- `queryElementById(id)` - Query DOM elements

### `logseq.Git`
Git operations for the current graph.

**Key methods:**
- `execCommand(args)` - Execute git command

### `logseq.Assets`
Asset management.

**Key methods:**
- `listFilesOfCurrentGraph(path)` - List files in graph

## Common Workflows

### Read Content

```javascript
// Get current page
const page = await logseq.Editor.getCurrentPage();

// Get all blocks on a page
const blocks = await logseq.Editor.getPageBlocksTree('Daily Notes');

// Get a specific block
const block = await logseq.Editor.getBlock('block-uuid-here');

// Query with Datalog
const results = await logseq.DB.q(`
  [:find (pull ?b [*])
   :where [?b :block/marker "TODO"]]
`);
```

### Write Content

```javascript
// Create a new page
await logseq.Editor.createPage('Project Notes', {
  tags: 'project',
  status: 'active'
}, { redirect: false });

// Insert a block
const block = await logseq.Editor.insertBlock(
  'target-block-uuid',
  '- New task item',
  { before: false, sibling: true }
);

// Update a block
await logseq.Editor.updateBlock('block-uuid', 'Updated content');

// Batch insert multiple blocks
const blocks = [
  { content: 'First item' },
  { content: 'Second item', children: [
    { content: 'Nested item' }
  ]}
];
await logseq.Editor.insertBatchBlock('parent-uuid', blocks, { sibling: false });
```

### Task Management

```javascript
// Find all TODO items
const todos = await logseq.DB.q(`
  [:find (pull ?b [*])
   :where
   [?b :block/marker ?marker]
   [(contains? #{"TODO" "DOING"} ?marker)]]
`);

// Mark task as DONE
await logseq.Editor.updateBlock('task-uuid', 'DONE Task content');

// Get tasks on current page
const page = await logseq.Editor.getCurrentPage();
const blocks = await logseq.Editor.getPageBlocksTree(page.name);
const tasks = blocks.filter(b => b.marker === 'TODO' || b.marker === 'DOING');
```

### Navigation and UI

```javascript
// Navigate to a page
logseq.App.pushState('page', { name: 'Project Notes' });

// Show notification
logseq.UI.showMsg('✅ Task completed!', 'success');

// Get app config
const configs = await logseq.App.getUserConfigs();
console.log('Theme:', configs.preferredThemeMode);
console.log('Format:', configs.preferredFormat);
```

## Implementation Approaches

Since Logseq's Plugin API is browser-based, you have several options:

### Option 1: Bridge Plugin
Create a minimal Logseq plugin that exposes API calls via HTTP:

```javascript
// In Logseq plugin (index.js)
logseq.ready(() => {
  // Expose API endpoints
  logseq.provideModel({
    async handleAPICall({ method, args }) {
      return await logseq.Editor[method](...args);
    }
  });
});

// Then call from external script via HTTP POST
```

### Option 2: Node.js Script with @logseq/libs
For automation scripts, use the `@logseq/libs` package:

```bash
npm install @logseq/libs
```

**Note:** This requires a running Logseq instance and proper connection setup.

### Option 3: Direct Plugin Development
Develop a full Logseq plugin following the plugin samples at:
https://github.com/logseq/logseq-plugin-samples

## API Reference

For complete API documentation, see:
- **API Docs**: https://logseq.github.io/plugins/
- **Plugin Samples**: https://github.com/logseq/logseq-plugin-samples
- **Type Definitions**: `references/api-types.md` (extracted from `@logseq/libs`)

## Key Data Structures

### BlockEntity
```typescript
{
  id: number,           // Entity ID
  uuid: string,         // Block UUID
  content: string,      // Block content
  format: 'markdown' | 'org',
  page: { id: number }, // Parent page
  parent: { id: number }, // Parent block
  left: { id: number }, // Previous sibling
  properties: {},       // Block properties
  marker?: string,      // TODO/DOING/DONE
  children?: []         // Child blocks
}
```

### PageEntity
```typescript
{
  id: number,
  uuid: string,
  name: string,              // Page name (lowercase)
  originalName: string,       // Original case
  'journal?': boolean,
  properties: {},
  journalDay?: number,       // YYYYMMDD for journals
}
```

## Tips & Best Practices

1. **Always check for null**: API methods may return `null` if entity doesn't exist
2. **Use UUIDs over IDs**: Block UUIDs are stable, entity IDs can change
3. **Batch operations**: Use `insertBatchBlock` for multiple inserts
4. **Query efficiently**: Datalog queries are powerful but can be slow on large graphs
5. **Properties are objects**: Access with `block.properties.propertyName`
6. **Format matters**: Respect user's preferred format (markdown vs org-mode)
7. **Async all the way**: All API calls return Promises

## Common Gotchas

- **Page names are lowercase**: When querying, use lowercase page names
- **Journal pages**: Use `journalDay` format (YYYYMMDD) not date strings
- **Block hierarchy**: Respect parent/child relationships when inserting
- **Format differences**: Markdown uses `-` for bullets, Org uses `*`
- **Properties syntax**: Different between markdown (`prop::`) and org (`:PROPERTIES:`)
