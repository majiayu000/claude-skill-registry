---
name: umbraco-tiptap-toolbar-extension
description: Implement Tiptap toolbar extensions for Umbraco rich text editor using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Tiptap Toolbar Extension

## What is it?
A Tiptap Toolbar Extension adds buttons or controls to the Rich Text Editor's toolbar. It provides an `execute` method that runs when clicked, and can indicate active/disabled states. Several "kinds" are available: `button` (simple toggle), `colorPickerButton` (color selection), `menu` (dropdown menu), and `styleMenu` (style selection dropdown).

## Documentation
Always fetch the latest docs before implementing:

- **Extension Types**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types
- **Rich Text Editor**: https://docs.umbraco.com/umbraco-cms/fundamentals/backoffice/property-editors/built-in-umbraco-property-editors/rich-text-editor
- **Tiptap Docs**: https://tiptap.dev/docs/editor/extensions/overview
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Related Skills

- **Tiptap Extension**: For adding editor functionality
  - Reference skill: `umbraco-tiptap-extension`

- **Modals**: When toolbar buttons open modal dialogs
  - Reference skill: `umbraco-modals`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - Button, menu, or color picker? What action to execute?
3. **Generate files** - Create manifest + API class based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Button Kind Manifest (manifests.ts)
```typescript
import type { ManifestTiptapToolbarExtensionButtonKind } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestTiptapToolbarExtensionButtonKind = {
  type: 'tiptapToolbarExtension',
  kind: 'button',
  alias: 'My.TiptapToolbar.Bold',
  name: 'Bold Toolbar Button',
  api: () => import('./bold.tiptap-toolbar-api.js'),
  forExtensions: ['Umb.Tiptap.Bold'], // Links to the tiptap extension
  meta: {
    alias: 'bold',
    icon: 'icon-bold',
    label: 'Bold',
  },
};

export const manifests = [manifest];
```

### Button API (bold.tiptap-toolbar-api.ts)
```typescript
import { UmbTiptapToolbarElementApiBase } from '@umbraco-cms/backoffice/tiptap';
import type { Editor } from '@tiptap/core';

export default class BoldToolbarApi extends UmbTiptapToolbarElementApiBase {
  execute(editor?: Editor) {
    editor?.chain().focus().toggleBold().run();
  }
}
```

### Button with Custom Active/Disabled State
```typescript
import { UmbTiptapToolbarElementApiBase } from '@umbraco-cms/backoffice/tiptap';
import type { Editor } from '@tiptap/core';

export default class CustomToolbarApi extends UmbTiptapToolbarElementApiBase {
  execute(editor?: Editor) {
    editor?.chain().focus().toggleHighlight().run();
  }

  // Override to customize active state detection
  isActive(editor?: Editor): boolean {
    return editor?.isActive('highlight') ?? false;
  }

  // Override to customize disabled state
  isDisabled(editor?: Editor): boolean {
    return !editor?.can().toggleHighlight() ?? true;
  }
}
```

### Menu Kind Manifest
```typescript
import type { ManifestTiptapToolbarExtensionMenuKind } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestTiptapToolbarExtensionMenuKind = {
  type: 'tiptapToolbarExtension',
  kind: 'menu',
  alias: 'My.TiptapToolbar.Headings',
  name: 'Headings Menu',
  api: () => import('./headings.tiptap-toolbar-api.js'),
  forExtensions: ['Umb.Tiptap.Heading'],
  meta: {
    alias: 'headings',
    icon: 'icon-heading',
    label: 'Headings',
    look: 'text', // 'icon' or 'text'
  },
  items: [
    { label: 'Heading 1', data: { level: 1 } },
    { label: 'Heading 2', data: { level: 2 } },
    { label: 'Heading 3', data: { level: 3 } },
    { label: 'Paragraph', data: { level: 0 } },
  ],
};
```

### Menu API
```typescript
import { UmbTiptapToolbarElementApiBase } from '@umbraco-cms/backoffice/tiptap';
import type { Editor } from '@tiptap/core';

export default class HeadingsToolbarApi extends UmbTiptapToolbarElementApiBase {
  execute(editor?: Editor, level?: number) {
    if (level === 0) {
      editor?.chain().focus().setParagraph().run();
    } else {
      editor?.chain().focus().toggleHeading({ level: level as 1 | 2 | 3 | 4 | 5 | 6 }).run();
    }
  }

  isActive(editor?: Editor, level?: number): boolean {
    if (level === 0) {
      return editor?.isActive('paragraph') ?? false;
    }
    return editor?.isActive('heading', { level }) ?? false;
  }
}
```

### Style Menu Kind
```typescript
import type { ManifestTiptapToolbarExtensionStyleMenuKind } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestTiptapToolbarExtensionStyleMenuKind = {
  type: 'tiptapToolbarExtension',
  kind: 'styleMenu',
  alias: 'My.TiptapToolbar.Styles',
  name: 'Style Menu',
  api: () => import('./styles.tiptap-toolbar-api.js'),
  meta: {
    alias: 'styles',
    icon: 'icon-palette',
    label: 'Styles',
  },
  items: [
    {
      label: 'Lead Paragraph',
      data: { class: 'lead' },
      appearance: { style: 'font-size: 1.2em' },
    },
    {
      label: 'Small Text',
      data: { class: 'small' },
      appearance: { style: 'font-size: 0.85em' },
    },
    {
      label: 'Highlight Box',
      data: { class: 'highlight-box' },
    },
  ],
};
```

### Color Picker Button Kind
```typescript
import type { ManifestTiptapToolbarExtensionColorPickerButtonKind } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestTiptapToolbarExtensionColorPickerButtonKind = {
  type: 'tiptapToolbarExtension',
  kind: 'colorPickerButton',
  alias: 'My.TiptapToolbar.TextColor',
  name: 'Text Color',
  api: () => import('./text-color.tiptap-toolbar-api.js'),
  meta: {
    alias: 'textColor',
    icon: 'icon-palette',
    label: 'Text Color',
  },
};
```

### Toolbar Button Opening Modal
```typescript
import { UmbTiptapToolbarElementApiBase } from '@umbraco-cms/backoffice/tiptap';
import { UMB_MODAL_MANAGER_CONTEXT } from '@umbraco-cms/backoffice/modal';
import type { Editor } from '@tiptap/core';

export default class LinkToolbarApi extends UmbTiptapToolbarElementApiBase {
  async execute(editor?: Editor) {
    const modalManager = await this.getContext(UMB_MODAL_MANAGER_CONTEXT);

    const modal = modalManager.open(this, MY_LINK_MODAL, {
      data: {
        currentHref: editor?.getAttributes('link').href,
      },
    });

    const result = await modal.onSubmit();
    if (result?.href) {
      editor?.chain().focus().setLink({ href: result.href }).run();
    }
  }
}
```

## Toolbar Extension Kinds

| Kind | Use Case |
|------|----------|
| `button` | Simple toggle button |
| `colorPickerButton` | Color selection |
| `menu` | Dropdown with options |
| `styleMenu` | Style/class selection |

## Meta Properties

| Property | Description |
|----------|-------------|
| `alias` | Used for isActive detection |
| `icon` | Toolbar button icon |
| `label` | Tooltip text |
| `look` | (menu only) 'icon' or 'text' |

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
