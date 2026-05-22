---
name: umbraco-tree
description: Implement trees in Umbraco backoffice using official docs
version: 1.2.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Tree

## What is it?
A tree in Umbraco is a hierarchical structure of nodes registered in the Backoffice extension registry. Trees display organized content hierarchies and can be rendered anywhere in the Backoffice using the `<umb-tree />` element. They require a data source implementation to fetch root items, children, and ancestors.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/tree
- **Sections & Trees**: https://docs.umbraco.com/umbraco-cms/customizing/overview
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## CRITICAL: Tree + Workspace Integration

**Trees and workspaces are tightly coupled.** When using `kind: 'default'` tree items:

1. **Tree items REQUIRE workspaces** - Clicking a tree item navigates to a workspace for that entity type. Without a workspace registered for the `entityType`, clicking causes "forever loading"

2. **Workspaces must be `kind: 'routable'`** - For proper tree item selection state and navigation between items of the same type, use `kind: 'routable'` workspaces (not `kind: 'default'`)

3. **Entity types link trees to workspaces** - The `entityType` in your tree item data must match the `entityType` in your workspace manifest

When implementing trees with clickable items, also reference the `umbraco-workspace` skill.

## File Structure

Modern trees use 2-3 files:
```
my-tree/
├── manifest.ts          # Registers repository and tree
├── tree.repository.ts   # Repository + inline data source
└── types.ts             # Type definitions (optional)
```

## Reference Example

The Umbraco source includes a working example:

**Location**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/tree/`

This example demonstrates a complete custom tree with data source, repository, and menu integration. Study this for production patterns.

## Related Foundation Skills

If you need to explain these foundational concepts when implementing trees, reference these skills:

- **Repository Pattern**: When implementing tree data sources, repositories, data fetching, or CRUD operations
  - Reference skill: `umbraco-repository-pattern`

- **Context API**: When implementing repository contexts or explaining how repositories connect to UI components
  - Reference skill: `umbraco-context-api`

- **State Management**: When implementing reactive tree updates, observables, or managing tree state
  - Reference skill: `umbraco-state-management`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What data will the tree display? What repository will provide the data? Where will it appear? **Will tree items be clickable?**
3. **Generate files** - Create minimal files based on latest docs
   - ✅ Create: `manifest.ts`, `tree.repository.ts` (with inline data source)
   - ❌ Don't create: `tree.store.ts` (deprecated), separate `tree.data-source.ts` (can inline)
   - **Use the inline data source pattern** shown in examples below
4. **If clickable** - Also create routable workspaces for each entity type (reference `umbraco-workspace` skill)
5. **Explain** - Show what was created and how to test

## Key Configuration Options

### hideTreeRoot on MenuItem (NOT on Tree)
To show tree items at root level (without a parent folder), use `hideTreeRoot: true` on the **menuItem** manifest:

```typescript
// CORRECT - hideTreeRoot on menuItem
{
  type: 'menuItem',
  kind: 'tree',
  alias: 'My.MenuItem.Tree',
  meta: {
    treeAlias: 'My.Tree',
    menus: ['My.Menu'],
    hideTreeRoot: true,  // Shows items at root level
  },
}

// WRONG - hideTreeRoot on tree (has no effect)
{
  type: 'tree',
  meta: {
    hideTreeRoot: true,  // This does nothing!
  },
}
```

## Minimal Examples

### Tree Manifest
```typescript
export const manifests: UmbExtensionManifest[] = [
  // Repository
  {
    type: 'repository',
    alias: 'My.Tree.Repository',
    name: 'My Tree Repository',
    api: () => import('./tree.repository.js'),
  },
  // Tree
  {
    type: 'tree',
    kind: 'default',
    alias: 'My.Tree',
    name: 'My Tree',
    meta: {
      repositoryAlias: 'My.Tree.Repository',
    },
  },
  // Tree Items - use kind: 'default' when workspaces exist
  {
    type: 'treeItem',
    kind: 'default',
    alias: 'My.TreeItem',
    name: 'My Tree Item',
    forEntityTypes: ['my-entity'],
  },
  // MenuItem - hideTreeRoot here
  {
    type: 'menuItem',
    kind: 'tree',
    alias: 'My.MenuItem.Tree',
    meta: {
      treeAlias: 'My.Tree',
      menus: ['My.Menu'],
      hideTreeRoot: true,
    },
  },
];
```

### Repository with Inline Data Source (tree.repository.ts)

**Modern simplified pattern - everything in one file:**

```typescript
import { UmbTreeRepositoryBase, UmbTreeServerDataSourceBase } from '@umbraco-cms/backoffice/tree';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';
import type { UmbApi } from '@umbraco-cms/backoffice/extension-api';
import type { MyTreeItemModel, MyTreeRootModel } from './types.js';
import { MY_ROOT_ENTITY_TYPE, MY_ENTITY_TYPE } from './entity.js';

// Data source as simple class using helper base
class MyTreeDataSource extends UmbTreeServerDataSourceBase<any, MyTreeItemModel> {
  constructor(host: UmbControllerHost) {
    super(host, {
      getRootItems: async (args) => {
        // Fetch from API or return mock data
        const items: MyTreeItemModel[] = [
          {
            unique: 'item-1',
            parent: { unique: null, entityType: MY_ROOT_ENTITY_TYPE },
            entityType: MY_ENTITY_TYPE,
            name: 'Item 1',
            hasChildren: false,
            isFolder: false,
            icon: 'icon-document',
          },
        ];
        return { data: { items, total: items.length } };
      },
      getChildrenOf: async (args) => {
        // Return children for parent
        return { data: { items: [], total: 0 } };
      },
      getAncestorsOf: async (args) => {
        // Return ancestor path
        return { data: [] };
      },
      mapper: (item: any) => item, // Identity mapper for this example
    });
  }
}

// Repository
export class MyTreeRepository
  extends UmbTreeRepositoryBase<MyTreeItemModel, MyTreeRootModel>
  implements UmbApi
{
  constructor(host: UmbControllerHost) {
    super(host, MyTreeDataSource);
  }

  async requestTreeRoot() {
    const data: MyTreeRootModel = {
      unique: null,
      entityType: MY_ROOT_ENTITY_TYPE,
      name: 'My Tree',
      hasChildren: true,
      isFolder: true,
    };
    return { data };
  }
}

export { MyTreeRepository as api };
```

**Why this is simpler:**
- ✅ One file instead of two
- ✅ Uses `UmbTreeServerDataSourceBase` helper (pass functions, not methods)
- ✅ Data fetching logic inline (easier to understand)
- ✅ No separate data source file to maintain

**For complex trees with API calls**, you can still separate into different files, but it's not required.

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
