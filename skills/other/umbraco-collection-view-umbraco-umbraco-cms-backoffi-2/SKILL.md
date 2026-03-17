---
name: umbraco-collection-view
description: Implement collection views in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Collection View

## What is it?
A Collection View defines how data is displayed within a collection. It allows you to create custom visual representations of entity lists - such as tables, grids, cards, or any custom layout. Collection views can be added to existing collections or custom ones, and users can switch between available views.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/collections/collection-view
- **Collections**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/collections
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Related Foundation Skills

- **Context API**: For accessing collection context and items data
  - Reference skill: `umbraco-context-api`

- **State Management**: For subscribing to collection data changes
  - Reference skill: `umbraco-state-management`

- **Umbraco Element**: For implementing the view element
  - Reference skill: `umbraco-umbraco-element`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What collection? Table, grid, or custom layout? What columns/fields?
3. **Generate files** - Create manifest + view element based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestCollectionView } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestCollectionView = {
  type: 'collectionView',
  alias: 'My.CollectionView.Cards',
  name: 'Card View',
  element: () => import('./card-view.element.js'),
  meta: {
    label: 'Cards',
    icon: 'icon-grid',
    pathName: 'cards',
  },
  conditions: [
    {
      alias: 'Umb.Condition.CollectionAlias',
      match: 'My.Collection',
    },
  ],
};

export const manifests = [manifest];
```

### View Element (card-view.element.ts)
```typescript
import { html, css, customElement, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { UMB_COLLECTION_CONTEXT } from '@umbraco-cms/backoffice/collection';

@customElement('my-card-view')
export class MyCardViewElement extends UmbLitElement {
  @state()
  private _items: Array<any> = [];

  constructor() {
    super();

    this.consumeContext(UMB_COLLECTION_CONTEXT, (context) => {
      this.observe(context.items, (items) => {
        this._items = items;
      });
    });
  }

  render() {
    return html`
      <div class="card-grid">
        ${this._items.map(
          (item) => html`
            <div class="card">
              <h3>${item.name}</h3>
              <p>${item.description || 'No description'}</p>
            </div>
          `
        )}
      </div>
    `;
  }

  static styles = css`
    .card-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: var(--uui-size-space-4);
      padding: var(--uui-size-space-4);
    }

    .card {
      background: var(--uui-color-surface);
      border: 1px solid var(--uui-color-border);
      border-radius: var(--uui-border-radius);
      padding: var(--uui-size-space-4);
    }
  `;
}

export default MyCardViewElement;

declare global {
  interface HTMLElementTagNameMap {
    'my-card-view': MyCardViewElement;
  }
}
```

### Table View Example
```typescript
import { html, css, customElement, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { UMB_COLLECTION_CONTEXT } from '@umbraco-cms/backoffice/collection';

@customElement('my-table-view')
export class MyTableViewElement extends UmbLitElement {
  @state()
  private _items: Array<any> = [];

  constructor() {
    super();

    this.consumeContext(UMB_COLLECTION_CONTEXT, (context) => {
      this.observe(context.items, (items) => {
        this._items = items;
      });
    });
  }

  render() {
    return html`
      <uui-table>
        <uui-table-head>
          <uui-table-head-cell>Name</uui-table-head-cell>
          <uui-table-head-cell>Status</uui-table-head-cell>
          <uui-table-head-cell>Updated</uui-table-head-cell>
        </uui-table-head>
        ${this._items.map(
          (item) => html`
            <uui-table-row>
              <uui-table-cell>${item.name}</uui-table-cell>
              <uui-table-cell>${item.status}</uui-table-cell>
              <uui-table-cell>${item.updateDate}</uui-table-cell>
            </uui-table-row>
          `
        )}
      </uui-table>
    `;
  }
}

export default MyTableViewElement;
```

### View for Built-in Collection (e.g., Media)
```typescript
const manifest: ManifestCollectionView = {
  type: 'collectionView',
  alias: 'My.CollectionView.MediaThumbnails',
  name: 'Thumbnail View',
  element: () => import('./thumbnail-view.element.js'),
  weight: 100, // Higher weight = appears first in view switcher
  meta: {
    label: 'Thumbnails',
    icon: 'icon-picture',
    pathName: 'thumbnails',
  },
  conditions: [
    {
      alias: 'Umb.Condition.CollectionAlias',
      match: 'Umb.Collection.Media',
    },
  ],
};
```

### Accessing User-Defined Columns
```typescript
this.consumeContext(UMB_COLLECTION_CONTEXT, (context) => {
  // Get configured columns/properties
  this.observe(context.userDefinedProperties, (properties) => {
    this._columns = properties;
  });

  // Get items
  this.observe(context.items, (items) => {
    this._items = items;
  });
});
```

## Meta Properties

| Property | Description |
|----------|-------------|
| `label` | Display name in view switcher |
| `icon` | Icon in view switcher |
| `pathName` | URL path segment for deep linking |

## Common Collection Aliases for Conditions

- `Umb.Collection.Document`
- `Umb.Collection.Media`
- `Umb.Collection.Member`
- `Umb.Collection.User`

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
