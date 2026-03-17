---
name: umbraco-tiptap-extension
description: Implement Tiptap extensions for Umbraco rich text editor using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Tiptap Extension

## What is it?
A Tiptap Extension adds functionality to Umbraco's Rich Text Editor (which is built on Tiptap). Extensions can add new node types (like custom blocks), marks (like custom formatting), or other editor capabilities. The extension API provides the underlying Tiptap extensions that get registered with the editor.

## Documentation
Always fetch the latest docs before implementing:

- **Extension Types**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types
- **Rich Text Editor**: https://docs.umbraco.com/umbraco-cms/fundamentals/backoffice/property-editors/built-in-umbraco-property-editors/rich-text-editor
- **Tiptap Docs**: https://tiptap.dev/docs/editor/extensions/overview
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Related Skills

- **Tiptap Toolbar Extension**: For adding toolbar buttons
  - Reference skill: `umbraco-tiptap-toolbar-extension`

- **Tiptap Statusbar Extension**: For adding statusbar elements
  - Reference skill: `umbraco-tiptap-statusbar-extension`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What functionality? Node, Mark, or Extension? Custom styles needed?
3. **Generate files** - Create manifest + API class based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestTiptapExtension } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestTiptapExtension = {
  type: 'tiptapExtension',
  alias: 'My.TiptapExtension.Highlight',
  name: 'Highlight Extension',
  api: () => import('./highlight.tiptap-api.js'),
  meta: {
    icon: 'icon-marker',
    label: 'Highlight',
    group: 'formatting',
  },
};

export const manifests = [manifest];
```

### Extension API (highlight.tiptap-api.ts)
```typescript
import { UmbTiptapExtensionApiBase } from '@umbraco-cms/backoffice/tiptap';
import type { UmbTiptapExtensionArgs } from '@umbraco-cms/backoffice/tiptap';
import Highlight from '@tiptap/extension-highlight';

export default class HighlightTiptapExtensionApi extends UmbTiptapExtensionApiBase {
  getTiptapExtensions(args?: UmbTiptapExtensionArgs) {
    return [
      Highlight.configure({
        multicolor: true,
      }),
    ];
  }
}
```

### Custom Node Extension
```typescript
import { UmbTiptapExtensionApiBase } from '@umbraco-cms/backoffice/tiptap';
import { Node } from '@tiptap/core';

export default class CalloutTiptapExtensionApi extends UmbTiptapExtensionApiBase {
  getTiptapExtensions() {
    const CalloutNode = Node.create({
      name: 'callout',
      group: 'block',
      content: 'block+',

      addAttributes() {
        return {
          type: {
            default: 'info',
          },
        };
      },

      parseHTML() {
        return [{ tag: 'div[data-callout]' }];
      },

      renderHTML({ HTMLAttributes }) {
        return ['div', { 'data-callout': '', ...HTMLAttributes }, 0];
      },
    });

    return [CalloutNode];
  }
}
```

### Custom Mark Extension
```typescript
import { UmbTiptapExtensionApiBase } from '@umbraco-cms/backoffice/tiptap';
import { Mark } from '@tiptap/core';

export default class CustomMarkTiptapExtensionApi extends UmbTiptapExtensionApiBase {
  getTiptapExtensions() {
    const CustomMark = Mark.create({
      name: 'customHighlight',

      addAttributes() {
        return {
          color: {
            default: 'yellow',
          },
        };
      },

      parseHTML() {
        return [{ tag: 'mark' }];
      },

      renderHTML({ HTMLAttributes }) {
        return ['mark', { style: `background-color: ${HTMLAttributes.color}` }, 0];
      },
    });

    return [CustomMark];
  }
}
```

### Extension with Custom Styles
```typescript
import { UmbTiptapExtensionApiBase } from '@umbraco-cms/backoffice/tiptap';
import { css } from '@umbraco-cms/backoffice/external/lit';
import Highlight from '@tiptap/extension-highlight';

export default class StyledHighlightApi extends UmbTiptapExtensionApiBase {
  getTiptapExtensions() {
    return [Highlight];
  }

  // Custom styles for the editor
  getStyles() {
    return css`
      mark {
        background-color: yellow;
        padding: 0.1em 0.2em;
        border-radius: 2px;
      }
    `;
  }
}
```

### Using Configuration from Property Editor
```typescript
import { UmbTiptapExtensionApiBase } from '@umbraco-cms/backoffice/tiptap';
import type { UmbTiptapExtensionArgs } from '@umbraco-cms/backoffice/tiptap';
import Highlight from '@tiptap/extension-highlight';

export default class ConfigurableHighlightApi extends UmbTiptapExtensionApiBase {
  getTiptapExtensions(args?: UmbTiptapExtensionArgs) {
    // Access data type configuration
    const multicolor = args?.configuration?.getValueByAlias('multicolor') ?? false;

    return [
      Highlight.configure({
        multicolor,
      }),
    ];
  }
}
```

## Meta Properties

| Property | Description |
|----------|-------------|
| `icon` | Icon shown in configuration UI |
| `label` | Display name |
| `group` | Group for organizing extensions |
| `description` | Optional description |

## Common Extension Groups

- `formatting` - Text formatting (bold, italic, etc.)
- `structure` - Structural elements (headings, lists, etc.)
- `media` - Media elements (images, embeds, etc.)
- `misc` - Other functionality

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
