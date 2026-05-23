---
name: create-custom-filter
description: Create a custom filter for Datagrok by extending DG.Filter
argument-hint: "[filter-name] [package-path]"
---

# Create Custom Filter

Create a custom filter widget for the Datagrok filter panel.

## Usage

```
/create-custom-filter [filter-name] [package-path]
```

## Instructions

When this skill is invoked, help the user create a custom filter by extending `DG.Filter`.

### Step 1: Create the filter class

Create a new TypeScript file in the package's `src/filters/` directory.

The class must extend `DG.Filter` and implement the filtering logic. When the filter state changes, call `this.dataFrame.filter` to update the bitset.

```ts
import * as DG from 'datagrok-api/dg';

export class MyFilter extends DG.Filter {
  constructor() {
    super();
    // Initialize filter state
  }

  attach(dataFrame: DG.DataFrame): void {
    super.attach(dataFrame);
    // Set up UI, subscribe to events
    this.column = dataFrame.columns.byName(this.columnName);
    this.render();
  }

  applyFilter(): void {
    // Apply filtering logic to this.dataFrame.filter (a DG.BitSet)
    let filter = this.dataFrame.filter;
    for (let i = 0; i < this.dataFrame.rowCount; i++)
      filter.set(i, this.shouldInclude(i), false);
    filter.fireChanged();
  }

  private render(): void {
    // Build the filter's UI
    this.root.appendChild(/* UI elements */);
  }
}
```

### Step 2: Register the filter

Use the decorator approach (preferred for `datagrok-tools` >= 4.12.x):

```ts
@grok.decorators.filter({
  semType: 'Country',  // optional: auto-apply to columns with this semantic type
})
export class MyFilter extends DG.Filter {
  /* ... */
}
```

Or use the function annotation approach in `package.ts`:

```ts
//name: My Filter
//description: A custom filter
//tags: filter
//output: filter result
export function myFilter() {
  return new MyFilter();
}
```

### Step 3: Use the filter programmatically

The filter can be invoked via JS API:

```ts
let tv = grok.shell.addTableView(grok.data.demo.demog());
tv.filters({filters: [
  {type: 'MyPackage:myFilter', columnName: 'race'},
]});
```

Or added through the UI via the filter panel.

### Key points

- The `semType` option in the decorator auto-applies the filter to columns with that semantic type
- Call `this.dataFrame.filter.set(i, value, notify)` to include/exclude rows; call `fireChanged()` after
- The `root` property is the HTMLElement where you build the filter's UI
- `attach()` is called when the filter is attached to a dataframe
- For a real example, see: `public/packages/Widgets/src/filters/radio-button-filter.ts`
- Both decorator and function annotation approaches are equivalent; prefer decorators

## Behavior

1. Ask the user what kind of filtering logic they need if not specified
2. Create the filter class extending `DG.Filter` with proper filtering logic
3. Register the filter using the decorator approach (or function annotation if preferred)
4. Build appropriate UI for the filter widget
5. Ensure imports are correct (`import * as DG from 'datagrok-api/dg'`, `import * as grok from 'datagrok-api/grok'`, `import * as ui from 'datagrok-api/ui'`)
6. Remind the user to build and publish the package
