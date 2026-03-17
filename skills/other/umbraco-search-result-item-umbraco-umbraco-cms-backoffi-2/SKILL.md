---
name: umbraco-search-result-item
description: Implement search result items in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Search Result Item

## What is it?
A Search Result Item is a custom component that controls how individual search results are displayed in the backoffice search results. It allows you to customize the visual presentation of search results for specific entity types - showing additional information, custom icons, badges, or any other visual elements.

## Documentation
Always fetch the latest docs before implementing:

- **Extension Types**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Related Foundation Skills

- **Umbraco Element**: For implementing the result item element
  - Reference skill: `umbraco-umbraco-element`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What entity type? What additional info to display?
3. **Generate files** - Create manifest + element based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestSearchResultItem } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestSearchResultItem = {
  type: 'searchResultItem',
  alias: 'My.SearchResultItem',
  name: 'My Search Result Item',
  element: () => import('./my-search-result-item.element.js'),
  forEntityTypes: ['my-entity'],
};

export const manifests = [manifest];
```

### Element Implementation (my-search-result-item.element.ts)
```typescript
import { html, css, customElement, property } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import type { UmbSearchResultItemModel } from '@umbraco-cms/backoffice/search';

@customElement('my-search-result-item')
export class MySearchResultItemElement extends UmbLitElement {
  @property({ type: Object })
  item?: UmbSearchResultItemModel;

  render() {
    if (!this.item) return html``;

    return html`
      <a href=${this.item.href} class="result-item">
        <umb-icon name=${this.item.icon ?? 'icon-document'}></umb-icon>
        <div class="content">
          <span class="name">${this.item.name}</span>
          <span class="type">${this.item.entityType}</span>
        </div>
      </a>
    `;
  }

  static styles = css`
    .result-item {
      display: flex;
      align-items: center;
      gap: var(--uui-size-space-3);
      padding: var(--uui-size-space-3);
      text-decoration: none;
      color: inherit;
    }

    .result-item:hover {
      background: var(--uui-color-surface-alt);
    }

    .content {
      display: flex;
      flex-direction: column;
    }

    .name {
      font-weight: 500;
    }

    .type {
      font-size: var(--uui-type-small-size);
      color: var(--uui-color-text-alt);
    }
  `;
}

export default MySearchResultItemElement;

declare global {
  interface HTMLElementTagNameMap {
    'my-search-result-item': MySearchResultItemElement;
  }
}
```

### Result Item with Extended Data
```typescript
// If your search provider returns extended data
interface MySearchResultModel extends UmbSearchResultItemModel {
  description?: string;
  status?: string;
  updatedDate?: string;
}

@customElement('my-search-result-item')
export class MySearchResultItemElement extends UmbLitElement {
  @property({ type: Object })
  item?: MySearchResultModel;

  render() {
    if (!this.item) return html``;

    return html`
      <a href=${this.item.href} class="result-item">
        <umb-icon name=${this.item.icon ?? 'icon-document'}></umb-icon>
        <div class="content">
          <span class="name">${this.item.name}</span>
          ${this.item.description
            ? html`<span class="description">${this.item.description}</span>`
            : ''}
          <div class="meta">
            ${this.item.status
              ? html`<uui-tag>${this.item.status}</uui-tag>`
              : ''}
            ${this.item.updatedDate
              ? html`<span class="date">${this.item.updatedDate}</span>`
              : ''}
          </div>
        </div>
      </a>
    `;
  }
}
```

### Result Item for Multiple Entity Types
```typescript
const manifest: ManifestSearchResultItem = {
  type: 'searchResultItem',
  alias: 'My.SearchResultItem.Custom',
  name: 'Custom Search Result Item',
  element: () => import('./custom-result-item.element.js'),
  forEntityTypes: ['my-entity-a', 'my-entity-b', 'my-entity-c'],
};
```

### Picker Search Result Item
```typescript
// For customizing results in picker search (content pickers, media pickers, etc.)
import type { ManifestPickerSearchResultItem } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestPickerSearchResultItem = {
  type: 'pickerSearchResultItem',
  alias: 'My.PickerSearchResultItem',
  name: 'My Picker Search Result',
  element: () => import('./my-picker-result.element.js'),
  forEntityTypes: ['my-entity'],
};
```

## Item Model Properties

| Property | Description |
|----------|-------------|
| `entityType` | The entity type identifier |
| `unique` | Unique identifier for the item |
| `name` | Display name |
| `icon` | Icon name (optional) |
| `href` | URL to navigate when clicked |

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
