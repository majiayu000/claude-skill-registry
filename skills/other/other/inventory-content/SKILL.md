---
name: inventory-content
description: Systematic cataloging of information assets. Creates comprehensive inventories of all content with metadata and characteristics.
required_roles:
  scribe: roles/scribe.viewer
personas: [information-architect, content-manager, librarian]
---

# Content Inventory Skill

Create a systematic catalog of information assets within a specified path. This skill builds a comprehensive inventory including metadata, file characteristics, and format analysis to support content governance and strategic planning.

## Inputs

- `PATH` - The directory or file path to inventory (e.g., "/documentation")
- `OUTPUT_FORMAT` - (Optional) The output format for the inventory, e.g., "csv", "json", "markdown" (default: "json")
- `METADATA_EXTRACTION` - (Optional) Boolean, whether to extract deep metadata (author, date, tags) (default: true)
- `FORMAT_ANALYSIS` - (Optional) Boolean, whether to analyze file formats and types (default: true)

## Workflow

### Step 1: Asset Discovery

Recursively scan the `PATH` to identify all files and assets.
- Record file paths, names, and sizes.
- Identify file types (Markdown, HTML, PDF, Image, etc.).

### Step 2: Metadata Extraction

If `METADATA_EXTRACTION` is true, extract metadata from each asset:
- **System Metadata**: Creation date, modification date, owner.
- **Embedded Metadata**: Frontmatter (YAML), title headers, tags, categories.
- **Content Metrics**: Word count, reading time estimation.

### Step 3: Format & Structure Analysis

If `FORMAT_ANALYSIS` is true, analyze the structure:
- **Template Usage**: Identify if standard templates are used.
- **Hierarchy Depth**: Depth in the directory structure.
- **Resource Dependencies**: Images or other assets linked.

### Step 4: Inventory Report Generation

Compile the data into a structured inventory format (CSV, JSON, or Markdown Table) as specified by `OUTPUT_FORMAT`.

## Required Outputs

A `CONTENT_INVENTORY_REPORT` in the specified `OUTPUT_FORMAT` containing:
- **Asset List**: Full list of discovered assets.
- **Metadata Table**: Columns for Title, URL/Path, Author, Last Modified, Type, Tags.
- **Summary Statistics**: Total count by type, average age, volume by category.

## Quick Reference

- **Purpose**: Establish a baseline understanding of content assets for governance.
- **Use Case**: Migration planning, audit preparation, consolidation projects.
