---
name: word-processor-expert
description: Expert guide for building professional word processors with Tiptap/ProseMirror. Use for text editor features, document formatting, export functionality, and achieving Word/Pages/Docs feature parity.
---

# Word Processor Expert Skill

## Overview

This skill provides rapid guidance for implementing professional word processor features in id8composer using Tiptap (ProseMirror). Get you to Microsoft Word, Apple Pages, and Google Docs quality with modern web technologies.

## Current Stack (id8composer)

- **Editor**: Tiptap v3.10.7 (ProseMirror-based)
- **Framework**: Next.js 15.5.6 + React 19
- **State**: Zustand
- **Export**: `docx` v9.5.1, `jspdf` v3.0.3

## Quick Reference: Missing Features

### ❌ Not Yet Implemented
- Text alignment (left/center/right/justify)
- Font family/size controls
- Heading styles (H1-H6 with styling)
- Line spacing (1.0, 1.5, 2.0)
- Paragraph spacing
- Indentation controls
- Find & Replace
- Page breaks
- Headers/Footers
- Page setup (margins, orientation)
- Proper DOCX/PDF export
- Styles/Templates
- Comments/Track changes

### ✅ Already Working
- Bold, italic, underline
- Lists (bullet, ordered)
- Tables
- Images, links
- Color & highlight
- Undo/Redo
- Auto-save
- Character/word count

## Essential Tiptap Extensions

### Install Missing Extensions

```bash
npm install @tiptap/extension-text-align
npm install @tiptap/extension-font-family
npm install @tiptap/extension-heading
npm install @tiptap/extension-hard-break
```

### Text Alignment

```typescript
// Add to editor extensions
import { TextAlign } from '@tiptap/extension-text-align'

const editor = useEditor({
  extensions: [
    TextAlign.configure({
      types: ['heading', 'paragraph'],
      alignments: ['left', 'center', 'right', 'justify'],
      defaultAlignment: 'left',
    }),
    // ... other extensions
  ],
})

// Toolbar buttons
<button onClick={() => editor.chain().focus().setTextAlign('left').run()}>
  <AlignLeft />
</button>
<button onClick={() => editor.chain().focus().setTextAlign('center').run()}>
  <AlignCenter />
</button>
<button onClick={() => editor.chain().focus().setTextAlign('right').run()}>
  <AlignRight />
</button>
<button onClick={() => editor.chain().focus().setTextAlign('justify').run()}>
  <AlignJustify />
</button>
```

### Font Family & Size

```typescript
import { FontFamily } from '@tiptap/extension-font-family'
import { TextStyle } from '@tiptap/extension-text-style' // Already installed

// Custom Font Size extension
import { Extension } from '@tiptap/core'

export const FontSize = Extension.create({
  name: 'fontSize',

  addOptions() {
    return {
      types: ['textStyle'],
    }
  },

  addGlobalAttributes() {
    return [
      {
        types: this.options.types,
        attributes: {
          fontSize: {
            default: null,
            parseHTML: element => element.style.fontSize.replace('px', ''),
            renderHTML: attributes => {
              if (!attributes.fontSize) return {}
              return {
                style: `font-size: ${attributes.fontSize}px`,
              }
            },
          },
        },
      },
    ]
  },

  addCommands() {
    return {
      setFontSize: (fontSize: string) => ({ chain }) => {
        return chain().setMark('textStyle', { fontSize }).run()
      },
      unsetFontSize: () => ({ chain }) => {
        return chain().setMark('textStyle', { fontSize: null }).run()
      },
    }
  },
})

// Usage in editor
const editor = useEditor({
  extensions: [
    TextStyle, // Required
    FontFamily.configure({
      types: ['textStyle'],
    }),
    FontSize,
    // ...
  ],
})

// Dropdowns in toolbar
<select onChange={(e) => editor.chain().focus().setFontFamily(e.target.value).run()}>
  <option value="Arial">Arial</option>
  <option value="Times New Roman">Times New Roman</option>
  <option value="Courier New">Courier New</option>
  <option value="Georgia">Georgia</option>
</select>

<select onChange={(e) => editor.chain().focus().setFontSize(e.target.value).run()}>
  <option value="12">12pt</option>
  <option value="14">14pt</option>
  <option value="16">16pt</option>
  <option value="18">18pt</option>
  <option value="24">24pt</option>
</select>
```

### Line Spacing

```typescript
// Custom Line Height extension
import { Extension } from '@tiptap/core'

export const LineHeight = Extension.create({
  name: 'lineHeight',

  addOptions() {
    return {
      types: ['paragraph', 'heading'],
      defaultLineHeight: '1.5',
    }
  },

  addGlobalAttributes() {
    return [
      {
        types: this.options.types,
        attributes: {
          lineHeight: {
            default: this.options.defaultLineHeight,
            parseHTML: element => element.style.lineHeight || this.options.defaultLineHeight,
            renderHTML: attributes => {
              if (!attributes.lineHeight) return {}
              return { style: `line-height: ${attributes.lineHeight}` }
            },
          },
        },
      },
    ]
  },

  addCommands() {
    return {
      setLineHeight: (lineHeight: string) => ({ commands }) => {
        return this.options.types.every((type: string) =>
          commands.updateAttributes(type, { lineHeight })
        )
      },
    }
  },
})

// Toolbar dropdown
<select onChange={(e) => editor.chain().focus().setLineHeight(e.target.value).run()}>
  <option value="1.0">Single</option>
  <option value="1.15">1.15</option>
  <option value="1.5">1.5</option>
  <option value="2.0">Double</option>
</select>
```

### Indentation

```typescript
// Install @tiptap/extension-indent if available, or create custom
export const Indent = Extension.create({
  name: 'indent',

  addOptions() {
    return {
      types: ['paragraph', 'heading'],
      minIndent: 0,
      maxIndent: 10,
    }
  },

  addGlobalAttributes() {
    return [
      {
        types: this.options.types,
        attributes: {
          indent: {
            default: 0,
            parseHTML: element => {
              const indent = element.style.paddingLeft
              return indent ? parseInt(indent) / 40 : 0
            },
            renderHTML: attributes => {
              if (!attributes.indent) return {}
              return { style: `padding-left: ${attributes.indent * 40}px` }
            },
          },
        },
      },
    ]
  },

  addCommands() {
    return {
      indent: () => ({ commands, state }) => {
        const { indent = 0 } = state.selection.$from.node().attrs
        if (indent >= this.options.maxIndent) return false
        return this.options.types.every((type: string) =>
          commands.updateAttributes(type, { indent: indent + 1 })
        )
      },
      outdent: () => ({ commands, state }) => {
        const { indent = 0 } = state.selection.$from.node().attrs
        if (indent <= this.options.minIndent) return false
        return this.options.types.every((type: string) =>
          commands.updateAttributes(type, { indent: indent - 1 })
        )
      },
    }
  },

  addKeyboardShortcuts() {
    return {
      Tab: () => this.editor.commands.indent(),
      'Shift-Tab': () => this.editor.commands.outdent(),
    }
  },
})

// Toolbar buttons
<button onClick={() => editor.chain().focus().indent().run()}>
  <IndentIncrease />
</button>
<button onClick={() => editor.chain().focus().outdent().run()}>
  <IndentDecrease />
</button>
```

### Page Breaks

```typescript
// Custom Page Break node
import { Node, mergeAttributes } from '@tiptap/core'

export const PageBreak = Node.create({
  name: 'pageBreak',
  group: 'block',
  parseHTML() {
    return [{ tag: 'div.page-break' }]
  },
  renderHTML({ HTMLAttributes }) {
    return ['div', mergeAttributes(HTMLAttributes, { class: 'page-break' }), ['hr']]
  },
  addCommands() {
    return {
      setPageBreak: () => ({ commands }) => {
        return commands.insertContent({ type: this.name })
      },
    }
  },
})

// CSS for page breaks
/* styles/editor.css */
.page-break {
  page-break-after: always;
  break-after: page;
  margin: 2rem 0;
  border: none;
  border-top: 2px dashed #ccc;
  text-align: center;
}

.page-break::after {
  content: "Page Break";
  display: inline-block;
  position: relative;
  top: -0.7em;
  padding: 0 1em;
  background: white;
  color: #999;
  font-size: 0.8em;
}

// Toolbar button
<button onClick={() => editor.chain().focus().setPageBreak().run()}>
  Insert Page Break
</button>
```

### Find & Replace

```typescript
'use client'
import { useState } from 'react'

export function FindReplace({ editor }: { editor: Editor }) {
  const [searchTerm, setSearchTerm] = useState('')
  const [replaceTerm, setReplaceTerm] = useState('')
  const [caseSensitive, setCaseSensitive] = useState(false)

  const findNext = () => {
    const content = editor.getText()
    const flags = caseSensitive ? 'g' : 'gi'
    const regex = new RegExp(searchTerm, flags)
    const matches = [...content.matchAll(regex)]

    if (matches.length > 0) {
      // Highlight first match
      const match = matches[0]
      // Implementation: Use Tiptap's TextSelection to highlight
    }
  }

  const replaceNext = () => {
    const { from, to } = editor.state.selection
    const selectedText = editor.state.doc.textBetween(from, to)

    if (selectedText === searchTerm || (!caseSensitive && selectedText.toLowerCase() === searchTerm.toLowerCase())) {
      editor.chain().focus().insertContentAt({ from, to }, replaceTerm).run()
      findNext()
    }
  }

  const replaceAll = () => {
    const content = editor.getHTML()
    const flags = caseSensitive ? 'g' : 'gi'
    const regex = new RegExp(searchTerm, flags)
    const newContent = content.replace(regex, replaceTerm)
    editor.commands.setContent(newContent)
  }

  return (
    <div className="flex gap-2 p-4 border rounded">
      <input
        type="text"
        placeholder="Find"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="border px-2 py-1"
      />
      <input
        type="text"
        placeholder="Replace"
        value={replaceTerm}
        onChange={(e) => setReplaceTerm(e.target.value)}
        className="border px-2 py-1"
      />
      <label className="flex items-center gap-1">
        <input
          type="checkbox"
          checked={caseSensitive}
          onChange={(e) => setCaseSensitive(e.target.checked)}
        />
        Case sensitive
      </label>
      <button onClick={findNext} className="px-3 py-1 bg-blue-500 text-white rounded">
        Find Next
      </button>
      <button onClick={replaceNext} className="px-3 py-1 bg-blue-500 text-white rounded">
        Replace
      </button>
      <button onClick={replaceAll} className="px-3 py-1 bg-red-500 text-white rounded">
        Replace All
      </button>
    </div>
  )
}
```

## Professional DOCX Export

```typescript
import { Document, Paragraph, TextRun, HeadingLevel, AlignmentType, Packer } from 'docx'
import { saveAs } from 'file-saver'

export async function exportToDocx(editor: Editor, filename: string) {
  // Convert Tiptap JSON to DOCX structure
  const doc = new Document({
    sections: [{
      properties: {},
      children: convertTiptapToDocx(editor.getJSON()),
    }],
  })

  const blob = await Packer.toBlob(doc)
  saveAs(blob, `${filename}.docx`)
}

function convertTiptapToDocx(tiptapJson: any): Paragraph[] {
  const paragraphs: Paragraph[] = []

  tiptapJson.content?.forEach((node: any) => {
    if (node.type === 'paragraph') {
      const runs: TextRun[] = []

      node.content?.forEach((inline: any) => {
        if (inline.type === 'text') {
          runs.push(new TextRun({
            text: inline.text,
            bold: inline.marks?.some((m: any) => m.type === 'bold'),
            italics: inline.marks?.some((m: any) => m.type === 'italic'),
            underline: inline.marks?.some((m: any) => m.type === 'underline') ? {} : undefined,
            color: inline.marks?.find((m: any) => m.type === 'textStyle')?.attrs?.color?.replace('#', ''),
            size: parseInt(inline.marks?.find((m: any) => m.type === 'textStyle')?.attrs?.fontSize || '24') * 2, // Half-points
          }))
        }
      })

      paragraphs.push(new Paragraph({
        children: runs,
        alignment: getAlignment(node.attrs?.textAlign),
        spacing: {
          before: 120,
          after: 120,
          line: parseInt(node.attrs?.lineHeight || '1.5') * 240,
        },
        indent: {
          left: (node.attrs?.indent || 0) * 720, // Twips (1/20th of a point)
        },
      }))
    } else if (node.type === 'heading') {
      paragraphs.push(new Paragraph({
        text: node.content?.[0]?.text || '',
        heading: getHeadingLevel(node.attrs?.level),
        alignment: getAlignment(node.attrs?.textAlign),
      }))
    }
  })

  return paragraphs
}

function getAlignment(align: string): AlignmentType {
  switch (align) {
    case 'left': return AlignmentType.LEFT
    case 'center': return AlignmentType.CENTER
    case 'right': return AlignmentType.RIGHT
    case 'justify': return AlignmentType.JUSTIFIED
    default: return AlignmentType.LEFT
  }
}

function getHeadingLevel(level: number): HeadingLevel {
  const levels = [
    HeadingLevel.HEADING_1,
    HeadingLevel.HEADING_2,
    HeadingLevel.HEADING_3,
    HeadingLevel.HEADING_4,
    HeadingLevel.HEADING_5,
    HeadingLevel.HEADING_6,
  ]
  return levels[level - 1] || HeadingLevel.HEADING_1
}
```

## Professional PDF Export

```typescript
import jsPDF from 'jspdf'

export function exportToPdf(editor: Editor, filename: string) {
  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'pt',
    format: 'letter',
  })

  const content = editor.getHTML()

  // Convert HTML to PDF (basic approach)
  // For production, consider using html2pdf or server-side rendering
  doc.html(content, {
    callback: (doc) => {
      doc.save(`${filename}.pdf`)
    },
    margin: [72, 72, 72, 72], // 1 inch margins
    x: 72,
    y: 72,
    width: 468, // 6.5 inches at 72 DPI
    windowWidth: 816, // 8.5 inches at 96 DPI
  })
}

// Better approach: Server-side with Puppeteer
// app/api/export-pdf/route.ts
import puppeteer from 'puppeteer'

export async function POST(req: Request) {
  const { html } = await req.json()

  const browser = await puppeteer.launch()
  const page = await browser.newPage()

  await page.setContent(html, { waitUntil: 'networkidle0' })

  const pdf = await page.pdf({
    format: 'letter',
    margin: {
      top: '1in',
      right: '1in',
      bottom: '1in',
      left: '1in',
    },
    printBackground: true,
  })

  await browser.close()

  return new Response(pdf, {
    headers: {
      'Content-Type': 'application/pdf',
      'Content-Disposition': 'attachment; filename=document.pdf',
    },
  })
}
```

## Print Layout View

```typescript
// Print-friendly CSS
/* styles/print-layout.css */
@media print {
  @page {
    size: letter;
    margin: 1in;
  }

  .editor-content {
    font-family: 'Times New Roman', serif;
    font-size: 12pt;
    line-height: 1.5;
  }

  .page-break {
    page-break-after: always;
  }

  .no-print {
    display: none;
  }
}

/* Print preview mode */
.print-preview .editor-content {
  width: 8.5in;
  min-height: 11in;
  margin: 0 auto;
  padding: 1in;
  background: white;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.print-preview .page {
  width: 8.5in;
  height: 11in;
  margin-bottom: 0.5in;
  background: white;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  page-break-after: always;
}
```

## Keyboard Shortcuts Reference

```typescript
// Add to editor configuration
const editor = useEditor({
  editorProps: {
    handleKeyDown: (view, event) => {
      // Cmd/Ctrl + B: Bold
      // Cmd/Ctrl + I: Italic
      // Cmd/Ctrl + U: Underline
      // Cmd/Ctrl + E: Center align
      // Cmd/Ctrl + L: Left align
      // Cmd/Ctrl + R: Right align
      // Cmd/Ctrl + J: Justify
      // Cmd/Ctrl + F: Find
      // Cmd/Ctrl + H: Replace
      // Cmd/Ctrl + S: Save
      // Cmd/Ctrl + P: Print
      // Cmd/Ctrl + Z: Undo
      // Cmd/Ctrl + Y: Redo
      // Tab: Increase indent
      // Shift+Tab: Decrease indent

      return false // Let Tiptap handle defaults
    },
  },
})
```

## Performance Optimization

```typescript
// Virtual scrolling for large documents
import { FixedSizeList } from 'react-window'

// Debounced auto-save
import { useDebouncedCallback } from 'use-debounce'

const debouncedSave = useDebouncedCallback(
  (content) => {
    // Save to backend
    saveDocument(content)
  },
  2000 // 2 second delay
)

// Lazy load heavy extensions
const editor = useEditor({
  extensions: [
    StarterKit,
    // Conditionally load based on feature flags
    ...(features.tables ? [Table, TableRow, TableCell] : []),
    ...(features.images ? [Image] : []),
  ],
})
```

## When to Use This Skill

Invoke this skill when you need:
- Quick implementation of text editor features
- Tiptap extension examples
- Document export functionality (DOCX/PDF)
- Formatting toolbar patterns
- Keyboard shortcuts
- Print layout CSS
- Performance tips for large documents
- Word processor feature parity

For deep architectural work, use the **text-editor-architect** agent instead.
