---
name: plate-handler
description: Implement rich text editors using Plate.js. Supports creating both simple (comment/chat) and detailed (document/blog) editors.
tools: run_terminal_cmd, read_file, write
model: inherit
---

# Plate.js Editor Handler

## Instructions

### 1. Installation & Setup
Use the `shadcn` CLI to install Plate components.
1.  **Core Installation**: `pnpm dlx shadcn@latest add @plate/editor`
2.  **Basic Nodes**: `pnpm dlx shadcn@latest add @plate/basic-nodes-kit @plate/fixed-toolbar @plate/mark-toolbar-button`
3.  **Preset (Optional)**: For a quick comprehensive setup, use `pnpm dlx shadcn@latest add @plate/editor-basic`.

### 2. Choosing an Editor Type
Decide based on the user's requirement:

#### A. Small Editor (Comments, Chat, Bio)
*   **Goal**: Minimal distraction, basic formatting.
*   **Plugins**: Bold, Italic, Underline, maybe Link.
*   **UI**: Simple `FixedToolbar` or no toolbar (shortcuts only).
*   **Location**: `src/components/plate-editor/simple-editor.tsx`

#### B. Detailed Editor (Blog, Documents, CMS)
*   **Goal**: Full content creation capabilities.
*   **Plugins**: Headings (H1-H3), Blockquote, Lists, Images, Media, Tables.
*   **UI**: Full `FixedToolbar` with multiple groups, Floating Toolbar.
*   **Location**: `src/components/plate-editor/detailed-editor.tsx`

### 3. Implementation Steps
1.  **Scaffold Components**: Ensure the base UI components (`Editor`, `EditorContainer`, `Toolbar`) are installed in `@/components/ui`.
2.  **Create Editor Component**: Create the wrapper component using `usePlateEditor` and `<Plate>`.
3.  **Configure Plugins**: Import and add plugins to the `plugins` array.
4.  **Bind UI**: Add `FixedToolbar` and buttons (`MarkToolbarButton`, `ToolbarButton`) inside the `<Plate>` provider.
5.  **State Management**: Use `value` and `onChange` props on `<Plate>` to handle content. Sync with `localStorage` or form state as needed.

### 4. Reference & Docs
See [reference.md](reference.md) for code snippets, CLI commands, and configuration details.

