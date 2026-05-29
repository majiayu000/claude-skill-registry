---
name: skill-visualizer
description: Generate interactive HTML visualizations of the skills collection, codebase structure, or dependency graphs. Uses D3.js for interactive visualization with collapsible nodes, color-coded categories, and hover details. Triggers on "visualize skills", "generate skill map", "codebase visualization", or "show skill dependencies".
allowed-tools: Bash(python *), Read, Glob, Write
argument-hint: "[type: skills|codebase|deps]"
---

# Skill Visualizer

Generate interactive HTML visualizations for exploring skills, codebase structure, and dependencies.

## Overview

This skill creates browser-viewable HTML files with interactive diagrams. It supports multiple visualization types and outputs self-contained HTML files that open directly in any browser.

## Arguments

- `$0`: Output type - `skills`, `codebase`, or `deps` (default: skills)

Examples:
- `/skill-visualizer` - Generate skills collection map
- `/skill-visualizer skills` - Generate skills collection map
- `/skill-visualizer codebase` - Generate codebase structure visualization
- `/skill-visualizer deps` - Generate skill dependency graph

## Visualization Types

### Skills Map (`skills`)

Generates an interactive force-directed graph of all skills showing:
- Skill nodes with name and type indicator
- Color coding by skill type:
  - **Green**: Orchestrators (context: fork)
  - **Blue**: Read-only (allowed-tools restrictions)
  - **Orange**: Hybrid (standard skills)
- Hover tooltips with skill descriptions
- Drag to reposition nodes

### Codebase Structure (`codebase`)

Generates a treemap visualization of the project structure:
- Directory hierarchy with expandable nodes
- File type distribution by color
- Size indicators for each file/directory

### Dependency Graph (`deps`)

Generates a directed graph showing skill dependencies:
- Which skills invoke other skills
- Integration points between skills
- Visual workflow representation

## Usage

1. Invoke the skill with desired output type
2. The skill runs Python scripts to analyze the codebase
3. Generates self-contained HTML with embedded CSS/JS
4. Opens in default browser automatically

```bash
# Run directly
python ~/.claude/skills/skill-visualizer/scripts/visualize.py skills

# Output location
docs/visualizations/skills-map-YYYY-MM-DD.html
```

## Output

All visualizations are saved to `docs/visualizations/`:
- `skills-map-YYYY-MM-DD.html`
- `codebase-structure-YYYY-MM-DD.html`
- `skill-deps-YYYY-MM-DD.html`

## HTML Features

- **Self-contained**: No external dependencies (D3.js embedded)
- **Responsive design**: Works on any screen size
- **Interactive**: Pan, zoom, drag nodes
- **Tooltips**: Hover for details
- **Dark theme**: Easy on the eyes
- **Export-ready**: Can screenshot for documentation

## Python Scripts

The skill uses Python scripts in `scripts/` directory:
- `visualize.py` - Main visualization generator
- Requires only standard library (no pip install needed)
