---
name: ag-grid
description: "Standards-compliant best practices for implementing advanced data tables with AG Grid in React and TypeScript. Configuration, accessibility, column definitions, cell renderers. Trigger: When implementing AG Grid data tables, configuring grid features, or creating custom cell renderers."
skills:
  - conventions
  - react
  - typescript
  - a11y
allowed-tools:
  - documentation-reader
  - web-search
  - file-reader
dependencies:
  ag-grid-community: ">=29.0.0 <31.0.0"
  ag-grid-react: ">=29.0.0 <31.0.0"
  react: ">=17.0.0 <19.0.0"
  typescript: ">=5.0.0 <6.0.0"
---

# AG Grid Skill

## Overview

This skill provides comprehensive guidance for implementing AG Grid data tables in React and TypeScript applications, covering configuration, accessibility, performance optimization, and integration patterns.

## Objective

Enable developers to implement robust, accessible, and performant data grids using AG Grid with proper TypeScript typing, React integration, and accessibility standards.

---

## When to Use

Use this skill when:

- Implementing data tables with sorting, filtering, pagination
- Creating editable grids with inline editing
- Building complex data grids with grouping and aggregation
- Requiring high-performance tables with virtualization
- Implementing Excel-like functionality

Don't use this skill for:

- Simple tables (use HTML table or MUI Table)
- Non-tabular data visualization (use charts)
- Mobile-first tables (consider simpler alternatives)

---

## Critical Patterns

### ✅ REQUIRED: Use TypeScript Interfaces for Type Safety

```typescript
// ✅ CORRECT: Typed column definitions
import { ColDef } from "ag-grid-community";

interface RowData {
  id: number;
  name: string;
}

const columnDefs: ColDef<RowData>[] = [{ field: "id" }, { field: "name" }];

// ❌ WRONG: Untyped columns
const columnDefs = [{ field: "id" }, { field: "name" }];
```

### ✅ REQUIRED: Use defaultColDef for Common Settings

```typescript
// ✅ CORRECT: DRY column configuration
const defaultColDef: ColDef = {
  sortable: true,
  filter: true,
  resizable: true,
};

<AgGridReact defaultColDef={defaultColDef} />

// ❌ WRONG: Repeating config for each column
const columnDefs = [
  { field: 'id', sortable: true, filter: true, resizable: true },
  { field: 'name', sortable: true, filter: true, resizable: true },
];
```

### ✅ REQUIRED: Enable Accessibility Features

```typescript
// ✅ CORRECT: Accessibility enabled
<AgGridReact
  enableAccessibility={true}
  suppressMenuHide={false}
/>
```

---

## Conventions

Refer to conventions for:

- Code organization
- Documentation standards

Refer to a11y for:

- Keyboard navigation
- Screen reader support
- ARIA attributes

### AG Grid Specific

- Use TypeScript interfaces for column definitions
- Implement proper cell renderers for custom content
- Configure accessibility features (keyboard navigation, screen reader support)
- Use AG Grid's built-in features over custom implementations
- Handle loading and error states appropriately

---

## Decision Tree

**Custom cell content?** → Use `cellRenderer` or `cellRendererFramework` for React components.

**Editable grid?** → Set `editable: true` on columns, handle `onCellValueChanged`.

**Filtering needed?** → Enable with `filter: true` or specify filter type: `'agTextColumnFilter'`, `'agNumberColumnFilter'`.

**Large dataset?** → Use `rowModelType: 'infinite'` for server-side pagination.

**Grouping/aggregation?** → Enable row grouping with `rowGroup: true` on columns.

**Export data?** → Use built-in `exportDataAsCsv()` or `exportDataAsExcel()` methods.

**Performance issues?** → Enable row virtualization (default), use `immutableData: true` for React optimization.

---

## Example

```typescript
import { ColDef } from 'ag-grid-community';
import { AgGridReact } from 'ag-grid-react';

interface RowData {
  id: number;
  name: string;
  value: number;
}

const columnDefs: ColDef<RowData>[] = [
  { field: 'id', headerName: 'ID' },
  { field: 'name', headerName: 'Name', sortable: true },
  { field: 'value', headerName: 'Value', filter: 'agNumberColumnFilter' }
];

<AgGridReact<RowData>
  rowData={data}
  columnDefs={columnDefs}
  defaultColDef={{ flex: 1, minWidth: 100 }}
/>
```

## Edge Cases

- Handle empty data sets with appropriate messaging
- Manage loading states during data fetching
- Implement error boundaries for grid failures
- Handle resize events properly
- Test keyboard navigation thoroughly

## References

- https://www.ag-grid.com/react-data-grid/
- https://www.ag-grid.com/react-data-grid/accessibility/
