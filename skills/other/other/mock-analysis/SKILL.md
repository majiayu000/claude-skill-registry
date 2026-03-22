---
name: mock-analysis
description: |
  Patterns for analyzing HTML/CSS mocks from Stitch, Figma, or similar tools.
  Covers section identification, component detection, and Tailwind config extraction.
  Use this skill when parsing mocks for block conversion.
allowed-tools: Read, Glob, Grep, Bash
version: 1.0.0
---

# Mock Analysis Skill

Patterns for parsing and analyzing HTML/CSS mocks to prepare for block conversion.

## When to Use This Skill

- Analyzing Stitch exports (code.html + screen.png)
- Parsing Figma HTML exports
- Understanding mock structure before conversion
- Extracting design tokens from inline Tailwind config

## Mock File Structure

Standard export structure (flexible detection):

```
mock-folder/
├── code.html          # Main HTML markup (or *.html)
├── screen.png         # Visual screenshot (or *.png, *.jpg)
├── assets/            # Images, fonts (optional)
│   ├── images/
│   └── fonts/
└── tailwind.config.js # Sometimes included inline in HTML
```

**Flexible File Detection:**

| File Type | Detection Pattern | Required |
|-----------|-------------------|----------|
| HTML | `code.html`, `index.html`, `*.html` | Recommended |
| Screenshot | `screen.png`, `*.png`, `*.jpg`, `*.jpeg` | Required |
| Tailwind Config | `tailwind.config.js`, inline in HTML | Optional |
| Assets | `assets/`, `images/` | Optional |
| PDF | `*.pdf` (for Figma exports) | Alternative |

**Detection Priority:**
1. `code.html` → Primary HTML file
2. `index.html` → Alternative name
3. Any `*.html` → Fallback
4. `screen.png` → Primary screenshot
5. `screenshot.png`, `screen.jpg` → Alternatives
6. Any `*.png`, `*.jpg` → Fallback

**Workflow Integration:**
- BLOCKS: Mock is required
- TASK/STORY: Mock is optional
- Phase 0.6 runs mock-analyst when mock is selected
- Output files go to session's `mocks/` folder

## Section Identification Heuristics

### Hero Sections
```html
<!-- Indicators -->
<section class="...min-h-[500px]...">  <!-- Large min-height -->
<section class="...h-screen...">       <!-- Full viewport -->
<div class="...bg-cover...">           <!-- Background image -->
<h1>...</h1>                           <!-- Main heading -->
```

**Classification:** `type: "hero"`

### Navigation/Header
```html
<header>...</header>
<nav>...</nav>
<div class="...fixed...top-0...">
```

**Classification:** `type: "navigation"`

### Feature Grids
```html
<div class="...grid...grid-cols-3...">
  <div>...</div>  <!-- Repeated pattern -->
  <div>...</div>
  <div>...</div>
</div>
```

**Classification:** `type: "features"`

### CTA Sections
```html
<section class="...text-center...py-16...">
  <h2>...</h2>
  <p>...</p>
  <button>...</button>  <!-- 1-2 buttons -->
</section>
```

**Classification:** `type: "cta"`

### Footer
```html
<footer>...</footer>
<div class="...mt-auto...">  <!-- At bottom -->
```

**Classification:** `type: "footer"`

## Component Detection Patterns

### Buttons
```html
<button class="...">Text</button>
<a href="..." class="...btn...">Text</a>
<a href="..." class="...rounded...bg-...">Text</a>
```

### Forms
```html
<form>...</form>
<input type="...">
<div class="...flex...gap-...">
  <input>
  <button>Submit</button>
</div>
```

### Cards
```html
<div class="...rounded...border...shadow...">
  <img>
  <h3>...</h3>
  <p>...</p>
</div>
```

### Icons
```html
<svg>...</svg>
<i class="...icon...">
<span class="...lucide-...">
```

## Tailwind Config Extraction

Look for inline config in HTML:

```html
<script>
tailwind.config = {
  theme: {
    extend: {
      colors: {
        primary: '#137fec',
        'background-dark': '#101922',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    }
  }
}
</script>
```

**Extract:**
- `colors` → For ds-mapping
- `fontFamily` → For typography mapping
- `spacing` → If customized
- `borderRadius` → If customized

## Output Format: analysis.json

```json
{
  "mockPath": "_tmp/mocks/stitch/landing-page",
  "htmlFile": "code.html",
  "screenshotFile": "screen.png",
  "analyzedAt": "2025-01-09T12:00:00Z",

  "tailwindConfig": {
    "found": true,
    "colors": {
      "primary": "#137fec",
      "background-dark": "#101922",
      "accent": "#00d4ff"
    },
    "fonts": {
      "sans": ["Inter", "sans-serif"],
      "mono": ["JetBrains Mono", "monospace"]
    }
  },

  "sections": [
    {
      "id": "section-1",
      "type": "hero",
      "selector": "section:first-of-type",
      "htmlSnippet": "<section class=\"relative min-h-[600px]...\">",
      "components": [
        {"type": "heading", "level": 1, "text": "Build faster..."},
        {"type": "paragraph", "text": "The complete..."},
        {"type": "button", "text": "Get Started", "variant": "primary"},
        {"type": "custom", "name": "terminal-animation"}
      ],
      "layout": {
        "type": "centered-flex",
        "minHeight": "600px",
        "hasBackground": true,
        "backgroundType": "gradient"
      },
      "estimatedComplexity": "high",
      "notes": "Contains animated terminal component"
    },
    {
      "id": "section-2",
      "type": "features",
      "selector": "section:nth-of-type(2)",
      "components": [
        {"type": "heading", "level": 2},
        {"type": "grid", "columns": 3, "items": 6}
      ],
      "layout": {
        "type": "grid",
        "columns": "3",
        "gap": "6"
      },
      "estimatedComplexity": "low"
    }
  ],

  "componentInventory": {
    "headings": {"h1": 1, "h2": 4, "h3": 12},
    "buttons": 8,
    "links": 24,
    "images": 6,
    "icons": 18,
    "forms": 1,
    "customComponents": [
      {"name": "terminal-animation", "section": "section-1"},
      {"name": "tabs-preview", "section": "section-4"},
      {"name": "chat-widget", "section": "section-5"}
    ]
  },

  "summary": {
    "totalSections": 7,
    "complexity": "medium-high",
    "customComponentsCount": 3,
    "estimatedBlocks": {
      "new": 3,
      "existing": 4
    }
  }
}
```

## Analysis Protocol

1. **Validate mock folder** - Check required files exist
2. **Parse HTML** - Load and parse code.html
3. **Extract Tailwind config** - Find inline configuration
4. **Identify sections** - Segment by semantic sections
5. **Classify sections** - Apply heuristics for type
6. **Detect components** - Inventory all components per section
7. **Assess complexity** - Estimate block requirements
8. **Generate analysis.json** - Output structured analysis

## Related Skills

- `design-system` - For token mapping after analysis
- `page-builder-blocks` - For understanding target block structure
- `shadcn-components` - For component pattern matching
