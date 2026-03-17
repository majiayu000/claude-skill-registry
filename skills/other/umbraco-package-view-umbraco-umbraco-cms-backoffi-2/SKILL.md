---
name: umbraco-package-view
description: Implement package views in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Package View

## What is it?
Package Views provide custom UI panels for installed packages in Umbraco. They appear in the Packages section and allow package developers to create dedicated configuration or information pages for their packages. When a user clicks on an installed package, the package view is displayed as a modal or panel.

## Documentation
Always fetch the latest docs before implementing:

- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry
- **Umbraco Element**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/umbraco-element

## Related Foundation Skills

- **Umbraco Element**: Base class for creating UI components
  - Reference skill: `umbraco-umbraco-element`

- **Modals**: Package views are displayed in modal context
  - Reference skill: `umbraco-modals`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What package? What configuration options?
3. **Generate files** - Create manifest + element based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestPackageView } from '@umbraco-cms/backoffice/packages';

export const manifests: Array<ManifestPackageView> = [
  {
    type: 'packageView',
    alias: 'My.PackageView',
    name: 'My Package View',
    element: () => import('./my-package-view.element.js'),
    meta: {
      packageName: 'My Package',
    },
  },
];
```

### Element Implementation with Lit (my-package-view.element.ts)
```typescript
import { html, customElement } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { UmbModalBaseElement } from '@umbraco-cms/backoffice/modal';

@customElement('my-package-view')
export class MyPackageViewElement extends UmbModalBaseElement {
  override render() {
    return html`
      <umb-body-layout headline="My Package">
        <uui-box>
          <h2>Package Configuration</h2>
          <p>Configure your package settings here.</p>

          <uui-form>
            <uui-form-layout-item>
              <uui-label slot="label">Setting 1</uui-label>
              <uui-input></uui-input>
            </uui-form-layout-item>
          </uui-form>
        </uui-box>

        <div slot="actions">
          <uui-button @click=${this.#onClose} label="Close"></uui-button>
          <uui-button look="primary" @click=${this.#onSave} label="Save"></uui-button>
        </div>
      </umb-body-layout>
    `;
  }

  #onClose() {
    this.modalContext?.reject();
  }

  #onSave() {
    // Save logic here
    this.modalContext?.submit();
  }
}

export default MyPackageViewElement;
```

### Vanilla JS Element (my-package-view.js)
```javascript
const template = document.createElement('template');
template.innerHTML = `
  <umb-body-layout>
    <h1 slot="header">My Package</h1>

    <uui-box>
      <p>Package information and settings</p>
    </uui-box>

    <uui-action-bar slot="footer-info">
      <uui-button look="primary" type="button">Close</uui-button>
    </uui-action-bar>
  </umb-body-layout>
`;

export default class MyPackageViewElement extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.appendChild(template.content.cloneNode(true));

    this.shadowRoot.querySelector('uui-button').addEventListener('click', this.onClick.bind(this));
  }

  onClick() {
    this.modalContext.close();
  }
}

customElements.define('my-package-view', MyPackageViewElement);
```

## Interface Reference

```typescript
interface ManifestPackageView extends ManifestElement {
  type: 'packageView';
  meta: MetaPackageView;
}

interface MetaPackageView {
  packageName: string;  // Must match the package name in umbraco-package.json
}
```

## Package Integration

The package view is linked by matching `meta.packageName` with your package's name in `umbraco-package.json`:

```json
{
  "$schema": "../../umbraco-package-schema.json",
  "name": "My Package",
  "version": "1.0.0",
  "extensions": [
    {
      "type": "packageView",
      "alias": "My.PackageView",
      "name": "My Package View",
      "element": "/App_Plugins/MyPackage/my-package-view.js",
      "meta": {
        "packageName": "My Package"
      }
    }
  ]
}
```

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
