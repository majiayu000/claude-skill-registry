---
name: infographic-creation
description: Create beautiful infographics based on the given text content. Use this when users request creating infographics.
---
An infographic (Infographic) transforms data, information, and knowledge into perceivable visual language. It combines visual design with data visualization, using intuitive symbols to compress complex information and help audiences quickly understand and remember key points.
`Infographic = Information Structure + Visual Expression`
This is a task that utilizes [AntV Infographic](https://infographic.antv.vision/) to create visual infographics.
Before you start the task, you need to understand the AntV Infographic Syntax specification, including template lists, data structures, themes, and more.

## SPECs

### AntV Infographic Syntax
AntV Infographic Syntax is a mermaid-like DSL for describing infographic rendering configuration. It uses indentation to describe information, has strong robustness, and makes it easy to render infographics through AI streaming output. It mainly contains the following information:
1. template: Use template to express text information structure.
2. data: the infographic data, which contains title, desc, items, etc. The items is an array containing label, value, desc, icon, children, etc.
3. theme: Theme contains palette, font, and other styling options.

e.g.:
```plain
infographic list-row-horizontal-icon-arrow
data
title Title
desc Description
items
- label Label
  value 12.5
  desc Explanation
  icon mdi/rocket-launch
theme
palette #3b82f6 #8b5cf6 #f97316
```

### The Syntax
- The first line starts with `infographic `, and the template is selected from the list below (the _Available Templates_ section).
- Use blocks to describe data / theme, with two-space indentation
- Key-value pairs are expressed as "key value", and arrays are expressed as "-" items
- The icon value is provided directly with keywords or icon names (such as `mdi/chart-line`)
- `data` should contain title/desc/items (which can be omitted according to semantics)
- `data.items` should contain label(string)/value(number)/desc(string)/icon(string)/children(object), where children represents the hierarchical structure
- For comparison templates (template names starting with `compare-`), construct exactly two root nodes and place every comparison item under them as children to keep the hierarchy clear
- `theme` field is for customizing the theme of the infographic, including palette, font, etc.

e.g. dark theme with custom palette:
```plain
infographic list-row-simple-horizontal-arrow
theme dark
palette
- #61DDAA
- #F6BD16
- #F08BB4
data
items
- label Step 1
  desc Start
- label Step 2
  desc In Progress
- label Step 3
  desc Complete
```

- Use `theme.base.text.font-family` to specify fonts, such as the handwriting style '851tegakizatsu'
- Use `theme.stylize` to select built-in styles and pass parameters

Common stylization types include:
- `rough`: Apply hand-drawn style to make graphics look like they were drawn by hand.
- `pattern`: Apply pattern fill to add repeated pattern effects to graphics.
- `linear-gradient` / `radial-gradient`: Apply linear or radial gradient effects to graphics.

e.g: Hand-drawn style (rough):
```plain
infographic list-row-simple-horizontal-arrow
theme
stylize rough
base
text
  font-family 851tegakizatsu
data
items
- label Step 1
  desc Start
- label Step 2
  desc In Progress
- label Step 3
  desc Complete
```

Typescript definition for data field:
```ts
interface Data {
  title?: string;
  desc?: string;
  items: ItemDatum[];
  [key: string]: any;
}
interface ItemDatum {
  icon?: string;
  label?: string;
  desc?: string;
  value?: number;
  illus?: string;
  children?: ItemDatum[];
  [key: string]: any;
}
```

### Icon and Illustration Resources

**Icons (from Iconify)**:
- Format: `/`, e.g., `mdi/rocket-launch`
- Popular collections:
  - `mdi/*` - Material Design Icons (most commonly used)
  - `fa/*` - Font Awesome
  - `bi/*` - Bootstrap Icons
  - `heroicons/*` - Heroicons
- Browse at: https://icon-sets.iconify.design/
- Common icon examples:
  - Tech: `mdi/code-tags`, `mdi/database`, `mdi/api`, `mdi/cloud`
  - Business: `mdi/chart-line`, `mdi/briefcase`, `mdi/currency-usd`
  - Process: `mdi/check-circle`, `mdi/arrow-right`, `mdi/cog`
  - People: `mdi/account`, `mdi/account-group`, `mdi/shield-account`

**Illustrations (from unDraw)**:
- Format: illustration filename (without .svg), e.g., `coding`
- Browse at: https://undraw.co/illustrations
- Common themes:
  - Tech: `coding`, `programmer`, `server`, `cloud-sync`
  - Business: `business-plan`, `team-work`, `analytics`
  - Abstract: `abstract`, `building-blocks`, `connection`
- Note: Use sparingly as illustrations are larger and more detailed than icons

**Usage Tips**:
- For `sequence-*` and `list-*` templates → use `icon`
- For larger illustration needs → use `illus`
- Not all templates support both icon and illus - refer to template examples

### Available Templates
- sequence-zigzag-steps-underline-text
- sequence-horizontal-zigzag-underline-text
- sequence-horizontal-zigzag-simple-illus
- sequence-circular-simple
- sequence-filter-mesh-simple
- sequence-mountain-underline-text
- sequence-cylinders-3d-simple
- sequence-color-snake-steps-horizontal-icon-line
- sequence-pyramid-simple
- sequence-roadmap-vertical-simple
- sequence-roadmap-vertical-plain-text
- sequence-zigzag-pucks-3d-simple
- sequence-ascending-steps
- sequence-ascending-stairs-3d-underline-text
- sequence-snake-steps-compact-card
- sequence-snake-steps-underline-text
- sequence-snake-steps-simple
- sequence-stairs-front-compact-card
- sequence-stairs-front-pill-badge
- sequence-timeline-simple
- sequence-timeline-rounded-rect-node
- sequence-timeline-simple-illus
- compare-binary-horizontal-simple-fold
- compare-hierarchy-left-right-circle-node-pill-badge
- compare-swot
- quadrant-quarter-simple-card
- quadrant-quarter-circular
- quadrant-simple-illus
- relation-circle-icon-badge
- relation-circle-circular-progress
- compare-binary-horizontal-badge-card-arrow
- compare-binary-horizontal-underline-text-vs
- hierarchy-tree-tech-style-capsule-item
- hierarchy-tree-curved-line-rounded-rect-node
- hierarchy-tree-tech-style-badge-card
- chart-column-simple
- chart-bar-plain-text
- chart-line-plain-text
- chart-pie-plain-text
- chart-pie-compact-card
- chart-pie-donut-plain-text
- chart-pie-donut-pill-badge
- chart-wordcloud
- list-grid-badge-card
- list-grid-candy-card-lite
- list-grid-ribbon-card
- list-row-horizontal-icon-arrow
- list-row-simple-illus
- list-sector-plain-text
- list-column-done-list
- list-column-vertical-icon-arrow
- list-column-simple-vertical-arrow

**Template Selection Guidelines:**
- For strict sequential order: processes/steps/development trends → `sequence-*` series
- Timeline → `sequence-timeline-*`
- Staircase diagram → `sequence-stairs-*`
- Roadmap → `sequence-roadmap-vertical-*`
- Zigzag steps → `sequence-zigzag-*`
- Circular progress → `sequence-circular-simple`
- Color snake steps → `sequence-color-snake-steps-*`
- Pyramid diagram → `sequence-pyramid-simple`
- For listing viewpoints → `list-row-*` series or `list-column-*` series
- For comparative analysis (comparing pros and cons of two parties) → `compare-binary-*` series
- For SWOT analysis → `compare-swot`
- For hierarchical structure (tree diagram) → `hierarchy-tree-*`
- For data charts → `chart-*` series
- For quadrant analysis → `quadrant-*` series
- For grid lists (bullet points) → `list-grid-*` series
- For relationship display → `relation-circle-*`
- For word cloud → `chart-wordcloud`

### Example
Draw an information graph of the Internet technology evolution
```plain
infographic list-row-horizontal-icon-arrow
data
title Internet Technology Evolution
desc From Web 1.0 to AI era, key milestones
items
- time 1991
  label Web 1.0
  desc Tim Berners-Lee published the first website, opening the Internet era
  icon mdi/web
- time 2004
  label Web 2.0
  desc Social media and user-generated content become mainstream
  icon mdi/account-multiple
- time 2007
  label Mobile
  desc iPhone released, smartphone changes the world
  icon mdi/cellphone
- time 2015
  label Cloud Native
  desc Containerization and microservices architecture are widely used
  icon mdi/cloud
- time 2020
  label Low Code
  desc Visual development lowers the technology threshold
  icon mdi/application-brackets
- time 2023
  label AI Large Model
  desc ChatGPT ignites the generative AI revolution
  icon mdi/brain
```

### Example 2: Using Illustrations
```plain
infographic sequence-horizontal-zigzag-simple-illus
data
title Product Development Phases
desc Key stages in our development process
items
- label Research
  desc Understanding user needs
  illus user-research
- label Design
  desc Creating user experience
  illus design-thinking
- label Development
  desc Building the product
  illus coding
- label Launch
  desc Going to market
  illus launch-day
```

## Creation Process

### Step 1: Understanding User Requirements
Before creating the infographic, it is important to understand the user's requirements and the information they want to present. This will help in defining the template and the data structure.

If the user provides a clear and concise description of the information they want to present, break down the information into a clear and concise structure.

Otherwise, ask the user for clarification (e.g., "Please provide a clear and concise description of the information you want to present.", "Which template would you prefer to use?")

- Extract key information structure (title, description, items, etc).
- Identify the required data fields (e.g., title, description, items, labels, values, icons, etc.).
- Select an appropriate template.
- Use the AntV Infographic Syntax to describe the content of the infographic `{syntax}`.

**CRITICAL NOTE**: Must respect the language of the user's input content. e.g. if the user's input content is in Chinese, the text content in infographic syntax must be in Chinese.

### Step 2: Rendering the Infographic
Once you have the final AntV Infographic Syntax, you can generate the complete infographic HTML file by following these steps:

1. Create a complete HTML file with the following structure:
- DOCTYPE and HTML meta tags (charset: utf-8)
- Title: `{title} - Infographic`
- Include AntV Infographic library script: `https://unpkg.com/@antv/infographic@latest/dist/infographic.min.js`
- Add a resource loader script that handles icon loading from Iconify and illustration loading from unDraw
- Create a container div with id `container` where the infographic will render
- Initialize the Infographic instance with `width: '100%'` and `height: '100%'`
- Replace the placeholder `{title}` with the actual title
- Replace the placeholder `{syntax}` with the actual AntV Infographic Syntax
- Include export functionality that allows users to download the infographic as SVG `const svgDataUrl = await infographic.toDataURL({ type: 'svg' });`

The Html template you can follow:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Infographic</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            width: 100vw;
            height: 100vh;
            overflow: hidden;
        }
        #container {
            width: 100%;
            height: 100%;
        }
        .export-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 20px;
            background: #3b82f6;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            z-index: 1000;
        }
        .export-btn:hover {
            background: #2563eb;
        }
    </style>
</head>
<body>
    <button class="export-btn" onclick="exportSVG()">Export SVG</button>
    <div id="container"></div>
    <script src="https://unpkg.com/@antv/infographic@latest/dist/infographic.min.js"></script>
    <script>
        // Resource loader for icons and illustrations
        const resourceLoader = {
            icons: new Set(),
            illustrations: new Set(),
            loadIcon(name) {
                this.icons.add(name);
                return `https://api.iconify.design/${name}.svg`;
            },
            loadIllustration(name) {
                this.illustrations.add(name);
                return `https://unpkg.com/undraw-cli@0.0.1/static/illustrations/${name}.svg`;
            }
        };

        const infographic = new Infographic({
            container: 'container',
            width: '100%',
            height: '100%',
            data: `{syntax}`
        });

        async function exportSVG() {
            const svgDataUrl = await infographic.toDataURL({ type: 'svg' });
            const link = document.createElement('a');
            link.href = svgDataUrl;
            link.download = '{title}.svg';
            link.click();
        }
    </script>
</body>
</html>
```

2. Write the HTML file named `-infographic.html` using the Write tool

3. Display to the user:
   - The generated file path with instruction: "Open this file directly in a browser to view and save the SVG"
   - Display your output syntax with instruction: "If you need to adjust the template/colors/content, just let me know"

**Note:** The HTML file must include:
- Complete resource loader for handling icon and illustration assets from external sources
- SVG export functionality via the export button
- Responsive container that takes 100% width and height
- Proper error handling for failed resource loads
