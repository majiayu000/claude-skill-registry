---
name: gluestack-mcp-tools
description: Use when discovering, exploring, or retrieving gluestack-ui components via MCP tools. Provides access to component source code, variants, demos, and metadata.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# gluestack-ui MCP Tools

Expert knowledge for using the gluestack-ui MCP server tools to discover, explore, and retrieve component source code and metadata.

## Overview

The gluestack-ui MCP server provides direct access to the gluestack-ui component library through 6 specialized tools. Use these tools to explore available components, understand their variants, retrieve source code, and access Storybook demos.

## When to Use These Tools

Use the MCP tools when you need to:

- Discover what components are available in gluestack-ui
- Get the actual source code for a component to copy into a project
- Understand the variants (NativeWind, Themed, Unstyled) of a component
- Access Storybook demos showing component usage patterns
- Retrieve TypeScript props and dependencies for a component
- Navigate the gluestack-ui monorepo structure

## Available Tools

### list_components

Lists all 70+ gluestack-ui components with their names and basic descriptions.

**When to use:** Start here when you need to know what components are available or find a component by name.

**Example workflow:**

1. Call `list_components` to see all available components
2. Identify the component that matches your needs
3. Use `get_component` or `get_component_metadata` for details

### list_component_variants

Shows the available style variants for a specific component: NativeWind, Themed, and Unstyled.

**When to use:** After identifying a component, use this to understand which styling approaches are supported.

**Variants explained:**

- **NativeWind**: Tailwind CSS classes for React Native (recommended for new projects)
- **Themed**: Token-based theming with design system integration
- **Unstyled**: Base component with no styles (for complete customization)

### get_directory_structure

Navigate the gluestack-ui monorepo to understand the package organization.

**When to use:** When you need to understand how gluestack-ui organizes its packages or find specific files within the repository.

### get_component

Retrieves the complete source code for any gluestack-ui component.

**When to use:** When you need to copy component code into your project or understand the implementation details.

**Example workflow:**

1. Use `list_components` to find the component name
2. Use `list_component_variants` to choose a variant
3. Call `get_component` with the component name and variant
4. Copy the source code into your project's `components/ui/` directory

### get_component_demo

Accesses Storybook examples showing real-world usage patterns for components.

**When to use:** When you need to see how a component is used in practice, including prop combinations and composition patterns.

**What you get:**

- Working code examples
- Different prop combinations
- Composition patterns with sub-components
- Interactive states and variations

### get_component_metadata

Retrieves TypeScript props, dependencies, and other metadata for a component.

**When to use:** When you need to understand the TypeScript interface, required props, or peer dependencies for a component.

**Information provided:**

- TypeScript prop types and interfaces
- Required vs optional props
- Default values
- Peer dependencies
- Import statements

## Common Workflows

### Adding a New Component to Your Project

1. **Discover**: `list_components` - Find the component you need
2. **Explore variants**: `list_component_variants` - Choose NativeWind, Themed, or Unstyled
3. **Get source**: `get_component` - Retrieve the full source code
4. **Check demos**: `get_component_demo` - See usage examples
5. **Copy to project**: Add the code to your `components/ui/` directory

### Understanding Component API

1. **Get metadata**: `get_component_metadata` - See TypeScript props
2. **Check demos**: `get_component_demo` - See prop usage in context
3. **Read source**: `get_component` - Understand the implementation

### Exploring Available Components

1. **List all**: `list_components` - See the full component library
2. **Check structure**: `get_directory_structure` - Understand organization
3. **Review demos**: `get_component_demo` - See component capabilities

## Best Practices

### 1. Start with Discovery

Always use `list_components` first when exploring. This gives you the canonical names to use with other tools.

```
# Good: Start with discovery
1. list_components -> find "Button"
2. get_component("Button", "nativewind")

# Avoid: Guessing component names
get_component("Btn") -> might not find it
```

### 2. Choose the Right Variant

- **NativeWind**: Best for new projects using Tailwind CSS
- **Themed**: Best when you have an existing design token system
- **Unstyled**: Best when you need complete styling control

### 3. Check Demos Before Implementing

The Storybook demos show real-world usage patterns that may reveal:

- Required composition patterns (e.g., Button needs ButtonText)
- Prop combinations that work well together
- Edge cases and accessibility considerations

### 4. Verify Dependencies

Use `get_component_metadata` to understand:

- Peer dependencies that need to be installed
- Other components that are used internally
- TypeScript types that may need importing

## Environment Configuration

The MCP server can operate in two modes:

### GitHub Mode (Default)

Fetches components directly from the gluestack-ui GitHub repository.

```bash
# Optional: Increase API rate limits
export GITHUB_TOKEN="your-token-here"
```

### Local Mode

Uses a local clone of the gluestack-ui repository for offline access.

```bash
# Point to your local clone
export GLUESTACK_PATH="/path/to/gluestack-ui"
```

## Integration with Other Skills

Combine MCP tools with other jutsu-gluestack skills:

- **gluestack-components**: After getting source code, use component skill for implementation patterns
- **gluestack-theming**: Use with Themed variant components for design token integration
- **gluestack-accessibility**: Ensure retrieved components are implemented accessibly

## Troubleshooting

### Component Not Found

- Verify the exact component name using `list_components`
- Component names are case-sensitive
- Some components may be grouped (e.g., FormControl components)

### Rate Limiting

If using GitHub mode without a token:

- Set `GITHUB_TOKEN` for increased limits
- Or clone the repo locally and set `GLUESTACK_PATH`

### Outdated Components

The MCP server fetches from the latest gluestack-ui repository. If you need a specific version:

- Clone the specific version locally
- Set `GLUESTACK_PATH` to your local clone
