---
name: Chapter Analyzer
description: Validates and analyzes Docusaurus MDX chapters for structure, pedagogical quality, and component usage.
---

# Chapter Analyzer Logic

## Target Directory
- **Location**: `textbook/docs/`
- **Format**: MDX (`.mdx` or `.md`)

## Structural Validation
Every chapter must have valid YAML frontmatter:
```yaml
---
id: my-chapter-id
title: My Chapter Title
sidebar_label: Sidebar Label
description: Brief summary of the chapter.
---
```

## Content Rules
1.  **Heading Hierarchy**:
    - The Docusaurus title acts as H1.
    - Start content with H2 (`##`).
    - Do not use H1 (`#`) within the body.
2.  **Pedagogical Flow**:
    - **Introduction**: Hook the reader.
    - **Learning Objectives**: Bullet points on what will be learned.
    - **Core Content**: Explained with text + diagrams/code.
    - **Interactive Element**: At least one Quiz or Simulation per major section.
    - **Summary**: Recap key points.

## Interactive Components
We use custom components in MDX:
- `<Quiz questions={[...]} />`: For knowledge checks.
- `<Simulation type="ros2-node" ... />`: For embedded simulations.
- `<Tabs>` / `<TabItem>`: For multi-language code blocks (Python/C++).

## Tone Check
- **Voice**: Encouraging, Authoritative but Accessible.
- **Perspective**: "We will learn", "Let's explore".
- **Clarity**: Avoid jargon without explanation.
