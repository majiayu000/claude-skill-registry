---
name: ui-designer
description: UI/UX design skill for creating wireframes, interactive HTML mockups, design specifications, and component patterns using Material UI (primary) and Tailwind CSS (secondary). Use when designing user interfaces, creating mockups for review, documenting design specs, or collaborating with frontend developers on implementation.
---

# UI Designer

## Design Workflow

```
1. Understand Requirements → 2. Wireframes → 3. Mockups → 4. Specs → 5. Handoff
```

| Phase | Deliverable | Tool |
|-------|-------------|------|
| Wireframes | Low-fi layouts | HTML skeleton |
| Mockups | Interactive prototype | Standalone HTML or Next.js |
| Specs | Developer documentation | Markdown + code snippets |
| Components | Reusable patterns | MUI + Tailwind code |

## Deliverable Types

### 1. Wireframes (Low-Fidelity)

Use for: Early exploration, layout decisions, user flow validation

```html
<!-- wireframe.html - Simple box model wireframe -->
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    .wireframe-box {
      background: #f0f0f0;
      border: 2px dashed #999;
      min-height: 40px;
    }
  </style>
</head>
<body class="p-8">
  <div class="max-w-4xl mx-auto space-y-4">
    <!-- Header -->
    <div class="wireframe-box h-16 flex items-center px-4">
      <span class="text-gray-500">[Logo] [Nav Item] [Nav Item] [Avatar]</span>
    </div>

    <!-- Main Content -->
    <div class="flex gap-4">
      <div class="wireframe-box w-64 p-4">
        <span class="text-gray-500">[Sidebar Nav]</span>
      </div>
      <div class="wireframe-box flex-1 p-4 space-y-4">
        <div class="wireframe-box h-12">[Page Title + Actions]</div>
        <div class="wireframe-box h-64">[Data Table / Content Area]</div>
      </div>
    </div>
  </div>
</body>
</html>
```

### 2. Interactive Mockups (High-Fidelity)

**Format Selection:**
- **Standalone HTML** - Single page, simple interactions, quick review
- **Next.js preview** - Multi-page flows, complex state, form interactions

See [assets/mockup-template.html](assets/mockup-template.html) for standalone template.

```html
<!-- mockup.html - High-fidelity with MUI -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard Mockup</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto:wght@400;500;700&display=swap">
  <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
  <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://unpkg.com/@mui/material@5/umd/material-ui.development.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body>
  <div id="root"></div>
  <script type="text/babel">
    const { AppBar, Toolbar, Typography, Button, Card, CardContent, Grid, Box } = MaterialUI;

    function DashboardMockup() {
      return (
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static">
            <Toolbar>
              <Typography variant="h6" sx={{ flexGrow: 1 }}>
                Dashboard
              </Typography>
              <Button color="inherit">Profile</Button>
            </Toolbar>
          </AppBar>

          <Box sx={{ p: 3 }}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      Total Users
                    </Typography>
                    <Typography variant="h4">1,234</Typography>
                  </CardContent>
                </Card>
              </Grid>
              {/* More cards... */}
            </Grid>
          </Box>
        </Box>
      );
    }

    ReactDOM.render(<DashboardMockup />, document.getElementById('root'));
  </script>
</body>
</html>
```

### 3. Design Specifications

Document for developers with exact values:

```markdown
## Component: User Card

### Structure
┌─────────────────────────────────────┐
│ [Avatar]  User Name                  │
│           user@email.com             │
│           ─────────────────────────  │
│           Role: Admin                │
│           Status: ● Active           │
│                          [Edit] [···]│
└─────────────────────────────────────┘

### Spacing
- Card padding: 16px (--spacing-4)
- Avatar margin-right: 12px (--spacing-3)
- Section gap: 8px (--spacing-2)

### Typography
- Name: H6 (14px/600)
- Email: Body2 (14px/400, text.secondary)
- Role/Status: Caption (12px/400)

### Colors
- Background: surface.main (#fff)
- Border: 1px solid divider (#e0e0e0)
- Active indicator: success.main (#2e7d32)

### Implementation
```tsx
<Card sx={{ p: 2, border: 1, borderColor: 'divider' }}>
  <Box sx={{ display: 'flex', gap: 1.5 }}>
    <Avatar src={user.avatar} />
    <Box sx={{ flex: 1 }}>
      <Typography variant="h6">{user.name}</Typography>
      <Typography variant="body2" color="text.secondary">
        {user.email}
      </Typography>
    </Box>
  </Box>
</Card>
```
```

## Design System (MUI Defaults)

### Color Palette

```tsx
// Primary colors
primary.main:    #1976d2  // Buttons, links, active states
primary.light:   #42a5f5  // Hover states
primary.dark:    #1565c0  // Pressed states
primary.contrastText: #fff

// Secondary colors
secondary.main:  #9c27b0  // Accent elements
secondary.light: #ba68c8
secondary.dark:  #7b1fa2

// Semantic colors
error.main:      #d32f2f  // Errors, destructive actions
warning.main:    #ed6c02  // Warnings
success.main:    #2e7d32  // Success states
info.main:       #0288d1  // Informational

// Surface colors
background.default: #fafafa
background.paper:   #fff
text.primary:       rgba(0,0,0,0.87)
text.secondary:     rgba(0,0,0,0.6)
divider:            rgba(0,0,0,0.12)
```

### Typography Scale

| Variant | Size | Weight | Line Height | Use |
|---------|------|--------|-------------|-----|
| h1 | 2.5rem (40px) | 700 | 1.2 | Page titles |
| h2 | 2rem (32px) | 700 | 1.3 | Section headers |
| h3 | 1.75rem (28px) | 600 | 1.3 | Subsections |
| h4 | 1.5rem (24px) | 600 | 1.4 | Card titles |
| h5 | 1.25rem (20px) | 600 | 1.4 | Dialog titles |
| h6 | 1rem (16px) | 600 | 1.5 | Component headers |
| body1 | 1rem (16px) | 400 | 1.5 | Primary text |
| body2 | 0.875rem (14px) | 400 | 1.43 | Secondary text |
| caption | 0.75rem (12px) | 400 | 1.5 | Labels, hints |
| button | 0.875rem (14px) | 500 | 1.75 | Button text |

### Spacing Scale

```tsx
// MUI spacing unit = 8px
spacing(0.5) = 4px   // Tight gaps
spacing(1)   = 8px   // Default gap
spacing(1.5) = 12px  // Comfortable gap
spacing(2)   = 16px  // Section padding
spacing(3)   = 24px  // Card padding
spacing(4)   = 32px  // Container padding
spacing(5)   = 40px  // Large gaps
spacing(6)   = 48px  // Section margins
spacing(8)   = 64px  // Page margins
```

### Component Patterns

See [references/components.md](references/components.md) for detailed patterns.

#### Buttons

```tsx
// Primary action
<Button variant="contained" color="primary">
  Save Changes
</Button>

// Secondary action
<Button variant="outlined">
  Cancel
</Button>

// Tertiary/Text action
<Button variant="text">
  Learn More
</Button>

// Destructive action
<Button variant="contained" color="error">
  Delete
</Button>

// With icon
<Button variant="contained" startIcon={<AddIcon />}>
  Add Item
</Button>
```

#### Form Controls

```tsx
// Text field
<TextField
  label="Email"
  type="email"
  helperText="We'll never share your email"
  fullWidth
/>

// Select
<FormControl fullWidth>
  <InputLabel>Role</InputLabel>
  <Select value={role} label="Role">
    <MenuItem value="admin">Admin</MenuItem>
    <MenuItem value="user">User</MenuItem>
  </Select>
</FormControl>

// Checkbox
<FormControlLabel
  control={<Checkbox defaultChecked />}
  label="I agree to terms"
/>
```

## Common Layout Patterns

### Dashboard Layout

```tsx
<Box sx={{ display: 'flex', minHeight: '100vh' }}>
  {/* Sidebar */}
  <Box sx={{ width: 240, flexShrink: 0 }}>
    <Sidebar />
  </Box>

  {/* Main content */}
  <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
    <Header />
    <Box component="main" sx={{ flexGrow: 1, p: 3, bgcolor: 'grey.100' }}>
      {children}
    </Box>
  </Box>
</Box>
```

### Form Layout

```tsx
<Box component="form" sx={{ maxWidth: 600, mx: 'auto', p: 3 }}>
  <Typography variant="h5" sx={{ mb: 3 }}>
    Create Account
  </Typography>

  <Stack spacing={2}>
    <TextField label="Full Name" fullWidth required />
    <TextField label="Email" type="email" fullWidth required />
    <TextField label="Password" type="password" fullWidth required />

    <Box sx={{ display: 'flex', gap: 1, justifyContent: 'flex-end', mt: 2 }}>
      <Button variant="outlined">Cancel</Button>
      <Button variant="contained" type="submit">Create</Button>
    </Box>
  </Stack>
</Box>
```

### Card Grid

```tsx
<Grid container spacing={3}>
  {items.map((item) => (
    <Grid item xs={12} sm={6} md={4} key={item.id}>
      <Card>
        <CardMedia
          component="img"
          height="140"
          image={item.image}
        />
        <CardContent>
          <Typography variant="h6">{item.title}</Typography>
          <Typography variant="body2" color="text.secondary">
            {item.description}
          </Typography>
        </CardContent>
        <CardActions>
          <Button size="small">View</Button>
          <Button size="small">Edit</Button>
        </CardActions>
      </Card>
    </Grid>
  ))}
</Grid>
```

## Developer Handoff Checklist

When handing off designs to frontend developers:

- [ ] All colors from MUI theme or documented custom values
- [ ] Typography variants specified (h1-h6, body1, body2, caption)
- [ ] Spacing using MUI spacing scale (0.5, 1, 2, 3, 4...)
- [ ] Responsive breakpoints noted (xs, sm, md, lg, xl)
- [ ] Interactive states shown (hover, focus, disabled, loading)
- [ ] Component code snippet provided
- [ ] Edge cases documented (empty states, error states, long text)

## References

- **Component Patterns**: See [references/components.md](references/components.md) for detailed MUI component examples
- **Page Templates**: See [references/templates.md](references/templates.md) for common page layouts
- **Tailwind Integration**: See [references/tailwind-mui.md](references/tailwind-mui.md) for combining both systems

## Assets

- **Mockup Template**: Use [assets/mockup-template.html](assets/mockup-template.html) as starting point for standalone HTML mockups
