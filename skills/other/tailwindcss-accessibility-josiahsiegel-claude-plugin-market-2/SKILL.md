---
name: tailwindcss-accessibility
description: Tailwind CSS accessibility patterns including WCAG 2.2 compliance, touch targets, focus management, and ARIA support
---

# Tailwind CSS Accessibility Patterns (WCAG 2.2 - 2025/2026)

## WCAG 2.2 Overview (Current Standard)

WCAG 2.2 was released October 2023 and is the current W3C standard. Key additions relevant to Tailwind:

- **2.5.8 Target Size (Level AA)**: 24x24 CSS pixels minimum, 44x44 recommended
- **2.4.11 Focus Not Obscured**: Focus indicators must be visible
- **2.4.13 Focus Appearance**: Enhanced focus indicator requirements
- **3.3.7 Redundant Entry**: Don't require re-entering information
- **3.2.6 Consistent Help**: Help mechanisms in consistent locations

## Focus Management

### Focus Ring Utilities

```html
<!-- Default focus ring -->
<button class="focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2">
  Button
</button>

<!-- Focus-visible for keyboard users only -->
<button class="focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500">
  Only shows ring for keyboard focus
</button>

<!-- Focus-within for parent containers -->
<div class="focus-within:ring-2 focus-within:ring-brand-500 rounded-lg p-1">
  <input type="text" class="border-none focus:outline-none" />
</div>

<!-- Custom focus ring component -->
```

```css
@layer components {
  .focus-ring {
    @apply focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2;
  }

  .focus-ring-inset {
    @apply focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-inset;
  }
}
```

### Skip Links

```html
<!-- Skip to main content -->
<a
  href="#main-content"
  class="
    sr-only focus:not-sr-only
    focus:absolute focus:top-4 focus:left-4 focus:z-50
    focus:bg-white focus:px-4 focus:py-2 focus:rounded-md focus:shadow-lg
    focus:ring-2 focus:ring-brand-500
  "
>
  Skip to main content
</a>

<header>Navigation...</header>
<main id="main-content" tabindex="-1">
  Main content
</main>
```

### Focus Trap Pattern

```html
<!-- Modal with focus management -->
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  class="fixed inset-0 z-50 flex items-center justify-center"
>
  <div class="fixed inset-0 bg-black/50" aria-hidden="true"></div>
  <div
    class="relative bg-white rounded-xl p-6 max-w-md w-full"
    role="document"
  >
    <h2 id="modal-title" class="text-lg font-semibold">Modal Title</h2>
    <p>Modal content</p>
    <button class="focus-ring">Close</button>
  </div>
</div>
```

## Screen Reader Utilities

### Visually Hidden Content

```html
<!-- Hidden visually but available to screen readers -->
<span class="sr-only">Additional context for screen readers</span>

<!-- Show on focus (skip links) -->
<a href="#main" class="sr-only focus:not-sr-only">Skip to main</a>

<!-- Icon with accessible label -->
<button>
  <svg aria-hidden="true">...</svg>
  <span class="sr-only">Close menu</span>
</button>

<!-- Form labels -->
<label>
  <span class="sr-only">Search</span>
  <input type="search" placeholder="Search..." />
</label>
```

### Announcing Dynamic Content

```html
<!-- Live region for announcements -->
<div
  role="status"
  aria-live="polite"
  aria-atomic="true"
  class="sr-only"
>
  <!-- Dynamic content announced to screen readers -->
  3 items added to cart
</div>

<!-- Alert for important messages -->
<div
  role="alert"
  aria-live="assertive"
  class="bg-red-100 text-red-800 p-4 rounded-lg"
>
  Error: Please correct the form
</div>
```

## Color Contrast

### High Contrast Patterns

```html
<!-- Ensure sufficient contrast -->
<p class="text-gray-700 bg-white">4.5:1 contrast ratio</p>
<p class="text-gray-500 bg-white">May not meet WCAG AA (3:1 min for large text)</p>

<!-- Large text (18pt+) needs 3:1 -->
<h1 class="text-4xl text-gray-600 bg-white">Large text - 3:1 ratio OK</h1>

<!-- Interactive elements need 3:1 against adjacent colors -->
<button class="
  bg-brand-500 text-white
  border-2 border-brand-500
  focus:ring-2 focus:ring-brand-500 focus:ring-offset-2
">
  Accessible Button
</button>
```

### Dark Mode Contrast

```html
<!-- Maintain contrast in both modes -->
<p class="text-gray-900 dark:text-gray-100">
  High contrast text
</p>

<p class="text-gray-600 dark:text-gray-400">
  Secondary text with adequate contrast
</p>

<!-- Avoid low contrast combinations -->
<p class="text-gray-400 dark:text-gray-600">
  ⚠️ May have contrast issues in dark mode
</p>
```

### Focus Indicator Contrast

```css
@theme {
  /* High contrast focus ring */
  --color-focus: oklch(0.55 0.25 250);
  --color-focus-offset: oklch(1 0 0);
}
```

```html
<button class="
  focus:outline-none
  focus-visible:ring-2
  focus-visible:ring-[var(--color-focus)]
  focus-visible:ring-offset-2
  focus-visible:ring-offset-[var(--color-focus-offset)]
">
  High contrast focus
</button>
```

## Motion and Animation

### Reduced Motion

```html
<!-- Respect user's motion preferences -->
<div class="
  animate-bounce
  motion-reduce:animate-none
">
  Bouncing element (static for motion-sensitive users)
</div>

<!-- Safer alternative animations -->
<div class="
  transition-opacity duration-300
  motion-reduce:transition-none
">
  Fades in (instant for motion-sensitive)
</div>

<!-- Use opacity instead of movement -->
<div class="
  transition-all
  hover:scale-105 hover:shadow-lg
  motion-reduce:hover:scale-100 motion-reduce:hover:shadow-md
">
  Scales on hover (shadow only for motion-sensitive)
</div>
```

### Safe Animation Patterns

```css
@layer components {
  /* Animations that respect reduced motion */
  .animate-fade-in {
    @apply animate-in fade-in duration-300;
    @apply motion-reduce:animate-none motion-reduce:opacity-100;
  }

  .animate-slide-up {
    @apply animate-in slide-in-from-bottom-4 duration-300;
    @apply motion-reduce:animate-none motion-reduce:translate-y-0;
  }
}
```

### Pause Animation on Hover

```html
<!-- Allow users to pause animations -->
<div class="
  animate-spin
  hover:animate-pause
  motion-reduce:animate-none
">
  Loading spinner
</div>
```

## Form Accessibility

### Accessible Form Fields

```html
<div class="space-y-4">
  <!-- Text input with label -->
  <div>
    <label for="email" class="block text-sm font-medium text-gray-700">
      Email address
      <span class="text-red-500" aria-hidden="true">*</span>
    </label>
    <input
      type="email"
      id="email"
      name="email"
      required
      aria-required="true"
      aria-describedby="email-hint email-error"
      class="
        mt-1 block w-full rounded-md border-gray-300
        focus:border-brand-500 focus:ring-brand-500
        aria-invalid:border-red-500 aria-invalid:ring-red-500
      "
    />
    <p id="email-hint" class="mt-1 text-sm text-gray-500">
      We'll never share your email
    </p>
    <p id="email-error" class="mt-1 text-sm text-red-600 hidden" role="alert">
      Please enter a valid email
    </p>
  </div>

  <!-- Checkbox with accessible label -->
  <div class="flex items-start gap-3">
    <input
      type="checkbox"
      id="terms"
      name="terms"
      class="
        h-4 w-4 rounded border-gray-300 text-brand-500
        focus:ring-brand-500
      "
    />
    <label for="terms" class="text-sm text-gray-700">
      I agree to the
      <a href="/terms" class="text-brand-500 underline">terms and conditions</a>
    </label>
  </div>

  <!-- Radio group -->
  <fieldset>
    <legend class="text-sm font-medium text-gray-700">Notification preference</legend>
    <div class="mt-2 space-y-2">
      <div class="flex items-center gap-3">
        <input type="radio" id="email-pref" name="notification" value="email" class="h-4 w-4" />
        <label for="email-pref">Email</label>
      </div>
      <div class="flex items-center gap-3">
        <input type="radio" id="sms-pref" name="notification" value="sms" class="h-4 w-4" />
        <label for="sms-pref">SMS</label>
      </div>
    </div>
  </fieldset>
</div>
```

### Error States

```html
<!-- Input with error -->
<div>
  <label for="password" class="block text-sm font-medium text-gray-700">
    Password
  </label>
  <input
    type="password"
    id="password"
    aria-invalid="true"
    aria-describedby="password-error"
    class="
      mt-1 block w-full rounded-md
      border-red-500 text-red-900
      focus:border-red-500 focus:ring-red-500
    "
  />
  <p id="password-error" class="mt-1 text-sm text-red-600" role="alert">
    <span class="sr-only">Error:</span>
    Password must be at least 8 characters
  </p>
</div>
```

### Form Validation Feedback

```css
/* Style based on aria-invalid attribute */
@custom-variant aria-invalid (&[aria-invalid="true"]);
```

```html
<input
  class="
    border-gray-300
    aria-invalid:border-red-500
    aria-invalid:text-red-900
    aria-invalid:focus:ring-red-500
  "
  aria-invalid="true"
/>
```

## Interactive Components

### Accessible Buttons

```html
<!-- Button with loading state -->
<button
  type="submit"
  aria-busy="true"
  aria-disabled="true"
  class="
    relative
    aria-busy:cursor-wait
    aria-disabled:opacity-50 aria-disabled:cursor-not-allowed
  "
>
  <span class="aria-busy:invisible">Submit</span>
  <span class="absolute inset-0 flex items-center justify-center aria-busy:visible invisible">
    <svg class="animate-spin h-5 w-5" aria-hidden="true">...</svg>
    <span class="sr-only">Loading...</span>
  </span>
</button>

<!-- Icon button -->
<button
  type="button"
  aria-label="Close dialog"
  class="rounded-full p-2 hover:bg-gray-100 focus-ring"
>
  <svg aria-hidden="true" class="h-5 w-5">...</svg>
</button>

<!-- Toggle button -->
<button
  type="button"
  aria-pressed="false"
  class="
    px-4 py-2 rounded-lg border
    aria-pressed:bg-brand-500 aria-pressed:text-white aria-pressed:border-brand-500
  "
>
  <span class="sr-only">Toggle feature</span>
  Feature
</button>
```

### Accessible Dropdowns

```html
<div class="relative">
  <button
    type="button"
    aria-haspopup="menu"
    aria-expanded="false"
    aria-controls="dropdown-menu"
    class="flex items-center gap-2 px-4 py-2 rounded-lg border focus-ring"
  >
    Options
    <svg aria-hidden="true" class="h-4 w-4">...</svg>
  </button>

  <ul
    id="dropdown-menu"
    role="menu"
    aria-labelledby="dropdown-button"
    class="
      absolute top-full mt-1 w-48 rounded-lg bg-white shadow-lg border
      hidden aria-expanded:block
    "
  >
    <li role="none">
      <a
        href="#"
        role="menuitem"
        tabindex="-1"
        class="block px-4 py-2 hover:bg-gray-100 focus:bg-gray-100 focus:outline-none"
      >
        Edit
      </a>
    </li>
    <li role="none">
      <a
        href="#"
        role="menuitem"
        tabindex="-1"
        class="block px-4 py-2 hover:bg-gray-100 focus:bg-gray-100 focus:outline-none"
      >
        Delete
      </a>
    </li>
  </ul>
</div>
```

### Accessible Tabs

```html
<div>
  <div role="tablist" aria-label="Account settings" class="flex border-b">
    <button
      role="tab"
      aria-selected="true"
      aria-controls="panel-1"
      id="tab-1"
      class="
        px-4 py-2 border-b-2
        aria-selected:border-brand-500 aria-selected:text-brand-500
        hover:text-gray-700
        focus-visible:ring-2 focus-visible:ring-inset
      "
    >
      Profile
    </button>
    <button
      role="tab"
      aria-selected="false"
      aria-controls="panel-2"
      id="tab-2"
      tabindex="-1"
      class="px-4 py-2 border-b-2 border-transparent"
    >
      Settings
    </button>
  </div>

  <div
    role="tabpanel"
    id="panel-1"
    aria-labelledby="tab-1"
    tabindex="0"
    class="p-4 focus:outline-none focus-visible:ring-2 focus-visible:ring-inset"
  >
    Profile content
  </div>

  <div
    role="tabpanel"
    id="panel-2"
    aria-labelledby="tab-2"
    tabindex="0"
    hidden
    class="p-4"
  >
    Settings content
  </div>
</div>
```

## Touch Targets (WCAG 2.2 - Critical for 2025/2026)

### WCAG 2.2 Target Size Requirements

| Level | Requirement | Tailwind Class |
|-------|-------------|----------------|
| **AA (2.5.8)** | 24x24 CSS pixels minimum | `min-h-6 min-w-6` |
| **Recommended** | 44x44 CSS pixels | `min-h-11 min-w-11` |
| **AAA (2.5.5)** | 44x44 CSS pixels | `min-h-11 min-w-11` |
| **Optimal** | 48x48 CSS pixels | `min-h-12 min-w-12` |

Platform guidelines comparison:
- **Apple iOS**: 44x44 points minimum
- **Google Android**: 48x48 dp minimum
- **Microsoft Fluent**: 44x44 pixels minimum

### Minimum Touch Target Size

```html
<!-- WCAG 2.2 Level AA minimum (24px) -->
<button class="min-h-6 min-w-6 p-1">
  <svg class="h-4 w-4">...</svg>
</button>

<!-- Recommended size (44px) - preferred for mobile -->
<button class="min-h-11 min-w-11 p-2.5">
  <svg class="h-6 w-6" aria-hidden="true">...</svg>
  <span class="sr-only">Action</span>
</button>

<!-- Optimal for primary actions (48px) -->
<button class="min-h-12 min-w-12 px-6 py-3 text-base font-medium">
  Primary Action
</button>
```

### Extend Touch Target Beyond Visible Element

```html
<!-- Small visible link with extended tap area -->
<a href="#" class="relative inline-block text-sm">
  Small Link Text
  <span class="absolute -inset-3" aria-hidden="true"></span>
</a>

<!-- Icon button with extended target -->
<button class="relative p-2 -m-2 rounded-lg hover:bg-gray-100">
  <svg class="h-5 w-5" aria-hidden="true">...</svg>
  <span class="sr-only">Close menu</span>
</button>

<!-- Card with full-surface tap target -->
<article class="relative p-4 rounded-lg border hover:shadow-md">
  <h3>Card Title</h3>
  <p>Description text</p>
  <a href="/details" class="after:absolute after:inset-0">
    <span class="sr-only">View details</span>
  </a>
</article>
```

### Spacing Between Interactive Elements

WCAG 2.2 requires 24px spacing OR targets must be 24px minimum:

```html
<!-- Adequate spacing between touch targets (12px gap minimum) -->
<div class="flex gap-3">
  <button class="min-h-11 px-4 py-2">Button 1</button>
  <button class="min-h-11 px-4 py-2">Button 2</button>
</div>

<!-- Stacked links with adequate height and spacing -->
<nav class="flex flex-col">
  <a href="#" class="py-3 px-4 min-h-11 border-b border-gray-100">Link 1</a>
  <a href="#" class="py-3 px-4 min-h-11 border-b border-gray-100">Link 2</a>
  <a href="#" class="py-3 px-4 min-h-11">Link 3</a>
</nav>

<!-- Button group with safe spacing -->
<div class="flex flex-wrap gap-3">
  <button class="min-h-11 px-4 py-2 border rounded-lg">Cancel</button>
  <button class="min-h-11 px-4 py-2 bg-blue-600 text-white rounded-lg">Confirm</button>
</div>
```

### Touch Target Exceptions (WCAG 2.2)

Targets can be smaller than 24x24 if:
- Inline text links within sentences
- Browser-provided controls (scrollbars)
- Size is essential to information
- A larger equivalent target exists on same page

## Text Accessibility

### Readable Text

```html
<!-- Adequate line height for body text -->
<p class="leading-relaxed">
  Long form content with comfortable line height
</p>

<!-- Limit line length for readability -->
<article class="max-w-prose">
  <p class="leading-relaxed">
    Content with optimal line length (45-75 characters)
  </p>
</article>

<!-- Adequate paragraph spacing -->
<div class="space-y-6">
  <p>Paragraph 1</p>
  <p>Paragraph 2</p>
</div>
```

### Text Resizing

```html
<!-- Use relative units for text -->
<p class="text-base">Scales with user's font size preferences</p>

<!-- Don't use fixed pixel values for text -->
<p class="text-[14px]">⚠️ Won't scale with browser zoom</p>

<!-- Container that doesn't break on text zoom -->
<div class="min-h-[auto]">
  Content height adjusts with text size
</div>
```

## Semantic HTML with Tailwind

### Landmark Regions

```html
<body class="min-h-screen flex flex-col">
  <header class="sticky top-0 bg-white shadow z-50">
    <nav aria-label="Main navigation">...</nav>
  </header>

  <main id="main-content" class="flex-1">
    <article>
      <h1>Page Title</h1>
      <section aria-labelledby="section-1">
        <h2 id="section-1">Section Title</h2>
        <p>Content...</p>
      </section>
    </article>

    <aside aria-label="Related content" class="hidden lg:block">
      Sidebar content
    </aside>
  </main>

  <footer class="bg-gray-800 text-white">
    <nav aria-label="Footer navigation">...</nav>
  </footer>
</body>
```

### Heading Hierarchy

```html
<article class="prose">
  <h1 class="text-4xl font-bold">Main Title (H1)</h1>

  <section>
    <h2 class="text-2xl font-semibold">Section (H2)</h2>

    <section>
      <h3 class="text-xl font-medium">Subsection (H3)</h3>
      <p>Content...</p>
    </section>
  </section>
</article>
```

## Testing Accessibility

### Browser DevTools Checklist

1. **Color contrast**: Use contrast checker
2. **Focus order**: Tab through the page
3. **Zoom**: Test at 200% zoom
4. **Reduced motion**: Enable in OS settings

### Automated Testing

```javascript
// axe-core integration
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('component is accessible', async () => {
  const { container } = render(<Component />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

## Best Practices Summary (WCAG 2.2 - 2025/2026)

| Pattern | Implementation | WCAG Level |
|---------|---------------|------------|
| Focus visible | `focus-visible:ring-2 focus-visible:ring-offset-2` | 2.4.7 (AA) |
| Screen reader only | `sr-only` | 1.3.1 (A) |
| Skip links | `sr-only focus:not-sr-only focus:absolute` | 2.4.1 (A) |
| Reduced motion | `motion-reduce:animate-none motion-reduce:transition-none` | 2.3.3 (AAA) |
| Touch targets (min) | `min-h-6 min-w-6` (24px) | 2.5.8 (AA) |
| Touch targets (rec) | `min-h-11 min-w-11` (44px) | 2.5.5 (AAA) |
| Touch spacing | `gap-3` (12px minimum between targets) | 2.5.8 (AA) |
| Text contrast | 4.5:1 for normal, 3:1 for large text | 1.4.3 (AA) |
| Form errors | `aria-invalid="true"` + `role="alert"` | 3.3.1 (A) |
| Focus not obscured | Avoid `z-index` covering focused elements | 2.4.11 (AA) |

### Quick Reference: Touch-Friendly Component

```html
<!-- Accessible, touch-friendly button component -->
<button
  type="button"
  class="
    /* Touch target size (44px minimum) */
    min-h-11 min-w-11 px-4 py-2.5

    /* Typography */
    text-sm md:text-base font-medium

    /* Colors with sufficient contrast */
    bg-blue-600 text-white
    hover:bg-blue-700

    /* Focus indicator (visible, not obscured) */
    focus:outline-none
    focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2

    /* Shape */
    rounded-lg

    /* Disabled state */
    disabled:opacity-50 disabled:cursor-not-allowed

    /* Respect motion preferences */
    transition-colors motion-reduce:transition-none
  "
>
  Button Text
</button>
```
