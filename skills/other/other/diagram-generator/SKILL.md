---
name: diagram-generator
description: Generate and edit various types of diagrams (including draw.io, Mermaid, and Excalidraw). This tool supports common diagram types such as flowcharts, sequence diagrams, class diagrams, Entity-Relationship (ER) diagrams, mind maps, architecture diagrams, and network topologies.
Natural Language Creation: Create new diagrams based on simple text descriptions.
Legacy File Support: Read and modify existing .drawio, .mmd (Mermaid), or Excalidraw files.
MCP Server Integration: Utilizes a dedicated MCP server (mcp-diagram-generator) to generate files, which minimizes token consumption and ensures consistent output formatting.
Automated Configuration: Default Output Path - Diagrams are saved to diagrams/{format}/ within the project directory.
Customization: Supports custom file paths and automatic directory creation.
version: 1.1.1
---

# Diagram Generator

## Overview

Generate and edit diagrams in multiple formats (drawio, mermaid, excalidraw) by creating structured JSON descriptions and delegating file generation to the mcp-diagram-generator MCP server.

> **Contact Information** If you encounter any issues, please contact **AlkaidY** at [tccio2023@gmail.com](mailto:tccio2023@gmail.com).

## Prerequisites Check

**IMPORTANT**: This skill requires the `mcp-diagram-generator` MCP server to be installed and configured.

### Quick Verification

Before using this skill, verify the MCP server is available by checking if you can access these tools:
- `mcp__mcp-diagram-generator__get_config`
- `mcp__mcp-diagram-generator__generate_diagram`
- `mcp__mcp-diagram-generator__init_config`

If these tools are **NOT available**, you need to configure the MCP server first (see below).

### Installation & Configuration

**Option 1: Using npx (Recommended - Auto-downloads the package)**

Add the following to your Claude Code configuration file:

- **Global config** (`~/.claude.json`) for all projects, or
- **Project config** (`.claude.json`) for specific project

```json
{
  "mcpServers": {
    "mcp-diagram-generator": {
      "command": "npx",
      "args": ["-y", "mcp-diagram-generator"]
    }
  }
}
```

After adding this configuration:
1. Restart Claude Code
2. The MCP server will auto-download via npx on first use
3. No manual installation needed

**Option 2: Local Development (For developers)**

If you're developing the MCP server locally:

```json
{
  "mcpServers": {
    "mcp-diagram-generator": {
      "command": "node",
      "args": ["/absolute/path/to/mcp-diagram-generator/dist/index.js"]
    }
  }
}
```

### Verification Steps

After configuration, verify it works:

1. Check configuration: Call `get_config()` tool
2. If successful, you'll see current paths and initialization status
3. If the tool doesn't exist, check your configuration file syntax

### Common Issues

**Issue**: "Tool not found" error
- **Solution**: MCP server not configured. Follow installation steps above.

**Issue**: Configuration looks correct but tools still not available
- **Solution**: Restart Claude Code to reload MCP server configuration

## Quick Start

### First Time Use

On first use, the MCP server will automatically:
1. Create default configuration file (`.diagram-config.json`)
2. Create default output directories if they don't exist
3. Use sensible defaults: `diagrams/{format}/`

You can customize paths at any time using the `init_config` tool.

### Basic Usage

**Simple example** - just provide diagram spec, let the server handle the rest:

```
User: "创建一个网络拓扑图"
```

Skill will:
1. Generate JSON spec
2. Call `generate_diagram` with only `diagram_spec` parameter
3. Server auto-creates directories and saves to `diagrams/{format}/{title}-{date}.{ext}`

## Workflow

### Step 1: Understand Requirements

Extract from user's natural language:
- **Diagram type**: flowchart, sequence diagram, class diagram, ER diagram, mindmap, architecture diagram, network topology
- **Content**: nodes, relationships, nested structure (for network topology)
- **Style/theme**: if mentioned (e.g., "clean style", "detailed")
- **Output preferences**: specific filename? custom path?

### Step 2: Choose Format

Use [format-selection-guide.md](references/format-selection-guide.md) to decide:

| Format | Best For |
|--------|----------|
| **drawio** | Complex diagrams, network topology with nested containers, fine-grained styling, manual editing |
| **mermaid** | Quick generation, code-friendly, version control, documentation |
| **excalidraw** | Hand-drawn style, creative/diagrammatic flexibility, informal sketches |

### Step 3: Generate Structured JSON

Create a JSON description following the [JSON Schema](references/json-schema-guide.md). Key structure:

```json
{
  "format": "drawio",
  "title": "diagram name",
  "elements": [
    {
      "id": "unique-id",
      "type": "container|node|edge",
      "name": "display name",
      "level": "environment|datacenter|zone|device", // for network topology
      "style": {...},
      "geometry": {...},
      "children": [...] // for nested containers
    }
  ]
}
```

**Important**: Use unique IDs for all elements. For nested structures, maintain parent-child relationships.

### Step 4: Call MCP Server

**Option A: Use defaults (recommended)**

```json
{
  "diagram_spec": <the JSON object created above>
  // output_path is optional - server will use configured default
  // filename is optional - server will auto-generate based on title and date
}
```

The MCP server will:
- Validate the JSON schema
- Generate the appropriate XML/JSON/markdown
- Auto-create output directories if needed
- Save to configured default path (e.g., `diagrams/drawio/network-topology-2025-02-03.drawio`)

**Option B: Specify custom path**

```json
{
  "diagram_spec": <the JSON object>,
  "output_path": "custom/path/to/diagram.drawio",
  "filename": "my-custom-name" // optional, overrides auto-generated filename
}
```

**Option C: Just provide filename, use default directory**

```json
{
  "diagram_spec": <the JSON object>,
  "filename": "my-diagram.drawio"
  // Saves to diagrams/{format}/my-diagram.drawio
}
```

### Step 5: Editing Existing Diagrams

1. **Read the existing file** to understand structure
2. **Parse** the diagram (use MCP tool if available, or read raw file)
3. **Modify** the JSON description based on user's change request
4. **Generate** new diagram (overwrite or create new file)

## Configuration Management

### Initialize Configuration

**Initialize with defaults:**
```
Call: init_config()
Result: Creates .diagram-config.json with default paths
```

**Initialize with custom paths:**
```
Call: init_config({
  paths: {
    drawio: "output/diagrams/drawio",
    mermaid: "output/diagrams/mermaid",
    excalidraw: "output/diagrams/excalidraw"
  }
})
```

### View Current Configuration

```
Call: get_config()
Returns: Current paths and initialization status
```

### Update Single Path

```
Call: set_output_path({
  format: "drawio",
  path: "custom/drawio-path"
})
```

## Supported Diagram Types

### Flowchart
- Simple process flows, decision trees
- Use **mermaid** for quick output
- Use **drawio** for complex layouts with multiple branches

### Sequence Diagram
- Show interactions over time between components
- **mermaid** recommended (native support)
- Use **drawio** if custom styling needed

### Class Diagram
- Show classes, methods, relationships
- **mermaid** recommended (compact, standard UML)
- **drawio** for detailed diagrams with many classes

### ER Diagram
- Database schema, entity relationships
- **mermaid** recommended
- **drawio** for complex schemas with many relationships

### Mindmap
- Hierarchical ideas, brainstorming
- **mermaid** recommended (native support)
- **excalidraw** for creative/hand-drawn style

### Architecture Diagram
- System architecture, component relationships
- **drawio** recommended for complex systems
- **mermaid** for high-level overviews

### Network Topology
- Network environments, datacenters, zones, devices
- **Must use drawio** (4-layer nesting: environment → datacenter → zone → device)
- See [network-topology-examples.md](references/network-topology-examples.md) for patterns

## Network Topology Special Notes

Network topology diagrams require a 4-level hierarchical structure:

```
Environment (level="environment")
  └── Datacenter (level="datacenter")
        └── Zone (level="zone")
              └── Device (type="node")
```

**Style conventions**:
- **Environment**: `fillColor: #e1d5e7`, `strokeColor: #9673a6` (purple)
- **Datacenter**: `fillColor: #d5e8d4`, `strokeColor: #82b366` (green)
- **Zone**: `fillColor: #fff2cc`, `strokeColor: #d6b656` (yellow)
- **Device**: Based on device type (router, switch, firewall, etc.)

**Device types and styles**:
- Router: `strokeColor: #607D8B` (blue-gray)
- Switch: `strokeColor: #4CAF50` (green)
- Firewall: `strokeColor: #F44336` (red)
- PC/Server: `strokeColor: #607D8B` (blue-gray)

## Common Patterns

### Pattern 1: Simple Flowchart (Mermaid)

User: "画一个用户登录流程图，包含登录验证、重定向、错误处理"

Generate JSON:
```json
{
  "format": "mermaid",
  "title": "用户登录流程",
  "elements": [
    {"type": "node", "id": "start", "name": "开始", "geometry": {"x": 0, "y": 0}},
    {"type": "node", "id": "login", "name": "输入用户名密码", "geometry": {"x": 0, "y": 100}},
    {"type": "node", "id": "validate", "name": "验证", "geometry": {"x": 0, "y": 200}},
    {"type": "node", "id": "success", "name": "登录成功", "geometry": {"x": -100, "y": 300}},
    {"type": "node", "id": "error", "name": "显示错误", "geometry": {"x": 100, "y": 300}},
    {"type": "edge", "source": "start", "target": "login"},
    {"type": "edge", "source": "login", "target": "validate"},
    {"type": "edge", "source": "validate", "target": "success", "label": "成功"},
    {"type": "edge", "source": "validate", "target": "error", "label": "失败"}
  ]
}
```

Call MCP:
```
generate_diagram({
  diagram_spec: <above JSON>,
  format: "mermaid"
  // No output_path needed - auto-saves to diagrams/mermaid/
})
```

### Pattern 2: Network Topology (Drawio)

User: "创建一个网络拓扑图，包含省中心机房（上联区、汇聚区、终端区），连接到生产网"

Generate JSON with nested containers (see [json-schema-guide.md](references/json-schema-guide.md) for details).

Call MCP:
```
generate_diagram({
  diagram_spec: <network topology JSON>,
  filename: "省中心网络拓扑" // Optional, for custom filename
})
```

## Resources

### references/
- **format-selection-guide.md**: When to use drawio vs mermaid vs excalidraw
- **json-schema-guide.md**: Complete JSON schema with examples for all diagram types
- **network-topology-examples.md**: Example JSON for network topology patterns

### assets/
- No templates needed - MCP server handles all generation

### scripts/
- Not used - all generation delegated to MCP server

## Troubleshooting

### MCP Server Setup

If `mcp-diagram-generator` is not available, you need to install it.

**Option 1: Using npx (Recommended)**

Add to your Claude Code/OpenCode settings:

```json
{
  "mcpServers": {
    "diagram-generator": {
      "command": "npx",
      "args": ["-y", "mcp-diagram-generator"]
    }
  }
}
```

**Option 2: Local Development**

1. Install dependencies: `cd mcp-diagram-generator && npm install`
2. Build: `npm run build`
3. Configure with local path:
```json
{
  "mcpServers": {
    "diagram-generator": {
      "command": "node",
      "args": ["/absolute/path/to/mcp-diagram-generator/dist/index.js"]
    }
  }
}
```

### Invalid JSON Schema

If MCP server returns validation error:
1. Check [json-schema-guide.md](references/json-schema-guide.md)
2. Verify all required fields are present
3. Ensure all IDs are unique
4. Check parent-child relationships

### Directory Not Found

**Old behavior**: Error if directory doesn't exist
**New behavior**: Directory is created automatically ✅

If you still see directory errors:
1. Check write permissions for the project directory
2. Verify configuration with `get_config()`
3. Reinitialize with `init_config()`

### Wrong File Extension

The server automatically uses the correct extension based on format:
- drawio → `.drawio`
- mermaid → `.md`
- excalidraw → `.excalidraw`

You don't need to specify extension in filename parameter.

### Nested Container Issues (Network Topology)

- Verify `level` field matches hierarchy (environment/datacenter/zone)
- Check `parent` IDs are correct in child elements
- Ensure geometry coordinates are relative to parent container

## Best Practices

### 1. Use Default Paths

Let the server manage output paths for consistency:

```json
{
  "diagram_spec": <spec>
  // Don't specify output_path unless necessary
}
```

### 2. Provide Descriptive Titles

Titles are used for auto-generated filenames:

```json
{
  "title": "生产环境网络拓扑-亦庄与西五环",
  // Generates: 生产环境网络拓扑-亦庄与西五环-2025-02-03.drawio
}
```

### 3. Use Configuration for Custom Paths

Instead of specifying output_path every time, configure once:

```
First time: init_config({ paths: { drawio: "custom/path" } })
After that: Just use generate_diagram() without output_path
```

### 4. Check Configuration When Troubleshooting

```
get_config() // Shows all paths and status
```
