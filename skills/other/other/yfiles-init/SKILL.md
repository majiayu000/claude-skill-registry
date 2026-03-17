---
name: yfiles-init
description: Initializes new yFiles for HTML applications with GraphComponent, license registration, and basic setup. Use when creating demos, starting projects, scaffolding applications, or when user mentions "create app", "new demo", "initialize", or "setup yfiles".
---

# Initialize yFiles Application

Creates a complete yFiles application following package conventions.

## Quick Start

```
/yfiles-init [demo-name]
```

Creates in current directory if no name specified.

## Setup Checklist

Copy this checklist and track progress:

```
Setup Progress:
- [ ] Verify GraphComponent API with yFiles MCP
- [ ] Create HTML entry point
- [ ] Create main TypeScript/JavaScript file
- [ ] Adjust import paths for license
- [ ] Configure ESLint with yFiles plugin (recommended)
- [ ] Test in browser
```

## Implementation

**Step 1: Verify APIs**

Use yFiles MCP server to confirm current API:

```
yfiles:yfiles_get_symbol_details(name="GraphComponent")
yfiles:yfiles_list_members(name="GraphComponent", includeInherited=true)
```

**Step 2: Create files**

See [examples.md](examples.md) for complete file templates.

**Essential pattern:**
```typescript
import { GraphComponent, GraphEditorInputMode, License } from '@yfiles/yfiles'
import licenseData from '../../lib/license.json'

License.value = licenseData  // MUST come first

const graphComponent = new GraphComponent('#graphComponent')
graphComponent.inputMode = new GraphEditorInputMode()
```

**Step 3: Adjust import paths**

License path depends on demo location:
- `demos-ts/category/demo/`: Use `../../../lib/license.json`
- Adjust depth as needed

**Step 4: Configure ESLint (Recommended)**

The official `@yfiles/eslint-plugin` helps catch common mistakes and ensures yFiles 3.0 best practices:

```bash
npm i -D eslint typescript typescript-eslint @yfiles/eslint-plugin
```

See [reference.md](reference.md) for complete ESLint configuration.

**Step 5: Test**

```bash
npm start
# Navigate to http://localhost:4242/demos-ts/your-demo/
```

## Key Rules

- **License first**: `License.value = licenseData` before any yFiles API
- **Use CSS selectors**: `new GraphComponent('#id')` or `new GraphComponent(element)`
- **Access graph via**: `graphComponent.graph`
- **Set defaults before creating**: Configure `graph.nodeDefaults.style` before `createNode()`

## Reference Files

- **[examples.md](examples.md)**: Complete code templates
- **[reference.md](reference.md)**: API patterns and options

## MCP Tools for Reference

- `yfiles:yfiles_get_symbol_details` - Get API details
- `yfiles:yfiles_search_symbols` - Find classes/interfaces
- `yfiles:yfiles_search_documentation` - Find tutorials
