---
name: theme-consistency
description: Enforce consistent theming across all prototype mockup screens. Auto-loads theme.yaml, validates CSS variable usage, prevents hardcoded values, and maintains visual consistency session-to-session. Use during /prototype create when generating new screens.
---

<objective>
The theme-consistency skill ensures all prototype screens share a unified visual design by:

1. Loading and enforcing theme.yaml values during mockup generation
2. Preventing hardcoded colors, spacing, and typography values
3. Validating new screens match established patterns
4. Locking theme after first screen approval to ensure session-to-session consistency

This prevents the common problem where screens created in different sessions drift in style, creating an inconsistent prototype that undermines the design intent.
</objective>

<quick_start>
<when_to_invoke>
Automatically invoke this skill when:
- `/prototype create [screen]` is called and theme.yaml exists
- Generating HTML mockup content for any screen
- User requests a new prototype screen in any session

Do NOT invoke when:
- Creating the very first screen (theme not yet established)
- User explicitly requests to reset/modify theme
</when_to_invoke>

<basic_workflow>
1. **Load Theme** - Read `design/prototype/theme.yaml`
2. **Check Lock Status** - If `locked: true`, enforce; if `false`, may update
3. **Load Context** - Get app_type, core_goal, layout, tone, density
4. **Generate Screen** - Create HTML using theme CSS variables
5. **Validate** - Check for hardcoded values, fix violations
</basic_workflow>

<key_rules>
**NEVER use:**
- Hardcoded hex colors: `#3b82f6`, `#ffffff`
- Hardcoded RGB: `rgb(59, 130, 246)`
- Hardcoded spacing: `padding: 17px`, `margin: 32px`
- Arbitrary values: `text-[15px]`, `p-[23px]`

**ALWAYS use:**
- Theme CSS variables: `var(--color-primary)`, `var(--space-4)`
- Shared component classes: `.btn--primary`, `.card`, `.form-input`
- Density classes: `.density-compact`, `.density-spacious`
</key_rules>
</quick_start>

<detailed_procedures>
<theme_loading>
## Loading Theme Configuration

When generating any prototype screen, FIRST load the theme:

```yaml
# Read design/prototype/theme.yaml
theme:
  locked: true|false
  palette:
    primary: "oklch(55% 0.2 250)"
    # ... all colors
  typography:
    heading_font: "Inter, system-ui, sans-serif"
    # ... font settings
  spacing:
    unit: "8px"
    # ... spacing scale
  tone:
    style: "professional"  # affects content voice
    density: "comfortable" # affects spacing multipliers
```

### Lock Status Behavior

**If `locked: true`:**
- Theme is immutable
- All new screens MUST use existing theme values
- Warn if user requests theme changes
- Suggest creating new prototype instead

**If `locked: false`:**
- First screen is being created
- Theme values may be refined based on user feedback
- After user approves first mockup, set `locked: true`
</theme_loading>

<screen_generation>
## Generating Consistent Screens

### HTML Structure
Every screen MUST follow base.html structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>{{SCREEN_TITLE}} - {{APP_NAME}}</title>
  <link rel="stylesheet" href="../../theme.css">
  <link rel="stylesheet" href="../../shared.css">
  <style>/* Screen-specific overrides only */</style>
</head>
<body class="theme-{{TONE_STYLE}} density-{{DENSITY}}">
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <!-- Navigation (if applicable) -->
  <nav class="nav nav--{{LAYOUT}}">...</nav>

  <!-- Main Content -->
  <main id="main-content" class="main main--{{LAYOUT}}">
    {{SCREEN_CONTENT}}
  </main>
</body>
</html>
```

### CSS Variable Usage

| Element | Correct | Incorrect |
|---------|---------|-----------|
| Button background | `var(--color-primary)` | `#3b82f6` |
| Card padding | `var(--space-4)` | `32px` |
| Heading size | `var(--text-2xl)` | `1.953rem` |
| Border radius | `var(--radius-md)` | `8px` |
| Box shadow | `var(--shadow-md)` | `0 4px 6px rgba(...)` |
| Transition | `var(--transition-base)` | `150ms ease` |

### Component Reuse

Use shared.css classes instead of inline styles:

```html
<!-- CORRECT -->
<button class="btn btn--primary">Submit</button>
<div class="card card--elevated">...</div>
<input class="form-input" type="text">

<!-- INCORRECT -->
<button style="background: #3b82f6; padding: 8px 16px;">Submit</button>
<div style="background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">...</div>
```
</screen_generation>

<validation>
## Validation Checks

After generating screen HTML, validate:

### 1. No Hardcoded Colors
```bash
# Check for hex colors
grep -E "#[0-9a-fA-F]{3,6}" screen.html

# Check for rgb/rgba
grep -E "rgb\(|rgba\(" screen.html

# Check for hsl/hsla
grep -E "hsl\(|hsla\(" screen.html
```

### 2. No Hardcoded Spacing
```bash
# Check for pixel values not in variables
grep -E "padding:\s*\d+px" screen.html
grep -E "margin:\s*\d+px" screen.html
grep -E "gap:\s*\d+px" screen.html
```

### 3. Font Usage
```bash
# Check for hardcoded font-family
grep -E "font-family:\s*[^v]" screen.html  # Should use var()
```

### 4. Theme Variable Coverage
Ensure all visual properties use theme variables:
- Colors: `var(--color-*)`
- Spacing: `var(--space-*)`
- Typography: `var(--text-*)`, `var(--font-*)`
- Effects: `var(--shadow-*)`, `var(--radius-*)`
</validation>

<content_presentation>
## Content Presentation by Screen Type

Use context from theme.yaml to guide content structure:

### Entry/Auth Screens
- Single focus, minimal distraction
- Centered card layout
- Clear primary CTA
- Minimal navigation

### Dashboard/Overview Screens
- Scannable grid layout
- Summary cards with key metrics
- Quick action shortcuts
- Navigation hub role

### Create/Edit Screens
- Form-focused layout
- Progressive disclosure if complex
- Clear validation feedback
- Save/Cancel actions visible

### Browse/List Screens
- Table or card grid
- Search/filter bar at top
- Pagination or infinite scroll
- Quick actions per item

### Detail/View Screens
- Hero section with primary info
- Tabbed or sectioned content
- Action buttons in header
- Related items/navigation
</content_presentation>
</detailed_procedures>

<validation_output>
## Validation Report Format

After screen generation, output validation status:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THEME CONSISTENCY CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Screen: dashboard-overview.html
Theme: [APP_NAME] Theme (locked)

CHECKLIST:
✅ Uses theme.css variables
✅ Imports shared.css
✅ No hardcoded colors
✅ No hardcoded spacing
✅ Uses shared component classes
✅ Follows base.html structure
✅ Includes skip link
✅ Matches layout pattern (sidebar)
✅ Applies density setting (comfortable)

STATUS: PASS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If violations found:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THEME CONSISTENCY CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Screen: settings-form.html
Theme: [APP_NAME] Theme (locked)

VIOLATIONS FOUND:

Line 45: Hardcoded color
  Before: background: #f3f4f6;
  After:  background: var(--color-neutral-100);

Line 67: Hardcoded spacing
  Before: padding: 24px;
  After:  padding: var(--space-3);

Line 89: Missing shared class
  Before: <button style="...">
  After:  <button class="btn btn--primary">

STATUS: FAIL (3 violations)
Auto-fixing violations...
STATUS: PASS (after fixes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
</validation_output>

<references>
## Related Resources

- **Theme Template**: `.spec-flow/templates/prototype/theme.yaml`
- **CSS Variables**: `.spec-flow/templates/prototype/theme.css`
- **Base HTML**: `.spec-flow/templates/prototype/base.html`
- **Shared Styles**: `.spec-flow/templates/prototype/shared.css`
- **Design Tokens**: `docs/project/style-guide.md`
</references>
