---
name: create-custom-viewer
description: Develop a custom JavaScript viewer extending DG.JsViewer with properties, rendering, and interactivity
---

# Create a Custom Viewer

Help the user develop a custom interactive viewer for Datagrok by extending `DG.JsViewer`.

## Usage
```
/create-custom-viewer [viewer-name] [--library <d3|echarts|plotly>]
```

## Instructions

### 1. Scaffold the viewer

From the package directory:
```shell
grok add viewer <ViewerName>
```

This creates a viewer class file. The naming convention is to add a `Viewer` postfix to the class name (e.g., `AwesomeViewer`).

### 2. Define the viewer class

Create a subclass of `DG.JsViewer` in a separate file (e.g., `src/awesome-viewer.ts`):

```typescript
import * as DG from 'datagrok-api/dg';
import * as ui from 'datagrok-api/ui';

export class AwesomeViewer extends DG.JsViewer {
  constructor() {
    super();
    // Register properties (appear in the context panel)
    this.splitColumnName = this.string('splitColumnName', 'site');
    this.valueColumnName = this.int('valueColumnName', 'age');
    this.valueAggrType = this.string('valueAggrType', 'avg', { choices: ['avg', 'count', 'sum'] });
    this.color = this.string('color', 'steelblue', { choices: ['darkcyan', 'seagreen', 'steelblue'] });
    this.initialized = false;
  }

  onTableAttached() {
    this.init();
    this.subs.push(DG.debounce(this.dataFrame.selection.onChanged, 50).subscribe((_) => this.render()));
    this.subs.push(DG.debounce(this.dataFrame.filter.onChanged, 50).subscribe((_) => this.render()));
    this.subs.push(DG.debounce(ui.onSizeChanged(this.root), 50).subscribe((_) => this.render(false)));
    this.render();
  }

  detach() {
    this.subs.forEach(sub => sub.unsubscribe());
  }

  onPropertyChanged(property) {
    super.onPropertyChanged(property);
    if (this.initialized)
      this.render();
  }

  render(computeData = true) {
    // Rendering logic here
  }
}
```

### 3. Register the viewer

In `src/package.ts`, add the annotated function:

```typescript
import {AwesomeViewer} from './awesome-viewer';

//name: AwesomeViewer
//description: Creates an awesome viewer
//tags: viewer
//meta.icon: images/icon.svg
//meta.toolbox: true
//meta.trellisable: true
//output: viewer result
export function awesome() {
  return new AwesomeViewer();
}
```

Or use the decorator approach (requires datagrok-tools >= 4.12.x):

```typescript
@grok.decorators.viewer({
  icon: 'images/icon.png',
  toolbox: true,
})
export class AwesomeViewer extends DG.JsViewer { /* ... */ }
```

### 4. Property types and naming conventions

Available property types in the constructor:
- `this.int(name, defaultValue, options)` -- integer
- `this.float(name, defaultValue, options)` -- floating point
- `this.string(name, defaultValue, options)` -- string
- `this.stringList(name, defaultValue, options)` -- string array
- `this.bool(name, defaultValue, options)` -- boolean
- `this.dateTime(name, defaultValue, options)` -- datetime

Property grouping in the UI is determined by naming:
- `Data` tab: properties ending with `ColumnName`
- `Colors` tab: properties ending with `color`
- `Axes` tab: properties containing `axis`
- `Legend` tab: properties starting with `legend`
- `Margins` tab: properties containing `margin`
- `Misc` tab: everything else

### 5. Data preparation with filter support

Always respect the dataframe filter when preparing data:

```typescript
render(computeData = true) {
  if (computeData) {
    this.data.length = 0;
    this.aggregatedTable = this.dataFrame
      .groupBy([this.splitColumnName])
      .whereRowMask(this.dataFrame.filter)
      .add(this.valueAggrType, this.valueColumnName, 'result')
      .aggregate();
    // Process aggregated data...
  }
  // Render using this.root as the container
}
```

### 6. Events and interactivity

Add tooltips and selection handling to visual elements:

```typescript
// Row group tooltips on hover
element.on('mouseover', (event, d) => ui.tooltip.showRowGroup(this.dataFrame, i => {
  return d.category === this.dataFrame.getCol(this.splitColumnName).get(i);
}, event.x, event.y));
element.on('mouseout', () => ui.tooltip.hide());

// Selection on click
element.on('mousedown', (event, d) => {
  this.dataFrame.selection.handleClick(i => {
    return d.category === this.dataFrame.getCol(this.splitColumnName).get(i);
  }, event);
});
```

### 7. External dependencies

Add libraries (e.g., D3, ECharts) to `package.json` dependencies. Do NOT add platform-provided externals (datagrok-api, rxjs, cash-dom, dayjs, wu, openchemlib/full) to your bundle.

### 8. Build and test

```shell
npm run build
grok publish dev
```

Test with: `grok.shell.addTableView(grok.data.demo.demog()).addViewer('AwesomeViewer');`

## Behavior

- Ask for the viewer name and what it should visualize if not specified.
- Always include filter and selection event subscriptions for proper interactivity.
- Add subscriptions to `this.subs` so they are cleaned up when the viewer is detached.
- Use `DG.debounce` on frequently firing events (selection, filter, resize) for performance.
- Separate data computation from rendering to avoid recomputing on resize.
- Follow Datagrok coding conventions: no excessive comments, no curly brackets for one-line if/for, catch/else-if on new line.
- Suggest the decorator approach for registration when using datagrok-tools >= 4.12.x.
