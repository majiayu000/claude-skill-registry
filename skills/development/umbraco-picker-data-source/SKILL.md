---
name: umbraco-picker-data-source
description: Implement custom picker data sources for property editors in Umbraco backoffice
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Picker Data Source

## What is it?

A Picker Data Source provides data for picker-based property editors. It allows you to create custom data sources that supply items for content pickers, defining how items are fetched, searched, and displayed in a tree or collection format. This is useful for creating pickers that select from custom entities, external APIs, or filtered subsets of existing content.

## Documentation

Always fetch the latest docs before implementing:

- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry
- **Property Editors**: https://docs.umbraco.com/umbraco-cms/customizing/property-editors

## Reference Example

The Umbraco source includes working examples:

**Location**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/picker-data-source/`

This example demonstrates multiple picker data source implementations:
- Custom collection picker
- Custom tree picker with search
- Document picker with start node configuration
- Media, Language, Webhook, and User pickers

## Related Foundation Skills

- **Repository Pattern**: For data fetching patterns
  - Reference skill: `umbraco-repository-pattern`

- **Tree**: For tree-based picker data sources
  - Reference skill: `umbraco-tree`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What data to pick? Tree or collection? Search needed? Configuration options?
3. **Generate files** - Create manifest + data source class based on latest docs
4. **Explain** - Show what was created and how to use with a property editor

---

## Manifest Example

```typescript
import { UMB_PICKER_DATA_SOURCE_TYPE } from '@umbraco-cms/backoffice/picker-data-source';

export const manifests: Array<UmbExtensionManifest> = [
  {
    type: 'propertyEditorDataSource',
    dataSourceType: UMB_PICKER_DATA_SOURCE_TYPE,
    alias: 'My.PropertyEditorDataSource.CustomPicker',
    name: 'Custom Picker Data Source',
    api: () => import('./my-picker-data-source.js'),
    meta: {
      label: 'Custom Items',
      icon: 'icon-list',
      description: 'Pick from custom items',
    },
  },
];
```

---

## Tree Picker Data Source

For hierarchical data with parent-child relationships:

```typescript
import { UmbControllerBase } from '@umbraco-cms/backoffice/class-api';
import type {
  UmbPickerSearchableDataSource,
  UmbPickerTreeDataSource,
} from '@umbraco-cms/backoffice/picker-data-source';
import type { UmbSearchRequestArgs, UmbSearchResultItemModel } from '@umbraco-cms/backoffice/search';
import type { UmbTreeChildrenOfRequestArgs, UmbTreeItemModel } from '@umbraco-cms/backoffice/tree';

export class MyPickerTreeDataSource
  extends UmbControllerBase
  implements UmbPickerTreeDataSource, UmbPickerSearchableDataSource
{
  // Filter function to determine which items can be picked
  treePickableFilter: (treeItem: UmbTreeItemModel) => boolean = (treeItem) =>
    !!treeItem.unique && treeItem.entityType === 'my-entity';

  searchPickableFilter: (searchItem: UmbSearchResultItemModel) => boolean = (searchItem) =>
    !!searchItem.unique && searchItem.entityType === 'my-entity';

  // Return the root node (container for all items)
  async requestTreeRoot() {
    return {
      data: {
        unique: null,
        name: 'My Items',
        icon: 'icon-folder',
        hasChildren: true,
        entityType: 'my-entity-root',
        isFolder: true,
      },
    };
  }

  // Return items at the root level
  async requestTreeRootItems() {
    const rootItems = myItems.filter((item) => item.parent.unique === null);
    return {
      data: {
        items: rootItems,
        total: rootItems.length,
      },
    };
  }

  // Return children of a specific item
  async requestTreeItemsOf(args: UmbTreeChildrenOfRequestArgs) {
    const items = myItems.filter(
      (item) =>
        item.parent.entityType === args.parent.entityType &&
        item.parent.unique === args.parent.unique
    );
    return {
      data: {
        items: items,
        total: items.length,
      },
    };
  }

  // Return ancestors for breadcrumb navigation
  async requestTreeItemAncestors() {
    return { data: [] };
  }

  // Return specific items by their unique IDs
  async requestItems(uniques: Array<string>) {
    const items = myItems.filter((x) => uniques.includes(x.unique));
    return { data: items };
  }

  // Search items by query string
  async search(args: UmbSearchRequestArgs) {
    const result = myItems.filter((item) =>
      item.name.toLowerCase().includes(args.query.toLowerCase())
    );
    return {
      data: {
        items: result,
        total: result.length,
      },
    };
  }
}

export { MyPickerTreeDataSource as api };

// Sample data
const myItems: Array<UmbTreeItemModel> = [
  {
    unique: '1',
    entityType: 'my-entity',
    name: 'Item 1',
    icon: 'icon-document',
    parent: { unique: null, entityType: 'my-entity-root' },
    isFolder: false,
    hasChildren: false,
  },
  {
    unique: '2',
    entityType: 'my-entity',
    name: 'Item 2',
    icon: 'icon-document',
    parent: { unique: null, entityType: 'my-entity-root' },
    isFolder: false,
    hasChildren: false,
  },
];
```

---

## Collection Picker Data Source

For flat lists without hierarchy:

```typescript
import { UmbControllerBase } from '@umbraco-cms/backoffice/class-api';
import type { UmbPickerCollectionDataSource } from '@umbraco-cms/backoffice/picker-data-source';
import type { UmbCollectionItemModel } from '@umbraco-cms/backoffice/collection';

export class MyPickerCollectionDataSource
  extends UmbControllerBase
  implements UmbPickerCollectionDataSource
{
  async requestCollection() {
    const items: UmbCollectionItemModel[] = [
      { unique: '1', entityType: 'my-entity', name: 'Item 1', icon: 'icon-document' },
      { unique: '2', entityType: 'my-entity', name: 'Item 2', icon: 'icon-document' },
      { unique: '3', entityType: 'my-entity', name: 'Item 3', icon: 'icon-document' },
    ];

    return {
      data: {
        items,
        total: items.length,
      },
    };
  }

  async requestItems(uniques: Array<string>) {
    // Return specific items by unique IDs
    const allItems = await this.requestCollection();
    const items = allItems.data.items.filter((x) => uniques.includes(x.unique));
    return { data: items };
  }
}

export { MyPickerCollectionDataSource as api };
```

---

## Data Source with Configuration

Add settings to your picker data source:

```typescript
export const manifests: Array<UmbExtensionManifest> = [
  {
    type: 'propertyEditorDataSource',
    dataSourceType: UMB_PICKER_DATA_SOURCE_TYPE,
    alias: 'My.PropertyEditorDataSource.ConfigurablePicker',
    name: 'Configurable Picker Data Source',
    api: () => import('./my-configurable-picker-data-source.js'),
    meta: {
      label: 'Configurable Items',
      icon: 'icon-settings',
      description: 'Pick items with configuration options',
      settings: {
        properties: [
          {
            alias: 'startNode',
            label: 'Start Node',
            description: 'Select where to start picking from',
            propertyEditorUiAlias: 'Umb.PropertyEditorUi.ContentPicker.Source',
          },
          {
            alias: 'filter',
            label: 'Filter Types',
            description: 'Select which types can be picked',
            propertyEditorUiAlias: 'Umb.PropertyEditorUi.ContentPicker.SourceType',
          },
        ],
      },
    },
  },
];
```

---

## Interfaces

```typescript
interface UmbPickerTreeDataSource {
  treePickableFilter?: (treeItem: UmbTreeItemModel) => boolean;
  requestTreeRoot(): Promise<{ data: UmbTreeItemModel }>;
  requestTreeRootItems(): Promise<{ data: { items: UmbTreeItemModel[]; total: number } }>;
  requestTreeItemsOf(args: UmbTreeChildrenOfRequestArgs): Promise<{ data: { items: UmbTreeItemModel[]; total: number } }>;
  requestTreeItemAncestors(): Promise<{ data: UmbTreeItemModel[] }>;
  requestItems(uniques: string[]): Promise<{ data: UmbTreeItemModel[] }>;
}

interface UmbPickerSearchableDataSource {
  searchPickableFilter?: (searchItem: UmbSearchResultItemModel) => boolean;
  search(args: UmbSearchRequestArgs): Promise<{ data: { items: UmbSearchResultItemModel[]; total: number } }>;
}

interface UmbPickerCollectionDataSource {
  requestCollection(): Promise<{ data: { items: UmbCollectionItemModel[]; total: number } }>;
  requestItems(uniques: string[]): Promise<{ data: UmbCollectionItemModel[] }>;
}
```

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| `dataSourceType` | Must be `UMB_PICKER_DATA_SOURCE_TYPE` for picker data sources |
| `treePickableFilter` | Function to determine which tree items can be selected |
| `searchPickableFilter` | Function to determine which search results can be selected |
| `requestItems` | Returns items by their unique IDs (for displaying selected values) |
| `entityType` | Identifies the type of entity (used for filtering and routing) |

---

## Best Practices

1. **Implement search** - Users expect to search in pickers with many items
2. **Use appropriate icons** - Help users identify item types visually
3. **Filter pickable items** - Not all tree items should be selectable (e.g., folders)
4. **Handle configuration** - Support start nodes and type filters when applicable
5. **Return consistent data** - Ensure `requestItems` returns the same format as tree/collection

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
