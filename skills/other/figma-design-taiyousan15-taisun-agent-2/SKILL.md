---
name: figma-design
description: Use this skill when working with Figma designs to generate code. Converts Figma layouts, components, and styles into production-ready code. Triggers on keywords like "Figma", "design to code", "implement this design", or when referencing Figma file URLs.
---

# Figma Design-to-Code

This skill enables AI-powered code generation from Figma designs using the Figma MCP server.

## Problem Solved

Traditional design-to-code workflow:
- Manual inspection of Figma designs
- Guessing spacing, colors, and typography
- Multiple iterations to match design
- Inconsistent implementation

With Figma MCP:
- Direct access to design specifications
- Exact colors, spacing, typography values
- Component structure understanding
- One-shot accurate implementation

## When to Use

- Implementing UI from Figma designs
- Converting Figma components to React/Vue/etc.
- Extracting design tokens (colors, spacing, typography)
- Understanding component hierarchy
- Ensuring pixel-perfect implementation

## Available Tools

### 1. get_file
Retrieves complete Figma file data including all pages, frames, and components.

```
Input: Figma file key (from URL)
Output: Complete design structure with properties
```

### 2. get_file_nodes
Gets specific nodes from a Figma file by their IDs.

```
Input: File key + node IDs
Output: Detailed node information
```

### 3. get_images
Exports images from Figma nodes in various formats.

```
Input: File key + node IDs + format (png, jpg, svg, pdf)
Output: Image URLs
```

### 4. get_components
Lists all components in a file or team library.

```
Input: File key or team ID
Output: Component list with metadata
```

### 5. get_styles
Retrieves style definitions (colors, text, effects).

```
Input: File key
Output: Style definitions
```

## Example Usage

### Basic Design Implementation

```
User: このFigmaデザインを実装して
https://www.figma.com/file/ABC123/MyDesign

AI: [Calls get_file with file key ABC123]
    [Analyzes component structure]
    [Extracts colors, spacing, typography]
    [Generates React/CSS code]

Output:
- Component structure matching Figma layers
- Exact CSS values from design
- Responsive breakpoints if defined
```

### Component Extraction

```
User: FigmaのButtonコンポーネントをReactで作って

AI: [Calls get_components]
    [Finds Button component]
    [Gets variants and properties]
    [Generates typed React component]
```

### Design Token Export

```
User: Figmaからデザイントークンを抽出して

AI: [Calls get_styles]
    [Extracts color palette]
    [Extracts typography scale]
    [Generates CSS variables or Tailwind config]
```

## Required Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `FIGMA_API_KEY` | Figma Personal Access Token | Yes |

## Setup

### 1. Get Figma API Token

1. Go to Figma account settings
2. Navigate to "Personal access tokens"
3. Generate new token with read access
4. Copy the token

### 2. Set Environment Variable

```bash
# Add to .env
FIGMA_API_KEY=figd_xxxxxxxxxxxxxxxx
```

Or in shell:
```bash
export FIGMA_API_KEY="figd_xxxxxxxxxxxxxxxx"
```

## Best Practices

1. **Provide Figma URL directly**
   ```
   ✅ "このデザインを実装して: https://www.figma.com/file/..."
   ❌ "このデザインを実装して" (URLなし)
   ```

2. **Specify target framework**
   ```
   「React + Tailwindで実装して」
   「Vue 3のComposition APIで」
   ```

3. **Request specific components**
   ```
   「HeaderとFooterだけ実装して」
   「モバイル版のみ」
   ```

4. **Combine with Context7 for framework docs**
   ```
   「use context7 でTailwind v4を使ってこのFigmaを実装して」
   ```

## Integration with TAISUN

Figma MCP is automatically available via MCP. The system will:
1. Detect Figma URLs in prompts
2. Extract file keys and node IDs
3. Fetch design data
4. Generate framework-specific code

## Figma URL Structure

```
https://www.figma.com/file/{file_key}/{file_name}?node-id={node_id}
                          ^^^^^^^^^^              ^^^^^^^^^^
                          Required                Optional (specific frame)
```

## Sources

- [Figma MCP Server Guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server)
- [figma-developer-mcp NPM](https://www.npmjs.com/package/figma-developer-mcp)
- [Figma Developer Docs](https://developers.figma.com/docs/figma-mcp-server/)
