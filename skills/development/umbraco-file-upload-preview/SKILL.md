---
name: umbraco-file-upload-preview
description: Implement file upload preview components in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco File Upload Preview

## What is it?
File Upload Previews are custom web components that render previews for specific file types during upload in Umbraco. They allow you to create visual representations for files based on their MIME types, such as displaying thumbnails for images, waveforms for audio, or custom icons for specific file formats.

## Documentation
Always fetch the latest docs before implementing:

- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry
- **Umbraco Element**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/umbraco-element

## Related Foundation Skills

- **Umbraco Element**: Base class for creating UI components
  - Reference skill: `umbraco-umbraco-element`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What MIME types? What preview display?
3. **Generate files** - Create manifest + element based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
export const manifests: Array<UmbExtensionManifest> = [
  {
    type: 'fileUploadPreview',
    alias: 'My.FileUploadPreview.Custom',
    name: 'Custom File Upload Preview',
    weight: 100,
    element: () => import('./my-file-preview.element.js'),
    forMimeTypes: ['application/pdf', 'application/x-pdf'],
  },
];
```

### Element Implementation (my-file-preview.element.ts)
```typescript
import { html, customElement, property, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import type { UmbFileUploadPreviewElement } from '@umbraco-cms/backoffice/media';

@customElement('my-file-preview')
export class MyFilePreviewElement extends UmbLitElement implements UmbFileUploadPreviewElement {
  @property({ type: Object })
  file?: File;

  @state()
  private _previewUrl?: string;

  override updated(changedProperties: Map<string, unknown>) {
    if (changedProperties.has('file') && this.file) {
      this._previewUrl = URL.createObjectURL(this.file);
    }
  }

  override disconnectedCallback() {
    super.disconnectedCallback();
    if (this._previewUrl) {
      URL.revokeObjectURL(this._previewUrl);
    }
  }

  override render() {
    if (!this.file) return html``;

    return html`
      <div class="preview-container">
        <uui-icon name="icon-document"></uui-icon>
        <span>${this.file.name}</span>
      </div>
    `;
  }
}

export default MyFilePreviewElement;
```

## Interface Reference

```typescript
interface ManifestFileUploadPreview extends ManifestElement<UmbFileUploadPreviewElement> {
  type: 'fileUploadPreview';
  forMimeTypes: string | Array<string>; // e.g., 'image/*', ['image/png', 'image/jpeg']
}

interface UmbFileUploadPreviewElement {
  file?: File;
}
```

## Common MIME Type Patterns

- `image/*` - All image types
- `video/*` - All video types
- `audio/*` - All audio types
- `application/pdf` - PDF files
- `*/*` - Fallback for all types (use with lower weight)

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
