---
name: create-cell-renderer
description: Create a custom grid cell renderer for Datagrok
argument-hint: "[cell-type] [package-path]"
---

# Create Cell Renderer

Create a custom cell renderer for the Datagrok grid/table viewer.

## Usage

```
/create-cell-renderer [cell-type] [package-path]
```

## Instructions

When this skill is invoked, help the user create a custom cell renderer that extends `DG.GridCellRenderer`.

### Step 1: Create the renderer class

Create a new TypeScript file in the package's `src/` directory (e.g., `src/renderers/my-renderer.ts`).

The class must extend `DG.GridCellRenderer` and implement:

- `get name()` - unique renderer name
- `get cellType()` - the cell type string (e.g., `'piechart'`, `'barchart'`)
- `render(g, x, y, w, h, gridCell, cellStyle)` - main drawing method using CanvasRenderingContext2D
- `renderSettings(gridColumn)` (optional) - returns an HTMLElement for renderer settings UI

```ts
export class MyRenderer extends DG.GridCellRenderer {
  get name() { return 'My Renderer'; }
  get cellType() { return 'mytype'; }

  render(g: CanvasRenderingContext2D, x: number, y: number, w: number, h: number,
    gridCell: DG.GridCell, cellStyle: DG.GridCellStyle): void {
    // Draw using Canvas 2D API within the bounds (x, y, w, h)
  }

  renderSettings(gridColumn: DG.GridColumn): HTMLElement | null {
    // Optional: return UI element for settings
    return null;
  }
}
```

### Step 2: Register the renderer

Use the decorator approach (preferred for `datagrok-tools` >= 4.12.x):

```ts
@grok.decorators.cellRenderer({
  cellType: 'mytype',
  virtual: true,
})
export class MyRenderer extends DG.GridCellRenderer {
  /* ... */
}
```

The `virtual: true` flag is used for summary/calculated columns.

Or use the function annotation approach in `package.ts`:

```ts
//name: myRenderer
//tags: cellRenderer
//meta.cellType: mytype
//meta.virtual: true
//output: grid_cell_renderer result
export function myRendererFunc() {
  return new MyRenderer();
}
```

### Step 3: Build and publish

The decorator approach auto-generates a `package.g.ts` file via `FuncGeneratorPlugin` during build. This file must be committed.

```bash
npm run build
grok publish
```

### Key points

- The `cellType` string links the renderer to summary columns of that type
- The `render` method receives a Canvas 2D context; draw within the bounding box (x, y, w, h)
- For real examples, see the PowerGrid package: `public/packages/PowerGrid/src/sparklines/`
- Both decorator and function annotation approaches are equivalent; prefer decorators

## Behavior

1. Ask the user what type of cell visualization they want if not specified
2. Create the renderer class file with the appropriate drawing logic
3. Register it using the decorator approach (or function annotation if the user prefers)
4. Ensure the package imports are correct (`import * as DG from 'datagrok-api/dg'`, `import * as grok from 'datagrok-api/grok'`)
5. Remind the user to build and publish the package
