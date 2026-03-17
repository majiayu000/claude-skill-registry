---
name: prosemirror-notes
description: Guide for working with the ProseMirror-based notes editor. Use when editing notes feature code, fixing editor bugs, working with todos/checkboxes, wiki_links, decorations, or serialization.
---

# ProseMirror Notes Editor

This skill documents how the notes editor works, common pitfalls, and how to debug issues.

## Key Files

| File | Purpose |
|------|---------|
| `src/features/notes/simple-todo.ts` | Todo checkbox plugin (decorations, toggle, keyboard handling) |
| `src/components/prosemirror/tables/schema.ts` | Schema including `wiki_link` node definition |
| `src/components/prosemirror/tables/serializer.ts` | Markdown serialization |
| `src/components/prosemirror/tables/parser.ts` | Markdown parsing |
| `src/components/prosemirror/wiki-links/plugin.ts` | Wikilink autocomplete (`[[`) |

## Critical Concepts

### 1. Atom Nodes

The `wiki_link` node is defined as `atom: true`:

```typescript
const wikiLinkNodeSpec: NodeSpec = {
    group: "inline",
    inline: true,
    atom: true,  // <-- This is critical!
    attrs: { href: { default: "" }, title: { default: "" } },
    // ...
};
```

**What `atom: true` means:**
- The node is treated as a single indivisible unit
- Cursor cannot be placed inside it
- `textBetween()` represents it based on the `leafText` parameter, NOT its content

### 2. The `textBetween` Trap

`node.textBetween(from, to, blockSeparator?, leafText?)` extracts text, but:

- **Text nodes**: Returns their text content
- **Atom nodes**: Returns the `leafText` parameter value (default: empty string)

**THE BUG THAT BREAKS EVERYTHING:**

```typescript
// BAD - wiki_link becomes "\n", breaking regex matching
const text = node.textBetween(0, node.content.size, undefined, "\n");

// GOOD - wiki_link becomes "", regex works correctly
const text = node.textBetween(0, node.content.size, undefined, "");
```

If you use `"\n"` as leafText, a todo like:
```
- [ ] text [[link]] more
```

Becomes:
```
"- [ ] text \n more"
```

And `TODO_REGEX = /^(\s*)- \[([ xX])\] ?(.*)$/` fails because:
- `(.*)` stops at the newline
- `$` doesn't match (there's still `\n more` remaining)

### 3. Preserving Inline Nodes During Edits

When modifying a line that contains inline nodes (wiki_link, marks, etc.):

**BAD - Destroys inline nodes:**
```typescript
// This replaces entire line with plain text
transaction.replaceWith(
    range.lineStart,
    range.lineEnd,
    state.schema.text(newText)  // <-- Creates plain text, destroys wiki_links!
);
```

**GOOD - Preserves inline nodes:**
```typescript
// Only replace the specific character that needs to change
// For toggling checkbox: only replace the " " or "x" character
const checkboxPos = range.lineStart + indent.length + 3;  // Position of checkbox char
transaction.replaceWith(
    checkboxPos,
    checkboxPos + 1,
    state.schema.text(newChecked)  // Just " " or "x"
);
```

### 4. How Todo Decorations Work

The todo system uses ProseMirror decorations to:
1. Hide the raw `- [ ] ` markdown
2. Show a checkbox widget in its place
3. Apply styling classes to the paragraph

```typescript
function buildTodoDecorations(doc: PMNode): DecorationSet {
    doc.descendants((node, pos) => {
        // Get text content (atom nodes become empty string)
        const text = node.textBetween(0, node.content.size, undefined, "");

        // Match todo pattern
        const match = text.match(TODO_REGEX);
        if (match) {
            // 1. Node decoration for styling
            decorations.push(Decoration.node(pos, pos + node.nodeSize, {
                class: "todo-paragraph"
            }));

            // 2. Inline decoration to hide "- [ ] "
            decorations.push(Decoration.inline(markerStart, markerEnd, {
                class: "todo-marker-hidden"
            }));

            // 3. Widget decoration for checkbox
            decorations.push(Decoration.widget(markerStart,
                () => createCheckboxWidget(isChecked)
            ));
        }
    });
}
```

## Debugging Checklist

When todos/wikilinks aren't working:

1. **Check `textBetween` calls** - Are they using problematic `leafText` values?
2. **Check document structure** - Use `console.log(JSON.stringify(node.toJSON(), null, 2))`
3. **Check if decorations apply** - Inspect element to see if `todo-paragraph` class is present
4. **Check serialization** - Does saving and reloading preserve content?

## Common Patterns

### Getting Text for Regex Matching
```typescript
// Always use empty string for leafText when matching patterns
// This applies to BOTH node.textBetween() and state.doc.textBetween()
const text = node.textBetween(0, node.content.size, undefined, "");
const lineText = state.doc.textBetween(start, end, undefined, "");
```

**ALL functions that use textBetween for regex matching must include `leafText: ""`:**
- `toggleTodoWithinRange`
- `handleTodoBackspace`
- `handleTodoEnter`
- `handleTodoClick`
- `handleTodoIndent`
- `handleTodoOutdent`
- `buildTodoDecorations`

### Safe Todo Toggle
```typescript
// For existing todos, only replace the checkbox character
if (isTodoLine) {
    const checkboxPos = lineStart + indent.length + 3;
    tr.replaceWith(checkboxPos, checkboxPos + 1, schema.text(newState));
}
```

### Inserting Inline Nodes
```typescript
// When inserting wiki_link via autocomplete
const wikiLinkNode = schema.nodes.wiki_link.create({
    href: noteName,
    title: displayTitle
});
tr.replaceWith(from, to, [wikiLinkNode, schema.text(" ")]);
```

## The Todo Regex Patterns

```typescript
// Standalone paragraph todo: "- [ ] text" or "- [x] text"
const TODO_REGEX = /^(\s*)- \[([ xX])\] ?(.*)$/;

// List item todo (inside list_item): "[ ] text" or "[x] text"
const LIST_TODO_REGEX = /^\[([ xX])\] ?(.*)$/;

// Trigger pattern for creating new todo
const TRIGGER_REGEX = /^(\s*)(-\s*)?\[\]$/;

// Empty todo detection
const EMPTY_TODO_REGEX = /^(\s*)- \[([ xX])\]\s*$/;
```

### CRITICAL: Handle BOTH Todo Formats

There are TWO todo formats that must be handled in every keyboard handler:

| Format | Regex | Example | Used In |
|--------|-------|---------|---------|
| Standalone | `TODO_REGEX` | `- [ ] text` | Paragraphs |
| List item | `LIST_TODO_REGEX` | `[ ] text` | Inside list items |

**Every handler must check BOTH patterns:**
- `handleTodoBackspace` - must handle both formats
- `handleTodoEnter` - must handle both formats
- `toggleTodoWithinRange` - must handle both formats
- `handleTodoClick` - checks both with `text.match(TODO_REGEX) \|\| text.match(LIST_TODO_REGEX)`

## Keyboard Handler Behaviors

### Enter Key (`handleTodoEnter`)

When pressing Enter on a todo line:
1. **Empty todo** → Remove the marker, leave empty line
2. **Todo with content** → Create new empty todo below

```typescript
// Always create a NEW empty todo (don't try to split content)
// This avoids position mapping issues with inline nodes
const newTodoContent = `${indent}- [ ] `;
```

### Backspace Key (`handleTodoBackspace`)

When pressing Backspace:
1. **Cursor at content start** → Remove the todo marker
2. **Empty todo, cursor anywhere after marker** → Remove the marker

```typescript
// Check if todo is empty/whitespace-only
const isEmptyTodo = !contentText.trim();

// Handle backspace if:
// 1. Cursor is at the very start of content, OR
// 2. Todo is empty and cursor is at or after content start
const atContentStart = cursorOffsetInLine === contentStartOffset;
const inEmptyTodo = isEmptyTodo && cursorOffsetInLine >= contentStartOffset;
```

**Marker length calculations:**
- Standalone todo `- [ ] `: marker is 6 chars (with trailing space) or 5 chars (without)
- List item todo `[ ] `: marker is 4 chars (with trailing space) or 3 chars (without)

## Position Calculations

### Document Positions vs Text Positions

- **Document positions**: Used by ProseMirror for cursor, selections, ranges
- **Text positions**: Character indices in strings from `textBetween()`

For plain text, these are equivalent. But with atom nodes (wiki_link):
- Atom node takes **1 document position**
- Atom node takes **0 text characters** (with `leafText: ""`)

This can cause mismatches when:
```typescript
// Document position-based
const cursorOffsetInLine = selection.from - paragraphRange.lineStart;

// Text position-based
const contentStartOffset = indent.length + markerLength;
```

**Solution**: For complex operations, work with document positions directly or avoid slicing text based on cursor position.

## Testing Changes

After modifying todo/wikilink code:

1. **Basic todo**: Create `- [ ] test`, verify checkbox renders
2. **With wikilink**: Add `[[link]]` via autocomplete, verify checkbox still works
3. **Toggle**: Click checkbox, verify wikilink preserved
4. **Enter on todo**: Press Enter, verify new checkbox created (not bullet)
5. **Enter on empty todo**: Press Enter, verify marker removed
6. **Backspace on empty todo**: Press Backspace, verify marker removed
7. **Indented todos**: Test all above with indented todos (2+ spaces)
8. **List item todos**: Test with `[ ] text` format inside lists
9. **Save/reload**: Verify content persists correctly
