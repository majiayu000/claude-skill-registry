---
name: ggterm-publish
description: Export terminal plots to publication-quality formats (PNG, SVG, PDF, HTML). Use when the user wants to save, export, publish, or create a high-quality version of a plot.
allowed-tools: Bash(bun:*, npx:*, vl2*), Read, Write
---

# Publication Export with ggterm

Export terminal plots to publication-quality formats using Vega-Lite.

## Prerequisites

The Vega-Lite CLI tools must be installed:

```bash
npm install -g vega-lite vega-cli canvas
```

## How It Works

When a plot is created with the CLI, ggterm saves:
- `.ggterm/last-plot.json` - The PlotSpec (ggterm format)
- `.ggterm/last-plot-vegalite.json` - The Vega-Lite spec

## Export Commands

### To PNG (Raster)

```bash
npx vl2png .ggterm/last-plot-vegalite.json > plot.png
```

### To SVG (Vector)

```bash
npx vl2svg .ggterm/last-plot-vegalite.json > plot.svg
```

### To PDF

```bash
npx vl2pdf .ggterm/last-plot-vegalite.json > plot.pdf
```

### To HTML (Interactive)

```bash
cat > plot.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
</head>
<body>
  <div id="vis"></div>
  <script>
    const spec = SPEC_PLACEHOLDER;
    vegaEmbed('#vis', spec);
  </script>
</body>
</html>
EOF

# Replace placeholder with actual spec
bun -e "
const spec = require('./.ggterm/last-plot-vegalite.json');
const html = require('fs').readFileSync('plot.html', 'utf-8');
const result = html.replace('SPEC_PLACEHOLDER', JSON.stringify(spec, null, 2));
require('fs').writeFileSync('plot.html', result);
"
```

## Custom Dimensions

To export with different dimensions, modify the Vega-Lite spec first:

```bash
bun -e "
const spec = require('./.ggterm/last-plot-vegalite.json');
spec.width = 800;
spec.height = 600;
require('fs').writeFileSync('.ggterm/last-plot-vegalite.json', JSON.stringify(spec, null, 2));
"
npx vl2png .ggterm/last-plot-vegalite.json > plot-large.png
```

## Workflow

1. User creates a terminal plot using `/ggterm-plot`
2. User asks to export it for publication
3. This skill exports to the requested format

## Troubleshooting

If vl2png/vl2svg fail, ensure dependencies are installed:

```bash
npm install -g vega-lite vega-cli canvas
```

On macOS, canvas may require additional setup:

```bash
brew install pkg-config cairo pango libpng jpeg giflib librsvg
npm install -g canvas --build-from-source
```

$ARGUMENTS
