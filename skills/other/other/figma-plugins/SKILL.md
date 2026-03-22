---
name: figma-plugins
description: "Build Figma plugins with full Plugin API access. Use when creating plugins for Figma, FigJam, Slides, or Dev Mode that manipulate designs, generate content, export assets, manage styles/variables, work with components, integrate external services, or monetize with payments. Covers manifest configuration, sandbox architecture, UI development with React, node manipulation, auto layout, text/font handling, image processing, variables (design tokens), annotations, codegen, payments, data storage, and publishing. Also trigger for Figma Slides plugin development, Dev Mode codegen plugins, or any work involving the Figma Plugin API."
---

# Figma Plugin Development

## Architecture Overview

Figma plugins consist of three parts:

1. **manifest.json** — Configuration, permissions, and capabilities
2. **Main code** (code.ts) — Runs in QuickJS sandbox with `figma` API access
3. **UI** (optional) — HTML/CSS/JS iframe with browser APIs

```
┌─────────────────────────────────────────────────────────┐
│  MAIN THREAD (Sandbox)     │     UI IFRAME (Browser)   │
│  ✓ figma global API        │     ✓ DOM, fetch, Canvas  │
│  ✓ Document manipulation   │     ✓ React/Vue/Svelte    │
│  ✓ Native fetch API        │     ✓ WebSockets          │
│  ✗ No DOM access           │     ✗ No figma API        │
│            └────── postMessage ──────┘                  │
└─────────────────────────────────────────────────────────┘
```

**Important**: The sandbox now has a native **Fetch API** — network requests no longer require the UI iframe.

## Quick Start

### Minimal manifest.json
```json
{
  "name": "My Plugin",
  "id": "000000000000000000",
  "api": "1.0.0",
  "main": "code.js",
  "editorType": ["figma"],
  "documentAccess": "dynamic-page"
}
```

### Minimal Plugin (No UI)
```typescript
const rect = figma.createRectangle();
rect.fills = [figma.util.solidPaint('#FF5500')];
figma.currentPage.appendChild(rect);
figma.closePlugin('Created rectangle');
```

### Plugin with UI
```typescript
// code.ts
figma.showUI(__html__, { width: 300, height: 200, themeColors: true });
figma.ui.onmessage = async (msg) => {
  if (msg.type === 'create-rect') {
    const rect = figma.createRectangle();
    rect.resize(msg.width, msg.height);
    figma.currentPage.appendChild(rect);
  }
  figma.closePlugin();
};
```
```html
<!-- ui.html -->
<button id="create">Create</button>
<script>
  document.getElementById('create').onclick = () => {
    parent.postMessage({ pluginMessage: { type: 'create-rect', width: 100, height: 100 } }, '*');
  };
</script>
```

## Manifest Configuration

### Required Fields
| Field | Description |
|-------|-------------|
| `name` | Plugin name in Figma menu |
| `id` | Unique ID (assigned by Figma on publish) |
| `api` | API version, always `"1.0.0"` |
| `main` | Path to compiled JavaScript entry |
| `editorType` | Array: `"figma"`, `"figjam"`, `"dev"`, `"slides"`, `"buzz"` |
| `documentAccess` | **Always `"dynamic-page"`** — mandatory for all new plugins |

### Editor Types
Five editor types with distinct API surfaces:
- **`"figma"`** — Full design editor (default)
- **`"figjam"`** — Whiteboard (stickies, connectors, tables, stamps, timer)
- **`"dev"`** — Dev Mode (read-only, codegen, inspect, dev resources)
- **`"slides"`** — Figma Slides (SlideNode, SlideRowNode, transitions)
- **`"buzz"`** — Figma Buzz (marketing assets, smart resize)

Invalid combinations: `["figjam", "dev"]` and `["slides", "dev"]`.

### Permissions
```json
{ "permissions": ["currentuser", "activeusers", "fileusers", "teamlibrary", "payments"] }
```

### Capabilities
```json
{ "capabilities": ["codegen", "inspect", "textreview", "vscode"] }
```
- `codegen` — Code generation in Dev Mode (requires `codegenLanguages`)
- `inspect` — Custom inspect panel in Dev Mode
- `textreview` — Text review/linting (fires `textreview` event)
- `vscode` — VS Code integration

### Network Access
```json
{
  "networkAccess": {
    "allowedDomains": ["api.example.com", "*.example.com"],
    "reasoning": "Required for fetching data from our API",
    "devAllowedDomains": ["http://localhost:3000"]
  }
}
```
Supports wildcards, WebSocket schemes (`ws://`, `wss://`), `["none"]`, or `["*"]` (unrestricted, requires `reasoning`). Plugin iframes have a `null` origin — CORS with `Access-Control-Allow-Origin: *` is required on target servers.

### Menu Commands and Mode
```json
{
  "menu": [
    { "name": "Create Shape", "command": "create" },
    { "separator": true },
    { "name": "Settings", "command": "settings" }
  ]
}
```
```typescript
figma.on('run', ({ command }) => {
  if (command === 'settings') figma.showUI(__uiFiles__['settings']);
});
figma.mode // 'default' | 'textreview' | 'inspect' | 'codegen' | 'linkpreview' | 'auth'
```

## Project Setup

### TypeScript Configuration
```bash
npm init -y
npm install --save-dev typescript @figma/plugin-typings esbuild
```
**tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2020", "lib": ["ES2020"], "strict": true,
    "typeRoots": ["./node_modules/@types", "./node_modules/@figma"],
    "outDir": "./dist"
  },
  "include": ["src/**/*.ts"]
}
```
Current `@figma/plugin-typings`: **1.121.0**. Use `eslint-plugin-figma-plugins` to catch deprecated sync API calls.

### Build with esbuild
```javascript
import * as esbuild from 'esbuild';
await esbuild.build({
  entryPoints: ['src/code.ts'], bundle: true, outfile: 'dist/code.js',
  target: 'es2020', minify: process.argv.includes('--minify'),
});
```

## Essential Patterns

### Selection Handling
```typescript
const selection = figma.currentPage.selection;
if (selection.length === 0) {
  figma.notify('Select at least one layer', { error: true });
  figma.closePlugin();
  return;
}
for (const node of selection) {
  if (node.type === 'TEXT') { /* process */ }
}
```

### Node Creation
```typescript
const rect = figma.createRectangle();
const frame = figma.createFrame();
const text = figma.createText();
const component = figma.createComponent();
const section = figma.createSection();
const slide = figma.createSlide();       // Slides
const slideRow = figma.createSlideRow(); // Slides

node.x = 100; node.y = 200;
node.resize(300, 200);
frame.appendChild(rect);
```

### Colors and Fills
**RGB values are 0-1, not 0-255.**
```typescript
const solidPaint = figma.util.solidPaint('#FF5500');
rect.fills = [{ type: 'SOLID', color: { r: 1, g: 0.5, b: 0 }, opacity: 0.8 }];

// CRITICAL: Clone before modifying — fills/strokes/effects are read-only
const fills = JSON.parse(JSON.stringify(rect.fills));
fills[0].color.r = 0.5;
rect.fills = fills;
```

### Text (MUST Load Fonts)
```typescript
const text = figma.createText();
await figma.loadFontAsync({ family: 'Inter', style: 'Regular' });
text.characters = 'Hello World';
text.fontSize = 24;
text.fontName = { family: 'Inter', style: 'Bold' };

text.setRangeFontSize(0, 5, 32);
text.setRangeFills(0, 5, [figma.util.solidPaint('#FF0000')]);
text.setRangeHyperlink(0, 5, { type: 'URL', value: 'https://example.com' });

if (text.fontName === figma.mixed) {
  const fonts = text.getRangeAllFontNames(0, text.characters.length);
  await Promise.all(fonts.map(f => figma.loadFontAsync(f)));
}
```

### Auto Layout
```typescript
const frame = figma.createFrame();
frame.layoutMode = 'HORIZONTAL'; // 'VERTICAL' | 'NONE'
frame.primaryAxisSizingMode = 'AUTO';
frame.counterAxisSizingMode = 'AUTO';
frame.itemSpacing = 16;
frame.paddingTop = frame.paddingBottom = 20;
frame.paddingLeft = frame.paddingRight = 16;
frame.primaryAxisAlignItems = 'CENTER';
frame.counterAxisAlignItems = 'CENTER';
frame.layoutWrap = 'WRAP';
frame.counterAxisSpacing = 12;
child.layoutSizingHorizontal = 'FILL'; // 'FIXED' | 'HUG' | 'FILL'
```

### Variables (Design Tokens)
Variables are the API for design tokens. See [references/variables-api.md](references/variables-api.md) for the full reference.
```typescript
const collection = figma.variables.createVariableCollection('Colors');
const primaryColor = figma.variables.createVariable('primary', collection, 'COLOR');
primaryColor.setValueForMode(collection.defaultModeId, { r: 0.2, g: 0.4, b: 1 });

rect.setBoundVariable('fills', primaryColor);       // 30+ bindable fields
rect.setBoundVariable('cornerRadius', radiusVar);
rect.setBoundVariable('itemSpacing', spacingVar);

const allColors = await figma.variables.getLocalVariablesAsync('COLOR');
const libVar = await figma.variables.importVariableByKeyAsync(key);
```

### Annotations
```typescript
node.annotations = [{
  label: 'Ready for development',
  properties: [{ type: 'fills' }, { type: 'width' }, { type: 'fontSize' }]
}];
const categories = await figma.annotations.getAnnotationCategoriesAsync();
```

### Components and Instances
```typescript
const component = figma.createComponent();
component.addComponentProperty("Label", "TEXT", "Button");
component.addComponentProperty("Disabled", "BOOLEAN", false);
component.addComponentProperty("Icon", "INSTANCE_SWAP", iconId, {
  preferredValues: [{ type: 'COMPONENT', key: starIcon.key }]
});

const instance = component.createInstance();
instance.setProperties({ 'Label#0:1': 'Submit' });
const main = await instance.getMainComponentAsync(); // ASYNC required
```

### Data Storage
```typescript
node.setPluginData('key', JSON.stringify({ value: 1 }));
const data = JSON.parse(node.getPluginData('key') || '{}');

await figma.clientStorage.setAsync('prefs', { theme: 'dark' });
const prefs = await figma.clientStorage.getAsync('prefs');
```

### Images
```typescript
const image = await figma.createImageAsync('https://example.com/image.png');
rect.fills = [{ type: 'IMAGE', imageHash: image.hash, scaleMode: 'FILL' }];
const bytes = await node.exportAsync({ format: 'PNG', constraint: { type: 'SCALE', value: 2 } });
```

### Payments (Monetization)
Requires `"payments"` in manifest `permissions`.
```typescript
const { status } = figma.payments;
if (status.type === 'UNPAID') {
  await figma.payments.initiateCheckoutAsync({ interstitial: 'TRIAL_ENDED' });
} else if (status.type === 'PAID') { /* Full access */ }

const secondsSinceFirstRun = figma.payments.getUserFirstRanSecondsAgo();
```

## UI Communication
```typescript
figma.ui.postMessage({ type: 'data', items: [1, 2, 3] });           // code → UI
parent.postMessage({ pluginMessage: { type: 'action', data: 123 } }, '*'); // UI → code
```

### Theme CSS Variables
With `themeColors: true`, detect dark mode via `.figma-dark` on `<body>`:
```css
body { background: var(--figma-color-bg); color: var(--figma-color-text); }
.button { background: var(--figma-color-bg-brand); color: var(--figma-color-text-onbrand); }
```

### Plugin UI Libraries
- **`@create-figma-plugin/ui`** (v4+) — Best option. Preact components matching Figma UI3.
- **`figma-plugin-ds`** — Vanilla CSS/JS, older UI2 style.
- Figma's **UI3 Kit** is a design file only (no code components).

## Events
```typescript
figma.on('run', ({ command, parameters }) => { });
figma.on('selectionchange', () => { });
figma.on('currentpagechange', () => { });
figma.on('documentchange', (event) => { /* event.documentChanges */ });
figma.on('drop', (event) => { return false; });
figma.on('stylechange', (event) => { });
figma.on('close', () => { /* SYNC ONLY */ });
figma.currentPage.on('nodechange', ({ nodeChanges }) => { }); // page-level
```

## Performance
```typescript
figma.skipInvisibleInstanceChildren = true; // ALWAYS enable
const texts = figma.currentPage.findAllWithCriteria({ types: ['TEXT'] });
const tagged = figma.currentPage.findAllWithCriteria({ pluginData: { keys: ['myKey'] } });
await page.loadAsync(); // load only needed pages
```

## Critical Rules
1. **Always call `figma.closePlugin()`** — Plugin runs forever otherwise
2. **Use `documentAccess: "dynamic-page"`** — Mandatory for all new plugins
3. **Use async API methods** — Sync versions are deprecated. Use `Async` variants.
4. **Load fonts before text changes** — Throws without loaded font
5. **Clone arrays before modifying** — fills, effects, strokes are read-only
6. **No async in `close` event** — Must be synchronous
7. **Declare network domains** — CSP blocks undeclared domains
8. **RGB values are 0-1** — Not 0-255
9. **UI messages need `pluginMessage` wrapper** — `{ pluginMessage: data }`
10. **Dev Mode plugins are read-only** — Cannot create or modify nodes
11. **Codegen `generate` has 15s timeout** — No `showUI()` inside it

## References
- **Full API Reference**: See [references/api-reference.md](references/api-reference.md) for node types (35), methods, properties, text API, components
- **Variables API**: See [references/variables-api.md](references/variables-api.md) for design tokens — collections, modes, binding, scopes
- **Editors & Codegen**: See [references/editors-codegen.md](references/editors-codegen.md) for FigJam, Slides, Buzz, Dev Mode, codegen, dev resources, annotations
- **Publishing**: See [references/publishing.md](references/publishing.md) for review, payments setup, distribution

## Debugging
```typescript
console.log('Debug:', value);  // Plugins > Development > Open Console
figma.notify('Status message');
figma.notify('Error', { error: true, timeout: 5000 });
```
