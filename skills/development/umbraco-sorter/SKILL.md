---
name: umbraco-sorter
description: Implement drag-and-drop sorting with UmbSorterController in Umbraco backoffice
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Sorter

## What is it?

The UmbSorterController provides drag-and-drop sorting functionality for lists of items in the Umbraco backoffice. It handles reordering items within a container, moving items between containers, and supports nested sorting scenarios. This is useful for block editors, content trees, and any UI that requires user-driven ordering.

## Documentation

Always fetch the latest docs before implementing:

- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Reference Examples

The Umbraco source includes working examples:

**Nested Containers**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/sorter-with-nested-containers/`

This example demonstrates nested sorting with items that can contain child items.

**Two Containers**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/sorter-with-two-containers/`

This example shows moving items between two separate containers.

## Related Foundation Skills

- **State Management**: For reactive updates when order changes
  - Reference skill: `umbraco-state-management`

- **Umbraco Element**: For creating sortable item elements
  - Reference skill: `umbraco-umbraco-element`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - Single or multiple containers? Nested items? What data model?
3. **Generate files** - Create container element + item element + sorter setup
4. **Explain** - Show what was created and how sorting works

---

## Basic Sorter Setup

```typescript
import { UmbSorterController } from '@umbraco-cms/backoffice/sorter';
import { html, customElement, property, repeat } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';

interface MyItem {
  id: string;
  name: string;
}

@customElement('my-sortable-list')
export class MySortableListElement extends UmbLitElement {
  #sorter = new UmbSorterController<MyItem, HTMLElement>(this, {
    // Get unique identifier from DOM element
    getUniqueOfElement: (element) => {
      return element.getAttribute('data-id') ?? '';
    },
    // Get unique identifier from data model
    getUniqueOfModel: (modelEntry) => {
      return modelEntry.id;
    },
    // Identifier shared by all connected sorters (for cross-container dragging)
    identifier: 'my-sortable-list',
    // CSS selector for sortable items
    itemSelector: '.sortable-item',
    // CSS selector for the container
    containerSelector: '.sortable-container',
    // Called when order changes
    onChange: ({ model }) => {
      this._items = model;
      this.requestUpdate();
      this.dispatchEvent(new CustomEvent('change', { detail: { items: model } }));
    },
  });

  @property({ type: Array, attribute: false })
  public get items(): MyItem[] {
    return this._items;
  }
  public set items(value: MyItem[]) {
    this._items = value;
    this.#sorter.setModel(value);
    this.requestUpdate();
  }
  private _items: MyItem[] = [];

  override render() {
    return html`
      <div class="sortable-container">
        ${repeat(
          this._items,
          (item) => item.id,
          (item) => html`
            <div class="sortable-item" data-id=${item.id}>
              ${item.name}
            </div>
          `
        )}
      </div>
    `;
  }
}
```

---

## Nested Sorter (Items with Children)

```typescript
import { UmbSorterController } from '@umbraco-cms/backoffice/sorter';
import { html, customElement, property, repeat, css } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';

export interface NestedItem {
  name: string;
  children?: NestedItem[];
}

@customElement('my-sorter-group')
export class MySorterGroupElement extends UmbLitElement {
  #sorter = new UmbSorterController<NestedItem, MySorterItemElement>(this, {
    getUniqueOfElement: (element) => element.name,
    getUniqueOfModel: (modelEntry) => modelEntry.name,
    // IMPORTANT: Same identifier allows items to move between all nested groups
    identifier: 'my-nested-sorter',
    itemSelector: 'my-sorter-item',
    containerSelector: '.sorter-container',
    onChange: ({ model }) => {
      const oldValue = this._value;
      this._value = model;
      this.requestUpdate('value', oldValue);
      this.dispatchEvent(new CustomEvent('change'));
    },
  });

  @property({ type: Array, attribute: false })
  public get value(): NestedItem[] {
    return this._value ?? [];
  }
  public set value(value: NestedItem[]) {
    this._value = value;
    this.#sorter.setModel(value);
    this.requestUpdate();
  }
  private _value?: NestedItem[];

  override render() {
    return html`
      <div class="sorter-container">
        ${repeat(
          this.value,
          (item) => item.name,
          (item) => html`
            <my-sorter-item .name=${item.name}>
              <!-- Recursive nesting -->
              <my-sorter-group
                .value=${item.children ?? []}
                @change=${(e: Event) => {
                  item.children = (e.target as MySorterGroupElement).value;
                }}
              ></my-sorter-group>
            </my-sorter-item>
          `
        )}
      </div>
    `;
  }

  static override styles = css`
    :host {
      display: block;
      min-height: 20px;
      border: 1px dashed rgba(122, 122, 122, 0.25);
      border-radius: var(--uui-border-radius);
      padding: var(--uui-size-space-1);
    }
  `;
}
```

---

## Sortable Item Element

```typescript
import { html, customElement, property, css } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';

@customElement('my-sorter-item')
export class MySorterItemElement extends UmbLitElement {
  @property({ type: String })
  name = '';

  override render() {
    return html`
      <div class="item-wrapper">
        <div class="drag-handle">
          <uui-icon name="icon-navigation"></uui-icon>
        </div>
        <div class="item-content">
          <span>${this.name}</span>
          <slot name="action"></slot>
        </div>
        <div class="children">
          <slot></slot>
        </div>
      </div>
    `;
  }

  static override styles = css`
    :host {
      display: block;
      background: var(--uui-color-surface);
      border: 1px solid var(--uui-color-border);
      border-radius: var(--uui-border-radius);
      margin: var(--uui-size-space-1) 0;
    }

    .item-wrapper {
      padding: var(--uui-size-space-3);
    }

    .drag-handle {
      cursor: grab;
      display: inline-block;
      margin-right: var(--uui-size-space-2);
    }

    .drag-handle:active {
      cursor: grabbing;
    }

    .children {
      margin-left: var(--uui-size-space-5);
      margin-top: var(--uui-size-space-2);
    }
  `;
}

declare global {
  interface HTMLElementTagNameMap {
    'my-sorter-item': MySorterItemElement;
  }
}
```

---

## Two Containers (Cross-Container Sorting)

```typescript
@customElement('my-dual-sorter-dashboard')
export class MyDualSorterDashboard extends UmbLitElement {
  listOneItems: MyItem[] = [
    { id: '1', name: 'Apple' },
    { id: '2', name: 'Banana' },
  ];

  listTwoItems: MyItem[] = [
    { id: '3', name: 'Carrot' },
    { id: '4', name: 'Date' },
  ];

  override render() {
    return html`
      <div class="container">
        <my-sortable-list
          .items=${this.listOneItems}
          @change=${(e: CustomEvent) => {
            this.listOneItems = e.detail.items;
          }}
        ></my-sortable-list>

        <my-sortable-list
          .items=${this.listTwoItems}
          @change=${(e: CustomEvent) => {
            this.listTwoItems = e.detail.items;
          }}
        ></my-sortable-list>
      </div>
    `;
  }
}
```

**Key**: Both lists use the same `identifier` in their UmbSorterController to enable dragging between them.

---

## UmbSorterController Options

| Option | Type | Description |
|--------|------|-------------|
| `identifier` | `string` | Shared ID for connected sorters (enables cross-container dragging) |
| `itemSelector` | `string` | CSS selector for sortable items |
| `containerSelector` | `string` | CSS selector for the container |
| `getUniqueOfElement` | `(element) => string` | Extract unique ID from DOM element |
| `getUniqueOfModel` | `(model) => string` | Extract unique ID from data model |
| `onChange` | `({ model }) => void` | Called when order changes |
| `onStart` | `() => void` | Called when dragging starts |
| `onEnd` | `() => void` | Called when dragging ends |

---

## Key Methods

```typescript
// Set the model (call when items change externally)
this.#sorter.setModel(items);

// Get current model
const currentItems = this.#sorter.getModel();

// Disable sorting temporarily
this.#sorter.disable();

// Re-enable sorting
this.#sorter.enable();
```

---

## CSS Classes Applied During Drag

| Class | Applied To | When |
|-------|------------|------|
| `.umb-sorter-dragging` | Container | While any item is being dragged |
| `.umb-sorter-placeholder` | Placeholder element | Indicates drop position |

---

## Best Practices

1. **Use unique identifiers** - Each item must have a unique ID
2. **Match selectors carefully** - `itemSelector` and `containerSelector` must match your DOM
3. **Share identifier** - Use same `identifier` for connected sorters
4. **Handle nested updates** - Propagate changes up through nested structures
5. **Use repeat directive** - Always use `repeat()` with a key function for proper DOM diffing
6. **Provide visual feedback** - Style drag handles and drop zones clearly

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
