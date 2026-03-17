---
name: figma
description: Integrate with Figma API for design automation and code generation. Use when extracting design tokens, generating React/CSS code from Figma components, syncing design systems, building Figma plugins, or automating design-to-code workflows. Triggers on Figma API, design tokens, Figma plugin, design-to-code, Figma export, Figma component, Dev Mode.
---

# Figma API Integration

Extract design data, generate code from components, and automate design workflows with Figma's API.

## Quick Start

### Authentication
```typescript
const FIGMA_TOKEN = process.env.FIGMA_TOKEN;

const headers = {
  'X-Figma-Token': FIGMA_TOKEN
};

// Get file
const response = await fetch(
  `https://api.figma.com/v1/files/${FILE_KEY}`,
  { headers }
);
```

### File Key & Node IDs
```typescript
// Extract from Figma URL: figma.com/file/FILE_KEY/Name?node-id=NODE_ID
const figmaUrl = 'https://www.figma.com/file/abc123/MyDesign?node-id=1%3A2';
const fileKey = figmaUrl.match(/file\/([^/]+)/)?.[1];  // abc123
const nodeId = new URL(figmaUrl).searchParams.get('node-id');  // 1:2
```

## Core API Endpoints

### Get File
```typescript
// Full file
GET https://api.figma.com/v1/files/:file_key

// Specific nodes (components)
GET https://api.figma.com/v1/files/:file_key/nodes?ids=1:2,1:3

// With geometry for SVG paths
GET https://api.figma.com/v1/files/:file_key?geometry=paths

// With plugin data
GET https://api.figma.com/v1/files/:file_key?plugin_data=shared
```

### Get Components
```typescript
// Get all components in a file
GET https://api.figma.com/v1/files/:file_key/components

// Get component sets (variants)
GET https://api.figma.com/v1/files/:file_key/component_sets

// Get team's published components
GET https://api.figma.com/v1/teams/:team_id/components
```

### Export Images
```typescript
// Export nodes as images
GET https://api.figma.com/v1/images/:file_key?ids=1:2,1:3&format=png&scale=2

// Export as SVG
GET https://api.figma.com/v1/images/:file_key?ids=1:2&format=svg

// Response
{
  "images": {
    "1:2": "https://s3.amazonaws.com/...",
    "1:3": "https://s3.amazonaws.com/..."
  }
}
```

## Component Code Generation

### Figma Node to React Component
```typescript
interface FigmaNode {
  id: string;
  name: string;
  type: string;
  children?: FigmaNode[];
  absoluteBoundingBox?: { x: number; y: number; width: number; height: number };
  fills?: Fill[];
  strokes?: Stroke[];
  effects?: Effect[];
  cornerRadius?: number;
  paddingLeft?: number;
  paddingRight?: number;
  paddingTop?: number;
  paddingBottom?: number;
  itemSpacing?: number;
  layoutMode?: 'HORIZONTAL' | 'VERTICAL' | 'NONE';
  primaryAxisAlignItems?: string;
  counterAxisAlignItems?: string;
  characters?: string;
  style?: TextStyle;
}

async function getComponentCode(fileKey: string, nodeId: string): Promise<string> {
  const response = await fetch(
    `https://api.figma.com/v1/files/${fileKey}/nodes?ids=${nodeId}`,
    { headers: { 'X-Figma-Token': process.env.FIGMA_TOKEN! } }
  );
  const data = await response.json();
  const node = data.nodes[nodeId].document;
  
  return generateReactComponent(node);
}

function generateReactComponent(node: FigmaNode): string {
  const componentName = toPascalCase(node.name);
  const styles = extractStyles(node);
  const children = node.children?.map(child => generateJSX(child)).join('\n') || '';
  
  return `
import React from 'react';

export function ${componentName}() {
  return (
    <div style={${JSON.stringify(styles, null, 2)}}>
      ${children}
    </div>
  );
}
`;
}

function extractStyles(node: FigmaNode): React.CSSProperties {
  const styles: React.CSSProperties = {};
  
  // Dimensions
  if (node.absoluteBoundingBox) {
    styles.width = node.absoluteBoundingBox.width;
    styles.height = node.absoluteBoundingBox.height;
  }
  
  // Background
  if (node.fills?.length) {
    const fill = node.fills.find(f => f.visible !== false && f.type === 'SOLID');
    if (fill?.color) {
      styles.backgroundColor = rgbaToHex(fill.color);
    }
  }
  
  // Border radius
  if (node.cornerRadius) {
    styles.borderRadius = node.cornerRadius;
  }
  
  // Padding
  if (node.paddingLeft) styles.paddingLeft = node.paddingLeft;
  if (node.paddingRight) styles.paddingRight = node.paddingRight;
  if (node.paddingTop) styles.paddingTop = node.paddingTop;
  if (node.paddingBottom) styles.paddingBottom = node.paddingBottom;
  
  // Flexbox (Auto Layout)
  if (node.layoutMode && node.layoutMode !== 'NONE') {
    styles.display = 'flex';
    styles.flexDirection = node.layoutMode === 'HORIZONTAL' ? 'row' : 'column';
    styles.gap = node.itemSpacing;
    
    // Alignment
    const alignMap: Record<string, string> = {
      'MIN': 'flex-start',
      'CENTER': 'center',
      'MAX': 'flex-end',
      'SPACE_BETWEEN': 'space-between',
    };
    if (node.primaryAxisAlignItems) {
      styles.justifyContent = alignMap[node.primaryAxisAlignItems] || 'flex-start';
    }
    if (node.counterAxisAlignItems) {
      styles.alignItems = alignMap[node.counterAxisAlignItems] || 'flex-start';
    }
  }
  
  return styles;
}

function generateJSX(node: FigmaNode): string {
  const styles = extractStyles(node);
  
  if (node.type === 'TEXT') {
    return `<span style={${JSON.stringify(styles)}}>${node.characters || ''}</span>`;
  }
  
  if (node.type === 'VECTOR' || node.type === 'BOOLEAN_OPERATION') {
    return `{/* Vector: ${node.name} - export as SVG */}`;
  }
  
  const children = node.children?.map(child => generateJSX(child)).join('\n') || '';
  return `<div style={${JSON.stringify(styles)}}>${children}</div>`;
}
```

### Generate Tailwind CSS from Figma
```typescript
function figmaToTailwind(node: FigmaNode): string {
  const classes: string[] = [];
  
  // Dimensions
  if (node.absoluteBoundingBox) {
    const { width, height } = node.absoluteBoundingBox;
    classes.push(`w-[${Math.round(width)}px]`, `h-[${Math.round(height)}px]`);
  }
  
  // Background color
  if (node.fills?.length) {
    const fill = node.fills.find(f => f.visible !== false && f.type === 'SOLID');
    if (fill?.color) {
      const hex = rgbaToHex(fill.color);
      classes.push(`bg-[${hex}]`);
    }
  }
  
  // Border radius
  if (node.cornerRadius) {
    const radiusMap: Record<number, string> = {
      4: 'rounded-sm', 6: 'rounded-md', 8: 'rounded-lg',
      12: 'rounded-xl', 16: 'rounded-2xl', 9999: 'rounded-full'
    };
    classes.push(radiusMap[node.cornerRadius] || `rounded-[${node.cornerRadius}px]`);
  }
  
  // Padding
  if (node.paddingLeft === node.paddingRight && 
      node.paddingTop === node.paddingBottom &&
      node.paddingLeft === node.paddingTop) {
    classes.push(`p-[${node.paddingLeft}px]`);
  } else {
    if (node.paddingLeft) classes.push(`pl-[${node.paddingLeft}px]`);
    if (node.paddingRight) classes.push(`pr-[${node.paddingRight}px]`);
    if (node.paddingTop) classes.push(`pt-[${node.paddingTop}px]`);
    if (node.paddingBottom) classes.push(`pb-[${node.paddingBottom}px]`);
  }
  
  // Flexbox
  if (node.layoutMode && node.layoutMode !== 'NONE') {
    classes.push('flex');
    classes.push(node.layoutMode === 'HORIZONTAL' ? 'flex-row' : 'flex-col');
    if (node.itemSpacing) classes.push(`gap-[${node.itemSpacing}px]`);
    
    const justifyMap: Record<string, string> = {
      'MIN': 'justify-start', 'CENTER': 'justify-center',
      'MAX': 'justify-end', 'SPACE_BETWEEN': 'justify-between'
    };
    const alignMap: Record<string, string> = {
      'MIN': 'items-start', 'CENTER': 'items-center', 'MAX': 'items-end'
    };
    if (node.primaryAxisAlignItems) classes.push(justifyMap[node.primaryAxisAlignItems]);
    if (node.counterAxisAlignItems) classes.push(alignMap[node.counterAxisAlignItems]);
  }
  
  return classes.join(' ');
}
```

### Extract All Components from File
```typescript
interface ComponentInfo {
  key: string;
  name: string;
  description: string;
  nodeId: string;
  thumbnailUrl?: string;
}

async function getAllComponents(fileKey: string): Promise<ComponentInfo[]> {
  const response = await fetch(
    `https://api.figma.com/v1/files/${fileKey}/components`,
    { headers: { 'X-Figma-Token': process.env.FIGMA_TOKEN! } }
  );
  const data = await response.json();
  
  return data.meta.components.map((comp: any) => ({
    key: comp.key,
    name: comp.name,
    description: comp.description || '',
    nodeId: comp.node_id,
    thumbnailUrl: comp.thumbnail_url,
  }));
}

// Generate code for all components
async function generateAllComponentsCode(fileKey: string): Promise<Map<string, string>> {
  const components = await getAllComponents(fileKey);
  const codeMap = new Map<string, string>();
  
  for (const comp of components) {
    const code = await getComponentCode(fileKey, comp.nodeId);
    codeMap.set(comp.name, code);
  }
  
  return codeMap;
}
```

## Design Token Extraction

### Extract Colors
```typescript
async function extractColors(fileKey: string) {
  const file = await fetch(
    `https://api.figma.com/v1/files/${fileKey}/styles`,
    { headers }
  ).then(r => r.json());
  
  const colors = {};
  
  for (const style of file.meta.styles) {
    if (style.style_type === 'FILL') {
      const nodeData = await getStyleNode(fileKey, style.node_id);
      const fill = nodeData.fills[0];
      
      if (fill.type === 'SOLID') {
        colors[style.name] = rgbaToHex(fill.color);
      }
    }
  }
  
  return colors;
}

function rgbaToHex({ r, g, b, a = 1 }) {
  const toHex = (n) => Math.round(n * 255).toString(16).padStart(2, '0');
  return `#${toHex(r)}${toHex(g)}${toHex(b)}${a < 1 ? toHex(a) : ''}`;
}
```

### Extract Typography Tokens
```typescript
async function extractTypography(fileKey: string) {
  const response = await fetch(
    `https://api.figma.com/v1/files/${fileKey}/styles`,
    { headers: { 'X-Figma-Token': process.env.FIGMA_TOKEN! } }
  );
  const data = await response.json();
  
  const typography: Record<string, any> = {};
  
  for (const style of data.meta.styles) {
    if (style.style_type === 'TEXT') {
      const nodeResponse = await fetch(
        `https://api.figma.com/v1/files/${fileKey}/nodes?ids=${style.node_id}`,
        { headers: { 'X-Figma-Token': process.env.FIGMA_TOKEN! } }
      );
      const nodeData = await nodeResponse.json();
      const node = nodeData.nodes[style.node_id].document;
      
      typography[style.name] = {
        fontFamily: node.style?.fontFamily,
        fontWeight: node.style?.fontWeight,
        fontSize: node.style?.fontSize,
        lineHeight: node.style?.lineHeightPx,
        letterSpacing: node.style?.letterSpacing,
      };
    }
  }
  
  return typography;
}
```

### Generate Complete Design Tokens
```typescript
interface DesignTokens {
  colors: Record<string, string>;
  typography: Record<string, any>;
  spacing: Record<string, number>;
  shadows: Record<string, string>;
  radii: Record<string, number>;
}

async function generateDesignTokens(fileKey: string): Promise<DesignTokens> {
  const [colors, typography] = await Promise.all([
    extractColors(fileKey),
    extractTypography(fileKey),
  ]);
  
  return {
    colors,
    typography,
    spacing: { xs: 4, sm: 8, md: 16, lg: 24, xl: 32 },  // Extract from file
    shadows: {},  // Extract from effect styles
    radii: {},    // Extract from nodes
  };
}

// Generate CSS Variables
function tokensToCSSVariables(tokens: DesignTokens): string {
  let css = ':root {\n';
  
  // Colors
  for (const [name, value] of Object.entries(tokens.colors)) {
    const cssName = name.toLowerCase().replace(/[\s/]+/g, '-');
    css += `  --color-${cssName}: ${value};\n`;
  }
  
  // Typography
  for (const [name, style] of Object.entries(tokens.typography)) {
    const cssName = name.toLowerCase().replace(/[\s/]+/g, '-');
    css += `  --font-${cssName}-family: "${style.fontFamily}";\n`;
    css += `  --font-${cssName}-size: ${style.fontSize}px;\n`;
    css += `  --font-${cssName}-weight: ${style.fontWeight};\n`;
    css += `  --font-${cssName}-line-height: ${style.lineHeight}px;\n`;
  }
  
  css += '}\n';
  return css;
}

// Generate Tailwind Config
function tokensToTailwindConfig(tokens: DesignTokens): string {
  const colors: Record<string, string> = {};
  for (const [name, value] of Object.entries(tokens.colors)) {
    const key = name.toLowerCase().replace(/[\s/]+/g, '-');
    colors[key] = value;
  }
  
  return `
module.exports = {
  theme: {
    extend: {
      colors: ${JSON.stringify(colors, null, 6)},
      fontFamily: {
        ${Object.entries(tokens.typography).map(([name, style]) => 
          `'${name.toLowerCase()}': ['${style.fontFamily}', 'sans-serif']`
        ).join(',\n        ')}
      },
    },
  },
};
`;
}
```

## Variables API (Design Tokens 2.0)

```typescript
// Get variables (requires enterprise/organization plan)
GET https://api.figma.com/v1/files/:file_key/variables/local

// Get variable collections
GET https://api.figma.com/v1/files/:file_key/variables/local/collections

// Response structure
interface VariableCollection {
  id: string;
  name: string;
  modes: { modeId: string; name: string }[];
  variableIds: string[];
}

interface Variable {
  id: string;
  name: string;
  resolvedType: 'BOOLEAN' | 'FLOAT' | 'STRING' | 'COLOR';
  valuesByMode: Record<string, any>;
}

async function getVariables(fileKey: string) {
  const response = await fetch(
    `https://api.figma.com/v1/files/${fileKey}/variables/local`,
    { headers: { 'X-Figma-Token': process.env.FIGMA_TOKEN! } }
  );
  return response.json();
}
```

## Dev Mode Integration

### Code Snippets from Dev Mode
```typescript
// Get Dev Resources (annotations, measurements)
GET https://api.figma.com/v1/files/:file_key/dev_resources

// Create Dev Resource
POST https://api.figma.com/v1/dev_resources
{
  "dev_resource": {
    "name": "React Component",
    "url": "https://github.com/...",
    "file_key": "abc123",
    "node_id": "1:2"
  }
}
```

## Webhooks

### Setup Webhook
```typescript
POST https://api.figma.com/v2/webhooks

{
  "event_type": "FILE_UPDATE",
  "team_id": "123456",
  "endpoint": "https://your-server.com/figma-webhook",
  "passcode": "your-secret-passcode"
}

// Available events:
// - FILE_UPDATE
// - FILE_DELETE  
// - FILE_VERSION_UPDATE
// - LIBRARY_PUBLISH
// - FILE_COMMENT
```

### Handle Webhook
```typescript
app.post('/figma-webhook', async (req, res) => {
  const { passcode } = req.body;
  
  if (passcode !== process.env.FIGMA_WEBHOOK_SECRET) {
    return res.status(401).send('Unauthorized');
  }
  
  const { event_type, file_key, timestamp } = req.body;
  
  switch (event_type) {
    case 'FILE_UPDATE':
      await syncDesignTokens(file_key);
      break;
    case 'LIBRARY_PUBLISH':
      await regenerateComponents(file_key);
      break;
    case 'FILE_COMMENT':
      await notifyTeam(req.body);
      break;
  }
  
  res.status(200).send('OK');
});
```

## Complete Design-to-Code Pipeline

```typescript
// Full pipeline: Figma file → React components + tokens
async function figmaToCode(fileKey: string, outputDir: string) {
  // 1. Get all components
  const components = await getAllComponents(fileKey);
  
  // 2. Generate design tokens
  const tokens = await generateDesignTokens(fileKey);
  await fs.writeFile(
    `${outputDir}/tokens.css`,
    tokensToCSSVariables(tokens)
  );
  await fs.writeFile(
    `${outputDir}/tailwind.config.js`,
    tokensToTailwindConfig(tokens)
  );
  
  // 3. Generate React components
  for (const comp of components) {
    const code = await getComponentCode(fileKey, comp.nodeId);
    const fileName = toPascalCase(comp.name) + '.tsx';
    await fs.writeFile(`${outputDir}/components/${fileName}`, code);
  }
  
  // 4. Export icons as SVGs
  const icons = components.filter(c => c.name.startsWith('Icon/'));
  if (icons.length) {
    const iconIds = icons.map(i => i.nodeId).join(',');
    const svgResponse = await fetch(
      `https://api.figma.com/v1/images/${fileKey}?ids=${iconIds}&format=svg`,
      { headers: { 'X-Figma-Token': process.env.FIGMA_TOKEN! } }
    );
    const svgData = await svgResponse.json();
    
    for (const icon of icons) {
      const svgUrl = svgData.images[icon.nodeId];
      const svg = await fetch(svgUrl).then(r => r.text());
      await fs.writeFile(`${outputDir}/icons/${icon.name}.svg`, svg);
    }
  }
  
  console.log(`Generated ${components.length} components and ${Object.keys(tokens.colors).length} color tokens`);
}
```

## Figma Plugin Development

### Plugin Manifest (manifest.json)
```json
{
  "name": "My Figma Plugin",
  "id": "123456789",
  "api": "1.0.0",
  "main": "code.js",
  "ui": "ui.html",
  "editorType": ["figma", "figjam"],
  "capabilities": ["codegen"],
  "codegenLanguages": [
    { "label": "React", "value": "react" },
    { "label": "Vue", "value": "vue" }
  ]
}
```

### Plugin Code (code.ts)
```typescript
// Show UI
figma.showUI(__html__, { width: 400, height: 500 });

// Handle selection
figma.on('selectionchange', () => {
  const selection = figma.currentPage.selection;
  figma.ui.postMessage({ type: 'selection', nodes: selection.map(nodeToJSON) });
});

// Handle messages from UI
figma.ui.onmessage = async (msg) => {
  if (msg.type === 'export-code') {
    const node = figma.currentPage.selection[0];
    const code = generateCode(node);
    figma.ui.postMessage({ type: 'code-generated', code });
  }
};

function nodeToJSON(node: SceneNode) {
  return {
    id: node.id,
    name: node.name,
    type: node.type,
    width: node.width,
    height: node.height,
  };
}
```

## Resources

- **Figma API Docs**: https://www.figma.com/developers/api
- **Figma REST API Reference**: https://www.figma.com/developers/api#intro
- **Plugin API Docs**: https://www.figma.com/plugin-docs/
- **Variables API**: https://www.figma.com/developers/api#variables
- **Dev Mode**: https://www.figma.com/dev-mode/
- **Figma Community Plugins**: https://www.figma.com/community/plugins
