---
name: web-editor-tiptap
description: Rich text editor framework with TipTap and ProseMirror
---

# TipTap Editor Patterns

> **Quick Guide:** TipTap is a headless, framework-agnostic rich text editor built on ProseMirror. Everything is an extension -- nodes define block/inline content, marks define formatting, extensions add functionality. Use `useEditor` hook (React/Vue) or the `Editor` class directly. Prefer JSON serialization over HTML. Set `immediatelyRender: false` for SSR. **Current: v3.x** -- Floating UI replaces Tippy.js, menus import from `/menus` sub-path, StarterKit includes Link/Underline by default.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST set `immediatelyRender: false` in useEditor when using SSR/SSG frameworks -- TipTap must never render on the server)**

**(You MUST import BubbleMenu and FloatingMenu from the `/menus` sub-path -- e.g. `@tiptap/react/menus` in v3)**

**(You MUST define `name`, `group`, `parseHTML`, and `renderHTML` on every custom Node -- missing any breaks schema resolution)**

**(You MUST use `editor.chain().focus()...run()` for chained commands -- forgetting `.focus()` loses cursor position, forgetting `.run()` silently does nothing)**

</critical_requirements>

---

**Auto-detection:** TipTap, tiptap, @tiptap/core, @tiptap/react, @tiptap/vue-3, @tiptap/starter-kit, useEditor, EditorContent, BubbleMenu, FloatingMenu, Node.create, Mark.create, Extension.create, NodeViewWrapper, NodeViewContent, ReactNodeViewRenderer, ProseMirror, editor.chain, editor.commands, addKeyboardShortcuts, addInputRules, addNodeView

**When to use:**

- Building rich text editors with custom formatting and block types
- Creating WYSIWYG editors with toolbar, bubble menu, or floating menu UIs
- Implementing custom nodes (embeds, mentions, code blocks with syntax highlighting)
- Serializing editor content to JSON or HTML for persistence
- Adding keyboard shortcuts, input rules, or paste rules to an editor

**When NOT to use:**

- Plain text input or textarea (use native HTML elements)
- Markdown-only editors without rich text rendering (use a markdown parser)
- Read-only content display (use a static renderer or HTML)

**Key patterns covered:**

- Editor setup with useEditor hook and EditorContent component
- Extension architecture: Node, Mark, and Extension types
- Custom node and mark creation with schema, commands, and keyboard shortcuts
- BubbleMenu and FloatingMenu for contextual toolbars
- React node views for complex interactive blocks
- Content serialization (JSON preferred) and persistence
- Input rules and paste rules for automatic formatting

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Editor setup, extensions, serialization, toolbar
- [examples/custom-extensions.md](examples/custom-extensions.md) - Custom nodes, marks, input rules, keyboard shortcuts
- [examples/menus.md](examples/menus.md) - BubbleMenu, FloatingMenu, slash commands
- [reference.md](reference.md) - Decision frameworks, StarterKit contents, anti-patterns

---

<philosophy>

## Philosophy

TipTap is a **headless editor framework** -- it provides behavior, schema, and state management without imposing any UI. You build the UI (toolbars, menus, formatting controls) yourself using your preferred component framework and styling solution.

**Everything is an extension.** Even core features like paragraphs, bold text, and undo/redo are extensions. This means:

1. **You control the schema** -- only include what your editor needs
2. **Extensions are composable** -- combine, configure, or extend any extension
3. **Custom content types are first-class** -- creating a custom node is the same API as built-in nodes

**ProseMirror under the hood.** TipTap wraps ProseMirror, so you get its battle-tested schema system, transaction model, and plugin architecture. When TipTap's API isn't enough, drop down to ProseMirror directly via `addProseMirrorPlugins()`.

**Framework-agnostic core.** `@tiptap/core` works with vanilla JS. Framework adapters (`@tiptap/react`, `@tiptap/vue-3`) add hooks and components but the editor logic is shared.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Editor Setup

The `useEditor` hook initializes the editor with extensions and content. `EditorContent` renders the editable area.

```typescript
import { useEditor, EditorContent } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";

const INITIAL_CONTENT = "<p>Start typing...</p>";

function RichTextEditor() {
  const editor = useEditor({
    extensions: [StarterKit],
    content: INITIAL_CONTENT,
    immediatelyRender: false, // Required for SSR frameworks
  });

  return <EditorContent editor={editor} />;
}
```

**Why good:** StarterKit bundles common extensions (paragraphs, headings, lists, bold, italic, etc.), `immediatelyRender: false` prevents SSR hydration mismatch

**Key useEditor options:** `extensions` (required), `content` (HTML string or JSON), `editable`, `autofocus` (`"start"`, `"end"`, `"all"`, number, boolean), `editorProps` (ProseMirror props like `attributes` for CSS classes), `onUpdate` callback

See [examples/core.md](examples/core.md) for full setup with toolbar and configuration options.

---

### Pattern 2: Extension Types

TipTap has three extension types that map to ProseMirror's schema model:

| Type          | Purpose                              | Examples                                     |
| ------------- | ------------------------------------ | -------------------------------------------- |
| **Node**      | Content blocks and inline elements   | Paragraph, Heading, Image, CodeBlock, Table  |
| **Mark**      | Formatting applied to text ranges    | Bold, Italic, Link, Highlight, Code          |
| **Extension** | Functionality without schema changes | UndoRedo, CharacterCount, Placeholder, Focus |

```typescript
import { Node } from "@tiptap/core";
import { Mark } from "@tiptap/core";
import { Extension } from "@tiptap/core";

// Each type uses the same .create() factory
const CustomNode = Node.create({ name: "customNode" /* ... */ });
const CustomMark = Mark.create({ name: "customMark" /* ... */ });
const CustomExt = Extension.create({ name: "customExt" /* ... */ });
```

**Key distinction:** Nodes and Marks define schema (parseHTML/renderHTML). Extensions add behavior only.

See [examples/custom-extensions.md](examples/custom-extensions.md) for complete custom node and mark examples.

---

### Pattern 3: Commands and Chaining

Commands modify editor state. Chain multiple commands and call `.run()` to execute.

```typescript
// Single command
editor.commands.toggleBold();

// Chained commands -- focus() keeps cursor in editor
editor.chain().focus().toggleBold().run();

// Check if a command can execute (without running it)
const canToggleBold = editor.can().toggleBold();

// Conditional formatting
editor.chain().focus().toggleHeading({ level: 2 }).run();
```

**Why `.focus()` matters:** Without it, clicking a toolbar button moves focus out of the editor. `.focus()` restores it before applying the command.

**Why `.run()` matters:** Chain builds a transaction but does not apply it until `.run()` is called. Forgetting `.run()` silently does nothing.

See [examples/core.md](examples/core.md) for toolbar integration with `isActive` checks.

---

### Pattern 4: Content Serialization

TipTap supports JSON and HTML output. **JSON is recommended** -- it preserves the document structure, is easier to parse, and allows external edits without an HTML parser.

```typescript
// Get content as JSON (recommended for persistence)
const json = editor.getJSON();

// Get content as HTML
const html = editor.getHTML();

// Get plain text
const text = editor.getText({ blockSeparator: "\n\n" });

// Set content from JSON or HTML
editor.commands.setContent(jsonData);
editor.commands.setContent("<p>HTML content</p>");
```

**Why JSON over HTML:** JSON maps directly to the ProseMirror document tree. HTML requires parsing and may lose information if the schema changes. JSON also enables easier diffing, validation, and migration.

See [examples/core.md](examples/core.md) for persistence patterns with localStorage and API.

---

### Pattern 5: Custom Node Creation

Custom nodes define new content types in the editor schema. Every node needs `name`, `group`, `parseHTML`, and `renderHTML`.

```typescript
import { Node, mergeAttributes } from "@tiptap/core";

const Callout = Node.create({
  name: "callout",
  group: "block",
  content: "block+",

  addAttributes() {
    return {
      type: { default: "info" },
    };
  },

  parseHTML() {
    return [{ tag: 'div[data-type="callout"]' }];
  },

  renderHTML({ HTMLAttributes }) {
    return [
      "div",
      mergeAttributes({ "data-type": "callout" }, HTMLAttributes),
      0,
    ];
  },
});
```

**Key schema properties:** `group` ("block" or "inline"), `content` (ProseMirror content expression like "block+", "inline*", "text*"), `inline` (boolean), `atom` (true = non-editable unit), `selectable`, `draggable`

**The `0` in renderHTML:** Represents the content hole where child content renders. Omit for atom/leaf nodes.

See [examples/custom-extensions.md](examples/custom-extensions.md) for complete nodes with commands, keyboard shortcuts, and input rules.

---

### Pattern 6: Custom Mark Creation

Marks apply formatting to text ranges. They need `parseHTML` and `renderHTML` like nodes but use `addAttributes` for styling properties.

```typescript
import { Mark, mergeAttributes } from "@tiptap/core";

const Highlight = Mark.create({
  name: "highlight",

  addAttributes() {
    return {
      color: { default: "yellow" },
    };
  },

  parseHTML() {
    return [{ tag: "mark" }];
  },

  renderHTML({ HTMLAttributes }) {
    return ["mark", mergeAttributes(HTMLAttributes), 0];
  },

  addCommands() {
    return {
      toggleHighlight:
        (attrs) =>
        ({ commands }) => {
          return commands.toggleMark(this.name, attrs);
        },
    };
  },
});
```

**Mark-specific options:** `inclusive` (whether typing at mark boundary extends the mark), `excludes` (marks that cannot coexist -- e.g. bold excludes itself), `spanning` (whether mark can span multiple nodes)

See [examples/custom-extensions.md](examples/custom-extensions.md) for marks with keyboard shortcuts and input rules.

---

### Pattern 7: BubbleMenu and FloatingMenu

BubbleMenu appears on text selection. FloatingMenu appears on empty lines. Both use Floating UI for positioning in v3.

```typescript
import { BubbleMenu, FloatingMenu } from "@tiptap/react/menus";

// BubbleMenu -- appears when text is selected
<BubbleMenu editor={editor}>
  <button onClick={() => editor.chain().focus().toggleBold().run()}>Bold</button>
</BubbleMenu>

// FloatingMenu -- appears on empty lines
<FloatingMenu editor={editor}>
  <button onClick={() => editor.chain().focus().setHeading({ level: 1 }).run()}>H1</button>
</FloatingMenu>
```

**Key props:** `editor` (required), `shouldShow` callback for custom visibility logic, `pluginKey` for multiple menu instances, Floating UI middleware options (`placement`, `offset`, `flip`)

See [examples/menus.md](examples/menus.md) for shouldShow patterns, multiple menus, and slash command implementation.

---

### Pattern 8: React Node Views

For complex interactive blocks (widgets, embeds, counters), use React components as node views.

```tsx
import { NodeViewWrapper, NodeViewContent } from "@tiptap/react";
import { ReactNodeViewRenderer } from "@tiptap/react";

// The React component receives props from TipTap
function CalloutView({ node, updateAttributes }) {
  return (
    <NodeViewWrapper className="callout" data-type={node.attrs.type}>
      <select
        contentEditable={false}
        value={node.attrs.type}
        onChange={(e) => updateAttributes({ type: e.target.value })}
      >
        <option value="info">Info</option>
        <option value="warning">Warning</option>
      </select>
      <NodeViewContent className="callout-content" />
    </NodeViewWrapper>
  );
}

// Register in the node extension
const CalloutNode = Node.create({
  name: "callout",
  // ... schema config ...
  addNodeView() {
    return ReactNodeViewRenderer(CalloutView);
  },
});
```

**Props available:** `editor`, `node`, `selected`, `extension`, `getPos()`, `updateAttributes()`, `deleteNode()`, `decorations`

**NodeViewWrapper is required** -- it sets up the DOM structure TipTap expects. `NodeViewContent` renders editable child content. Use `contentEditable={false}` on non-editable parts (buttons, selects).

See [examples/custom-extensions.md](examples/custom-extensions.md) for complete React node view examples.

</patterns>

---

<decision_framework>

## Decision Framework

### Extension Type Selection

```
What are you adding to the editor?
|
+-> New content type (renders in document)?
|   +-> Block-level (paragraph, heading, image)? -> Node with group: "block"
|   +-> Inline element (mention, emoji)? -> Node with group: "inline", inline: true
|   +-> Text formatting (bold, highlight, link)? -> Mark
|
+-> New behavior (no schema change)?
    +-> Keyboard shortcut? -> Extension with addKeyboardShortcuts
    +-> Character count, placeholder? -> Extension
    +-> ProseMirror plugin? -> Extension with addProseMirrorPlugins
```

### Node Interactivity

```
How interactive is the node?
|
+-> Static content (just renders HTML)?
|   -> renderHTML only, no node view needed
|
+-> Needs editable child content?
|   -> NodeViewContent inside NodeViewWrapper
|
+-> Complex interactive UI (buttons, inputs)?
    -> ReactNodeViewRenderer with contentEditable={false} on controls
```

### Content Serialization

```
How will you store editor content?
|
+-> Database / API? -> JSON (getJSON) -- structured, diffable, migratable
+-> Display as HTML elsewhere? -> HTML (getHTML) -- for rendering outside editor
+-> Search indexing? -> Plain text (getText) -- for full-text search
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Missing `immediatelyRender: false` with SSR frameworks -- causes hydration mismatch and server rendering errors
- Importing BubbleMenu/FloatingMenu from `@tiptap/react` instead of `@tiptap/react/menus` in v3 -- wrong import path
- Forgetting `.run()` on command chains -- builds transaction but never applies it, silently does nothing
- Forgetting `.focus()` before commands in toolbar buttons -- cursor leaves editor, commands may target wrong position
- Missing `parseHTML`/`renderHTML` on custom nodes/marks -- content cannot be loaded from or exported to HTML/JSON
- Using `editor.state.doc` directly to modify content instead of commands/transactions -- bypasses TipTap's update cycle

**Medium Priority Issues:**

- Not checking `editor.can()` before rendering toolbar buttons as active/disabled -- buttons appear clickable when command would fail
- Creating one monolithic extension instead of composable smaller ones -- harder to reuse and configure
- Using HTML for persistence when JSON would work -- JSON is more structured, diffable, and schema-aware
- Inline `editor.getJSON()` on every keystroke without debouncing -- performance issue on large documents

**Gotchas & Edge Cases:**

- `getPos()` in node views can return `undefined` in v3 -- always check before using
- `editor` from `useEditor` is `null` on first render and during SSR -- guard all `editor.` access
- StarterKit v3 includes Link and Underline by default -- adding them separately causes duplicate extension errors
- `NodeViewContent` tag cannot change at runtime -- set `as` prop once (e.g. `as="p"`)
- `mergeAttributes` is required in `renderHTML` to preserve user-added attributes (class, style, data-\*)
- `addInputRules` regex must end with `$` (caret at cursor position); `addPasteRules` regex should NOT end with `$` but must use `/g` flag
- Multiple input rules matching the same pattern -- only the first match in extension order fires
- ProseMirror content expressions: `"block+"` means one-or-more blocks, `"inline*"` means zero-or-more inline, `"text*"` means text only -- mismatches cause schema validation errors

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST set `immediatelyRender: false` in useEditor when using SSR/SSG frameworks -- TipTap must never render on the server)**

**(You MUST import BubbleMenu and FloatingMenu from the `/menus` sub-path -- e.g. `@tiptap/react/menus` in v3)**

**(You MUST define `name`, `group`, `parseHTML`, and `renderHTML` on every custom Node -- missing any breaks schema resolution)**

**(You MUST use `editor.chain().focus()...run()` for chained commands -- forgetting `.focus()` loses cursor position, forgetting `.run()` silently does nothing)**

**Failure to follow these rules will cause SSR crashes, import errors, silent command failures, and broken editor schemas.**

</critical_reminders>
