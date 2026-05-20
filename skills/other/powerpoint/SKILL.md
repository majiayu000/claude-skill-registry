---
name: powerpoint
description: Create and manipulate Microsoft PowerPoint presentations (.pptx files). Use for creating slides, presentations, pitch decks, and visual content with text, bullets, tables, and charts.
allowed-tools: Read, Write, Bash
---

# PowerPoint Presentation Tool

This skill enables creating and manipulating Microsoft PowerPoint presentations using Node.js tools.

## Capabilities

- **Create** new presentations from scratch with multiple slides
- **Add slides** with different layouts (title, content, section, blank)
- **Insert text** including titles, subtitles, and bullet points
- **Add tables** with headers and data rows
- **Create charts** (bar, line, pie) from data
- **Insert images** at specific positions and sizes
- **Apply formatting** with fonts, colors, and positioning

## When to Use

Invoke this skill when the user:
- Mentions PowerPoint, presentations, slides, or .pptx files
- Asks to create a presentation, pitch deck, or slideshow
- Needs to visualize information in slide format
- Wants to create slides from outlines or data
- Asks for visual presentations or reports

## How to Use

The PowerPoint tool is implemented at `src/tools/powerpoint-tool.ts`. Invoke using the Bash tool:

### Creating a Presentation
```bash
ts-node src/tools/powerpoint-tool.ts create "/path/to/presentation.pptx" '{"title":"My Presentation","slides":[{"type":"title","title":"Welcome","subtitle":"Introduction"}]}'
```

### Creating from Outline
```bash
ts-node src/tools/powerpoint-tool.ts outline "/path/to/presentation.pptx" '{"title":"Product Launch","slides":[{"title":"Overview","points":["Point 1","Point 2"]}]}'
```

## JSON Structure for Creating Presentations

### Full Structure
```json
{
  "title": "Presentation Title",
  "author": "Author Name",
  "slides": [
    {
      "type": "title",
      "title": "Main Title",
      "subtitle": "Subtitle Text"
    },
    {
      "type": "content",
      "title": "Slide Title",
      "content": ["Bullet 1", "Bullet 2", "Bullet 3"]
    },
    {
      "type": "section",
      "title": "Section Header"
    }
  ]
}
```

### Outline Format (Simpler)
```json
{
  "title": "Presentation Title",
  "slides": [
    {
      "title": "Slide 1 Title",
      "points": ["Point 1", "Point 2"]
    }
  ]
}
```

## Implementation

Uses the `pptxgenjs` npm library for PowerPoint file generation.
