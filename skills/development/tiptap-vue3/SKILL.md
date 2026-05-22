---
name: tiptap-vue3
description: This skill should be used when implementing, debugging, or fixing Tiptap WYSIWYG editors in Vue 3 applications. Triggers on Tiptap setup, WYSIWYG editors, rich text editors, task list creation, markdown editing, and Vue 3 editor implementation. Provides production-ready patterns with ZERO auto-conversion interference.
---

# Tiptap Vue 3 Skill

Implement production-ready Tiptap WYSIWYG editors in Vue 3 with clean API and full control over input behavior.

## Why Tiptap Over Milkdown

| Feature | Tiptap | Milkdown |
|---------|--------|----------|
| Input rule control | `enableInputRules: false` - one flag | Must skip multiple imports |
| Vue 3 integration | Official `@tiptap/vue-3` | Works but more complex |
| Bundle size | Smaller (modular) | Larger |
| Documentation | Excellent | Good |
| Task lists | Built-in extension | Requires GFM preset |

**Key Advantage**: Tiptap lets you disable auto-conversion with a single option, preventing the common issue where typing `-` automatically creates bullet lists before you can type `- [ ]` for task lists.

## When to Use

- Setting up rich text/WYSIWYG editor in Vue 3
- Disabling markdown auto-conversion (typing `-` shouldn't auto-bullet)
- Implementing task lists with checkboxes
- Adding toolbar controls (bold, italic, links)
- Needing clean ProseMirror-based editing

## Installation

```bash
npm install @tiptap/vue-3 @tiptap/starter-kit @tiptap/extension-task-list @tiptap/extension-task-item @tiptap/extension-link @tiptap/pm
```

## The Pattern (MEMORIZE THIS)

### TiptapEditor.vue Component

```vue
<template>
  <div class="tiptap-editor-container">
    <div class="editor-toolbar">
      <button class="toolbar-btn" title="Undo (Ctrl+Z)" @click="editor?.chain().focus().undo().run()" :disabled="!editor?.can().undo()">
        <Undo :size="14" />
      </button>
      <button class="toolbar-btn" title="Redo (Ctrl+Y)" @click="editor?.chain().focus().redo().run()" :disabled="!editor?.can().redo()">
        <Redo :size="14" />
      </button>
      <div class="toolbar-divider" />
      <button
        class="toolbar-btn"
        :class="{ active: editor?.isActive('bold') }"
        title="Bold (Ctrl+B)"
        @click="editor?.chain().focus().toggleBold().run()"
      >
        <BoldIcon :size="14" />
      </button>
      <button
        class="toolbar-btn"
        :class="{ active: editor?.isActive('italic') }"
        title="Italic (Ctrl+I)"
        @click="editor?.chain().focus().toggleItalic().run()"
      >
        <ItalicIcon :size="14" />
      </button>
      <button
        class="toolbar-btn"
        :class="{ active: editor?.isActive('bulletList') }"
        title="Bullet List"
        @click="editor?.chain().focus().toggleBulletList().run()"
      >
        <List :size="14" />
      </button>
      <button
        class="toolbar-btn"
        :class="{ active: editor?.isActive('taskList') }"
        title="Task List"
        @click="editor?.chain().focus().toggleTaskList().run()"
      >
        <CheckSquare :size="14" />
      </button>
      <button
        class="toolbar-btn"
        :class="{ active: editor?.isActive('link') }"
        title="Link (Ctrl+K)"
        @click="setLink"
      >
        <LinkIcon :size="14" />
      </button>
    </div>
    <div class="tiptap-surface" :dir="textDirection">
      <EditorContent :editor="editor" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { watch, onBeforeUnmount } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import TaskList from '@tiptap/extension-task-list'
import TaskItem from '@tiptap/extension-task-item'
import Link from '@tiptap/extension-link'
import { Bold as BoldIcon, Italic as ItalicIcon, List, CheckSquare, Link as LinkIcon, Undo, Redo } from 'lucide-vue-next'

interface Props {
  modelValue: string
  textDirection: 'ltr' | 'rtl'
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

// CRITICAL: enableInputRules: false prevents auto-conversion
// This means typing "-" won't auto-convert to bullet list
// Users can type "- [ ]" freely without interference
const editor = useEditor({
  content: props.modelValue,
  extensions: [
    StarterKit.configure({
      bulletList: {},
      orderedList: {},
    }),
    TaskList,
    TaskItem.configure({
      nested: true,
    }),
    Link.configure({
      openOnClick: false,
      HTMLAttributes: {
        class: 'editor-link',
      },
    }),
  ],
  // KEY OPTION: Disable all input rules (no auto-conversion)
  enableInputRules: false,
  // Keep paste rules for pasting formatted content
  enablePasteRules: true,
  onUpdate: ({ editor }) => {
    emit('update:modelValue', editor.getHTML())
  },
})

// Sync external value changes
watch(() => props.modelValue, (newValue) => {
  if (editor.value && editor.value.getHTML() !== newValue) {
    editor.value.commands.setContent(newValue, false)
  }
})

// Clean up on unmount
onBeforeUnmount(() => {
  editor.value?.destroy()
})

// Link dialog
const setLink = () => {
  if (!editor.value) return
  const previousUrl = editor.value.getAttributes('link').href
  const url = window.prompt('URL', previousUrl)
  if (url === null) return
  if (url === '') {
    editor.value.chain().focus().extendMarkRange('link').unsetLink().run()
    return
  }
  editor.value.chain().focus().extendMarkRange('link').setLink({ href: url }).run()
}
</script>
```

### Wrapper Component (MarkdownEditor.vue)

```vue
<template>
  <div class="markdown-editor" :dir="textDirection">
    <TiptapEditor
      :modelValue="internalValue"
      :textDirection="textDirection"
      @update:modelValue="handleInternalUpdate"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useDebounceFn } from '@vueuse/core'
import TiptapEditor from './TiptapEditor.vue'

interface Props {
  modelValue: string
  placeholder?: string
  rows?: number
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  placeholder: 'Type here...',
  rows: 4
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const internalValue = ref(props.modelValue)

const handleInternalUpdate = (html: string) => {
  if (html !== internalValue.value) {
    internalValue.value = html
    emit('update:modelValue', html)
  }
}

watch(() => props.modelValue, (newVal) => {
  if (newVal !== internalValue.value) {
    internalValue.value = newVal
  }
})

// RTL detection
const textDirection = ref<'ltr' | 'rtl'>('ltr')
const updateTextDirection = useDebounceFn((content: string) => {
  if (!content.trim()) {
    textDirection.value = 'ltr'
    return
  }
  const sample = content.trim().substring(0, 100)
  const rtlRegex = /[\u0590-\u05FF\u0600-\u06FF]/
  textDirection.value = rtlRegex.test(sample) ? 'rtl' : 'ltr'
}, 300)

watch(internalValue, updateTextDirection, { immediate: true })
</script>
```

## Critical Rules

| Rule | Correct | Wrong |
|------|---------|-------|
| Disable auto-convert | `enableInputRules: false` | Omitting this option |
| Cleanup | `onBeforeUnmount(() => editor.value?.destroy())` | No cleanup |
| Check editor exists | `editor?.chain()` | `editor.chain()` |
| External sync | Compare before setting | Always setContent |

## Key Configuration Options

```typescript
useEditor({
  content: '', // Initial HTML content
  extensions: [...], // Array of extensions

  // INPUT BEHAVIOR
  enableInputRules: false, // DISABLE auto-conversion (e.g., - to bullet)
  enablePasteRules: true,  // KEEP paste formatting

  // CALLBACKS
  onUpdate: ({ editor }) => { /* emit changes */ },
  onFocus: ({ editor }) => { /* handle focus */ },
  onBlur: ({ editor }) => { /* handle blur */ },
})
```

## Toolbar Command Patterns

```typescript
// Toggle formatting
editor.chain().focus().toggleBold().run()
editor.chain().focus().toggleItalic().run()
editor.chain().focus().toggleStrike().run()

// Lists
editor.chain().focus().toggleBulletList().run()
editor.chain().focus().toggleOrderedList().run()
editor.chain().focus().toggleTaskList().run()

// History
editor.chain().focus().undo().run()
editor.chain().focus().redo().run()

// Check if can do action
editor.can().undo()
editor.can().redo()

// Check active state
editor.isActive('bold')
editor.isActive('bulletList')
```

## Styling the Editor

```css
/* Basic Tiptap styles */
:deep(.tiptap) {
  outline: none;
  min-height: 100px;
}

:deep(.tiptap p) {
  margin: 0 0 0.5em 0;
}

/* Task list styling */
:deep(.tiptap ul[data-type="taskList"]) {
  list-style: none;
  padding-left: 0;
}

:deep(.tiptap ul[data-type="taskList"] li) {
  display: flex;
  align-items: flex-start;
  gap: 0.5em;
}

:deep(.tiptap ul[data-type="taskList"] li > label input[type="checkbox"]) {
  cursor: pointer;
  width: 16px;
  height: 16px;
}

/* Links */
:deep(.tiptap a) {
  color: var(--primary-400);
  text-decoration: underline;
}
```

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Auto-conversion on typing | Add `enableInputRules: false` |
| Editor not cleaning up | Add `onBeforeUnmount(() => editor.value?.destroy())` |
| Changes not emitting | Use `onUpdate` callback |
| External value not syncing | Watch prop and use `setContent()` |

## Quick Test Checklist

After setup, verify:
1. Type `-` → stays as `-` (no auto-bullet)
2. Type `- [ ]` → stays as text (no auto-conversion)
3. Click Task List button → creates proper checkbox
4. Click Bold button → toggles bold
5. Check console → no errors

## Comparison: With vs Without Input Rules

```typescript
// WITH enableInputRules: true (DEFAULT - causes problems)
// Type: - <space>
// Result: Auto-converts to bullet list immediately!
// User can't type "- [ ]" for task list

// WITH enableInputRules: false (RECOMMENDED)
// Type: - <space>
// Result: Stays as "- " text
// User CAN type "- [ ]" freely
// Use toolbar buttons for formatting instead
```

## Reference Implementation

See working implementation at:
- `src/components/common/TiptapEditor.vue`
- `src/components/common/MarkdownEditor.vue`
