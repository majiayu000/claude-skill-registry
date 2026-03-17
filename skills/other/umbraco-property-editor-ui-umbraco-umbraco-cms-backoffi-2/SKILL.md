---
name: umbraco-property-editor-ui
description: Implement property editor UIs in Umbraco backoffice using official docs
version: 1.2.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Property Editor UI

## What is it?
A Property Editor UI is the visual component that users interact with in the Umbraco backoffice to input and manage content data. It's one half of a property editor - the UI (client-side TypeScript) pairs with a Schema (server-side C#) that defines data storage.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/property-editors
- **Tutorial**: https://docs.umbraco.com/umbraco-cms/tutorials/creating-a-property-editor
- **Configuration**: https://docs.umbraco.com/umbraco-cms/tutorials/creating-a-property-editor/adding-configuration-to-a-property-editor
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Reference Example

The Umbraco source includes a working example:

**Location**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/property-editor/`

This example demonstrates a complete property editor UI implementation with configuration. Study this for production patterns.

## Related Foundation Skills

- **Umbraco Element**: When implementing the UI element with UmbElementMixin
  - Reference skill: `umbraco-umbraco-element`

- **State Management**: When implementing reactive value updates
  - Reference skill: `umbraco-state-management`

- **Localization**: When adding multi-language support to labels
  - Reference skill: `umbraco-localization`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What data type? What UI components needed? Configuration options?
3. **Generate files** - Create manifest + element based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (umbraco-package.json)

> **WARNING:** The `propertyEditorSchemaAlias` below uses `Umbraco.Plain.String`, a built-in schema.
> If you use a custom alias like `MyPackage.CustomSchema`, you MUST have a corresponding C# `DataEditor` on the server or you'll get a **404 error** when creating a Data Type.

```json
{
  "name": "My Property Editor",
  "extensions": [
    {
      "type": "propertyEditorUi",
      "alias": "My.PropertyEditorUi.Custom",
      "name": "My Custom Editor",
      "element": "/App_Plugins/MyEditor/editor.js",
      "elementName": "my-editor-ui",
      "meta": {
        "label": "My Custom Editor",
        "icon": "icon-edit",
        "group": "common",
        "propertyEditorSchemaAlias": "Umbraco.Plain.String"
      }
    }
  ]
}
```

### Element Implementation (editor.ts)
```typescript
import { LitElement, html, css, customElement, property } from '@umbraco-cms/backoffice/external/lit';
import { UmbElementMixin } from '@umbraco-cms/backoffice/element-api';
import { UmbChangeEvent } from '@umbraco-cms/backoffice/event';
import type { UmbPropertyEditorUiElement } from '@umbraco-cms/backoffice/property-editor';

@customElement('my-editor-ui')
export default class MyEditorElement extends UmbElementMixin(LitElement) implements UmbPropertyEditorUiElement {
  @property({ type: String })
  public value = '';

  #onChange(e: Event) {
    const input = e.target as HTMLInputElement;
    this.value = input.value;
    this.dispatchEvent(new UmbChangeEvent());
  }

  render() {
    return html`
      <uui-input
        .value=${this.value || ''}
        @change=${this.#onChange}
      ></uui-input>
    `;
  }

  static styles = css`
    :host {
      display: block;
    }
  `;
}

declare global {
  interface HTMLElementTagNameMap {
    'my-editor-ui': MyEditorElement;
  }
}
```

### With Configuration
```typescript
import type { UmbPropertyEditorConfigCollection } from '@umbraco-cms/backoffice/property-editor';

@customElement('my-editor-ui')
export default class MyEditorElement extends UmbElementMixin(LitElement) implements UmbPropertyEditorUiElement {
  @property({ type: String })
  public value = '';

  @state()
  private _maxChars?: number;

  @state()
  private _placeholder?: string;

  @property({ attribute: false })
  public set config(config: UmbPropertyEditorConfigCollection) {
    this._maxChars = config.getValueByAlias('maxChars');
    this._placeholder = config.getValueByAlias('placeholder');
  }

  render() {
    return html`
      <uui-input
        .value=${this.value || ''}
        .placeholder=${this._placeholder || ''}
        .maxlength=${this._maxChars}
        @change=${this.#onChange}
      ></uui-input>
    `;
  }
}
```

### Configuration in Manifest
```json
{
  "type": "propertyEditorUi",
  "alias": "My.PropertyEditorUi.Custom",
  "name": "My Custom Editor",
  "element": "/App_Plugins/MyEditor/editor.js",
  "elementName": "my-editor-ui",
  "meta": {
    "label": "My Custom Editor",
    "propertyEditorSchemaAlias": "Umbraco.Plain.String",
    "settings": {
      "properties": [
        {
          "alias": "maxChars",
          "label": "Maximum Characters",
          "propertyEditorUiAlias": "Umb.PropertyEditorUi.Integer"
        },
        {
          "alias": "placeholder",
          "label": "Placeholder Text",
          "propertyEditorUiAlias": "Umb.PropertyEditorUi.TextBox"
        }
      ],
      "defaultData": [
        { "alias": "maxChars", "value": 100 }
      ]
    }
  }
}
```

## Built-in Schema Aliases (Safe Defaults)

The `propertyEditorSchemaAlias` in your manifest must reference a schema that exists **on the server**:

| Part | Location | Language |
|------|----------|----------|
| Property Editor UI | Client | TypeScript |
| Property Editor Schema | Server | C# |

- **Built-in schemas** (listed below) are always available - use these for simple storage needs
- **Custom schemas** require a C# `DataEditor` class - only needed for custom validation/conversion

These built-in schemas are always available:

| Schema Alias | Stores | Use Case |
|--------------|--------|----------|
| `Umbraco.Plain.String` | `string` | Simple text values |
| `Umbraco.Integer` | `int` | Numbers, ratings, counts |
| `Umbraco.Decimal` | `decimal` | Prices, percentages |
| `Umbraco.Plain.Json` | `object` | Complex JSON data |
| `Umbraco.DateTime` | `DateTime` | Dates and times |
| `Umbraco.TrueFalse` | `bool` | Toggles, checkboxes |
| `Umbraco.TextBox` | `string` | Textbox with validation |
| `Umbraco.TextArea` | `string` | Multi-line text |

## Troubleshooting

See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for common issues including:
- 404 errors when creating Data Types
- Values not persisting with `Umbraco.Plain.Json`

See [UUI-GOTCHAS.md](./UUI-GOTCHAS.md) for UUI component issues (combobox, input, etc.).

---

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
