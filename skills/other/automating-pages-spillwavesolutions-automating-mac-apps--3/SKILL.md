---
name: automating-pages
description: Automates Apple Pages using JXA with AppleScript dictionary discovery. Use when asked to "automate Pages documents", "create documents programmatically", "JXA Pages scripting", or "export Pages to PDF". Covers documents, templates, text, styles, export, tables, images, and AppleScript bridge fallbacks.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Automating Pages (JXA-first, AppleScript discovery)

## Relationship to the macOS automation skill
- Standalone for Pages, aligned with `automating-mac-apps` patterns.
- Use `automating-mac-apps` for permissions, shell, and UI scripting guidance.
- **PyXA Installation:** To use PyXA examples in this skill, see the installation instructions in `automating-mac-apps` skill (PyXA Installation section).

## Core framing
- Pages dictionary is AppleScript-first; discover there.
- JXA provides the logic and data handling.
- **Objects are specifiers**: References to Pages elements that require methods for reads (e.g., `doc.body.text()`) and assignments for writes (e.g., `doc.body.text = 'new text'`).

### Example: Create Document
```javascript
const pages = Application('Pages');
const doc = pages.Document({templateName: 'Blank'});
pages.documents.push(doc);
doc.body.text = "Hello World";
```

## Workflow (default)
1) **Discover**: Open Script Editor > File > Open Dictionary > Pages.
2) **Prototype**: Write minimal AppleScript to verify the command works.
3) **Port to JXA**: Convert AppleScript syntax to JXA objects.
   - Example: `make new document` becomes `pages.documents.push(pages.Document())`.
   - Add error handling (try/catch blocks).
4) **Optimize**: Use batch text operations when possible to avoid performance penalties.
5) **Fallback**: Use AppleScript bridge or UI scripting for dictionary gaps (e.g., specific layout changes).

## Image Insertion (Critical Difference from Keynote)

**IMPORTANT**: Pages does **NOT** support direct image insertion like Keynote does:
```javascript
// THIS WORKS IN KEYNOTE:
Keynote.Image({ file: Path("/path/to/image.png"), position: {x: 100, y: 100} });

// THIS DOES NOT WORK IN PAGES!
Pages.Image({ file: Path("/path/to/image.png") }); // ❌ Will fail
```

**Solution**: Use ObjC Pasteboard bridging (see `pages-advanced.md` for details):
```javascript
ObjC.import('AppKit');
const nsImage = $.NSImage.alloc.initWithContentsOfFile("/path/to/image.png");
const pb = $.NSPasteboard.generalPasteboard;
pb.clearContents;
pb.setDataForType(nsImage.TIFFRepresentation, $.NSPasteboardTypeTIFF);
// Then use System Events to paste (Cmd+V)
```

**Example Script**: See `automating-pages/scripts/insert_images.js` for a complete working example.

## Common Pitfalls
- **Image insertion**: Pages lacks a native `Image` constructor unlike Keynote. Use ObjC Pasteboard method.
- **Dictionary gaps**: Some features (like sophisticated layout adjustments) aren't in the dictionary. Use the AppleScript bridge or UI scripting.
- **Permissions**: Ensure 'Accessibility' settings are enabled for UI scripting.
- **Saving**: Always use `doc.save({in: file_path})` with a valid path object.

## Validation Checklist
- [ ] Document opens without errors
- [ ] Text insertion and formatting succeeds
- [ ] Save operations complete with valid path objects
- [ ] Template application works if used
- [ ] Export to target format produces valid output (PDF, Word)
- [ ] Error handling covers missing files and permissions

## When Not to Use
- Cross-platform document automation (use python-docx or pandoc)
- AppleScript alone suffices (skip JXA complexity)
- Web-based documents (Google Docs API)
- Non-macOS platforms
- Complex page layout requiring manual design tools

## What to load
### Level 1: Basics
- JXA Pages basics: `automating-pages/references/pages-basics.md` (Core objects and document lifecycle)

### Level 2: Recipes & Common Tasks
- Recipes (templates, export, text): `automating-pages/references/pages-recipes.md` (Standard operations)
- Export options matrix: `automating-pages/references/pages-export-matrix.md` (PDF, Word, ePub formats)
- Template strategy: `automating-pages/references/pages-template-strategy.md` (Managing custom templates)

### Level 3: Advanced
- Advanced patterns (tables, images, AppleScript bridge): `automating-pages/references/pages-advanced.md` (Complex integrations)
- UI scripting patterns: `automating-pages/references/pages-ui-scripting.md` (Fallbacks)
- Dictionary translation table: `automating-pages/references/pages-dictionary.md` (AppleScript to JXA mapping)
- PyXA (Python) alternative: `automating-pages/references/pages-pyxa.md`

### Example Scripts
- Image insertion: `automating-pages/scripts/insert_images.js` (ObjC Pasteboard method for inserting images)