---
name: umbraco-block-editor-custom-view
description: Implement block editor custom views in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Block Editor Custom View

## What is it?
A Block Editor Custom View provides a custom visual representation for blocks in Block List, Block Grid, or Block RTE editors. Instead of the default block rendering, you can create a custom Web Component that displays block content in a specialized way - useful for themed previews, domain-specific visualizations, or enhanced editing experiences.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/block-custom-view
- **Block Editor**: https://docs.umbraco.com/umbraco-cms/fundamentals/backoffice/property-editors/built-in-umbraco-property-editors/block-editor
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Related Foundation Skills

- **Umbraco Element**: For implementing the custom view element
  - Reference skill: `umbraco-umbraco-element`

## Reference Example

The Umbraco source includes a working example:

**Location**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/block-custom-view/`

This example demonstrates a custom block view implementation. Study this for production patterns.

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - Which block types? Which editors (list, grid, RTE)?
3. **Generate files** - Create manifest + view element based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (umbraco-package.json)
```json
{
  "name": "My Block Views",
  "extensions": [
    {
      "type": "blockEditorCustomView",
      "alias": "My.BlockView.Hero",
      "name": "Hero Block View",
      "element": "/App_Plugins/MyBlocks/hero-view.js",
      "forContentTypeAlias": "heroBlock",
      "forBlockEditor": "block-list"
    }
  ]
}
```

### Manifest (TypeScript)
```typescript
import type { ManifestBlockEditorCustomView } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestBlockEditorCustomView = {
  type: 'blockEditorCustomView',
  alias: 'My.BlockView.Hero',
  name: 'Hero Block View',
  element: () => import('./hero-block-view.element.js'),
  forContentTypeAlias: 'heroBlock',
  forBlockEditor: ['block-list', 'block-grid'],
};

export const manifests = [manifest];
```

### Custom View Element (hero-block-view.element.ts)
```typescript
import { html, css, customElement, property } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import type { UmbBlockEditorCustomViewElement, UmbBlockDataType } from '@umbraco-cms/backoffice/block';

@customElement('my-hero-block-view')
export class MyHeroBlockViewElement extends UmbLitElement implements UmbBlockEditorCustomViewElement {
  @property({ attribute: false })
  content?: UmbBlockDataType;

  @property({ attribute: false })
  settings?: UmbBlockDataType;

  render() {
    return html`
      <div class="hero-preview">
        <h2>${this.content?.headline ?? 'No headline'}</h2>
        <p>${this.content?.subheadline ?? ''}</p>
        ${this.content?.backgroundImage
          ? html`<div class="bg-indicator">Has background image</div>`
          : ''}
      </div>
    `;
  }

  static styles = css`
    :host {
      display: block;
    }

    .hero-preview {
      padding: var(--uui-size-space-4);
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border-radius: var(--uui-border-radius);
      min-height: 100px;
    }

    h2 {
      margin: 0 0 var(--uui-size-space-2);
      font-size: 1.2em;
    }

    p {
      margin: 0;
      opacity: 0.8;
    }

    .bg-indicator {
      margin-top: var(--uui-size-space-2);
      font-size: 0.8em;
      opacity: 0.6;
    }
  `;
}

export default MyHeroBlockViewElement;

declare global {
  interface HTMLElementTagNameMap {
    'my-hero-block-view': MyHeroBlockViewElement;
  }
}
```

### View for Multiple Content Types
```typescript
const manifest: ManifestBlockEditorCustomView = {
  type: 'blockEditorCustomView',
  alias: 'My.BlockView.Cards',
  name: 'Card Blocks View',
  element: () => import('./card-block-view.element.js'),
  forContentTypeAlias: ['cardBlock', 'featureCard', 'testimonialCard'],
  forBlockEditor: 'block-grid',
};
```

### View for All Blocks in an Editor
```typescript
// Omit forContentTypeAlias to apply to all blocks
const manifest: ManifestBlockEditorCustomView = {
  type: 'blockEditorCustomView',
  alias: 'My.BlockView.Universal',
  name: 'Universal Block View',
  element: () => import('./universal-view.element.js'),
  forBlockEditor: 'block-list', // Only specify editor type
};
```

### Accessing Settings Data
```typescript
@customElement('my-styled-block-view')
export class MyStyledBlockViewElement extends UmbLitElement implements UmbBlockEditorCustomViewElement {
  @property({ attribute: false })
  content?: UmbBlockDataType;

  @property({ attribute: false })
  settings?: UmbBlockDataType;

  render() {
    // Settings contain block configuration (colors, layout options, etc.)
    const bgColor = this.settings?.backgroundColor ?? '#ffffff';
    const padding = this.settings?.padding ?? 'medium';

    return html`
      <div style="background-color: ${bgColor}" class="padding-${padding}">
        <h3>${this.content?.title}</h3>
        <div>${this.content?.text}</div>
      </div>
    `;
  }
}
```

## Manifest Properties

| Property | Description |
|----------|-------------|
| `forContentTypeAlias` | Content type alias(es) this view applies to |
| `forBlockEditor` | Editor type(s): `block-list`, `block-grid`, `block-rte` |

## Element Properties

| Property | Type | Description |
|----------|------|-------------|
| `content` | `UmbBlockDataType` | The block's content data |
| `settings` | `UmbBlockDataType` | The block's settings data |

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
