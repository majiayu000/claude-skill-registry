---
name: color-system-designer
description: Creates color palettes and color systems for applications. Defines primary, secondary, neutral colors, and semantic colors (success, error, warning, info). Ensures accessibility compliance and provides usage guidelines.
---

# Color System Designer Skill

## Instructions

1. Analyze color requirements from task
2. Check for existing color system or brand colors
3. Create color palette (primary, secondary, neutrals, semantic)
4. Define color variations (light, dark, shades, tints)
5. Ensure accessibility compliance (contrast ratios)
6. Provide usage guidelines
7. Return structured color system specifications with:
   - Color palette (hex/rgb values)
   - Color variations and shades
   - Usage guidelines
   - Accessibility compliance
   - Design tokens format

## Examples

**Input:** "Create color system for application"
**Output:**
```markdown
### Color System

**Primary Colors:**
- Primary: #007bff (blue)
- Primary Dark: #0056b3
- Primary Light: #66b3ff
- Primary Lighter: #cce6ff

**Secondary Colors:**
- Secondary: #6c757d (gray)
- Secondary Dark: #545b62
- Secondary Light: #adb5bd

**Neutral Colors:**
- White: #ffffff
- Gray 100: #f8f9fa
- Gray 200: #e9ecef
- Gray 300: #dee2e6
- Gray 400: #ced4da
- Gray 500: #adb5bd
- Gray 600: #6c757d
- Gray 700: #495057
- Gray 800: #343a40
- Gray 900: #212529
- Black: #000000

**Semantic Colors:**
- Success: #28a745 (green)
- Error: #dc3545 (red)
- Warning: #ffc107 (yellow)
- Info: #17a2b8 (cyan)

**Accessibility:**
- All text colors meet WCAG AA (4.5:1 contrast)
- Primary on white: 4.5:1 ✓
- White on primary: 4.5:1 ✓
- Error text on white: 4.5:1 ✓

**Usage Guidelines:**
- Primary: Main actions, links, important elements
- Secondary: Secondary actions, less important elements
- Success: Success messages, positive feedback
- Error: Error messages, destructive actions
- Warning: Warning messages, caution
- Info: Informational messages
```

## Color System Components

- **Primary Colors**: Main brand/application colors
- **Secondary Colors**: Supporting colors
- **Neutral Colors**: Grays, whites, blacks for text and backgrounds
- **Semantic Colors**: Success, error, warning, info
- **Accent Colors**: Additional colors for variety
- **Background Colors**: Page and section backgrounds
- **Text Colors**: Primary and secondary text colors
- **Border Colors**: Border and divider colors

## Accessibility Requirements

- **Text Contrast**: Minimum 4.5:1 for normal text (WCAG AA)
- **Large Text Contrast**: Minimum 3:1 for large text (WCAG AA)
- **UI Components**: Minimum 3:1 for UI components
- **Focus Indicators**: High contrast focus colors
- **Error States**: Clear, high-contrast error colors

## Design Token Format

Provide colors in design token format:
```markdown
**Design Tokens:**
- `color.primary`: #007bff
- `color.primary.dark`: #0056b3
- `color.text.primary`: #212529
- `color.text.secondary`: #6c757d
- `color.background`: #ffffff
- `color.border`: #dee2e6
```
