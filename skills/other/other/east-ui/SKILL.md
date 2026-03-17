---
name: east-ui
description: UI component definitions for the East language. Use when building UIs with @elaraai/east-ui. Triggers for: (1) Creating UI components with Stack, Box, Grid, Card, Text, Button, (2) Building forms with Input, Select, Checkbox, Switch, Slider, (3) Displaying data with Table, DataList, Chart, Badge, Tag, Stat, (4) Using overlays like Dialog, Drawer, Popover, Tooltip, Menu, (5) Working with UIComponentType, (6) Styling with variants (FontWeight, TextAlign, ColorScheme, Size).
---

# East UI

UI component definitions for the East language. Components return data structures describing UI layouts rather than rendering directly, enabling portability across different rendering environments.

## Quick Start

```typescript
import { East, ArrayType } from "@elaraai/east";
import { Stack, Text, Button, UIComponentType } from "@elaraai/east-ui";

// Define a UI component
const MyComponent = East.function(
    [],
    UIComponentType,
    $ => {
        return Stack.Root([
            Text.Root("Hello, World!", { fontSize: "xl", fontWeight: "bold" }),
            Button.Root("Click Me", { variant: "solid", colorPalette: "blue" }),
        ], { gap: "4", direction: "column" });
    }
);

// Convert to IR for serialization or rendering
const ir = MyComponent.toIR();
```

## Decision Tree: Which Component to Use

```
Task -> What do you need?
    |
    +-- Layout (containers)
    |   +-- Box         -> Generic container with flexbox styling
    |   +-- Stack       -> Vertical or horizontal stack (.Root, .HStack, .VStack)
    |   +-- Grid        -> CSS Grid layout (.Root, .Item)
    |   +-- Splitter    -> Resizable split panels
    |   +-- Separator   -> Visual divider
    |
    +-- Typography
    |   +-- Text        -> Basic text display
    |   +-- Code        -> Inline code
    |   +-- Heading     -> Section headings
    |   +-- Link        -> Hyperlinks
    |   +-- List        -> Ordered/unordered lists
    |   +-- CodeBlock   -> Multi-line code blocks
    |
    +-- Buttons
    |   +-- Button      -> Standard button with variants
    |   +-- IconButton  -> Icon-only button
    |
    +-- Forms
    |   +-- Input       -> Text, Integer, Float, DateTime inputs
    |   +-- Select      -> Dropdown selection (.Root, .Item)
    |   +-- Checkbox    -> Boolean checkbox
    |   +-- Switch      -> Toggle switch
    |   +-- Slider      -> Range slider
    |   +-- Textarea    -> Multi-line text
    |   +-- TagsInput   -> Tag/chip input
    |   +-- FileUpload  -> File upload
    |   +-- Field       -> Form field wrapper with label
    |
    +-- Collections
    |   +-- Table       -> Data tables (.Root, .Row, .Cell)
    |   +-- DataList    -> Key-value list (.Root, .Item)
    |   +-- TreeView    -> Hierarchical tree
    |   +-- Gantt       -> Gantt chart timeline
    |
    +-- Charts
    |   +-- Chart.Area, Chart.Bar, Chart.Line, Chart.Pie
    |   +-- Chart.Radar, Chart.Scatter
    |   +-- Chart.BarList, Chart.BarSegment
    |   +-- Sparkline   -> Inline mini charts
    |
    +-- Display
    |   +-- Badge       -> Status indicators
    |   +-- Tag         -> Labels/tags
    |   +-- Avatar      -> User avatars
    |   +-- Stat        -> Statistics display
    |   +-- Icon        -> Icons
    |
    +-- Feedback
    |   +-- Alert       -> Alert messages
    |   +-- Progress    -> Progress indicators
    |
    +-- Disclosure
    |   +-- Accordion   -> Collapsible sections (.Root, .Item)
    |   +-- Tabs        -> Tabbed content
    |   +-- Carousel    -> Image/content carousel
    |
    +-- Overlays
    |   +-- Dialog      -> Modal dialogs
    |   +-- Drawer      -> Side drawers
    |   +-- Popover     -> Popovers
    |   +-- Tooltip     -> Tooltips
    |   +-- Menu        -> Context menus
    |   +-- HoverCard   -> Hover cards
    |
    +-- Container
        +-- Card        -> Content card with header/body
```

## Component Pattern

All components follow a consistent namespace pattern:

```typescript
import { Badge, Stack, Button } from "@elaraai/east-ui";

// Create component using .Root()
const badge = Badge.Root("New", { variant: "solid", colorPalette: "green" });

// Compound components have sub-factories
const stack = Stack.Root([
    Text.Root("Item 1"),
    Text.Root("Item 2"),
], { gap: "4" });

// Access East types via .Types
const badgeType = Badge.Types.Badge;
const styleType = Badge.Types.Style;
```

## Styling

Components accept style options with Chakra UI tokens:

```typescript
Button.Root("Click", {
    variant: "solid",        // solid, outline, subtle, ghost
    colorPalette: "blue",    // gray, red, orange, yellow, green, teal, blue, purple, pink
    size: "md",              // xs, sm, md, lg
});

Text.Root("Hello", {
    fontSize: "xl",
    fontWeight: "bold",      // normal, medium, semibold, bold
    color: "gray.600",
});

Stack.Root([...], {
    gap: "4",                // Chakra spacing tokens
    direction: "row",        // row, column
    align: "center",         // flex alignment
});
```

## Reference Documentation

- **[API Reference](./references/api.md)** - Complete component signatures and types
- **[Examples](./references/examples.md)** - Working code examples by use case
