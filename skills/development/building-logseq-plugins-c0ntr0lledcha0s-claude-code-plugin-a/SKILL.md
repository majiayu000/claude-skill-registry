---
name: building-logseq-plugins
version: 1.0.0
description: >
  Expert guidance for building Logseq plugins compatible with the new DB architecture.
  Auto-invokes when users want to create Logseq plugins, work with the Logseq Plugin API,
  extend Logseq functionality, or need help with plugin development for DB-based graphs.
  Covers plugin structure, API usage, and DB-specific considerations.
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch, Write, Edit, Bash
---

# Building Logseq Plugins

## When to Use This Skill

This skill auto-invokes when:
- User wants to create a Logseq plugin
- Questions about the Logseq Plugin API
- Working with logseq.Editor, logseq.DB, logseq.App namespaces
- Slash command registration
- Plugin settings schema definition
- DB vs MD version compatibility for plugins
- User mentions "logseq plugin", "logseq extension", "@logseq/libs"

You are an expert in Logseq plugin development, with special focus on DB-version compatibility.

## Plugin Architecture Overview

Logseq plugins run in sandboxed iframes and communicate with the main app via the Plugin API.

### Plugin Structure

```
my-logseq-plugin/
├── package.json          # Plugin manifest
├── index.html            # Entry point
├── index.js              # Main logic (or TypeScript)
├── icon.png              # Plugin icon (optional)
└── README.md             # Documentation
```

### package.json Manifest

```json
{
  "name": "logseq-my-plugin",
  "version": "1.0.0",
  "main": "index.html",
  "logseq": {
    "id": "my-plugin-id",
    "title": "My Plugin",
    "icon": "./icon.png",
    "description": "Plugin description"
  }
}
```

## Plugin API Basics

### Initialization

```javascript
import '@logseq/libs'

async function main() {
  console.log('Plugin loaded')

  // Register commands, settings, etc.
  logseq.Editor.registerSlashCommand('My Command', async () => {
    // Command logic
  })
}

logseq.ready(main).catch(console.error)
```

### Key API Namespaces

| Namespace | Purpose |
|-----------|---------|
| `logseq.Editor` | Block/page manipulation |
| `logseq.DB` | Database queries |
| `logseq.App` | App-level operations |
| `logseq.UI` | UI components |
| `logseq.Settings` | Plugin settings |

## DB-Version Specific APIs

### Working with Properties

```javascript
// Get block with properties (DB version)
const block = await logseq.Editor.getBlock(blockUuid, {
  includeChildren: true
})

// Properties are structured differently in DB version
// Access via block.properties object
const author = block.properties?.author

// Set property value
await logseq.Editor.upsertBlockProperty(blockUuid, 'author', 'John Doe')
```

### Working with Classes/Tags

```javascript
// Get blocks with a specific tag/class
const books = await logseq.DB.datascriptQuery(`
  [:find (pull ?b [*])
   :where
   [?b :block/tags ?t]
   [?t :block/title "Book"]]
`)

// Add tag to block
await logseq.Editor.upsertBlockProperty(blockUuid, 'tags', ['Book', 'Fiction'])
```

### Enhanced Block Properties APIs (2024+)

```javascript
// New APIs for DB version
await logseq.Editor.getBlockProperties(blockUuid)
await logseq.Editor.setBlockProperties(blockUuid, {
  author: 'Jane Doe',
  rating: 5,
  published: '2024-01-15'
})
```

## Datalog Queries in Plugins

### Basic Query

```javascript
const results = await logseq.DB.datascriptQuery(`
  [:find ?title
   :where
   [?p :block/title ?title]
   [?p :block/tags ?t]
   [?t :db/ident :logseq.class/Page]]
`)
```

### Query with Parameters

```javascript
const results = await logseq.DB.datascriptQuery(`
  [:find (pull ?b [*])
   :in $ ?tag-name
   :where
   [?b :block/tags ?t]
   [?t :block/title ?tag-name]]
`, ['Book'])
```

### DB vs MD Query Differences

```javascript
// MD version - file-based queries
const mdQuery = `
  [:find ?content
   :where
   [?b :block/content ?content]
   [?b :block/page ?p]
   [?p :block/name "my-page"]]
`

// DB version - entity-based queries
const dbQuery = `
  [:find ?title
   :where
   [?b :block/title ?title]
   [?b :block/tags ?t]
   [?t :block/title "My Tag"]]
`
```

## UI Components

### Slash Commands

```javascript
logseq.Editor.registerSlashCommand('Insert Book Template', async () => {
  await logseq.Editor.insertAtEditingCursor(`
- [[New Book]] #Book
  author::
  rating::
  status:: To Read
`)
})
```

### Block Context Menu

```javascript
logseq.Editor.registerBlockContextMenuItem('Convert to Task', async (e) => {
  const block = await logseq.Editor.getBlock(e.uuid)
  await logseq.Editor.upsertBlockProperty(e.uuid, 'tags', ['Task'])
  await logseq.Editor.upsertBlockProperty(e.uuid, 'status', 'Todo')
})
```

### Settings Schema

```javascript
logseq.useSettingsSchema([
  {
    key: 'apiKey',
    type: 'string',
    title: 'API Key',
    description: 'Your API key for the service',
    default: ''
  },
  {
    key: 'enableFeature',
    type: 'boolean',
    title: 'Enable Feature',
    default: true
  },
  {
    key: 'theme',
    type: 'enum',
    title: 'Theme',
    enumChoices: ['light', 'dark', 'auto'],
    default: 'auto'
  }
])
```

## DB-Version Compatibility Checklist

When building plugins for DB version:

- [ ] Use `:block/title` instead of `:block/content` for page names
- [ ] Handle structured properties (not just strings)
- [ ] Support typed property values (numbers, dates, checkboxes)
- [ ] Use tag-based queries instead of namespace queries
- [ ] Test with both DB and MD graphs if supporting both
- [ ] Handle the unified node model (pages ≈ blocks)
- [ ] Use new block properties APIs when available

## Common Patterns

### Feature Detection

```javascript
async function isDBGraph() {
  // Check if current graph is DB-based
  const graph = await logseq.App.getCurrentGraph()
  return graph?.name?.includes('db-') || graph?.type === 'db'
}

async function main() {
  const isDB = await isDBGraph()
  if (isDB) {
    // DB-specific initialization
  } else {
    // MD-specific initialization
  }
}
```

### Property Type Handling

```javascript
function formatPropertyValue(value, type) {
  switch (type) {
    case 'date':
      return new Date(value).toISOString().split('T')[0]
    case 'number':
      return Number(value)
    case 'checkbox':
      return Boolean(value)
    case 'node':
      return `[[${value}]]`
    default:
      return String(value)
  }
}
```

## Development Workflow

1. **Setup**: Clone logseq-plugin-template or start fresh
2. **Develop**: Use `npm run dev` for hot reload
3. **Test**: Load unpacked plugin in Logseq
4. **Build**: `npm run build` for production
5. **Publish**: Submit to Logseq Marketplace

### Loading Development Plugin

```
Logseq > Settings > Advanced > Developer Mode: ON
Logseq > Plugins > Load unpacked plugin > Select folder
```

## Resources

- [Logseq Plugin SDK](https://plugins-doc.logseq.com/)
- [Plugin API Reference](https://logseq.github.io/plugins/)
- [Plugin Examples](https://github.com/logseq/logseq-plugin-samples)
