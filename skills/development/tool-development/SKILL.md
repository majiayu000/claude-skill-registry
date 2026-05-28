---
name: tool-development
description: Guidelines for creating and modifying tools in the NimbusImage application including template structure, interface elements, and implementation patterns.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Edit
  - Write
  - Task
  - TodoWrite
user-invocable: true
---

# NimbusImage Tool Development

Guidelines for creating and modifying tools in the NimbusImage application.

## Overview

Tools in NimbusImage are configured through JSON templates and implemented in Vue components. The system supports manual annotation tools, selection tools, AI-powered tools, worker-based tools, and more.

## Key Files

- `public/config/templates.json` - Tool template definitions
- `src/tools/creation/ToolTypeSelection.vue` - Tool selection dialog
- `src/tools/creation/ToolConfiguration.vue` - Tool configuration form
- `src/components/AnnotationViewer.vue` - Tool interaction logic
- `src/store/model.ts` - TypeScript types including `TToolType`

## Template Structure

Each tool template in `templates.json` has:

```json
{
  "name": "Tool Section Name",
  "type": "toolType",
  "shortName": "Optional short name",
  "interface": [
    {
      "name": "Interface Element Name",
      "id": "elementId",
      "type": "elementType",
      "isSubmenu": true,
      "advanced": false,
      "meta": {}
    }
  ]
}
```

### Interface Element Types

| Type | Component | Purpose |
|------|-----------|---------|
| `annotation` | AnnotationConfiguration | Shape selection |
| `select` | v-select | Dropdown options |
| `checkbox` | v-checkbox | Boolean toggle |
| `radio` | v-radio-group | Single choice |
| `tags` | TagPicker | Tag selection |
| `dockerImage` | Worker selector | Docker worker tools |
| `restrictTagsAndLayer` | TagAndLayerRestriction | Filter annotations |

### Submenu Interface

One interface element should have `isSubmenu: true`. This creates the tool variants shown in the selection dialog. For `select` type submenus, each item in `meta.items` becomes a separate tool option.

## Adding a New Tool

### Step 1: Define Template

Add to `templates.json`:

```json
{
  "name": "My Tool Category",
  "type": "myTool",
  "interface": [
    {
      "name": "Tool Mode",
      "id": "mode",
      "type": "select",
      "isSubmenu": true,
      "meta": {
        "items": [
          {
            "text": "Mode A",
            "value": "mode_a",
            "description": "Brief description of Mode A"
          }
        ]
      }
    }
  ]
}
```

### Step 2: Add Type Definition

In `src/store/model.ts`, add to `TToolType`:

```typescript
export type TToolType =
  | "annotation"
  | "selection"
  // ... existing types
  | "myTool";
```

### Step 3: Implement Logic

In `src/components/AnnotationViewer.vue`:

**Set annotation mode** in `refreshAnnotationMode()`:
```typescript
case "myTool":
  this.geoJSAnnotationMode = "point"; // or null for custom handling
  break;
```

**Handle annotations** in `handleAnnotationChange()`:
```typescript
case "myTool":
  // Process the annotation/interaction
  break;
```

## Tool Descriptions

Add descriptions to make tools more discoverable:

```json
{
  "text": "Tool Name",
  "value": "tool_value",
  "description": "Brief action-oriented description"
}
```

Keep descriptions under 50 characters. Use action verbs: "Click to...", "Draw to...", "Select...".

## Featured Tools

Configure `public/config/featuredTools.json`:

```json
{
  "featuredTools": ["Tool Name 1", "Tool Name 2"]
}
```

Names must match the `text` field exactly.

## Docker Worker Tools

Worker-based tools use the `dockerImage` interface type. Workers are registered with labels:

- `interfaceName` - Display name
- `interfaceCategory` - Category for grouping
- `description` - Tool description
- `isAnnotationWorker` - Must be set for annotation workers
- `annotationShape` - Default output shape

## Common Patterns

### Direct Mouse Handling

For tools that don't create visible annotations during interaction:

```typescript
case "myTool":
  this.geoJSAnnotationMode = null;
  this.annotationLayer.bindEvent("mouseclick", this.handleMyToolClick);
  break;
```

### Hit Testing

Find annotations at a click location:

```typescript
const fakeAnnotation = { coordinates: [clickCoords], shape: "point" };
const hits = this.getSelectedAnnotationsFromAnnotation(fakeAnnotation);
```

### Updating Annotations

```typescript
await annotationStore.updateAnnotationsPerId({
  annotationsById: { [annotationId]: { tags: newTags } },
});
```

## Category Colors

Tools are color-coded by category in the selection dialog. To add a new category color, edit `ToolTypeSelection.vue`:

1. Add SCSS variable: `$color-mycategory: #hexcolor;`
2. Add to `categoryClassMap`: `"My Category": "category-mycategory"`
3. Add class: `.category-mycategory { @include category-colors($color-mycategory); }`
