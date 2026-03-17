---
name: lecture-builder
description: Build lectures with consistent format for the NextGenMed website. Use when creating new lecture files, converting HTML content to lecture format, or ensuring lectures follow the standardized structure with meta, video embed, sections, mechanisms table, implementation pathway, and references.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Lecture Builder for NextGenMed Website

## Overview
This skill creates lecture files with a **strict, consistent format** for the NextGenMed website. All lectures must follow the exact same structure, styling, and organization to maintain uniformity across the educational platform.

## Required Inputs
When building a lecture, you must provide:
1. **Title**: The lecture title
2. **Descript iframe**: Video embed code for the lecture video
3. **Output location**: File path where the lecture should be saved
4. **HTML content file**: Path to the HTML file containing the lecture content

## Fixed Lecture Structure
Every lecture MUST follow this exact sequence:
1. **Meta** (track, subtrack, title, duration, tags, abstract)
2. **Header** (generated from meta)
3. **Video Lecture** (Descript iframe embed)
4. **5-7 Content Sections** (text-based educational content)
5. **Key Mechanisms Table** (structured clinical takeaways)
6. **Implementation Pathway** (practical application steps)
7. **The Path Forward** (conclusion and next steps)
8. **References** (numbered citations)

## JSON Structure Template

All lecture data is structured as JSON following this exact format:

```json
{
  "meta": {
    "track": "",
    "subtrack": "",
    "title": "",
    "duration": "",
    "primary_tags": ["", "", ""],
    "abstract": ""
  },
  "video": {
    "video_url": "",
    "caption": "Watch the full lecture here."
  },
  "sections": [
    {
      "id": "fundamental-shift",
      "heading": "The Fundamental Shift",
      "type": "text",
      "paragraphs": ["...", "..."]
    },
    {
      "id": "mechanism",
      "heading": "How [Core Concept] Works",
      "type": "text",
      "paragraphs": ["...", "..."]
    },
    {
      "id": "evidence",
      "heading": "Clinical Performance Evidence",
      "type": "text",
      "paragraphs": ["...", "..."]
    },
    {
      "id": "applications",
      "heading": "[Domain] Applications",
      "type": "text",
      "paragraphs": ["...", "..."]
    },
    {
      "id": "mechanisms-table",
      "heading": "Key Mechanisms and Clinical Takeaways",
      "type": "table",
      "columns": ["Core Mechanism", "Clinical Application", "Implementation Consideration"],
      "rows": [
        ["...", "...", "..."]
      ]
    },
    {
      "id": "implementation",
      "heading": "Implementation Pathway",
      "type": "text",
      "paragraphs": ["**Start with...** ...", "**Build...** ..."]
    },
    {
      "id": "path-forward",
      "heading": "The Path Forward",
      "type": "text",
      "paragraphs": ["...", "..."]
    }
  ],
  "references": [
    "[1] ...",
    "[2] ..."
  ]
}
```

## Content Section Guidelines

### Standard Content Sections (5-7 required)
The content sections between the video and the mechanisms table should cover:
- **The Fundamental Shift**: Core paradigm change or key concept introduction
- **How [Concept] Works**: Mechanism explanation
- **Clinical Performance Evidence**: Research findings and data
- **[Domain] Applications**: Practical use cases
- Additional sections as needed (must be 5-7 total)

### Mechanisms Table (Required)
Always include a structured table with three columns:
- Core Mechanism
- Clinical Application
- Implementation Consideration

### Implementation Pathway (Required)
Structured with bold subheadings like:
- **Start with...**
- **Build...**
- **Integrate...**

### The Path Forward (Required)
Concluding section that synthesizes key points and provides direction.

## Processing Instructions

### Step 1: Read Input Content
- Read the provided HTML file
- Extract the lecture content, preserving structure and formatting
- Identify key sections, headings, and subsections

### Step 2: Structure into JSON
- Map the HTML content to the JSON structure
- Ensure exactly 5-7 content sections (text type)
- Create the mechanisms table from relevant content
- Extract or generate implementation pathway
- Format the path forward section
- Compile references in numbered format

### Step 3: Generate Lecture File
- Create the output file at the specified location
- Use consistent HTML/component structure (check existing lectures for reference)
- Embed the Descript iframe in the video section
- Apply uniform styling and CSS classes
- Ensure responsive design

### Step 4: Validate Consistency
- Verify all required sections are present and in order
- Check that styling matches existing lectures
- Confirm meta tags are complete
- Validate JSON structure integrity

## Example Usage

When invoked, provide:
```
Title: "Deep Learning in Radiology"
Descript iframe: <iframe src="https://..."></iframe>
Output: /lectures/radiology/deep-learning.html
Content: /input/deep-learning-content.html
```

The skill will:
1. Read the content HTML
2. Structure it into the JSON format
3. Generate a consistently-formatted lecture file
4. Save it to the specified output location

## Important Notes
- **Consistency is paramount**: All lectures must be identical in structure
- **Content varies, structure doesn't**: Only the actual text/data changes between lectures
- **Reference existing lectures**: Check other lecture files in the project to match exact styling
- **Preserve formatting**: Maintain bold text, italics, lists, and other formatting from source
- **Complete all sections**: Never skip required sections, even if creating placeholder content
