---
name: ggterm-style
description: Apply publication-quality style presets to plots. Use when the user wants to style a plot like Wilke, Tufte, Nature, The Economist, or apply minimal/publication styling.
allowed-tools: Read, Write, Bash(bun:*)
---

# Plot Style Presets

Apply expert-curated style presets to Vega-Lite specifications for publication-quality output.

## Available Presets

| Preset | Inspiration | Key Characteristics |
|--------|-------------|---------------------|
| `wilke` | Claus Wilke's *Fundamentals of Data Visualization* | Minimal, clean, no chartjunk, subtle gridlines |
| `tufte` | Edward Tufte's data-ink ratio principles | Maximum data-ink, no grid, no borders |
| `nature` | Nature journal style | Clean, serif fonts, specific dimensions |
| `economist` | The Economist charts | Bold colors, distinctive style |
| `minimal` | Generic minimal style | No grid, no borders, clean |
| `apa` | APA publication guidelines | Academic papers, grayscale-friendly |

## Workflow

1. Read `.ggterm/last-plot-vegalite.json`
2. Apply the requested style preset
3. Write the updated spec
4. Inform user they can export with `/ggterm-publish`

## Style Configurations

### Wilke Style (Recommended Default)

Based on Claus Wilke's *Fundamentals of Data Visualization* principles:
- No unnecessary gridlines (or very subtle if needed)
- Clean, sans-serif typography (Helvetica/Arial)
- No bold axis titles
- High data-ink ratio
- Muted, colorblind-safe palettes
- No 3D effects or gradients
- Appropriate aspect ratios

```javascript
const wilkeStyle = {
  config: {
    font: "Helvetica Neue, Helvetica, Arial, sans-serif",
    background: "white",
    view: { stroke: null },
    title: {
      fontSize: 14,
      fontWeight: "normal",
      anchor: "start",
      offset: 12
    },
    axis: {
      domain: true,
      domainColor: "#333333",
      domainWidth: 1,
      grid: false,
      gridColor: "#e5e5e5",
      gridWidth: 0.5,
      labelColor: "#333333",
      labelFontSize: 11,
      labelFontWeight: "normal",
      tickColor: "#333333",
      tickSize: 5,
      titleColor: "#333333",
      titleFontSize: 12,
      titleFontWeight: "normal",
      titlePadding: 10
    },
    axisX: {
      grid: false
    },
    axisY: {
      grid: true,
      gridColor: "#ebebeb",
      gridDash: [],
      gridWidth: 0.5
    },
    legend: {
      labelFontSize: 11,
      titleFontSize: 11,
      titleFontWeight: "normal",
      symbolSize: 100,
      orient: "right"
    },
    range: {
      category: ["#4C78A8", "#F58518", "#E45756", "#72B7B2", "#54A24B", "#EECA3B", "#B279A2", "#FF9DA6"]
    }
  }
}
```

### Tufte Style

Edward Tufte's principles: maximize data-ink ratio, minimize non-data ink.

```javascript
const tufteStyle = {
  config: {
    font: "Georgia, serif",
    background: "white",
    view: { stroke: null },
    title: {
      fontSize: 13,
      fontWeight: "normal",
      anchor: "start"
    },
    axis: {
      domain: false,
      grid: false,
      labelColor: "#333333",
      labelFontSize: 10,
      labelFontWeight: "normal",
      ticks: false,
      titleColor: "#333333",
      titleFontSize: 11,
      titleFontWeight: "normal"
    },
    legend: {
      labelFontSize: 10,
      titleFontSize: 10,
      titleFontWeight: "normal"
    },
    range: {
      category: ["#333333", "#666666", "#999999", "#CCCCCC"]
    }
  }
}
```

### Nature Style

Nature journal publication style.

```javascript
const natureStyle = {
  config: {
    font: "Arial, Helvetica, sans-serif",
    background: "white",
    view: { stroke: null },
    title: {
      fontSize: 10,
      fontWeight: "bold"
    },
    axis: {
      domain: true,
      domainColor: "#000000",
      domainWidth: 0.5,
      grid: false,
      labelColor: "#000000",
      labelFontSize: 8,
      labelFontWeight: "normal",
      tickColor: "#000000",
      tickSize: 4,
      tickWidth: 0.5,
      titleColor: "#000000",
      titleFontSize: 9,
      titleFontWeight: "normal"
    },
    legend: {
      labelFontSize: 8,
      titleFontSize: 8,
      symbolSize: 50
    }
  },
  width: 180,
  height: 150
}
```

### Economist Style

The Economist's distinctive chart style.

```javascript
const economistStyle = {
  config: {
    font: "Officina Sans, Arial, sans-serif",
    background: "#d5e4eb",
    view: { stroke: null },
    title: {
      fontSize: 14,
      fontWeight: "bold",
      color: "#000000",
      anchor: "start"
    },
    axis: {
      domain: false,
      grid: true,
      gridColor: "#ffffff",
      gridWidth: 1,
      labelColor: "#000000",
      labelFontSize: 11,
      tickColor: "#000000",
      titleColor: "#000000",
      titleFontSize: 12,
      titleFontWeight: "bold"
    },
    axisX: {
      grid: false,
      domain: true,
      domainColor: "#000000"
    },
    legend: {
      orient: "top",
      labelFontSize: 11,
      titleFontSize: 11
    },
    range: {
      category: ["#006BA2", "#3EBCD2", "#379A8B", "#EBB434", "#B4BA39", "#9A607F", "#D73F3F"]
    }
  }
}
```

### Minimal Style

Clean, distraction-free visualization.

```javascript
const minimalStyle = {
  config: {
    font: "system-ui, -apple-system, sans-serif",
    background: "white",
    view: { stroke: null },
    title: {
      fontSize: 14,
      fontWeight: "normal"
    },
    axis: {
      domain: false,
      grid: false,
      ticks: false,
      labelColor: "#666666",
      labelFontSize: 11,
      titleColor: "#333333",
      titleFontSize: 12,
      titleFontWeight: "normal"
    },
    legend: {
      labelFontSize: 11,
      titleFontSize: 11,
      titleFontWeight: "normal"
    }
  }
}
```

### APA Style

American Psychological Association publication guidelines.

```javascript
const apaStyle = {
  config: {
    font: "Times New Roman, serif",
    background: "white",
    view: { stroke: null },
    title: {
      fontSize: 12,
      fontWeight: "bold",
      anchor: "middle"
    },
    axis: {
      domain: true,
      domainColor: "#000000",
      grid: false,
      labelColor: "#000000",
      labelFontSize: 10,
      tickColor: "#000000",
      titleColor: "#000000",
      titleFontSize: 11,
      titleFontWeight: "normal",
      titleFontStyle: "italic"
    },
    legend: {
      labelFontSize: 10,
      titleFontSize: 10,
      titleFontStyle: "italic"
    },
    range: {
      category: ["#000000", "#666666", "#999999", "#CCCCCC"]
    }
  }
}
```

## Implementation Script

```javascript
const fs = require('fs');

// Style presets
const STYLES = {
  wilke: { /* config from above */ },
  tufte: { /* config from above */ },
  nature: { /* config from above */ },
  economist: { /* config from above */ },
  minimal: { /* config from above */ },
  apa: { /* config from above */ }
};

function applyStyle(spec, styleName) {
  const style = STYLES[styleName];
  if (!style) {
    throw new Error(`Unknown style: ${styleName}. Available: ${Object.keys(STYLES).join(', ')}`);
  }

  // Merge config (style config takes precedence)
  spec.config = { ...spec.config, ...style.config };

  // Apply dimensions if specified
  if (style.width) spec.width = style.width;
  if (style.height) spec.height = style.height;

  return spec;
}

// Read, apply, write
const specPath = '.ggterm/last-plot-vegalite.json';
const spec = JSON.parse(fs.readFileSync(specPath, 'utf-8'));
const styledSpec = applyStyle(spec, 'wilke'); // or requested style
fs.writeFileSync(specPath, JSON.stringify(styledSpec, null, 2));
```

## Usage Examples

User says: "style this like Wilke" or "apply wilke style"
- Read spec, apply wilkeStyle config, write spec

User says: "make it publication ready"
- Default to wilke style (most universally appropriate)

User says: "style for Nature journal"
- Apply natureStyle with specific dimensions

User says: "Tufte style" or "maximize data ink"
- Apply tufteStyle (no grid, no borders, minimal)

## Key Principles by Style

### Wilke Principles
1. **No chartjunk**: Remove unnecessary visual elements
2. **Subtle gridlines**: Y-axis only, very light gray
3. **Clear hierarchy**: Data first, then axes, then labels
4. **Colorblind-safe**: Use distinguishable palettes
5. **Appropriate aspect ratio**: ~1.6:1 for most plots

### Tufte Principles
1. **Data-ink ratio**: Maximize proportion of ink devoted to data
2. **No grid**: Lines should only appear when they represent data
3. **No borders**: View stroke removed
4. **Minimal ticks**: Only where necessary
5. **Direct labeling**: Prefer labels over legends when possible

## Response Format

After applying a style:

```
Applied **{style}** style to your plot.

Changes:
- {list key visual changes}

Export with `/ggterm-publish` to generate PNG/SVG/PDF.
```

$ARGUMENTS
