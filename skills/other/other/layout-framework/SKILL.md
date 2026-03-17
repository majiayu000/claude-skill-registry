---
name: layout-framework
description: Use for any frontend layout or form arrangement work in PierceDesk. Covers Box/Container/Grid/Stack/Paper/Card usage, surface selection, responsive sizing, spacing rules, page structure templates, and how to align pages with the app's layout framework. Trigger when asked to fix layout issues, align fields, create grids, select surfaces, or ensure design-system consistency.
---

# Layout Framework Skill

## Overview

This skill ensures consistent, responsive layouts across PierceDesk using MUI v7 components. The core principles:

1. **Grid for columns, Stack for vertical rhythm** - never use flex/Box for form layout
2. **fullWidth on ALL form inputs** - always
3. **Correct surface for the job** - Paper for containers, Card for structured content, Box for utility only
4. **Copy from exemplars** - never invent page structure from scratch

## The Iron Rules (MANDATORY)

### Rule 1: Grid for Columns, Stack for Vertical Rhythm

```jsx
// CORRECT: Grid for column layout
<Grid container spacing={{ xs: 2, md: 3 }}>
  <Grid size={{ xs: 12, md: 6 }}>
    <TextField fullWidth label="First Name" />
  </Grid>
  <Grid size={{ xs: 12, md: 6 }}>
    <TextField fullWidth label="Last Name" />
  </Grid>
</Grid>

// CORRECT: Stack for vertical spacing between sections
<Stack spacing={3}>
  <Typography variant="h6">Section 1</Typography>
  <Typography variant="h6">Section 2</Typography>
</Stack>
```

### Rule 2: fullWidth on ALL Form Inputs

```jsx
// WRONG
<TextField label="Description" />

// CORRECT
<TextField fullWidth label="Description" />
<Select fullWidth />
<Autocomplete fullWidth />
<DatePicker slotProps={{ textField: { fullWidth: true } }} />
```

### Rule 3: MUI v7 Grid Uses `size` Prop

```jsx
// WRONG - old MUI v5/v6 syntax
<Grid item xs={12} md={6}>

// CORRECT - MUI v7 syntax
<Grid size={{ xs: 12, md: 6 }}>
```

### Rule 4: No Hardcoded Widths on Inputs

```jsx
// WRONG
<TextField sx={{ width: 200 }} />
<TextField sx={{ width: '50%' }} />

// CORRECT
<Grid size={{ xs: 12, md: 6 }}>
  <TextField fullWidth />
</Grid>
```

### Rule 5: Correct Surface Component

```
Paper → General container, form wrapper, page section, sidebar, data table wrapper
Card  → Structured content: header/body/actions pattern (KPIs, products, profiles)
Box   → Utility ONLY: semantic HTML, positioning, decorative elements
```

---

## Surface Selection Guide

### Paper (General Surface)

Use for page sections, sidebars, form wrappers, data tables, filter bars.

```jsx
// Page section
<Paper background={1} sx={{ p: { xs: 3, md: 5 }, borderRadius: 6 }}>
  <Stack spacing={3}>
    <Typography variant="h6">Section Title</Typography>
    <Grid container spacing={2}>
      {/* form fields */}
    </Grid>
  </Stack>
</Paper>

// Sticky sidebar
<Paper background={1} sx={{ p: { xs: 3, md: 4 }, position: { md: 'sticky' }, top: { md: 80 } }}>
  {/* sidebar */}
</Paper>
```

### Card (Structured Content)

Use when content has a distinct header + body + actions structure.

```jsx
// KPI Card
<Card background={1} variant="outlined">
  <CardHeader title="Revenue" action={<IconButton>...</IconButton>} />
  <CardContent>
    <Typography variant="h4">$42,500</Typography>
  </CardContent>
  <CardActions>
    <Button size="small">View Report</Button>
  </CardActions>
</Card>

// Media Card
<Card background={1} variant="outlined" sx={{ maxWidth: 345 }}>
  <CardMedia component="img" image="/path.webp" sx={{ height: 200, objectFit: 'cover' }} />
  <CardContent>
    <Typography variant="h6">Product Name</Typography>
  </CardContent>
  <CardActions>
    <Button size="small">Details</Button>
  </CardActions>
</Card>

// Clickable Card
<Card background={1} variant="outlined">
  <CardActionArea onClick={handleClick}>
    <CardContent>
      <Typography variant="h6">Clickable card</Typography>
    </CardContent>
  </CardActionArea>
</Card>
```

**Card sub-components:**
| Component | Purpose |
|-----------|---------|
| `CardHeader` | Title, subtitle, avatar, action button |
| `CardContent` | Main body content (always wrap content) |
| `CardActions` | Buttons and action controls |
| `CardMedia` | Images, videos |
| `CardActionArea` | Makes entire card clickable |

### Box (Utility Only)

Box is NOT a surface. Use only for:

```jsx
// Semantic HTML
<Box component="section" sx={{ py: 4 }}>...</Box>

// Positioning
<Box sx={{ position: 'relative' }}>...</Box>

// Decorative
<Box sx={{ width: 40, height: 40, borderRadius: '50%', bgcolor: 'primary.main' }} />

// Button alignment
<Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
  <Button>Cancel</Button>
  <Button variant="contained">Save</Button>
</Box>
```

**NEVER use Box for:** form column layout, surface/cards, `display: 'flex'` with children, `flexDirection: 'row'` (use Stack)

---

## Page Structure Templates

### Settings/Form Page

```jsx
<Container maxWidth={false} sx={{ px: { xs: 0 } }}>
  <Stack spacing={3}>
    <Typography variant="h5">Settings</Typography>
    <Paper background={1} sx={{ p: { xs: 3, md: 5 }, borderRadius: 6 }}>
      <Stack spacing={3}>
        <Typography variant="h6">Section</Typography>
        <Grid container spacing={{ xs: 2, md: 3 }}>
          {/* fields */}
        </Grid>
      </Stack>
    </Paper>
  </Stack>
</Container>
```

> **Note:** Do NOT add `maxWidth: 660` or similar hard limits on Container — this restricts ALL child tab panels/content. Let child components control their own max-width if needed.

### Dashboard Page

```jsx
<Grid container spacing={{ xs: 2, md: 3 }}>
  <Grid size={{ xs: 12, sm: 6, lg: 3 }}>
    <Card background={1} variant="outlined">KPI</Card>
  </Grid>
  <Grid size={{ xs: 12, md: 8 }}>
    <Paper background={1} sx={{ p: { xs: 2, md: 3 } }}>Chart</Paper>
  </Grid>
  <Grid size={{ xs: 12, md: 4 }}>
    <Paper background={1} sx={{ p: { xs: 2, md: 3 } }}>Widget</Paper>
  </Grid>
</Grid>
```

### Detail Page (Main + Sidebar)

```jsx
<Grid container spacing={{ xs: 2, md: 3 }}>
  <Grid size={{ xs: 12, md: 8, xl: 9 }}>
    <Paper sx={{ p: { xs: 3, md: 5 } }}>Main content</Paper>
  </Grid>
  <Grid size={{ xs: 12, md: 4, xl: 3 }}>
    <Paper background={1} sx={{ p: { xs: 3, md: 4 }, position: { md: 'sticky' }, top: { md: 80 } }}>
      Sidebar
    </Paper>
  </Grid>
</Grid>
```

### Account Tab Panel Content

Tab panels in the Account section use simple vertical stacking — NOT Grid containers. The parent `AccountTabPanel.jsx` already handles the title/icon header. Tab panel content goes directly below.

```jsx
// CORRECT: Simple Stack for vertical sections within a tab panel
const MyTabPanel = () => (
  <Stack direction="column" spacing={3}>
    {/* Header/stats section */}
    <Paper background={1} sx={{ p: { xs: 3, md: 4 }, borderRadius: 6 }}>
      <Stack spacing={2}>
        <Typography variant="h6">Section Title</Typography>
        {/* metadata, legend, actions */}
      </Stack>
    </Paper>

    {/* Main content section */}
    <Paper background={1} sx={{ borderRadius: 6, minHeight: 400, overflow: 'auto' }}>
      {/* visualization, table, or form content */}
    </Paper>

    {/* Optional details panel */}
    {selectedItem && (
      <Paper background={1} sx={{ p: 3, borderRadius: 6 }}>
        {/* detail content */}
      </Paper>
    )}
  </Stack>
);
```

> **IMPORTANT:** Do NOT use Grid container for simple vertical stacking in tab panels. Stack is the correct choice. Match the pattern used by PersonalInfoTabPanel, UsersPermissionsTabPanel, and other existing tab panels.

### Visualization/Tree Layout (Pure React/CSS)

For tree or hierarchy visualizations, use pure React/CSS with recursive components. Do NOT use d3-based libraries (react-d3-tree, etc.) as they have Turbopack compatibility issues.

```jsx
// Recursive tree node with CSS connector lines
<Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
  {/* Node card */}
  <Box sx={{
    bgcolor: 'background.paper',
    borderLeft: `4px solid ${color}`,
    borderRadius: 2,
    p: 1.5,
    minWidth: 160,
    maxWidth: 220,
    boxShadow: 1,
  }}>
    {/* node content */}
  </Box>

  {/* Children with connector lines */}
  {hasChildren && (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mt: 2 }}>
      {/* Vertical line */}
      <Box sx={{ width: 2, height: 16, bgcolor: 'divider', mb: 1 }} />
      {/* Horizontal connector + children */}
      <Box sx={{ display: 'flex', flexDirection: 'row', gap: 3 }}>
        {children.map(child => <TreeNode key={child.id} node={child} />)}
      </Box>
    </Box>
  )}
</Box>
```

### List/Table Page

```jsx
<Stack spacing={3}>
  <Stack direction="row" justifyContent="space-between" alignItems="center">
    <Typography variant="h5">Items</Typography>
    <Button variant="contained">Add</Button>
  </Stack>
  <Paper background={1} sx={{ p: 2 }}>
    <Grid container spacing={2}>
      {/* filter fields */}
    </Grid>
  </Paper>
  <Paper sx={{ overflow: 'auto' }}>
    <DataGrid />
  </Paper>
</Stack>
```

---

## Dialog Form Layout

```jsx
<Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
  <DialogTitle>Add New Item</DialogTitle>
  <DialogContent>
    <Grid container spacing={2} sx={{ mt: 1 }}>
      <Grid size={12}>
        <TextField fullWidth label="Title" required autoFocus />
      </Grid>
      <Grid size={{ xs: 12, md: 6 }}>
        <TextField fullWidth select label="Category">
          <MenuItem value="a">Option A</MenuItem>
        </TextField>
      </Grid>
      <Grid size={{ xs: 12, md: 6 }}>
        <TextField fullWidth select label="Status">
          <MenuItem value="active">Active</MenuItem>
        </TextField>
      </Grid>
      <Grid size={12}>
        <TextField fullWidth multiline rows={3} label="Description" />
      </Grid>
    </Grid>
  </DialogContent>
  <DialogActions>
    <Button onClick={onClose}>Cancel</Button>
    <Button variant="contained" type="submit">Save</Button>
  </DialogActions>
</Dialog>
```

**Dialog rules:**
- `maxWidth="sm"` simple forms, `"md"` complex multi-column
- `fullWidth` prop on Dialog
- `sx={{ mt: 1 }}` on Grid (prevents label overlap)
- `fullWidth` on every input
- `autoFocus` on first field

---

## Grid Patterns

### Two-Column Form
```jsx
<Grid container spacing={{ xs: 2, md: 3 }}>
  <Grid size={{ xs: 12, md: 6 }}>Field 1</Grid>
  <Grid size={{ xs: 12, md: 6 }}>Field 2</Grid>
</Grid>
```

### Three-Column Row
```jsx
<Grid container spacing={2}>
  <Grid size={{ xs: 12, md: 4 }}>A</Grid>
  <Grid size={{ xs: 12, md: 4 }}>B</Grid>
  <Grid size={{ xs: 12, md: 4 }}>C</Grid>
</Grid>
```

### Primary + Sidebar (8/4)
```jsx
<Grid container spacing={3}>
  <Grid size={{ xs: 12, md: 8 }}>Main</Grid>
  <Grid size={{ xs: 12, md: 4 }}>Sidebar</Grid>
</Grid>
```

### Address Block
```jsx
<Grid container spacing={2}>
  <Grid size={12}><TextField fullWidth label="Street" /></Grid>
  <Grid size={{ xs: 12, md: 6 }}><TextField fullWidth label="City" /></Grid>
  <Grid size={{ xs: 6, md: 3 }}><TextField fullWidth label="State" /></Grid>
  <Grid size={{ xs: 6, md: 3 }}><TextField fullWidth label="ZIP" /></Grid>
</Grid>
```

### Auto-Growing Item (MUI v7)
```jsx
<Grid container spacing={2}>
  <Grid size="grow"><TextField fullWidth /></Grid>
  <Grid size="auto"><Button variant="contained">Go</Button></Grid>
</Grid>
```

---

## Anti-Patterns (NEVER DO)

### Flex for Form Columns
```jsx
// WRONG
<Box sx={{ display: 'flex', gap: 2 }}><TextField /><TextField /></Box>
// CORRECT
<Grid container spacing={2}>
  <Grid size={6}><TextField fullWidth /></Grid>
  <Grid size={6}><TextField fullWidth /></Grid>
</Grid>
```

### Stack direction="row" for Forms
```jsx
// WRONG
<Stack direction="row" spacing={2}><TextField /><TextField /></Stack>
// CORRECT
<Grid container spacing={2}>
  <Grid size={6}><TextField fullWidth /></Grid>
  <Grid size={6}><TextField fullWidth /></Grid>
</Grid>
```

### Hardcoded Widths
```jsx
// WRONG
<TextField sx={{ width: 200 }} />
// CORRECT
<Grid size={{ xs: 12, md: 6 }}><TextField fullWidth /></Grid>
```

### Box as Flex Container for Children
```jsx
// WRONG
<Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
  <Section1 /><Section2 />
</Box>
// CORRECT
<Stack spacing={3}>
  <Section1 /><Section2 />
</Stack>
```

### Paper Where Card Fits Better
```jsx
// WRONG - manually building header+body+actions
<Paper background={1} sx={{ p: 3 }}>
  <Stack direction="row" justifyContent="space-between">
    <Typography variant="h6">Revenue</Typography>
    <IconButton><MoreVertIcon /></IconButton>
  </Stack>
  <Typography variant="h4">$42,500</Typography>
  <Button size="small">View Details</Button>
</Paper>

// CORRECT - use Card's built-in structure
<Card background={1} variant="outlined">
  <CardHeader title="Revenue" action={<IconButton><MoreVertIcon /></IconButton>} />
  <CardContent>
    <Typography variant="h4">$42,500</Typography>
  </CardContent>
  <CardActions>
    <Button size="small">View Details</Button>
  </CardActions>
</Card>
```

### sx flexDirection Instead of Stack Direction
```jsx
// WRONG
<Stack sx={{ flexDirection: 'row' }}>
// CORRECT
<Stack direction="row">
```

### Grid Container for Simple Vertical Stacking
```jsx
// WRONG - Grid is for columns, not vertical stacking
<Grid container spacing={3}>
  <Grid size={12}><Paper>Header Section</Paper></Grid>
  <Grid size={12}><Paper>Content Section</Paper></Grid>
</Grid>

// CORRECT - Stack for vertical rhythm
<Stack spacing={3}>
  <Paper>Header Section</Paper>
  <Paper>Content Section</Paper>
</Stack>
```

### Ignoring Parent Container Constraints
```
// WRONG - Building a full-width component without checking parent
// The Account page Container had maxWidth: 660 that constrained ALL tab panels

// CORRECT - Always check the parent component chain:
// 1. What Container/Paper wraps this content?
// 2. Does it have maxWidth, width, or overflow constraints?
// 3. Will my component's min-width fit within the parent?
```

---

## Spacing Reference

| Context | Value |
|---------|-------|
| Grid container (forms) | `spacing={{ xs: 2, md: 3 }}` |
| Grid container (compact) | `spacing={2}` |
| Stack sections | `spacing={3}` |
| Stack items | `spacing={2}` |
| Paper padding (page sections) | `p: { xs: 3, md: 5 }` |
| Paper padding (compact) | `p: { xs: 2, md: 3 }` |
| Paper border radius | `borderRadius: 6` |
| DialogContent Grid | `sx={{ mt: 1 }}` |

---

## PierceDesk-Specific

### background Prop
```jsx
<Paper background={1} />  // Standard secondary surface
<Card background={1} variant="outlined" />  // Standard card
```

### Default Paper variant is "outlined" (PierceDesk theme override)

### IconifyIcon
```jsx
import IconifyIcon from 'components/base/IconifyIcon';
<IconifyIcon icon="material-symbols-light:edit" />
```

---

## MUI MCP Server (ALWAYS USE)

| Tool | When to Use |
|------|-------------|
| `mcp__mui-mcp__get_component_info` | Verify props and v7 syntax before using a component |
| `mcp__mui-mcp__search_components` | Find the right component for a use case |
| `mcp__mui-mcp__get_customization_guide` | sx prop, theming, breakpoints |
| `mcp__mui-mcp__get_mui_guide` | General best practices |

**Always cross-reference MUI MCP with PierceDesk patterns. PierceDesk patterns take precedence.**

---

## Process Checklist

1. Identify layout context (page, card, dialog, dashboard)
2. Select correct page structure template (above)
3. Choose correct surface (Paper vs Card vs Box)
4. Wrap form fields in `Grid container spacing={{ xs: 2, md: 3 }}`
5. Each field in `Grid size={{ xs: 12, md: X }}` where X = column width
6. Add `fullWidth` to every TextField, Select, Autocomplete, DatePicker
7. Use Stack only for vertical spacing between major sections
8. Self-review against anti-pattern list
9. Test at mobile and desktop breakpoints

---

## References

- [mui-component-guide.md](references/mui-component-guide.md) - Full decision trees, all patterns, exemplar files
- [layout-patterns.md](references/layout-patterns.md) - Common layout patterns
- [form-dialog-patterns.md](references/form-dialog-patterns.md) - Dialog form examples
- [component-docs-map.md](references/component-docs-map.md) - Component docs file map
- `src/docs/component-docs/` - Live code examples (CardDoc, PaperDoc, BoxDoc, GridDoc, StackDoc)
