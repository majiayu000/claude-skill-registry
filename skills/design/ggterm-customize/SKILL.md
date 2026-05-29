---
name: ggterm-customize
description: Customize plot aesthetics using natural language. Use when the user wants to change colors, fonts, titles, labels, themes, or any visual aspect of a plot before publication.
allowed-tools: Read, Write, Bash(bun:*)
---

# Natural Language Plot Customization

Modify Vega-Lite specifications based on natural language requests.

## Files

After creating a plot, these files exist:
- `.ggterm/last-plot.json` - Original PlotSpec
- `.ggterm/last-plot-vegalite.json` - Vega-Lite spec to modify

## Customization Workflow

1. Read the current Vega-Lite spec
2. Interpret the user's natural language request
3. Modify the appropriate properties
4. Write the updated spec
5. Show a preview or export

## Common Customizations

### Title and Labels

```javascript
// Vega-Lite spec modifications
spec.title = "New Title"
spec.title = { text: "Title", subtitle: "Subtitle" }

// Axis titles
spec.encoding.x.title = "X Axis Label"
spec.encoding.y.title = "Y Axis Label"

// Legend title
spec.encoding.color.title = "Legend Title"
```

### Colors

```javascript
// Single color for all marks
spec.mark.color = "#3366cc"

// Color scheme for categorical data
spec.encoding.color.scale = { scheme: "category10" }

// Color scheme for continuous data
spec.encoding.color.scale = { scheme: "viridis" }
spec.encoding.color.scale = { scheme: "blues" }

// Custom colors
spec.encoding.color.scale = {
  domain: ["A", "B", "C"],
  range: ["#e41a1c", "#377eb8", "#4daf4a"]
}
```

### Fonts

```javascript
spec.config = spec.config || {}
spec.config.font = "Helvetica"
spec.config.title = { fontSize: 18, fontWeight: "bold" }
spec.config.axis = { labelFontSize: 12, titleFontSize: 14 }
spec.config.legend = { labelFontSize: 11, titleFontSize: 12 }
```

### Themes

```javascript
// Minimal theme
spec.config = {
  view: { stroke: null },
  axis: { grid: false, domain: false }
}

// Dark theme
spec.config = {
  background: "#1a1a1a",
  title: { color: "#ffffff" },
  axis: {
    labelColor: "#cccccc",
    titleColor: "#ffffff",
    gridColor: "#333333"
  }
}
```

### Dimensions

```javascript
spec.width = 600
spec.height = 400
spec.autosize = { type: "fit", contains: "padding" }
```

### Mark Properties

```javascript
// Point size
spec.mark.size = 100

// Opacity
spec.mark.opacity = 0.7

// Line thickness
spec.mark.strokeWidth = 2

// Fill vs stroke
spec.mark.filled = true
```

### Legend Position

```javascript
spec.encoding.color.legend = {
  orient: "bottom",  // top, bottom, left, right
  title: null  // remove legend title
}
```

### Grid and Axes

```javascript
// Remove grid
spec.encoding.x.axis = { grid: false }
spec.encoding.y.axis = { grid: false }

// Remove axis
spec.encoding.x.axis = null

// Format axis labels
spec.encoding.x.axis = { format: ".2f" }  // Numbers
spec.encoding.x.axis = { format: "%Y-%m" }  // Dates
```

## Example Script

```javascript
// Read, modify, write pattern
const spec = JSON.parse(require('fs').readFileSync('.ggterm/last-plot-vegalite.json', 'utf-8'))

// Apply customizations based on user request
spec.title = { text: "Analysis Results", subtitle: "2024 Data" }
spec.config = {
  font: "Arial",
  title: { fontSize: 16 },
  axis: { labelFontSize: 11, titleFontSize: 13 }
}
spec.encoding.color.scale = { scheme: "tableau10" }

require('fs').writeFileSync('.ggterm/last-plot-vegalite.json', JSON.stringify(spec, null, 2))
console.log("Spec updated. Export with /ggterm-publish")
```

## Available Color Schemes

Categorical: category10, category20, tableau10, set1, set2, set3, pastel1, pastel2, accent, dark2
Sequential: blues, greens, greys, oranges, purples, reds, viridis, plasma, inferno, magma
Diverging: blueorange, redblue, redgrey, spectral

## Workflow

1. User asks to customize plot (e.g., "make the points blue and increase font size")
2. Read `.ggterm/last-plot-vegalite.json`
3. Apply the requested modifications
4. Write the updated spec
5. Optionally show preview or suggest export

$ARGUMENTS
