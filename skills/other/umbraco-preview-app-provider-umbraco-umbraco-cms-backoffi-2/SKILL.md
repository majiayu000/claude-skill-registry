---
name: umbraco-preview-app-provider
description: Implement preview app providers in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Preview App Provider

## What is it?
Preview App Providers add custom items to the preview window menu in Umbraco. When content editors preview their content, these apps appear in the preview menu allowing additional functionality like device simulation, accessibility checks, SEO analysis, or other preview-related tools.

## Documentation
Always fetch the latest docs before implementing:

- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry
- **Umbraco Element**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/umbraco-element

## Related Foundation Skills

- **Umbraco Element**: Base class for creating UI components
  - Reference skill: `umbraco-umbraco-element`

- **Context API**: When accessing preview state
  - Reference skill: `umbraco-context-api`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What preview functionality? What UI?
3. **Generate files** - Create manifest + element based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestPreviewAppProvider } from '@umbraco-cms/backoffice/extension-registry';

export const manifests: Array<ManifestPreviewAppProvider> = [
  {
    type: 'previewApp',
    alias: 'My.PreviewApp',
    name: 'My Preview App',
    element: () => import('./my-preview-app.element.js'),
  },
];
```

### Element Implementation (my-preview-app.element.ts)
```typescript
import { html, customElement, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';

@customElement('my-preview-app')
export class MyPreviewAppElement extends UmbLitElement {
  @state()
  private _isActive = false;

  override render() {
    return html`
      <uui-box headline="My Preview Tool">
        <p>Custom preview functionality</p>

        <uui-button
          look=${this._isActive ? 'primary' : 'default'}
          @click=${this.#toggle}
        >
          ${this._isActive ? 'Disable' : 'Enable'}
        </uui-button>
      </uui-box>
    `;
  }

  #toggle() {
    this._isActive = !this._isActive;
    // Apply your preview functionality
    this.#applyPreviewMode(this._isActive);
  }

  #applyPreviewMode(active: boolean) {
    // Access the preview iframe or apply styles
    const previewFrame = document.querySelector('iframe.preview-frame');
    if (previewFrame && active) {
      // Apply custom preview mode
    }
  }
}

export default MyPreviewAppElement;
```

### Device Simulator Example
```typescript
import { html, customElement, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';

@customElement('device-preview-app')
export class DevicePreviewAppElement extends UmbLitElement {
  @state()
  private _selectedDevice = 'desktop';

  private _devices = [
    { name: 'desktop', width: '100%', label: 'Desktop' },
    { name: 'tablet', width: '768px', label: 'Tablet' },
    { name: 'mobile', width: '375px', label: 'Mobile' },
  ];

  override render() {
    return html`
      <uui-box headline="Device Preview">
        ${this._devices.map(
          (device) => html`
            <uui-button
              look=${this._selectedDevice === device.name ? 'primary' : 'default'}
              @click=${() => this.#selectDevice(device)}
            >
              ${device.label}
            </uui-button>
          `
        )}
      </uui-box>
    `;
  }

  #selectDevice(device: { name: string; width: string }) {
    this._selectedDevice = device.name;
    // Dispatch event to resize preview
    this.dispatchEvent(
      new CustomEvent('preview-resize', {
        detail: { width: device.width },
        bubbles: true,
        composed: true,
      })
    );
  }
}

export default DevicePreviewAppElement;
```

## Interface Reference

```typescript
interface ManifestPreviewAppProvider extends ManifestElement {
  type: 'previewApp';
}
```

## Best Practices

- Keep the UI compact as it appears in a menu
- Provide clear enable/disable states
- Consider the preview context and available iframe
- Use appropriate icons for quick recognition

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
