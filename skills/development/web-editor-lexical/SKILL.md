---
name: web-editor-lexical
description: Extensible text editor framework by Meta
---

# Lexical Editor Patterns

> **Quick Guide:** Lexical is a lightweight (22kb min+gzip) extensible text editor framework. Use `LexicalComposer` for React setup with plugins as child components. Extend via the node system (ElementNode, TextNode, DecoratorNode), command system (createCommand + priorities), and transforms. EditorState is immutable -- all mutations happen inside `editor.update()`. Use `$`-prefixed functions only inside update/read closures. **Current: v0.42.x (pre-1.0)**

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST call `$`-prefixed functions (`$getRoot`, `$getSelection`, `$createTextNode`) ONLY inside `editor.update()` or `editor.read()` closures -- calling them outside throws runtime errors)**

**(You MUST register custom nodes in the `nodes` array of `initialConfig` -- unregistered nodes cause silent failures or runtime errors)**

**(You MUST return a cleanup function from `useEffect` when registering commands, transforms, or listeners -- Lexical register methods return unsubscribe functions)**

**(You MUST include preconditions in transforms to prevent infinite loops -- a transform that unconditionally modifies its target node re-triggers itself)**

</critical_requirements>

---

**Auto-detection:** Lexical, lexical, @lexical/react, @lexical/rich-text, @lexical/list, @lexical/code, @lexical/link, @lexical/html, @lexical/headless, LexicalComposer, EditorState, LexicalNode, ElementNode, TextNode, DecoratorNode, createCommand, dispatchCommand, registerCommand, COMMAND_PRIORITY, $getRoot, $getSelection, $createParagraphNode, $createTextNode, RichTextPlugin, OnChangePlugin, HistoryPlugin, useLexicalComposerContext, editor.update, editor.read, registerNodeTransform, exportJSON, importJSON, exportDOM, importDOM, NodeState, createState

**When to use:**

- Building rich text editors with custom formatting and embedded content
- Creating editors with custom node types (mentions, embeds, code blocks)
- Implementing collaborative editing with operational transforms
- Building structured content editors (not just plain text)

**When NOT to use:**

- Plain text inputs without formatting (use a standard `<textarea>`)
- Simple markdown editing without live preview (use a textarea with markdown parsing)
- Editors that need pure decorations without document mutation (Lexical decorator nodes mutate content)

**Key patterns covered:**

- React setup with LexicalComposer, plugins, and initialConfig
- Node system: ElementNode, TextNode, DecoratorNode, custom nodes
- Command system: createCommand, priorities, dispatching, propagation
- Transforms for automatic node mutations
- EditorState immutability and the update lifecycle
- JSON and HTML serialization

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Editor setup, plugins, commands, transforms
- [examples/custom-nodes.md](examples/custom-nodes.md) - Custom ElementNode, TextNode, DecoratorNode, NodeState API
- [examples/serialization.md](examples/serialization.md) - JSON/HTML serialization, import/export, headless usage
- [reference.md](reference.md) - Decision frameworks, command priority table, anti-patterns

---

<philosophy>

## Philosophy

Lexical is an editor framework, not a batteries-included editor. The core is intentionally minimal -- it provides the node tree, selection, reconciler, command system, and update lifecycle. Everything else (toolbars, formatting, lists, links, embeds) is a plugin.

**Key architectural principles:**

- **Immutable EditorState:** The editor maintains a frozen state snapshot. Mutations happen inside `editor.update()` closures that clone the state, apply changes, then reconcile to DOM.
- **`$`-function convention:** Functions prefixed with `$` (like `$getRoot()`, `$getSelection()`) must run inside `editor.update()` or `editor.read()` closures -- similar to React hooks requiring a component context.
- **Plugin = React component:** In the React binding, a plugin is a React component rendered as a child of `<LexicalComposer>`. It accesses the editor via `useLexicalComposerContext()` and registers commands/transforms/listeners in `useEffect`.
- **Command-driven architecture:** User interactions and plugin communication flow through typed commands with priority-based listeners, enabling plugins to intercept or augment behavior.
- **Node-driven content model:** Content is a tree of typed nodes. Custom content types (mentions, embeds, polls) are custom node classes.

**When to use Lexical:**

- Rich text editing with custom formatting and embedded content
- Content editors requiring structured output (not just HTML strings)
- Editors needing accessibility and screen reader support
- Applications requiring server-side rendering or headless processing of editor content

**When NOT to use Lexical:**

- Simple text inputs (a `<textarea>` is simpler and lighter)
- Editors needing pure decorations that don't affect document content
- Projects requiring a stable 1.0 API (Lexical is pre-1.0, APIs may change)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: React Editor Setup

The minimal setup uses `LexicalComposer` wrapping plugin components. Each plugin is a React component that accesses the editor via context.

```typescript
import { LexicalComposer } from "@lexical/react/LexicalComposer";
import { RichTextPlugin } from "@lexical/react/LexicalRichTextPlugin";
import { ContentEditable } from "@lexical/react/LexicalContentEditable";
import { HistoryPlugin } from "@lexical/react/LexicalHistoryPlugin";
import { LexicalErrorBoundary } from "@lexical/react/LexicalErrorBoundary";

const EDITOR_NAMESPACE = "MyEditor";

const theme = {
  paragraph: "editor-paragraph",
  text: {
    bold: "editor-text-bold",
    italic: "editor-text-italic",
  },
};

function onError(error: Error) {
  console.error(error);
}

const initialConfig = {
  namespace: EDITOR_NAMESPACE,
  theme,
  onError,
  nodes: [], // Register custom nodes here
};

export function Editor() {
  return (
    <LexicalComposer initialConfig={initialConfig}>
      <RichTextPlugin
        contentEditable={<ContentEditable className="editor-input" />}
        ErrorBoundary={LexicalErrorBoundary}
      />
      <HistoryPlugin />
    </LexicalComposer>
  );
}
```

**Why good:** Plugins compose as children, initialConfig centralizes node registration and theming, error boundary catches update errors gracefully

See [examples/core.md](examples/core.md) for the full setup with OnChangePlugin, AutoFocusPlugin, and custom plugins.

---

### Pattern 2: The `$`-Function Convention and Update Lifecycle

All state reads and mutations use `$`-prefixed functions inside `editor.update()` (mutable) or `editor.read()` (read-only) closures. This ensures state consistency and prevents stale reads.

```typescript
import { $getRoot, $createParagraphNode, $createTextNode } from "lexical";

// Writing: editor.update() clones state, applies changes, reconciles DOM
editor.update(() => {
  const root = $getRoot();
  const paragraph = $createParagraphNode();
  const text = $createTextNode("Hello world");
  paragraph.append(text);
  root.append(paragraph);
});

// Reading: editor.read() provides safe read-only access
editor.read(() => {
  const root = $getRoot();
  const textContent = root.getTextContent();
});
```

**Why good:** Immutable state model prevents race conditions, `$` prefix signals context requirement (like React hooks), update batching minimizes DOM reconciliation

**Gotcha:** `$`-functions called outside update/read closures throw runtime errors. There is no compile-time check.

---

### Pattern 3: Command System

Commands are the communication bus between plugins, toolbars, and the editor core. Create typed commands, dispatch them from UI, and register listeners with priorities.

```typescript
import {
  createCommand,
  COMMAND_PRIORITY_EDITOR,
  COMMAND_PRIORITY_LOW,
  type LexicalCommand,
} from "lexical";

// Create a typed command
export const INSERT_IMAGE_COMMAND: LexicalCommand<{
  src: string;
  alt: string;
}> = createCommand("INSERT_IMAGE_COMMAND");

// Dispatch from toolbar or UI
editor.dispatchCommand(INSERT_IMAGE_COMMAND, {
  src: "/image.png",
  alt: "Photo",
});
```

**Priority levels** (higher number = runs first, can intercept):

| Priority                    | Value | Use case                           |
| --------------------------- | ----- | ---------------------------------- |
| `COMMAND_PRIORITY_CRITICAL` | 4     | Emergency overrides                |
| `COMMAND_PRIORITY_HIGH`     | 3     | Table navigation, critical plugins |
| `COMMAND_PRIORITY_NORMAL`   | 2     | Standard plugin behavior           |
| `COMMAND_PRIORITY_LOW`      | 1     | Default for most plugins           |
| `COMMAND_PRIORITY_EDITOR`   | 0     | Base editor behavior               |

**Return `true`** from a listener to stop propagation to lower-priority listeners.

See [examples/core.md](examples/core.md) for the full command registration pattern with cleanup.

---

### Pattern 4: Custom Plugins (React)

A plugin is a React component that registers commands, transforms, or listeners via `useLexicalComposerContext`. Always return cleanup functions from `useEffect`.

```typescript
import { useEffect } from "react";
import { useLexicalComposerContext } from "@lexical/react/LexicalComposerContext";
import {
  COMMAND_PRIORITY_LOW,
  FORMAT_TEXT_COMMAND,
  type TextFormatType,
} from "lexical";

export function ToolbarPlugin() {
  const [editor] = useLexicalComposerContext();

  const handleFormat = (format: TextFormatType) => {
    editor.dispatchCommand(FORMAT_TEXT_COMMAND, format);
  };

  return (
    <div className="toolbar">
      <button onClick={() => handleFormat("bold")} type="button">
        Bold
      </button>
      <button onClick={() => handleFormat("italic")} type="button">
        Italic
      </button>
    </div>
  );
}
```

**Why good:** Plugin accesses editor through context hook, dispatches built-in FORMAT_TEXT_COMMAND, renders null or UI as needed

See [examples/core.md](examples/core.md) for plugins that register commands with useEffect cleanup.

---

### Pattern 5: Node Transforms

Transforms automatically mutate nodes when conditions are met. They run before DOM reconciliation, making them the most efficient way to react to content changes.

```typescript
import { TextNode } from "lexical";

// Transform: auto-capitalize first letter of paragraphs
editor.registerNodeTransform(TextNode, (textNode) => {
  const text = textNode.getTextContent();
  // CRITICAL: Precondition prevents infinite loop
  if (text.length > 0 && text[0] !== text[0].toUpperCase()) {
    textNode.setTextContent(text[0].toUpperCase() + text.slice(1));
  }
});
```

**Why preconditions matter:** Without the check, `setTextContent` marks the node dirty, re-triggering the transform infinitely.

**Transform execution order:** Leaf nodes first, then element nodes, then RootNode. Multiple transforms produce a single DOM reconciliation.

See [examples/core.md](examples/core.md) for transform registration with cleanup and use cases.

---

### Pattern 6: Custom Nodes

Lexical provides three extendable base nodes for custom content types:

| Base Node          | Purpose                                       | Key method                       |
| ------------------ | --------------------------------------------- | -------------------------------- |
| `ElementNode`      | Container nodes (blockquote, callout)         | `createDOM()`, `updateDOM()`     |
| `TextNode`         | Styled text variants (colored text, mentions) | `createDOM()`, `updateDOM()`     |
| `DecoratorNode<T>` | Embedded components (images, videos, polls)   | `decorate()` returns a component |

Every custom node requires:

1. `static getType()` -- unique string identifier
2. `static clone(node)` -- create copy for state snapshots
3. `createDOM()` -- return the HTMLElement representation
4. `updateDOM()` -- return `false` if existing DOM can be reused
5. `exportJSON()` / `static importJSON()` -- serialization
6. Registration in `initialConfig.nodes`

```typescript
import { DecoratorNode } from "lexical";
import type { LexicalNode, NodeKey, EditorConfig } from "lexical";

export class ImageNode extends DecoratorNode<JSX.Element> {
  __src: string;
  __alt: string;

  static getType(): string {
    return "image";
  }

  static clone(node: ImageNode): ImageNode {
    return new ImageNode(node.__src, node.__alt, node.__key);
  }

  constructor(src: string, alt: string, key?: NodeKey) {
    super(key);
    this.__src = src;
    this.__alt = alt;
  }

  createDOM(_config: EditorConfig): HTMLElement {
    return document.createElement("div");
  }

  updateDOM(): boolean {
    return false;
  }

  decorate(): JSX.Element {
    return <img src={this.__src} alt={this.__alt} />;
  }
}
```

**Property convention:** Prefix private properties with `__` (double underscore) to prevent minification issues. All properties must be JSON-serializable.

See [examples/custom-nodes.md](examples/custom-nodes.md) for complete ElementNode, TextNode, DecoratorNode examples with serialization and the NodeState API.

---

### Pattern 7: EditorState Serialization

Lexical supports JSON (preferred for persistence) and HTML (for display or interop).

```typescript
import { $generateHtmlFromNodes } from "@lexical/html";

// JSON: lossless round-trip
const json = editor.getEditorState().toJSON();
const jsonString = JSON.stringify(json);

// Restore from JSON
const editorState = editor.parseEditorState(jsonString);
editor.setEditorState(editorState);

// HTML: for rendering or export
editor.read(() => {
  const html = $generateHtmlFromNodes(editor, null);
});
```

**JSON vs HTML:** JSON preserves the full node tree and is the recommended format for persistence. HTML is lossy (loses custom node properties) but useful for display or email content.

See [examples/serialization.md](examples/serialization.md) for complete import/export patterns, HTML-to-Lexical conversion, and headless editor usage.

</patterns>

---

<decision_framework>

## Decision Framework

### Which Node Type to Extend

```
Does your content contain child nodes?
├─ YES → ElementNode (paragraphs, blockquotes, callouts)
└─ NO → Is it text with special formatting or behavior?
    ├─ YES → TextNode (colored text, mentions)
    └─ NO → Is it an embedded component (image, video, widget)?
        ├─ YES → DecoratorNode (renders arbitrary UI)
        └─ NO → Re-evaluate: most content fits one of the above
```

### Plugin vs Transform vs Listener

```
Need to react to content changes?
├─ YES → Does the reaction modify nodes?
│   ├─ YES → Transform (most efficient, runs before DOM reconciliation)
│   └─ NO → Update listener (read-only, runs after reconciliation)
└─ NO → Need to handle user actions or toolbar clicks?
    ├─ YES → Command (typed, priority-based, interceptable)
    └─ NO → Listener (registerUpdateListener for state observation)
```

### Command Priority Selection

```
Is this the base editor behavior?
├─ YES → COMMAND_PRIORITY_EDITOR (0)
└─ NO → Is this a standard plugin?
    ├─ YES → COMMAND_PRIORITY_LOW (1) or COMMAND_PRIORITY_NORMAL (2)
    └─ NO → Must it override other plugins (e.g., table navigation)?
        ├─ YES → COMMAND_PRIORITY_HIGH (3)
        └─ NO → Emergency override only?
            └─ YES → COMMAND_PRIORITY_CRITICAL (4)
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Calling `$`-prefixed functions outside `editor.update()` or `editor.read()` -- causes runtime errors with no compile-time warning
- Missing node registration in `initialConfig.nodes` -- custom nodes silently fail or throw when the editor encounters them
- Transforms without preconditions -- unconditional mutations retrigger the transform infinitely, freezing the editor
- Using `editor.update()` inside an update listener to modify state -- breaks undo/redo history and causes extra renders; use transforms instead
- Forgetting `useEffect` cleanup for register calls -- leaks listeners, causes stale references after component unmount

**Medium Priority Issues:**

- Direct DOM manipulation instead of using the node/command system -- bypasses the reconciler, causes state-DOM desync
- Storing non-JSON-serializable values in node properties (functions, Maps, Sets) -- breaks serialization silently
- Using `editor.setEditorState()` without cloning -- can cause unexpected focus changes; use `editorState.clone(null)` to prevent auto-focus
- Naming custom node `getType()` with a non-unique string -- collides with other nodes, causes deserialization failures
- Using `new MyNode()` directly instead of `$createMyNode()` factory -- bypasses the node replacement system (`$applyNodeReplacement`)
- Single underscore node properties (`_value` instead of `__value`) -- may be mangled by minifiers, breaking node access
- `console.log` in `onError` callback with no rethrow -- silently swallows editor errors; rethrow or send to error tracking

**Gotchas & Edge Cases:**

- `editor.update()` batches synchronously but reconciles asynchronously -- use `{ discrete: true }` option when you need synchronous DOM commit (e.g., before reading DOM measurements)
- Node property names must use `__` prefix convention -- single underscore properties may be mangled by minifiers
- `DecoratorNode.decorate()` returns a component that Lexical renders outside the normal React tree -- state management in decorator components needs care
- The `onError` callback in `initialConfig` receives errors from update closures -- if you don't rethrow, Lexical tries to recover gracefully
- `TextNode` modes: `"token"` makes text immutable (like a chip), `"segmented"` deletes word-by-word
- CSS `transition` does not work for animations based on node removal -- Lexical reconciles by removing DOM nodes, not hiding them
- The NodeState API (v0.26+) is experimental -- APIs may change without extended deprecation

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST call `$`-prefixed functions (`$getRoot`, `$getSelection`, `$createTextNode`) ONLY inside `editor.update()` or `editor.read()` closures -- calling them outside throws runtime errors)**

**(You MUST register custom nodes in the `nodes` array of `initialConfig` -- unregistered nodes cause silent failures or runtime errors)**

**(You MUST return a cleanup function from `useEffect` when registering commands, transforms, or listeners -- Lexical register methods return unsubscribe functions)**

**(You MUST include preconditions in transforms to prevent infinite loops -- a transform that unconditionally modifies its target node re-triggers itself)**

**Failure to follow these rules will cause runtime errors, memory leaks, frozen editors, and broken undo/redo history.**

</critical_reminders>
