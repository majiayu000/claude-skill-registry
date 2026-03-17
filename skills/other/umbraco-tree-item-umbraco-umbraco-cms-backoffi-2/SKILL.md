---
name: umbraco-tree-item
description: Implement tree items in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Tree Item

## What is it?
Tree Items define how entities are rendered in tree structures throughout the Umbraco backoffice. They control the visual representation and behavior of items in sidebars and navigation trees. Tree items are associated with entity types and can be customized to display additional information, icons, or custom rendering for specific entity types.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/tree
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## When to Use Custom Tree Item Contexts

Most tree items use `kind: 'default'` and **don't need a custom context**. Only create a custom context for:

- **Custom icon logic** - Dynamic icons based on item state
- **Custom labels or badges** - Additional visual information
- **Special rendering** - Unique behavior for specific entity types
- **Additional item behaviors** - Click handlers, drag-and-drop, etc.

If you just need standard tree items, use `kind: 'default'` without a custom context.

## Related Foundation Skills

- **Tree**: Tree items work within tree structures
  - Reference skill: `umbraco-tree`
  - **IMPORTANT**: Tree stores are deprecated in Umbraco 14+, see that skill for details

- **Repository Pattern**: When loading tree data
  - Reference skill: `umbraco-repository-pattern`

- **Context API**: When accessing tree context
  - Reference skill: `umbraco-context-api`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What entity types? What custom rendering?
3. **Generate files** - Create manifest + optional element/context
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Basic Manifest (manifests.ts)
```typescript
export const manifests: Array<UmbExtensionManifest> = [
  {
    type: 'treeItem',
    kind: 'default',
    alias: 'My.TreeItem',
    name: 'My Tree Item',
    forEntityTypes: ['my-entity-type'],
  },
];
```

### Custom Tree Item with Context
```typescript
import { MY_ENTITY_TYPE, MY_ROOT_ENTITY_TYPE } from '../entity.js';

export const manifests: Array<UmbExtensionManifest> = [
  {
    type: 'treeItem',
    kind: 'default',
    alias: 'My.TreeItem.Custom',
    name: 'My Custom Tree Item',
    forEntityTypes: [MY_ENTITY_TYPE, MY_ROOT_ENTITY_TYPE],
    api: () => import('./my-tree-item.context.js'),
  },
];
```

### Tree Item Context (my-tree-item.context.ts)
```typescript
import { UmbDefaultTreeItemContext } from '@umbraco-cms/backoffice/tree';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';
import type { UmbTreeItemModel, UmbTreeRootModel } from '@umbraco-cms/backoffice/tree';

export class MyTreeItemContext extends UmbDefaultTreeItemContext<
  UmbTreeItemModel,
  UmbTreeRootModel
> {
  constructor(host: UmbControllerHost) {
    super(host);
  }

  // Override to customize icon
  override async getIcon() {
    const item = this.getTreeItem();
    if (item?.hasChildren) {
      return 'icon-folder';
    }
    return 'icon-document';
  }

  // Override to add custom labels/badges
  override async getLabel() {
    const item = this.getTreeItem();
    return item?.name ?? 'Unknown';
  }
}

export { MyTreeItemContext as api };
```

### Complete Tree with Tree Item
```typescript
import { MY_ENTITY_TYPE, MY_ROOT_ENTITY_TYPE } from './entity.js';
import { MY_TREE_ALIAS, MY_TREE_REPOSITORY_ALIAS } from './constants.js';

export const manifests: Array<UmbExtensionManifest> = [
  // Tree definition
  {
    type: 'tree',
    kind: 'default',
    alias: MY_TREE_ALIAS,
    name: 'My Tree',
    meta: {
      repositoryAlias: MY_TREE_REPOSITORY_ALIAS,
    },
  },
  // Tree item for the entities
  {
    type: 'treeItem',
    kind: 'default',
    alias: 'My.TreeItem',
    name: 'My Tree Item',
    forEntityTypes: [MY_ROOT_ENTITY_TYPE, MY_ENTITY_TYPE],
  },
];
```

## Interface Reference

```typescript
interface ManifestTreeItem extends ManifestElementAndApi<UmbControllerHostElement, UmbTreeItemContext> {
  type: 'treeItem';
  forEntityTypes: Array<string>;  // Entity types this tree item renders
}
```

## Common Entity Types

Built-in entity types that have tree items:
- `document` - Content nodes
- `document-root` - Content root
- `media` - Media items
- `media-root` - Media root
- `member` - Members
- `data-type` - Data types
- `document-type` - Document types
- `template` - Templates

## Kinds

The `kind: 'default'` uses the standard tree item rendering. Custom kinds can be created for specialized rendering.

## Best Practices

- Use appropriate icons for different entity types
- Consider loading states for async data
- Keep tree items lightweight for performance
- Use entity type constants for type safety

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
