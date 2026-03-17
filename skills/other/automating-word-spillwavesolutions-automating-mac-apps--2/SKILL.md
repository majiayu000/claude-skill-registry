---
name: automating-word
description: Automates Microsoft Word via JXA with AppleScript dictionary discovery. Use when asked to "automate Word documents", "find and replace in Word", "JXA Word scripting", or "create Word documents programmatically". Covers documents, ranges, find/replace, tables, export, and ObjC bridge patterns.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Automating Word (JXA-first, AppleScript discovery)

## Relationship to the macOS automation skill
- Standalone for Word, aligned with `automating-mac-apps` patterns.
- Use `automating-mac-apps` skill for permissions, shell execution, and UI scripting guidance.
- **PyXA Installation:** To use PyXA examples in this skill, see the installation instructions in `automating-mac-apps` skill (PyXA Installation section).

## Core framing
- Word dictionary is AppleScript-first; discover there.
- JXA provides logic, data handling, and ObjC bridge access.
- Objects are specifiers; read via methods, write via assignments.
- Handle errors from Word operations using try/catch blocks and Application error checking.

## Implementation Workflow
1. **Discover AppleScript Dictionary:** Open Script Editor, browse Word's AppleScript dictionary to understand available objects and methods.
2. **Translate to JXA:** Use discovered AppleScript syntax as reference for JXA equivalents, consulting the dictionary translation table.
3. **Set Up JXA Script:** Initialize Word application object and document references.
4. **Implement Operations:** Apply find/replace, table manipulation, or export using JXA methods.
5. **Test and Validate:** Run script and verify document changes match expectations.

## Quick Examples

**Document opening:**
```javascript
// JXA
const word = Application('Microsoft Word');
word.documents.open('/path/to/document.docx');
```
```python
# PyXA (Recommended)
import PyXA
word = PyXA.Word()
word.documents().open("/path/to/document.docx")
```

**Find and replace:**
```javascript
// JXA
const range = word.activeDocument.content;
range.find.text = 'old text';
range.find.replacement.text = 'new text';
range.find.execute({replace: 'all'});
```
```python
# PyXA
doc = word.active_document()
find_obj = doc.content().find()
find_obj.text = 'old text'
find_obj.replacement.text = 'new text'
find_obj.execute(replace='all')
```

**Table creation:**
```javascript
// JXA
const table = word.activeDocument.tables.add(word.activeDocument.content, 3, 4);
table.cell(1, 1).range.text = 'Header';
```
```python
# PyXA
table = doc.tables().add(doc.content(), 3, 4)
table.cell(1, 1).range().text = 'Header'
```

For PyObjC Scripting Bridge examples, see `automating-word/references/word-pyxa.md`.

## Validation Checklist
After implementing Word automation:
- [ ] Test script execution without errors
- [ ] Verify document changes applied correctly
- [ ] Check ObjC bridge objects return expected values
- [ ] Run find/replace operations and confirm replacements
- [ ] Export documents and validate output formats

## When Not to Use
- For general macOS automation (use `automating-mac-apps`)
- For Excel automation (use `automating-excel`)
- For non-Microsoft Office applications
- For web-based document processing (use web APIs or Playwright)

## What to load
- Word JXA basics: `automating-word/references/word-basics.md` (core concepts only; see references for advanced usage)
- Recipes (ranges, find/replace, tables): `automating-word/references/word-recipes.md`
- Advanced patterns (export enums, ObjC bridge): `automating-word/references/word-advanced.md`
- Dictionary translation table: `automating-word/references/word-dictionary.md`
- PyXA (Python) alternative: `automating-word/references/word-pyxa.md`