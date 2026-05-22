---
name: apply-shadcn
description: Apply shadcn/ui components to React pages and components. This skill should be used when styling specific pages or components with shadcn/ui in a React project that has custom theming. The user will specify which pages or components to style.
allowed-tools: Bash, Write, Edit, Read, Glob, Grep, TodoWrite, mcp__shadcn__get_project_registries, mcp__shadcn__search_items_in_registries, mcp__shadcn__view_items_in_registries, mcp__shadcn__get_item_examples_from_registries, mcp__shadcn__get_add_command_for_items, mcp__shadcn__get_audit_checklist
---

## Overview

This skill applies shadcn/ui components to React pages and components while integrating with the project's custom theme defined in `frontend/src/index.css`.

## When to Use This Skill

Use this skill when the user requests to:
- Style specific pages with shadcn/ui components
- Apply shadcn/ui to a list of components
- Add shadcn/ui styling to authentication pages, navigation, or other UI elements

The user will provide either:
- A list of page/component names to style (e.g., "Style Login.jsx, SignUp.jsx, and NavBar.jsx")
- A category of pages to style (e.g., "Style all authentication pages")

## Workflow

### Step 1: Create a Todo List

Create a todo list with one task per page or component that needs styling. Each task should be named after the file being styled (e.g., "Style Login.jsx", "Style NavBar.jsx").

### Step 2: Install Required shadcn Components

Before styling any pages, ensure the necessary shadcn components are installed. Common components needed:

```bash
npx shadcn@latest add card input button table label separator navigation-menu
```

Adjust the component list based on what the pages require.

### Step 3: Style Each Page or Component

For each page or component in the todo list, follow this process:

1. **Mark the task as in_progress** in the todo list

2. **Read the existing file** to understand its current structure and functionality

3. **Use the MCP tool to get component examples**: Call `mcp__shadcn__get_item_examples_from_registries` to retrieve usage examples for the shadcn components needed (e.g., Card, Input, Button, Table)

4. **Review the examples** to understand:
   - Proper component structure and composition
   - Correct props and patterns
   - Layout best practices

5. **Apply shadcn styling with custom theme integration**:
   - Replace existing HTML elements with shadcn components
   - Integrate custom CSS variables from `frontend/src/index.css` for colors
   - Maintain existing functionality and logic
   - Follow the theme integration guidelines below

6. **Mark the task as completed** in the todo list

7. **Move to the next page or component**

### Step 4: Verify All Tasks Complete

After styling all pages, verify that every task in the todo list is marked as completed.

### Step 5: Verify Setup

Run `npm run build` to validate imports, dependencies, and syntax

## Theme Integration Guidelines

**CRITICAL:** The project uses custom CSS variables defined in `frontend/src/index.css`. When styling components that need custom colors, use these variables instead of shadcn's default theme classes.

### Custom CSS Variables

Available custom variables from `frontend/src/index.css`:
- `--color-primary-{50-950}` - Primary color scale
- `--color-secondary-{50-950}` - Secondary color scale
- `--color-accent-{50-950}` - Accent color scale
- `--color-success-{50-900}` - Success colors
- `--color-error-{50-900}` - Error colors

### Example: Styling Primary Buttons

Use custom CSS variables with Tailwind's arbitrary value syntax:

```jsx
<Button
  className="w-full bg-[var(--color-primary-600)] hover:bg-[var(--color-primary-700)] text-white"
>
  Button Text
</Button>
```

**Why use custom variables:** The custom theme uses specific color values (e.g., purple hue at 250) that differ from shadcn's default theme. Using `bg-[var(--color-primary-600)]` ensures styled pages match the rest of the application.

## Common shadcn Components Used

- `card` - Card, CardContent, CardDescription, CardHeader, CardTitle
- `input` - Input
- `button` - Button
- `table` - Table, TableBody, TableCell, TableHead, TableHeader, TableRow
- `navigation-menu` - Navigation menu components
- `label` - Label
- `separator` - Separator

## Notes

- Always use the MCP tool before editing to understand proper component usage
- Preserve existing component functionality and logic
- Integrate custom theme variables for consistent styling
- Work through the todo list systematically, one page at a time
- Mark each task as completed immediately after finishing it
