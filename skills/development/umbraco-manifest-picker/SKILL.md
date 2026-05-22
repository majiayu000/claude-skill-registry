---
name: umbraco-manifest-picker
description: Use umb-input-manifest to pick registered extensions in Umbraco backoffice
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Manifest Picker

## What is it?

The `<umb-input-manifest>` component provides a picker UI for selecting registered extensions from the Umbraco extension registry. It allows users to pick from any extension type (workspaces, dashboards, property editors, etc.) and returns the selected manifest. This is useful for configuration UIs where users need to reference other extensions.

## Documentation

Always fetch the latest docs before implementing:

- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Reference Example

The Umbraco source includes a working example:

**Location**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/manifest-picker/`

This example demonstrates a dashboard that lets users browse and select extensions by type.

## Related Foundation Skills

- **Extension Registry**: For understanding how extensions are registered
  - Reference skill: `umbraco-extension-registry`

- **Umbraco Element**: For creating picker UIs
  - Reference skill: `umbraco-umbraco-element`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What extension types to pick? How to use selection?
3. **Generate files** - Create element with manifest picker
4. **Explain** - Show what was created and how selection works

---

## Basic Usage

```typescript
import { html, customElement, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import type { UmbInputManifestElement } from '@umbraco-cms/backoffice/components';

@customElement('my-manifest-picker-example')
export class MyManifestPickerExampleElement extends UmbLitElement {
  @state()
  private _selectedManifest = '';

  #onChange(event: { target: UmbInputManifestElement }) {
    const selectedManifest = event.target.value;
    this._selectedManifest = selectedManifest?.value ?? '';
  }

  override render() {
    return html`
      <uui-box>
        <umb-property-layout label="Select a workspace">
          <div slot="editor">
            <umb-input-manifest
              .extensionType=${'workspace'}
              @change=${this.#onChange}
            ></umb-input-manifest>
          </div>
        </umb-property-layout>

        ${this._selectedManifest
          ? html`<p>Selected: <code>${this._selectedManifest}</code></p>`
          : ''}
      </uui-box>
    `;
  }
}
```

---

## Dynamic Extension Type Selection

```typescript
import { html, customElement, state, when, nothing } from '@umbraco-cms/backoffice/external/lit';
import { umbExtensionsRegistry } from '@umbraco-cms/backoffice/extension-registry';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import type { UmbInputManifestElement } from '@umbraco-cms/backoffice/components';
import type { UUISelectEvent } from '@umbraco-cms/backoffice/external/uui';

interface Option {
  name: string;
  value: string;
  selected: boolean;
}

@customElement('my-extension-browser')
export class MyExtensionBrowserElement extends UmbLitElement {
  #options: Option[] = [];

  @state()
  private _selectedExtensionType = 'dashboard';

  @state()
  private _selectedManifest = '';

  constructor() {
    super();

    // Build list of available extension types from registry
    this.observe(umbExtensionsRegistry.extensions, (extensions) => {
      const types = [...new Set(extensions.map((x) => x.type))];
      this.#options = types.sort().map((x) => ({
        name: x,
        value: x,
        selected: x === this._selectedExtensionType,
      }));
    });
  }

  #onTypeSelect(event: UUISelectEvent) {
    this._selectedManifest = '';
    this._selectedExtensionType = event.target.value as string;
  }

  #onManifestChange(event: { target: UmbInputManifestElement }) {
    const selectedManifest = event.target.value;
    this._selectedManifest = selectedManifest?.value ?? '';
  }

  override render() {
    return html`
      <uui-box>
        <umb-property-layout label="Extension Type">
          <uui-select
            slot="editor"
            label="Select type"
            placeholder="Select type..."
            .options=${this.#options}
            @change=${this.#onTypeSelect}
          ></uui-select>
        </umb-property-layout>

        ${when(
          this._selectedExtensionType,
          () => html`
            <umb-property-layout
              label="Select Extension"
              description="Pick a ${this._selectedExtensionType}"
            >
              <div slot="editor">
                <umb-input-manifest
                  .extensionType=${this._selectedExtensionType}
                  @change=${this.#onManifestChange}
                ></umb-input-manifest>
              </div>
            </umb-property-layout>
          `,
          () => nothing
        )}

        ${when(
          this._selectedManifest,
          () => html`
            <umb-property-layout label="Selected Manifest">
              <div slot="editor">
                <code>${this._selectedManifest}</code>
              </div>
            </umb-property-layout>
          `,
          () => nothing
        )}
      </uui-box>
    `;
  }
}
```

---

## Getting All Extension Types

```typescript
import { umbExtensionsRegistry } from '@umbraco-cms/backoffice/extension-registry';

// In your element constructor
this.observe(umbExtensionsRegistry.extensions, (extensions) => {
  // Get unique extension types
  const types = [...new Set(extensions.map((x) => x.type))];
  console.log('Available types:', types);

  // Filter by type
  const dashboards = extensions.filter((x) => x.type === 'dashboard');
  console.log('Dashboards:', dashboards);

  // Get extension by alias
  const specific = extensions.find((x) => x.alias === 'Umb.Dashboard.Welcome');
  console.log('Specific extension:', specific);
});
```

---

## Common Extension Types

| Type | Description |
|------|-------------|
| `dashboard` | Section dashboards |
| `workspace` | Entity workspaces |
| `workspaceView` | Views within workspaces |
| `workspaceAction` | Workspace action buttons |
| `propertyEditorUi` | Property editor UIs |
| `propertyEditorSchema` | Property editor schemas |
| `entityAction` | Context menu actions |
| `tree` | Navigation trees |
| `treeItem` | Tree item renderers |
| `section` | Backoffice sections |
| `sectionView` | Section views |
| `headerApp` | Header bar apps |
| `modal` | Modal dialogs |
| `condition` | Extension conditions |

---

## UmbInputManifest Properties

| Property | Type | Description |
|----------|------|-------------|
| `extensionType` | `string` | The type of extension to pick from |
| `value` | `ManifestBase \| undefined` | The selected manifest |

---

## Events

| Event | Detail | Description |
|-------|--------|-------------|
| `change` | `{ target: UmbInputManifestElement }` | Fired when selection changes |

---

## Accessing Selected Manifest Data

```typescript
#onManifestChange(event: { target: UmbInputManifestElement }) {
  const manifest = event.target.value;

  if (manifest) {
    console.log('Alias:', manifest.alias);
    console.log('Name:', manifest.name);
    console.log('Type:', manifest.type);
    console.log('Full manifest:', manifest);
  }
}
```

---

## Use Cases

1. **Configuration screens** - Let users select which dashboard/workspace to show
2. **Extension management** - Browse and inspect registered extensions
3. **Dynamic routing** - Configure navigation targets
4. **Condition configuration** - Select conditions to apply
5. **Package development** - Test extension registration

---

## Best Practices

1. **Clear selection** - Reset `_selectedManifest` when type changes
2. **Handle undefined** - Check if `value` exists before accessing properties
3. **Use property layout** - Wrap in `<umb-property-layout>` for consistent styling
4. **Show feedback** - Display selected manifest alias/name to confirm selection
5. **Sort types** - Sort extension type options alphabetically for usability

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
