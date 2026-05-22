---
name: design-guide
description: Ensures modern, professional UI design by providing principles for spacing, typography, colors, shadows, and interactive states. Use when building any UI component or interface with Next.js/React, Nuxt/Vue, shadcn UI, or Tailwind CSS to ensure consistent, clean, minimal design.
---

# Design Guide

This skill ensures every UI you build looks modern and professional by following proven design principles. Reference this skill whenever building any UI component.

## Core Design Principles

### 1. Clean and Minimal Layout
- Use generous white space throughout the interface
- Avoid cluttered designs - less is more
- Let content breathe with proper spacing
- Create visual hierarchy through spacing rather than decoration
- Remove unnecessary elements and decorations

### 2. Neutral Color Palette
- **Base colors**: Use grays and off-whites (not pure white) as the foundation
- **Accent color**: Choose ONE accent color and use it sparingly for emphasis
- **Avoid**: Generic purple/blue gradients - they look dated and unprofessional
- **Example palette**:
  - Background: `bg-zinc-50` or `bg-slate-50` or `bg-gray-50`
  - Text primary: `text-zinc-900` or `text-gray-900`
  - Text secondary: `text-zinc-600` or `text-gray-600`
  - Borders: `border-zinc-200` or `border-gray-200`
  - Accent: One brand color used only for CTAs and important elements
- **Bad practice**: Rainbow gradients everywhere, every element a different color

### 3. Spacing System (8px Grid)
Use consistent spacing based on an 8px grid system. In Tailwind CSS, this maps to:
- `gap-2` or `p-2` = 8px
- `gap-4` or `p-4` = 16px
- `gap-6` or `p-6` = 24px
- `gap-8` or `p-8` = 32px
- `gap-12` or `p-12` = 48px
- `gap-16` or `p-16` = 64px

**Guidelines**:
- Use these values consistently throughout your design
- Smaller spacing (8-16px) for related elements within a component
- Medium spacing (24-32px) for sections within a component
- Larger spacing (48-64px) for major layout sections and between components
- **Bad practice**: Inconsistent spacing (3px here, 17px there, 23px somewhere else)

### 4. Typography
- **Clear hierarchy**: Establish distinct heading levels with size and weight
- **Readable sizes**: Minimum 16px (`text-base`) for body text - never smaller
- **Font limit**: Use maximum 2 different fonts (one for headings, one for body)
- **Line height**: Ensure comfortable reading with `leading-relaxed` or `leading-normal`
- **Example hierarchy**:
  - H1: `text-3xl font-bold` or `text-4xl font-bold`
  - H2: `text-2xl font-semibold`
  - H3: `text-xl font-semibold`
  - Body: `text-base` (16px minimum)
  - Small: `text-sm text-zinc-600`
- **Bad practice**: Tiny unreadable text below 16px for body content

### 5. Shadows
- Use subtle shadows, not heavy or overdone effects
- **Light shadow**: `shadow-sm` for slight elevation
- **Medium shadow**: `shadow` for cards and elevated elements
- **Avoid**: `shadow-2xl`, dark shadows, or heavy drop shadows
- Cards should use either clean borders OR subtle shadows, not both
- **Bad practice**: Heavy, dark shadows that look dated

### 6. Rounded Corners
- Apply rounded corners thoughtfully - not everything needs to be rounded
- **Typical values**:
  - Buttons: `rounded-md` (6px) or `rounded-lg` (8px)
  - Cards: `rounded-lg` (8px) or `rounded-xl` (12px)
  - Small elements: `rounded` (4px)
  - Inputs: `rounded-md` (6px)
- Maintain consistency across similar element types
- Some elements (like data tables or certain layouts) look better without rounding

### 7. Interactive States
Always define clear states for all interactive elements:
- **Hover**: Subtle color change or slight elevation
- **Active/Pressed**: Slightly darker or more emphasis
- **Disabled**: Reduced opacity (`opacity-50`) and no hover effects
- **Focus**: Clear focus ring for accessibility (`focus:ring-2 focus:ring-offset-2`)
- Use smooth transitions: `transition-colors duration-150` or `transition-all duration-200`

**Bad practice**: Missing hover states, no disabled states, no focus indicators

### 8. Mobile-First Thinking
- Design for mobile viewport first, then enhance for larger screens
- Use responsive utilities: `sm:`, `md:`, `lg:`, `xl:`, `2xl:`
- Ensure touch targets are minimum 44x44px for mobile
- Test all interactive elements work well on mobile
- Stack vertically on mobile, use grid/flex on desktop

## Component Guidelines

### Buttons (Good Example)
```jsx
// Primary button - proper implementation
<button className="
  bg-zinc-900 text-white 
  px-4 py-2 
  rounded-lg 
  shadow-sm
  hover:bg-zinc-800 
  active:bg-zinc-950
  disabled:opacity-50 disabled:cursor-not-allowed
  focus:ring-2 focus:ring-offset-2 focus:ring-zinc-900
  transition-colors duration-150
">
  Click me
</button>

// Secondary button
<button className="
  bg-white text-zinc-900 
  border border-zinc-300
  px-4 py-2 
  rounded-lg 
  hover:bg-zinc-50 
  active:bg-zinc-100
  disabled:opacity-50 disabled:cursor-not-allowed
  transition-colors duration-150
">
  Secondary
</button>
```

**Key elements**:
- Subtle shadow (`shadow-sm`)
- Proper padding: `px-4 py-2` minimum
- Clear hover state with smooth transition
- NO gradients
- Disabled state defined
- Focus state for accessibility

**Bad practice**: Heavy gradients, no hover state, insufficient padding, tiny text

### Cards (Good Example)
```jsx
// Option 1: Clean borders
<div className="
  bg-white 
  border border-zinc-200 
  rounded-lg 
  p-6
">
  Card content
</div>

// Option 2: Subtle shadow (not both!)
<div className="
  bg-white 
  shadow 
  rounded-lg 
  p-6
">
  Card content
</div>
```

**Key elements**:
- Use borders OR shadows, not both
- Adequate padding: `p-6` or `p-8`
- Rounded corners: `rounded-lg` or `rounded-xl`
- White or off-white background
- Generous spacing between content

**Bad practice**: Both heavy borders AND heavy shadows, cramped content, no padding

### Forms (Good Example)
```jsx
<div className="space-y-4">
  <div>
    <label className="block text-sm font-medium text-zinc-900 mb-2">
      Email
    </label>
    <input
      type="email"
      className="
        w-full px-3 py-2 
        border border-zinc-300 rounded-md
        focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 focus:border-blue-500
        disabled:bg-zinc-100 disabled:text-zinc-400
        transition-colors
      "
      placeholder="you@example.com"
    />
  </div>
  
  <div>
    <label className="block text-sm font-medium text-zinc-900 mb-2">
      Password
    </label>
    <input
      type="password"
      className="
        w-full px-3 py-2 
        border border-zinc-300 rounded-md
        focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 focus:border-blue-500
      "
    />
    {error && (
      <p className="mt-2 text-sm text-red-600">
        {error}
      </p>
    )}
  </div>
</div>
```

**Key elements**:
- Clear labels with proper contrast and spacing
- Adequate input padding: `px-3 py-2` minimum
- Focus states with ring for accessibility
- Clear error states with proper color and spacing
- Disabled states styled appropriately
- Good spacing between fields (`space-y-4`)

**Bad practice**: No labels, cramped inputs, unclear error states, inconsistent spacing, missing focus indicators

### Navigation
```jsx
// Desktop navigation
<nav className="flex items-center gap-6">
  <a href="/" className="
    text-zinc-600 hover:text-zinc-900 
    transition-colors
  ">
    Home
  </a>
  <a href="/about" className="
    text-zinc-900 font-medium
  ">
    About
  </a>
</nav>

// Mobile navigation (hamburger menu)
<nav className="flex flex-col gap-4 p-4">
  <a href="/" className="
    text-zinc-900 py-2
    hover:text-zinc-600
  ">
    Home
  </a>
</nav>
```

**Key elements**:
- Clean, minimal design
- Clear active state indication
- Adequate spacing: `gap-4` or `gap-6`
- Mobile: Hamburger menu for space efficiency
- Smooth transitions on hover

## shadcn UI Integration

When using shadcn UI components:
- Components already follow most of these principles
- Customize the color scheme in `tailwind.config.js` to match your neutral palette
- Adjust spacing if needed to align with 8px grid
- Ensure your accent color is used consistently
- Modify default shadows if they appear too heavy
- Check that all interactive states are properly defined

## Quick Pre-Flight Checklist

Before considering any UI complete, verify:
- [ ] Generous white space used throughout, not cluttered
- [ ] Neutral grays with ONE accent color only
- [ ] Spacing follows 8px grid (8, 16, 24, 32, 48, 64px)
- [ ] Typography has clear hierarchy, minimum 16px body text
- [ ] Maximum 2 fonts used
- [ ] Shadows are subtle, not heavy
- [ ] Rounded corners used thoughtfully, not on everything
- [ ] All interactive elements have hover, active, disabled, and focus states
- [ ] Mobile-responsive with mobile-first approach
- [ ] No generic purple/blue gradients
- [ ] No rainbow gradients
- [ ] Text is readable (not too small, good contrast)
- [ ] Spacing is consistent throughout
- [ ] Cards use borders OR shadows, not both

## Common Mistakes to Avoid

### Color Mistakes
- ❌ Pure white backgrounds (`bg-white` everywhere)
- ✅ Use off-white (`bg-zinc-50`, `bg-gray-50`)
- ❌ Too many colors, rainbow gradients
- ✅ Grays + one accent color
- ❌ Generic purple/blue gradients
- ✅ Solid colors or very subtle gradients

### Spacing Mistakes
- ❌ Inconsistent spacing (3px, 17px, 23px random values)
- ✅ 8px grid system (8, 16, 24, 32, 48, 64px)
- ❌ Cramped, cluttered layouts
- ✅ Generous white space

### Typography Mistakes
- ❌ Text smaller than 16px for body content
- ✅ Minimum 16px (`text-base`) for body
- ❌ Using 5+ different fonts
- ✅ Maximum 2 fonts

### Shadow Mistakes
- ❌ Heavy, dark drop shadows
- ✅ Subtle shadows (`shadow-sm`, `shadow`)
- ❌ Cards with both heavy borders AND heavy shadows
- ✅ Borders OR shadows, not both

### Interactive State Mistakes
- ❌ No hover effects on buttons
- ✅ Clear hover, active, disabled, focus states
- ❌ Missing focus indicators (accessibility issue)
- ✅ Visible focus rings

### Mobile Mistakes
- ❌ Desktop-only design that breaks on mobile
- ✅ Mobile-first, responsive design
- ❌ Tiny touch targets (<44px)
- ✅ Minimum 44x44px touch targets

## Examples in Context

### Dashboard Card
```jsx
// Good example
<div className="bg-white border border-zinc-200 rounded-lg p-6">
  <h3 className="text-xl font-semibold text-zinc-900 mb-2">
    Revenue
  </h3>
  <p className="text-3xl font-bold text-zinc-900">
    $12,450
  </p>
  <p className="text-sm text-zinc-600 mt-2">
    +12% from last month
  </p>
</div>
```

### Feature Section
```jsx
// Good example with proper spacing
<section className="py-16 px-4">
  <div className="max-w-6xl mx-auto">
    <h2 className="text-3xl font-bold text-zinc-900 mb-4">
      Features
    </h2>
    <p className="text-base text-zinc-600 mb-12 max-w-2xl">
      Everything you need to build modern applications
    </p>
    
    <div className="grid md:grid-cols-3 gap-8">
      {/* Feature cards with 8px grid spacing */}
    </div>
  </div>
</section>
```

## When to Apply This Skill

Apply these principles for:
- Building new UI components in Next.js/React or Nuxt/Vue
- Creating pages and layouts
- Designing forms and inputs
- Building navigation menus
- Creating cards, buttons, and interactive elements
- Setting up color schemes and typography
- Implementing responsive designs
- Working with Tailwind CSS and shadcn UI

Always reference these guidelines before starting any UI work and verify against the checklist before considering the work complete.
