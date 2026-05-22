---
name: umbraco-monaco-markdown-editor-action
description: Implement Monaco markdown editor actions in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Monaco Markdown Editor Action

## What is it?
Monaco Markdown Editor Actions add custom toolbar buttons and keyboard shortcuts to the Markdown editor in Umbraco. They allow you to extend the editing experience with custom functionality like inserting links, images, or custom markdown syntax. Actions appear in the editor toolbar and can respond to keyboard shortcuts.

## Documentation
Always fetch the latest docs before implementing:

- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry
- **Monaco Editor**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types

## Related Foundation Skills

- **Modals**: When opening modal dialogs from actions
  - Reference skill: `umbraco-modals`

- **Localization**: When providing localized labels
  - Reference skill: `umbraco-localization`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What functionality? What keyboard shortcut? What icon?
3. **Generate files** - Create manifest + action class based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
export const manifests: Array<UmbExtensionManifest> = [
  {
    type: 'monacoMarkdownEditorAction',
    alias: 'My.MonacoMarkdownEditorAction.Custom',
    name: 'Custom Monaco Markdown Editor Action',
    api: () => import('./my-markdown-action.js'),
    meta: {
      label: 'Insert Custom',
      icon: 'icon-favorite',
    },
  },
];
```

### Action Implementation (my-markdown-action.ts)
```typescript
import { monaco } from '@umbraco-cms/backoffice/external/monaco-editor';
import { UmbControllerBase } from '@umbraco-cms/backoffice/class-api';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';
import type { UUIModalSidebarSize } from '@umbraco-cms/backoffice/external/uui';

export class MyMarkdownAction extends UmbControllerBase {
  constructor(host: UmbControllerHost) {
    super(host);
  }

  getUnique() {
    return 'My.MonacoMarkdownEditorAction.Custom';
  }

  getLabel() {
    return 'Insert Custom';
  }

  getKeybindings() {
    // Ctrl/Cmd + Shift + C
    return [monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KeyC];
  }

  async execute({ editor, overlaySize }: { editor: any; overlaySize: UUIModalSidebarSize }) {
    if (!editor) throw new Error('Editor not found');

    const selection = editor.getSelections()[0];
    if (!selection) return;

    const selectedValue = editor.getValueInRange(selection);

    // Insert custom markdown
    editor.monacoEditor?.executeEdits('', [
      { range: selection, text: `**${selectedValue || 'custom'}**` },
    ]);

    editor.monacoEditor?.focus();
  }
}

export { MyMarkdownAction as api };
```

### Action with Modal
```typescript
import { monaco } from '@umbraco-cms/backoffice/external/monaco-editor';
import { UmbControllerBase } from '@umbraco-cms/backoffice/class-api';
import { UMB_MODAL_MANAGER_CONTEXT } from '@umbraco-cms/backoffice/modal';

export class MyModalMarkdownAction extends UmbControllerBase {
  getUnique() {
    return 'My.MonacoMarkdownEditorAction.Modal';
  }

  getLabel() {
    return 'Insert with Modal';
  }

  getKeybindings() {
    return [monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyM];
  }

  async execute({ editor, overlaySize }) {
    const modalManager = await this.getContext(UMB_MODAL_MANAGER_CONTEXT);
    if (!modalManager) throw new Error('Modal manager not found');

    const selection = editor?.getSelections()[0];
    if (!selection) return;

    // Open a modal and use the result
    const modalContext = modalManager.open(this, MY_CUSTOM_MODAL, {
      modal: { size: overlaySize },
    });

    modalContext?.onSubmit().then((value) => {
      if (!value) return;
      editor.monacoEditor?.executeEdits('', [
        { range: selection, text: value.text },
      ]);
    });
  }
}

export { MyModalMarkdownAction as api };
```

## Interface Reference

```typescript
interface ManifestMonacoMarkdownEditorAction extends ManifestApi<any> {
  type: 'monacoMarkdownEditorAction';
  meta?: MetaMonacoMarkdownEditorAction;
}

interface MetaMonacoMarkdownEditorAction {
  icon?: string | null;
  label?: string | null;  // Can use localization key like '#buttons_linkInsert'
}
```

## Common Key Bindings

```typescript
// Single key
monaco.KeyCode.Enter

// Ctrl/Cmd combinations
monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyK  // Ctrl+K or Cmd+K
monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KeyC  // Ctrl+Shift+C
monaco.KeyMod.Alt | monaco.KeyCode.KeyI  // Alt+I
```

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
