---
name: ui-design
description: Extract UI and content organization entities from narrative text. Use when analyzing player choices, flowcharts, handouts, tokenboards, tags, templates, and notes.
---
# ui-design

Domain skill for UI Content Specialist. Specific extraction rules and expertise.

## Domain Expertise

- **User interfaces**: Menus, dialogs, choice systems
- **Flowcharts**: Story branching, dialogue trees, quest flow
- **Handouts**: Game materials, player notes, reference documents
- **Tokenboards**: Combat tokens, initiative tracking, game pieces
- **Content organization**: Tags, templates, note-taking systems
- **Inspiration systems**: Creative prompts, idea generation
- **Player tools**: In-game note-taking, journaling

## Entity Types (8 total)

- **choice** - Player choices
- **flowchart** - Flowcharts
- **handout** - Handouts
- **tokenboard** - Tokenboards
- **tag** - Tags
- **template** - Templates
- **inspiration** - Inspiration
- **note** - Notes

## Processing Guidelines

When extracting UI and content entities from chapter text:

1. **Identify UI/content elements**:
   - Player choices or dialog options
   - Quest flow or branching paths
   - Handouts or materials given to players
   - Tokenboards or combat systems
   - Tags or organizational systems
   - Templates or reusable formats
   - Notes or journals mentioned

2. **Extract UI/content details**:
   - Choice options and consequences
   - Flowchart structure and branches
   - Handout content and format
   - Tokenboard layout and pieces
   - Tag categories and usage
   - Template types and purposes
   - Note content and organization

3. **Analyze UI/content context**:
   - Player agency (meaningful vs illusion of choice)
   - Information presentation (clear vs confusing)
   - Tool utility (helpful vs cumbersome)
   - Content reusability

4. **Create schema-compliant entities** with proper JSON structure

## Key Considerations

- **Player agency**: Choices should feel meaningful
- **Clarity**: UI should be intuitive and clear
- **Accessibility**: Information should be easy to find and reference
- **Organization**: Tags and templates help manage content
- **Flexibility**: Templates should allow customization
