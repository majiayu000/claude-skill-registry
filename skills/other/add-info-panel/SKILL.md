---
name: add-info-panel
description: Create info panels that appear in the context panel based on semantic types and conditions
---

# Add an Info Panel

Help the user create info panels that display context-specific information in Datagrok's context panel.

## Usage
```
/add-info-panel [panel-name] [--semtype <semantic-type>] [--input-type <string|column|dataframe|file>]
```

## Instructions

### 1. Understand info panels

Info panels appear in the context panel on the right side of the Datagrok UI. They show additional information about the currently selected object (cell value, column, table, file). Panels are re-evaluated whenever the selected object changes.

### 2. Create a panel function in `src/package.ts`

A panel function must be annotated with `panel` tag and return a `widget`:

```typescript
//name: MyPanel
//tags: panel, widgets
//input: string str {semType: Molecule}
//output: widget result
export function myPanel(str: string) {
  return new DG.Widget(ui.divV([
    ui.divText('Info about: ' + str)
  ]));
}
```

Key annotations:
- `//tags: panel, widgets` -- marks this as a panel function returning a widget
- `//input:` -- defines what object triggers the panel
- `//output: widget result` -- panels must output a widget
- `{semType: <type>}` on the input -- restricts panel to columns with this semantic type

### 3. Input types

Panels accept a single input parameter of various types:

```typescript
// For cell values (filtered by semantic type)
//input: string str {semType: text}

// For columns
//input: column col

// For dataframes
//input: dataframe table

// For files
//input: file file

// For semantic values (preserves cell context)
//input: semantic_value smiles {semType: Molecule}
```

Using `semantic_value` gives access to the cell's column and row context:
```typescript
//input: semantic_value smiles {semType: Molecule}
//output: widget result
export function valueWidget(value) {
  return value
    ? new DG.Widget(ui.divText('Column: ' + value.cell.column.name))
    : new DG.Widget(ui.divText('No value'));
}
```

### 4. Visibility conditions

Control when panels appear using the `//condition:` annotation:

**By semantic type** (most common -- use `semType` on the input parameter):
```typescript
//input: string str {semType: Molecule}
```

**By column properties:**
```
//input: column x
//condition: x.isnumerical && x.name == "f3" && x.stats.missingvaluecount > 0
```

**By dataset:**
```
//condition: table.gettag("database") == "northwind"
```

**By user role:**
```
//condition: user.hasrole("chemist")
```

**By column semantic type in condition:**
```
//condition: columnName.semType == "Molecule"
```

**Custom function condition:**
```typescript
//condition: isTextFile(file)
```

Conditions use Grok Script syntax regardless of the panel's implementation language.

### 5. Panel scripts (server-side)

Panels can also be written as scripts in Python, R, etc. These execute on the server:

```python
# name: string length
# language: python
# tags: panel
# input: string s {semType: text}
# output: int length
# condition: true

length = len(s)
```

### 6. Panels with viewers

Return interactive visualizations in a panel:

```typescript
//name: ScatterPanel
//tags: panel, widgets
//input: dataframe table
//condition: table.columns.containsAll(["height", "weight"])
//output: widget result
export function scatterPanel(table: DG.DataFrame) {
  const viewer = DG.Viewer.scatterPlot(table, {x: 'height', y: 'weight'});
  return new DG.Widget(viewer.root);
}
```

### 7. Build and test

```shell
npm run build
grok publish dev
```

To test: open a dataset, click on a cell in a column with the matching semantic type, and check the context panel on the right for your panel.

To manually set a column's semantic type for testing: right-click the column header, select `Column Properties`, add the tag `quality: <semType>`.

## Behavior

- Ask for the panel name and what data it should display if not specified.
- Always ask what semantic type or condition should trigger the panel.
- Default to TypeScript panel functions (client-side) unless the user needs server-side computation.
- Use `DG.Widget` as the return wrapper -- the panel output must be a widget.
- Suggest `semantic_value` input type when the user needs access to cell/column context.
- Remind the user that semantic type detectors can be defined in `detectors.js` to auto-detect custom types.
- Follow Datagrok coding conventions: no excessive comments, no curly brackets for one-line if/for, catch/else-if on new line.
