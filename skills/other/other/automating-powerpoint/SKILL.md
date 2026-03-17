---
name: automating-powerpoint
description: Automates Microsoft PowerPoint via JXA with AppleScript dictionary discovery. Use when asked to "automate PowerPoint presentations", "create slides programmatically", "JXA PowerPoint scripting", or "export PowerPoint to PDF". Covers presentations, slides, shapes, text, tables, export enums, and interop with Excel.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Automating PowerPoint (JXA-first, AppleScript discovery)

## Relationship to the macOS automation skill
- Standalone for PowerPoint, aligned with `automating-mac-apps` patterns.
- Use `automating-mac-apps` for permissions, shell, and UI scripting guidance.

## Core Framing
- PowerPoint dictionary is AppleScript-first; discover there.
- JXA provides logic, data handling, and ObjC bridge access.
- Objects are specifiers; read via methods, write via assignments.
- **Prerequisites:** PowerPoint with Accessibility permissions, basic JXA/AppleScript knowledge.

## Workflow (default)
1) Discover dictionary terms in Script Editor (PowerPoint).
2) Prototype minimal AppleScript commands.
3) Port to JXA and add defensive checks.
4) Use explicit enums for save/export formats.
5) Use Excel interop for robust charting.

## Quick Start Example
Create a new presentation with a title slide:
```javascript
const powerpoint = Application('Microsoft PowerPoint');
const doc = powerpoint.documents[0] || powerpoint.documents.add();
const slide = doc.slides.add({index: 1, layout: powerpoint.slideLayouts['ppLayoutTitle']});
slide.shapes[0].textFrame.textRange.content = 'My Presentation';
doc.save({in: Path('/Users/username/Desktop/presentation.pptx')});
```

## Troubleshooting
- **Application not responding:** Ensure PowerPoint is launched and accessible via Accessibility permissions.
- **Dictionary discovery fails:** Open PowerPoint manually first, then retry Script Editor.
- **Export errors:** Verify file paths exist and use absolute paths; check enum values match PowerPoint's export constants.
- **Interop issues:** Confirm Excel is installed and both applications have proper permissions.

## Validation Checklist
- [ ] PowerPoint launches and responds to JXA commands
- [ ] Presentation creation succeeds with expected slides
- [ ] Shape/text manipulation renders correctly
- [ ] Export produces valid output files
- [ ] Enum values match PowerPoint dictionary constants
- [ ] Error handling covers missing app/permissions

## When Not to Use
- Windows PowerPoint automation (use VBA instead)
- Web-based PowerPoint (use Office 365 APIs)
- Complex animations or transitions (limited JXA support)
- Non-macOS platforms
- Real-time presentation collaboration scenarios

## What to load
- PowerPoint JXA basics: `automating-powerpoint/references/powerpoint-basics.md` (core objects, application setup)
- Recipes (slides, shapes, text): `automating-powerpoint/references/powerpoint-recipes.md`
- Advanced patterns (export enums, charts): `automating-powerpoint/references/powerpoint-advanced.md`
- Dictionary translation table: `automating-powerpoint/references/powerpoint-dictionary.md`
- Charting notes: `automating-powerpoint/references/powerpoint-charts.md`
- Export to video notes: `automating-powerpoint/references/powerpoint-export-video.md`
- Excel chart copy example: `automating-powerpoint/references/powerpoint-chart-copy.md`
- Layout presets: `automating-powerpoint/references/powerpoint-layouts.md`
- Export video workflow: `automating-powerpoint/references/powerpoint-export-video-steps.md`
- Deck generator example: `automating-powerpoint/references/powerpoint-deck-generator.md`
- Chart-aware deck pattern: `automating-powerpoint/references/powerpoint-chart-aware-deck.md`