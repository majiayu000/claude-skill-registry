---
name: markdown-img-alt-text
description: Adds detailed alt text to markdown image embeds that are missing it. Supports both Obsidian wiki-style (![[image]]) and standard markdown (![](path)) formats. Reads each image, describes its content thoroughly, and updates the embed inline. Triggers on "add alt text", "update alt text", "describe images", "missing alt text", or "image descriptions".
---

# Alt Text for Markdown Images

Scan markdown files for image embeds that are missing alt text and add detailed, descriptive alt text by reading each image.

## Supported Formats

- **Obsidian wiki-style**: `![[image.png]]` → `![[image.png|alt text here]]`
- **Standard markdown**: `![](path/to/image.png)` → `![alt text here](path/to/image.png)`

Detect which format the file uses and apply alt text accordingly.

## When to Use

- User asks to add or update alt text on images
- User asks to describe images in their notes
- User asks to make images accessible or searchable

## Process

### 1. Find Images Missing Alt Text

Search the target scope (a specific note, folder, or the whole project) for image embeds without alt text:

- **Obsidian**: `![[filename.ext]]` with no `|` pipe character (image extensions: png, jpg, jpeg, gif, svg, webp)
- **Standard markdown**: `![](path)` where the alt text between `[]` is empty

Images that already have alt text — `![[image.png|description]]` or `![description](path)` — should be skipped.

### 2. Read Each Image

For each image found, use the Read tool to view the image file. Resolve the image path based on the project structure (e.g., an attachments folder, a public/images directory, or a relative path).

### 3. Write Detailed Alt Text

Write thorough, detailed alt text for each image. The alt text should:

- Describe the **full visual content** — what is shown, what text is visible, what the layout looks like
- Capture **specific details** like button labels, heading text, color choices, UI patterns, data values
- Be written as a **single continuous description** (no line breaks) since it goes inline in the embed
- Be detailed enough that someone reading only the alt text would understand the image without seeing it
- Avoid starting with "Image of" or "Screenshot of" — just describe what's there directly

### 4. Update the Embeds

Use the Edit tool to add alt text in the correct format for the embed style used in that file.

## Scope

- If the user specifies a file or folder, only process that scope
- If no scope is given, ask the user whether to process a specific file, folder, or the whole project
- Report how many images were found, how many already had alt text, and how many were updated

## Examples

Obsidian — before:
```
![[dashboard-screenshot.png]]
```

Obsidian — after:
```
![[dashboard-screenshot.png|Analytics dashboard showing a bar chart of monthly revenue from January to June 2026, with a sidebar navigation listing Overview, Reports, and Settings. The header reads "Q2 Performance" in bold with a blue export button in the top right.]]
```

Standard markdown — before:
```
![](images/dashboard-screenshot.png)
```

Standard markdown — after:
```
![Analytics dashboard showing a bar chart of monthly revenue from January to June 2026, with a sidebar navigation listing Overview, Reports, and Settings.](images/dashboard-screenshot.png)
```
