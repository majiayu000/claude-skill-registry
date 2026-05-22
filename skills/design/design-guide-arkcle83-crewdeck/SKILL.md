---
name: design-guide
description: Modern UI design principles and guidelines for building clean, professional interfaces. Use when creating any UI components, layouts, web pages, or interactive elements including buttons, forms, cards, navigation, or complete applications. Applies to HTML, CSS, React, Vue, Svelte, and any frontend framework. Ensures consistent, minimal, and accessible design patterns.
---

# Design Guide

## Core Philosophy

Apply modern, minimal design principles focused on clarity, consistency, and professionalism. Every UI element should serve a purpose, with intentional use of space, color, and typography.

## Design Principles

### 1. Clean and Minimal Layout

**Whitespace is essential**
- Use generous padding and margins
- Avoid cluttered interfaces
- Group related elements with clear visual separation
- Remove unnecessary decorative elements

**Visual hierarchy**
- Establish clear content priority through size and spacing
- Use whitespace to guide attention
- Limit elements per section (3-7 items optimal)

### 2. Color System

**Base palette**
- Primary background: Off-white (#FAFAFA, #F5F5F5) or pure white (#FFFFFF)
- Text colors:
  - Primary: Dark gray (#1A1A1A, #2D2D2D)
  - Secondary: Medium gray (#6B6B6B, #737373)
  - Tertiary: Light gray (#A0A0A0, #B3B3B3)
- Borders and dividers: Very light gray (#E5E5E5, #EBEBEB)

**Accent color**
- Choose ONE accent color for the entire interface
- Use sparingly for CTAs, links, and important interactive elements
- Recommended: Teal (#0D9488), Emerald (#059669), Indigo (#4F46E5), or custom brand color
- Apply to: Primary buttons, active states, key icons

**Forbidden patterns**
- No purple-blue gradients
- No rainbow or multi-color gradients
- No more than 3 colors total (base grays + one accent)
- No bright, saturated colors for large areas

### 3. Spacing System (8px Grid)

**Consistent spacing units**
- 8px: Compact spacing (icon padding, tight elements)
- 16px: Default spacing (between related elements, button padding)
- 24px: Medium spacing (section padding, card content)
- 32px: Large spacing (between sections)
- 48px: XL spacing (major section breaks)
- 64px: XXL spacing (page sections, hero spacing)

**Application**
- All margins, padding, gaps use these values exclusively
- Component dimensions follow 8px increments when possible
- Line heights: 1.5 for body, 1.2 for headings

### 4. Typography

**Font selection**
- Maximum 2 fonts: one for headings, one for body (or same for both)
- System fonts acceptable: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- Web fonts: Inter, Poppins, Work Sans, DM Sans

**Size hierarchy**
- Body text: 16px minimum (never below 14px)
- Small text: 14px (metadata, captions)
- Headings:
  - H1: 32-48px
  - H2: 24-32px
  - H3: 20-24px
  - H4: 18-20px

**Weight and style**
- Avoid excessive bold text
- Use weight variations (400, 500, 600, 700) for hierarchy
- Letter-spacing: -0.02em for large headings, 0 for body

### 5. Shadows and Depth

**Subtle elevation**
- Light shadow: `box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.06)`
- Medium shadow: `box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07), 0 2px 4px rgba(0, 0, 0, 0.05)`
- Avoid heavy, dramatic shadows

**When to use**
- Cards and modals: light to medium shadow
- Buttons: very subtle shadow on rest, slightly elevated on hover
- Dropdowns and popovers: medium shadow

### 6. Borders and Corners

**Border radius**
- Subtle rounding: 4-8px for most elements
- Medium rounding: 12-16px for cards and large containers
- Not everything needs rounding (tables, data grids can remain sharp)

**Border usage**
- Use either borders OR shadows, not both on the same element
- Thin borders: 1px solid with light gray (#E5E5E5)
- Input focus: 2px solid with accent color

### 7. Interactive States

**Required states for all interactive elements**

**Buttons**
```css
/* Default */
background: accent-color;
color: white;
padding: 12px 24px;
border-radius: 6px;
box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);

/* Hover */
background: slightly-darker-accent;
box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
transform: translateY(-1px);

/* Active */
transform: translateY(0);
box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);

/* Disabled */
background: light-gray;
color: medium-gray;
cursor: not-allowed;
opacity: 0.6;
```

**Links**
- Default: Accent color, no underline
- Hover: Underline, slightly darker
- Visited: Same as default (or slightly muted)

**Form inputs**
- Default: 1px border, light gray
- Focus: 2px border, accent color, subtle glow
- Error: Red border (#DC2626), error message below
- Disabled: Gray background, reduced opacity

### 8. Mobile-First Approach

**Responsive thinking**
- Design for mobile viewport first (320px-768px)
- Scale up to tablet (768px-1024px) and desktop (1024px+)
- Touch targets: Minimum 44x44px for buttons and interactive elements
- Stack vertically on mobile, consider horizontal on desktop

**Breakpoints**
```css
/* Mobile: base styles */
/* Tablet: 768px */
/* Desktop: 1024px */
/* Large desktop: 1440px */
```

## Component Patterns

### Buttons

**Good example**
```html
<button class="btn-primary">
  Save Changes
</button>

<style>
.btn-primary {
  background: #0D9488;
  color: white;
  padding: 12px 24px;
  border-radius: 6px;
  border: none;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.btn-primary:hover {
  background: #0F766E;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.btn-primary:disabled {
  background: #D1D5DB;
  color: #9CA3AF;
  cursor: not-allowed;
  transform: none;
}
</style>
```

**Bad example**
```css
/* Avoid */
.btn-bad {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 5px 10px; /* Too small */
  border-radius: 25px; /* Too rounded */
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.5); /* Too heavy */
  text-transform: uppercase;
  letter-spacing: 2px;
}
```

### Cards

**Good example**
```html
<div class="card">
  <h3 class="card-title">Dashboard</h3>
  <p class="card-description">View your analytics and metrics</p>
</div>

<style>
.card {
  background: white;
  border: 1px solid #E5E5E5;
  border-radius: 8px;
  padding: 24px;
  transition: border-color 0.2s ease;
}

.card:hover {
  border-color: #D1D5DB;
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #1A1A1A;
}

.card-description {
  font-size: 16px;
  color: #6B6B6B;
}
</style>
```

**Bad example**
```css
/* Avoid */
.card-bad {
  background: linear-gradient(to right, #fa709a, #fee140);
  border: 3px solid purple;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5);
  border-radius: 30px;
}
```

### Forms

**Good example**
```html
<form class="form">
  <div class="form-group">
    <label for="email">Email Address</label>
    <input type="email" id="email" placeholder="you@example.com">
    <span class="form-hint">We'll never share your email</span>
  </div>
  
  <div class="form-group">
    <label for="password">Password</label>
    <input type="password" id="password" class="error">
    <span class="form-error">Password must be at least 8 characters</span>
  </div>
</form>

<style>
.form-group {
  margin-bottom: 24px;
}

label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #2D2D2D;
  margin-bottom: 8px;
}

input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #D1D5DB;
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.2s ease;
}

input:focus {
  outline: none;
  border-color: #0D9488;
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}

input.error {
  border-color: #DC2626;
}

.form-hint {
  font-size: 14px;
  color: #6B6B6B;
  margin-top: 4px;
  display: block;
}

.form-error {
  font-size: 14px;
  color: #DC2626;
  margin-top: 4px;
  display: block;
}
</style>
```

## Anti-Patterns to Avoid

**Visual crimes**
- Rainbow gradients or multiple bright colors
- Text smaller than 14px (except in rare cases)
- Inconsistent spacing (mixing random pixel values)
- Every element in a different color
- Heavy drop shadows everywhere
- Over-animation and excessive transitions
- Centered text for long paragraphs
- Poor color contrast (text on similar-colored backgrounds)

**Structural issues**
- No clear visual hierarchy
- Cluttered layouts with no breathing room
- Missing interactive states
- Inconsistent component styling
- Mixing design patterns (e.g., outlined buttons with filled buttons randomly)

## Implementation Checklist

Before finalizing any UI component or page, verify:

- [ ] Spacing follows 8px grid system
- [ ] Maximum 3 colors used (grays + one accent)
- [ ] All text is 16px minimum (14px acceptable for metadata)
- [ ] Interactive elements have hover, active, and disabled states
- [ ] Shadows are subtle (not heavy or dramatic)
- [ ] No gradients used (unless explicitly requested)
- [ ] Typography hierarchy is clear
- [ ] Mobile viewport considered (touch targets 44px+)
- [ ] Color contrast meets accessibility standards (4.5:1 minimum)
- [ ] Consistent border radius values throughout

## When to Break These Rules

Rules can be broken with explicit user request or specific brand requirements. Document the deviation and ensure consistency in the exception.
