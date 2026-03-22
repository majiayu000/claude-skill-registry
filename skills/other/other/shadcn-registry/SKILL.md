---
name: shadcn-registry
description: Manages shadcn registry.json file for the Zaidan project. Creates and updates registry items for UI components, hooks, CSS files, blocks, and other registry item types. Use proactively when the user wants to add components to registry, update registry entries, give a list of files to add to the registry.
---

# Managing Shadcn Registry

This skill manages the `registry.json` file for the Zaidan project. It handles creating and updating registry items for various types: UI components, hooks, CSS files, blocks, themes, and more.

**IMPORTANT**: This skill ONLY modifies `registry.json`. It does NOT create or modify component files, hooks, or any other source files.

## Prerequisites

- The `registry.json` file must exist at the project root
- Component/hook files must already exist at their specified paths before adding to registry
- All paths should be relative to the project root (e.g., `src/registry/ui/button.tsx`)

## Registry Structure

The `registry.json` file has this structure:

```json
{
  "$schema": "https://ui.shadcn.com/schema/registry.json",
  "name": "zaidan",
  "homepage": "https://zaidan.carere.dev",
  "items": [
    // Registry items go here
  ]
}
```

## Item Types

| Type | Purpose | Typical Path |
|------|---------|--------------|
| `registry:ui` | UI components and single-file primitives | `src/registry/ui/` |
| `registry:hook` | SolidJS hooks | `src/registry/hooks/` |
| `registry:component` | Simple standalone components | `src/registry/` |
| `registry:block` | Complex components with multiple files | `src/registry/blocks/` |
| `registry:lib` | Utility and library code | `src/registry/lib/` |
| `registry:page` | Page or file-based routes | `src/registry/pages/` |
| `registry:file` | Miscellaneous files | varies |
| `registry:style` | Registry style definitions | varies |
| `registry:theme` | Theme configurations | varies |
| `registry:item` | Universal registry items | varies |

## Workflow

### Adding a UI Component

1. **Read the existing `registry.json`** to understand the current structure
2. **Verify the component file exists** at the specified path
3. **Determine dependencies**:
   - `dependencies`: npm packages (e.g., `@kobalte/core`, `lucide-solid`, `class-variance-authority`)
   - `registryDependencies`: other registry items this component depends on (e.g., `button`, `input`)
4. **Add the item** to the `items` array in alphabetical order by name
5. **Write the updated `registry.json`**

### Adding a Hook

1. **Read the existing `registry.json`**
2. **Verify the hook file exists** at `src/registry/hooks/`
3. **Determine dependencies**:
   - `dependencies`: npm packages (e.g., `@kobalte/core`, `lucide-solid`, `class-variance-authority`)
4. **Add the item** with `type: "registry:hook"`

### Adding CSS/Styling

For items that add CSS variables or styles, use the `cssVars` and `css` properties instead of files.

## Item Schema

### Basic Item (UI Component)

```json
{
  "name": "component-name",
  "type": "registry:ui",
  "dependencies": ["@kobalte/core"],
  "registryDependencies": ["button"],
  "files": [
    {
      "path": "src/registry/ui/component-name.tsx",
      "type": "registry:ui"
    }
  ]
}
```

### Hook Item

```json
{
  "name": "use-hook-name",
  "type": "registry:hook",
  "dependencies": [],
  "registryDependencies": [],
  "files": [
    {
      "path": "src/registry/hooks/use-hook-name.ts",
      "type": "registry:hook"
    }
  ]
}
```

### Block (Multi-file Component)

```json
{
  "name": "login-form",
  "type": "registry:block",
  "title": "Login Form",
  "description": "A login form with email and password fields.",
  "registryDependencies": ["button", "card", "input", "label"],
  "dependencies": [],
  "files": [
    {
      "path": "src/registry/blocks/login-form/page.tsx",
      "type": "registry:page",
      "target": "app/login/page.tsx"
    },
    {
      "path": "src/registry/blocks/login-form/login-form.tsx",
      "type": "registry:component"
    }
  ]
}
```

### Theme Item

```json
{
  "name": "custom-theme",
  "type": "registry:theme",
  "cssVars": {
    "light": {
      "background": "oklch(1 0 0)",
      "foreground": "oklch(0.141 0.005 285.823)",
      "primary": "oklch(0.546 0.245 262.881)"
    },
    "dark": {
      "background": "oklch(0.141 0.005 285.823)",
      "foreground": "oklch(1 0 0)",
      "primary": "oklch(0.707 0.165 254.624)"
    }
  }
}
```

### Style Item with CSS

```json
{
  "name": "custom-style",
  "type": "registry:style",
  "cssVars": {
    "theme": {
      "font-sans": "Inter, sans-serif"
    }
  },
  "css": {
    "@layer base": {
      "h1": { "font-size": "var(--text-2xl)" }
    },
    "@utility content-auto": {
      "content-visibility": "auto"
    }
  }
}
```

### Item with CSS Animations

```json
{
  "name": "animated-component",
  "type": "registry:component",
  "cssVars": {
    "theme": {
      "--animate-wiggle": "wiggle 1s ease-in-out infinite"
    }
  },
  "css": {
    "@keyframes wiggle": {
      "0%, 100%": { "transform": "rotate(-3deg)" },
      "50%": { "transform": "rotate(3deg)" }
    }
  },
  "files": [
    {
      "path": "src/registry/ui/animated-component.tsx",
      "type": "registry:ui"
    }
  ]
}
```

## Naming Conventions

- **Component names**: kebab-case (e.g., `alert-dialog`, `button-group`)
- **Hook names**: prefix with `use-` (e.g., `use-mobile`, `use-toast`)
- **File paths**: match the name (e.g., `alert-dialog.tsx` for `alert-dialog`)

## Examples

### Example 1: Add a Simple UI Component

User request: "Add the tooltip component to the registry"

You would:
1. Read `registry.json`
2. Verify `src/registry/ui/tooltip.tsx` exists
3. Add the item:
```json
{
  "name": "tooltip",
  "type": "registry:ui",
  "dependencies": ["@kobalte/core"],
  "registryDependencies": [],
  "files": [
    {
      "path": "src/registry/ui/tooltip.tsx",
      "type": "registry:ui"
    }
  ]
}
```
4. Insert in alphabetical order in the `items` array
5. Write the updated `registry.json`

### Example 2: Add a Hook

User request: "Add the use-toast hook to the registry"

You would:
1. Read `registry.json`
2. Verify `src/registry/hooks/use-toast.ts` exists
3. Add the item:
```json
{
  "name": "use-toast",
  "type": "registry:hook",
  "dependencies": [],
  "registryDependencies": ["sonner"],
  "files": [
    {
      "path": "src/registry/hooks/use-toast.ts",
      "type": "registry:hook"
    }
  ]
}
```
4. Write the updated `registry.json`

### Example 3: Add a Block with Multiple Files

User request: "Add the login-form block to the registry"

You would:
1. Read `registry.json`
2. Verify all block files exist
3. Add the item:
```json
{
  "name": "login-form",
  "type": "registry:block",
  "title": "Login Form",
  "description": "A login form with email and password fields.",
  "dependencies": [],
  "registryDependencies": ["button", "card", "input", "label"],
  "files": [
    {
      "path": "src/registry/blocks/login-form/page.tsx",
      "type": "registry:page",
      "target": "app/login/page.tsx"
    },
    {
      "path": "src/registry/blocks/login-form/login-form.tsx",
      "type": "registry:component"
    }
  ]
}
```
4. Write the updated `registry.json`

### Example 4: Add a Theme

User request: "Add a purple theme to the registry"

You would:
1. Read `registry.json`
2. Add the item (no files needed for themes):
```json
{
  "name": "purple-theme",
  "type": "registry:theme",
  "cssVars": {
    "light": {
      "primary": "oklch(0.546 0.245 280)",
      "primary-foreground": "oklch(0.97 0.014 280)"
    },
    "dark": {
      "primary": "oklch(0.707 0.165 280)",
      "primary-foreground": "oklch(0.97 0.014 280)"
    }
  }
}
```
3. Write the updated `registry.json`

### Example 5: Update Dependencies for Existing Component

User request: "Update the sidebar component to depend on the tooltip component"

You would:
1. Read `registry.json`
2. Find the `sidebar` item
3. Add `"tooltip"` to its `registryDependencies` array
4. Write the updated `registry.json`

## Important Notes

- Always maintain alphabetical order for items in the `items` array
- Always include both `dependencies` and `registryDependencies` arrays, even if empty
- Verify file paths are correct before adding items
- Use kebab-case for all names
- The `target` property is only needed for `registry:page` and `registry:file` types
