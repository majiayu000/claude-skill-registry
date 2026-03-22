---
name: worldbuilding
description: This skill should be used when the user asks to "create a location", "add a location", "magic system", "political system", "build the world", "add culture", "world history", "technology system", "religion", "economy", or wants to develop any aspect of a story's world and setting.
---

# Worldbuilding

## Overview

Create and manage world elements for a story project. Locations and systems (magic, politics, technology, etc.) are stored as markdown files in the `worldbuilding/` directory with YAML frontmatter. All elements cross-reference characters and other story elements.

## Prerequisites

A story project must already exist (created via the story-init skill). Verify by checking for `story.md` in the project root.

## Creating a Location

1. Read `story.md` for genre, era, and tone context
2. Read `worldbuilding/_index.md` for existing locations and systems
3. Ask for the location's name and type (city, fortress, wilderness, etc.)
4. Build the location through conversation, covering:
   - Physical description and atmosphere
   - History relevant to the story
   - Culture and customs of inhabitants
   - Notable features characters will interact with
   - Current state at story's timeline
5. Write the file using `references/location-template.md`
6. Save to `worldbuilding/locations/{name-kebab}.md`
7. Update `worldbuilding/_index.md` locations table
8. If notable characters are listed, verify those character files exist and add location references to them

## Creating a System

1. Read `story.md` for genre and themes context
2. Read `worldbuilding/_index.md` for existing systems
3. Identify the system type and consult `references/world-element-types.md` for the relevant prompts
4. Build the system through conversation, addressing the key questions for that type
5. Write the file using `references/system-template.md`
6. Save to `worldbuilding/systems/{name-kebab}.md`
7. Update `worldbuilding/_index.md` systems table
8. Cross-reference with characters who interact with the system (e.g., magic-users for a magic system)

## Updating World Elements

1. Read the existing file
2. Make the requested changes
3. If cross-references changed, update the linked files
4. Update `worldbuilding/_index.md` if name, type, or status changed

## Cross-Referencing

- Locations reference characters via `notable-characters` in frontmatter
- Systems reference practitioners via character tags
- When a location is used in a chapter, the chapter's frontmatter `locations` field links back
- Keep the `worldbuilding/_index.md` world overview section current as elements are added

## Reference Files

- **`references/location-template.md`** - Template for location files
- **`references/system-template.md`** - Template for system files
- **`references/world-element-types.md`** - Detailed prompts for each system type (magic, political, technology, religion, economic, military, social)
