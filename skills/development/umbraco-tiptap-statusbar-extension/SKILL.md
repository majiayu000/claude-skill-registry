---
name: umbraco-tiptap-statusbar-extension
description: Implement Tiptap statusbar extensions for Umbraco rich text editor using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Tiptap Statusbar Extension

## What is it?
A Tiptap Statusbar Extension adds components to the status bar at the bottom of the Rich Text Editor. Common uses include showing element path (breadcrumb navigation), word count, character count, or other editor state information. Unlike toolbar extensions, statusbar extensions are purely visual/informational elements.

## Documentation
Always fetch the latest docs before implementing:

- **Extension Types**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types
- **Rich Text Editor**: https://docs.umbraco.com/umbraco-cms/fundamentals/backoffice/property-editors/built-in-umbraco-property-editors/rich-text-editor
- **Tiptap Docs**: https://tiptap.dev/docs/editor/extensions/overview
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Related Skills

- **Tiptap Extension**: For adding editor functionality
  - Reference skill: `umbraco-tiptap-extension`

- **Umbraco Element**: For implementing the statusbar element
  - Reference skill: `umbraco-umbraco-element`

- **Context API**: For accessing the Tiptap RTE context
  - Reference skill: `umbraco-context-api`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What information to display? Real-time updates needed?
3. **Generate files** - Create manifest + element based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestTiptapStatusbarExtension } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestTiptapStatusbarExtension = {
  type: 'tiptapStatusbarExtension',
  alias: 'My.TiptapStatusbar.WordCount',
  name: 'Word Count Statusbar',
  element: () => import('./word-count.statusbar-element.js'),
  forExtensions: [], // Optional: link to specific tiptap extensions
  meta: {
    alias: 'wordCount',
    icon: 'icon-document',
    label: 'Word Count',
  },
};

export const manifests = [manifest];
```

### Statusbar Element (word-count.statusbar-element.ts)
```typescript
import { html, css, customElement, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { UMB_TIPTAP_RTE_CONTEXT } from '@umbraco-cms/backoffice/tiptap';

@customElement('my-word-count-statusbar')
export class WordCountStatusbarElement extends UmbLitElement {
  @state()
  private _wordCount = 0;

  @state()
  private _charCount = 0;

  constructor() {
    super();

    this.consumeContext(UMB_TIPTAP_RTE_CONTEXT, (context) => {
      this.observe(context.editor, (editor) => {
        if (editor) {
          // Update counts when editor content changes
          editor.on('update', () => this.#updateCounts(editor));
          // Initial count
          this.#updateCounts(editor);
        }
      });
    });
  }

  #updateCounts(editor: any) {
    const text = editor.getText();
    this._charCount = text.length;
    this._wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  }

  render() {
    return html`
      <span class="count">Words: ${this._wordCount}</span>
      <span class="count">Characters: ${this._charCount}</span>
    `;
  }

  static styles = css`
    :host {
      display: flex;
      gap: var(--uui-size-space-4);
      font-size: var(--uui-type-small-size);
      color: var(--uui-color-text-alt);
    }

    .count {
      padding: 0 var(--uui-size-space-2);
    }
  `;
}

export default WordCountStatusbarElement;

declare global {
  interface HTMLElementTagNameMap {
    'my-word-count-statusbar': WordCountStatusbarElement;
  }
}
```

### Element Path Statusbar (Breadcrumb Navigation)
```typescript
import { html, css, customElement, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { UMB_TIPTAP_RTE_CONTEXT } from '@umbraco-cms/backoffice/tiptap';

@customElement('my-element-path-statusbar')
export class ElementPathStatusbarElement extends UmbLitElement {
  @state()
  private _path: string[] = [];

  constructor() {
    super();

    this.consumeContext(UMB_TIPTAP_RTE_CONTEXT, (context) => {
      this.observe(context.editor, (editor) => {
        if (editor) {
          editor.on('selectionUpdate', () => this.#updatePath(editor));
          this.#updatePath(editor);
        }
      });
    });
  }

  #updatePath(editor: any) {
    const { $from } = editor.state.selection;
    const path: string[] = [];

    for (let depth = $from.depth; depth > 0; depth--) {
      const node = $from.node(depth);
      path.unshift(node.type.name);
    }

    this._path = path;
  }

  #handleClick(index: number) {
    // Could implement navigation to that element
    console.log('Navigate to:', this._path[index]);
  }

  render() {
    return html`
      ${this._path.map(
        (name, index) => html`
          ${index > 0 ? html`<span class="separator">›</span>` : ''}
          <button @click=${() => this.#handleClick(index)}>${name}</button>
        `
      )}
    `;
  }

  static styles = css`
    :host {
      display: flex;
      align-items: center;
      font-size: var(--uui-type-small-size);
    }

    button {
      background: none;
      border: none;
      padding: var(--uui-size-space-1) var(--uui-size-space-2);
      cursor: pointer;
      color: var(--uui-color-text-alt);
    }

    button:hover {
      color: var(--uui-color-text);
      text-decoration: underline;
    }

    .separator {
      color: var(--uui-color-border);
      margin: 0 var(--uui-size-space-1);
    }
  `;
}

export default ElementPathStatusbarElement;
```

### Cursor Position Statusbar
```typescript
import { html, css, customElement, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { UMB_TIPTAP_RTE_CONTEXT } from '@umbraco-cms/backoffice/tiptap';

@customElement('my-cursor-position-statusbar')
export class CursorPositionStatusbarElement extends UmbLitElement {
  @state()
  private _line = 1;

  @state()
  private _column = 1;

  constructor() {
    super();

    this.consumeContext(UMB_TIPTAP_RTE_CONTEXT, (context) => {
      this.observe(context.editor, (editor) => {
        if (editor) {
          editor.on('selectionUpdate', () => this.#updatePosition(editor));
        }
      });
    });
  }

  #updatePosition(editor: any) {
    const { from } = editor.state.selection;
    // Simplified line/column calculation
    const doc = editor.state.doc;
    let pos = 0;
    let line = 1;

    doc.descendants((node: any, nodePos: number) => {
      if (nodePos >= from) return false;
      if (node.isBlock) line++;
      return true;
    });

    this._line = line;
    this._column = from - pos;
  }

  render() {
    return html`
      <span>Ln ${this._line}, Col ${this._column}</span>
    `;
  }

  static styles = css`
    :host {
      font-size: var(--uui-type-small-size);
      color: var(--uui-color-text-alt);
    }
  `;
}

export default CursorPositionStatusbarElement;
```

## Meta Properties

| Property | Description |
|----------|-------------|
| `alias` | Unique identifier for the statusbar item |
| `icon` | Icon (used in configuration UI) |
| `label` | Display name |

## Accessing Editor Context

Use `UMB_TIPTAP_RTE_CONTEXT` to access the Tiptap editor instance and subscribe to events like:
- `update` - Content changed
- `selectionUpdate` - Cursor/selection changed
- `focus` / `blur` - Focus state changed

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
