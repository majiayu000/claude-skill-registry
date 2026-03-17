---
name: umbraco-collection
description: Implement collections in Umbraco backoffice using official docs
version: 1.1.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Collection

## What is it?
A Collection displays a list of entities in the Umbraco backoffice with built-in support for multiple views (table, grid), filtering, pagination, selection, and bulk actions. Collections connect to a repository for data and provide a standardized way to browse and interact with lists of items.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/collections
- **Collection View**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/collections/collection-view
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Collection Architecture

A complete collection consists of these components:

```
collection/
├── manifests.ts              # Main collection manifest
├── constants.ts              # Alias constants
├── types.ts                  # Item and filter types
├── my-collection.context.ts  # Collection context (extends UmbDefaultCollectionContext)
├── my-collection.element.ts  # Collection element (extends UmbCollectionDefaultElement)
├── repository/
│   ├── manifests.ts
│   ├── my-collection.repository.ts    # Implements UmbCollectionRepository
│   └── my-collection.data-source.ts   # API calls
├── views/
│   ├── manifests.ts
│   └── table/
│       └── my-table-view.element.ts   # Table view
└── action/
    ├── manifests.ts
    └── my-action.element.ts           # Collection action
```

## Reference Example

The Umbraco source includes a working example:

**Location**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/collection/`

This example demonstrates a complete custom collection with repository, views, and context. Study this for production patterns.

## Related Foundation Skills

- **Repository Pattern**: Collections require a repository for data access
  - Reference skill: `umbraco-repository-pattern`

- **Context API**: For accessing collection context in views
  - Reference skill: `umbraco-context-api`

- **State Management**: For understanding observables and reactive data
  - Reference skill: `umbraco-state-management`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What entities? What repository? What views needed? What actions?
3. **Define types** - Create item model and filter model interfaces
4. **Create repository** - Implement data source and repository
5. **Create context** - Extend `UmbDefaultCollectionContext` if custom behavior needed
6. **Create views** - Implement table/grid views
7. **Create actions** - Add collection actions (create, refresh, etc.)
8. **Explain** - Show what was created and how to test

## Complete Example

### 1. Constants (constants.ts)
```typescript
export const MY_COLLECTION_ALIAS = 'My.Collection';
export const MY_COLLECTION_REPOSITORY_ALIAS = 'My.Collection.Repository';
```

### 2. Types (types.ts)
```typescript
export interface MyCollectionItemModel {
  unique: string;
  entityType: string;
  name: string;
  // Add other fields
}

export interface MyCollectionFilterModel {
  skip?: number;
  take?: number;
  filter?: string;
  orderBy?: string;
  orderDirection?: 'asc' | 'desc';
  // Add custom filters
}
```

### 3. Data Source (repository/my-collection.data-source.ts)
```typescript
import type { MyCollectionItemModel, MyCollectionFilterModel } from '../types.js';
import type { UmbCollectionDataSource } from '@umbraco-cms/backoffice/collection';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';

export class MyCollectionDataSource implements UmbCollectionDataSource<MyCollectionItemModel> {
  #host: UmbControllerHost;

  constructor(host: UmbControllerHost) {
    this.#host = host;
  }

  async getCollection(filter: MyCollectionFilterModel) {
    // Call your API here
    const response = await fetch(`/api/my-items?skip=${filter.skip}&take=${filter.take}`);
    const data = await response.json();

    const items: MyCollectionItemModel[] = data.items.map((item: any) => ({
      unique: item.id,
      entityType: 'my-entity',
      name: item.name,
    }));

    return { data: { items, total: data.total } };
  }
}
```

### 4. Repository (repository/my-collection.repository.ts)
```typescript
import type { MyCollectionFilterModel } from '../types.js';
import { MyCollectionDataSource } from './my-collection.data-source.js';
import { UmbRepositoryBase } from '@umbraco-cms/backoffice/repository';
import type { UmbCollectionRepository } from '@umbraco-cms/backoffice/collection';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';

export class MyCollectionRepository extends UmbRepositoryBase implements UmbCollectionRepository {
  #dataSource: MyCollectionDataSource;

  constructor(host: UmbControllerHost) {
    super(host);
    this.#dataSource = new MyCollectionDataSource(host);
  }

  async requestCollection(filter: MyCollectionFilterModel) {
    return this.#dataSource.getCollection(filter);
  }
}

export default MyCollectionRepository;
```

### 5. Repository Manifest (repository/manifests.ts)
```typescript
import { MY_COLLECTION_REPOSITORY_ALIAS } from '../constants.js';

export const manifests: Array<UmbExtensionManifest> = [
  {
    type: 'repository',
    alias: MY_COLLECTION_REPOSITORY_ALIAS,
    name: 'My Collection Repository',
    api: () => import('./my-collection.repository.js'),
  },
];
```

### 6. Collection Context (my-collection.context.ts)
```typescript
import type { MyCollectionItemModel, MyCollectionFilterModel } from './types.js';
import { UmbDefaultCollectionContext } from '@umbraco-cms/backoffice/collection';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';

// Default view alias - must match one of your collectionView aliases
const MY_TABLE_VIEW_ALIAS = 'My.CollectionView.Table';

export class MyCollectionContext extends UmbDefaultCollectionContext<
  MyCollectionItemModel,
  MyCollectionFilterModel
> {
  constructor(host: UmbControllerHost) {
    super(host, MY_TABLE_VIEW_ALIAS);
  }

  // Override or add custom methods if needed
}

export { MyCollectionContext as api };
```

### 7. Collection Element (my-collection.element.ts)
```typescript
import { customElement } from '@umbraco-cms/backoffice/external/lit';
import { UmbCollectionDefaultElement } from '@umbraco-cms/backoffice/collection';

@customElement('my-collection')
export class MyCollectionElement extends UmbCollectionDefaultElement {
  // Override renderToolbar() to customize header
  // protected override renderToolbar() {
  //   return html`<umb-collection-toolbar slot="header"></umb-collection-toolbar>`;
  // }
}

export default MyCollectionElement;
export { MyCollectionElement as element };

declare global {
  interface HTMLElementTagNameMap {
    'my-collection': MyCollectionElement;
  }
}
```

### 8. Table View (views/table/my-table-view.element.ts)
```typescript
import type { MyCollectionItemModel } from '../../types.js';
import { UMB_COLLECTION_CONTEXT } from '@umbraco-cms/backoffice/collection';
import { css, customElement, html, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import type { UmbTableColumn, UmbTableConfig, UmbTableItem } from '@umbraco-cms/backoffice/components';

@customElement('my-table-collection-view')
export class MyTableCollectionViewElement extends UmbLitElement {
  @state()
  private _tableItems: Array<UmbTableItem> = [];

  @state()
  private _selection: Array<string> = [];

  #collectionContext?: typeof UMB_COLLECTION_CONTEXT.TYPE;

  private _tableConfig: UmbTableConfig = {
    allowSelection: true,
  };

  private _tableColumns: Array<UmbTableColumn> = [
    { name: 'Name', alias: 'name', allowSorting: true },
    { name: '', alias: 'entityActions', align: 'right' },
  ];

  constructor() {
    super();
    this.consumeContext(UMB_COLLECTION_CONTEXT, (context) => {
      this.#collectionContext = context;
      // IMPORTANT: Call setupView for workspace modal routing
      context?.setupView(this);
      this.#observeItems();
      this.#observeSelection();
    });
  }

  #observeItems() {
    if (!this.#collectionContext) return;

    this.observe(
      this.#collectionContext.items,
      (items) => {
        this._tableItems = (items as MyCollectionItemModel[]).map((item) => ({
          id: item.unique,
          icon: 'icon-document',
          entityType: item.entityType,
          data: [
            { columnAlias: 'name', value: item.name },
            {
              columnAlias: 'entityActions',
              value: html`<umb-entity-actions-table-column-view
                .value=${{ entityType: item.entityType, unique: item.unique }}
              ></umb-entity-actions-table-column-view>`,
            },
          ],
        }));
      },
      '_observeItems',
    );
  }

  #observeSelection() {
    if (!this.#collectionContext) return;

    this.observe(
      this.#collectionContext.selection.selection,
      (selection) => {
        this._selection = selection as string[];
      },
      '_observeSelection',
    );
  }

  #handleSelect(event: CustomEvent) {
    event.stopPropagation();
    const table = event.target as any;
    this.#collectionContext?.selection.setSelection(table.selection);
  }

  #handleDeselect(event: CustomEvent) {
    event.stopPropagation();
    const table = event.target as any;
    this.#collectionContext?.selection.setSelection(table.selection);
  }

  override render() {
    return html`
      <umb-table
        .config=${this._tableConfig}
        .columns=${this._tableColumns}
        .items=${this._tableItems}
        .selection=${this._selection}
        @selected=${this.#handleSelect}
        @deselected=${this.#handleDeselect}
      ></umb-table>
    `;
  }
}

export default MyTableCollectionViewElement;

declare global {
  interface HTMLElementTagNameMap {
    'my-table-collection-view': MyTableCollectionViewElement;
  }
}
```

### 9. Views Manifest (views/manifests.ts)
```typescript
import { MY_COLLECTION_ALIAS } from '../constants.js';
import { UMB_COLLECTION_ALIAS_CONDITION } from '@umbraco-cms/backoffice/collection';

export const manifests: Array<UmbExtensionManifest> = [
  {
    type: 'collectionView',
    alias: 'My.CollectionView.Table',
    name: 'My Table Collection View',
    element: () => import('./table/my-table-view.element.js'),
    weight: 200,
    meta: {
      label: 'Table',
      icon: 'icon-list',
      pathName: 'table',
    },
    conditions: [
      {
        alias: UMB_COLLECTION_ALIAS_CONDITION,
        match: MY_COLLECTION_ALIAS,
      },
    ],
  },
];
```

### 10. Collection Action (action/manifests.ts)
```typescript
import { MY_COLLECTION_ALIAS } from '../constants.js';
import { UMB_COLLECTION_ALIAS_CONDITION } from '@umbraco-cms/backoffice/collection';

export const manifests: Array<UmbExtensionManifest> = [
  {
    type: 'collectionAction',
    kind: 'button',
    alias: 'My.CollectionAction.Refresh',
    name: 'Refresh Collection Action',
    element: () => import('./refresh-action.element.js'),
    weight: 100,
    meta: {
      label: 'Refresh',
    },
    conditions: [
      {
        alias: UMB_COLLECTION_ALIAS_CONDITION,
        match: MY_COLLECTION_ALIAS,
      },
    ],
  },
];
```

### 11. Main Collection Manifest (manifests.ts)
```typescript
import { manifests as repositoryManifests } from './repository/manifests.js';
import { manifests as viewManifests } from './views/manifests.js';
import { manifests as actionManifests } from './action/manifests.js';
import { MY_COLLECTION_ALIAS, MY_COLLECTION_REPOSITORY_ALIAS } from './constants.js';

export const manifests: Array<UmbExtensionManifest> = [
  {
    type: 'collection',
    alias: MY_COLLECTION_ALIAS,
    name: 'My Collection',
    api: () => import('./my-collection.context.js'),
    element: () => import('./my-collection.element.js'),
    meta: {
      repositoryAlias: MY_COLLECTION_REPOSITORY_ALIAS,
    },
  },
  ...repositoryManifests,
  ...viewManifests,
  ...actionManifests,
];
```

## Rendering a Collection in a Dashboard

```typescript
import { html, customElement } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';

@customElement('my-dashboard')
export class MyDashboardElement extends UmbLitElement {
  override render() {
    return html`<umb-collection alias="My.Collection"></umb-collection>`;
  }
}
```

## Built-in Features

The collection system provides these features automatically:

| Feature | Description |
|---------|-------------|
| **Selection** | `UmbSelectionManager` on `context.selection` |
| **Pagination** | `UmbPaginationManager` on `context.pagination` |
| **Loading state** | Observable via `context.loading` |
| **Items** | Observable via `context.items` |
| **Total count** | Observable via `context.totalItems` |
| **Filtering** | Via `context.setFilter()` method |
| **View switching** | Multiple views with `UmbCollectionViewManager` |

## Key Condition

Use `UMB_COLLECTION_ALIAS_CONDITION` to target your collection:

```typescript
import { UMB_COLLECTION_ALIAS_CONDITION } from '@umbraco-cms/backoffice/collection';

conditions: [
  {
    alias: UMB_COLLECTION_ALIAS_CONDITION,
    match: 'My.Collection',
  },
],
```

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
