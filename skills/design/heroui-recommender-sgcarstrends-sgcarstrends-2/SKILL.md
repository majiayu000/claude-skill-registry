---
name: heroui-recommender
description: Recommend appropriate HeroUI components for new features and ensure proper usage. Use when implementing new UI features or migrating from shadcn/ui to HeroUI.
---

# HeroUI Component Recommender Skill

This Skill helps developers select and implement the right HeroUI components for features, ensuring consistent UI/UX across the application.

## When to Activate

- Starting implementation of new UI features
- Migrating components from shadcn/ui to HeroUI
- Uncertain which HeroUI component fits requirements
- Need usage examples with TypeScript types
- Want to verify proper HeroUI patterns

## Available HeroUI Components

The project uses these HeroUI components (from package.json):

### Interactive Components
- **Button** (`@heroui/button`) - Actions, CTAs, form submissions
- **Tabs** (`@heroui/tabs`) - Section navigation, category switching
- **Pagination** (`@heroui/pagination`) - List navigation, data tables
- **Input** (`@heroui/input`) - Form fields, search boxes
- **Popover** (`@heroui/popover`) - Contextual information, tooltips
- **Tooltip** (`@heroui/tooltip`) - Hover hints, icon explanations

### Display Components
- **Card** (`@heroui/card`) - Content containers, dashboard widgets
- **Table** (`@heroui/table`) - Data grids, listings
- **Chip** (`@heroui/chip`) - Tags, badges, status indicators
- **Alert** (`@heroui/alert`) - Notifications, warnings, info messages
- **Toast** (`@heroui/toast`) - Temporary notifications, success messages

### Layout Components
- **Spacer** (`@heroui/spacer`) - Flexible spacing between elements
- **Spinner** (`@heroui/spinner`) - Loading states, async operations

### Complete Suite
- **@heroui/react** - Full HeroUI component library

## Actions Performed

1. **Analyze Requirements**: Understand the feature/UI needs
2. **Recommend Components**: Suggest appropriate HeroUI components
3. **Provide Examples**: Show TypeScript usage with proper types
4. **Fetch Latest Docs**: Use Context7 MCP to get up-to-date HeroUI documentation
5. **Check Patterns**: Ensure semantic colors and accessibility best practices
6. **Migration Guide**: If replacing shadcn/ui, provide migration steps

## Example Recommendations

### Feature: Data Table with Pagination

**Recommended Components**:
- `Table` from `@heroui/table` - Main data display
- `Pagination` from `@heroui/pagination` - Navigation controls
- `Chip` from `@heroui/chip` - Status badges
- `Spinner` from `@heroui/spinner` - Loading state

**Usage Example**:
```typescript
import { Table, TableHeader, TableColumn, TableBody, TableRow, TableCell } from "@heroui/table";
import { Pagination } from "@heroui/pagination";
import { Chip } from "@heroui/chip";

export function DataTable() {
  return (
    <div className="flex flex-col gap-4">
      <Table aria-label="Car registrations">
        <TableHeader>
          <TableColumn>Make</TableColumn>
          <TableColumn>Model</TableColumn>
          <TableColumn>Status</TableColumn>
        </TableHeader>
        <TableBody>
          <TableRow key="1">
            <TableCell>Toyota</TableCell>
            <TableCell>Camry</TableCell>
            <TableCell>
              <Chip color="success" variant="flat">Active</Chip>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
      <Pagination total={10} initialPage={1} />
    </div>
  );
}
```

### Feature: Form with Validation

**Recommended Components**:
- `Input` from `@heroui/input` - Form fields
- `Button` from `@heroui/button` - Submit action
- `Alert` from `@heroui/alert` - Error messages

### Feature: Dashboard Cards

**Recommended Components**:
- `Card` from `@heroui/card` - Container
- `Chip` from `@heroui/chip` - Metrics, trends
- `Spinner` from `@heroui/spinner` - Loading state

## Semantic Color System

All HeroUI components support semantic colors:

**Text Colors**:
- `text-foreground` - Primary text (auto-adjusts for light/dark mode)
- `text-default-900` - Strong emphasis
- `text-default-600` - Secondary text
- `text-muted-foreground` - Metadata, captions

**Component Colors**:
- `color="default"` - Neutral, standard UI
- `color="primary"` - Main actions, CTAs
- `color="secondary"` - Supporting actions
- `color="success"` - Positive states, confirmations
- `color="warning"` - Caution, important notices
- `color="danger"` - Errors, destructive actions

## Accessibility Guidelines

Ensure all HeroUI components include:
- `aria-label` attributes for screen readers
- Keyboard navigation support
- Focus indicators
- Semantic HTML structure
- Proper heading hierarchy

## Migration from shadcn/ui

**Common Mappings**:
- shadcn `Button` → `@heroui/button`
- shadcn `Card` → `@heroui/card`
- shadcn `Badge` → `@heroui/chip`
- shadcn `Table` → `@heroui/table`
- shadcn `Tabs` → `@heroui/tabs`
- shadcn `Tooltip` → `@heroui/tooltip`

**Note**: Do NOT modify files in `src/components/ui/` (shadcn/ui). Create new HeroUI components in appropriate directories.

## Tools Used

- **Context7 MCP**: Fetch latest HeroUI documentation
  - `mcp__context7__resolve-library-id` - Find HeroUI library ID
  - `mcp__context7__get-library-docs` - Get component documentation
- **Read**: Examine existing component implementations
- **Grep**: Find similar patterns in codebase

## Documentation Resources

When fetching HeroUI docs via Context7:
- Library ID: `/heroui/react` or component-specific packages
- Focus on: TypeScript types, props, variants, colors, accessibility

## Project-Specific Guidelines

From `apps/web/CLAUDE.md`:
- **New Features**: Use HeroUI components with TypeScript-first approach
- **Component Selection**: Leverage HeroUI's professional design system
- **Data Visualisation**: Use HeroUI's table and chart components for market data
- **Customisation**: Apply HeroUI theming to match Singapore car market branding
- **Performance**: Take advantage of tree-shakeable, optimized components
- **Legacy Code**: Gradually migrate shadcn/ui to HeroUI equivalents
