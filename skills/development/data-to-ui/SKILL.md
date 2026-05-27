---
name: data-to-ui
description: Data-to-UI pipeline patterns. Use when transforming JSON data into React components, creating TypeScript types from schemas, building derived types, or creating data utilities.
---

# Data to UI

## Overview
Patterns for transforming static data into type-safe React components. This skill covers JSON → TypeScript → React pipelines with emphasis on semantic color systems, derived types, and formatting utilities.

## Workflows

### 1. JSON Schema → TypeScript Types
- [ ] Read JSON schema/data structure
- [ ] Create base TypeScript interfaces matching JSON shape
- [ ] Export union types for enums (e.g., `type Severity = 'safety_hazard' | 'repair_needed'`)
- [ ] Use optional properties (`?`) for nullable/missing fields
- [ ] Add JSDoc comments for complex types

### 2. Derived Types for UI
- [ ] Create composed types extending base types with `extends`
- [ ] Use `Pick<T, K>` and `Omit<T, K>` for component props
- [ ] Build intersection types with `&` for joined data (e.g., `FindingWithAsset`)
- [ ] Create aggregate interfaces for statistics/summaries

### 3. Color Mapping Systems
- [ ] Define `Record<EnumType, ColorValue>` for semantic colors
- [ ] Provide multiple color formats: badge, bg, text, border, dot
- [ ] Use Tailwind utility classes (e.g., `'bg-red-500 text-red-600'`)
- [ ] Export accessor functions (e.g., `getSeverityColors()`)
- [ ] Document color choices with comments

### 4. Icon Mapping
- [ ] Create `Record<EnumType, string>` mapping to lucide-react icon names
- [ ] Use PascalCase icon names (e.g., `'AlertTriangle'`, `'Thermometer'`)
- [ ] Export accessor function (e.g., `getSeverityIcon()`)

### 5. Formatting Utilities
- [ ] Currency: Use `Intl.NumberFormat` with USD, no decimals
- [ ] Dates: Use `toLocaleDateString` with short month format
- [ ] Calculations: Create helpers for years, percentages, lifespans
- [ ] Labels: Create human-readable label maps

### 6. Aggregation & Grouping
- [ ] Implement `groupBy` patterns using reduce or forEach
- [ ] Sort with custom comparators using severity/priority order
- [ ] Calculate summary statistics (min, max, avg, count)
- [ ] Return strongly-typed aggregates

## Reference Implementation

### Color Mapping System
```typescript
// Single source of truth for semantic colors
export interface SeverityColors {
  badge: string;  // 'text-red-600 bg-red-100'
  bg: string;     // 'bg-red-500'
  text: string;   // 'text-red-600'
  border: string; // 'border-red-500'
  dot: string;    // 'bg-red-500'
}

const SEVERITY_COLOR_MAP: Record<Severity, SeverityColors> = {
  safety_hazard: {
    badge: 'text-red-600 bg-red-100',
    bg: 'bg-red-500',
    text: 'text-red-600',
    dot: 'bg-red-500',
    border: 'border-red-500',
  },
  // ... other severities
};

export function getSeverityColors(severity: Severity): SeverityColors {
  return SEVERITY_COLOR_MAP[severity];
}
```

### Icon Mapping
```typescript
export function getSeverityIcon(severity: Severity): string {
  const icons: Record<Severity, string> = {
    safety_hazard: 'AlertTriangle',
    repair_needed: 'Wrench',
    maintenance_item: 'Settings',
    monitor: 'Eye',
    informational: 'Info'
  };
  return icons[severity];
}
```

### Derived Types
```typescript
// Base type
export interface Finding {
  id: string;
  assetId?: string | null;
  severity: Severity;
  title: string;
}

// Derived type with relationship
export interface FindingWithAsset extends Finding {
  asset?: Asset;
}

// Aggregate type
export interface PropertyWithDetails {
  property: Property;
  inspectionReport: InspectionReport;
  findings: Finding[];
  assets: Asset[];
}
```

### Formatting Utilities
```typescript
export function formatCurrency(value: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value);
}

export function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}

export function yearsSince(dateString: string): number {
  const date = new Date(dateString);
  const now = new Date();
  return Math.floor((now.getTime() - date.getTime()) / (365.25 * 24 * 60 * 60 * 1000));
}
```

### Aggregation Patterns
```typescript
// Group by enum value
export function groupFindingsBySeverity(findings: Finding[]): Record<Severity, Finding[]> {
  const grouped: Record<Severity, Finding[]> = {
    safety_hazard: [],
    repair_needed: [],
    maintenance_item: [],
    monitor: [],
    informational: []
  };

  findings.forEach(f => grouped[f.severity].push(f));
  return grouped;
}

// Sort by priority
export function sortFindingsBySeverity(findings: Finding[]): Finding[] {
  const severityOrder: Record<Severity, number> = {
    safety_hazard: 0,
    repair_needed: 1,
    maintenance_item: 2,
    monitor: 3,
    informational: 4
  };
  return [...findings].sort((a, b) =>
    severityOrder[a.severity] - severityOrder[b.severity]
  );
}
```

## Best Practices

- **Single Source of Truth**: All color/icon mappings in one place with accessor functions
- **Multi-Format Colors**: Provide badge, bg, text, border, dot variants for flexibility
- **Type Safety**: Use `Record<EnumType, Value>` instead of plain objects
- **Intl APIs**: Use `Intl.NumberFormat` and `Intl.DateTimeFormat` for localization
- **Immutability**: Use spread operator when sorting/filtering arrays
- **Documentation**: Add JSDoc comments explaining color choices and data structures
- **Colocate Utilities**: Keep types and utilities in same file for easy import

## Anti-Patterns

- **DO NOT** use generic color names without semantic meaning (e.g., `'red'` instead of `'safety_hazard'`)
- **DO NOT** inline color classes in components; always use mapping functions
- **DO NOT** use `any` types; prefer `unknown` and type guards
- **DO NOT** mutate input arrays in sort/filter functions; always create copies
- **DO NOT** hardcode date formats; use `Intl.DateTimeFormat` for consistency
- **DO NOT** create separate files for simple utilities; colocate with types
- **DO NOT** forget to handle null/undefined in optional fields
- **DO NOT** use snake_case or kebab-case for TypeScript file names; use camelCase

## Feedback Loops

1. **Type Checking**: Run `tsc --noEmit` to validate types
2. **Runtime Validation**: Consider Zod for JSON schema validation at runtime
3. **Visual Testing**: Build Storybook stories to verify color systems
4. **Data Consistency**: Compare aggregated stats with source data counts
5. **Import Verification**: Ensure all utilities are exported and importable

## Related Skills

- `interface-design` - Use color systems in React components
- `refactoring-code` - Consolidate duplicate color/formatting logic
