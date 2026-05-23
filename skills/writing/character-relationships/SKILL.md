---
name: character-relationships
description: Analyze story character relationships, identify types, characteristics, and development changes. Suitable for deeply understanding character relationship networks, analyzing the plot-driving role of relationships, and providing relationship support for plot design
category: character-analysis
version: 2.1.0
last_updated: 2026-01-11
license: MIT
compatibility: Claude Code 1.0+
maintainer: Gong Fan
allowed-tools:
  - Read
model: opus
changelog:
  - version: 2.1.0
    date: 2026-01-11
    changes:
      - type: improved
        content: Optimized description field to be more concise and comply with imperative language specifications
      - type: changed
        content: Changed model to opus
      - type: improved
        content: Optimized descriptions of functionality, use cases, core steps, input requirements, and output format to comply with imperative language specifications
      - type: added
        content: Added constraints, examples, and detailed documentation sections
  - version: 2.0.0
    date: 2026-01-11
    changes:
      - type: breaking
        content: Refactored according to Agent Skills official specifications
      - type: improved
        content: Optimized description, using imperative language, simplified main content
      - type: added
        content: Added license and compatibility optional fields
      - type: added
        content: Added allowed-tools (Read) and model fields
  - version: 1.0.0
    date: 2026-01-10
    changes:
      - type: added
        content: Initial version
---

# Character Relationship Analysis Expert

## Functionality

Analyze relationships between characters in stories, identify relationship types and characteristics, and describe their development process and changes.

## Use Cases

- Deeply understand character relationship networks in stories.
- Analyze the plot-driving role of character relationships.
- Provide relationship perspectives for character shaping.
- Provide relationship support for plot design.

## Core Steps

1. **Identify Characters**: Identify all main characters in the story.
2. **Analyze Relationships**: Analyze relationship types and characteristics between characters.
3. **Classify and Organize**: Classify and organize character relationships.
4. **Describe Characteristics**: Describe specific characteristics of character relationships.
5. **Analyze Changes**: Analyze the development process and changes of character relationships.

## Input Requirements

- Complete story text containing character relationship information.
- Can specify character relationships to be analyzed (optional).
- Recommended text length: 500+ words.

## Output Format

```
[Character Relationship Analysis]

I. Relationship Network Overview
- Main Character List: [Character List]
- Relationship Type Statistics: [Number of Each Type of Relationship]

II. Main Character Relationship Details

[Relationship 1: Character A ↔ Character B]
- Relationship Type: [Family/Friendship/Love/Hostile/Mentor-Disciple/Colleague, etc.]
- Relationship Characteristics: [Description of Relationship Characteristics]
- Relationship Development Process: [How the Relationship Develops and Changes]
- Reasons for Relationship Change: [Causes Leading to Changes]
- Impact on Story: [How It Affects Plot Development]

[Relationship 2: Character A ↔ Character C]
...

III. Character Relationship Map
- Central Character: [Who is the Center of Relationships]
- Secondary Characters: [Minor Character Relationships]
- Peripheral Characters: [Peripheral Character Relationships]

IV. Character Relationship Change Trajectory
- Initial State: [Relationship at the Beginning of the Story]
- Intermediate Changes: [How the Relationship Changes]
- Final State: [Relationship at the End of the Story]
```

## Constraints

- Strictly analyze based on provided story text, do not create on your own.
- Ensure accuracy and completeness of character relationship identification.
- Describe character relationship development process with clear logic and organization.

## Examples

Please refer to `{baseDir}/references/examples.md` for detailed examples. This file contains character relationship analysis reports and analysis instructions for various story types (such as romance, workplace, family, etc.).

## Detailed Documentation

See `{baseDir}/references/` directory for more documentation:
- `guide.md` - Complete character relationship analysis guide
- `examples.md` - More analysis examples for different scenarios

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-01-11 | Optimized description field to be more concise and comply with imperative language specifications; changed model to opus; optimized descriptions of functionality, use cases, core steps, input requirements, and output format to comply with imperative language specifications; added constraints, examples, and detailed documentation sections. |
| 2.0.0 | 2026-01-11 | Refactored according to official specifications; added allowed-tools (Read) and model fields |
| 1.0.0 | 2026-01-10 | Initial version |
